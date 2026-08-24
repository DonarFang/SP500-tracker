"""SA-step-3: verified-source to track-isolated UV Membership Events."""

from __future__ import annotations

from datetime import date, datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile
from typing import Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from e1r_engine.universe_versioning.contracts import EventStatus, MembershipEvent
from e1r_engine.universe_versioning.hashing import canonical_json_bytes, content_hash
from e1r_engine.universe_versioning.resolver import MembershipResolver
from e1r_engine.universe_versioning.storage import TrackStorage


class EventPublicationError(RuntimeError):
    pass


def _sha(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _plain(path: Path) -> None:
    cursor = path
    while cursor != cursor.parent:
        if cursor.exists() and cursor.is_symlink():
            raise EventPublicationError("SYMLINK_PATH_REJECTED:" + str(cursor))
        cursor = cursor.parent
    if path.exists() and (not path.is_file() or path.stat().st_nlink != 1):
        raise EventPublicationError("UNSAFE_FILE_REJECTED:" + str(path))


def _atomic(path: Path, payload: Any, immutable: bool = False) -> None:
    _plain(path)
    body = canonical_json_bytes(payload) + b"\n"
    if immutable and path.exists():
        if path.read_bytes() == body:
            return
        raise EventPublicationError("IMMUTABLE_CONFLICT:" + str(path))
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".sa3-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(body)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, str(path))
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _valid_rows(rows: Sequence[Mapping[str, Any]], minimum: int = 252) -> List[Dict[str, Any]]:
    normalized: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        try:
            trading_date = date.fromisoformat(str(row.get("date", ""))[:10]).isoformat()
            values = {name: float(row.get(name)) for name in ("open", "high", "low", "close")}
            volume = float(row.get("volume", 0.0))
        except (TypeError, ValueError):
            continue
        if any(not math.isfinite(value) or value <= 0 for value in values.values()):
            continue
        if not math.isfinite(volume) or volume < 0:
            continue
        normalized[trading_date] = dict({"date": trading_date}, **values, volume=volume)
    result = [normalized[key] for key in sorted(normalized)]
    if len(result) < minimum:
        raise EventPublicationError("PRICE_HISTORY_INSUFFICIENT:%d" % len(result))
    return result


def _resolve_track_snapshot(
    repo_root: Path,
    track: str,
    execution_date: str,
    extra_events: Sequence[MembershipEvent] = (),
):
    storage = TrackStorage(Path(repo_root), track)
    baseline_path = storage.export_root / "baseline" / "PRODUCTION_BASELINE.json"
    _plain(baseline_path)
    if not baseline_path.is_file():
        raise EventPublicationError("PRODUCTION_BASELINE_MISSING:" + track)
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    members = baseline.get("symbols")
    baseline_id = str(baseline.get("snapshot_id", ""))
    if not isinstance(members, list) or not members or not baseline_id:
        raise EventPublicationError("PRODUCTION_BASELINE_INVALID:" + track)
    reconciliation_path = (
        storage.data_root / "pre_activation_reconciliations.json"
    )
    if reconciliation_path.is_file():
        _plain(reconciliation_path)
        correction = json.loads(
            reconciliation_path.read_text(encoding="utf-8")
        )
        recorded_hash = correction.pop("content_hash", None)
        if (
            correction.get("track") != track
            or correction.get("status")
            != "CANONICAL_PRE_ACTIVATION_RECONCILIATION"
            or recorded_hash != content_hash(correction)
        ):
            raise EventPublicationError(
                "PRE_ACTIVATION_RECONCILIATION_INVALID:" + track
            )
        reconciled = set(str(symbol).upper() for symbol in members)
        applied_corrections = []
        for row in correction.get("reconciliations", []):
            outgoing = str(row.get("outgoing", "")).upper()
            incoming = str(row.get("incoming", "")).upper()
            effective_date = str(row.get("effective_date", ""))
            if not outgoing or not incoming or outgoing == incoming:
                raise EventPublicationError(
                    "PRE_ACTIVATION_RECONCILIATION_ROW_INVALID:" + track
                )
            try:
                is_effective = (
                    date.fromisoformat(effective_date)
                    <= date.fromisoformat(execution_date)
                )
            except ValueError as exc:
                raise EventPublicationError(
                    "PRE_ACTIVATION_RECONCILIATION_DATE_INVALID:" + track
                ) from exc
            if is_effective:
                reconciled.discard(outgoing)
                reconciled.add(incoming)
                applied_corrections.append(
                    outgoing + "->" + incoming + "@" + effective_date
                )
        members = sorted(reconciled)
        if applied_corrections:
            baseline_id += "+PRE-" + str(recorded_hash)[:16]
    from e1r_engine.universe_versioning.event_parser import parse_membership_event
    events = [parse_membership_event(value) for value in storage.load_events()]
    events.extend(extra_events)
    return MembershipResolver(track, "2026-08-10T00:00:00Z").resolve(
        execution_date, baseline_id, members, events,
    )


def refresh_track_snapshot(repo_root: Path, track: str, execution_date: str):
    storage = TrackStorage(Path(repo_root), track)
    snapshot = _resolve_track_snapshot(repo_root, track, execution_date)
    storage.publish_snapshot(snapshot)
    return snapshot


class VerifiedEventPublisher:
    def __init__(
        self,
        repo_root: Path,
        price_provider: Callable[[str], Sequence[Mapping[str, Any]]],
        now: Optional[Callable[[], datetime]] = None,
    ) -> None:
        self.root = Path(repo_root).resolve()
        self.price_provider = price_provider
        self.now = now or (lambda: datetime.now(timezone.utc))

    def _authority(self) -> Tuple[Dict[str, Any], Dict[str, Any], Path]:
        current = self.root / "data/sp500_source_monitor/state/current.json"
        scan = json.loads(current.read_text(encoding="utf-8"))
        source_ids = scan.get("source_ids")
        if scan.get("status") != "PASS_SOURCE_SCAN" or not isinstance(source_ids, list) or len(source_ids) != 1:
            raise EventPublicationError("SOURCE_SCAN_AUTHORITY_INVALID")
        source_id = str(source_ids[0])
        detection_path = self.root / "data/sp500_source_monitor/detections" / source_id / "detection.json"
        detection = json.loads(detection_path.read_text(encoding="utf-8"))
        raw_path = self.root / "data/sp500_source_monitor" / str(detection.get("raw_document_path", ""))
        _plain(raw_path)
        if not raw_path.is_file() or _sha(raw_path.read_bytes()) != detection.get("source_document_sha256"):
            raise EventPublicationError("RAW_SOURCE_AUTHORITY_INVALID")
        accepted = []
        for path in sorted((self.root / "data/sp500_source_verification/verifications" / source_id).glob("SA2-*.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            if value.get("status") == "VERIFIED_NO_EVENT" and value.get("manual_intervention_required") is False:
                accepted.append(value)
        if not accepted:
            raise EventPublicationError("NO_ACCEPTED_VERIFICATION")

        verification_current_path = self.root / "data/sp500_source_verification/state/current.json"
        _plain(verification_current_path)
        if not verification_current_path.is_file():
            raise EventPublicationError("VERIFICATION_CURRENT_MISSING")
        verification_current = json.loads(verification_current_path.read_text(encoding="utf-8"))
        if (
            verification_current.get("status") != "VERIFIED_NO_EVENT"
            or verification_current.get("source_id") != source_id
            or verification_current.get("manual_intervention_required") is not False
        ):
            raise EventPublicationError("VERIFICATION_CURRENT_NOT_ACCEPTED")

        def semantic(value: Mapping[str, Any]) -> bytes:
            rows = []
            for row in value.get("entries", []):
                identity = row.get("identity", {})
                rows.append({
                    "action": row.get("action"), "company_name": row.get("company_name"),
                    "spdj_symbol": identity.get("spdj_symbol"),
                    "engine_symbol": identity.get("engine_symbol"),
                    "yahoo_symbol": identity.get("yahoo_symbol"),
                    "status": row.get("status"), "mapping_status": identity.get("status"),
                })
            return canonical_json_bytes({
                "source_id": value.get("source_id"), "effective_date": value.get("effective_date"),
                "provider": value.get("provider"), "provider_mapping_sha256": value.get("provider_mapping_sha256"),
                "entries": rows,
            })

        basis = semantic(accepted[0])
        if any(semantic(value) != basis for value in accepted[1:]):
            raise EventPublicationError("CONFLICTING_ACCEPTED_VERIFICATIONS")
        authority = min(accepted, key=lambda value: (str(value.get("verified_at_utc", "")), str(value.get("verification_id", ""))))
        if (
            semantic(verification_current) != basis
            or verification_current.get("verification_id") != authority.get("verification_id")
        ):
            raise EventPublicationError("VERIFICATION_CURRENT_AUTHORITY_MISMATCH")
        return detection, authority, raw_path

    def publish(self) -> Dict[str, Any]:
        detection, verification, raw_path = self._authority()
        entries = verification.get("entries", [])
        additions = sorted(row["identity"]["engine_symbol"] for row in entries if row.get("action") == "ADD")
        deletions = sorted(row["identity"]["engine_symbol"] for row in entries if row.get("action") == "REMOVE")
        if not additions or not deletions or set(additions) & set(deletions):
            raise EventPublicationError("MEMBERSHIP_CHANGE_INVALID")

        stable = {
            "index_id": "SP500", "source_document_hash": detection["source_document_sha256"],
            "effective_date": verification["effective_date"], "additions": additions, "deletions": deletions,
        }
        event_id = "SP500-" + content_hash(stable)[:20]
        audit_path = self.root / "data/sp500_source_events/events" / event_id / "publication.json"
        if audit_path.is_file():
            _plain(audit_path)
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            if (
                audit.get("status") != "PASS_SA_STEP_3_EVENT_PUBLISHED"
                or audit.get("event_id") != event_id
                or audit.get("source_id") != detection.get("source_id")
            ):
                raise EventPublicationError("EXISTING_PUBLICATION_CONFLICT")
            for key in ("forward_event_path", "live_event_path"):
                path = self.root / str(audit.get(key, ""))
                _plain(path)
                if not path.is_file():
                    raise EventPublicationError("EXISTING_PUBLICATION_INCOMPLETE")
            _atomic(self.root / "data/sp500_source_events/state/current.json", audit)
            return audit

        prepared: Dict[str, List[Dict[str, Any]]] = {}
        prep_results = []
        identities = []
        by_engine = {row["identity"]["engine_symbol"]: row for row in entries}
        for symbol in additions:
            row = by_engine[symbol]
            identity = row["identity"]
            yahoo = str(identity.get("yahoo_symbol", ""))
            if not yahoo or identity.get("status") != "VERIFIED":
                raise EventPublicationError("YAHOO_MAPPING_NOT_VERIFIED:" + symbol)
            prices = _valid_rows(self.price_provider(yahoo))
            prepared[symbol] = prices
            evidence_hash = _sha(canonical_json_bytes(prices))
            prep_results.append({
                "security_id": "SPDJI:" + symbol,
                "engine_symbol": symbol, "provider_symbol": yahoo,
                "status": "PASS", "evidence_hash": evidence_hash,
                "history_start": prices[0]["date"], "history_end": prices[-1]["date"],
                "row_count": len(prices), "failure_codes": [],
            })
        for row in entries:
            identity = row["identity"]
            engine = str(identity["engine_symbol"])
            identities.append({
                "security_id": "SPDJI:" + engine,
                "spdj_symbol": str(identity["spdj_symbol"]),
                "engine_symbol": engine,
                "yahoo_symbol": str(identity["yahoo_symbol"]),
                "exchange": str(identity.get("exchange") or "YAHOO_CONFIRMED"),
                "asset_type": "COMMON_STOCK", "share_class": str(identity.get("share_class") or ""),
                "currency": str(identity.get("currency") or "USD"),
                "mapping_effective_from": verification["effective_date"],
                "mapping_effective_to": None, "mapping_status": "VERIFIED",
                "mapping_evidence_hash": str(identity.get("price_evidence_sha256") or verification["provider_mapping_sha256"]),
            })

        announcement = parsedate_to_datetime(str(detection["published_text"])).astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        event = MembershipEvent(
            event_id=event_id, revision=1, index_id="SP500", source_type="SPDJI_INDEX_NEWS",
            source_url=detection["source_url"], source_document_hash=detection["source_document_sha256"],
            announcement_timestamp=announcement, effective_date=verification["effective_date"],
            effective_time="09:30:00", effective_timezone="America/New_York",
            additions=additions, deletions=deletions, identity_mapping_results=identities,
            price_preparation_results=prep_results, event_status=EventStatus.AUTO_VERIFIED,
            detected_at=detection.get("detected_at_utc"), validated_at=verification.get("verified_at_utc"),
        )

        snapshots = [
            _resolve_track_snapshot(self.root, track, verification["effective_date"], (event,))
            for track in ("forward", "live")
        ]
        event_paths = [
            TrackStorage(self.root, track).data_root / "events" / event.event_id / "revision-001.json"
            for track in ("forward", "live")
        ]
        snapshot_paths = [
            TrackStorage(self.root, track).data_root / "snapshots" / (snapshot.snapshot_id + ".json")
            for track, snapshot in zip(("forward", "live"), snapshots)
        ]
        pointer_paths = [
            TrackStorage(self.root, track).data_root / "state" / "current.json"
            for track in ("forward", "live")
        ]
        audit = {
            "status": "PASS_SA_STEP_3_EVENT_PUBLISHED",
            "event_id": event.event_id, "event_hash": event.event_hash,
            "source_id": detection["source_id"], "verification_id": verification["verification_id"],
            "effective_date": event.effective_date, "additions": additions, "deletions": deletions,
            "forward_event_path": str(event_paths[0].relative_to(self.root)),
            "live_event_path": str(event_paths[1].relative_to(self.root)),
            "forward_snapshot_id": snapshots[0].snapshot_id,
            "live_snapshot_id": snapshots[1].snapshot_id,
            "price_symbols_written": additions, "production_run_performed": False,
            "broker_call_performed": False, "strategy_modified": False,
        }
        current_audit_path = self.root / "data/sp500_source_events/state/current.json"
        transaction_paths = list(event_paths) + list(snapshot_paths) + list(pointer_paths) + [audit_path, current_audit_path]
        for track_root in ("fw_prices", "live_prices"):
            transaction_paths.extend(self.root / "data" / track_root / (symbol + ".json") for symbol in prepared)
        backups: Dict[Path, Optional[bytes]] = {}
        for target in transaction_paths:
            _plain(target)
            backups[target] = target.read_bytes() if target.exists() else None
        try:
            for track_root in ("fw_prices", "live_prices"):
                for symbol, prices in prepared.items():
                    target = self.root / "data" / track_root / (symbol + ".json")
                    _atomic(target, prices)
            for track, snapshot in zip(("forward", "live"), snapshots):
                storage = TrackStorage(self.root, track)
                storage.append_event(event)
                storage.publish_snapshot(snapshot)
            _atomic(audit_path, audit, immutable=True)
            _atomic(current_audit_path, audit)
        except Exception:
            for target, body in reversed(list(backups.items())):
                if body is None and target.exists():
                    target.unlink()
                elif body is not None:
                    target.write_bytes(body)
            raise
        return audit
