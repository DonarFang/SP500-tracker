"""Bounded deployment tests; temporary accounts only; stdlib unittest."""
from __future__ import annotations
import copy
from dataclasses import replace
from datetime import date
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace as NS
import unittest
from unittest.mock import patch, Mock

from e1r_engine.lss07_deployment import production_engine, load_deployment, CONFIG_REL, ENGINE_ID, DEPLOYMENT_ID
from e1r_engine.lss07 import VERSION, apply_lss07
from e1r_engine.core import E1RCoreEngine
from e1r_engine.state import AccountState
from e1r_engine.live_persistence import LiveRuntimeRepository
from e1r_engine.live_production import LiveProductionRuntime
from e1r_engine.live_account import LiveOpeningState
import test_lss07_step5 as prior


def deployment():
    return dict(schema_version='1.0', deployment_id=DEPLOYMENT_ID, strategy_version=VERSION,
                enabled=True, effective_signal_date=prior.DAY, tracks=['forward','live'],
                history_policy='PRESERVE_NO_REPLAY', live_execution='RECOMMENDATION_USER_CONFIRMED')


class DeploymentTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.path=self.root/CONFIG_REL
        self.path.parent.mkdir(parents=True)
        self.config=deployment();self.write()
    def write(self): self.path.write_text(json.dumps(self.config))
    def official(self,track):
        p=self.root/'exports/official'/ENGINE_ID/track
        return p/'runtime' if track=='forward' else p
    def engine(self,track): return production_engine(track,self.official(track),repo_root=self.root)

    def test_both_tracks_share_frozen_core_and_keep_other_configuration(self):
        baseline=E1RCoreEngine().config
        for track in ('forward','live'):
            engine=self.engine(track)
            self.assertIs(type(engine),E1RCoreEngine)
            self.assertTrue(engine.config.lss07.enabled)
            self.assertEqual(replace(engine.config,lss07=baseline.lss07),baseline)

    def test_research_and_unconfigured_roots_stay_disabled(self):
        for track in ('forward','live'):
            self.assertFalse(production_engine(track,self.root/'research'/track,repo_root=self.root).config.lss07.enabled)
        self.path.unlink()
        self.assertFalse(self.engine('forward').config.lss07.enabled)

    def test_invalid_configuration_fails_closed(self):
        for field,value in [('enabled','true'),('strategy_version','OTHER'),('tracks',['forward']),('effective_signal_date',None)]:
            self.config=deployment();self.config[field]=value;self.write()
            with self.assertRaises((ValueError,TypeError)): self.engine('live')

    def test_effective_date_boundary_and_existing_position_identity(self):
        result=prior.result_for();before=copy.deepcopy(result)
        cfg=self.engine('forward').config.lss07
        with patch('e1r_engine.lss07.observations',return_value={'X':prior.OBS}) as obs:
            out=apply_lss07(snapshot=prior.snapshot_empty('2026-05-14'),result=result,config=cfg)
            self.assertIs(out,result);obs.assert_not_called()
            out=apply_lss07(snapshot=prior.snapshot_empty(),result=result,config=cfg)
        self.assertEqual(result,before)
        self.assertEqual(out.account_after,before.account_after)
        self.assertEqual(out.order_intents[0].reason,'LSS07_EXTREME_EXIT')
        self.assertEqual(out.metadata['lss07']['effective_signal_date'],prior.DAY)

    def test_shutdown_preserves_pending_and_does_not_rewrite_config(self):
        self.config['enabled']=False;self.write();raw=self.path.read_bytes()
        result=prior.result_for('EXIT');pending=copy.deepcopy(result.order_intents)
        out=apply_lss07(snapshot=prior.snapshot_empty(),result=result,config=self.engine('live').config.lss07)
        self.assertIs(out,result);self.assertEqual(out.order_intents,pending)
        self.assertEqual(self.path.read_bytes(),raw)

    def test_forward_composition_injects_only_decision_engine(self):
        import e1r_engine.forward_production_composition as mod
        from e1r_engine.forward_orchestrator import ForwardStrategyInputBuilder
        engine=self.engine('forward');builder=ForwardStrategyInputBuilder(management_action_provider=Mock(),engine=E1RCoreEngine())
        data=NS(trading_dates=(prior.DAY,),series_by_symbol={},universe=('X',),required_execution_symbols=('SPX',),source_hashes={})
        with patch.object(mod.ProductionForwardDataAdapter,'load',return_value=data),patch.object(mod,'production_engine',return_value=engine) as factory:
            comp=mod.build_production_forward_composition(seed_root=self.root/'seed',runtime_root=self.official('forward'),price_files_by_symbol={},universe=('X',),strategy_input_builder=builder,runtime_commit_provider=lambda:'test')
        factory.assert_called_once_with('forward',self.official('forward'))
        self.assertIs(comp.decision_router.engine,engine)
        self.assertIs(comp.strategy_input_builder,builder)
        self.assertFalse(comp.repository.exists())

    def test_active_live_composition_wiring_and_unactivated_isolation(self):
        import e1r_engine.live_composition as mod
        engine=self.engine('live')
        for unactivated in (False,True):
            with patch.object(mod,'validate_current_data_status'),patch.object(mod,'discover_live_stock_symbols',return_value=('X',)),patch.object(mod,'discover_live_eligible_stock_symbols',return_value=(('X',),())),patch.object(mod,'LivePriceRepository') as prices,patch.object(mod,'LiveRuntimeRepository') as repos,patch.object(mod,'production_engine',return_value=engine) as factory:
                comp=mod._compose_live_production_components(price_root=self.root/'live_prices',live_root=self.official('live'),data_status_path=self.root/'status',market_date=date(2026,5,15),expected_execution_date=date(2026,5,18),expected_stock_count=1,min_bars=120,opening=LiveOpeningState(),initialize_unactivated=unactivated)
                if unactivated:
                    factory.assert_not_called();self.assertFalse(comp.runtime.processor.engine.engine.config.lss07.enabled)
                else:
                    factory.assert_called_once_with('live',self.official('live'))
                    self.assertIs(comp.runtime.processor.engine.engine,engine)
                    repos.return_value.initialize_unactivated.assert_not_called()

    def live_case(self, audit, day='2026-05-15'):
        root=self.root/'live';repo=LiveRuntimeRepository(root)
        repo.replace_current('runtime_state.json',dict(status='ACTIVE',opening_activated=True,activation_required=False,opening_date='2026-05-01',last_committed_market_date='2026-05-14'))
        old=root/'runtime/daily/2026-05-14/sentinel.json';old.parent.mkdir(parents=True);old.write_bytes(b'old immutable advice')
        account=dict(positions={'X':{'shares':'7.99','average_cost':'100'}},actual_cash='100',positions_value='719.10',total_equity='819.10',trading_pnl='0',cash_difference='0')
        payload=dict(account=account,regime='UPTREND',regime_subclass=None,market_state='ON',market_gate='ALLOW',entry_capacity=0,strategy_branch='UPTREND',reference_top3=[],position_recommendations=[],evidence={'engine_result_metadata':({'lss07':audit} if audit else {})})
        result=NS(market_date=date.fromisoformat(day),decision=NS(position_recommendations=()),result_hash='test',to_payload=lambda:copy.deepcopy(payload))
        runtime=LiveProductionRuntime(repository=repo,processor=Mock(),opening=LiveOpeningState())
        return runtime,result,old,account

    def test_live_new_advice_persists_version_without_confirmed_trades(self):
        audit=dict(version=VERSION,effective_signal_date=prior.DAY,status='EVALUATED',evaluations=[],changed_symbols=[])
        runtime,result,old,account=self.live_case(audit)
        out=runtime.commit_active_daily(result=result,expected_execution_date=date(2026,5,18))
        self.assertFalse(out['actual_trades_recorded']);self.assertFalse(out['automatic_execution_enabled'])
        root=runtime.repository.paths.root
        row=json.loads((root/'runtime/daily/2026-05-15/engine_recommendations.json').read_text())
        self.assertEqual(row['lss07'],audit);self.assertEqual(row['strategy_version'],VERSION)
        self.assertEqual(json.loads((root/'runtime/current/account_state.json').read_text()),account)
        self.assertEqual(old.read_bytes(),b'old immutable advice')
        self.assertFalse(runtime.repository.transaction_path.exists())
        self.assertFalse(runtime.repository.journal_path.exists())

    def test_pre_effective_live_advice_retains_schema(self):
        runtime,result,old,account=self.live_case(None)
        runtime.commit_active_daily(result=result,expected_execution_date=date(2026,5,18))
        row=json.loads((runtime.repository.paths.current/'latest_recommendations.json').read_text())
        self.assertNotIn('lss07',row);self.assertNotIn('strategy_version',row)
        self.assertEqual(old.read_bytes(),b'old immutable advice')

    def test_live_existing_date_is_not_recommitted(self):
        runtime,result,old,account=self.live_case(None,day='2026-05-14')
        with patch.object(runtime.repository,'load_ledger',side_effect=AssertionError('must not replay')):
            out=runtime.commit_active_daily(result=result,expected_execution_date=date(2026,5,15))
        self.assertEqual(out['decision'],'PASS_LIVE_ACTIVE_NO_NEW_DATE')
        self.assertEqual(old.read_bytes(),b'old immutable advice')

if __name__=='__main__': unittest.main()
