# CURRENT PROJECT STATE

```text
STATUS: CANONICAL ENTRY POINTER
PROJECT: SP500趋势跟踪分析及交易辅助系统
ENGINE: FD-M3180125-SP500-TOP3-engine
```

唯一当前入口：

```text
docs/canonical/FD-M3180125_ENGINE_CANONICAL_CURRENT_STATE.md
```

启动顺序：

```text
1. 读取 CURRENT_PROJECT_STATE.md
2. 读取 Canonical Current State
3. 读取最近 3 天 Daily Log
4. 仅在发生问题时读取相关 RCA
5. 核对 HEAD / origin/main / working tree
6. 区分 FACT / INFERENCE / UNKNOWN
7. 再提出下一步
```

历史文件地位：

```text
Daily Logs / RCA / Handoffs / Superseded Architecture
= HISTORICAL / AUDIT ONLY
```

它们不得覆盖 Canonical Current State。

冲突规则：

```text
若当前源码、确切 HEAD 与 Canonical Current State 冲突：
STOP
只读取证
不得猜测
不得修改
明确报告冲突
等待用户批准
```
