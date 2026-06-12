#!/usr/bin/env python3
"""fetch_data.py — 每日更新入口（GitHub Actions 调用）"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from src.utils.config import ensure_dirs
from src.pipeline.daily_run import run

if __name__ == "__main__":
    ensure_dirs()
    run(force_full="--full" in sys.argv)
