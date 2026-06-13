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
    # Storage / Hardware
    "STX":"Technology","WDC":"Technology","NTAP":"Technology","SMCI":"Technology",
    # Industrials / Construction
    "URI":"Industrials","CTAS":"Industrials","PWR":"Industrials","PCAR":"Industrials",
    "JBHT":"Transportation","ODFL":"Transportation","NSC":"Transportation",
    "UNP":"Transportation","CSX":"Transportation","DAL":"Airlines","UAL":"Airlines",
    "LUV":"Airlines","AAL":"Airlines",
    # Materials / Steel
    "STLD":"Materials","NUE":"Materials","RS":"Materials","X":"Materials",
    "CLF":"Materials","AA":"Materials","FCX":"Mining","NEM":"Mining",
    "ALB":"Chemicals","LIN":"Chemicals","PPG":"Chemicals","SHW":"Chemicals",
    "DD":"Chemicals","DOW":"Chemicals","LYB":"Chemicals","CE":"Chemicals",
    "EMN":"Chemicals","IFF":"Chemicals","RPM":"Chemicals",
    # Cybersecurity
    "FTNT":"Cybersecurity","PANW":"Cybersecurity","CRWD":"Cybersecurity",
    "ZS":"Cybersecurity","OKTA":"Cybersecurity","S":"Cybersecurity",
    # Healthcare / Managed Care
    "HUM":"Healthcare","UNH":"Healthcare","ELV":"Healthcare","CNC":"Healthcare",
    "MOH":"Healthcare","CVS":"Healthcare",
    # Medical Devices
    "MDT":"Med Devices","EW":"Med Devices","ZBH":"Med Devices","STE":"Med Devices",
    "RVTY":"Med Devices","WAT":"Med Devices","IDXX":"Med Devices",
    # Real Estate
    "AMT":"REITs","CCI":"REITs","SBAC":"REITs","DLR":"REITs","EXR":"REITs",
    "PSA":"REITs","AVB":"REITs","EQR":"REITs","MAA":"REITs","UDR":"REITs",
    # Utilities
    "NEE":"Utilities","DUK":"Utilities","SO":"Utilities","AEP":"Utilities",
    "EXC":"Utilities","XEL":"Utilities","ED":"Utilities","ES":"Utilities",
    "WEC":"Utilities","ETR":"Utilities","FE":"Utilities","PPL":"Utilities",
    "AEE":"Utilities","CMS":"Utilities","NI":"Utilities","EVRG":"Utilities",
    "LNT":"Utilities","ATO":"Utilities","PNW":"Utilities",
    # Energy
    "XOM":"Energy","CVX":"Energy","COP":"Energy","SLB":"Energy","EOG":"Energy",
    "PXD":"Energy","DVN":"Energy","MRO":"Energy","HES":"Energy","APA":"Energy",
    "FANG":"Energy","PSX":"Energy","VLO":"Energy","MPC":"Energy",
    # Consumer Discretionary
    "AMZN":"E-Commerce/Cloud","TSLA":"Auto","HD":"Retail","LOW":"Retail",
    "MCD":"Food & Bev","SBUX":"Food & Bev","NKE":"Apparel","LULU":"Apparel",
    "TJX":"Retail","ROST":"Retail","BKNG":"Travel","MAR":"Travel",
    "HLT":"Travel","CCL":"Travel","RCL":"Travel","NCLH":"Travel",
    "LVS":"Entertainment","MGM":"Entertainment","WYNN":"Entertainment",
    # Financial
    "BRK-B":"Financials","JPM":"Financials","BAC":"Financials","WFC":"Financials",
    "C":"Financials","GS":"Financials","MS":"Financials","USB":"Financials",
    "PNC":"Financials","TFC":"Financials","COF":"Financials","AXP":"Financials",
    "V":"Payments","MA":"Payments","PYPL":"Fintech","SQ":"Fintech",
    "BLK":"Asset Mgmt","SCHW":"Financials","CME":"Exchange","ICE":"Exchange",
    "CBOE":"Exchange","NDAQ":"Exchange","SPGI":"Ratings","MCO":"Ratings",
    "MMC":"Insurance","AON":"Insurance","CB":"Insurance","AIG":"Insurance",
    "PRU":"Insurance","MET":"Insurance","AFL":"Insurance","ALL":"Insurance",
    "TRV":"Insurance","PGR":"Insurance","HIG":"Insurance",
    # Misc missing
    "URI":"Industrials","JBHT":"Transportation","STLD":"Materials","NUE":"Materials",
    "STX":"Technology","BLDR":"Industrials","GNRC":"Industrials","TDG":"Industrials",
    "HWM":"Industrials","ITW":"Industrials","EMR":"Industrials","ROK":"Industrials",
    "PH":"Industrials","DOV":"Industrials","CARR":"Industrials","OTIS":"Industrials",
    "GD":"Industrials","LMT":"Industrials","RTX":"Industrials","NOC":"Industrials",
    "BA":"Industrials","HII":"Industrials","LHX":"Industrials","LDOS":"Industrials",
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


SECTOR_MAP: dict[str, str] = {
    # ── Semiconductors ──────────────────────────────
    "NVDA":"Semiconductors","AMD":"Semiconductors","INTC":"Semiconductors",
    "MU":"Semiconductors","AVGO":"Semiconductors","QCOM":"Semiconductors",
    "LRCX":"Semiconductors","AMAT":"Semiconductors","KLAC":"Semiconductors",
    "SNDK":"Semiconductors","SWKS":"Semiconductors","MCHP":"Semiconductors",
    "MPWR":"Semiconductors","ON":"Semiconductors","ALAB":"Semiconductors",
    "TXN":"Semiconductors","ADI":"Semiconductors","MRVL":"Semiconductors",
    "WOLF":"Semiconductors","NXPI":"Semiconductors","QRVO":"Semiconductors",
    # ── Technology ──────────────────────────────────
    "AAPL":"Technology","MSFT":"Technology","GOOGL":"Technology","GOOG":"Technology",
    "META":"Technology","ORCL":"Technology","CRM":"Technology","ADBE":"Technology",
    "INTU":"Technology","NOW":"Technology","WDAY":"Technology","AKAM":"Technology",
    "GEN":"Technology","DELL":"Technology","IBM":"Technology","CSCO":"Technology",
    "ANET":"Technology","SNOW":"Technology","DDOG":"Technology","NET":"Technology",
    "CRWD":"Technology","PANW":"Technology","FTNT":"Cybersecurity","ZS":"Cybersecurity",
    "PLTR":"Technology","AXON":"Technology","FICO":"Technology","SNPS":"Technology",
    "CDNS":"Technology","ACN":"Technology","ADSK":"Technology","ANSS":"Technology",
    "CDW":"Technology","CTSH":"Technology","FFIV":"Technology","GDDY":"Technology",
    "IT":"Technology","JKHY":"Technology","JNPR":"Technology","KEYS":"Technology",
    "MSCI":"Technology","MSI":"Technology","PTC":"Technology","TER":"Technology",
    "TRMB":"Technology","TYL":"Technology","VRSK":"Technology","VRSN":"Technology",
    "ZBRA":"Technology","APH":"Technology","TEL":"Technology","GLW":"Technology",
    "FDS":"Technology","EPAM":"Technology","SOLV":"Technology","VLTO":"Technology",
    "CSGP":"Technology","ROP":"Technology","BR":"Technology","ADP":"Technology",
    "PAYC":"Technology","PAYX":"Technology","MKTX":"Technology","HPE":"Technology",
    "HPQ":"Technology","SMCI":"Technology","WDC":"Technology","STX":"Technology",
    "NTAP":"Technology","HOOD":"Technology","RBLX":"Gaming","TTWO":"Gaming",
    "EA":"Gaming","TKO":"Entertainment",
    # ── Cybersecurity ────────────────────────────────
    "PANW":"Cybersecurity","CRWD":"Cybersecurity",
    # ── E-Commerce / Internet ───────────────────────
    "AMZN":"E-Commerce/Cloud","SHOP":"E-Commerce","MELI":"E-Commerce",
    "ETSY":"E-Commerce","EBAY":"E-Commerce","W":"E-Commerce",
    "BKNG":"Travel","ABNB":"Travel","EXPE":"Travel",
    "UBER":"Transportation","DASH":"Delivery",
    # ── Auto ─────────────────────────────────────────
    "TSLA":"Auto","F":"Auto","GM":"Auto","APTV":"Auto","BWA":"Auto","LKQ":"Auto",
    # ── Financials ───────────────────────────────────
    "JPM":"Financials","BAC":"Financials","GS":"Financials","WFC":"Financials",
    "USB":"Financials","C":"Financials","TFC":"Financials","PNC":"Financials",
    "COF":"Financials","AXP":"Financials","V":"Payments","MA":"Payments",
    "PYPL":"Fintech","CPAY":"Fintech","COIN":"Crypto","BLK":"Asset Mgmt",
    "MCO":"Ratings","SPGI":"Ratings","CME":"Exchange","ICE":"Exchange",
    "CBOE":"Exchange","NDAQ":"Exchange","SCHW":"Financials","BX":"Financials",
    "BEN":"Financials","IVZ":"Financials","TROW":"Financials","AMP":"Financials",
    "AJG":"Financials","BRO":"Financials","CINF":"Financials","AIZ":"Financials",
    "ACGL":"Financials","PFG":"Financials","STT":"Financials","RF":"Financials",
    "KEY":"Financials","CFG":"Financials","HBAN":"Financials","FITB":"Financials",
    "MTB":"Financials","SYF":"Financials","NTRS":"Financials","FIS":"Financials",
    "FI":"Financials","DFS":"Financials","RJF":"Financials","WRB":"Financials",
    "WTW":"Financials","L":"Financials","J":"Financials","SYF":"Financials",
    "CB":"Insurance","AON":"Insurance","MMC":"Insurance","PRU":"Insurance",
    "MET":"Insurance","AFL":"Insurance","ALL":"Insurance","TRV":"Insurance",
    "PGR":"Insurance","HIG":"Insurance","AIG":"Insurance","VICI":"Financials",
    "O":"REITs","KIM":"REITs","REG":"REITs","FRT":"REITs","CPT":"REITs",
    "ESS":"REITs","HST":"REITs","INVH":"REITs","IRM":"REITs","WELL":"REITs",
    "WY":"REITs","SPG":"REITs","ARE":"REITs","EQR":"REITs","AVB":"REITs",
    "PSA":"REITs","DLR":"REITs","AMT":"REITs","CCI":"REITs","SBAC":"REITs",
    "EQIX":"REITs","PLD":"REITs","EXR":"REITs","VTR":"REITs","UDR":"REITs",
    "CSGP":"Technology",
    # ── Healthcare ───────────────────────────────────
    "UNH":"Healthcare","ELV":"Healthcare","HUM":"Healthcare","CNC":"Healthcare",
    "MOH":"Healthcare","CVS":"Healthcare","CI":"Healthcare",
    "LLY":"Pharma","MRK":"Pharma","ABBV":"Pharma","PFE":"Pharma","JNJ":"Pharma",
    "BMY":"Pharma","AMGN":"Biotech","BIIB":"Biotech","MRNA":"Biotech",
    "GILD":"Biotech","REGN":"Biotech","VRTX":"Biotech","INCY":"Biotech",
    "ZTS":"Med Devices","TMO":"Med Devices","ABT":"Med Devices","DHR":"Med Devices",
    "SYK":"Med Devices","ISRG":"Med Devices","BSX":"Med Devices","MDT":"Med Devices",
    "EW":"Med Devices","ZBH":"Med Devices","STE":"Med Devices","RVTY":"Med Devices",
    "WAT":"Med Devices","IDXX":"Med Devices","A":"Med Devices","BAX":"Med Devices",
    "BDX":"Med Devices","CAH":"Healthcare","COR":"Healthcare","DVA":"Healthcare",
    "HCA":"Healthcare","IQV":"Healthcare","LH":"Healthcare","RMD":"Healthcare",
    "UHS":"Healthcare","VTRS":"Pharma","WST":"Healthcare","COO":"Med Devices",
    "DXCM":"Med Devices","HOLX":"Healthcare","PODD":"Med Devices","TFX":"Med Devices",
    "ALGN":"Med Devices","GEHC":"Healthcare","MTD":"Med Devices","DGX":"Healthcare",
    "HSIC":"Healthcare","SOLV":"Healthcare","DAY":"Healthcare","EG":"Healthcare",
    # ── Energy ───────────────────────────────────────
    "XOM":"Energy","CVX":"Energy","COP":"Energy","SLB":"Energy","EOG":"Energy",
    "DVN":"Energy","MRO":"Energy","HES":"Energy","APA":"Energy","FANG":"Energy",
    "PSX":"Energy","VLO":"Energy","MPC":"Energy","OXY":"Energy","BKR":"Energy",
    "KMI":"Energy","OKE":"Energy","WMB":"Energy","TRGP":"Energy","EQT":"Energy",
    "CTRA":"Energy","HAL":"Energy",
    # ── Industrials ──────────────────────────────────
    "GE":"Industrials","CAT":"Industrials","HON":"Industrials","RTX":"Industrials",
    "DE":"Industrials","EMR":"Industrials","ITW":"Industrials","ROK":"Industrials",
    "PH":"Industrials","DOV":"Industrials","CARR":"Industrials","OTIS":"Industrials",
    "GD":"Industrials","LMT":"Industrials","NOC":"Industrials","BA":"Industrials",
    "HII":"Industrials","LHX":"Industrials","LDOS":"Industrials","TDG":"Industrials",
    "HWM":"Industrials","GEV":"Industrials","BLDR":"Industrials","GNRC":"Industrials",
    "URI":"Industrials","CTAS":"Industrials","PWR":"Industrials","PCAR":"Industrials",
    "WM":"Industrials","RSG":"Industrials","FDX":"Industrials","UPS":"Industrials",
    "AME":"Industrials","AOS":"Industrials","BR":"Technology","CBRE":"Industrials",
    "CPRT":"Industrials","EXPD":"Industrials","FAST":"Industrials","FTV":"Industrials",
    "GPC":"Industrials","GWW":"Industrials","IEX":"Industrials","IR":"Industrials",
    "JCI":"Industrials","MAS":"Industrials","MLM":"Industrials","MMM":"Industrials",
    "NDSN":"Industrials","PNR":"Industrials","SNA":"Industrials","SWK":"Industrials",
    "TDY":"Industrials","TT":"Industrials","TXT":"Industrials","VMC":"Industrials",
    "WAB":"Industrials","XYL":"Industrials","AME":"Industrials","HUBB":"Industrials",
    "ETN":"Industrials","ROL":"Industrials","ALLE":"Industrials",
    "PHM":"Industrials","NVR":"Industrials","LEN":"Industrials","DHI":"Industrials",
    "TOL":"Industrials","AXTA":"Industrials","WRK":"Materials","ADP":"Technology",
    # ── Transportation ───────────────────────────────
    "JBHT":"Transportation","ODFL":"Transportation","NSC":"Transportation",
    "UNP":"Transportation","CSX":"Transportation","DAL":"Airlines","UAL":"Airlines",
    "LUV":"Airlines","AAL":"Airlines","ALK":"Airlines","FDX":"Industrials",
    # ── Materials ────────────────────────────────────
    "STLD":"Materials","NUE":"Materials","RS":"Materials","FCX":"Mining",
    "NEM":"Mining","ALB":"Chemicals","LIN":"Chemicals","PPG":"Chemicals",
    "SHW":"Chemicals","DD":"Chemicals","DOW":"Chemicals","LYB":"Chemicals",
    "CE":"Chemicals","EMN":"Chemicals","IFF":"Chemicals","APD":"Materials",
    "AMCR":"Materials","AVY":"Materials","BALL":"Materials","BG":"Materials",
    "CF":"Materials","ECL":"Chemicals","FMC":"Materials","MOS":"Materials",
    "PKG":"Materials","SEE":"Materials","ATI":"Materials","BMS":"Materials",
    "IP":"Materials","WY":"REITs","AA":"Materials","CLF":"Materials",
    "X":"Materials",
    # ── Consumer Discretionary ───────────────────────
    "COST":"Retail","WMT":"Retail","TGT":"Retail","HD":"Retail","LOW":"Retail",
    "TJX":"Retail","DLTR":"Retail","DG":"Retail","TSCO":"Retail","BBY":"Retail",
    "AZO":"Retail","ORLY":"Retail","ULTA":"Retail","KMX":"Retail","W":"E-Commerce",
    "MCD":"Food & Bev","SBUX":"Food & Bev","CMG":"Food & Bev","YUM":"Food & Bev",
    "DPZ":"Food & Bev","DRI":"Food & Bev","POOL":"Consumer","WHR":"Consumer",
    "SJM":"Consumer","LW":"Consumer","MHK":"Consumer","TPR":"Apparel",
    "RL":"Apparel","DECK":"Apparel","HAS":"Entertainment","LULU":"Apparel",
    "NKE":"Apparel","MAR":"Travel","HLT":"Travel","CCL":"Travel","RCL":"Travel",
    "NCLH":"Travel","LVS":"Entertainment","MGM":"Entertainment","WYNN":"Entertainment",
    "CZR":"Entertainment","DIS":"Entertainment","NFLX":"Streaming","CMCSA":"Telecom",
    # ── Consumer Staples ─────────────────────────────
    "PG":"Consumer","KO":"Consumer","PEP":"Consumer","PM":"Consumer","MO":"Consumer",
    "MNST":"Consumer","CL":"Consumer","MDLZ":"Consumer","GIS":"Consumer",
    "HRL":"Consumer","HSY":"Consumer","K":"Consumer","KHC":"Consumer",
    "KMB":"Consumer","KR":"Consumer","KVUE":"Consumer","CAG":"Consumer",
    "CHD":"Consumer","CLX":"Consumer","CPB":"Consumer","EL":"Consumer",
    "TAP":"Consumer","TSN":"Consumer","ADM":"Consumer","SYY":"Consumer",
    # ── Utilities ────────────────────────────────────
    "NEE":"Utilities","DUK":"Utilities","SO":"Utilities","AEP":"Utilities",
    "EXC":"Utilities","XEL":"Utilities","ED":"Utilities","ES":"Utilities",
    "WEC":"Utilities","ETR":"Utilities","FE":"Utilities","PPL":"Utilities",
    "AEE":"Utilities","CMS":"Utilities","NI":"Utilities","EVRG":"Utilities",
    "LNT":"Utilities","ATO":"Utilities","PNW":"Utilities","AES":"Utilities",
    "AWK":"Utilities","CNP":"Utilities","D":"Utilities","DTE":"Utilities",
    "EIX":"Utilities","NRG":"Utilities","PCG":"Utilities","PEG":"Utilities",
    "SRE":"Utilities","SW":"Utilities","CEG":"Utilities","VST":"Utilities",
    # ── Telecom / Media ──────────────────────────────
    "T":"Telecom","VZ":"Telecom","TMUS":"Telecom","CHTR":"Telecom",
    "FOXA":"Media","FOX":"Media","NWS":"Media","NWSA":"Media","OMC":"Media",
    "PARA":"Media","WBD":"Media","IPG":"Media","LYV":"Entertainment",
    # ── Clean Energy ─────────────────────────────────
    "ENPH":"Clean Energy","BE":"Clean Energy","FSLR":"Clean Energy",
    # ── Final 12 ─────────────────────────────────────
    "BRK-B":"Financials","CMI":"Industrials","CTVA":"Agriculture",
    "EFX":"Technology","GRMN":"Technology","KDP":"Consumer",
    "LEG":"Consumer","MAA":"REITs","MS":"Financials",
    "ROST":"Retail","STZ":"Consumer","WBA":"Healthcare",
    # ── Misc ─────────────────────────────────────────
    "GEV":"Industrials","HOOD":"Fintech","DASH":"Delivery","RBLX":"Gaming",
    "TTWO":"Gaming","TKO":"Entertainment","SMCI":"Technology",
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
