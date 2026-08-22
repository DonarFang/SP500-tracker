import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from e1r_engine.universe_versioning.contracts import EventStatus
from e1r_engine.universe_versioning.event_parser import parse_membership_event
from e1r_engine.universe_versioning.identity import IdentityRegistry
from e1r_engine.universe_versioning.validator import validate_event


def payload(**changes):
    value = {
        "index_id": "SP500", "source_type": "SPDJI_INDEX_NEWS",
        "source_url": "https://www.spglobal.com/spdji/notice", "source_document_hash": "a" * 64,
        "announcement_timestamp": "2026-08-10T12:00:00-04:00", "effective_date": "2026-08-17",
        "effective_time": "09:30:00", "effective_timezone": "America/New_York",
        "additions": [], "deletions": ["OLD"],
    }
    value.update(changes)
    return value


class ContractTests(unittest.TestCase):
    def check_hold(self, **changes):
        result = validate_event(parse_membership_event(payload(**changes)), IdentityRegistry())
        self.assertEqual(result.event_status, EventStatus.HOLD)

    def test_C01_missing_announcement(self): self.check_hold(announcement_timestamp="")
    def test_C02_missing_effective_fields(self): self.check_hold(effective_timezone="")
    def test_C03_overlap(self): self.check_hold(additions=["X"], deletions=["X"])
    def test_C04_wrong_index(self):
        result = validate_event(parse_membership_event(payload(index_id="SP500_ESG")), IdentityRegistry())
        self.assertEqual(result.event_status, EventStatus.REJECTED_SOURCE_SCOPE)
    def test_C05_deterministic_duplicate_identity(self):
        self.assertEqual(parse_membership_event(payload()).event_id, parse_membership_event(payload()).event_id)
    def test_C06_superseding_revision_preserved(self):
        event = parse_membership_event(payload(revision=2, supersedes_event_id="old"))
        self.assertEqual((event.revision, event.supersedes_event_id), (2, "old"))
    def test_C07_asymmetric_changes_allowed(self):
        result = validate_event(parse_membership_event(payload(additions=[], deletions=["A", "B"])), IdentityRegistry())
        self.assertEqual(result.event_status, EventStatus.AUTO_VERIFIED)
    def test_C08_member_count_not_hardcoded(self):
        result = validate_event(parse_membership_event(payload()), IdentityRegistry())
        self.assertEqual(result.event_status, EventStatus.AUTO_VERIFIED)


if __name__ == "__main__": unittest.main()
