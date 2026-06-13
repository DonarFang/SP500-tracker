# Layer D: Portfolio Simulation Assumptions

## Version 1.0 (Frozen)

**Date:** 2026-06-13
**Status:** FROZEN — 所有回测必须使用以下参数，不得修改。
如需更改，创建 v1.1 并记录原因。

---

## Capital & Position Sizing

| Parameter | Value | Notes |
|-----------|-------|-------|
| Initial Capital | $100,000 | 基准资金 |
| Max Positions | 10 | 同时最多持有10只 |
| BUY Position Size | 10% of portfolio | 初始建仓 = 组合的10% |
| ADD Position Size | +5% of portfolio | 加仓增量 = 组合的5% |
| Max Single Position | 15% of portfolio | 单只最大仓位上限 |
| Equal Weight | Yes | 初始建仓等权重 |
| Cash Yield | 0% | 现金不计利息 |
| Leverage | None | 不允许杠杆 |
| Short Selling | None | 不允许做空 |

---

## Position State Machine

```
size:
  0.0  = no position (cash)
  0.5  = half position  (5% of portfolio)
  1.0  = full position  (10% of portfolio)
  1.5  = overweight     (15% of portfolio, max)

BUY:    size == 0  → size = 1.0   (open new trade)
ADD:    size > 0   → size = min(1.5, size + 0.5)
HOLD:   size > 0   → maintain, update highest_close
REDUCE: size > 0.5 → size = max(0.5, size - 0.5)
EXIT:   size > 0   → size = 0.0   (close full position)
```

---

## Execution Rules

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Execution Price | Next trading day close | 避免前视偏差（信号日当天无法执行） |
| Transaction Cost | 0.05% per trade | 单边手续费 |
| Slippage | 0.05% per trade | 滑点假设 |
| Total Round Trip Cost | 0.20% | 买入+卖出合计 |
| Partial Fill | Not modeled | 假设全部成交 |
| Dividend | Not included | 不计股息再投资 |

---

## Risk Rules

| Parameter | Value |
|-----------|-------|
| Stop Loss | Signal-based only (EXIT signal) |
| Take Profit | Signal-based only (EXIT signal) |
| Max Drawdown Halt | None (full simulation) |
| Rebalancing | Signal-driven only |

---

## Benchmark

| Benchmark | Description |
|-----------|-------------|
| Primary | SPX Buy & Hold（同期持有SPX） |
| Secondary | Equal Weight S&P500 |

---

## Rationale for Key Decisions

**为什么用次日收盘价执行？**
信号基于当日收盘数据计算，当日无法执行，次日收盘是最保守的假设，避免前视偏差。

**为什么初始仓位10%（而不是等分持仓）？**
允许 ADD 加仓到15%，如果一开始就满仓（10只 × 10%），则没有空间加仓。

**为什么设 0.05% 交易成本？**
对应现代美股 ETF 级别的低佣金环境，保守合理。

**为什么 Cash Yield = 0%？**
简化假设，不引入利率变量，专注于股票选择的 Alpha。

---

## Frozen Parameters Summary

```python
LAYER_D_ASSUMPTIONS = {
    "initial_capital":     100_000,
    "max_positions":       10,
    "buy_size":            1.0,    # 10% of portfolio
    "add_size":            0.5,    # +5% of portfolio
    "max_single_size":     1.5,    # 15% of portfolio
    "transaction_cost":    0.0005, # 0.05% one-way
    "slippage":            0.0005, # 0.05% one-way
    "execution":           "next_day_close",
    "cash_yield":          0.0,
    "leverage":            False,
    "short_selling":       False,
}
```

---

*任何对上述参数的修改必须创建新版本（v1.1）并说明理由。*
*首轮回测必须使用 v1.0 参数，不得在验证期间调整。*
