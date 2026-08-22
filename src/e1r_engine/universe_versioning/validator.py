"""Hard-gate validation for normalized membership events."""

from dataclasses import replace
from datetime import date, datetime
from typing import Iterable, List, Set

from .contracts import EventStatus, MembershipEvent
from .identity import IdentityRegistry


OFFICIAL_SOURCE_TYPES: Set[str] = {"SPDJI_INDEX_NEWS", "SPDJI_OFFICIAL_NOTICE", "SPDJI_PRO_FORMA"}
SP500_INDEX_IDS: Set[str] = {"SP500", "S&P 500", "SPX"}


def _valid_iso_datetime(value: str) -> bool:
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return bool(value)
    except ValueError:
        return False


def _valid_iso_date(value: str) -> bool:
    try:
        date.fromisoformat(value)
        return True
    except ValueError:
        return False


def validate_event(
    event: MembershipEvent,
    registry: IdentityRegistry,
    known_event_hashes: Iterable[str] = (),
) -> MembershipEvent:
    failures: List[str] = []
    rejected_scope = False
    if event.source_type not in OFFICIAL_SOURCE_TYPES or not event.source_url or not event.source_document_hash:
        failures.append("UNVERIFIED_OFFICIAL_SOURCE")
    if event.index_id not in SP500_INDEX_IDS:
        failures.append("REJECTED_SOURCE_SCOPE")
        rejected_scope = True
    if not _valid_iso_datetime(event.announcement_timestamp):
        failures.append("MISSING_OR_INVALID_ANNOUNCEMENT_TIMESTAMP")
    if not _valid_iso_date(event.effective_date) or not event.effective_time or not event.effective_timezone:
        failures.append("MISSING_OR_INVALID_EFFECTIVE_TIMESTAMP")
    if set(event.additions) & set(event.deletions):
        failures.append("ADDITION_DELETION_OVERLAP")
    if event.event_hash in set(known_event_hashes):
        failures.append("DUPLICATE_EVENT")
    for symbol in event.additions:
        try:
            registry.require_verified(symbol)
        except ValueError:
            failures.append("IDENTITY_OR_MAPPING_HOLD:" + symbol)
        prep = [item for item in event.price_preparation_results if item.get("engine_symbol") == symbol]
        if not prep or any(item.get("status") != "PASS" for item in prep):
            failures.append("PRICE_PREPARATION_HOLD:" + symbol)
    if failures:
        status = EventStatus.REJECTED_SOURCE_SCOPE if rejected_scope else EventStatus.HOLD
        return replace(event, event_status=status, failure_codes=sorted(set(failures)))
    return replace(event, event_status=EventStatus.AUTO_VERIFIED, failure_codes=[])
