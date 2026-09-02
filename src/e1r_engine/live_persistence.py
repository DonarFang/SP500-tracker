"""Append-only persistence for the independent Personal Live Track."""

from __future__ import annotations

from dataclasses import asdict, dataclass, is_dataclass
from datetime import date, datetime, timezone
from decimal import Decimal
from enum import Enum
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Mapping, Optional

from .live_ledger import CashControlEvent, LiveLedger, TransactionEvent


class LivePersistenceError(ValueError):
    pass


def _jsonable(value: Any) -> Any:
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, (date, datetime)):
        return value.isoformat()
    if isinstance(value, Enum):
        return value.value
    if is_dataclass(value):
        return _jsonable(asdict(value))
    if isinstance(value, Mapping):
        return {str(key): _jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(item) for item in value]
    return value


def canonical_json(payload: Mapping[str, Any]) -> bytes:
    return (
        json.dumps(
            _jsonable(dict(payload)),
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
        )
        + "\n"
    ).encode("utf-8")


def _compact_json(payload: Mapping[str, Any]) -> str:
    return json.dumps(
        _jsonable(dict(payload)),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )


def sha256_bytes(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def atomic_write(path: Path, body: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(body)
    os.replace(temporary, path)


@dataclass(frozen=True)
class LiveRuntimePaths:
    root: Path

    @property
    def contracts(self) -> Path:
        return self.root / "contracts"

    @property
    def current(self) -> Path:
        return self.root / "runtime" / "current"

    @property
    def daily(self) -> Path:
        return self.root / "runtime" / "daily"

    @property
    def history(self) -> Path:
        return self.root / "runtime" / "history"

    @property
    def automation(self) -> Path:
        return self.root / "automation"


class LiveRuntimeRepository:
    EXPECTED_ROOT_NAME = "live"

    def __init__(self, root: Path) -> None:
        self.paths = LiveRuntimePaths(Path(root))
        if self.paths.root.name != self.EXPECTED_ROOT_NAME:
            raise LivePersistenceError("Live runtime root must be named live")

    @property
    def transaction_path(self) -> Path:
        return self.paths.history / "transactions.jsonl"

    @property
    def cash_control_path(self) -> Path:
        return self.paths.history / "cash_control.jsonl"

    @property
    def journal_path(self) -> Path:
        return self.paths.history / "ledger_journal.jsonl"

    def initialize_unactivated(self, *, opening_cash: str = "100000.00") -> None:
        self.write_once(
            self.paths.contracts / "live_runtime_contract.json",
            {
                "engine": "FD-M3180125-SP500-TOP3-engine",
                "mode": "PERSONAL_LIVE",
                "status": "UNACTIVATED",
                "opening_date": None,
                "opening_cash": opening_cash,
                "positions": {},
                "record_type": "USER_DECLARED_OPENING_CASH",
                "shared_with_other_modes": "ENGINE_CODE_ONLY",
                "five_year_data_shared": False,
                "engine_forward_data_shared": False,
            },
        )
        self.write_once(
            self.paths.current / "runtime_state.json",
            {
                "status": "UNACTIVATED",
                "opening_date": None,
                "last_committed_market_date": None,
                "last_successful_run_at": None,
                "activation_required": True,
            },
        )

    def write_once(self, path: Path, payload: Mapping[str, Any]) -> str:
        body = canonical_json(payload)
        digest = sha256_bytes(body)
        if path.exists():
            if path.read_bytes() == body:
                return digest
            raise LivePersistenceError(f"conflicting immutable write: {path}")
        atomic_write(path, body)
        return digest

    def replace_current(self, name: str, payload: Mapping[str, Any]) -> str:
        path = self.paths.current / name
        body = canonical_json(payload)
        atomic_write(path, body)
        return sha256_bytes(body)

    def _load_jsonl(self, path: Path) -> list[dict[str, Any]]:
        if not path.exists():
            return []
        rows = []
        for line_number, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise LivePersistenceError(
                    f"invalid JSONL at {path}:{line_number}"
                ) from exc
            if not isinstance(row, dict):
                raise LivePersistenceError(
                    f"JSONL row must be object: {path}:{line_number}"
                )
            rows.append(row)
        return rows

    def _append_line(self, path: Path, payload: Mapping[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as stream:
            stream.write(_compact_json(payload) + "\n")

    def _find_event(self, event_id: str) -> Optional[dict[str, Any]]:
        for row in self._load_jsonl(self.journal_path):
            if row.get("event_id") == event_id:
                return row
        return None

    def _append_event(
        self,
        *,
        ledger_name: str,
        event_payload: Mapping[str, Any],
        projection_path: Path,
        audit_payload: Optional[Mapping[str, Any]] = None,
    ) -> str:
        event_id = str(event_payload["event_id"])
        fingerprint = hashlib.sha256(
            _compact_json(event_payload).encode("utf-8")
        ).hexdigest()

        existing = self._find_event(event_id)
        if existing is not None:
            if existing.get("event_fingerprint") == fingerprint:
                return fingerprint
            raise LivePersistenceError(f"conflicting event_id: {event_id}")

        sequence = len(self._load_jsonl(self.journal_path)) + 1

        projection = dict(audit_payload or event_payload)
        projection["record_hash"] = hashlib.sha256(
            _compact_json(projection).encode("utf-8")
        ).hexdigest()

        journal = {
            "sequence": sequence,
            "ledger": ledger_name,
            "event_id": event_id,
            "event_fingerprint": fingerprint,
            "event": dict(event_payload),
        }
        journal["record_hash"] = hashlib.sha256(
            _compact_json(journal).encode("utf-8")
        ).hexdigest()

        self._append_line(self.journal_path, journal)
        self._append_line(projection_path, projection)
        return fingerprint

    def append_transaction(
        self,
        event: TransactionEvent,
        *,
        audit_payload: Optional[Mapping[str, Any]] = None,
    ) -> str:
        return self._append_event(
            ledger_name="TRANSACTION",
            event_payload=event.canonical_payload(),
            projection_path=self.transaction_path,
            audit_payload=audit_payload,
        )

    def append_cash_control(
        self,
        event: CashControlEvent,
        *,
        cash_before: Decimal | int | float | str,
        created_at: Optional[datetime] = None,
    ) -> str:
        before = Decimal(str(cash_before))
        after = event.actual_cash
        created = created_at or datetime.now(timezone.utc)
        if created.tzinfo is None:
            raise LivePersistenceError("created_at must be timezone-aware")

        return self._append_event(
            ledger_name="CASH_CONTROL",
            event_payload=event.canonical_payload(),
            projection_path=self.cash_control_path,
            audit_payload={
                "event_type": "CASH_CONTROL",
                "cash_adjustment_id": event.event_id,
                "event_id": event.event_id,
                "effective_date": event.effective_date,
                "created_at": created,
                "cash_before": before,
                "cash_after": after,
                "cash_delta": after - before,
                "actual_cash": after,
                "source": "USER_CONFIRMED_CASH",
                "notes": event.notes,
            },
        )

    def load_ledger(self) -> LiveLedger:
        ledger = LiveLedger()
        expected_sequence = 1

        for row in self._load_jsonl(self.journal_path):
            if row.get("sequence") != expected_sequence:
                raise LivePersistenceError(
                    "ledger journal sequence is not contiguous"
                )
            expected_sequence += 1

            ledger_name = row.get("ledger")
            payload = row.get("event")
            if not isinstance(payload, dict):
                raise LivePersistenceError("journal event must be object")

            event_type = payload.get("event_type")
            clean = {
                key: value
                for key, value in payload.items()
                if key != "event_type"
            }

            if ledger_name == "TRANSACTION":
                if event_type != "TRANSACTION":
                    raise LivePersistenceError("transaction type mismatch")
                for field_name in (
                    "trade_date",
                    "signal_date",
                    "expected_execution_date",
                ):
                    if clean.get(field_name) is not None:
                        clean[field_name] = date.fromisoformat(
                            str(clean[field_name])
                        )
                ledger.append_transaction(TransactionEvent(**clean))
            elif ledger_name == "CASH_CONTROL":
                if event_type != "CASH_CONTROL":
                    raise LivePersistenceError("cash-control type mismatch")
                clean["effective_date"] = date.fromisoformat(
                    str(clean["effective_date"])
                )
                ledger.append_cash_control(CashControlEvent(**clean))
            else:
                raise LivePersistenceError(
                    f"unsupported ledger name: {ledger_name}"
                )

        return ledger

    def commit_daily(
        self,
        *,
        market_date: str,
        artifacts: Mapping[str, Mapping[str, Any]],
    ) -> dict[str, str]:
        target = self.paths.daily / market_date
        manifest_hashes: dict[str, str] = {}

        for name, payload in sorted(artifacts.items()):
            filename = name if name.endswith(".json") else f"{name}.json"
            manifest_hashes[filename] = self.write_once(
                target / filename,
                payload,
            )

        manifest_hashes["manifest.json"] = self.write_once(
            target / "manifest.json",
            {
                "market_date": market_date,
                "files": manifest_hashes,
                "validation_status": "PASS",
            },
        )
        return manifest_hashes

    def append_history(
        self,
        name: str,
        payload: Mapping[str, Any],
        *,
        event_id: str,
    ) -> str:
        filename = name if name.endswith(".jsonl") else f"{name}.jsonl"
        path = self.paths.history / filename
        normalized = dict(payload)
        normalized["event_id"] = event_id
        digest = hashlib.sha256(
            _compact_json(normalized).encode("utf-8")
        ).hexdigest()
        normalized["record_hash"] = digest

        for row in self._load_jsonl(path):
            if row.get("event_id") == event_id:
                if row == normalized:
                    return digest
                raise LivePersistenceError(
                    f"conflicting history event_id: {event_id}"
                )

        self._append_line(path, normalized)
        return digest

    def update_automation(
        self,
        name: str,
        payload: Mapping[str, Any],
    ) -> str:
        filename = name if name.endswith(".json") else f"{name}.json"
        body = canonical_json(payload)
        atomic_write(self.paths.automation / filename, body)
        return sha256_bytes(body)
