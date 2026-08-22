"""Parse normalized official-source payloads without network access."""

from typing import Any, Dict, Iterable, List

from .contracts import EventStatus, MembershipEvent
from .hashing import content_hash


def _symbols(values: Iterable[Any]) -> List[str]:
    return sorted(set(str(value).strip().upper() for value in values if str(value).strip()))


def parse_membership_event(payload: Dict[str, Any]) -> MembershipEvent:
    additions = _symbols(payload.get("additions", []))
    deletions = _symbols(payload.get("deletions", []))
    stable_basis = {
        "index_id": payload.get("index_id"),
        "source_document_hash": payload.get("source_document_hash"),
        "effective_date": payload.get("effective_date"),
        "additions": additions,
        "deletions": deletions,
    }
    event_id = payload.get("event_id") or ("SP500-" + content_hash(stable_basis)[:20])
    status = payload.get("event_status", EventStatus.DETECTED.value)
    return MembershipEvent(
        event_id=str(event_id),
        revision=int(payload.get("revision", 1)),
        index_id=str(payload.get("index_id", "")),
        source_type=str(payload.get("source_type", "")),
        source_url=str(payload.get("source_url", "")),
        source_document_hash=str(payload.get("source_document_hash", "")),
        announcement_timestamp=str(payload.get("announcement_timestamp", "")),
        effective_date=str(payload.get("effective_date", "")),
        effective_time=str(payload.get("effective_time", "")),
        effective_timezone=str(payload.get("effective_timezone", "")),
        additions=additions,
        deletions=deletions,
        identity_mapping_results=list(payload.get("identity_mapping_results", [])),
        price_preparation_results=list(payload.get("price_preparation_results", [])),
        event_status=EventStatus(status),
        supersedes_event_id=payload.get("supersedes_event_id"),
        detected_at=payload.get("detected_at"),
        validated_at=payload.get("validated_at"),
        applied_at=payload.get("applied_at"),
        failure_codes=list(payload.get("failure_codes", [])),
    )
