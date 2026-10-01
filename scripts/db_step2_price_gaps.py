"""Validate every pending held/index bar before the existing atomic promotion.
No synthetic bars, eligibility override, strategy change or ledger write.
"""
import json
from datetime import date, timedelta
from pathlib import Path

LIVE = Path('exports/official/FD-M3180125-SP500-TOP3-engine/live')

def pending_dates(root, expected, calendar):
    state = json.loads((root / LIVE / 'runtime/current/runtime_state.json').read_text())
    last = state.get('last_committed_market_date')
    start = calendar.next_session(date.fromisoformat(last)) if last else date.fromisoformat(state['opening_date'])
    result = []
    end = date.fromisoformat(expected)
    while start <= end:
        result.append(start.isoformat())
        if len(result) > 30:
            raise RuntimeError('HOLD_DB_STEP2: catchup exceeds 30 sessions; manual review required')
        start = calendar.next_session(start)
    return result

def gaps(rows_by_file, symbols, dates, valid):
    missing = {}
    for symbol in sorted(symbols):
        rows = rows_by_file.get(symbol + '.json', [])
        bad = [d for d in dates if len([r for r in rows if r.get('date') == d and valid(r)]) != 1]
        if bad:
            missing[symbol] = bad
    return missing

def ensure_pending_bars(*, root, merged_by_file, expected, download, merge, clip, valid, write):
    from e1r_engine.live_calendar import load_live_trading_calendar
    calendar = load_live_trading_calendar(root / 'config/live_calendar/us_equity_calendar_v1.0.json')
    dates = pending_dates(root, expected, calendar)
    account = json.loads((root / LIVE / 'runtime/current/account_state.json').read_text())
    positions = account.get('positions')
    if not isinstance(positions, dict):
        raise RuntimeError('HOLD_DB_STEP2: positions must be an object')
    symbols = set(positions) | {'SPX','NDX','SOX','VIX'}
    if any(not s or not all(c.isalnum() or c in '.-' for c in s) for s in symbols):
        raise RuntimeError('HOLD_DB_STEP2: invalid symbol')
    # Even a no-op catchup must meet the builder's existing index freshness gate.
    required_dates = dates or [expected]
    before = gaps(merged_by_file, symbols, required_dates, valid)
    repairs = []
    index = {'SPX':'^GSPC','NDX':'^NDX','SOX':'^SOX','VIX':'^VIX'}
    for symbol, missing in before.items():
        if symbol + '.json' not in merged_by_file:
            continue  # Never change the frozen catalogue.
        for attempt in range(2):
            frame = download(index.get(symbol,symbol), min(missing), (date.fromisoformat(max(missing))+timedelta(days=1)).isoformat())
            if frame is None:
                continue
            frame = clip(frame, expected)
            if frame is None:
                continue
            # Fill only missing/invalid pending rows; do not overwrite good rows.
            frame = frame.loc[frame['date'].isin(missing)].copy()
            old = merged_by_file[symbol + '.json']
            merged_by_file[symbol + '.json'] = merge(old,frame)
            missing = gaps(merged_by_file,{symbol},required_dates,valid).get(symbol,[])
            repairs.append({'symbol':symbol,'attempt':attempt+1,'remaining_dates':missing})
            if not missing:
                break
    after = gaps(merged_by_file,symbols,required_dates,valid)
    report = {'pending_dates':dates,'required_symbols':sorted(symbols),'gaps_before':before,'attempts':repairs,'gaps_after':after,'status':'HOLD' if after else 'PASS'}
    write(root / LIVE / 'automation/db_step2/price_gaps.json',report)
    print('DB_STEP2_PRICE_GAPS=' + json.dumps(report,sort_keys=True))
    if after:
        raise RuntimeError('HOLD_DB_STEP2_PENDING_BARS: ' + json.dumps(after,sort_keys=True))
