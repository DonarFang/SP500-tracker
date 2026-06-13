#!/usr/bin/env python3
"""
run_backtest.py — 回测运行入口
用法：python run_backtest.py [--full]
  --full: 包含 Layer B（较慢，约30分钟）
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from src.utils.config import ensure_dirs
from src.utils import logger

if __name__ == "__main__":
    ensure_dirs()
    run_layer_b = "--full" in sys.argv

    logger.info("加载价格数据...")
    from src.utils.helpers import read_json
    from src.utils.config import CONSTITUENTS_FILE
    from src.data_ingestion.fetch_yahoo import get_price_series

    symbols = read_json(CONSTITUENTS_FILE) or []
    logger.info(f"成分股：{len(symbols)} 只")

    # 加载价格 + 日期
    prices_map: dict = {}
    dates_map:  dict = {}
    for sym in symbols:
        d, p = get_price_series(sym)
        if len(p) >= 120:
            prices_map[sym] = p
            dates_map[sym]  = d
    logger.info(f"有效价格序列：{len(prices_map)} 只")

    # SPX
    from src.pipeline.update_pipeline import get_prices_safe
    spx_dates, spx_prices = get_prices_safe("^GSPC")
    if not spx_prices:
        spx_dates, spx_prices = get_price_series("SPY")
    logger.info(f"SPX: {len(spx_prices)} bars")

    # 运行回测
    from src.engine.backtest import run_full_backtest
    results = run_full_backtest(
        list(prices_map.keys()),
        prices_map,
        spx_prices,
        dates_map  = dates_map,
        spx_dates  = spx_dates,
        run_layer_b= run_layer_b,
        run_layer_d= True,
    )

    # 输出到 exports/backtest.json
    from src.utils.helpers import write_json
    from src.utils.config import EXPORTS_DIR
    from datetime import datetime
    try:
        import pytz
        ET = pytz.timezone("America/New_York")
    except:
        from datetime import timezone, timedelta
        ET = timezone(timedelta(hours=-4))

    now_str = datetime.now(ET).isoformat()
    now_disp = datetime.now(ET).strftime("%Y年%-m月%-d日 %H:%M ET")
    meta = {"generated_at": now_str, "generated_at_display": now_disp}

    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # backtest.json — 完整摘要
    write_json(EXPORTS_DIR / "backtest.json", {**meta, "backtest": results})

    # 独立文件
    layer_results = results.get("results", {})

    # action_forward_returns.json — Layer C2
    if "layer_c2" in layer_results:
        write_json(EXPORTS_DIR / "action_forward_returns.json", {
            **meta, **layer_results["layer_c2"]
        })

    # portfolio_backtest.json — Layer D 核心指标（不含交易记录）
    if "layer_d" in layer_results:
        ld = layer_results["layer_d"]
        write_json(EXPORTS_DIR / "portfolio_backtest.json", {
            **meta,
            **{k: v for k, v in ld.items() if k not in ("trades","equity_curve","spx_curve","daily_log")},
        })

        # trade_log.json — Layer D 完整交易记录（最重要）
        write_json(EXPORTS_DIR / "trade_log.json", {
            **meta,
            "total_trades": ld.get("total_trades_all", 0),
            "trades": ld.get("trades", []),
        })

        # equity_curve.json — 净值曲线
        write_json(EXPORTS_DIR / "equity_curve.json", {
            **meta,
            "equity_curve":  ld.get("equity_curve", []),
            "spx_curve":     ld.get("spx_curve", []),
            "daily_log":     ld.get("daily_log", []),
        })

    logger.ok("✅ 回测完成！")
    logger.ok(f"  exports/backtest.json")
    logger.ok(f"  exports/action_forward_returns.json")
    logger.ok(f"  exports/portfolio_backtest.json")
    logger.ok(f"  exports/trade_log.json")
    logger.ok(f"  exports/equity_curve.json")

    # 打印摘要
    print("\n" + "="*60)
    print(f"回测结果摘要 — {results['overall_status']}")
    print("="*60)
    for layer_key, layer_data in results["results"].items():
        print(f"\n{layer_data['name']}: {layer_data['status']}")

        if layer_key == "layer_a":
            a1 = layer_data.get("a1_top_bucket_edge","—")
            a2 = layer_data.get("a2_full_monotonic","—")
            print(f"  A1 Top Bucket Edge: {a1}  |  A2 Full Monotonic: {a2}")
            print(f"  {layer_data.get('interpretation','')}")
            # 样本量
            sc = layer_data.get("bucket_sample_counts",{})
            print(f"  样本量(20日): A={sc.get('A',{}).get('fwd20d','—')} B={sc.get('B',{}).get('fwd20d','—')} C={sc.get('C',{}).get('fwd20d','—')} D={sc.get('D',{}).get('fwd20d','—')} E={sc.get('E',{}).get('fwd20d','—')}")
            for days in [5, 10, 20, 30]:
                k = f"fwd{days}d"
                row = []
                for b in ["A","B","C","D","E"]:
                    info = layer_data["bucket_summary"].get(b, {}).get(k, {})
                    avg = info.get("avg_ret", None)
                    n   = info.get("n", 0)
                    row.append(f"{avg:+.2f}%(n={n})" if avg is not None else "—")
                print(f"  {days:2d}日: A={row[0]} B={row[1]} C={row[2]} D={row[3]} E={row[4]}")

        elif layer_key == "layer_c":
            buy_n = layer_data.get("buy_signal_count", 0)
            sig_raw = layer_data.get("signal_counts_raw", {})
            dedup = layer_data.get("dedup_gap_days", 5)
            print(f"  BUY 有效信号数: {buy_n} (去重间隔{dedup}天，原始信号: {sig_raw})")
            for days in [5, 10, 20, 30]:
                k = f"fwd{days}d"
                buy_info = layer_data["signal_summary"].get("BUY",{}).get(k,{})
                spx_info = layer_data["spx_benchmark"].get(k,{})
                buy_avg  = buy_info.get("avg_ret", None)
                buy_wr   = buy_info.get("win_rate", None)
                spx_avg  = spx_info.get("avg_ret", None)
                better = "✅" if buy_avg is not None and spx_avg is not None and buy_avg > spx_avg else "❌"
                if buy_avg is not None:
                    print(f"  {days:2d}日: BUY={buy_avg:+.2f}%(WR={buy_wr}%) vs SPX={spx_avg:+.2f}% {better}")
                else:
                    print(f"  {days}日: 无数据")

        elif layer_key == "layer_c2":
            print(f"  验证每种 Action 的前向收益：")
            for days in [5, 10, 20, 30]:
                k = f"fwd{days}d"
                row = {}
                for a in ["BUY","ADD","HOLD","REDUCE","EXIT"]:
                    v = layer_data["action_summary"].get(a,{}).get(k,{}).get("avg_ret",None)
                    row[a] = f"{v:+.2f}%" if v is not None else "—"
                spx_v = layer_data["spx_benchmark"].get(k,{}).get("avg_ret",None)
                spx_s = f"{spx_v:+.2f}%" if spx_v is not None else "—"
                print(f"  {days:2d}日: BUY={row['BUY']} ADD={row['ADD']} HOLD={row['HOLD']} REDUCE={row['REDUCE']} EXIT={row['EXIT']} SPX={spx_s}")
            interp = layer_data.get("interpretation",{})
            for k,v in interp.items():
                print(f"  → {k}: {v}")

        elif layer_key == "layer_d":
            d = layer_data
            print(f"  Total Return:   {d.get('total_return_pct',0):+.2f}%  vs SPX {d.get('spx_total_return_pct',0):+.2f}%  Alpha: {d.get('alpha_pct',0):+.2f}%")
            print(f"  CAGR:           {d.get('cagr_pct',0):+.2f}%  vs SPX CAGR {d.get('spx_cagr_pct',0):+.2f}%")
            print(f"  Max Drawdown:   {d.get('max_drawdown_pct',0):.1f}%")
            print(f"  Win Rate:       {d.get('win_rate_pct',0):.1f}%")
            print(f"  Profit Factor:  {d.get('profit_factor',0):.2f}")
            print(f"  Sharpe Ratio:   {d.get('sharpe_ratio',0):.2f}")
            print(f"  Trades:         {d.get('number_of_trades',0)}  (Avg Hold: {d.get('avg_holding_days',0):.1f}天)")
            print(f"  Orders:         Executed={d.get('pending_orders_executed',0)}  Skipped={d.get('pending_orders_skipped',0)}  Invalid={d.get('invalid_trades_count',0)}")
            print(f"  Avg Winner:     {d.get('avg_winner_pct',0):+.2f}%  Avg Loser: {d.get('avg_loser_pct',0):+.2f}%")
            print(f"  Exposure:       {d.get('exposure_pct',0):.1f}%  (Max Pos: {d.get('avg_position_size',0):.1f}% each)")
            print(f"\n  交易记录（最近10笔）:")
            print(f"  {'Symbol':<8} {'Entry':>12} {'Exit':>12} {'Entry Sig':>10} {'Exit Sig':>10} {'Days':>5} {'Return':>8}")
            print(f"  {'-'*70}")
            for t in d.get("trades",[])[-10:]:
                print(f"  {t['symbol']:<8} {t['entry_date']:>12} {t['exit_date']:>12} {t['entry_signal']:>10} {t['exit_signal']:>10} {t['holding_days']:>5} {t['return_pct']:>+7.2f}%")
