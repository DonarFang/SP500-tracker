# E1R 4C-2C-4E-ENGINE-B-R1 — Normalized Input / Data Adapter Contract Audit

Generated At: `2026-07-10T05:16:43.030360+00:00`

## Policy
```json
{
  "strategy_logic_changed": false,
  "contract_audit_only": true,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "adapter_implementation_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "frozen_strategy_files_changed": false,
  "invalid_artifacts_used_as_source": false,
  "composer_used": false,
  "return_curve_stitching_used": false
}
```

## Data Inventory Summary
```json
{
  "research_stocks": {
    "path": "data/research/e1_5y/raw/stocks",
    "exists": true,
    "json_count": 542,
    "sample_files": [
      "A.json",
      "AAL.json",
      "AAPL.json",
      "ABBV.json",
      "ABNB.json",
      "ABT.json",
      "ACGL.json",
      "ACN.json",
      "ADBE.json",
      "ADI.json"
    ],
    "sample_shapes": [
      {
        "path": "data/research/e1_5y/raw/stocks/A.json",
        "exists": true,
        "type": "dict",
        "top_level_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "formal_pass_fail_allowed",
          "price_adjustment",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "survivorship_bias",
          "symbol",
          "yahoo_ticker"
        ],
        "date_keyed_dict": false,
        "date_key_sample": [],
        "has_symbol": true
      },
      {
        "path": "data/research/e1_5y/raw/stocks/AAL.json",
        "exists": true,
        "type": "dict",
        "top_level_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "formal_pass_fail_allowed",
          "price_adjustment",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "survivorship_bias",
          "symbol",
          "yahoo_ticker"
        ],
        "date_keyed_dict": false,
        "date_key_sample": [],
        "has_symbol": true
      },
      {
        "path": "data/research/e1_5y/raw/stocks/AAPL.json",
        "exists": true,
        "type": "dict",
        "top_level_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "formal_pass_fail_allowed",
          "price_adjustment",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "survivorship_bias",
          "symbol",
          "yahoo_ticker"
        ],
        "date_keyed_dict": false,
        "date_key_sample": [],
        "has_symbol": true
      }
    ]
  },
  "research_indices": {
    "path": "data/research/e1_5y/raw/indices",
    "exists": true,
    "json_count": 3,
    "sample_files": [
      "NDX.json",
      "SOX.json",
      "SPX.json"
    ],
    "sample_shapes": [
      {
        "path": "data/research/e1_5y/raw/indices/NDX.json",
        "exists": true,
        "type": "dict",
        "top_level_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "symbol",
          "yahoo_ticker"
        ],
        "date_keyed_dict": false,
        "date_key_sample": [],
        "has_symbol": true
      },
      {
        "path": "data/research/e1_5y/raw/indices/SOX.json",
        "exists": true,
        "type": "dict",
        "top_level_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "symbol",
          "yahoo_ticker"
        ],
        "date_keyed_dict": false,
        "date_key_sample": [],
        "has_symbol": true
      },
      {
        "path": "data/research/e1_5y/raw/indices/SPX.json",
        "exists": true,
        "type": "dict",
        "top_level_keys": [
          "bars",
          "data_end",
          "data_start",
          "dataset_mode",
          "downloaded_at",
          "requested_end",
          "requested_start",
          "schema_version",
          "source",
          "symbol",
          "yahoo_ticker"
        ],
        "date_keyed_dict": false,
        "date_key_sample": [],
        "has_symbol": true
      }
    ]
  },
  "research_regimes": {
    "path": "data/research/e1_5y/regimes",
    "exists": true,
    "json_count": 6,
    "sample_files": [
      "e1_equity_regime_attribution.json",
      "e1_regime_attribution.json",
      "regime_summary.json",
      "spx_regime_daily.json",
      "spx_regime_episodes.json",
      "spx_weekly_regimes.json"
    ],
    "sample_shapes": [
      {
        "path": "data/research/e1_5y/regimes/e1_equity_regime_attribution.json",
        "exists": true,
        "type": "dict",
        "top_level_keys": [
          "by_regime",
          "daily_equity_record_count",
          "input",
          "record_count",
          "sim_end_liquidation_included",
          "status",
          "strategy_id",
          "total_pnl_usd",
          "total_return_pct_of_initial"
        ],
        "date_keyed_dict": false,
        "date_key_sample": []
      },
      {
        "path": "data/research/e1_5y/regimes/e1_regime_attribution.json",
        "exists": true,
        "type": "dict",
        "top_level_keys": [
          "attribution_by_dominant_regime",
          "attribution_by_entry_regime",
          "cross_regime_count",
          "dataset_note",
          "generated_at",
          "method",
          "tagged_trades",
          "trade_count"
        ],
        "date_keyed_dict": false,
        "date_key_sample": []
      },
      {
        "path": "data/research/e1_5y/regimes/regime_summary.json",
        "exists": true,
        "type": "dict",
        "top_level_keys": [
          "episode_count_by_regime",
          "generated_at",
          "note",
          "pass_checks",
          "regime_days",
          "regime_pct",
          "spec_version",
          "subclass_days",
          "total_episodes",
          "total_trading_days",
          "unclassified_days",
          "validation_window"
        ],
        "date_keyed_dict": false,
        "date_key_sample": []
      }
    ]
  },
  "prod_prices": {
    "path": "data/prices",
    "exists": true,
    "json_count": 498,
    "sample_files": [
      "A.json",
      "AAL.json",
      "AAPL.json",
      "ABBV.json",
      "ABNB.json",
      "ABT.json",
      "ACGL.json",
      "ACN.json",
      "ADBE.json",
      "ADI.json"
    ],
    "sample_shapes": [
      {
        "path": "data/prices/A.json",
        "exists": true,
        "type": "list",
        "list_len": 789,
        "sample": [
          {
            "date": "2023-05-16",
            "open": 124.1,
            "high": 124.53,
            "low": 122.95,
            "close": 123.44,
            "volume": 1190000.0
          }
        ],
        "sample_keys": [
          "close",
          "date",
          "high",
          "low",
          "open",
          "volume"
        ],
        "sample_key_frequency": {
          "date": 100,
          "open": 100,
          "high": 100,
          "low": 100,
          "close": 100,
          "volume": 100
        }
      },
      {
        "path": "data/prices/AAL.json",
        "exists": true,
        "type": "list",
        "list_len": 789,
        "sample": [
          {
            "date": "2023-05-16",
            "open": 14.21,
            "high": 14.45,
            "low": 13.97,
            "close": 14.2,
            "volume": 20303200.0
          }
        ],
        "sample_keys": [
          "close",
          "date",
          "high",
          "low",
          "open",
          "volume"
        ],
        "sample_key_frequency": {
          "date": 100,
          "open": 100,
          "high": 100,
          "low": 100,
          "close": 100,
          "volume": 100
        }
      },
      {
        "path": "data/prices/AAPL.json",
        "exists": true,
        "type": "list",
        "list_len": 789,
        "sample": [
          {
            "date": "2023-05-16",
            "open": 169.61,
            "high": 170.75,
            "low": 169.42,
            "close": 169.69,
            "volume": 42110300.0
          }
        ],
        "sample_keys": [
          "close",
          "date",
          "high",
          "low",
          "open",
          "volume"
        ],
        "sample_key_frequency": {
          "date": 100,
          "open": 100,
          "high": 100,
          "low": 100,
          "close": 100,
          "volume": 100
        }
      }
    ]
  }
}
```

## Loader Candidate Summary
```json
{
  "candidate_count": 287,
  "top_candidates": [
    {
      "path": "src/engine/backtest.py",
      "name": "run_strategy_variant_comparison",
      "start_line": 2489,
      "end_line": 2895,
      "line_count": 407,
      "args": [
        "symbols",
        "prices_map",
        "dates_map",
        "spx_prices",
        "spx_dates",
        "ndx_prices",
        "ndx_dates",
        "sox_prices",
        "sox_dates",
        "vix_prices",
        "vix_dates"
      ],
      "score": 23,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:json.load",
        "contains:json.loads",
        "contains:prices_map",
        "contains:dates_map",
        "contains:data/research/e1_5y",
        "contains:SPX.json",
        "contains:spx_regime_daily",
        "contains:raw/stocks",
        "contains:raw/indices",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_research_5y_data",
        "uses_regime"
      ],
      "risks": []
    },
    {
      "path": "scripts/e1r_continuous_stateful_smoke_4c2c4e_b3.py",
      "name": "call_backtest_engine",
      "start_line": 371,
      "end_line": 423,
      "line_count": 53,
      "args": [
        "stock_dir",
        "regime_daily"
      ],
      "score": 16,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:load_stock",
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "src/engine/backtest.py",
      "name": "run_stateful_simulation",
      "start_line": 763,
      "end_line": 2486,
      "line_count": 1724,
      "args": [
        "symbols",
        "prices_map",
        "dates_map",
        "spx_prices",
        "spx_dates",
        "ohlc_map",
        "assumptions",
        "step",
        "min_history",
        "market_score_default",
        "sim_start_date",
        "sim_end_date",
        "ndx_prices",
        "ndx_dates",
        "sox_prices",
        "sox_dates",
        "vix_prices",
        "vix_dates"
      ],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/export_e1_5y_core_equity.py",
      "name": "main",
      "start_line": 295,
      "end_line": 514,
      "line_count": 220,
      "args": [],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:load_stock",
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/run_e1r_unified_5y_full_account_4c2c.py",
      "name": "main",
      "start_line": 679,
      "end_line": 890,
      "line_count": 212,
      "args": [],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_regime_wiring_4c2b4.py",
      "name": "main",
      "start_line": 497,
      "end_line": 703,
      "line_count": 207,
      "args": [],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_regime_wiring_trade_window_4c2b5.py",
      "name": "main",
      "start_line": 514,
      "end_line": 707,
      "line_count": 194,
      "args": [],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_4c2b.py",
      "name": "main",
      "start_line": 219,
      "end_line": 384,
      "line_count": 166,
      "args": [],
      "score": 14,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_4c2b1.py",
      "name": "main",
      "start_line": 319,
      "end_line": 481,
      "line_count": 163,
      "args": [],
      "score": 14,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_4c2b2.py",
      "name": "main",
      "start_line": 375,
      "end_line": 542,
      "line_count": 168,
      "args": [],
      "score": 14,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_4c2b3.py",
      "name": "main",
      "start_line": 385,
      "end_line": 569,
      "line_count": 185,
      "args": [],
      "score": 14,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/e1r_uptrend_provider_candidate_verification_4c2c4e_d2.py",
      "name": "classify_function",
      "start_line": 216,
      "end_line": 302,
      "line_count": 87,
      "args": [
        "src"
      ],
      "score": 13,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime"
      ],
      "risks": []
    },
    {
      "path": "src/engine/backtest.py",
      "name": "_load_e1r_regime_daily",
      "start_line": 2551,
      "end_line": 2562,
      "line_count": 12,
      "args": [],
      "score": 7,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:json.load",
        "contains:json.loads",
        "contains:data/research/e1_5y",
        "contains:spx_regime_daily",
        "uses_research_5y_data",
        "uses_regime"
      ],
      "risks": []
    },
    {
      "path": "src/data_ingestion/fetch_yahoo.py",
      "name": "load_prices",
      "start_line": 250,
      "end_line": 251,
      "line_count": 2,
      "args": [
        "sym"
      ],
      "score": 3,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:read_json",
        "contains:load_price",
        "contains:load_prices"
      ],
      "risks": []
    },
    {
      "path": "src/data_ingestion/fetch_yahoo.py",
      "name": "load_prices",
      "start_line": 569,
      "end_line": 570,
      "line_count": 2,
      "args": [
        "sym"
      ],
      "score": 3,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:read_json",
        "contains:load_price",
        "contains:load_prices"
      ],
      "risks": []
    },
    {
      "path": "src/engine/e1r_sidecar_sleeve.py",
      "name": "load_regimes",
      "start_line": 182,
      "end_line": 189,
      "line_count": 8,
      "args": [
        "path"
      ],
      "score": 3,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:json.load",
        "contains:json.loads",
        "uses_regime"
      ],
      "risks": []
    },
    {
      "path": "src/engine/e1r_sidecar_sleeve.py",
      "name": "load_asset",
      "start_line": 126,
      "end_line": 155,
      "line_count": 30,
      "args": [
        "path"
      ],
      "score": 2,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:json.load",
        "contains:json.loads"
      ],
      "risks": []
    },
    {
      "path": "src/engine/e1r_sidecar_sleeve.py",
      "name": "load_stock_universe",
      "start_line": 158,
      "end_line": 179,
      "line_count": 22,
      "args": [
        "stock_dir",
        "config"
      ],
      "score": 2,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:load_stock",
        "uses_symbols"
      ],
      "risks": []
    },
    {
      "path": "src/oos/event_store.py",
      "name": "load_all_events",
      "start_line": 67,
      "end_line": 80,
      "line_count": 14,
      "args": [],
      "score": 2,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:json.load",
        "contains:json.loads"
      ],
      "risks": []
    },
    {
      "path": "src/pipeline/update_pipeline.py",
      "name": "load_members_map",
      "start_line": 83,
      "end_line": 96,
      "line_count": 14,
      "args": [
        "symbols"
      ],
      "score": 2,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:read_json",
        "uses_symbols"
      ],
      "risks": []
    },
    {
      "path": "src/utils/helpers.py",
      "name": "read_json",
      "start_line": 6,
      "end_line": 10,
      "line_count": 5,
      "args": [
        "path"
      ],
      "score": 2,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:json.load",
        "contains:read_json"
      ],
      "risks": []
    },
    {
      "path": "src/data_ingestion/fetch_yahoo.py",
      "name": "fetch_members",
      "start_line": 121,
      "end_line": 137,
      "line_count": 17,
      "args": [],
      "score": 1,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:read_json"
      ],
      "risks": []
    },
    {
      "path": "src/data_ingestion/fetch_yahoo.py",
      "name": "download_bulk",
      "start_line": 167,
      "end_line": 196,
      "line_count": 30,
      "args": [
        "symbols",
        "start",
        "end",
        "batch_size",
        "sleep"
      ],
      "score": 1,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "uses_symbols"
      ],
      "risks": []
    },
    {
      "path": "src/data_ingestion/fetch_yahoo.py",
      "name": "fetch_members",
      "start_line": 440,
      "end_line": 456,
      "line_count": 17,
      "args": [],
      "score": 1,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "contains:read_json"
      ],
      "risks": []
    },
    {
      "path": "src/data_ingestion/fetch_yahoo.py",
      "name": "download_bulk",
      "start_line": 486,
      "end_line": 515,
      "line_count": 30,
      "args": [
        "symbols",
        "start",
        "end",
        "batch_size",
        "sleep"
      ],
      "score": 1,
      "classification": "RUNTIME_LOADER_CANDIDATE",
      "classification_rank": 90,
      "reasons": [
        "uses_symbols"
      ],
      "risks": []
    }
  ]
}
```

## Backtest Input Signature
```json
{
  "import_ok": true,
  "signature": "(symbols: 'list[str]', prices_map: 'dict[str, list[float]]', dates_map: 'dict[str, list[str]]', spx_prices: 'list[float]', spx_dates: 'list[str]', ohlc_map: 'dict' = None, assumptions: 'dict' = None, step: 'int' = 1, min_history: 'int' = 120, market_score_default: 'float' = 60.0, sim_start_date: 'str' = None, sim_end_date: 'str' = None, ndx_prices: 'list' = None, ndx_dates: 'list' = None, sox_prices: 'list' = None, sox_dates: 'list' = None, vix_prices: 'list' = None, vix_dates: 'list' = None) -> 'dict'",
  "parameters": [
    "symbols",
    "prices_map",
    "dates_map",
    "spx_prices",
    "spx_dates",
    "ohlc_map",
    "assumptions",
    "step",
    "min_history",
    "market_score_default",
    "sim_start_date",
    "sim_end_date",
    "ndx_prices",
    "ndx_dates",
    "sox_prices",
    "sox_dates",
    "vix_prices",
    "vix_dates"
  ],
  "required_core_inputs": [
    "symbols",
    "prices_map",
    "dates_map",
    "spx_prices",
    "spx_dates",
    "ohlc_map",
    "assumptions",
    "sim_start_date",
    "sim_end_date",
    "ndx_prices",
    "ndx_dates",
    "sox_prices",
    "sox_dates",
    "vix_prices",
    "vix_dates"
  ]
}
```

## Normalized Input Contract
```json
{
  "contract_name": "E1R_NORMALIZED_INPUT_DATA_ADAPTER_CONTRACT_V1",
  "reason": "Standalone E1R Engine requires one normalized input boundary shared by historical backtest, forward paper tracking, and future live trading. D4B-R1 showed ad hoc JSON parsing is unsafe.",
  "normalized_market_snapshot": {
    "date": "YYYY-MM-DD",
    "universe": "list[str]",
    "prices_by_symbol": {
      "symbol": {
        "close": "float",
        "history": "list[DailyBar]",
        "ohlc_optional": "open/high/low/close/volume if available"
      }
    },
    "indices": {
      "SPX": "required",
      "NDX": "required if available",
      "SOX": "required if available",
      "VIX": "explicit optional / fallback path"
    },
    "regime": {
      "spx_regime": "UPTREND | SIDEWAYS | DOWNTREND",
      "subclass": "MA_CONFLICT | DETERIORATION_TRANSITION | RECOVERY_TRANSITION | NO_SUBCLASS"
    },
    "features": {
      "leader_features_by_symbol": [
        "leader_rank",
        "leader_score",
        "rs_score",
        "momentum_score",
        "trend_health",
        "ma20",
        "ma50",
        "ma20_slope",
        "ma50_slope"
      ]
    }
  },
  "adapter_contract": {
    "HistoricalDataAdapter": {
      "purpose": "Load 5Y historical data and provide normalized MarketSnapshot sequence.",
      "may_do": [
        "read JSON files",
        "normalize schema",
        "align dates",
        "provide rolling history",
        "provide index/regime snapshots"
      ],
      "must_not_do": [
        "decide trading actions",
        "change entry/exit/sizing/market gate",
        "silently use invalid artifacts",
        "silently fork logic from forward adapter"
      ]
    },
    "ForwardDataAdapter": {
      "purpose": "Load latest daily data and provide the same MarketSnapshot schema.",
      "may_do": [
        "read latest production data",
        "normalize schema",
        "provide rolling history",
        "provide current regime snapshot"
      ],
      "must_not_do": [
        "own trading logic",
        "use run_oos_day as a separate decision engine",
        "override E1R Core decisions"
      ]
    },
    "LiveDataAdapter_future": {
      "purpose": "Future live-data normalization only, disabled until explicit approval.",
      "must_not_do": [
        "bypass E1R Core Engine",
        "introduce broker-specific trading rules"
      ]
    }
  },
  "acceptance_criteria_for_next_stage": [
    "Identify a reusable runtime loader or explicitly conclude none is safe.",
    "Lock real JSON schema for stock/index/regime files.",
    "Define canonical parser behavior for HistoricalDataAdapter.",
    "Confirm ForwardDataAdapter can use the same MarketSnapshot schema.",
    "No strategy logic changes.",
    "No full 5Y run.",
    "No official result."
  ]
}
```

## Validations
```json
{
  "fail_safe_report_written": true,
  "contract_audit_only": true,
  "strategy_logic_changed": false,
  "backtest_engine_run": false,
  "full_5y_backtest_run": false,
  "forward_runner_run": false,
  "provider_extraction_run": false,
  "adapter_implementation_run": false,
  "official_result_generated": false,
  "dashboard_changed": false,
  "strategy_files_unchanged": true,
  "invalid_artifacts_not_used_as_source": true,
  "composer_not_used": true,
  "return_curve_stitching_not_used": true,
  "engine_a_loaded": true,
  "data_inventory_completed": true,
  "loader_candidates_scanned": true,
  "backtest_signature_audited": true,
  "normalized_market_snapshot_contract_defined": true,
  "historical_data_adapter_contract_defined": true,
  "forward_data_adapter_contract_defined": true,
  "future_live_data_adapter_boundary_defined": true,
  "selected_loader_not_locked_yet": true,
  "adapter_implementation_not_allowed_yet": true,
  "strategy_core_extraction_not_allowed_yet": true,
  "decision_generated": true
}
```

## Decision
```json
{
  "normalized_input_contract_defined": true,
  "loader_candidates_found": 287,
  "reusable_runtime_loader_candidate_count": 41,
  "audit_only_candidate_count": 49,
  "selected_loader_locked": false,
  "historical_adapter_implementation_allowed_now": false,
  "forward_adapter_implementation_allowed_now": false,
  "strategy_core_extraction_allowed_now": false,
  "full_5y_backtest_allowed_now": false,
  "conclusion": "NORMALIZED_INPUT_CONTRACT_READY_REUSABLE_LOADER_CANDIDATES_FOUND",
  "recommended_next_action": "Proceed to 4C-2C-4E-ENGINE-C: verify top reusable loader candidates with a no-strategy data-harness smoke. Do not implement trading core yet.",
  "engineering_rule": "Backtest, forward test, and future live trading must share one normalized MarketSnapshot/DataBundle input contract. Data adapters normalize inputs; they do not own trading logic.",
  "top_reusable_candidates": [
    {
      "path": "src/engine/backtest.py",
      "name": "run_strategy_variant_comparison",
      "start_line": 2489,
      "end_line": 2895,
      "line_count": 407,
      "args": [
        "symbols",
        "prices_map",
        "dates_map",
        "spx_prices",
        "spx_dates",
        "ndx_prices",
        "ndx_dates",
        "sox_prices",
        "sox_dates",
        "vix_prices",
        "vix_dates"
      ],
      "score": 23,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:json.load",
        "contains:json.loads",
        "contains:prices_map",
        "contains:dates_map",
        "contains:data/research/e1_5y",
        "contains:SPX.json",
        "contains:spx_regime_daily",
        "contains:raw/stocks",
        "contains:raw/indices",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_research_5y_data",
        "uses_regime"
      ],
      "risks": []
    },
    {
      "path": "scripts/e1r_continuous_stateful_smoke_4c2c4e_b3.py",
      "name": "call_backtest_engine",
      "start_line": 371,
      "end_line": 423,
      "line_count": 53,
      "args": [
        "stock_dir",
        "regime_daily"
      ],
      "score": 16,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:load_stock",
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "src/engine/backtest.py",
      "name": "run_stateful_simulation",
      "start_line": 763,
      "end_line": 2486,
      "line_count": 1724,
      "args": [
        "symbols",
        "prices_map",
        "dates_map",
        "spx_prices",
        "spx_dates",
        "ohlc_map",
        "assumptions",
        "step",
        "min_history",
        "market_score_default",
        "sim_start_date",
        "sim_end_date",
        "ndx_prices",
        "ndx_dates",
        "sox_prices",
        "sox_dates",
        "vix_prices",
        "vix_dates"
      ],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/export_e1_5y_core_equity.py",
      "name": "main",
      "start_line": 295,
      "end_line": 514,
      "line_count": 220,
      "args": [],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:load_stock",
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/run_e1r_unified_5y_full_account_4c2c.py",
      "name": "main",
      "start_line": 679,
      "end_line": 890,
      "line_count": 212,
      "args": [],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_regime_wiring_4c2b4.py",
      "name": "main",
      "start_line": 497,
      "end_line": 703,
      "line_count": 207,
      "args": [],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_regime_wiring_trade_window_4c2b5.py",
      "name": "main",
      "start_line": 514,
      "end_line": 707,
      "line_count": 194,
      "args": [],
      "score": 15,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_regime",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_4c2b.py",
      "name": "main",
      "start_line": 219,
      "end_line": 384,
      "line_count": 166,
      "args": [],
      "score": 14,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_4c2b1.py",
      "name": "main",
      "start_line": 319,
      "end_line": 481,
      "line_count": 163,
      "args": [],
      "score": 14,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_ohlc"
      ],
      "risks": []
    },
    {
      "path": "scripts/smoke_invoke_unified_engine_4c2b2.py",
      "name": "main",
      "start_line": 375,
      "end_line": 542,
      "line_count": 168,
      "args": [],
      "score": 14,
      "classification": "BACKTEST_HARNESS_CANDIDATE",
      "classification_rank": 100,
      "reasons": [
        "contains:prices_map",
        "contains:dates_map",
        "uses_prices_map",
        "uses_dates_map",
        "uses_symbols",
        "uses_spx_series",
        "feeds_run_stateful_simulation",
        "uses_ohlc"
      ],
      "risks": []
    }
  ]
}
```
