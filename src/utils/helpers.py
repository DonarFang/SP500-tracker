from __future__ import annotations
import json
from pathlib import Path
from typing import Any

def read_json(path) -> Any:
    p = Path(path)
    if not p.exists(): return None
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def write_json(path, data: Any, indent: int = 2) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent)

def price_file(symbol: str) -> Path:
    from .config import PRICES_DIR
    return PRICES_DIR / f"{symbol.replace('^','_')}.json"

def safe_round(v, n=2):
    try: return round(float(v), n) if v is not None and v == v else None
    except: return None
