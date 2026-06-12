#!/usr/bin/env python3
"""init_data.py — 一次性初始化，拉取2年历史数据"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from src.utils.config import ensure_dirs
from src.utils import logger

if __name__ == "__main__":
    ensure_dirs()
    # 直接用 force_full=True 运行，update_pipeline 会自动处理四大指数
    from src.pipeline.daily_run import run
    logger.info("🚀 初始化：拉取 2 年历史数据...")
    run(force_full=True)
    logger.ok("✅ 初始化完成！")
