import sys
from datetime import datetime, timezone, timedelta

def _ts():
    try:
        import pytz
        return datetime.now(pytz.timezone("America/New_York")).strftime("%H:%M:%S")
    except:
        # UTC-4 (EDT) fallback
        return datetime.now(timezone(timedelta(hours=-4))).strftime("%H:%M:%S")

def log(msg, level="INFO"): print(f"[{_ts()}] {level:5s} {msg}", flush=True)
def info(msg):  log(msg, "INFO")
def warn(msg):  log(msg, "WARN")
def error(msg): log(msg, "ERROR")
def ok(msg):    log(f"✅ {msg}", "OK")
