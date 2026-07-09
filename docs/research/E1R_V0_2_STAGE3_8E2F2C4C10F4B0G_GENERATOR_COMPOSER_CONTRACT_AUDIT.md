# Stage 3.8E-2F-2C-4C-10F-4B-0G Generator / Composer Contract Audit

Generated At: `2026-07-09T10:31:30.586953+00:00`

## Status

- Status: `E1R_GENERATOR_COMPOSER_CONTRACT_AUDIT_COMPLETE_NO_EXECUTION`
- Source-only audit: `True`
- Generator executed: `False`
- Composer executed: `False`
- E1R canonical written: `False`
- Strategy files unchanged: `True`
- Canonical existence unchanged: `True`

## Conclusion

- `GENERATOR_COMPOSER_CONTRACT_NEEDS_RUNTIME_RETURN_PROBE`
- Recommended: Next run a narrow runtime-return probe around compose_e1r_v0_2_variant to print actual return keys/list lengths without writing canonical exports.

## Source Flags

```json
{
  "generator_has_compose_call": false,
  "generator_has_core_variant_result": false,
  "generator_has_sidecar_result": false,
  "generator_has_daily_or_equity_records": true,
  "composer_has_compose_def": true,
  "composer_mentions_core_variant_result": true,
  "composer_mentions_sidecar_result": true,
  "composer_mentions_daily_or_equity_records": true
}
```

## Findings

- Composer defines compose_e1r_v0_2_variant.
- core_variant_result is referenced in generator/composer source.
- sidecar_result is referenced in generator/composer source.
- daily/equity record names are referenced in generator/composer source.
- Generator writes both summary and equity_curve export names.

## Risks

- Generator does not directly reference compose_e1r_v0_2_variant; dry-run candidate may be wrapper-only or summary replay.

## Import Probe

```json
{
  "attempted": true,
  "ok": false,
  "objects": {
    "e1r_composer": {
      "path": "src/engine/e1r_composer.py",
      "target_objects": {
        "compose_e1r_v0_2_variant": {
          "type": "function",
          "signature": "(core_variant_result: 'dict[str, Any]', sidecar_result: 'dict[str, Any]', initial_equity: 'float' = 100000.0) -> 'dict[str, Any]'",
          "source_file": "/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/e1r_composer.py",
          "source_line": 283
        },
        "build_equity_records_from_returns": {
          "type": "function",
          "signature": "(interval_records: 'Sequence[dict[str, Any]]', initial_equity: 'float') -> 'list[dict[str, Any]]'",
          "source_file": "/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/e1r_composer.py",
          "source_line": 171
        },
        "extract_core_interval_returns": {
          "type": "function",
          "signature": "(core_daily_equity_records: 'Sequence[dict[str, Any]]', sidecar_records: 'Sequence[dict[str, Any]]') -> 'list[dict[str, Any]]'",
          "source_file": "/Users/dongfang/Downloads/sp500-tracker-v13/src/engine/e1r_composer.py",
          "source_line": 94
        }
      },
      "public_relevant_objects": {
        "build_equity_records_from_returns": {
          "type": "function",
          "signature": "(interval_records: 'Sequence[dict[str, Any]]', initial_equity: 'float') -> 'list[dict[str, Any]]'"
        },
        "compose_e1r_v0_2_variant": {
          "type": "function",
          "signature": "(core_variant_result: 'dict[str, Any]', sidecar_result: 'dict[str, Any]', initial_equity: 'float' = 100000.0) -> 'dict[str, Any]'"
        },
        "compound_return": {
          "type": "function",
          "signature": "(returns: 'Sequence[Optional[float]]') -> 'float'"
        },
        "extract_core_interval_returns": {
          "type": "function",
          "signature": "(core_daily_equity_records: 'Sequence[dict[str, Any]]', sidecar_records: 'Sequence[dict[str, Any]]') -> 'list[dict[str, Any]]'"
        },
        "summarize_combined_variant": {
          "type": "function",
          "signature": "(interval_records: 'Sequence[dict[str, Any]]', equity_records: 'Sequence[dict[str, Any]]', initial_equity: 'float') -> 'dict[str, Any]'"
        }
      }
    }
  },
  "errors": [
    "e1r_sidecar_sleeve: AttributeError: 'NoneType' object has no attribute '__dict__'"
  ]
}
```

## Relevant Definitions

```json
{
  "scripts/export_canonical_5y_equity_curves.py": [
    {
      "name": "import_composer",
      "type": "FunctionDef",
      "line": 119,
      "end_line": 148,
      "matched_terms": [
        "build_equity_records_from_returns",
        "extract_core_interval_returns"
      ],
      "assignments_of_interest": [],
      "returns": [
        "result"
      ]
    },
    {
      "name": "run_build_equity_smoke",
      "type": "FunctionDef",
      "line": 151,
      "end_line": 220,
      "matched_terms": [
        "build_equity_records_from_returns"
      ],
      "assignments_of_interest": [],
      "returns": [
        "{'ok': any((a.get('ok') for a in attempts)), 'attempts': attempts}",
        "{'ok': False, 'error': 'build_equity_records_from_returns not found'}"
      ]
    },
    {
      "name": "inspect_mode",
      "type": "FunctionDef",
      "line": 223,
      "end_line": 241,
      "matched_terms": [
        "e1r_v0_2_backtest_equity_curve.json",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve"
      ],
      "assignments_of_interest": [],
      "returns": [
        "{'composer': composer_clean, 'source_files': [summarize_json(p) for p in source_files]}"
      ]
    },
    {
      "name": "smoke_mode",
      "type": "FunctionDef",
      "line": 244,
      "end_line": 280,
      "matched_terms": [
        "build_equity_records_from_returns"
      ],
      "assignments_of_interest": [],
      "returns": [
        "{'composer_import_ok': True, 'build_equity_records_from_returns': build_smoke, 'utility_functions': utility_smoke}",
        "{'composer_import_ok': False, 'error': composer_result.get('error', 'composer import failed')}"
      ]
    },
    {
      "name": "load_existing_5y_generation_inputs",
      "type": "FunctionDef",
      "line": 284,
      "end_line": 446,
      "matched_terms": [
        "build_equity_records_from_returns",
        "daily_equity_records",
        "daily_records",
        "e1r_v0_2_backtest_equity_curve.json",
        "e1r_v0_2_backtest_summary.json",
        "equity_curve",
        "extract_core_interval_returns",
        "variant_results"
      ],
      "assignments_of_interest": [
        {
          "target": "source_summary",
          "value": "{'core_sources': [], 'sidecar_sources': [], 'interval_sources': []}"
        },
        {
          "target": "variant_results",
          "value": "portfolio.get('variant_results') if isinstance(portfolio, dict) else {}"
        },
        {
          "target": "sidecar",
          "value": "read_json(ROOT / 'exports/oos_e1r_v0_2_sidecar.json', default={})"
        },
        {
          "target": "core_candidates",
          "value": "[x for x in source_summary['core_sources'] if x.get('has_core_minimum')]"
        },
        {
          "target": "sidecar_candidates",
          "value": "[x for x in source_summary['sidecar_sources'] if x.get('has_sidecar_minimum')]"
        },
        {
          "target": "source_summary['attempts']",
          "value": "attempts"
        },
        {
          "target": "source_summary['can_generate_from_persisted_inputs']",
          "value": "any((a.get('ok') and a.get('interval_count', 0) > 0 and (a.get('equity_count', 0) > 0) for a in attempts))"
        },
        {
          "target": "frozen_summary",
          "value": "read_json(ROOT / 'exports/e1r_v0_2_backtest_summary.json', default={})"
        },
        {
          "target": "source_summary['frozen_metric_targets']",
          "value": "{'total_return_pct': frozen_summary.get('total_return_pct'), 'spx_return_pct': frozen_summary.get('spx_return_pct'), 'alpha_pct': frozen_summary.get('alpha_pct'), 'max_drawdown_pct': frozen_summary.get('max_drawdown_pct'), 'profit_factor': frozen_summary.get('profit_factor'), 'sharpe_ratio': frozen_summary.get('sharpe_ratio')}"
        },
        {
          "target": "source_summary['decision']",
          "value": "'PERSISTED_INPUTS_SUFFICIENT' if source_summary['can_generate_from_persisted_inputs'] else 'PERSISTED_INPUTS_INSUFFICIENT_NEED_FROZEN_GENERATOR_DRY_RUN'"
        },
        {
          "target": "variant",
          "value": "parts[3]"
        },
        {
          "target": "core_rows",
          "value": "resolve_rows(core['label'])"
        },
        {
          "target": "side_rows",
          "value": "resolve_rows(side['label'])"
        },
        {
          "target": "interval_records",
          "value": "composer.extract_core_interval_returns(core_rows, side_rows)"
        },
        {
          "target": "equity_records",
          "value": "composer.build_equity_records_from_returns(interval_records, 100000.0) if interval_records else []"
        }
      ],
      "returns": [
        "source_summary",
        "{'label': label, 'is_list': True, 'length': len(rows), 'keys': sorted(keys), 'has_core_minimum': 'date' in keys and ('daily_return' in keys or 'daily_return_pct' in keys or 'total_equity' in keys or ('equity' in keys)), 'has_sidecar_minimum': 'date' in keys and 'next_date' in keys and ('sidecar_return' in keys or 'sidecar_return_pct' in keys), 'has_interval_minimum': 'date' in keys and 'next_date' in keys and ('combined_return' in keys)}",
        "[]",
        "{'label': label, 'is_list': False}",
        "portfolio.get('daily_records')",
        "variant_results.get(variant, {}).get('daily_records')",
        "oos_e1.get('curve')",
        "e1r_diag.get('rows')",
        "e1r_diag.get('equity_curve')",
        "sidecar.get(key) if isinstance(sidecar, dict) else sidecar"
      ]
    },
    {
      "name": "main",
      "type": "FunctionDef",
      "line": 470,
      "end_line": 540,
      "matched_terms": [
        "build_equity_records_from_returns",
        "equity_curve"
      ],
      "assignments_of_interest": [],
      "returns": [
        "0"
      ]
    },
    {
      "name": "resolve_rows",
      "type": "FunctionDef",
      "line": 380,
      "end_line": 396,
      "matched_terms": [
        "daily_records",
        "e1r_v0_2_backtest_equity_curve.json",
        "equity_curve",
        "variant_results"
      ],
      "assignments_of_interest": [
        {
          "target": "variant",
          "value": "parts[3]"
        }
      ],
      "returns": [
        "[]",
        "portfolio.get('daily_records')",
        "variant_results.get(variant, {}).get('daily_records')",
        "oos_e1.get('curve')",
        "e1r_diag.get('rows')",
        "e1r_diag.get('equity_curve')",
        "sidecar.get(key) if isinstance(sidecar, dict) else sidecar"
      ]
    }
  ],
  "src/engine/e1r_composer.py": [
    {
      "name": "extract_core_interval_returns",
      "type": "FunctionDef",
      "line": 94,
      "end_line": 168,
      "matched_terms": [
        "daily_equity_records",
        "extract_core_interval_returns"
      ],
      "assignments_of_interest": [
        {
          "target": "core_by_end_date",
          "value": "{}"
        },
        {
          "target": "core_by_end_date[date]",
          "value": "row | {'_normalized_daily_return': r}"
        },
        {
          "target": "core",
          "value": "core_by_end_date.get(next_date)"
        },
        {
          "target": "core_return",
          "value": "safe_float(core.get('_normalized_daily_return')) or 0.0"
        },
        {
          "target": "sidecar_return",
          "value": "safe_float(sidecar.get('portfolio_return')) or 0.0"
        }
      ],
      "returns": [
        "aligned"
      ]
    },
    {
      "name": "build_equity_records_from_returns",
      "type": "FunctionDef",
      "line": 171,
      "end_line": 211,
      "matched_terms": [
        "build_equity_records_from_returns"
      ],
      "assignments_of_interest": [
        {
          "target": "equity",
          "value": "initial_equity"
        },
        {
          "target": "records",
          "value": "[]"
        }
      ],
      "returns": [
        "records"
      ]
    },
    {
      "name": "summarize_combined_variant",
      "type": "FunctionDef",
      "line": 214,
      "end_line": 280,
      "matched_terms": [
        "equity_curve"
      ],
      "assignments_of_interest": [
        {
          "target": "core_returns",
          "value": "[safe_float(r.get('core_return')) or 0.0 for r in interval_records]"
        },
        {
          "target": "sidecar_returns",
          "value": "[safe_float(r.get('sidecar_return')) or 0.0 for r in interval_records]"
        },
        {
          "target": "equity_curve",
          "value": "[initial_equity] + [safe_float(r.get('equity')) or initial_equity for r in equity_records]"
        },
        {
          "target": "core_return",
          "value": "compound_return(core_returns)"
        },
        {
          "target": "sidecar_return",
          "value": "compound_return(sidecar_returns)"
        },
        {
          "target": "active_records",
          "value": "[r for r in interval_records if r.get('sidecar_active')]"
        },
        {
          "target": "sidecar_return_row",
          "value": "safe_float(row.get('sidecar_return')) or 0.0"
        }
      ],
      "returns": [
        "{'total_return_pct': pct_display(total_return), 'core_return_pct': pct_display(core_return), 'sidecar_return_pct': pct_display(sidecar_return), 'spx_return_pct': pct_display(spx_return), 'alpha_pct': pct_display(total_return - spx_return), 'max_drawdown_pct': abs(pct_display(max_drawdown(equity_curve)) or 0.0), 'profit_factor': profit_factor(combined_returns), 'sharpe_ratio': sharpe_ratio(combined_returns), 'daily_win_rate_pct': 100.0 * sum((1 for r in combined_returns if r > 0)) / len(combined_returns) if combined_returns else None, 'total_days': len(interval_records), 'daily_equity_record_count': len(equity_records), 'sidecar_active_days': len(active_records), 'sidecar_active_by_regime': active_by_regime, 'sidecar_active_by_subclass': active_by_subclass, 'sidecar_simple_contribution_by_regime_pct': {k: pct_display(v) for (k, v) in contribution_by_regime.items()}, 'sidecar_simple_contribution_by_subclass_pct': {k: pct_display(v) for (k, v) in contribution_by_subclass.items()}}"
      ]
    },
    {
      "name": "compose_e1r_v0_2_variant",
      "type": "FunctionDef",
      "line": 283,
      "end_line": 360,
      "matched_terms": [
        "E1R_REGIME_AWARE_V0_2",
        "build_equity_records_from_returns",
        "compose_e1r_v0_2_variant",
        "core_variant_result",
        "daily_equity_records",
        "extract_core_interval_returns",
        "sidecar_result"
      ],
      "assignments_of_interest": [
        {
          "target": "core_records",
          "value": "core_variant_result.get('daily_equity_records', [])"
        },
        {
          "target": "sidecar_records",
          "value": "sidecar_result.get('records', [])"
        },
        {
          "target": "interval_records",
          "value": "extract_core_interval_returns(core_records, sidecar_records)"
        },
        {
          "target": "equity_records",
          "value": "build_equity_records_from_returns(interval_records, initial_equity)"
        },
        {
          "target": "summary",
          "value": "summarize_combined_variant(interval_records, equity_records, initial_equity)"
        },
        {
          "target": "sidecar_summary",
          "value": "sidecar_result.get('summary', {}) or {}"
        },
        {
          "target": "result['sidecar_active_days']",
          "value": "summary['sidecar_active_days']"
        },
        {
          "target": "result['sidecar_active_by_regime']",
          "value": "summary['sidecar_active_by_regime']"
        },
        {
          "target": "result['sidecar_active_by_subclass']",
          "value": "summary['sidecar_active_by_subclass']"
        },
        {
          "target": "result['sidecar_simple_contribution_by_regime_pct']",
          "value": "summary['sidecar_simple_contribution_by_regime_pct']"
        },
        {
          "target": "result['sidecar_simple_contribution_by_subclass_pct']",
          "value": "summary['sidecar_simple_contribution_by_subclass_pct']"
        }
      ],
      "returns": [
        "result"
      ]
    }
  ],
  "src/engine/e1r_sidecar_sleeve.py": [
    {
      "name": "summarize_sidecar",
      "type": "FunctionDef",
      "line": 473,
      "end_line": 535,
      "matched_terms": [
        "equity_curve"
      ],
      "assignments_of_interest": [
        {
          "target": "equity",
          "value": "config.initial_equity"
        },
        {
          "target": "equity_curve",
          "value": "[equity]"
        },
        {
          "target": "daily_returns",
          "value": "[r['portfolio_return'] for r in records]"
        },
        {
          "target": "active_records",
          "value": "[r for r in records if r['is_active']]"
        }
      ],
      "returns": [
        "{'name': 'E1R_SIDEWAYS_MA_CONFLICT_TOP10_25PCT_SLEEVE', 'allowed_subclasses': list(config.allowed_subclasses), 'top_n': config.top_n, 'gross_exposure': config.gross_exposure, 'excluded_symbols': list(config.excluded_symbols), 'total_days': len(records), 'active_days': len(active_records), 'exposure_pct_full_period': 100.0 * len(active_records) / len(records) if records else None, 'full_period_strategy_return_pct': pct_display(full_strategy_return), 'full_period_spx_return_pct': pct_display(full_spx_return), 'full_period_excess_vs_spx_pct': pct_display(full_strategy_return - full_spx_return), 'active_window_strategy_return_pct': pct_display(active_strategy_return), 'active_window_spx_return_pct': pct_display(active_spx_return), 'active_window_excess_vs_spx_pct': pct_display(active_strategy_return - active_spx_return), 'max_drawdown_pct': pct_display(max_drawdown(equity_curve)), 'profit_factor': profit_factor(daily_returns), 'sharpe': sharpe_ratio(daily_returns), 'active_day_win_rate_pct': 100.0 * len(wins) / len(active_records) if active_records else None, 'winning_active_days': len(wins), 'losing_active_days': len(losses), 'avg_active_day_return_pct': pct_display(mean_or_none(active_returns)), 'median_active_day_return_pct': pct_display(median_or_none(active_returns)), 'trade_count_approx': sum((len(r['holdings']) for r in active_records)), 'equity_start': config.initial_equity, 'equity_end': equity_curve[-1]}"
      ]
    },
    {
      "name": "build_e1r_sidecar_sleeve",
      "type": "FunctionDef",
      "line": 538,
      "end_line": 594,
      "matched_terms": [
        "build_e1r_sidecar_sleeve"
      ],
      "assignments_of_interest": [
        {
          "target": "records",
          "value": "run_daily_rebalanced_sidecar(rankings, spx, regimes, intervals, config)"
        },
        {
          "target": "summary",
          "value": "summarize_sidecar(records, config)"
        }
      ],
      "returns": [
        "{'engine': 'e1r_sidecar_sleeve', 'version': 'v0.2_formal_sleeve_engine', 'config': {'start_date': config.start_date, 'end_date': config.end_date, 'allowed_subclasses': list(config.allowed_subclasses), 'top_n': config.top_n, 'gross_exposure': config.gross_exposure, 'min_history_days': config.min_history_days, 'min_price': config.min_price, 'initial_equity': config.initial_equity, 'excluded_symbols': list(config.excluded_symbols)}, 'sample': {'intervals': len(intervals), 'first_interval': {'date': intervals[0][0], 'next_date': intervals[0][1]} if intervals else None, 'last_interval': {'date': intervals[-1][0], 'next_date': intervals[-1][1]} if intervals else None, 'stock_universe_after_exclusions': len(stocks), 'excluded_symbols_found_in_raw_data': excluded_found, 'regime_counts': regime_counts, 'sideways_subclass_counts': subclass_counts}, 'summary': summary, 'records': records}"
      ]
    }
  ],
  "src/engine/backtest.py": [
    {
      "name": "run_stateful_simulation",
      "type": "FunctionDef",
      "line": 763,
      "end_line": 2486,
      "matched_terms": [
        "daily_equity_records",
        "daily_records",
        "equity_curve",
        "run_stateful_simulation"
      ],
      "assignments_of_interest": [
        {
          "target": "strategy_variant",
          "value": "a.get('strategy_variant', 'top3_entry_rs_minhold_relstop')"
        },
        {
          "target": "e1r_regime_daily",
          "value": "a.get('e1r_regime_daily', {}) or {}"
        },
        {
          "target": "market_shock_daily_return",
          "value": "float(a.get('market_shock_daily_return', -0.02))"
        },
        {
          "target": "market_gate_variant",
          "value": "'D1_NO_MARKET_GATE' if not market_gate_enabled else 'D2_RISK_OFF_GATE' if not market_shock_gate_enabled else 'D3_RISK_OFF_PLUS_SHOCK_GATE'"
        },
        {
          "target": "equity_curve",
          "value": "[]"
        },
        {
          "target": "daily_records",
          "value": "[]"
        },
        {
          "target": "daily_equity_records",
          "value": "[]"
        },
        {
          "target": "daily_equity_peak",
          "value": "init_cap"
        },
        {
          "target": "e1r_candidate_records",
          "value": "[]"
        },
        {
          "target": "final_equity",
          "value": "cash"
        },
        {
          "target": "total_equity",
          "value": "cash + position_value"
        },
        {
          "target": "_prev_equity",
          "value": "daily_equity_records[-1]['total_equity'] if daily_equity_records else init_cap"
        },
        {
          "target": "_daily_return_pct",
          "value": "(total_equity / _prev_equity - 1) * 100 if _prev_equity and _prev_equity > 0 else 0.0"
        },
        {
          "target": "daily_equity_peak",
          "value": "max(daily_equity_peak, total_equity)"
        }
      ],
      "returns": [
        "{'layer': 'D', 'name': 'Stateful Portfolio Backtest', 'status': status, 'version': 'v1.6-top3-rs-minhold-relstop', 'execution_model': a.get('execution_model', 'adverse_intraday'), 'strategy_variant': strategy_variant, 'entry_top_n': entry_top_n, 'rank_based_exit': rank_based_exit, 'strategy_controls': {'entry_rs_min': entry_rs_min, 'ls60_exit_mode': ls60_exit_mode, 'candidate_top_n': candidate_top_n, 'qualified_entry_enabled': qualified_entry_enabled, 'qualified_rs_min': qualified_rs_min, 'qualified_momentum_min': qualified_momentum_min, 'qualified_th_min': qualified_th_min, 'qualified_states': list(qualified_states), 'qualified_price_above_ma50': qualified_price_above_ma50, 'qualified_ma50_slope_min': qualified_ma50_slope_min, 'qp_avg_pool_size': round(qp_diag['pool_size_sum'] / max(qp_diag['pool_days'], 1), 1), 'qp_pool_days': qp_diag['pool_days'], 'qp_days_pool_lt_3': qp_diag['days_pool_lt_3'], 'qp_days_pool_ge_10': qp_diag['days_pool_ge_10'], 'qp_buy_orders_generated': qp_diag['buy_orders_generated'], 'min_holding_days': min_holding_days, 'min_hold_allow_broken_exit': min_hold_allow_broken_exit, 'e1r_regime_wiring_enabled': e1r_regime_wiring_enabled, 'e1r_regime_source': a.get('e1r_regime_source') if e1r_regime_wiring_enabled else None, 'relative_stop_enabled': relative_stop_enabled, 'relative_stop_underperform_pct': round(relative_stop_underperform * 100, 2), 'relative_stop_action': relative_stop_action, 'relative_stop_once_per_position': relative_stop_once, 'relative_stop_stats': relative_stop_stats, 'fixed_take_profit_enabled': take_profit_enabled}, 'partial_take_profit': {'name': 'TP7-P', 'enabled': take_profit_enabled, 'trigger_gain_pct': round(take_profit_threshold * 100, 2), 'sell_fraction_pct': round(take_profit_fraction * 100, 1), 'trigger_price': 'signal-day close vs actual average cost', 'execution': 'T+1 adverse low minus one-way costs', 'once_per_position': True, 'block_add_after_trigger': block_add_after_take_profit, 'stats': take_profit_stats, 'note': 'Partial reduction releases cash but does not free a Max3 symbol slot.'}, 'market_entry_gate': {'variant': market_gate_variant, 'enabled': market_gate_enabled, 'risk_off_rule': 'SPX close < SPX MA50' if risk_off_below_spx_ma50 else 'disabled', 'market_shock_rule': f'SPX daily return <= {market_shock_daily_return * 100:.1f}%' if market_shock_gate_enabled else 'disabled', 'blocked_actions': ['BUY', 'ADD'], 'unaffected_actions': ['HOLD', 'REDUCE', 'EXIT'], 'days': market_gate_days}, 'sample_validity': {'is_valid': sample_valid, 'sample_status': status if status == 'INSUFFICIENT_SAMPLE' else 'VALID' if sample_valid else 'INSUFFICIENT', 'simulation_start_date': sim_start_date, 'simulation_end_date': sim_end_date, 'simulation_days': simulation_days, 'total_trades': total_trades, 'completed_trades': completed_trades, 'sim_end_trades': sim_end_count, 'sim_end_ratio_pct': round(sim_end_ratio * 100, 1), 'invalid_trades': len(invalid_trades), 'minimum_required': {'sim_days': 252, 'trades': 20, 'sim_end_ratio_pct': 50, 'invalid': 0}}, 'skipped_orders_by_reason': skip_reasons, 'initial_capital': init_cap, 'final_equity': round(final_equity, 2), 'total_return_pct': round(total_return, 2), 'cagr_pct': round(cagr, 2), 'max_drawdown_pct': round(max_dd * 100, 2), 'win_rate_pct': round(len(wins) / len(rets) * 100, 1) if rets else 0, 'profit_factor': pf, 'sharpe_ratio': sharpe, 'number_of_trades': total_trades, 'avg_holding_days': round(avg_h, 1), 'avg_winner_pct': round(sum(wins) / len(wins), 2) if wins else 0, 'avg_loser_pct': round(sum(losses) / len(losses), 2) if losses else 0, 'exposure_pct': exposure, 'spx_total_return_pct': spx_total, 'spx_cagr_pct': spx_cagr, 'alpha_pct': round(total_return - spx_total, 2), 'pending_orders_executed': orders_executed, 'pending_orders_skipped': sum(skip_reasons.values()), 'portfolio_action_distribution': portfolio_action_dist, 'executed_exit_reason_distribution': executed_exit_reason_dist, 'executed_reduce_reason_distribution': executed_reduce_reason_dist, 'pending_signal_reason_distribution': pending_signal_reason_dist, 'avg_execution_drag_pct': round(sum((t.get('total_execution_drag_pct', 0) for t in closed_trades)) / len(closed_trades), 3) if closed_trades else 0, 'p0_passed': len(invalid_trades) == 0 and reasonable, 'invalid_trades_count': len(invalid_trades), 'invalid_trades': invalid_trades[:10], 'equity_curve': [round(e, 2) for e in equity_curve[::5]], 'spx_curve': [round(e * init_cap, 2) for e in spx_curve[::5]], 'daily_records': daily_records, 'daily_equity_records': daily_equity_records, 'daily_equity_record_count': len(daily_equity_records), 'sim_end_liquidation_record': sim_end_liquidation_record, 'e1r_candidates': e1r_candidate_records if e1r_shell_mode else [], 'e1r_candidate_count': len(e1r_candidate_records) if e1r_shell_mode else 0, 'e1r_uptrend_execution_enabled': e1r_uptrend_execution_enabled, 'trades': closed_trades, 'total_trades_all': total_trades}",
        "'UNCLASSIFIED'",
        "'UNCLASSIFIED_NO_RISK_EXPANSION'",
        "{'mode': 'UNCLASSIFIED_DEFENSIVE', 'max_positions': 0, 'max_total_exposure_pct': 0.0}",
        "max(weights.items(), key=lambda kv: kv[1])[0]",
        "m",
        "lookup.get(date, fallback)",
        "data[i]",
        "data[:end_idx + 1]",
        "{'layer': 'D', 'name': 'Stateful Portfolio Backtest', 'status': 'NO_TRADES', 'skipped_orders_by_reason': skip_reasons}",
        "'N/A'",
        "rec.get('regime') or rec.get('spx_regime') or rec.get('weekly_regime') or 'UNCLASSIFIED'",
        "rec",
        "'UPTREND_EMERGING_CONFIRMED_ENABLED'",
        "'SIDEWAYS_QUALITY_BREAKOUT_ONLY'",
        "'DOWNTREND_EXCEPTION_ONLY'",
        "'N/A'",
        "{'mode': 'UPTREND_RISK_ON', 'max_positions': 3, 'max_total_exposure_pct': 100.0}",
        "{'mode': 'SIDEWAYS_LIMITED', 'max_positions': 2, 'max_total_exposure_pct': 33.3}",
        "{'mode': 'DOWNTREND_DEFENSIVE', 'max_positions': 1, 'max_total_exposure_pct': 10.0}"
      ]
    },
    {
      "name": "run_strategy_variant_comparison",
      "type": "FunctionDef",
      "line": 2489,
      "end_line": 2895,
      "matched_terms": [
        "E1R_REGIME_AWARE_V0_2",
        "build_e1r_sidecar_sleeve",
        "compose_e1r_v0_2_variant",
        "core_variant_result",
        "daily_equity_records",
        "run_stateful_simulation",
        "run_strategy_variant_comparison",
        "sidecar_result",
        "variant_results"
      ],
      "assignments_of_interest": [
        {
          "target": "_e1r_regime_daily",
          "value": "_load_e1r_regime_daily()"
        },
        {
          "target": "variants",
          "value": "{'E1_AUDITED_G4_MINHOLD10': {**base, **_gate_g4, 'strategy_variant': 'E1_audited_g4_minhold10', 'min_holding_days': 10, 'dynamic_exit_enabled': False, 'relative_stop_enabled': False, 'version': 'E1-audited-g4-minhold10'}, 'E1R_REGIME_AWARE_V0_1': {**base, **_gate_g4, 'strategy_variant': 'E1R_regime_aware_v0_1_shell', 'min_holding_days': 10, 'dynamic_exit_enabled': False, 'relative_stop_enabled': False, 'version': 'E1R-uptrend-execution-v0.1', 'e1r_shell_mode': True, 'e1r_uptrend_execution_enabled': True, 'e1r_regime_wiring_enabled': True, 'e1r_regime_daily': _e1r_regime_daily, 'e1r_regime_source': 'data/research/e1_5y/regimes/spx_regime_daily.json', 'e1r_spec_ref': 'docs/research/E1R_REGIME_AWARE_STRATEGY_SPEC_v0.1.md'}, 'E2_DYNAMIC_EXIT_V2': {**base, **_gate_g4, 'strategy_variant': 'E2_dynamic_exit_v2', 'min_holding_days': 0, 'dynamic_exit_enabled': True, 'relative_stop_enabled': False, 'version': 'E2-dynamic-exit-v2'}}"
        },
        {
          "target": "variant_results",
          "value": "period_results[_full_period_key]['variants']"
        },
        {
          "target": "comparison_rows",
          "value": "[]"
        },
        {
          "target": "daily",
          "value": "obj.get('daily_regime', obj) if isinstance(obj, dict) else {}"
        },
        {
          "target": "_core_e1r",
          "value": "variant_results.get('E1R_REGIME_AWARE_V0_1')"
        },
        {
          "target": "_core_records",
          "value": "(_core_e1r or {}).get('daily_equity_records', []) if _core_e1r else []"
        },
        {
          "target": "period_results[period_key]['variants'][variant_id]",
          "value": "_result"
        },
        {
          "target": "_sidecar_cfg",
          "value": "E1RSidecarConfig(start_date=_core_records[0]['date'], end_date=_core_records[-1]['date'], allowed_subclasses=('MA_CONFLICT',), top_n=10, gross_exposure=0.25, min_history_days=200, min_price=5.0, initial_equity=float(base.get('initial_capital', 100000)), excluded_symbols=('VIXY',))"
        },
        {
          "target": "_sidecar_result",
          "value": "build_e1r_sidecar_sleeve(stock_dir=_stock_dir, spx_path=_spx_path, regime_path=_regime_path, config=_sidecar_cfg)"
        },
        {
          "target": "variant_results['E1R_REGIME_AWARE_V0_2']",
          "value": "compose_e1r_v0_2_variant(core_variant_result=_core_e1r, sidecar_result=_sidecar_result, initial_equity=float(base.get('initial_capital', 100000)))"
        },
        {
          "target": "_sidecar_summary",
          "value": "_sidecar_result.get('summary', {}) or {}"
        }
      ],
      "returns": [
        "{**selected_result, 'name': 'Strategy Variant Comparison', 'version': 'v1.6-ls60-mode-comparison', 'selected_variant': selected_id, 'selection_policy': 'status(PASS>PARTIAL>FAIL), then total return, then profit factor, then Sharpe, then lower max drawdown', 'comparison': comparison_rows, 'variant_results': variant_results, 'period_comparison': {pk: {'label': pv['label'], 'variants': {vid: {'status': r.get('status'), 'total_return_pct': r.get('total_return_pct'), 'alpha_pct': r.get('alpha_pct'), 'cagr_pct': r.get('cagr_pct'), 'max_drawdown_pct': r.get('max_drawdown_pct'), 'profit_factor': r.get('profit_factor'), 'sharpe_ratio': r.get('sharpe_ratio'), 'number_of_trades': r.get('number_of_trades'), 'win_rate_pct': r.get('win_rate_pct'), 'avg_holding_days': r.get('avg_holding_days'), 'simulation_days': r.get('sample_validity', {}).get('simulation_days'), 'sim_start_date': r.get('sample_validity', {}).get('simulation_start_date'), 'sim_end_date': r.get('sample_validity', {}).get('simulation_end_date')} for (vid, r) in pv['variants'].items()}} for (pk, pv) in period_results.items()}}",
        "daily if isinstance(daily, dict) else {}",
        "(status_rank.get(result.get('status'), 0), result.get('alpha_pct', -10000), result.get('profit_factor', -10000), result.get('total_return_pct', -10000), result.get('sharpe_ratio', -10000), -result.get('max_drawdown_pct', 10000))",
        "{}",
        "{}"
      ]
    },
    {
      "name": "run_full_backtest",
      "type": "FunctionDef",
      "line": 2904,
      "end_line": 2978,
      "matched_terms": [
        "run_strategy_variant_comparison"
      ],
      "assignments_of_interest": [],
      "returns": [
        "{'overall_status': overall, 'methodology': 'Backtest Methodology v1.0', 'model_version': 'Quantitative Model Spec v1.0 (Frozen)', 'results': results}"
      ]
    }
  ]
}
```

## Grep Context

```json
{
  "scripts/export_canonical_5y_equity_curves.py": {
    "hit_count": 38,
    "hits": [
      {
        "line": 128,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 125,
            "text": "        result[\"module\"] = \"src.engine.e1r_composer\""
          },
          {
            "line": 126,
            "text": "        result[\"functions\"] = {}"
          },
          {
            "line": 127,
            "text": "        for name in ["
          },
          {
            "line": 128,
            "text": "            \"build_equity_records_from_returns\","
          },
          {
            "line": 129,
            "text": "            \"extract_core_interval_returns\","
          },
          {
            "line": 130,
            "text": "            \"compound_return\","
          },
          {
            "line": 131,
            "text": "            \"max_drawdown\","
          }
        ]
      },
      {
        "line": 129,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 126,
            "text": "        result[\"functions\"] = {}"
          },
          {
            "line": 127,
            "text": "        for name in ["
          },
          {
            "line": 128,
            "text": "            \"build_equity_records_from_returns\","
          },
          {
            "line": 129,
            "text": "            \"extract_core_interval_returns\","
          },
          {
            "line": 130,
            "text": "            \"compound_return\","
          },
          {
            "line": 131,
            "text": "            \"max_drawdown\","
          },
          {
            "line": 132,
            "text": "            \"sharpe_ratio\","
          }
        ]
      },
      {
        "line": 152,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 149,
            "text": ""
          },
          {
            "line": 150,
            "text": ""
          },
          {
            "line": 151,
            "text": "def run_build_equity_smoke(composer: Any) -> Dict[str, Any]:"
          },
          {
            "line": 152,
            "text": "    fn = getattr(composer, \"build_equity_records_from_returns\", None)"
          },
          {
            "line": 153,
            "text": "    if fn is None:"
          },
          {
            "line": 154,
            "text": "        return {\"ok\": False, \"error\": \"build_equity_records_from_returns not found\"}"
          },
          {
            "line": 155,
            "text": ""
          }
        ]
      },
      {
        "line": 154,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 151,
            "text": "def run_build_equity_smoke(composer: Any) -> Dict[str, Any]:"
          },
          {
            "line": 152,
            "text": "    fn = getattr(composer, \"build_equity_records_from_returns\", None)"
          },
          {
            "line": 153,
            "text": "    if fn is None:"
          },
          {
            "line": 154,
            "text": "        return {\"ok\": False, \"error\": \"build_equity_records_from_returns not found\"}"
          },
          {
            "line": 155,
            "text": ""
          },
          {
            "line": 156,
            "text": "    attempts = []"
          },
          {
            "line": 157,
            "text": ""
          }
        ]
      },
      {
        "line": 230,
        "matched": [
          "e1r_v0_2_backtest_summary.json"
        ],
        "context": [
          {
            "line": 227,
            "text": "    source_files = ["
          },
          {
            "line": 228,
            "text": "        ROOT / \"data/research/e1r/e1r_formal_backtest_v0_1.json\","
          },
          {
            "line": 229,
            "text": "        ROOT / \"exports/portfolio_backtest.json\","
          },
          {
            "line": 230,
            "text": "        ROOT / \"exports/e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 231,
            "text": "        ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 232,
            "text": "        ROOT / \"exports/oos_e1r_v0_2_equity_curve.json\","
          },
          {
            "line": 233,
            "text": "        ROOT / \"exports/oos_equity_curve.json\","
          }
        ]
      },
      {
        "line": 231,
        "matched": [
          "equity_curve",
          "e1r_v0_2_backtest_equity_curve.json"
        ],
        "context": [
          {
            "line": 228,
            "text": "        ROOT / \"data/research/e1r/e1r_formal_backtest_v0_1.json\","
          },
          {
            "line": 229,
            "text": "        ROOT / \"exports/portfolio_backtest.json\","
          },
          {
            "line": 230,
            "text": "        ROOT / \"exports/e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 231,
            "text": "        ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 232,
            "text": "        ROOT / \"exports/oos_e1r_v0_2_equity_curve.json\","
          },
          {
            "line": 233,
            "text": "        ROOT / \"exports/oos_equity_curve.json\","
          },
          {
            "line": 234,
            "text": "        ROOT / \"data/research/e1_5y/regimes/spx_regime_daily.json\","
          }
        ]
      },
      {
        "line": 232,
        "matched": [
          "equity_curve"
        ],
        "context": [
          {
            "line": 229,
            "text": "        ROOT / \"exports/portfolio_backtest.json\","
          },
          {
            "line": 230,
            "text": "        ROOT / \"exports/e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 231,
            "text": "        ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 232,
            "text": "        ROOT / \"exports/oos_e1r_v0_2_equity_curve.json\","
          },
          {
            "line": 233,
            "text": "        ROOT / \"exports/oos_equity_curve.json\","
          },
          {
            "line": 234,
            "text": "        ROOT / \"data/research/e1_5y/regimes/spx_regime_daily.json\","
          },
          {
            "line": 235,
            "text": "        ROOT / \"data/research/e1_5y/raw/indices/SPX.json\","
          }
        ]
      },
      {
        "line": 233,
        "matched": [
          "equity_curve"
        ],
        "context": [
          {
            "line": 230,
            "text": "        ROOT / \"exports/e1r_v0_2_backtest_summary.json\","
          },
          {
            "line": 231,
            "text": "        ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\","
          },
          {
            "line": 232,
            "text": "        ROOT / \"exports/oos_e1r_v0_2_equity_curve.json\","
          },
          {
            "line": 233,
            "text": "        ROOT / \"exports/oos_equity_curve.json\","
          },
          {
            "line": 234,
            "text": "        ROOT / \"data/research/e1_5y/regimes/spx_regime_daily.json\","
          },
          {
            "line": 235,
            "text": "        ROOT / \"data/research/e1_5y/raw/indices/SPX.json\","
          },
          {
            "line": 236,
            "text": "    ]"
          }
        ]
      },
      {
        "line": 278,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 275,
            "text": ""
          },
          {
            "line": 276,
            "text": "    return {"
          },
          {
            "line": 277,
            "text": "        \"composer_import_ok\": True,"
          },
          {
            "line": 278,
            "text": "        \"build_equity_records_from_returns\": build_smoke,"
          },
          {
            "line": 279,
            "text": "        \"utility_functions\": utility_smoke,"
          },
          {
            "line": 280,
            "text": "    }"
          },
          {
            "line": 281,
            "text": ""
          }
        ]
      },
      {
        "line": 291,
        "matched": [
          "daily_equity_records"
        ],
        "context": [
          {
            "line": 288,
            "text": "    This function intentionally does not write canonical exports."
          },
          {
            "line": 289,
            "text": "    It inspects whether the current repository has enough persisted inputs"
          },
          {
            "line": 290,
            "text": "    to generate E1R 5Y interval records:"
          },
          {
            "line": 291,
            "text": "      core_daily_equity_records + sidecar_records"
          },
          {
            "line": 292,
            "text": "      -> extract_core_interval_returns(...)"
          },
          {
            "line": 293,
            "text": "      -> build_equity_records_from_returns(...)"
          },
          {
            "line": 294,
            "text": "    \"\"\""
          }
        ]
      },
      {
        "line": 292,
        "matched": [
          "extract_core_interval_returns"
        ],
        "context": [
          {
            "line": 289,
            "text": "    It inspects whether the current repository has enough persisted inputs"
          },
          {
            "line": 290,
            "text": "    to generate E1R 5Y interval records:"
          },
          {
            "line": 291,
            "text": "      core_daily_equity_records + sidecar_records"
          },
          {
            "line": 292,
            "text": "      -> extract_core_interval_returns(...)"
          },
          {
            "line": 293,
            "text": "      -> build_equity_records_from_returns(...)"
          },
          {
            "line": 294,
            "text": "    \"\"\""
          },
          {
            "line": 295,
            "text": "    from src.engine import e1r_composer as composer  # type: ignore"
          }
        ]
      },
      {
        "line": 293,
        "matched": [
          "build_equity_records_from_returns"
        ],
        "context": [
          {
            "line": 290,
            "text": "    to generate E1R 5Y interval records:"
          },
          {
            "line": 291,
            "text": "      core_daily_equity_records + sidecar_records"
          },
          {
            "line": 292,
            "text": "      -> extract_core_interval_returns(...)"
          },
          {
            "line": 293,
            "text": "      -> build_equity_records_from_returns(...)"
          },
          {
            "line": 294,
            "text": "    \"\"\""
          },
          {
            "line": 295,
            "text": "    from src.engine import e1r_composer as composer  # type: ignore"
          },
          {
            "line": 296,
            "text": ""
          }
        ]
      },
      {
        "line": 344,
        "matched": [
          "daily_records"
        ],
        "context": [
          {
            "line": 341,
            "text": "            source_summary[bucket].append(shape)"
          },
          {
            "line": 342,
            "text": ""
          },
          {
            "line": 343,
            "text": "    portfolio = read_json(ROOT / \"exports/portfolio_backtest.json\", default={})"
          },
          {
            "line": 344,
            "text": "    append_if_list(\"core_sources\", \"exports/portfolio_backtest.json.daily_records\", portfolio.get(\"daily_records\"))"
          },
          {
            "line": 345,
            "text": "    variant_results = portfolio.get(\"variant_results\") if isinstance(portfolio, dict) else {}"
          },
          {
            "line": 346,
            "text": "    if isinstance(variant_results, dict):"
          },
          {
            "line": 347,
            "text": "        for variant, obj in variant_results.items():"
          }
        ]
      },
      {
        "line": 345,
        "matched": [
          "variant_results"
        ],
        "context": [
          {
            "line": 342,
            "text": ""
          },
          {
            "line": 343,
            "text": "    portfolio = read_json(ROOT / \"exports/portfolio_backtest.json\", default={})"
          },
          {
            "line": 344,
            "text": "    append_if_list(\"core_sources\", \"exports/portfolio_backtest.json.daily_records\", portfolio.get(\"daily_records\"))"
          },
          {
            "line": 345,
            "text": "    variant_results = portfolio.get(\"variant_results\") if isinstance(portfolio, dict) else {}"
          },
          {
            "line": 346,
            "text": "    if isinstance(variant_results, dict):"
          },
          {
            "line": 347,
            "text": "        for variant, obj in variant_results.items():"
          },
          {
            "line": 348,
            "text": "            if isinstance(obj, dict):"
          }
        ]
      },
      {
        "line": 346,
        "matched": [
          "variant_results"
        ],
        "context": [
          {
            "line": 343,
            "text": "    portfolio = read_json(ROOT / \"exports/portfolio_backtest.json\", default={})"
          },
          {
            "line": 344,
            "text": "    append_if_list(\"core_sources\", \"exports/portfolio_backtest.json.daily_records\", portfolio.get(\"daily_records\"))"
          },
          {
            "line": 345,
            "text": "    variant_results = portfolio.get(\"variant_results\") if isinstance(portfolio, dict) else {}"
          },
          {
            "line": 346,
            "text": "    if isinstance(variant_results, dict):"
          },
          {
            "line": 347,
            "text": "        for variant, obj in variant_results.items():"
          },
          {
            "line": 348,
            "text": "            if isinstance(obj, dict):"
          },
          {
            "line": 349,
            "text": "                append_if_list(\"core_sources\", f\"exports/portfolio_backtest.json.variant_results.{variant}.daily_records\", obj.get(\"daily_records\"))"
          }
        ]
      },
      {
        "line": 347,
        "matched": [
          "variant_results"
        ],
        "context": [
          {
            "line": 344,
            "text": "    append_if_list(\"core_sources\", \"exports/portfolio_backtest.json.daily_records\", portfolio.get(\"daily_records\"))"
          },
          {
            "line": 345,
            "text": "    variant_results = portfolio.get(\"variant_results\") if isinstance(portfolio, dict) else {}"
          },
          {
            "line": 346,
            "text": "    if isinstance(variant_results, dict):"
          },
          {
            "line": 347,
            "text": "        for variant, obj in variant_results.items():"
          },
          {
            "line": 348,
            "text": "            if isinstance(obj, dict):"
          },
          {
            "line": 349,
            "text": "                append_if_list(\"core_sources\", f\"exports/portfolio_backtest.json.variant_results.{variant}.daily_records\", obj.get(\"daily_records\"))"
          },
          {
            "line": 350,
            "text": ""
          }
        ]
      },
      {
        "line": 349,
        "matched": [
          "daily_records",
          "variant_results"
        ],
        "context": [
          {
            "line": 346,
            "text": "    if isinstance(variant_results, dict):"
          },
          {
            "line": 347,
            "text": "        for variant, obj in variant_results.items():"
          },
          {
            "line": 348,
            "text": "            if isinstance(obj, dict):"
          },
          {
            "line": 349,
            "text": "                append_if_list(\"core_sources\", f\"exports/portfolio_backtest.json.variant_results.{variant}.daily_records\", obj.get(\"daily_records\"))"
          },
          {
            "line": 350,
            "text": ""
          },
          {
            "line": 351,
            "text": "    oos_e1 = read_json(ROOT / \"exports/oos_equity_curve.json\", default={})"
          },
          {
            "line": 352,
            "text": "    if isinstance(oos_e1, dict):"
          }
        ]
      },
      {
        "line": 351,
        "matched": [
          "equity_curve"
        ],
        "context": [
          {
            "line": 348,
            "text": "            if isinstance(obj, dict):"
          },
          {
            "line": 349,
            "text": "                append_if_list(\"core_sources\", f\"exports/portfolio_backtest.json.variant_results.{variant}.daily_records\", obj.get(\"daily_records\"))"
          },
          {
            "line": 350,
            "text": ""
          },
          {
            "line": 351,
            "text": "    oos_e1 = read_json(ROOT / \"exports/oos_equity_curve.json\", default={})"
          },
          {
            "line": 352,
            "text": "    if isinstance(oos_e1, dict):"
          },
          {
            "line": 353,
            "text": "        append_if_list(\"core_sources\", \"exports/oos_equity_curve.json.curve\", oos_e1.get(\"curve\"))"
          },
          {
            "line": 354,
            "text": ""
          }
        ]
      },
      {
        "line": 353,
        "matched": [
          "equity_curve"
        ],
        "context": [
          {
            "line": 350,
            "text": ""
          },
          {
            "line": 351,
            "text": "    oos_e1 = read_json(ROOT / \"exports/oos_equity_curve.json\", default={})"
          },
          {
            "line": 352,
            "text": "    if isinstance(oos_e1, dict):"
          },
          {
            "line": 353,
            "text": "        append_if_list(\"core_sources\", \"exports/oos_equity_curve.json.curve\", oos_e1.get(\"curve\"))"
          },
          {
            "line": 354,
            "text": ""
          },
          {
            "line": 355,
            "text": "    e1r_diag = read_json(ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\", default={})"
          },
          {
            "line": 356,
            "text": "    if isinstance(e1r_diag, dict):"
          }
        ]
      },
      {
        "line": 355,
        "matched": [
          "equity_curve",
          "e1r_v0_2_backtest_equity_curve.json"
        ],
        "context": [
          {
            "line": 352,
            "text": "    if isinstance(oos_e1, dict):"
          },
          {
            "line": 353,
            "text": "        append_if_list(\"core_sources\", \"exports/oos_equity_curve.json.curve\", oos_e1.get(\"curve\"))"
          },
          {
            "line": 354,
            "text": ""
          },
          {
            "line": 355,
            "text": "    e1r_diag = read_json(ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\", default={})"
          },
          {
            "line": 356,
            "text": "    if isinstance(e1r_diag, dict):"
          },
          {
            "line": 357,
            "text": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.rows\", e1r_diag.get(\"rows\"))"
          },
          {
            "line": 358,
            "text": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.equity_curve\", e1r_diag.get(\"equity_curve\"))"
          }
        ]
      },
      {
        "line": 357,
        "matched": [
          "equity_curve",
          "e1r_v0_2_backtest_equity_curve.json"
        ],
        "context": [
          {
            "line": 354,
            "text": ""
          },
          {
            "line": 355,
            "text": "    e1r_diag = read_json(ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\", default={})"
          },
          {
            "line": 356,
            "text": "    if isinstance(e1r_diag, dict):"
          },
          {
            "line": 357,
            "text": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.rows\", e1r_diag.get(\"rows\"))"
          },
          {
            "line": 358,
            "text": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.equity_curve\", e1r_diag.get(\"equity_curve\"))"
          },
          {
            "line": 359,
            "text": ""
          },
          {
            "line": 360,
            "text": "    sidecar = read_json(ROOT / \"exports/oos_e1r_v0_2_sidecar.json\", default={})"
          }
        ]
      },
      {
        "line": 358,
        "matched": [
          "equity_curve",
          "e1r_v0_2_backtest_equity_curve.json"
        ],
        "context": [
          {
            "line": 355,
            "text": "    e1r_diag = read_json(ROOT / \"exports/e1r_v0_2_backtest_equity_curve.json\", default={})"
          },
          {
            "line": 356,
            "text": "    if isinstance(e1r_diag, dict):"
          },
          {
            "line": 357,
            "text": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.rows\", e1r_diag.get(\"rows\"))"
          },
          {
            "line": 358,
            "text": "        append_if_list(\"core_sources\", \"exports/e1r_v0_2_backtest_equity_curve.json.equity_curve\", e1r_diag.get(\"equity_curve\"))"
          },
          {
            "line": 359,
            "text": ""
          },
          {
            "line": 360,
            "text": "    sidecar = read_json(ROOT / \"exports/oos_e1r_v0_2_sidecar.json\", default={})"
          },
          {
            "line": 361,
            "text": "    if isinstance(sidecar, dict):"
          }
        ]
      },
      {
        "line": 381,
        "matched": [
          "daily_records"
        ],
        "context": [
          {
            "line": 378,
            "text": "    ]"
          },
          {
            "line": 379,
            "text": ""
          },
          {
            "line": 380,
            "text": "    def resolve_rows(label: str) -> Any:"
          },
          {
            "line": 381,
            "text": "        if label == \"exports/portfolio_backtest.json.daily_records\":"
          },
          {
            "line": 382,
            "text": "            return portfolio.get(\"daily_records\")"
          },
          {
            "line": 383,
            "text": "        if label.startswith(\"exports/portfolio_backtest.json.variant_results.\"):"
          },
          {
            "line": 384,
            "text": "            parts = label.split(\".\")"
          }
        ]
      },
      {
        "line": 382,
        "matched": [
          "daily_records"
        ],
        "context": [
          {
            "line": 379,
            "text": ""
          },
          {
            "line": 380,
            "text": "    def resolve_rows(label: str) -> Any:"
          },
          {
            "line": 381,
            "text": "        if label == \"exports/portfolio_backtest.json.daily_records\":"
          },
          {
            "line": 382,
            "text": "            return portfolio.get(\"daily_records\")"
          },
          {
            "line": 383,
            "text": "        if label.startswith(\"exports/portfolio_backtest.json.variant_results.\"):"
          },
          {
            "line": 384,
            "text": "            parts = label.split(\".\")"
          },
          {
            "line": 385,
            "text": "            variant = parts[3]"
          }
        ]
      },
      {
        "line": 383,
        "matched": [
          "variant_results"
        ],
        "context": [
          {
            "line": 380,
            "text": "    def resolve_rows(label: str) -> Any:"
          },
          {
            "line": 381,
            "text": "        if label == \"exports/portfolio_backtest.json.daily_records\":"
          },
          {
            "line": 382,
            "text": "            return portfolio.get(\"daily_records\")"
          },
          {
            "line": 383,
            "text": "        if label.startswith(\"exports/portfolio_backtest.json.variant_results.\"):"
          },
          {
            "line": 384,
            "text": "            parts = label.split(\".\")"
          },
          {
            "line": 385,
            "text": "            variant = parts[3]"
          },
          {
            "line": 386,
            "text": "            return variant_results.get(variant, {}).get(\"daily_records\")"
          }
        ]
      },
      {
        "line": 386,
        "matched": [
          "daily_records",
          "variant_results"
        ],
        "context": [
          {
            "line": 383,
            "text": "        if label.startswith(\"exports/portfolio_backtest.json.variant_results.\"):"
          },
          {
            "line": 384,
            "text": "            parts = label.split(\".\")"
          },
          {
            "line": 385,
            
```

## Next Stage

- `Stage 3.8E-2F-2C-4C-10F-4B-0H`: Runtime return-shape probe for compose_e1r_v0_2_variant
- Recommended action: Next run a narrow runtime-return probe around compose_e1r_v0_2_variant to print actual return keys/list lengths without writing canonical exports.

