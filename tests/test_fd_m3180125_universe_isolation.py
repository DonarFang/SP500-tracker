import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from e1r_engine.universe_versioning.contracts import EventStatus, MembershipEvent
from e1r_engine.universe_versioning.resolver import MembershipResolver
from e1r_engine.universe_versioning.storage import StorageBoundaryError, TrackStorage


def event(): return MembershipEvent("E", 1, "SP500", "SPDJI_INDEX_NEWS", "u", "h", "2026-08-11T00:00:00Z", "2026-08-12", "09:30", "America/New_York", ["NEW"], ["OLD"], event_status=EventStatus.AUTO_VERIFIED)


class IsolationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.root = Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def test_I01_same_event_separate_files(self):
        f, l = TrackStorage(self.root, "forward"), TrackStorage(self.root, "live")
        self.assertNotEqual(f.append_event(event()), l.append_event(event()))
    def test_I02_forward_failure_does_not_touch_live(self):
        live = TrackStorage(self.root, "live"); live.write_baseline({"x": 1})
        with self.assertRaises(StorageBoundaryError): live.atomic_write(self.root / "data/fw_universe/x.json", {})
        self.assertTrue((live.export_root / "baseline/LEGACY_BASELINE_PRESERVED.json").exists())
    def test_I03_live_failure_does_not_touch_forward(self):
        fw = TrackStorage(self.root, "forward"); fw.write_baseline({"x": 1})
        with self.assertRaises(StorageBoundaryError): fw.atomic_write(self.root / "data/live_universe/x.json", {})
        self.assertTrue((fw.export_root / "baseline/LEGACY_BASELINE_PRESERVED.json").exists())
    def test_I04_idempotent_immutable_event(self):
        store = TrackStorage(self.root, "forward"); first = store.append_event(event()); second = store.append_event(event())
        self.assertEqual(first.read_bytes(), second.read_bytes())
    def test_I05_conflict_holds_immutable_revision(self):
        store = TrackStorage(self.root, "forward"); store.append_event(event())
        with self.assertRaises(StorageBoundaryError): store.append_event(event().__class__(**{**event().__dict__, "source_url": "changed"}))
    def test_I06_atomic_write_leaves_no_temp(self):
        store = TrackStorage(self.root, "forward"); store.write_baseline({"x": 1})
        self.assertEqual(list(store.export_root.rglob("*.tmp")), [])
    def test_I07_snapshot_hash_checked(self):
        snap = MembershipResolver("forward", "2026-08-10T00:00:00Z").resolve("2026-08-12", "B", ["OLD"], [event()])
        path = TrackStorage(self.root, "forward").publish_snapshot(snap)
        self.assertEqual(json.loads(path.read_text())["content_hash"], snap.content_hash)
    def test_I08_symlink_storage_rejected(self):
        outside = self.root / "outside"; outside.mkdir(); link = self.root / "data/fw_universe"; link.parent.mkdir(); link.symlink_to(outside, target_is_directory=True)
        with self.assertRaises(StorageBoundaryError): TrackStorage(self.root, "forward").append_event(event())
    def test_I09_nonwhitelist_write_rejected(self):
        with self.assertRaises(StorageBoundaryError): TrackStorage(self.root, "forward").atomic_write(self.root / "dashboard/x.json", {})
    def test_I10_dashboard_absence_irrelevant(self):
        self.assertFalse((self.root / "dashboard").exists()); self.assertTrue(TrackStorage(self.root, "forward").data_root.name == "fw_universe")


if __name__ == "__main__": unittest.main()
