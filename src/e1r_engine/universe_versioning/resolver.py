"""Resolve membership only for a Runtime-supplied execution date."""

from datetime import date
from typing import Iterable, List, Set

from .contracts import EventStatus, MembershipEvent, MembershipSnapshot
from .hashing import content_hash


class MembershipResolutionError(ValueError):
    pass


class MembershipResolver:
    def __init__(self, track: str, activation_time: str) -> None:
        if track not in {"forward", "live"}:
            raise MembershipResolutionError("track must be explicitly forward or live")
        self.track = track
        self.activation_time = activation_time

    def resolve(
        self,
        expected_execution_date: str,
        baseline_snapshot_id: str,
        baseline_membership: Iterable[str],
        events: Iterable[MembershipEvent],
    ) -> MembershipSnapshot:
        if not expected_execution_date:
            raise MembershipResolutionError("Runtime-supplied expected_execution_date is required")
        try:
            execution_date = date.fromisoformat(expected_execution_date)
        except ValueError as exc:
            raise MembershipResolutionError("invalid expected_execution_date") from exc
        members: Set[str] = set(str(item).upper() for item in baseline_membership)
        applied: List[str] = []
        ordered = sorted(events, key=lambda item: (item.effective_date, item.event_id, item.revision))
        for event in ordered:
            if event.event_status not in {EventStatus.AUTO_VERIFIED, EventStatus.SCHEDULED, EventStatus.EFFECTIVE}:
                continue
            if event.announcement_timestamp < self.activation_time and event.effective_date < self.activation_time[:10]:
                continue
            if date.fromisoformat(event.effective_date) > execution_date:
                continue
            members.difference_update(event.deletions)
            members.update(event.additions)
            applied.append(event.event_id + "@r" + str(event.revision))
        basis = {
            "track": self.track,
            "date": expected_execution_date,
            "members": sorted(members),
            "events": applied,
            "baseline": baseline_snapshot_id,
        }
        return MembershipSnapshot(
            track=self.track,
            snapshot_id=(self.track.upper() + "-" + expected_execution_date + "-" + content_hash(basis)[:16]),
            as_of_execution_date=expected_execution_date,
            effective_membership=sorted(members),
            source_event_ids=applied,
            baseline_snapshot_id=baseline_snapshot_id,
        )


def daily_eligible_entry_universe(
    snapshot: MembershipSnapshot,
    data_ready_symbols: Iterable[str],
    quarantined_symbols: Iterable[str] = (),
) -> List[str]:
    ready = set(item.upper() for item in data_ready_symbols)
    blocked = set(item.upper() for item in quarantined_symbols)
    return sorted(set(snapshot.effective_membership) & ready - blocked)


def execution_allows_risk_increase(snapshot: MembershipSnapshot, symbol: str, action: str) -> bool:
    if action not in {"BUY", "ADD"}:
        return True
    return symbol.upper() in set(snapshot.effective_membership)
