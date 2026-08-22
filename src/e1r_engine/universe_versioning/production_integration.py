"""UV-step-4 production Universe gate and controlled activation.

This module owns only Membership eligibility and BUY/ADD risk-increase
enforcement.  It does not implement strategy, ranking, sizing, exits, account,
execution, price updating, event acquisition, Workflow, Dashboard, or 5Y logic.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from datetime import datetime, timezone
import json
from pathlib import Path
import stat
from typing import Any, Dict, Iterable, Mapping, Sequence, Tuple

from .contracts import MembershipSnapshot
from .event_parser import parse_membership_event
from .hashing import content_hash, symbol_list_hash
from .resolver import MembershipResolver, daily_eligible_entry_universe
from .storage import TrackStorage


ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
MODES = {"OFF", "ENFORCE"}
TRACK_STEMS = {"forward": "fw", "live": "live"}
UV_ACTIVATION_TIME = "2026-08-10T00:00:00Z"


class ProductionUniverseError(RuntimeError):
    def __init__(self, track: str, message: str) -> None:
        decision = "HOLD_UV_STEP_4_" + track.upper() + "_PRODUCTION"
        super().__init__(decision + ": " + message)
        self.track = track
        self.decision = decision


def _symbols(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(sorted(set(str(x).strip().upper() for x in values if str(x).strip())))


def _assert_plain_file(path: Path, repo_root: Path, track: str) -> None:
    cursor = path
    while True:
        try:
            mode = cursor.lstat().st_mode
        except FileNotFoundError:
            mode = None
        if mode is not None and stat.S_ISLNK(mode):
            raise ProductionUniverseError(track, "symlink path rejected: " + str(cursor))
        if cursor == repo_root:
            break
        if cursor.parent == cursor:
            raise ProductionUniverseError(track, "path escaped repository")
        cursor = cursor.parent
    if path.is_file() and path.stat().st_nlink != 1:
        raise ProductionUniverseError(track, "hardlink file rejected: " + str(path))


@dataclass(frozen=True)
class ProductionUniverseDecision:
    track: str
    mode: str
    expected_execution_date: str
    snapshot_id: str
    snapshot_hash: str
    effective_membership: Tuple[str, ...]
    eligible_buy_universe: Tuple[str, ...]
    required_data_universe: Tuple[str, ...]
    blocked_risk_increases: Tuple[Dict[str, str], ...]
    evidence_hash: str

    def allows_risk_increase(self, symbol: str, action: str) -> bool:
        if str(action).upper() not in {"BUY", "ADD"}:
            return True
        return str(symbol).upper() in set(self.eligible_buy_universe)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "track": self.track,
            "mode": self.mode,
            "expected_execution_date": self.expected_execution_date,
            "snapshot_id": self.snapshot_id,
            "snapshot_hash": self.snapshot_hash,
            "effective_membership": list(self.effective_membership),
            "eligible_buy_universe": list(self.eligible_buy_universe),
            "required_data_universe": list(self.required_data_universe),
            "blocked_risk_increases": list(self.blocked_risk_increases),
            "evidence_hash": self.evidence_hash,
        }


class ProductionUniverseGate:
    def __init__(self, repo_root: Path, track: str) -> None:
        root = Path(repo_root).resolve()
        if track not in TRACK_STEMS:
            raise ProductionUniverseError(track, "track must be forward or live")
        self.repo_root = root
        self.track = track
        self.storage = TrackStorage(root, track)
        self.mode_path = self.storage.data_root / "production" / "mode.json"

    def mode(self) -> str:
        _assert_plain_file(self.mode_path, self.repo_root, self.track)
        if not self.mode_path.exists():
            return "OFF"
        payload = json.loads(self.mode_path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict) or payload.get("track") != self.track:
            raise ProductionUniverseError(self.track, "invalid production mode payload")
        recorded_hash = payload.pop("content_hash", None)
        if recorded_hash != content_hash(payload):
            raise ProductionUniverseError(self.track, "production mode content hash mismatch")
        mode = str(payload.get("mode", ""))
        if mode not in MODES:
            raise ProductionUniverseError(self.track, "invalid production mode")
        return mode

    def _load_snapshot(self) -> MembershipSnapshot:
        pointer_path = self.storage.data_root / "state" / "current.json"
        if not pointer_path.is_file():
            raise ProductionUniverseError(self.track, "current pointer is missing")
        _assert_plain_file(pointer_path, self.repo_root, self.track)
        pointer = json.loads(pointer_path.read_text(encoding="utf-8"))
        snapshot_id = str(pointer.get("snapshot_id", ""))
        snapshot_path = self.storage.data_root / "snapshots" / (snapshot_id + ".json")
        if not snapshot_id or not snapshot_path.is_file():
            raise ProductionUniverseError(self.track, "current snapshot is missing")
        _assert_plain_file(snapshot_path, self.repo_root, self.track)
        raw = json.loads(snapshot_path.read_text(encoding="utf-8"))
        snapshot = MembershipSnapshot(
            track=str(raw.get("track", "")),
            snapshot_id=str(raw.get("snapshot_id", "")),
            as_of_execution_date=str(raw.get("as_of_execution_date", "")),
            effective_membership=list(raw.get("effective_membership", [])),
            source_event_ids=list(raw.get("source_event_ids", [])),
            baseline_snapshot_id=str(raw.get("baseline_snapshot_id", "")),
            status=str(raw.get("status", "")),
        )
        if snapshot.track != self.track or snapshot.status != "EFFECTIVE":
            raise ProductionUniverseError(self.track, "snapshot track/status mismatch")
        if raw.get("content_hash") != snapshot.content_hash:
            raise ProductionUniverseError(self.track, "snapshot content hash mismatch")
        if pointer.get("content_hash") != snapshot.content_hash:
            raise ProductionUniverseError(self.track, "pointer content hash mismatch")
        return snapshot

    def refresh_snapshot(self, expected_execution_date: str) -> MembershipSnapshot:
        """Resolve and publish the track-local snapshot for the exact run date."""
        from e1r_engine.source_automation.event_publication import refresh_track_snapshot
        try:
            return refresh_track_snapshot(self.repo_root, self.track, expected_execution_date)
        except Exception as exc:
            if isinstance(exc, ProductionUniverseError):
                raise
            raise ProductionUniverseError(self.track, "snapshot refresh failed: " + str(exc)) from exc

    def _assert_event_completeness(self, snapshot: MembershipSnapshot, execution_date: str) -> None:
        included = set(snapshot.source_event_ids)
        for raw in self.storage.load_events():
            event = parse_membership_event(raw)
            if event.event_status.value not in {"AUTO_VERIFIED", "SCHEDULED", "EFFECTIVE"}:
                continue
            if (
                event.announcement_timestamp < UV_ACTIVATION_TIME
                and event.effective_date < UV_ACTIVATION_TIME[:10]
            ):
                continue
            if date.fromisoformat(event.effective_date) <= date.fromisoformat(execution_date):
                token = event.event_id + "@r" + str(event.revision)
                if token not in included:
                    raise ProductionUniverseError(self.track, "current snapshot omits effective event " + token)

    def resolve(
        self,
        *,
        expected_execution_date: str,
        production_catalogue: Iterable[str],
        production_eligible: Iterable[str],
        holdings_symbols: Iterable[str],
        data_ready_symbols: Iterable[str],
        required_indices: Iterable[str],
        candidate_actions: Sequence[Mapping[str, Any]] = (),
    ) -> ProductionUniverseDecision:
        try:
            date.fromisoformat(expected_execution_date)
        except ValueError as exc:
            raise ProductionUniverseError(self.track, "invalid expected_execution_date") from exc
        mode = self.mode()
        catalogue = _symbols(production_catalogue)
        production_daily = _symbols(production_eligible)
        holdings = _symbols(holdings_symbols)
        ready = _symbols(data_ready_symbols)
        indices = _symbols(required_indices)
        if not catalogue:
            raise ProductionUniverseError(self.track, "production catalogue is empty")
        if mode == "OFF":
            membership = catalogue
            eligible = production_daily
            snapshot_id = "PRODUCTION-MODE-OFF"
            snapshot_hash = symbol_list_hash(membership)
        else:
            snapshot = self.refresh_snapshot(expected_execution_date)
            if date.fromisoformat(snapshot.as_of_execution_date) > date.fromisoformat(expected_execution_date):
                raise ProductionUniverseError(self.track, "snapshot is from the future")
            self._assert_event_completeness(snapshot, expected_execution_date)
            membership = _symbols(snapshot.effective_membership)
            eligible = tuple(daily_eligible_entry_universe(snapshot, ready))
            snapshot_id = snapshot.snapshot_id
            snapshot_hash = snapshot.content_hash
        required = _symbols(tuple(eligible) + holdings + indices)
        missing_holdings = sorted(set(holdings) - set(ready))
        if mode == "ENFORCE" and missing_holdings:
            raise ProductionUniverseError(self.track, "held symbols are not data-ready: " + ",".join(missing_holdings))
        blocked = []
        for raw in candidate_actions:
            symbol = str(raw.get("symbol", "")).strip().upper()
            action = str(raw.get("action", raw.get("intent_type", ""))).strip().upper()
            if symbol and action in {"BUY", "ADD"} and symbol not in set(eligible):
                blocked.append({"symbol": symbol, "action": action})
        basis = {
            "track": self.track, "mode": mode, "date": expected_execution_date,
            "snapshot_id": snapshot_id, "snapshot_hash": snapshot_hash,
            "membership": membership, "eligible": eligible, "required": required,
            "blocked": blocked,
        }
        return ProductionUniverseDecision(
            track=self.track, mode=mode, expected_execution_date=expected_execution_date,
            snapshot_id=snapshot_id, snapshot_hash=snapshot_hash,
            effective_membership=membership, eligible_buy_universe=eligible,
            required_data_universe=required, blocked_risk_increases=tuple(blocked),
            evidence_hash=content_hash(basis),
        )

    def activate(
        self,
        *,
        expected_execution_date: str,
        baseline_membership: Iterable[str],
        authority_head: str,
        contract_hash: str,
    ) -> ProductionUniverseDecision:
        catalogue = _symbols(baseline_membership)
        if not catalogue:
            raise ProductionUniverseError(self.track, "activation baseline is empty")
        baseline_path = self.storage.export_root / "baseline" / "PRODUCTION_BASELINE.json"
        if baseline_path.is_file():
            _assert_plain_file(baseline_path, self.repo_root, self.track)
            baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
            members = _symbols(baseline.get("symbols", ()))
            if (
                baseline.get("track") != self.track
                or baseline.get("status") != "PRODUCTION_BASELINE"
                or baseline.get("content_hash") != symbol_list_hash(members)
            ):
                raise ProductionUniverseError(self.track, "invalid preserved production baseline")
            baseline_id = str(baseline.get("snapshot_id", ""))
        else:
            members = catalogue
            baseline_id = self.track.upper() + "-PRODUCTION-BASELINE-" + symbol_list_hash(members)[:16]
            baseline = {
                "track": self.track, "snapshot_id": baseline_id,
                "status": "PRODUCTION_BASELINE", "symbols": list(members),
                "symbol_count": len(members), "content_hash": symbol_list_hash(members),
                "authority_head": authority_head, "contract_hash": contract_hash,
            }
            self.storage.atomic_write(baseline_path, baseline, immutable=True)
        events = [parse_membership_event(raw) for raw in self.storage.load_events()]
        snapshot = MembershipResolver(self.track, UV_ACTIVATION_TIME).resolve(
            expected_execution_date, baseline_id, members, events,
        )
        self.storage.publish_snapshot(snapshot)
        mode_payload = {
            "track": self.track, "mode": "ENFORCE", "authority_head": authority_head,
            "contract_hash": contract_hash, "snapshot_id": snapshot.snapshot_id,
            "snapshot_hash": snapshot.content_hash, "activation_time": UV_ACTIVATION_TIME,
        }
        self._publish_mode_change(mode_payload)
        return self.resolve(
            expected_execution_date=expected_execution_date,
            production_catalogue=catalogue, production_eligible=catalogue,
            holdings_symbols=(), data_ready_symbols=catalogue, required_indices=(),
        )

    def deactivate(self, *, authority_head: str, contract_hash: str) -> None:
        self._publish_mode_change({
            "track": self.track, "mode": "OFF", "authority_head": authority_head,
            "contract_hash": contract_hash,
        })

    def _publish_mode_change(self, payload: Mapping[str, Any]) -> None:
        basis = dict(payload)
        basis["recorded_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        evidence_hash = content_hash(basis)
        evidence = dict(basis)
        evidence["content_hash"] = evidence_hash
        evidence_path = (
            self.storage.export_root / "production" / "mode_changes" /
            (evidence_hash + ".json")
        )
        self.storage.atomic_write(evidence_path, evidence, immutable=True)
        pointer = dict(payload)
        pointer["evidence_hash"] = evidence_hash
        pointer["content_hash"] = content_hash(pointer)
        self.storage.atomic_write(self.mode_path, pointer)


__all__ = [
    "ProductionUniverseDecision", "ProductionUniverseError", "ProductionUniverseGate",
]
