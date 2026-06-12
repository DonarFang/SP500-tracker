"""fetch_yahoo.py — Yahoo Finance 数据抓取"""
from __future__ import annotations
import time
from typing import Optional
import pandas as pd
from ..utils.config import MEMBERS_FILE, CONSTITUENTS_FILE, SPY_SYMBOL
from ..utils.helpers import read_json, write_json, price_file, safe_round
from ..utils import logger

_FALLBACK = list(dict.fromkeys([
    "AAPL","MSFT","NVDA","GOOGL","AMZN","META","TSLA","BRK-B","AVGO","LLY",
    "JPM","V","UNH","XOM","MA","HD","PG","COST","ABBV","MRK","CVX","BAC",
    "CRM","NFLX","AMD","ACN","WMT","TMO","ORCL","CSCO","ABT","TXN","DHR",
    "NEE","ADBE","PM","PEP","MCD","INTC","IBM","GE","CAT","AMGN","QCOM",
    "HON","RTX","BKNG","INTU","ISRG","LOW","AMAT","VRTX","AXP","GS","SBUX",
    "ELV","MDLZ","TJX","BLK","DE","ADI","GILD","SYK","REGN","MMC","LRCX",
    "MU","KLAC","PANW","ZTS","ADP","SO","CB","WM","SNPS","CDNS","CME",
    "AON","MCO","PGR","ITW","EMR","BSX","SHW","EQIX","CTAS","APH","USB",
    "WFC","DELL","DDOG","NET","CRWD","MELI","ABNB","COIN","PLTR","AXON",
    "UBER","SHOP","PYPL","KO","PFE","JNJ","BMY","BIIB","MRNA","SNDK",
    "AKAM","MNST","GEN","CPAY","WAT","HUM","CNC","ZBRA","TKO","TTWO",
    "F","JBHT","ODFL","ROK","RVTY","APTV","ANET","LULU","NKE","DIS",
    "CMCSA","T","VZ","TMUS","NOW","WDAY","ZS","FTNT","SWKS","MCHP","ON",
    "MPWR","ENPH","FSLR","FCX","NEM","ALB","LIN","ALK","ALAB","MRVL",
    "WOLF","BE","PLD","SPGI","SNOW","GEV","HOOD","RBLX","DASH",
]))

SECTOR_MAP = {
    "NVDA":"Semiconductors","AMD":"Semiconductors","INTC":"Semiconductors","MU":"Semiconductors",
    "AVGO":"Semiconductors","QCOM":"Semiconductors","LRCX":"Semiconductors","AMAT":"Semiconductors",
    "KLAC":"Semiconductors","SNDK":"Semiconductors","SWKS":"Semiconductors","MCHP":"Semiconductors",
    "MPWR":"Semiconductors","ON":"Semiconductors","ALAB":"Semiconductors","TXN":"Semiconductors",
    "ADI":"Semiconductors","MRVL":"Semiconductors","WOLF":"Semiconductors","NXPI":"Semiconductors",
    "AAPL":"Technology","MSFT":"Technology","GOOGL":"Technology","GOOG":"Technology","META":"Technology",
    "ORCL":"Technology","CRM":"Technology","ADBE":"Technology","INTU":"Technology","NOW":"Technology",
    "WDAY":"Technology","AKAM":"Technology","GEN":"Technology","DELL":"Technology","IBM":"Technology",
    "CSCO":"Technology","ANET":"Technology","SNOW":"Technology","DDOG":"Technology","NET":"Technology",
    "CRWD":"Technology","PANW":"Technology","FTNT":"Technology","ZS":"Technology","PLTR":"Technology",
    "AXON":"Technology","FICO":"Technology","SNPS":"Technology","CDNS":"Technology",
    "AMZN":"E-Commerce/Cloud","SHOP":"E-Commerce","MELI":"E-Commerce","BKNG":"Travel","ABNB":"Travel",
    "UBER":"Transportation","TSLA":"Auto","F":"Auto","APTV":"Auto",
    "JPM":"Financials","BAC":"Financials","GS":"Financials","WFC":"Financials","V":"Payments","MA":"Payments",
    "PYPL":"Fintech","CPAY":"Fintech","COIN":"Crypto","BLK":"Asset Mgmt","MCO":"Ratings","SPGI":"Ratings",
    "AXP":"Financials","CME":"Exchange","CB":"Insurance","AON":"Insurance","MMC":"Insurance",
    "UNH":"Healthcare","ELV":"Healthcare","HUM":"Healthcare","CNC":"Healthcare",
    "LLY":"Pharma","MRK":"Pharma","ABBV":"Pharma","PFE":"Pharma","JNJ":"Pharma","BMY":"Pharma",
    "AMGN":"Biotech","BIIB":"Biotech","MRNA":"Biotech","GILD":"Biotech","REGN":"Biotech","VRTX":"Biotech",
    "TMO":"Med Devices","ABT":"Med Devices","DHR":"Med Devices","SYK":"Med Devices","ISRG":"Med Devices",
    "XOM":"Energy","CVX":"Energy","COP":"Energy","SLB":"Energy",
    "GE":"Industrials","CAT":"Industrials","HON":"Industrials","RTX":"Industrials","DE":"Industrials",
    "COST":"Retail","WMT":"Retail","TGT":"Retail","HD":"Retail","LOW":"Retail","TJX":"Retail",
    "MCD":"Food & Bev","SBUX":"Food & Bev","DIS":"Entertainment","NFLX":"Streaming",
    "PG":"Consumer","KO":"Consumer","PEP":"Consumer","PM":"Consumer","MNST":"Consumer",
    "NEE":"Utilities","DUK":"Utilities","SO":"Utilities","T":"Telecom","VZ":"Telecom","TMUS":"Telecom",
    "FCX":"Mining","NEM":"Mining","ALB":"Chemicals","LIN":"Chemicals",
    "ALK":"Airlines","ENPH":"Clean Energy","BE":"Clean Energy","FSLR":"Clean Energy",
    "PLD":"REITs","EQIX":"REITs","GEV":"Industrials","HOOD":"Fintech","DASH":"Delivery",
    "RBLX":"Gaming","TTWO":"Gaming","TKO":"Entertainment",
}

def get_sector(sym): return SECTOR_MAP.get(sym,"Other")

def fetch_members() -> list[dict]:
    # 优先用本地成分股文件
    data = read_json(CONSTITUENTS_FILE)
    if data and isinstance(data,list) and len(data)>=500:
        logger.ok(f"成分股库：{len(data)} 只（sp500_constituents.json）")
        return [{"symbol":s,"name":s,"sector":get_sector(s)} for s in data]
    # fallback: 维基百科
    try:
        tables=pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies",attrs={"id":"constituents"})
        df=tables[0]
        members=[{"symbol":str(r["Symbol"]).replace(".","=").strip(),"name":str(r.get("Security","")),
                  "sector":str(r.get("GICS Sector",get_sector(str(r["Symbol"]))))} for _,r in df.iterrows()]
        logger.ok(f"维基百科成分股：{len(members)} 只")
        return members
    except Exception as e:
        logger.warn(f"维基百科失败（{e}），使用兜底列表 {len(_FALLBACK)} 只")
        return [{"symbol":s,"name":s,"sector":get_sector(s)} for s in _FALLBACK]

def _parse(raw, sym) -> Optional[pd.DataFrame]:
    if raw is None or raw.empty: return None
    try:
        # yfinance 新版本单只股票也可能返回 MultiIndex
        if isinstance(raw.columns, pd.MultiIndex):
            # MultiIndex: (field, ticker) 或 (ticker, field)
            try:
                raw = raw.xs(sym, axis=1, level=1)
            except:
                try:
                    raw = raw.xs(sym, axis=1, level=0)
                except:
                    raw = raw.droplevel(0, axis=1)
        df = pd.DataFrame()
        for c in ["Open","High","Low","Close","Volume"]:
            m = [x for x in raw.columns if str(x).lower()==c.lower()]
            if m: df[c.lower()] = raw[m[0]]
        if "close" not in df.columns:
            logger.warn(f"  {sym}: 解析后无 close 列，columns={list(raw.columns)[:5]}")
            return None
        df.index.name = "date"
        df = df.reset_index()
        df["date"] = df["date"].astype(str).str[:10]
        return df.dropna(subset=["close"])
    except Exception as e:
        logger.warn(f"  {sym} _parse error: {e}")
        return None

def download_bulk(symbols,start,end,batch_size=50,sleep=1.5) -> dict[str,pd.DataFrame]:
    import yfinance as yf
    result={}
    batches=[symbols[i:i+batch_size] for i in range(0,len(symbols),batch_size)]
    for bi,batch in enumerate(batches):
        logger.info(f"  批次 {bi+1}/{len(batches)} ({len(batch)} 只)...")
        try:
            raw=yf.download(batch,start=start,end=end,interval="1d",auto_adjust=True,progress=False,threads=True)
            if raw.empty: continue
            for sym in batch:
                try:
                    if len(batch)==1:
                        df=_parse(raw,sym)
                    else:
                        sub={}
                        for col in ["Open","High","Low","Close","Volume"]:
                            if col in raw.columns:
                                c=raw[col]
                                if isinstance(c,pd.DataFrame) and sym in c.columns: sub[col.lower()]=c[sym]
                                elif isinstance(c,pd.Series): sub[col.lower()]=c
                        if not sub or "close" not in sub: continue
                        df_tmp=pd.DataFrame(sub,index=raw.index)
                        df_tmp.index.name="date"; df_tmp=df_tmp.reset_index()
                        df_tmp["date"]=df_tmp["date"].astype(str).str[:10]
                        df=df_tmp.dropna(subset=["close"])
                    if df is not None and not df.empty: result[sym]=df
                except: pass
        except Exception as e: logger.warn(f"  批次{bi+1}失败: {e}")
        if bi<len(batches)-1: time.sleep(sleep)
    return result

def download_single(symbol,start,end) -> Optional[pd.DataFrame]:
    """
    下载单只股票或指数。
    对指数（^开头）使用 Ticker.history()，比 yf.download 更稳定。
    """
    import yfinance as yf
    import pandas as pd
    try:
        # 优先用 Ticker.history()，对 ^GSPC 等指数更可靠
        ticker = yf.Ticker(symbol)
        raw = ticker.history(start=start, end=end, interval="1d", auto_adjust=True)
        if raw is not None and not raw.empty:
            df = pd.DataFrame()
            for c in ["Open","High","Low","Close","Volume"]:
                if c in raw.columns:
                    df[c.lower()] = raw[c]
            if "close" not in df.columns:
                raise ValueError(f"no close column, got {list(raw.columns)}")
            df.index.name = "date"
            df = df.reset_index()
            df["date"] = df["date"].astype(str).str[:10]
            result = df.dropna(subset=["close"])
            if not result.empty:
                return result
        # fallback: yf.download
        raw2 = yf.download(symbol, start=start, end=end, interval="1d",
                           auto_adjust=True, progress=False)
        return _parse(raw2, symbol)
    except Exception as e:
        logger.warn(f"{symbol}: {e}")
        return None

def download_with_fallback(
    primary: str,
    fallbacks: list[str],
    start: str,
    end: str,
) -> tuple[str, any]:
    """
    带 fallback 的下载：先试 primary，失败依次试 fallbacks。
    返回 (used_sym, df)，used_sym 是实际成功的代码。
    无论用哪个代码下载，调用方应统一存储到 primary 路径。
    """
    for sym in [primary] + fallbacks:
        df = download_single(sym, start, end)
        if df is not None and not df.empty:
            if sym != primary:
                logger.info(f"  {primary}: fallback 到 {sym} 成功")
            return sym, df
    return primary, None


def load_prices(sym) -> list[dict]:
    d=read_json(price_file(sym)); return d if isinstance(d,list) else []

def save_prices(sym, records): write_json(price_file(sym), records)

def append_prices(sym, df: pd.DataFrame) -> int:
    existing=load_prices(sym); existing_dates={r["date"] for r in existing}
    new=[]
    for row in df.itertuples():
        d=str(row.date)[:10]
        if d not in existing_dates:
            new.append({"date":d,"open":safe_round(getattr(row,"open",None)),
                        "high":safe_round(getattr(row,"high",None)),
                        "low":safe_round(getattr(row,"low",None)),
                        "close":safe_round(row.close),
                        "volume":safe_round(getattr(row,"volume",0),0)})
    if new:
        combined=sorted(existing+new,key=lambda x:x["date"])
        save_prices(sym,combined)
    return len(new)

def get_price_series(sym,field="close") -> tuple[list[str],list[float]]:
    records=load_prices(sym)
    dates=[r["date"] for r in records if r.get(field) is not None]
    values=[float(r[field]) for r in records if r.get(field) is not None]
    return dates,values
