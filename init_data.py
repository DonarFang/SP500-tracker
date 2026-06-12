#!/usr/bin/env python3
"""init_data.py — 一次性初始化，拉取2年历史数据"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from src.utils.config import ensure_dirs
from src.pipeline.daily_run import run

if __name__ == "__main__":
    ensure_dirs()
    print("🚀 初始化：拉取 2 年历史数据（约 15-20 分钟）...")
    run(force_full=True)
    print("✅ 初始化完成！")
