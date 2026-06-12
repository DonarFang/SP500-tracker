#!/usr/bin/env python3
"""
init_data.py — 一次性初始化，拉取2年历史数据
包含：成分股 + 四大指数（^GSPC, ^NDX, ^VIX, ^SOX, SPY）
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from src.utils.config import ensure_dirs
from src.utils import logger

if __name__ == "__main__":
    ensure_dirs()
    from datetime import datetime, timedelta
    try:
        import pytz
        ET = pytz.timezone("America/New_York")
    except:
        from datetime import timezone, timedelta as td
        ET = timezone(td(hours=-4))

    now   = datetime.now(ET)
    start = (now - timedelta(days=730)).strftime("%Y-%m-%d")
    end   = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    from src.data_ingestion.fetch_yahoo import (
        download_bulk, download_single, append_prices, fetch_members
    )
    from src.utils.helpers import write_json
    from src.utils.config import MEMBERS_FILE, CONSTITUENTS_FILE

    # Step 1: 成分股
    logger.info(f"🚀 初始化：拉取 2 年历史数据 {start} → {end}")
    from src.utils.helpers import read_json
    symbols = read_json(CONSTITUENTS_FILE) or []
    if len(symbols) < 500:
        members = fetch_members()
        write_json(MEMBERS_FILE, members)
        symbols = [m["symbol"] for m in members]
    logger.info(f"成分股：{len(symbols)} 只")

    # Step 2: 批量下载成分股（2年历史）
    logger.info("[1/2] 下载成分股历史数据...")
    data = download_bulk(symbols + ["SPY"], start, end, batch_size=50, sleep=2.0)
    updated = sum(1 for sym, df in data.items() if append_prices(sym, df) > 0)
    logger.info(f"  → 写入 {updated} 只股票")

    # Step 3: 单独下载四大指数（2年历史）
    logger.info("[2/2] 下载四大指数历史数据...")
    indices = ["^GSPC", "^NDX", "^VIX", "^SOX"]
    for sym in indices:
        logger.info(f"  下载 {sym}...")
        df = download_single(sym, start, end)
        if df is not None and not df.empty:
            n = append_prices(sym, df)
            logger.ok(f"  {sym}: {n} 条")
        else:
            logger.warn(f"  {sym}: 下载失败")

    # Step 4: 运行信号引擎
    logger.info("运行信号引擎...")
    from src.pipeline.daily_run import run
    run(force_full=False)

    logger.ok("✅ 初始化完成！")
