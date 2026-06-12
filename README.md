# SP500 Trend Decision Support Cockpit

> Swing Trend Following · 持仓周期 1–3周

每天回答6个问题：今天适合交易吗？最强股是谁？买什么？持有什么？卖什么？下一批领导股是谁？

**Dashboard**: https://donarfang.github.io/SP500-tracker/dashboard/

---

## 快速部署

```bash
# 1. 上传代码到 GitHub
git push

# 2. Settings → Pages → GitHub Actions

# 3. Actions → 初始化历史数据 → Run workflow（约15分钟）

# 4. 每日 18:00 ET 自动更新
```

## 架构

```
data/sp500_constituents.json  ← 504只成分股（本地权威库）
data/prices/*.json            ← 每只股票独立价格文件
       ↓
src/features/   rs · momentum · trend_health
src/engine/     market_regime · market_score · leader_ranking
                trend_state · trade_decision · watchlist
                index_analysis · validation
       ↓
exports/*.json  → dashboard/
```

## 自动更新时间

| 时区 | 时间 |
|------|------|
| 美东 ET | 18:00 |
| 北京（夏） | 06:00 次日 |
| 北京（冬） | 07:00 次日 |

*不构成投资建议。*
