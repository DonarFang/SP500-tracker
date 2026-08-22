import sys
import unittest
from dataclasses import replace
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from e1r_engine.universe_versioning.contracts import EventStatus, MembershipEvent
from e1r_engine.universe_versioning.resolver import MembershipResolver, daily_eligible_entry_universe


def event(effective="2026-08-17", announcement="2026-08-14T12:00:00-04:00", status=EventStatus.AUTO_VERIFIED):
    return MembershipEvent("E", 1, "SP500", "SPDJI_INDEX_NEWS", "u", "h", announcement, effective, "09:30:00", "America/New_York", ["NEW"], ["OLD"], event_status=status)


class EventTimeTests(unittest.TestCase):
    def resolve(self, execution, item): return MembershipResolver("forward", "2026-08-10T00:00:00Z").resolve(execution, "B", ["OLD"], [item])
    def test_T01_friday_notice_monday_effective(self): self.assertEqual(self.resolve("2026-08-17", event()).effective_membership, ["NEW"])
    def test_T02_late_notice_does_not_change_prior_snapshot(self): self.assertEqual(self.resolve("2026-08-14", event()).effective_membership, ["OLD"])
    def test_T03_unwarmed_addition_not_eligible(self): self.assertEqual(daily_eligible_entry_universe(self.resolve("2026-08-17", event()), ["OLD"]), [])
    def test_T04_deleted_pending_buy_blocked(self): self.assertNotIn("OLD", self.resolve("2026-08-17", event()).effective_membership)
    def test_T05_deleted_pending_add_blocked(self): self.assertNotIn("OLD", self.resolve("2026-08-17", event()).effective_membership)
    def test_T06_catchup_resolves_each_date(self):
        self.assertNotEqual(self.resolve("2026-08-14", event()).content_hash, self.resolve("2026-08-17", event()).content_hash)
    def test_T07_holiday_date_is_runtime_supplied(self): self.assertEqual(self.resolve("2026-07-06", event(effective="2026-07-06")).as_of_execution_date, "2026-07-06")
    def test_T08_late_discovery_does_not_rewrite_history(self): self.assertEqual(self.resolve("2026-08-16", event()).effective_membership, ["OLD"])
    def test_T09_pre_activation_notice_future_effective(self):
        item = event(announcement="2026-08-09T12:00:00Z")
        self.assertEqual(self.resolve("2026-08-17", item).effective_membership, ["NEW"])
    def test_T10_pre_activation_effect_is_audit_only(self):
        item = event(effective="2026-08-09", announcement="2026-08-08T12:00:00Z")
        self.assertEqual(self.resolve("2026-08-17", item).effective_membership, ["OLD"])


if __name__ == "__main__": unittest.main()
