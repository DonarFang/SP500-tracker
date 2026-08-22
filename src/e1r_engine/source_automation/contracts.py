"""Frozen SA-step-1 contracts, compatible with Python 3.9."""

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class CandidateChange:
    action: str
    company_name: str
    official_symbol: str
    replaced_company_name: str = ""
    replaced_official_symbol: str = ""
    effective_date_text: str = ""
    effective_timing_text: str = ""
    evidence_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class SourceDetection:
    source_id: str
    source_url: str
    source_document_sha256: str
    fetched_at_utc: str
    published_text: str
    title: str
    content_type: str
    parser_version: str
    status: str
    candidates: List[CandidateChange] = field(default_factory=list)
    failure_codes: List[str] = field(default_factory=list)
    raw_document_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        value = asdict(self)
        value["candidates"] = [candidate.to_dict() for candidate in self.candidates]
        return value
