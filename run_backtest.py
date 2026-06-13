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

    # 加载价格
    prices_map = {}
    for sym in symbols:
        d, p = get_price_series(sym)
        if len(p) >= 120:
            prices_map[sym] = p
    logger.info(f"有效价格序列：{len(prices_map)} 只")

    # SPX
    from src.pipeline.update_pipeline import get_prices_safe
    _, spx_prices = get_prices_safe("^GSPC")
    if not spx_prices:
        _, spx_prices = get_price_series("SPY")
    logger.info(f"SPX: {len(spx_prices)} bars")

    # 运行回测
    from src.engine.backtest import run_full_backtest
    results = run_full_backtest(
        list(prices_map.keys()),
        prices_map,
        spx_prices,
        run_layer_b=run_layer_b,
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

    output = {
        "generated_at":         datetime.now(ET).isoformat(),
        "generated_at_display": datetime.now(ET).strftime("%Y年%-m月%-d日 %H:%M ET"),
        "backtest": results,
    }
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    write_json(EXPORTS_DIR / "backtest.json", output)
    logger.ok("✅ 回测完成！结果已写入 exports/backtest.json")

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
