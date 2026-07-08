# Stage 3.8E-2F-2C-4C-1 5Y Equity Artifact Audit

Generated At: `2026-07-08T10:21:02.478976+00:00`

## Status

- Status: `AUDIT_COMPLETE_NO_SOURCE_CHANGES`
- Dashboard changed: `False`
- Exports changed: `False`
- State changed: `False`
- Workflow changed: `False`
- Strategy logic changed: `False`

## Known Files

- `exports/backtest.json`: kind=`unknown`, rows=`0`, dates=`None→None`, unique_dates=`0`, max_rows_per_date=`None`
- `exports/oos_equity_curve.json`: kind=`portfolio_daily_equity_candidate`, rows=`12`, dates=`2026-06-18→2026-07-07`, unique_dates=`12`, max_rows_per_date=`1`
- `exports/e1r_v0_2_backtest_summary.json`: kind=`summary_metadata`, rows=`0`, dates=`None→None`, unique_dates=`0`, max_rows_per_date=`None`
- `exports/e1r_v0_2_backtest_equity_curve.json`: kind=`symbol_level_or_diagnostic_rows`, rows=`8819`, dates=`2021-06-11→2026-06-16`, unique_dates=`859`, max_rows_per_date=`19`
- `exports/oos_e1r_v0_2_equity_curve.json`: kind=`portfolio_daily_equity_candidate`, rows=`1`, dates=`2026-06-18→2026-06-18`, unique_dates=`1`, max_rows_per_date=`1`
- `exports/oos_e1r_v0_2_summary.json`: kind=`summary_metadata`, rows=`0`, dates=`None→None`, unique_dates=`0`, max_rows_per_date=`None`
- `data/research/e1_5y/regimes/spx_regime_daily.json`: kind=`unknown`, rows=`0`, dates=`None→None`, unique_dates=`0`, max_rows_per_date=`None`

## Top E1 Candidates

- score `8` · `exports/oos_equity_curve.json` · kind `portfolio_daily_equity_candidate` · rows `12` · dates `2026-06-18→2026-07-07` · unique_dates `12`
- score `5` · `exports/oos_e1r_v0_2_equity_curve.json` · kind `portfolio_daily_equity_candidate` · rows `1` · dates `2026-06-18→2026-06-18` · unique_dates `1`
- score `2` · `data/research/e1r/e1r_formal_backtest_v0_1.json` · kind `numeric_equity_array_candidate` · rows `131` · dates `None→None` · unique_dates `0`

## Top E1R Candidates

- score `12` · `exports/oos_e1r_v0_2_equity_curve.json` · kind `portfolio_daily_equity_candidate` · rows `1` · dates `2026-06-18→2026-06-18` · unique_dates `1`
- score `9` · `data/research/e1r/e1r_formal_backtest_v0_1.json` · kind `numeric_equity_array_candidate` · rows `131` · dates `None→None` · unique_dates `0`
- score `8` · `exports/oos_equity_curve.json` · kind `portfolio_daily_equity_candidate` · rows `12` · dates `2026-06-18→2026-07-07` · unique_dates `12`

## Diagnosis

- exports/backtest.json equity_curve length=None, simulation window=None to None.
- exports/e1r_v0_2_backtest_equity_curve.json kind=symbol_level_or_diagnostic_rows row_count=8819 unique_dates=859 max_rows_per_date=19.
- E1R backtest equity file is not safe as a portfolio-level line without aggregation/deduplication.
- E1R forward equity rows=1, date range=2026-06-18 to 2026-06-18.
- Top E1 canonical candidate: exports/oos_equity_curve.json score=8.
- Top E1R canonical candidate: exports/oos_e1r_v0_2_equity_curve.json score=12.

## Recommendation

- Do not patch the chart until canonical 5Y portfolio-level E1 and E1R equity sources are selected.
- Reject symbol-level/diagnostic rows as direct chart lines unless aggregated to one portfolio value per date.
- If E1 5Y artifact exists, align chart on 5Y dates and pad shorter series with null.
- For E1R forward continuity, scale forward strategy_indexed by the E1R backtest ending indexed value, not by 100.
