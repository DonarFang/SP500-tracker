from __future__ import annotations
from ..features.momentum import linreg_slope, moving_average
from ..utils.config import AD_RATIO_BULL, AD_RATIO_BEAR

def compute(spx_prices: list[float], advance_decline: float) -> dict:
    n = len(spx_prices)
    if n < 50: return {"state":"Neutral","spx_close":0,"spx_ma50":0,"spx_ma200":0,"spx_slope20":0,"pct_above_ma50":0,"advance_decline":1.0}
    last  = spx_prices[-1]
    ma50  = sum(spx_prices[-50:])/50
    ma200 = sum(spx_prices[-200:])/200 if n>=200 else sum(spx_prices)/n
    sl20  = linreg_slope(spx_prices[-20:]) if n>=20 else 0
    if last>ma50>ma200 and sl20>0 and advance_decline>AD_RATIO_BULL: state="Risk-On"
    elif last<ma50 or advance_decline<AD_RATIO_BEAR: state="Risk-Off"
    else: state="Neutral"
    return {"state":state,"spx_close":round(last,2),"spx_ma50":round(ma50,2),
            "spx_ma200":round(ma200,2),"spx_slope20":round(sl20,6),
            "pct_above_ma50":round((last-ma50)/ma50*100,2),"advance_decline":round(advance_decline,2)}
