import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from e1r_engine.universe_versioning.contracts import EventStatus, MembershipEvent
from e1r_engine.universe_versioning.resolver import MembershipResolver, execution_allows_risk_increase


def snapshot():
    event = MembershipEvent("E", 1, "SP500", "SPDJI_INDEX_NEWS", "u", "h", "2026-08-11T00:00:00Z", "2026-08-12", "09:30", "America/New_York", [], ["OLD"], event_status=EventStatus.AUTO_VERIFIED)
    return MembershipResolver("live", "2026-08-10T00:00:00Z").resolve("2026-08-12", "B", ["OLD", "KEEP"], [event])


class HoldingTests(unittest.TestCase):
    def test_H01_deleted_no_holding_blocks_buy(self): self.assertFalse(execution_allows_risk_increase(snapshot(), "OLD", "BUY"))
    def test_H02_deleted_holding_can_reduce(self): self.assertTrue(execution_allows_risk_increase(snapshot(), "OLD", "REDUCE"))
    def test_H03_liquidated_symbol_not_required_by_membership(self): self.assertNotIn("OLD", snapshot().effective_membership)
    def test_H04_deleted_top3_cannot_add(self): self.assertFalse(execution_allows_risk_increase(snapshot(), "OLD", "ADD"))
    def test_H05_membership_drop_does_not_force_exit(self): self.assertTrue(execution_allows_risk_increase(snapshot(), "OLD", "HOLD"))


if __name__ == "__main__": unittest.main()
