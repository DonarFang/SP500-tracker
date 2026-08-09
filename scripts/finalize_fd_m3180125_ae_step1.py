#!/usr/bin/env python3
"""Finalize the Canonical record after an accepted AE-step 1 rebuild."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import tempfile
from typing import Any


ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
VARIANT_ID = "E1R_CAPPED_ATR_A0_V1"
DISPLAY_NAME = "E1R CAPPED-ATR Engine"
PASS_DECISION = (
    "PASS_AE_STEP_1_CAPPED_ATR_OFFICIAL_BACKTEST_ARTIFACT_EXPORT"
)
BEGIN_MARKER = "<!-- AE_STEP1_CAPPED_ATR_BEGIN -->"
END_MARKER = "<!-- AE_STEP1_CAPPED_ATR_END -->"


def read_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object: {path}")
    return value


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def write_atomic(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=path.parent,
        prefix=f".{path.name}.",
        delete=False,
    ) as stream:
        stream.write(text)
        stream.flush()
        os.fsync(stream.fileno())
        temporary = Path(stream.name)
    temporary.replace(path)


def build_record(
    *,
    generated_at: str,
    source_commit: str,
    result_sha: str,
    manifest_sha: str,
    result: dict[str, Any],
) -> str:
    metrics = {
        key: result[key]
        for key in (
            "final_equity",
            "total_return_pct",
            "cagr_pct",
            "max_drawdown_pct",
            "sharpe_ratio",
            "profit_factor",
            "number_of_trades",
            "exposure_pct",
        )
    }
    return f"""# FD-M3180125 — AE-step 1 CAPPED-ATR Migration Record

```text
STATUS: PASS
OFFICIAL_STEP: AE-step 1
ENGINE_ID: {ENGINE_ID}
VARIANT_ID: {VARIANT_ID}
DISPLAY_NAME: {DISPLAY_NAME}
GENERATED_AT: {generated_at}
SOURCE_COMMIT: {source_commit}
```

## Promoted stop contract

```text
A0 = first BUY cost-adjusted execution price
ATR20 = simple mean of the last 20 complete True Range observations as of first-entry signal day T EOD
distance = clip(3 * ATR20, 12% * A0, 20% * A0)
trigger = A0 - distance
signal = T close <= trigger
execution = T+1 original adverse low fill
A0 / ATR20 / distance / trigger remain frozen for the position cycle
ADD does not update stop state
regime change does not reset stop state
full exit clears stop state
same-symbol re-entry on stop execution day remains allowed
```

## Accepted Canonical 5Y metrics

```json
{json.dumps(metrics, indent=2, ensure_ascii=False)}
```

## Integrity

```text
Canonical result SHA256: {result_sha}
Official manifest SHA256: {manifest_sha}
CAPPED-ATR trigger rows: {len(result.get('capped_atr_stop_trace', []))}
Executed HARD_LOSS_STOP exits: {result.get('executed_exit_reason_distribution', {}).get('HARD_LOSS_STOP')}
```

## Scope boundary

```text
Forward changed: false
Live changed: false
Workflow changed: false
Dashboard changed: false
Next official step: AE-step 2 (not started by AE-step 1)
```
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()

    repo = args.repo.resolve()
    result_path = repo / "exports/e1r_unified_5y_full_account_v1_result.json"
    official_dir = (
        repo
        / "exports/official/FD-M3180125-SP500-TOP3-engine"
        / "backtest/canonical_5y"
    )
    decision_path = official_dir / "STEP1_OFFICIAL_EXPORT_DECISION.json"
    manifest_path = official_dir / "current_manifest.json"
    result = read_json(result_path)
    decision = read_json(decision_path)

    checks = {
        "engine_id": result.get("engine_id") == ENGINE_ID,
        "variant_id": result.get("strategy_variant") == VARIANT_ID,
        "display_name": result.get("strategy_display_name") == DISPLAY_NAME,
        "official_decision": decision.get("decision") == PASS_DECISION,
        "source_commit": (
            decision.get("canonical_strategy_commit") == args.source_commit
        ),
        "source_sha": decision.get("source_result_sha256") == sha256(result_path),
        "metrics": (
            result.get("final_equity") == 312687.26
            and result.get("total_return_pct") == 212.69
            and result.get("cagr_pct") == 25.59
            and result.get("max_drawdown_pct") == 25.66
            and result.get("sharpe_ratio") == 0.76
            and result.get("profit_factor") == 2.36
            and result.get("number_of_trades") == 92
            and result.get("exposure_pct") == 69.2
        ),
        "stop_trace": len(result.get("capped_atr_stop_trace", [])) == 8,
        "hard_stop_exits": (
            result.get("executed_exit_reason_distribution", {}).get(
                "HARD_LOSS_STOP"
            )
            == 3
        ),
        "sample_valid": result.get("sample_validity", {}).get("is_valid") is True,
        "p0": result.get("p0_passed") is True,
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError("AE-step 1 finalization checks failed: " + ",".join(failed))

    generated_at = datetime.now(timezone.utc).isoformat()
    record = build_record(
        generated_at=generated_at,
        source_commit=args.source_commit,
        result_sha=sha256(result_path),
        manifest_sha=sha256(manifest_path),
        result=result,
    )
    record_path = (
        repo
        / "docs/canonical/FD-M3180125_AE_STEP1_CAPPED_ATR_MIGRATION_RECORD.md"
    )
    write_atomic(record_path, record)

    current_state_path = (
        repo / "docs/canonical/FD-M3180125_ENGINE_CANONICAL_CURRENT_STATE.md"
    )
    current = current_state_path.read_text(encoding="utf-8")
    section = (
        BEGIN_MARKER
        + "\n\n"
        + "## AE-step 1 — CAPPED-ATR production migration (latest authority)\n\n"
        + "The former V00 stop/result section below is historical. The current "
        + f"formal variant is `{VARIANT_ID}` (`{DISPLAY_NAME}`).\n\n"
        + f"- Source commit: `{args.source_commit}`\n"
        + f"- Canonical result SHA256: `{sha256(result_path)}`\n"
        + "- Final equity: `312687.26`\n"
        + "- Return / CAGR / MaxDD: `212.69% / 25.59% / 25.66%`\n"
        + "- Sharpe / PF / Trades / Exposure: `0.76 / 2.36 / 92 / 69.2%`\n"
        + "- Forward / Live / Workflow / Dashboard: unchanged in AE-step 1\n"
        + "- Full record: `docs/canonical/FD-M3180125_AE_STEP1_CAPPED_ATR_MIGRATION_RECORD.md`\n\n"
        + END_MARKER
    )
    if BEGIN_MARKER in current and END_MARKER in current:
        start = current.index(BEGIN_MARKER)
        end = current.index(END_MARKER, start) + len(END_MARKER)
        current = current[:start] + section + current[end:]
    else:
        current = current.rstrip() + "\n\n" + section + "\n"
    write_atomic(current_state_path, current)

    print(
        json.dumps(
            {
                "decision": "PASS_AE_STEP_1_CANONICAL_FINALIZATION",
                "record": str(record_path.relative_to(repo)),
                "current_state": str(current_state_path.relative_to(repo)),
                "checks": checks,
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
