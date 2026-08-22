import hashlib
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from e1r_engine.universe_versioning.storage import TrackStorage


def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()


class ZeroHistoryImpactTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
        self.protected = {}
        for name in ["data/research/e1_5y/a", "data/forward/daily/a", "data/live/daily/a", "data/forward/account/a", "data/live/ledger/a", "data/fw_prices/A.json", "src/e1r_engine/core.py", "data/legacy/a", "data/screening/a"]:
            path = self.root / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(name); self.protected[name] = digest(path)
    def tearDown(self): self.tmp.cleanup()
    def unchanged(self, name): self.assertEqual(digest(self.root / name), self.protected[name])
    def test_Z01_5y_unchanged(self): TrackStorage(self.root, "forward").write_baseline({"x": 1}); self.unchanged("data/research/e1_5y/a")
    def test_Z02_forward_daily_unchanged(self): TrackStorage(self.root, "forward").write_baseline({"x": 1}); self.unchanged("data/forward/daily/a")
    def test_Z03_live_daily_unchanged(self): TrackStorage(self.root, "live").write_baseline({"x": 1}); self.unchanged("data/live/daily/a")
    def test_Z04_forward_account_unchanged(self): TrackStorage(self.root, "forward").write_baseline({"x": 1}); self.unchanged("data/forward/account/a")
    def test_Z05_live_ledger_unchanged(self): TrackStorage(self.root, "live").write_baseline({"x": 1}); self.unchanged("data/live/ledger/a")
    def test_Z06_price_history_unchanged(self): TrackStorage(self.root, "forward").write_baseline({"x": 1}); self.unchanged("data/fw_prices/A.json")
    def test_Z07_engine_strategy_unchanged(self): TrackStorage(self.root, "forward").write_baseline({"x": 1}); self.unchanged("src/e1r_engine/core.py")
    def test_Z08_legacy_screening_unchanged(self):
        TrackStorage(self.root, "live").write_baseline({"x": 1}); self.unchanged("data/legacy/a"); self.unchanged("data/screening/a")
    def test_Z09_shadow_has_no_engine_output(self):
        TrackStorage(self.root, "forward").write_baseline({"x": 1}); self.assertFalse((self.root / "data/forward/orders").exists())
    def test_Z10_only_uv_paths_change(self):
        TrackStorage(self.root, "live").write_baseline({"x": 1})
        changed = [p.relative_to(self.root).as_posix() for p in self.root.rglob("*") if p.is_file() and p.relative_to(self.root).as_posix() not in self.protected]
        self.assertEqual(changed, ["exports/official/FD-M3180125-SP500-TOP3-engine/live/universe/baseline/LEGACY_BASELINE_PRESERVED.json"])


if __name__ == "__main__": unittest.main()
