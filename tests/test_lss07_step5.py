"""Bounded installation gates, stdlib unittest, no network or portfolio backtest."""
from __future__ import annotations
import copy
from dataclasses import asdict, replace
from datetime import date
import gzip
import json
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch, Mock

from e1r_engine.lss07 import LSS07Config, VERSION, evaluate, observations, apply_lss07
from e1r_engine.core import E1RCoreEngine, E1RCoreEngineConfig
from e1r_engine.contracts import DailyBar, MarketSnapshot
from e1r_engine.state import AccountState, PositionState, OrderIntent, DecisionTrace, DailyEngineResult
from e1r_engine.forward_runtime import PendingOrderLedger, T1ExecutionEngine
from e1r_engine.live_engine_adapter import LiveEngineAdapter
from test_fd_m3180125_canonical_engine_entry import CanonicalEngineEntryTests

FIX = Path(__file__).parent / 'fixtures/lss07'
OBS = dict(ready=True, score=59., rank=151, score_slope=-1., rank_slope=.01, close=90., previous_close=91.)
DAY = '2026-05-15'
CFG = LSS07Config(True, DAY)


def result_for(action='HOLD'):
    p = PositionState.create('X', 7.99, 100., 90., DAY)
    a = replace(AccountState.empty(DAY, 10000.), positions={'X':p}).mark_to_market({'X':90.}, DAY)
    o = OrderIntent(DAY, 'X', action, 'SELL' if action in ('EXIT','REDUCE') else 'BUY' if action=='ADD' else None,
                    0. if action=='EXIT' else None, None, 'existing', 'UPTREND', {'origin_branch':'UPTREND'})
    tr = DecisionTrace(DAY, 'UPTREND', 'UPTREND', 'NO_SUBCLASS', {'gate_state':'ALLOW'}, 0, [], [o], [])
    return DailyEngineResult(DAY,a,a,tr,[o],[],{})


def snapshot_empty(day=DAY):
    return MarketSnapshot(day, ['X'], {}, {}, None)


class LSS07Step5Tests(unittest.TestCase):
    def test_config_rejects_implicit_activation(self):
        for args in [(True,None), ('false',None), (True,'2026-99-01')]:
            with self.assertRaises((TypeError,ValueError)): LSS07Config(*args)
        self.assertFalse(LSS07Config().active(DAY))

    def test_strict_thresholds(self):
        self.assertEqual(evaluate(OBS), 'EXTREME_EXIT')
        for delta in [dict(score=60.),dict(rank=150),dict(score_slope=0.),dict(rank_slope=0.)]:
            self.assertEqual(evaluate(dict(OBS,**delta)), 'NO_TRIGGER')

    def test_price_repair_only_own_exit(self):
        up=dict(OBS,close=92.)
        self.assertEqual(evaluate(up), 'REPAIR_DEFER_TODAY_ONLY')
        self.assertEqual(evaluate(up,['EXIT']), 'CANONICAL_FULL_EXIT_PRIORITY')
        self.assertEqual(evaluate(dict(OBS,close=91.)), 'EXTREME_EXIT')

    def test_buy_add_priority(self):
        for action in ['BUY','ADD']:
            self.assertEqual(evaluate(OBS,[action]),'BUY_ADD_UNCHANGED_NO_OVERLAY')

    def test_golden_research_observations(self):
        rows=json.loads(gzip.decompress((FIX/'policy.json.gz').read_bytes()))
        self.assertGreater(len(rows),4000)
        for r in rows:
            o=r['observation'];actions=[o['canonical_action']]
            if o['hard_exit']: actions.append('EXIT')
            if o.get('same_symbol_buy'):actions.append('BUY')
            reason=evaluate(dict(o,ready=o['score_slope'] is not None and o['rank_slope'] is not None),actions)
            self.assertEqual(reason,r['reason'],(o['trade_key'],o['date']))

    def test_real_frozen_features_and_no_future_leak(self):
        raw=json.loads(gzip.decompress((FIX/'features.json.gz').read_bytes()))
        hist={s:{d:DailyBar(d,c,c,c,c) for d,c in rows} for s,rows in raw['history'].items()}
        self.assertGreaterEqual(len(raw['expected']),2)
        for target in raw['expected']:
            sym=target['trade_key'].split('|')[0];d=target['date']
            snap=MarketSnapshot(d,raw['symbols'],{}, {},None,history_by_symbol=hist)
            got=observations(snap,[sym])[sym]
            for k in ['score','rank','score_slope','rank_slope','close','previous_close']:
                self.assertAlmostEqual(got[k],target[k],places=9,msg=(sym,d,k))
        # The NET test above receives prices through 2026, yet matches 2023 frozen inputs.

    def test_ties_alphabetical_fraction(self):
        from datetime import timedelta
        dates=[(date(2025,1,1)+timedelta(days=i)).isoformat() for i in range(70)]
        hist={s:{d:DailyBar(d,100.,100.,100.,100.) for d in dates} for s in ['SPX','Z','A']}
        snap=MarketSnapshot(dates[-1],['Z','A'],{},{},None,history_by_symbol=hist)
        out=observations(snap,['Z','A']);self.assertEqual(out['A']['rank'],1);self.assertEqual(out['Z']['rank'],2)
        self.assertEqual(out['Z']['samples'][-1]['rank_fraction'],1.)

    def test_missing_history_keeps_original_orders(self):
        r=result_for();out=apply_lss07(snapshot=snapshot_empty(),result=r,config=CFG)
        self.assertEqual(out.order_intents,r.order_intents)
        self.assertEqual(out.metadata['lss07']['evaluations'][0]['reason'],'DATA_NOT_READY')

    def test_disabled_and_pre_effective_exact_identity(self):
        r=result_for()
        with patch('e1r_engine.lss07.observations',side_effect=AssertionError('must not compute')):
            for cfg in [LSS07Config(),LSS07Config(True,'2026-05-18')]:
                self.assertIs(apply_lss07(snapshot=snapshot_empty(),result=r,config=cfg),r)

    def test_full_exit_existing_fractional_position_no_account_mutation(self):
        r=result_for('REDUCE');before=copy.deepcopy(r)
        with patch('e1r_engine.lss07.observations',return_value={'X':OBS}):
            out=apply_lss07(snapshot=snapshot_empty(),result=r,config=CFG)
        self.assertEqual(r,before);self.assertIs(out.account_after,r.account_after)
        o=out.order_intents[0];self.assertEqual(o.intent_type,'EXIT');self.assertEqual(o.target_quantity,0.)
        self.assertEqual(o.metadata['lss07']['remaining_quantity'],7.99)
        self.assertEqual(o.metadata['lss07']['entry_date'],DAY) # min-hold exempt from entry day
        self.assertEqual(o.metadata['strategy_version'],VERSION)

    def test_other_orders_and_gate_unchanged(self):
        r=result_for();buy=OrderIntent(DAY,'Y','BUY','BUY',2.,None,'existing_buy','UPTREND',{})
        r=replace(r,order_intents=r.order_intents+[buy]);before=copy.deepcopy(r)
        with patch('e1r_engine.lss07.observations',return_value={'X':OBS}):out=apply_lss07(snapshot=snapshot_empty(),result=r,config=CFG)
        self.assertIn(buy,out.order_intents);self.assertEqual(out.decision_trace.inputs,before.decision_trace.inputs)
        self.assertEqual(out.account_after,before.account_after)

    def test_canonical_exit_and_add_preserved(self):
        for action in ['EXIT','ADD']:
            r=result_for(action)
            with patch('e1r_engine.lss07.observations',return_value={'X':OBS}):out=apply_lss07(snapshot=snapshot_empty(),result=r,config=CFG)
            self.assertEqual(out.order_intents,r.order_intents)

    def test_forward_t1_exit_and_deterministic_pending(self):
        r=result_for()
        with patch('e1r_engine.lss07.observations',return_value={'X':OBS}):out=apply_lss07(snapshot=snapshot_empty(),result=r,config=CFG)
        pending=PendingOrderLedger.create(out.order_intents)
        self.assertEqual(pending,PendingOrderLedger.create(out.order_intents))
        self.assertEqual(pending[0].signal_date,DAY)
        filled=T1ExecutionEngine().execute(execution_date='2026-05-18',account=r.account_after,pending_orders=pending,
                    bars_by_symbol={'X':DailyBar('2026-05-18',90.,92.,89.,91.)})
        self.assertNotIn('X',filled.account_after.positions);self.assertEqual(len(filled.fills),1)
        self.assertAlmostEqual(filled.account_after.cash-r.account_after.cash,7.99*89.*.999)
        self.assertEqual(r.account_after.positions['X'].quantity,7.99)

    def test_live_adapter_consumes_exit_without_changing_account(self):
        r=result_for()
        with patch('e1r_engine.lss07.observations',return_value={'X':OBS}):out=apply_lss07(snapshot=snapshot_empty(),result=r,config=CFG)
        engine=Mock();engine.step.return_value=out
        account_adapter=Mock();account_adapter.to_engine_account.return_value=r.account_before
        adapter=LiveEngineAdapter(data_adapter=Mock(),stock_symbols=['X'],engine=engine,account_adapter=account_adapter)
        live_account=Mock();market=Mock();market.market_date=date.fromisoformat(DAY)
        with patch('e1r_engine.live_engine_adapter._snapshot_from_bundle',return_value=snapshot_empty()):
            decision=adapter.decide(market_date=date.fromisoformat(DAY),market_data=market,account=live_account)
        self.assertEqual(decision.position_recommendations[0].action,'EXIT')
        self.assertEqual(decision.position_recommendations[0].reason,'LSS07_EXTREME_EXIT')
        self.assertEqual(decision.evidence['engine_result_metadata']['lss07']['version'],VERSION)
        self.assertEqual(r.account_after.positions['X'].quantity,7.99)
        self.assertEqual(live_account.mock_calls,[])

    def test_core_hook_and_capped_atr_priority(self):
        # Feed the formal entry; verify the overlay follows the real finalize boundary.
        snap=replace(snapshot_empty(),history_by_symbol={'SPX':{DAY:DailyBar(DAY,1.,1.,1.,1.)}})
        engine=E1RCoreEngine(config=E1RCoreEngineConfig(lss07=CFG))
        for action,expected in [('HOLD','LSS07_EXTREME_EXIT'),('EXIT','existing')]:
            r=result_for(action)
            with patch('e1r_engine.canonical_runtime.CanonicalRuntime.decide',return_value=(r,None)), \
                 patch.object(engine,'_finalize_capped_atr',return_value=r) as finalize, \
                 patch('e1r_engine.lss07.observations',return_value={'X':OBS}):
                out=engine.step(snap,r.account_before)
            finalize.assert_called_once();self.assertEqual(out.order_intents[0].reason,expected)

    def test_disabled_core_against_exact_prechange_source(self):
        mod=types.ModuleType('_lss07_prechange_core');sys.modules[mod.__name__]=mod
        exec(compile((FIX/'core_before.py.txt').read_text(),str(FIX/'core_before.py.txt'),'exec'),mod.__dict__)
        fixture=CanonicalEngineEntryTests();fixture.setUp()
        account=AccountState.empty(fixture.day)
        for cfg in [E1RCoreEngineConfig(),E1RCoreEngineConfig(lss07=LSS07Config(True,'2099-01-01'))]:
            before=mod.E1RCoreEngine().step(fixture.snapshot,account)
            after=E1RCoreEngine(config=cfg).step(fixture.snapshot,account)
            self.assertEqual(asdict(after),asdict(before))

    def test_restarting_does_not_accumulate_overlay_state(self):
        r=result_for()
        with patch('e1r_engine.lss07.observations',return_value={'X':OBS}):
            a=apply_lss07(snapshot=snapshot_empty(),result=r,config=CFG)
            b=apply_lss07(snapshot=snapshot_empty(),result=r,config=CFG)
        self.assertEqual(a,b)

if __name__=='__main__': unittest.main()
