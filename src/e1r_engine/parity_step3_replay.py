"""Read-only, causally bounded Parity-step-3 replay helpers."""

from __future__ import annotations

from datetime import date
import hashlib
import json
from pathlib import Path
import shutil
from typing import Any, Iterable, Mapping


PROTECTED_LIVE_PATHS = (
    "contracts/live_runtime_contract.json",
    "runtime/current/runtime_state.json",
    "runtime/history/transactions.jsonl",
    "runtime/history/cash_control.jsonl",
    "runtime/history/ledger_journal.jsonl",
)
PARITY_FIELDS = (
    "regime",
    "regime_subclass",
    "market_state",
    "market_gate",
    "entry_capacity",
    "strategy_branch",
)
FORBIDDEN_STOCK_SYMBOLS = frozenset({"QQQ", "SOXX", "VIXY"})


class ParityStep3Error(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ParityStep3Error(f"expected JSON object: {path}")
    return payload


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not Path(path).is_file():
        return []
    rows: list[dict[str, Any]] = []
    for number, line in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        row = json.loads(line)
        if not isinstance(row, dict):
            raise ParityStep3Error(f"JSONL row is not object: {path}:{number}")
        rows.append(row)
    return rows


def _row_effective_date(row: Mapping[str, Any]) -> date:
    raw = row.get("trade_date", row.get("effective_date"))
    if raw is None and isinstance(row.get("event"), Mapping):
        event = row["event"]
        raw = event.get("trade_date", event.get("effective_date"))
    if raw is None:
        raise ParityStep3Error("ledger row has no causal date")
    return date.fromisoformat(str(raw))


def causal_rows(rows: Iterable[Mapping[str, Any]], as_of: date) -> list[dict[str, Any]]:
    return [dict(row) for row in rows if _row_effective_date(row) <= as_of]


def _write_jsonl(path: Path, rows: Iterable[Mapping[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = "".join(json.dumps(dict(row), sort_keys=True, separators=(",", ":")) + "\n" for row in rows)
    path.write_text(body, encoding="utf-8")


def build_causal_live_projection(source_live: Path, target_live: Path, as_of: date) -> dict[str, int]:
    """Create a disposable Live root containing facts known by ``as_of``."""
    source_live, target_live = Path(source_live), Path(target_live)
    if target_live.name != "live":
        raise ParityStep3Error("causal projection root must be named live")
    for relative in ("contracts/live_runtime_contract.json", "runtime/current/runtime_state.json"):
        source = source_live / relative
        if not source.is_file():
            raise ParityStep3Error(f"missing Live authority file: {relative}")
        destination = target_live / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    tx = causal_rows(load_jsonl(source_live / "runtime/history/transactions.jsonl"), as_of)
    cash = causal_rows(load_jsonl(source_live / "runtime/history/cash_control.jsonl"), as_of)
    journal = causal_rows(load_jsonl(source_live / "runtime/history/ledger_journal.jsonl"), as_of)
    for sequence, row in enumerate(journal, 1):
        row["sequence"] = sequence
    _write_jsonl(target_live / "runtime/history/transactions.jsonl", tx)
    _write_jsonl(target_live / "runtime/history/cash_control.jsonl", cash)
    _write_jsonl(target_live / "runtime/history/ledger_journal.jsonl", journal)
    return {"transactions": len(tx), "cash_controls": len(cash), "journal_events": len(journal)}


def protected_hashes(live_root: Path) -> dict[str, str]:
    result: dict[str, str] = {}
    for relative in PROTECTED_LIVE_PATHS:
        path = Path(live_root) / relative
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else "MISSING"
    return result


def normalize_forward(trace: Mapping[str, Any]) -> dict[str, Any]:
    inputs = trace.get("inputs", {})
    return {
        "regime": trace.get("market_regime"),
        "regime_subclass": trace.get("metadata", {}).get("route", {}).get("subclass"),
        "market_state": inputs.get("market_state"),
        "market_gate": inputs.get("gate_state"),
        "entry_capacity": inputs.get("entry_capacity"),
        "strategy_branch": trace.get("branch"),
        "reference_top3": [row.get("symbol") for row in trace.get("metadata", {}).get("reference_top3", [])],
    }


def normalize_live(payload: Mapping[str, Any]) -> dict[str, Any]:
    return {
        **{field: payload.get(field) for field in PARITY_FIELDS},
        "reference_top3": [row.get("symbol") for row in payload.get("reference_top3", [])],
    }


def compare_contract(live: Mapping[str, Any], forward: Mapping[str, Any]) -> dict[str, Any]:
    # Forward and Live have isolated accounts.  Their holdings can therefore
    # legitimately remove different names from each account's reference Top3.
    # Only the account-independent contract is a parity gate.
    fields = PARITY_FIELDS
    mismatches = {field: {"live": live.get(field), "forward": forward.get(field)} for field in fields if live.get(field) != forward.get(field)}
    return {
        "decision": "PASS" if not mismatches else "FAIL",
        "mismatches": mismatches,
        "reference_top3_diagnostic": {
            "live": live.get("reference_top3"),
            "forward": forward.get("reference_top3"),
            "equal": live.get("reference_top3") == forward.get("reference_top3"),
            "parity_gating": False,
        },
    }


def validate_actions(payload: Mapping[str, Any]) -> list[str]:
    errors: list[str] = []
    for row in payload.get("position_recommendations", []):
        action = row.get("action")
        if action not in {"BUY", "ADD", "HOLD", "REDUCE", "EXIT"}:
            errors.append(f"unsupported action: {action}")
        if action == "REDUCE" and row.get("target_shares") is not None:
            errors.append(f"REDUCE must not carry target_shares: {row.get('symbol')}")
    return errors


def validate_forward_execution(payload: Mapping[str, Any]) -> list[str]:
    """Reject silent T+1 execution loss in the Forward authority.

    Step-3 previously compared decision fields only, so it could pass while
    executable BUY orders were discarded before fills were produced.
    """
    errors: list[str] = []
    for row in payload.get("skipped_orders", []):
        reason = str(row.get("skip_reason") or row.get("reason") or "")
        if reason == "MISSING_T1_BAR":
            errors.append(
                "Forward T+1 bar missing: "
                f"{row.get('symbol')} signal={row.get('signal_date')}"
            )
    return errors
