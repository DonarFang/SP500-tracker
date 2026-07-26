---
name: FD-M3180125_ENGINE_CANONICAL_CURRENT_STATE
project: SP500趋势跟踪分析及交易辅助系统
engine: FD-M3180125-SP500-TOP3-engine
status: CANONICAL_CURRENT_STATE
authority: CURRENT_IMPLEMENTATION_ENTRY
last_updated: 2026-07-26
---

# FD-M3180125 Engine Canonical Current State

## 0. 文档地位

本文件是 `FD-M3180125-SP500-TOP3-engine` 当前状态、当前架构和后续开发的唯一 Canonical Current State 入口。

历史 Daily Log、RCA、Handoff、旧方案和错误架构统一视为：

```text
STATUS = HISTORICAL / AUDIT ONLY
```

它们只用于审计、追溯和防止重犯，不得覆盖本文件，不得作为当前实现依据。

若当前源码和本文件冲突：

```text
STOP
READ-ONLY INVESTIGATION
IDENTIFY THE FIRST CONFLICT
DO NOT PATCH
DO NOT GUESS
REPORT FACT / INFERENCE / UNKNOWN
WAIT FOR USER APPROVAL
```

## 1. Canonical Identity

```text
Engine: FD-M3180125-SP500-TOP3-engine
Variant: E1R_REGIME_AWARE_V0_2_STATEFUL_MAX3
Repo: /Users/dongfang/Downloads/sp500-tracker-v13
Historical read-only repo: /Users/dongfang/Downloads/sp500-tracker-5y
Branch: main
```

## 2. CURRENT AUTHORITY ORDER

```text
1. 当前源码和确切 HEAD
2. Canonical Current State
3. 冻结合同和 Official Artifacts
4. 最新 Daily Log
5. 历史 RCA / Handoff
6. 对话记忆和推断
```

低优先级来源不得覆盖高优先级来源。若两个高优先级来源冲突，立即停止实现。

## 3. FACT / INFERENCE / UNKNOWN

```text
FACT：有源码、确切 commit、冻结合同、Official Artifact、日志、trace 或可复现实验证据。
INFERENCE：从 FACT 推导，必须明确标注。
UNKNOWN：尚未证明，不能作为实现依据，不能编码。
```

## 4. 固定总体计划

项目只有三步，不得新增、改名或扩展。

### Step 1 — Canonical 5Y Official Artifact

```text
STATUS: COMPLETE / PASS
```

已完成 UPTREND、SIDEWAYS / MA_CONFLICT、Canonical Regime、Market State、Market Gate、Regime Router、Ranking、Max-3、T+1、Account、Trades、Equity Curve 和 Official Artifacts。

正式 5Y 结果：

```text
Initial capital: 100,000.00
Final equity:    281,711.79
Total return:    +181.71%
SPX return:      +76.84%
Alpha:           +104.87%
CAGR:            +23.00%
Max Drawdown:    29.83%
Profit Factor:   2.21
Sharpe:          0.71
Trades:          92
Exposure:        69.3%
```

Canonical result SHA256：

```text
d8a5ea27ba0d8a7e8f7042bcbd09ffe67799f3b094a81cb92141a70f3075d593
```

### Step 2 — Shared Runtime + Forward / Live Tracks

```text
STATUS: IN_PROGRESS
```

包含两条严格隔离的轨道：

```text
Engine Forward Track
Personal Live Track
```

二者共享唯一 Engine 核心，但不共享运行事实。

### Step 3 — Dashboard Manifest Integration and E2E

```text
STATUS: NOT_STARTED
```

仅 Step 3 才允许 Dashboard 接入 Backtest / Forward / Live Official Artifacts、三条 Equity Curve、Forward vs Live 对比和最终切换。Dashboard 不得计算策略。

## 5. 唯一正确的 Engine 架构

唯一策略入口：

```text
E1RCoreEngine.step(...)
```

### 5.1 Engine 之前

Forward 和 Live 各自拥有独立输入：

```text
Forward:
  data/fw_prices
  Forward Account State

Live:
  data/live_prices
  Actual Live Account State
```

Data / Account Adapter 只负责：

```text
Raw Market Data → Standard Market Data Contract
Mode Account → Standard Engine AccountState
```

Adapter 不得生成 Canonical Regime、Market State、Market Gate、策略分支、Ranking、Sizing 或交易动作。

### 5.2 Mode-specific Thin Shell

Forward 和 Live 各自允许一个薄壳：

```text
Mode-specific Engine Adapter / Composition Thin Shell
```

薄壳只负责：

1. 接收标准 Market Data；
2. 接收标准 AccountState；
3. 调用一次 `E1RCoreEngine.step(...)`；
4. 读取 Engine Result；
5. 映射为 Forward 或 Live 的对外格式。

薄壳不得先调用 Market State / Gate 再输入 Engine，不得在 Engine 外重算 Regime、路由策略或生成第二套交易动作。

### 5.3 Engine 内唯一产生

以下内容只能由唯一 Engine 内部产生：

```text
Canonical Regime
Market State
Market Gate
Regime Router
UPTREND
SIDEWAYS / MA_CONFLICT
DOWNTREND
Ranking
Position Management
Position Sizing
BUY / ADD / HOLD / REDUCE / EXIT
Decision Trace
OrderIntent source decision
```

唯一正确调用链：

```text
Independent Raw Data + Account
→ Data / Account Adapter
→ Standard Engine Input
→ Mode-specific Thin Shell
→ ONE call to E1RCoreEngine.step(...)
→ Engine generates all states and strategy decisions
→ Mode-specific output mapping
```

## 6. Engine Forward Canonical Architecture

### 6.1 定位

Engine Forward 是 Canonical 5Y Backtest 在未来日期上的模型连续延伸。

### 6.2 正确链路

```text
Yahoo Finance
→ Engine Forward Price Updater
→ data/fw_prices
→ Forward Data Adapter
→ Forward Account Adapter / Repository
→ Standard Engine Input
→ Forward Composition Thin Shell
→ ONE call to E1RCoreEngine.step(...)
→ Engine OrderIntent
→ T+1 Model Execution
→ Model Fill
→ Forward Account State
→ Forward Runtime
→ Forward Equity Curve
```

### 6.3 独立边界

Forward 独立拥有：

```text
data/fw_prices
Forward Seed
Forward Account State
Forward Pending Orders
Forward OrderIntent
Forward Model Fills
Forward Runtime
Forward Daily Artifacts
Forward Equity Curve
Forward Automation Status
```

Forward 不得读取或写入 Live 数据、账户、账本、Runtime 或 Equity Curve。

### 6.4 执行语义

```text
Engine Decision = Model Execution
```

Forward 不允许人工改变 symbol、action、amount、execution choice、timing 或 model fill contract。无交易时仍必须完成 EOD mark-to-market。

### 6.5 当前状态

```text
Canonical Seed date = 2026-06-16
First Forward date  = 2026-06-17
```

已完成 Shared Runtime、Adapter、Composition、Formal Catch-up、Runtime Acceptance、独立 Runtime、独立 Equity、独立价格更新器、独立 schedule 和 Legacy 隔离。

当前唯一 Forward 下一入口：

```text
OBSERVE_FIRST_INDEPENDENT_ENGINE_FORWARD_PRODUCTION_RUN
```

## 7. Personal Live Canonical Architecture

### 7.1 定位

Live Track 基于用户真实账户和实际成交：

```text
Engine Recommendation != Actual User Execution
```

### 7.2 正确链路

```text
Yahoo Finance
→ Live Price Updater
→ data/live_prices
→ Live Data Adapter
→ Live Account Adapter
→ Standard Engine Input
→ Live Engine Adapter Thin Shell
→ ONE call to E1RCoreEngine.step(...)
→ Engine Decision
→ Live Recommendation Mapping
→ User Decision
→ Actual User Execution
→ Transaction Ledger
→ Cash Control Ledger
→ Rebuild Live Account State
→ Live Runtime
→ Live Equity Curve
```

### 7.3 独立边界

Live 独立拥有：

```text
data/live_prices
Live Opening State
Live Account State
Transaction Ledger
Cash Control Ledger
Engine Recommendations
Actual User Executions
Reconciliation
Live Runtime
Live Daily Artifacts
Live Equity Curve
```

Live 不得读取或写入 Forward Seed、账户、Orders、Fills、Runtime 或 Equity Curve。

### 7.4 两账本一个账户

```text
Opening State
+ Transaction Ledger
+ Cash Control Ledger
→ One Live Account State
```

`actual_cash` 为权威现金；`calculated_cash` 和 `cash_difference` 用于审计。

### 7.5 当前状态

已完成 Live Account Contract、Two-ledger Core、Daily Processing、Runtime Persistence、Reconciliation、独立数据、Data/Account/Engine Adapter、Production Composition、Real Engine unactivated E2E 和 Official Unactivated Live Acceptance。

当前保持：

```text
opening_activated = false
Live workflow = not created
real user account = not loaded
actual user trades = none
broker API = none
automatic execution = none
```

## 8. Forward / Live 严格隔离合同

只共享：

```text
E1R Engine source code
Frozen strategy contracts
Standard Engine data contracts
Standard Engine account contracts
```

不共享：

```text
Raw data directory
Seed / Opening
Account State
Pending Orders
OrderIntent / Fills
Transaction / Cash Ledgers
Runtime
Last processed date
Recovery state
Automation state
Equity Curve
Acceptance evidence
Tests as proof
```

禁止用 Forward 成功证明 Live，也禁止用 Live 成功证明 Forward。

## 9. SUPERSEDED / FORBIDDEN ARCHITECTURES

以下名称和架构已废弃：

```text
ExplicitMarketStateProvider
FormalMarketGateProvider
FormalManagementActionProvider
```

禁止：

```text
Data Adapter generates Market State / Gate
Data Adapter selects UPTREND / SIDEWAYS
Engine Adapter calls Market Status and feeds it back into Engine
Forward or Live recomputes Regime / State / Gate outside Engine
Forward and Live use different strategy cores
Forward or Live layer owns strategy decisions
Multiple sources of truth for Market State / Gate / actions
```

禁止作为当前架构的旧表述：

```text
Data Adapter
→ CanonicalRegimeGenerator
→ MarketStateEvaluator
→ MarketGateEvaluator
→ E1RCoreEngine
```

唯一正确替代：

```text
Data / Account Adapter
→ Standard Engine Input
→ Thin Shell calls E1RCoreEngine.step() once
→ Engine internally generates Regime / State / Gate / Strategy
→ Thin Shell maps Engine Result
```

## 10. 固定新对话 / 恢复开发启动流程

```text
1. 读取 CURRENT_PROJECT_STATE.md
2. 读取 docs/canonical/FD-M3180125_ENGINE_CANONICAL_CURRENT_STATE.md
3. 读取最近 3 天 Daily Log
4. 仅在出现问题时读取相关 RCA
5. 核对 HEAD / origin/main / working tree
6. 区分 FACT / INFERENCE / UNKNOWN
7. 再提出下一步
```

## 10A. 本地 Python 验证环境合同

本地验证必须读取：

```text
docs/canonical/FD-M3180125_LOCAL_PYTHON_VALIDATION_CONTRACT.md
```

统一环境解析器：

```text
scripts/lib/fd_m3180125_python_env.sh
```

冻结规则：

```text
不得写死用户专用 venv 路径
不得假设 system python3 已安装 pytest
不得为了让脚本通过而隐式安装 pytest
pytest 缺失不得被判定为 Engine / Adapter / 架构失败
```

本地强制验证基线：

```text
py_compile / compileall
纯 Python assertions
direct contract validation
必要时 AST / source-boundary validation
```

pytest 仅在解析出的 Python 环境已经提供 pytest 时可选运行；否则记录：

```text
TESTS_SKIPPED_PYTEST_UNAVAILABLE
```

## 11. 实施规则

代码、Shell、Workflow、配置或 Patch 之前必须先说明目标、范围、不做什么、依赖事实、修改文件、验收标准和失败保护，并获得用户确认。

同一目标连续失败三次：

```text
STOP
NO FOURTH PATCH
RCA REQUIRED
```

Git：

```text
No git add .
Explicit staging whitelist only
Commit
Push
HEAD == origin/main
Working tree clean
Daily Log updated
Archive completed
```

## 12. 当前下一步入口

```text
Forward:
OBSERVE_FIRST_INDEPENDENT_ENGINE_FORWARD_PRODUCTION_RUN

Live:
DO NOT ACTIVATE LIVE OPENING

Dashboard:
NOT_STARTED
```

## 13. Canonical Final Statement

```text
Forward 和 Live 使用不同的数据、账户、执行、Runtime 和 Equity Curve。

两者都通过各自的 Data / Account Adapter 构造标准 Engine 输入，
再由各自的 Thin Shell 只调用一次同一个 E1RCoreEngine.step()。

Canonical Regime、Market State、Market Gate、Regime Router、
UPTREND、SIDEWAYS / MA_CONFLICT、DOWNTREND、Ranking、Sizing 和
BUY / ADD / HOLD / REDUCE / EXIT 只能由唯一 Engine 内部产生。

差异只能发生在 Engine 之前和 Engine 之后，
不能发生在 Engine 策略核心内部。
```
