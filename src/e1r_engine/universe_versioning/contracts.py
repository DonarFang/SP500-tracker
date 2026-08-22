"""Frozen UV v1.0 data contracts (Python 3.9 compatible)."""

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .hashing import content_hash


class EventStatus(str, Enum):
    DETECTED = "DETECTED"
    STAGED = "STAGED"
    AUTO_VERIFIED = "AUTO_VERIFIED"
    SCHEDULED = "SCHEDULED"
    EFFECTIVE = "EFFECTIVE"
    HOLD = "HOLD"
    ENTRY_QUARANTINE = "ENTRY_QUARANTINE"
    REJECTED_SOURCE_SCOPE = "REJECTED_SOURCE_SCOPE"


class MappingStatus(str, Enum):
    VERIFIED = "VERIFIED"
    HOLD = "HOLD"


@dataclass(frozen=True)
class SecurityIdentity:
    security_id: str
    spdj_symbol: str
    engine_symbol: str
    yahoo_symbol: str
    exchange: str
    asset_type: str = "COMMON_STOCK"
    share_class: str = ""
    currency: str = "USD"
    issuer_id: Optional[str] = None
    mapping_effective_from: Optional[str] = None
    mapping_effective_to: Optional[str] = None
    mapping_status: MappingStatus = MappingStatus.VERIFIED
    mapping_evidence_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["mapping_status"] = self.mapping_status.value
        return value


@dataclass(frozen=True)
class PricePreparationResult:
    security_id: str
    engine_symbol: str
    provider_symbol: str
    status: str
    evidence_hash: str
    history_start: Optional[str] = None
    history_end: Optional[str] = None
    row_count: int = 0
    failure_codes: List[str] = field(default_factory=list)


@dataclass(frozen=True)
class MembershipEvent:
    event_id: str
    revision: int
    index_id: str
    source_type: str
    source_url: str
    source_document_hash: str
    announcement_timestamp: str
    effective_date: str
    effective_time: str
    effective_timezone: str
    additions: List[str]
    deletions: List[str]
    identity_mapping_results: List[Dict[str, Any]] = field(default_factory=list)
    price_preparation_results: List[Dict[str, Any]] = field(default_factory=list)
    event_status: EventStatus = EventStatus.DETECTED
    supersedes_event_id: Optional[str] = None
    detected_at: Optional[str] = None
    validated_at: Optional[str] = None
    applied_at: Optional[str] = None
    failure_codes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["event_status"] = self.event_status.value
        value["additions"] = sorted(set(self.additions))
        value["deletions"] = sorted(set(self.deletions))
        return value

    @property
    def event_hash(self) -> str:
        return content_hash(self.to_dict())


@dataclass(frozen=True)
class MembershipSnapshot:
    track: str
    snapshot_id: str
    as_of_execution_date: str
    effective_membership: List[str]
    source_event_ids: List[str]
    baseline_snapshot_id: str
    status: str = "EFFECTIVE"

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["effective_membership"] = sorted(set(self.effective_membership))
        value["source_event_ids"] = sorted(set(self.source_event_ids))
        value["content_hash"] = self.content_hash
        return value

    @property
    def content_hash(self) -> str:
        value = asdict(self)
        value["effective_membership"] = sorted(set(self.effective_membership))
        value["source_event_ids"] = sorted(set(self.source_event_ids))
        return content_hash(value)
