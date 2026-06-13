"""
update_pipeline.py — 每日更新管道 Phase 2

关键修复：
1. SPX 基准统一用 ^GSPC，禁止 SPY
2. 四大指数文件名修复（^ → _ 的转换）
3. 横截面百分位基准（全市场同日计算）
4. Momentum Score 需要全市场 ret20/ret60/ma50slope 列表
"""
from __future__ import annotations
from datetime import datetime, timedelta

try:
    import pytz
    ET = pytz.timezone("America/New_York")
except:
    from datetime import timezone, timedelta as td
    ET = timezone(td(hours=-4))

from ..data_ingestion.fetch_yahoo import (
    fetch_members, download_bulk, download_single,
    download_with_fallback, append_prices, get_price_series,
)
from ..features.rs import period_return, rs_percentile
from ..features.momentum import (
    moving_average, linreg_slope, period_return as mom_ret,
    ma50_slope as calc_ma50_slope, pct_rank,
)
from ..engine.market_regime import compute as compute_market
from ..engine.market_score import compute_market_score
from ..engine.index_analysis import analyze_all_indices
from ..engine.trend_state import compute_stock_state
from ..engine.leader_ranking import rank_stocks
from ..engine.trade_decision import enrich_action
from ..engine.watchlist import build_watchlist
from ..engine.rank_history import save_daily_snapshot
from ..engine.validation import run_validation
from ..export.export_json import export_all
from ..utils.config import (
    MEMBERS_FILE, CONSTITUENTS_FILE, SPY_SYMBOL,
    INCREMENTAL_DAYS, MIN_HISTORY_DAYS,
)
from ..utils.helpers import read_json, write_json
from ..utils import logger

# 四大指数下载代码：包含原始指数和 ETF 备用
# 原始指数（^ 开头）在某些环境下可能失败，ETF 作为备用
# 四大指数下载代码（主代码 + fallback）
WATCH_INDICES = ["^GSPC", "^NDX", "^VIX", "^SOX", "SPY"]

INDEX_FALLBACKS = {
    "^GSPC": ["SPY"],
    "^NDX":  ["QQQ"],
    "^VIX":  ["VIXY"],
    "^SOX":  ["SOXX"],
    "SPY":   [],
}

# 文件名安全转换：^ → _（文件系统不支持 ^ 开头）
def sym_to_file(sym: str) -> str:
    return sym.replace("^", "_")

def file_to_sym(fname: str) -> str:
    return fname  # 读取时用原始代码


def load_constituents() -> list[str]:
    data = read_json(CONSTITUENTS_FILE)
    if data and isinstance(data, list) and len(data) >= 500:
        logger.ok(f"成分股：{len(data)} 只")
        return data
    members = read_json(MEMBERS_FILE)
    if members and isinstance(members, list):
        syms = [m["symbol"] if isinstance(m, dict) else m for m in members]
        logger.warn(f"members.json 兜底：{len(syms)} 只")
        return syms
    from ..data_ingestion.fetch_yahoo import _FALLBACK
    return list(_FALLBACK)


def load_members_map(symbols) -> dict:
    from ..data_ingestion.fetch_yahoo import get_sector
    members = read_json(MEMBERS_FILE) or []
    m = {x["symbol"]: x for x in members if isinstance(x, dict) and "symbol" in x}
    # 对每个成分股，确保 sector 正确（优先用 members.json，否则用 SECTOR_MAP）
    for s in symbols:
        if s not in m:
            m[s] = {"symbol": s, "name": s, "sector": get_sector(s)}
        elif m[s].get("sector") in ("Other", "", None):
            # members.json 里有但 sector 为 Other，用 SECTOR_MAP 覆盖
            mapped = get_sector(s)
            if mapped != "Other":
                m[s]["sector"] = mapped
    return m


def get_prices_safe(sym: str) -> tuple[list[str], list[float]]:
    """
    安全读取价格：先尝试原始代码，再尝试文件名安全版本。
    修复：^GSPC 存储为 _GSPC.json
    """
    d, p = get_price_series(sym)
    if p:
        return d, p
    # 尝试文件名转义版本
    safe_sym = sym_to_file(sym)
    if safe_sym != sym:
        d, p = get_price_series(safe_sym)
    return d, p


def run_daily_update(force_full: bool = False) -> None:
    now   = datetime.now(ET)
    today = now.strftime("%Y-%m-%d")
    logger.info(f"=== SP500 Cockpit Phase 2 @ {now.strftime('%Y-%m-%d %H:%M')} ===")

    # ── P0-1: 成分股 ─────────────────────────────────
    symbols     = load_constituents()
    members_map = load_members_map(symbols)

    # ── P0-2: 增量下载 ────────────────────────────────
    logger.info("[1/6] 增量更新价格...")
    if force_full:
        start = (now - timedelta(days=730)).strftime("%Y-%m-%d")
        logger.info(f"  全量模式：{start}")
    else:
        start = (now - timedelta(days=INCREMENTAL_DAYS)).strftime("%Y-%m-%d")
    end = (now + timedelta(days=1)).strftime("%Y-%m-%d")

    new_data = download_bulk(symbols + [SPY_SYMBOL], start, end, batch_size=80, sleep=1.0)
    updated = sum(1 for sym, df in new_data.items() if append_prices(sym, df) > 0)
    logger.info(f"  → 更新 {updated} 只成分股")

    # 四大指数：用 download_with_fallback 下载
    # 无论用哪个代码下载成功，统一存储到原始代码路径（如 ^GSPC）
    idx_full_start = (now - timedelta(days=730)).strftime("%Y-%m-%d")
    for idx_sym in WATCH_INDICES:
        _, p_exist = get_prices_safe(idx_sym)
        idx_start_date = idx_full_start if len(p_exist) < 60 else start
        if len(p_exist) < 60:
            logger.info(f"  {idx_sym}: 首次下载2年历史...")
        used_sym, df = download_with_fallback(
            idx_sym,
            INDEX_FALLBACKS.get(idx_sym, []),
            idx_start_date,
            end,
        )
        if df is not None and not df.empty:
            # 存储到原始代码路径，不管实际用了哪个 fallback
            n = append_prices(idx_sym, df)
            if n > 0:
                logger.info(f"  {idx_sym}: +{n} 条 (source={used_sym})")
        else:
            logger.warn(f"  {idx_sym}: 所有 fallback 下载失败")

        # ── P0-3: 验证 ────────────────────────────────────
    logger.info("[2/6] 数据验证...")
    health = run_validation(symbols)
    if not health["signal_engine_enabled"]:
        logger.error("❌ 数据验证 FAIL，信号引擎已禁用")
        return

    # ── 加载价格序列 ──────────────────────────────────
    logger.info("[3/6] 加载价格序列...")
    prices_map: dict[str, list[float]] = {}
    dates_map:  dict[str, list[str]]   = {}

    for sym in symbols + WATCH_INDICES:
        d, p = get_prices_safe(sym)
        if len(p) >= MIN_HISTORY_DAYS:
            prices_map[sym] = p
            dates_map[sym]  = d

    # P0 修复：SPX 必须用 ^GSPC，不能用 SPY
    def get_idx(*keys):
        for k in keys:
            p = prices_map.get(k) or prices_map.get(k.replace("^","_")) or []
            if len(p) >= 20: return p
        return []

    spx_prices = get_idx("^GSPC", "SPY")
    ndx_prices = get_idx("^NDX",  "QQQ")
    vix_prices = get_idx("^VIX", "VIXY")
    sox_prices = get_idx("^SOX",  "SOXX")

    logger.info(f"  → 有效序列：{len(prices_map)} 只")
    logger.info(f"  → SPX: {len(spx_prices)} bars  NDX: {len(ndx_prices)} bars  VIX: {len(vix_prices)} bars  SOX: {len(sox_prices)} bars")

    # ── Phase 2 横截面基准计算 ──────────────────────────
    logger.info("[4/6] 计算横截面百分位基准...")
    all_ret20:     list[float] = []
    all_ret60:     list[float] = []
    all_ma50_slopes: list[float] = []

    for sym in symbols:
        if sym not in prices_map:
            continue
        p = prices_map[sym]
        all_ret20.append(mom_ret(p, 20))
        all_ret60.append(period_return(p, 60) or 0.0)
        all_ma50_slopes.append(calc_ma50_slope(p))

    logger.info(f"  → 横截面样本：{len(all_ret60)} 只")

    # ── 信号引擎 ──────────────────────────────────────
    logger.info("[5/6] 运行信号引擎...")
    stock_signals: list[dict] = []
    for sym in symbols:
        if sym not in prices_map:
            continue
        try:
            result = compute_stock_state(
                sym, prices_map[sym], dates_map[sym],
                spx_prices,          # P0 修复：用 ^GSPC
                all_ret20, all_ret60, all_ma50_slopes,
                members_map,
            )
            if result:
                stock_signals.append(enrich_action(result))
        except Exception as e:
            logger.warn(f"  {sym}: {e}")

    # 把 market_score 注入每只股票，供 trade_decision 使用
    msc_value = ms.get("market_score", 60) if isinstance(ms, dict) else 60
    for s in stock_signals:
        s["market_score"] = msc_value

    stock_signals = rank_stocks(stock_signals)
    leaders   = stock_signals[:10]

    # 保存每日排名快照（供 Rank Velocity 和 Momentum Acceleration 使用）
    save_daily_snapshot(today, stock_signals[:100])

    watchlist = build_watchlist(stock_signals)
    logger.info(f"  → {len(stock_signals)} 只完成 | Top3: {', '.join(s['symbol'] for s in leaders[:3])}")

    # ── Market Regime Engine ──────────────────────────
    logger.info("[6/6] Market Regime Engine + 导出...")
    ms = compute_market_score(spx_prices, ndx_prices, sox_prices, vix_prices)

    up  = sum(1 for p in prices_map.values() if len(p) >= 2 and p[-1] > p[-2])
    dn  = sum(1 for p in prices_map.values() if len(p) >= 2 and p[-1] < p[-2])
    adr = up / max(dn, 1)

    market = compute_market(spx_prices, adr)
    market.update({
        "date":          today,
        "advance_count": up,
        "decline_count": dn,
        "notes":         f"上涨{up}只 下跌{dn}只",
        "state":         ms["state"],
        "state_zh":      ms["state_zh"],
        "state_icon":    ms["state_icon"],
        "state_color":   ms["state_color"],
        "market_score":  ms["market_score"],
        "score_breakdown": ms["breakdown"],
        "leadership_confirmed": ms["leadership_confirmed"],
        "leadership_label":     ms["leadership_label"],
        "vix_state":     ms["vix_state"],
        "vix_color":     ms["vix_color"],
        "spx_score":     ms["spx_score"],
        "ndx_score":     ms["ndx_score"],
        "sox_score":     ms["sox_score"],
        "vix_score":     ms["vix_score"],
    })

    # P0 修复：用 ^GSPC 真实指数价格（约7500+，非SPY约756）
    if len(spx_prices) >= 50:
        ma50  = sum(spx_prices[-50:]) / 50
        ma200 = sum(spx_prices[-200:]) / 200 if len(spx_prices) >= 200 else sum(spx_prices) / len(spx_prices)
        sl20  = linreg_slope(spx_prices[-20:]) if len(spx_prices) >= 20 else 0
        market.update({
            "spx_close":      round(spx_prices[-1], 2),
            "spx_ma50":       round(ma50, 2),
            "spx_ma200":      round(ma200, 2),
            "spx_slope20":    round(sl20, 6),
            "pct_above_ma50": round((spx_prices[-1] - ma50) / ma50 * 100, 2),
        })

    # 四大指数分析
    indices = analyze_all_indices(prices_map, dates_map)
    market["indices"] = indices

    # market_score 注入每只股票，重新计算 trade_action
    msc_value = ms.get("market_score", 60)
    for s in stock_signals:
        s["market_score"] = msc_value
    stock_signals = [enrich_action(s) for s in stock_signals]
    leaders   = stock_signals[:10]
    watchlist = build_watchlist(stock_signals)

    logger.info(f"  Market Score: {ms['market_score']} → {ms['state_icon']} {ms['state_zh']}")
    logger.info(f"  Leadership: {ms['leadership_label']}")
    if spx_prices:
        logger.info(f"  SPX: {spx_prices[-1]:.2f}  NDX: {bool(ndx_prices)}  VIX: {bool(vix_prices)}  SOX: {bool(sox_prices)}")

    export_all(market, leaders, watchlist, stock_signals[:50])
    logger.ok(f"=== Phase 2 更新完成 @ {datetime.now(ET).strftime('%H:%M')} ===")
