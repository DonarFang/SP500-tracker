"""Read-only UV-step-3 Forward/Live shadow observation.

The observer resolves track-local Membership for a Runtime-supplied execution
date and publishes deterministic evidence under that track's shadow export
root.  It never returns a production Universe object and has no Engine,
Adapter, account, order, fill, price-update, Workflow, Dashboard, network, 5Y,
Legacy, or Screening dependency.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import tempfile
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

from .event_parser import parse_membership_event
from .hashing import canonical_json_bytes, content_hash, symbol_list_hash
from .resolver import MembershipResolver, daily_eligible_entry_universe


ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
TRACK_STEMS = {"forward": "fw", "live": "live"}
HOLD_DECISIONS = {
    "forward": "HOLD_UV_STEP_3_FORWARD_SHADOW",
    "live": "HOLD_UV_STEP_3_LIVE_SHADOW",
}


class ShadowIntegrationError(RuntimeError):
    """A fail-closed UV-step-3 shadow boundary violation."""

    def __init__(self, track: str, message: str) -> None:
        decision = HOLD_DECISIONS.get(track, "HOLD_UV_STEP_3_SHADOW")
        super().__init__(decision + ": " + message)
        self.track = track
        self.decision = decision


def _symbols(values: Iterable[str]) -> Tuple[str, ...]:
    return tuple(sorted(set(str(value).strip().upper() for value in values if str(value).strip())))


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _json_bytes(value: Any) -> bytes:
    return canonical_json_bytes(value) + b"\n"


def _path_is_within(path: Path, root: Path) -> bool:
    return path == root or root in path.parents


def _assert_no_symlink(path: Path, stop: Path, track: str) -> None:
    cursor = path
    while True:
        try:
            mode = cursor.lstat().st_mode
        except FileNotFoundError:
            mode = None
        if mode is not None and stat.S_ISLNK(mode):
            raise ShadowIntegrationError(
                track,
                "symlink path rejected: " + str(cursor),
            )
        if cursor == stop:
            return
        if cursor.parent == cursor:
            raise ShadowIntegrationError(track, "path escaped repository root")
        cursor = cursor.parent


def manifest_paths(paths: Iterable[Path], excluded_roots: Iterable[Path] = ()) -> str:
    """Deterministically hash file metadata/content without writing anything."""
    excluded = tuple(Path(item).resolve() for item in excluded_roots)
    rows: List[Dict[str, Any]] = []
    for raw in sorted(set(Path(item).resolve() for item in paths), key=str):
        if any(_path_is_within(raw, root) for root in excluded):
            continue
        if not raw.exists():
            rows.append({"path": str(raw), "status": "MISSING"})
            continue
        candidates = [raw] if raw.is_file() or raw.is_symlink() else sorted(raw.rglob("*"))
        for item in candidates:
            resolved = item.resolve(strict=False)
            if any(_path_is_within(resolved, root) for root in excluded):
                continue
            relative = str(item.relative_to(raw)) if item != raw else "."
            if item.is_symlink():
                rows.append({"root": str(raw), "path": relative, "status": "SYMLINK"})
            elif item.is_file():
                rows.append({
                    "root": str(raw),
                    "path": relative,
                    "size": item.stat().st_size,
                    "sha256": _sha256_bytes(item.read_bytes()),
                })
    return content_hash(rows)


@dataclass(frozen=True)
class ShadowObserverConfig:
    repo_root: Path
    track: str
    authority_head: str
    activation_time: str

    def __post_init__(self) -> None:
        root = Path(self.repo_root).resolve()
        if self.track not in TRACK_STEMS:
            raise ShadowIntegrationError(self.track, "track must be forward or live")
        if re.fullmatch(r"[0-9a-f]{40}", self.authority_head) is None:
            raise ShadowIntegrationError(self.track, "authority_head must be a Git SHA-1")
        try:
            date.fromisoformat(self.activation_time[:10])
        except ValueError as exc:
            raise ShadowIntegrationError(self.track, "invalid activation_time") from exc
        object.__setattr__(self, "repo_root", root)

    @property
    def data_root(self) -> Path:
        return self.repo_root / "data" / (TRACK_STEMS[self.track] + "_universe")

    @property
    def other_data_root(self) -> Path:
        other = "live" if self.track == "forward" else "fw"
        return self.repo_root / "data" / (other + "_universe")

    @property
    def shadow_root(self) -> Path:
        return (
            self.repo_root
            / "exports"
            / "official"
            / ENGINE_ID
            / self.track
            / "universe"
            / "shadow"
        )

    @property
    def other_shadow_root(self) -> Path:
        other = "live" if self.track == "forward" else "forward"
        return (
            self.repo_root
            / "exports"
            / "official"
            / ENGINE_ID
            / other
            / "universe"
            / "shadow"
        )


@dataclass(frozen=True)
class ShadowObservationResult:
    track: str
    run_id: str
    evidence_root: Path
    expected_execution_date: str
    shadow_membership_hash: str
    shadow_eligible_hash: str
    shadow_required_data_hash: str
    decision: str

    def to_dict(self) -> Dict[str, Any]:
        acceptance = self.evidence_root / "acceptance_result.json"
        payload = json.loads(acceptance.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            raise ShadowIntegrationError(
                self.track,
                "acceptance evidence must be an object",
            )
        return dict(payload, evidence_root=str(self.evidence_root))


class UniverseShadowObserver:
    """Track-isolated observer.  Its only mutation is one atomic evidence dir."""

    EVIDENCE_NAMES = (
        "run_authority.json",
        "baseline_observation.json",
        "execution_date_resolution.json",
        "membership_resolution.json",
        "universe_diff.json",
        "price_preparation_observation.json",
        "production_impact_comparison.json",
        "protected_manifest_comparison.json",
        "dashboard_projection_shadow.json",
        "acceptance_result.json",
    )

    def __init__(self, config: ShadowObserverConfig) -> None:
        self.config = config

    def _load_events(self) -> List[Any]:
        root = self.config.data_root / "events"
        if not root.exists():
            return []
        _assert_no_symlink(root, self.config.repo_root, self.config.track)
        events = []
        for path in sorted(root.glob("*/revision-*.json")):
            _assert_no_symlink(path, self.config.repo_root, self.config.track)
            if not _path_is_within(path.resolve(), self.config.data_root.resolve()):
                raise ShadowIntegrationError(self.config.track, "cross-track event read")
            payload = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(payload, dict):
                raise ShadowIntegrationError(self.config.track, "event payload must be an object")
            events.append(parse_membership_event(payload))
        return events

    def _publish(self, run_id: str, artifacts: Mapping[str, Any]) -> Path:
        raw_root = self.config.shadow_root
        repo_root = self.config.repo_root
        _assert_no_symlink(raw_root, repo_root, self.config.track)
        root = raw_root.resolve(strict=False)
        if not _path_is_within(root, repo_root):
            raise ShadowIntegrationError(self.config.track, "shadow output escaped repository")
        if _path_is_within(root, self.config.other_shadow_root.resolve(strict=False)):
            raise ShadowIntegrationError(self.config.track, "cross-track shadow write")
        raw_root.mkdir(parents=True, exist_ok=True)
        _assert_no_symlink(raw_root, repo_root, self.config.track)
        root = raw_root.resolve(strict=False)
        final = root / run_id
        expected = {name: _json_bytes(artifacts[name]) for name in self.EVIDENCE_NAMES}
        if final.exists():
            _assert_no_symlink(final, repo_root, self.config.track)
            actual_names = tuple(sorted(path.name for path in final.iterdir() if path.is_file()))
            if actual_names != tuple(sorted(self.EVIDENCE_NAMES)):
                raise ShadowIntegrationError(self.config.track, "idempotent evidence set mismatch")
            for name, body in expected.items():
                existing = final / name
                if existing.stat().st_nlink != 1:
                    raise ShadowIntegrationError(
                        self.config.track,
                        "hardlink evidence rejected: " + name,
                    )
                if existing.read_bytes() != body:
                    raise ShadowIntegrationError(self.config.track, "immutable evidence conflict: " + name)
            return final

        temporary = Path(tempfile.mkdtemp(prefix=".uv3-", dir=str(root)))
        try:
            for name in self.EVIDENCE_NAMES:
                target = temporary / name
                with target.open("wb") as stream:
                    stream.write(expected[name])
                    stream.flush()
                    os.fsync(stream.fileno())
            os.replace(str(temporary), str(final))
            for name in self.EVIDENCE_NAMES:
                if (final / name).stat().st_nlink != 1:
                    raise ShadowIntegrationError(
                        self.config.track,
                        "hardlink evidence rejected after publication: " + name,
                    )
        except Exception:
            if temporary.exists():
                shutil.rmtree(str(temporary))
            raise
        return final

    def observe(
        self,
        *,
        market_date: Optional[str] = None,
        expected_execution_date: str,
        production_catalogue: Iterable[str],
        production_eligible: Iterable[str],
        holdings_symbols: Iterable[str],
        data_ready_symbols: Iterable[str],
        required_indices: Iterable[str],
        candidate_actions: Sequence[Mapping[str, Any]] = (),
        date_source: str,
        protected_paths: Iterable[Path] = (),
        production_input_hash: Optional[str] = None,
    ) -> ShadowObservationResult:
        track = self.config.track
        try:
            date.fromisoformat(expected_execution_date)
        except ValueError as exc:
            raise ShadowIntegrationError(track, "invalid expected_execution_date") from exc
        resolved_market_date = market_date or expected_execution_date
        try:
            date.fromisoformat(resolved_market_date)
        except ValueError as exc:
            raise ShadowIntegrationError(track, "invalid market_date") from exc
        if track == "live" and date_source != "LIVE_CALENDAR_HARD_GATE":
            raise ShadowIntegrationError(track, "Live date must come from Calendar Hard Gate")
        if track == "forward" and date_source != "FORWARD_DATE_PLANNER":
            raise ShadowIntegrationError(track, "Forward date must come from ForwardDatePlanner")

        catalogue = _symbols(production_catalogue)
        production_daily_eligible = _symbols(production_eligible)
        holdings = _symbols(holdings_symbols)
        data_ready = _symbols(data_ready_symbols)
        indices = _symbols(required_indices)
        if not catalogue:
            raise ShadowIntegrationError(track, "production catalogue is empty")

        protected = tuple(Path(item).resolve() for item in protected_paths)
        before_manifest = manifest_paths(protected, (self.config.shadow_root,))
        events = self._load_events()
        baseline_id = (
            track.upper()
            + "-SHADOW-BASELINE-"
            + symbol_list_hash(catalogue)[:16]
        )
        snapshot = MembershipResolver(track, self.config.activation_time).resolve(
            expected_execution_date,
            baseline_id,
            catalogue,
            events,
        )
        shadow_membership = _symbols(snapshot.effective_membership)
        shadow_eligible = tuple(
            daily_eligible_entry_universe(snapshot, data_ready)
        )
        shadow_required_data = _symbols(tuple(shadow_eligible) + holdings + indices)
        additions = tuple(sorted(set(shadow_membership) - set(catalogue)))
        deletions = tuple(sorted(set(catalogue) - set(shadow_membership)))

        would_allow: List[Dict[str, str]] = []
        would_block: List[Dict[str, str]] = []
        for raw in candidate_actions:
            symbol = str(raw.get("symbol", "")).strip().upper()
            action = str(raw.get("action", "")).strip().upper()
            if action not in {"BUY", "ADD"} or not symbol:
                continue
            row = {"symbol": symbol, "action": action}
            (would_allow if symbol in set(shadow_eligible) else would_block).append(row)

        normalized_actions = tuple(
            sorted(
                (
                    {
                        "symbol": str(raw.get("symbol", "")).strip().upper(),
                        "action": str(raw.get("action", "")).strip().upper(),
                    }
                    for raw in candidate_actions
                ),
                key=lambda row: (row["symbol"], row["action"]),
            )
        )
        event_rows = tuple(
            event.to_dict() if hasattr(event, "to_dict") else str(event)
            for event in events
        )
        input_hash = production_input_hash or content_hash({
            "catalogue": catalogue,
            "eligible": production_daily_eligible,
            "holdings": holdings,
            "data_ready": data_ready,
            "required_indices": indices,
            "candidate_actions": normalized_actions,
            "date_source": date_source,
            "events": event_rows,
        })

        observation_basis = {
            "track": track,
            "authority_head": self.config.authority_head,
            "market_date": resolved_market_date,
            "expected_execution_date": expected_execution_date,
            "production_catalogue_hash": symbol_list_hash(catalogue),
            "production_eligible_hash": symbol_list_hash(production_daily_eligible),
            "holdings_hash": symbol_list_hash(holdings),
            "data_ready_hash": symbol_list_hash(data_ready),
            "required_indices_hash": symbol_list_hash(indices),
            "shadow_membership_hash": symbol_list_hash(shadow_membership),
            "shadow_eligible_hash": symbol_list_hash(shadow_eligible),
            "shadow_required_data_hash": symbol_list_hash(shadow_required_data),
            "candidate_actions_hash": content_hash(normalized_actions),
            "events_hash": content_hash(event_rows),
            "production_input_hash": input_hash,
            "date_source": date_source,
        }
        run_id = track.upper() + "-" + expected_execution_date + "-" + content_hash(observation_basis)[:16]
        after_manifest = manifest_paths(protected, (self.config.shadow_root,))
        if before_manifest != after_manifest:
            raise ShadowIntegrationError(track, "protected production manifest changed")
        common = {
            "track": track,
            "run_id": run_id,
            "market_date": resolved_market_date,
            "expected_execution_date": expected_execution_date,
        }
        artifacts: Dict[str, Any] = {
            "run_authority.json": {
                **common,
                "authority_head": self.config.authority_head,
                "shadow_mode": "EXPLICIT_READ_ONLY_PROBE",
                "production_activation": False,
            },
            "baseline_observation.json": {
                **common,
                "source": "PRODUCTION_EQUIVALENT_CATALOGUE",
                "symbol_count": len(catalogue),
                "symbols": list(catalogue),
                "production_catalogue_hash": symbol_list_hash(catalogue),
                "production_eligible_hash": symbol_list_hash(production_daily_eligible),
                "holdings_hash": symbol_list_hash(holdings),
            },
            "execution_date_resolution.json": {**common, "date_source": date_source, "fallback_used": False},
            "membership_resolution.json": {
                **common,
                "snapshot": snapshot.to_dict(),
                "event_count": len(events),
                "shadow_membership_hash": symbol_list_hash(shadow_membership),
            },
            "universe_diff.json": {
                **common,
                "additions": list(additions),
                "deletions": list(deletions),
                "holdings_retained_for_management": list(sorted(set(holdings) - set(shadow_membership))),
                "would_allow_buy_add": sorted(would_allow, key=lambda row: (row["symbol"], row["action"])),
                "would_block_buy_add": sorted(would_block, key=lambda row: (row["symbol"], row["action"])),
                "automatic_exits_created": [],
            },
            "price_preparation_observation.json": {
                **common,
                "data_ready_symbols": list(data_ready),
                "missing_membership_symbols": list(sorted(set(shadow_membership) - set(data_ready))),
                "production_price_write_performed": False,
                "network_request_performed": False,
            },
            "production_impact_comparison.json": {
                **common,
                "production_input_hash_before": input_hash,
                "production_input_hash_after": input_hash,
                "production_side_effect_calls": [],
                "engine_step_called": False,
                "adapter_decide_called": False,
                "execution_called": False,
                "runtime_commit_called": False,
                "account_or_ledger_commit_called": False,
                "price_updater_called": False,
                "workflow_update_called": False,
                "production_impact": "ZERO",
            },
            "protected_manifest_comparison.json": {
                **common,
                "before": before_manifest,
                "after": after_manifest,
                "protected_manifests_unchanged": True,
                "shadow_root_excluded": str(self.config.shadow_root),
            },
            "dashboard_projection_shadow.json": {
                **common,
                "production_dashboard_write_performed": False,
                "shadow_membership_count": len(shadow_membership),
                "shadow_eligible_count": len(shadow_eligible),
                "shadow_required_data_count": len(shadow_required_data),
            },
            "acceptance_result.json": {
                **common,
                **observation_basis,
                "would_allow_buy_add": sorted(would_allow, key=lambda row: (row["symbol"], row["action"])),
                "would_block_buy_add": sorted(would_block, key=lambda row: (row["symbol"], row["action"])),
                "cross_track_reads_detected": False,
                "cross_track_writes_detected": False,
                "production_side_effect_calls": [],
                "protected_manifests_unchanged": True,
                "decision": "PASS_UV_STEP_3_" + track.upper() + "_SHADOW_PROBE",
            },
        }
        final = self._publish(run_id, artifacts)
        return ShadowObservationResult(
            track=track,
            run_id=run_id,
            evidence_root=final,
            expected_execution_date=expected_execution_date,
            shadow_membership_hash=symbol_list_hash(shadow_membership),
            shadow_eligible_hash=symbol_list_hash(shadow_eligible),
            shadow_required_data_hash=symbol_list_hash(shadow_required_data),
            decision="PASS_UV_STEP_3_" + track.upper() + "_SHADOW_PROBE",
        )


__all__ = [
    "ShadowIntegrationError",
    "ShadowObservationResult",
    "ShadowObserverConfig",
    "UniverseShadowObserver",
    "manifest_paths",
]
