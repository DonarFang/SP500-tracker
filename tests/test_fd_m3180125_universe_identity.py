import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from e1r_engine.universe_versioning.contracts import MappingStatus, SecurityIdentity
from e1r_engine.universe_versioning.identity import IdentityConflict, IdentityRegistry, canonical_seed_identities


class IdentityTests(unittest.TestCase):
    def setUp(self): self.registry = IdentityRegistry(canonical_seed_identities())
    def test_M01_brkb(self): self.assertEqual(self.registry.require_verified("BRK.B").yahoo_symbol, "BRK-B")
    def test_M02_bfb(self): self.assertEqual(self.registry.require_verified("BF.B").yahoo_symbol, "BF-B")
    def test_M03_spx(self): self.assertEqual(self.registry.require_verified("SPX").yahoo_symbol, "^GSPC")
    def test_M04_etf_cannot_replace_index(self):
        with self.assertRaises(IdentityConflict):
            IdentityRegistry([SecurityIdentity("I", "SPX", "SPX", "SPY", "ARCA", asset_type="ETF")])
    def test_M05_same_name_different_exchange_is_not_guessed(self):
        self.assertIsNone(self.registry.get_by_engine_symbol("AMBIG"))
    def test_M06_ticker_revision_same_security(self):
        reg = IdentityRegistry([SecurityIdentity("S", "OLD", "OLD", "OLD", "NYSE")])
        self.assertEqual(reg.revise("S", engine_symbol="NEW", yahoo_symbol="NEW").security_id, "S")
    def test_M07_share_classes_are_distinct(self):
        reg = IdentityRegistry([SecurityIdentity("A", "X.A", "X.A", "X-A", "NYSE", share_class="A"), SecurityIdentity("B", "X.B", "X.B", "X-B", "NYSE", share_class="B")])
        self.assertEqual(len(reg.to_list()), 2)
    def test_M08_provider_symbol_collision(self):
        with self.assertRaises(IdentityConflict):
            IdentityRegistry([SecurityIdentity("A", "A", "A", "ONE", "NYSE"), SecurityIdentity("B", "B", "B", "ONE", "NYSE")])
    def test_M09_wrong_asset_type_hold(self):
        with self.assertRaises(IdentityConflict): IdentityRegistry([SecurityIdentity("A", "A", "A", "A", "NYSE", asset_type="ETF")])
    def test_M10_unverified_mapping_blocked(self):
        reg = IdentityRegistry([SecurityIdentity("A", "A", "A", "A", "NYSE", mapping_status=MappingStatus.HOLD)])
        with self.assertRaises(IdentityConflict): reg.require_verified("A")


if __name__ == "__main__": unittest.main()
