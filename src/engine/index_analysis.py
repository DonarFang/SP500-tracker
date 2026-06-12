"""
index_analysis.py — 四大指数分析
P0修复：^ 符号在文件名中存为 _，读取时需要同时尝试两种格式
"""
from __future__ import annotations
from ..features.momentum import linreg_slope, moving_average

INDEX_SYMBOLS = {"SPX":"^GSPC","NDX":"^NDX","VIX":"^VIX","SOX":"^SOX"}
INDEX_META = {
    "SPX":{"name":"标普500",     "desc":"大盘趋势基准"},
    "NDX":{"name":"纳斯达克100", "desc":"科技/成长股风向标"},
    "VIX":{"name":"波动率指数",  "desc":"市场恐惧/情绪指标"},
    "SOX":{"name":"费城半导体",  "desc":"半导体/科技先行指标"},
}

def _get(prices_map, sym):
    """尝试原始代码和 ^ → _ 转换后的代码两种格式。"""
    return (prices_map.get(sym) or
            prices_map.get(sym.replace("^","_")) or
            prices_map.get("_"+sym.lstrip("^")) or [])

def _get_dates(dates_map, sym):
    return (dates_map.get(sym) or
            dates_map.get(sym.replace("^","_")) or
            dates_map.get("_"+sym.lstrip("^")) or [])

def analyze_index(code: str, prices: list[float], dates: list[str]) -> dict:
    n = len(prices)
    if n < 5:
        return {"code":code,"available":False,"name":INDEX_META.get(code,{}).get("name",code)}
    last=prices[-1]; prev=prices[-2] if n>=2 else last
    chg=last-prev; chg_pct=chg/prev*100 if prev>0 else 0
    ma20=sum(prices[-20:])/min(n,20)
    ma50=sum(prices[-50:])/min(n,50) if n>=20 else last
    ma200=sum(prices[-200:])/min(n,200) if n>=100 else last
    sl20=linreg_slope(prices[-20:]) if n>=20 else 0
    w52=prices[-252:] if n>=252 else prices
    high52,low52=max(w52),min(w52)
    pct_from_high=(last-high52)/high52*100 if high52>0 else 0
    chart_ma20=[round(v,2) for v in moving_average(prices,20)[-60:]]
    chart_ma50=[round(v,2) for v in moving_average(prices,50)[-60:]] if n>=50 else []
    r={
        "code":code,"yahoo_symbol":INDEX_SYMBOLS.get(code,code),
        "name":INDEX_META[code]["name"],"desc":INDEX_META[code]["desc"],
        "available":True,"price":round(last,2),"change":round(chg,2),
        "change_pct":round(chg_pct,2),"ma20":round(ma20,2),"ma50":round(ma50,2),
        "ma200":round(ma200,2),"above_ma20":last>ma20,"above_ma50":last>ma50,
        "above_ma200":last>ma200,"slope20":round(sl20,6),
        "high52w":round(high52,2),"low52w":round(low52,2),
        "pct_from_high":round(pct_from_high,2),
        "chart_dates":dates[-60:],"chart_prices":[round(p,2) for p in prices[-60:]],
        "chart_ma20":chart_ma20,"chart_ma50":chart_ma50,
    }
    if code=="VIX":
        v=last
        if v<15:   st,col="低恐惧","#1D9E75"
        elif v<20: st,col="正常","#378ADD"
        elif v<25: st,col="偏高","#BA7517"
        elif v<35: st,col="高恐惧","#D85A30"
        else:      st,col="极度恐惧","#993C1D"
        trend="上升" if sl20>0.001 else "下降" if sl20<-0.001 else "横盘"
        r.update({"vix_state":st,"vix_signal":"Risk-Off" if v>=25 else "Neutral" if v>=20 else "Risk-On",
                  "vix_color":col,"vix_trend":trend})
    else:
        if last>ma50>ma200 and sl20>0:   tr,col="强势上涨","#1D9E75"
        elif last>ma50 and sl20>0:       tr,col="趋势向上","#378ADD"
        elif last>ma50:                  tr,col="震荡偏多","#BA7517"
        elif last>ma200:                 tr,col="弱势整理","#D85A30"
        else:                            tr,col="趋势向下","#993C1D"
        r.update({"trend":tr,"trend_color":col})
    return r

def analyze_all_indices(prices_map: dict, dates_map: dict) -> dict:
    results={}
    for code,sym in INDEX_SYMBOLS.items():
        p=_get(prices_map,sym)
        d=_get_dates(dates_map,sym)
        results[code]=analyze_index(code,p,d) if len(p)>=5 else {
            "code":code,"name":INDEX_META[code]["name"],"available":False}

    # 相对强弱
    ndx_p=_get(prices_map,"^NDX")
    spx_p=_get(prices_map,"^GSPC")
    sox_p=_get(prices_map,"^SOX")
    if len(ndx_p)>=20 and len(spx_p)>=20:
        nr=(ndx_p[-1]-ndx_p[-20])/ndx_p[-20]*100 if ndx_p[-20]>0 else 0
        sr=(spx_p[-1]-spx_p[-20])/spx_p[-20]*100 if spx_p[-20]>0 else 0
        tp=round(nr-sr,2)
        results["tech_premium"]=tp
        results["tech_premium_signal"]="科技领涨" if tp>2 else "科技同步" if tp>-2 else "科技落后"
    if len(sox_p)>=20 and len(spx_p)>=20:
        xr=(sox_p[-1]-sox_p[-20])/sox_p[-20]*100 if sox_p[-20]>0 else 0
        sr2=(spx_p[-1]-spx_p[-20])/spx_p[-20]*100 if spx_p[-20]>0 else 0
        sp=round(xr-sr2,2)
        results["sox_premium"]=sp
        results["sox_premium_signal"]="半导体领涨" if sp>3 else "半导体同步" if sp>-3 else "半导体落后"
    return results
