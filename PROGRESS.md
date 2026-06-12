# SP500 Cockpit — 开发进度

## 当前状态：Phase 2 完成 ✅

---

## Phase 2 变更摘要

### 指标公式全部冻结（禁止修改）

| 指标 | Phase 1 | Phase 2 |
|------|---------|---------|
| RS 基准 | SPY | **^GSPC（禁止SPY）** |
| Momentum Score | 斜率加权 | **0.30×Ret20Pct + 0.40×Ret60Pct + 0.30×MA50SlopePct，输出0-100** |
| Trend Health | 含RS/Momentum | **纯趋势质量：PS(30%)+MA50Slope(25%)+DD(25%)+Vol(20%)** |
| Leader Score | 0.5×RS+0.3×M+0.2×TH | **0.40×RS+0.35×M+0.25×TH** |
| Promotion Score | 旧公式 | **0.40×Mom+0.30×TH+0.20×RankVel+0.10×MomAccel** |
| Watchlist | Rank 11-30 | **Promotion Score Top20** |
| Trade Rules | 文字状态 | **量化阈值（BUY:Expansion+Mom≥80+RS≥80）** |
| Leadership | price/MA结构 | **SPX Score>70 AND NDX Score>70 AND SOX Score>70** |

### P0 修复
- SPX 显示 ~756 → 现在用 ^GSPC 真实指数价格（~7580）
- 四大指数 N/A → 修复 ^ 文件名匹配（get_prices_safe()）
- 横截面百分位基准：全市场同日计算 all_ret20/all_ret60/all_ma50_slopes

---

## Phase 2 文件清单 ✅

```
src/features/rs.py              ← RS基准改^GSPC，rs_score()输出0-100
src/features/momentum.py        ← 百分位制，需要全市场横截面列表
src/features/trend_health.py    ← 纯趋势质量，剔除RS/Momentum
src/engine/leader_ranking.py    ← 新权重0.40/0.35/0.25
src/engine/trade_decision.py    ← 量化阈值规则
src/engine/watchlist.py         ← Promotion Score Top20
src/engine/market_score.py      ← Leadership条件改为各指数Score>70
src/engine/trend_state.py       ← 整合所有Phase 2指标
src/engine/backtest.py          ← 新增：回测引擎
src/pipeline/update_pipeline.py ← 修复P0+整合横截面计算
src/export/export_json.py       ← 支持backtest.json输出
docs/state_definition.md        ← 指标冻结文档
```

---

## Phase 3 待办（下一次会话）

- Dashboard UI 精化（显示新指标字段）
- Trade Dashboard 显示 RS Score / Momentum Score 明细
- Lifecycle Tab 改用 Trend State 5档分类
- Watchlist 显示 Rank Velocity + Momentum Acceleration
- 运行完整2年回测，结果展示在新 Tab
- AI Summary 增强
- 手机端优化

---

## 关键路径

```
sp500_constituents.json (506只)
→ download_bulk() → data/prices/*.json
→ 横截面计算 (all_ret20/ret60/slopes)
→ compute_stock_state() [Phase 2指标]
→ rank_stocks() → build_watchlist() [Top20]
→ compute_market_score() [4指数]
→ export_all() → exports/*.json
→ dashboard/app.js
```

## GitHub
- Repo:  DonarFang/SP500-tracker
- Pages: https://donarfang.github.io/SP500-tracker/dashboard/
- EXPORTS_BASE: https://donarfang.github.io/SP500-tracker/exports
