# State Definition — Phase 2 Frozen

**冻结时间：Phase 2 完成**
**禁止修改本文档中的任何公式，除非完成新一轮回测。**

---

## 1. RS Score

```
Return60 = (Price_now - Price_60d_ago) / Price_60d_ago
RS_Score = percentile(Return60, all_SP500_60d_returns)
基准：SPX (^GSPC)，禁止 SPY
输出：0~100
```

---

## 2. Momentum Score

```
Momentum Score =
  0.30 × Return20_Percentile
+ 0.40 × Return60_Percentile
+ 0.30 × MA50_Slope_Percentile
输出：0~100（全市场横截面百分位）
```

---

## 3. Trend Health Score

```
= Price_Structure(30%)
+ MA50_Slope_Quality(25%)
+ Drawdown_Stability(25%)
+ Volatility_Quality(20%)
禁止包含 RS 或 Momentum
输出：0~100
```

### Price Structure（满分30）
- Close > MA20 = +10
- Close > MA50 = +10
- Close > MA200 = +10

### MA50 Slope Quality（满分25）
- 斜率归一化映射到 0-25

### Drawdown Stability（满分25）
| 回撤 | 原始分 | 得分 |
|------|--------|------|
| <5%  | 100    | 25   |
| 5~8% | 80     | 20   |
| 8~12%| 50     | 12.5 |
| 12~15%| 25    | 6.25 |
| >15% | 0      | 0    |

### Volatility Quality（满分20）
| 波动率 | 原始分 | 得分 |
|--------|--------|------|
| <20%   | 100    | 20   |
| 20~35% | 75     | 15   |
| 35~50% | 50     | 10   |
| 50~70% | 25     | 5    |
| >70%   | 0      | 0    |

---

## 4. Leader Score

```
= 0.40 × RS_Score
+ 0.35 × Momentum_Score
+ 0.25 × Trend_Health
输出：0~100
```

---

## 5. Promotion Score

```
= 0.40 × Momentum_Score
+ 0.30 × Trend_Health
+ 0.20 × Rank_Velocity
+ 0.10 × Momentum_Acceleration
输出：0~100
```

---

## 6. Trend Lifecycle States

| State | 条件 |
|-------|------|
| Expansion    | TH≥80 AND Mom≥80 AND RS≥80 |
| Healthy Trend| TH≥65 AND Mom≥65 |
| Mature Trend | TH≥50 |
| Weakening Trend | TH≥30 |
| Broken Trend | TH<30 |

---

## 7. Trade Rules（量化阈值）

| Action | 条件 |
|--------|------|
| BUY    | Expansion AND Mom≥80 AND RS≥80 |
| ADD    | Healthy AND Mom≥70 |
| HOLD   | Mature |
| REDUCE | Weakening |
| EXIT   | Broken OR Price < MA50 |

---

## 8. Market Score

```
= SPX_Score × 35%
+ NDX_Score × 25%
+ SOX_Score × 25%
+ VIX_Score × 15%
输出：0~100
≥80 = Risk-On，60~79 = Neutral，<60 = Risk-Off
```

### Leadership Confirmed
```
SPX_Score > 70 AND NDX_Score > 70 AND SOX_Score > 70
```
