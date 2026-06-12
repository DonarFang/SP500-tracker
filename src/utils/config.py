from __future__ import annotations
import os
from pathlib import Path

ROOT_DIR    = Path(__file__).parent.parent.parent
DATA_DIR    = ROOT_DIR / "data"
PRICES_DIR  = DATA_DIR / "prices"
EXPORTS_DIR = ROOT_DIR / "exports"

HISTORY_DAYS     = 730
MIN_HISTORY_DAYS = 60
INCREMENTAL_DAYS = 7
MA_SHORT, MA_MID, MA_LONG = 20, 50, 200
RS_WINDOW        = 60
MOMENTUM_THRESH  = 0.06
TH_HIGH          = 80
AD_RATIO_BULL    = 1.2
AD_RATIO_BEAR    = 0.8
LEADER_TOP_N     = 10
WATCHLIST_START  = 10
WATCHLIST_END    = 30
SPY_SYMBOL       = "SPY"
SPX_SYMBOL       = "^GSPC"

MEMBERS_FILE          = DATA_DIR / "members.json"
CONSTITUENTS_FILE     = DATA_DIR / "sp500_constituents.json"
SIGNALS_HISTORY_FILE  = DATA_DIR / "signals_history.json"
LEADERBOARD_HIST_FILE = DATA_DIR / "leaderboard_history.json"
WATCHLIST_HIST_FILE   = DATA_DIR / "watchlist_history.json"

EXPORT_MARKET     = EXPORTS_DIR / "market_state.json"
EXPORT_LEADERBOARD= EXPORTS_DIR / "leaderboard.json"
EXPORT_WATCHLIST  = EXPORTS_DIR / "watchlist.json"
EXPORT_TRADES     = EXPORTS_DIR / "trade_actions.json"
EXPORT_LIFECYCLE  = EXPORTS_DIR / "lifecycle.json"
EXPORT_HEALTH     = EXPORTS_DIR / "data_health.json"

def ensure_dirs():
    for d in [DATA_DIR, PRICES_DIR, EXPORTS_DIR]:
        d.mkdir(parents=True, exist_ok=True)
