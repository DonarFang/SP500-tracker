import hashlib
import json
import tempfile
import unittest
from unittest.mock import patch
from datetime import date, timedelta
from pathlib import Path

from e1r_engine.source_automation.event_publication import (
    EventPublicationError,
    VerifiedEventPublisher,
    refresh_track_snapshot,
)


class SA3EventTests(unittest.TestCase):
    def prepare(self, root):
        root = Path(root)
        source_id = "SPD-JI-test"
        raw = root / "data/sp500_source_monitor/documents" / source_id / "source.html"
        raw.parent.mkdir(parents=True)
        raw.write_bytes(b"official")
        detection = {
            "source_id": source_id, "status": "DETECTED",
            "source_url": "https://press.spglobal.com/test",
            "source_document_sha256": hashlib.sha256(b"official").hexdigest(),
            "raw_document_path": "documents/%s/source.html" % source_id,
            "published_text": "Thu, 13 Aug 2026 18:12:00 -0400",
            "detected_at_utc": "2026-08-13T22:13:00Z",
        }
        dp = root / "data/sp500_source_monitor/detections" / source_id / "detection.json"
        dp.parent.mkdir(parents=True)
        dp.write_text(json.dumps(detection))
        state = root / "data/sp500_source_monitor/state/current.json"
        state.parent.mkdir(parents=True)
        state.write_text(json.dumps({"status": "PASS_SOURCE_SCAN", "source_ids": [source_id]}))
        verification = {
            "status": "VERIFIED_NO_EVENT", "source_id": source_id,
            "verification_id": "SA2-first", "verified_at_utc": "2026-08-13T23:00:00Z",
            "effective_date": "2026-08-18", "provider": "Yahoo Finance",
            "provider_mapping_sha256": "a" * 64, "manual_intervention_required": False,
            "membership_event_created": False, "price_data_written": False, "production_invoked": False,
            "entries": [
                {"action": "ADD", "company_name": "Reddit Inc", "status": "VERIFIED", "identity": {
                    "spdj_symbol": "RDDT", "engine_symbol": "RDDT", "yahoo_symbol": "RDDT",
                    "status": "VERIFIED", "currency": "USD", "price_evidence_sha256": "b" * 64,
                }},
                {"action": "REMOVE", "company_name": "AvalonBay", "status": "VERIFIED", "identity": {
                    "spdj_symbol": "AVB", "engine_symbol": "AVB", "yahoo_symbol": "AVB",
                    "status": "VERIFIED", "currency": "USD", "price_evidence_sha256": "c" * 64,
                }},
            ],
        }
        vp = root / "data/sp500_source_verification/verifications" / source_id / "SA2-first.json"
        vp.parent.mkdir(parents=True)
        vp.write_text(json.dumps(verification))
        current = root / "data/sp500_source_verification/state/current.json"
        current.parent.mkdir(parents=True)
        current.write_text(json.dumps(verification))
        for track in ("forward", "live"):
            baseline = root / "exports/official/FD-M3180125-SP500-TOP3-engine" / track / "universe/baseline/PRODUCTION_BASELINE.json"
            baseline.parent.mkdir(parents=True)
            baseline.write_text(json.dumps({"snapshot_id": track.upper() + "-BASE", "symbols": ["AAA", "AVB"]}))
        return root, verification

    def prices(self):
        start = date(2024, 1, 2)
        return [
            {"date": (start + timedelta(days=i)).isoformat(), "open": 10+i/100, "high": 11+i/100,
             "low": 9+i/100, "close": 10.5+i/100, "volume": 1000+i}
            for i in range(300)
        ]

    def test_publish_is_dual_track_atomic_and_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.prepare(directory)
            calls = []
            publisher = VerifiedEventPublisher(root, lambda symbol: calls.append(symbol) or self.prices())
            first = publisher.publish()
            second = publisher.publish()
            self.assertEqual(first, second)
            self.assertEqual(calls, ["RDDT"])
            self.assertEqual(first["additions"], ["RDDT"])
            self.assertEqual(first["deletions"], ["AVB"])
            fw = root / first["forward_event_path"]
            live = root / first["live_event_path"]
            self.assertEqual(json.loads(fw.read_text()), json.loads(live.read_text()))
            self.assertNotEqual(fw.stat().st_ino, live.stat().st_ino)
            self.assertNotEqual((root / "data/fw_prices/RDDT.json").stat().st_ino, (root / "data/live_prices/RDDT.json").stat().st_ino)
            for track, stem in (("forward", "fw"), ("live", "live")):
                pointer = json.loads((root / ("data/%s_universe/state/current.json" % stem)).read_text())
                snapshot = json.loads((root / ("data/%s_universe/snapshots" % stem) / (pointer["snapshot_id"] + ".json")).read_text())
                self.assertIn("RDDT", snapshot["effective_membership"])
                self.assertNotIn("AVB", snapshot["effective_membership"])

    def test_price_failure_creates_no_event_or_price(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.prepare(directory)
            with self.assertRaises(EventPublicationError):
                VerifiedEventPublisher(root, lambda symbol: []).publish()
            self.assertFalse((root / "data/fw_prices/RDDT.json").exists())
            self.assertFalse((root / "data/fw_universe/events").exists())
            self.assertFalse((root / "data/live_universe/events").exists())

    def test_second_track_failure_rolls_back_entire_publication(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.prepare(directory)
            from e1r_engine.universe_versioning.storage import TrackStorage
            original = TrackStorage.publish_snapshot

            def fail_live(storage, snapshot):
                if storage.track == "live":
                    raise RuntimeError("injected live publication failure")
                return original(storage, snapshot)

            with patch.object(TrackStorage, "publish_snapshot", fail_live):
                with self.assertRaisesRegex(RuntimeError, "injected live"):
                    VerifiedEventPublisher(root, lambda symbol: self.prices()).publish()
            for path in (
                "data/fw_prices/RDDT.json", "data/live_prices/RDDT.json",
                "data/fw_universe/events", "data/live_universe/events",
                "data/fw_universe/state/current.json", "data/live_universe/state/current.json",
                "data/sp500_source_events/state/current.json",
            ):
                target = root / path
                self.assertFalse(target.is_file() if target.suffix else any(target.rglob("*.json")) if target.exists() else False)

    def test_conflicting_accepted_verification_holds(self):
        with tempfile.TemporaryDirectory() as directory:
            root, verification = self.prepare(directory)
            conflict = json.loads(json.dumps(verification))
            conflict["verification_id"] = "SA2-conflict"
            conflict["entries"][0]["identity"]["yahoo_symbol"] = "WRONG"
            path = root / "data/sp500_source_verification/verifications/SPD-JI-test/SA2-conflict.json"
            path.write_text(json.dumps(conflict))
            with self.assertRaisesRegex(EventPublicationError, "CONFLICTING_ACCEPTED_VERIFICATIONS"):
                VerifiedEventPublisher(root, lambda symbol: self.prices()).publish()

    def test_current_verification_hold_blocks_manual_publication(self):
        with tempfile.TemporaryDirectory() as directory:
            root, verification = self.prepare(directory)
            verification["status"] = "VERIFICATION_HOLD"
            verification["manual_intervention_required"] = True
            current = root / "data/sp500_source_verification/state/current.json"
            current.write_text(json.dumps(verification))
            with self.assertRaisesRegex(EventPublicationError, "VERIFICATION_CURRENT_NOT_ACCEPTED"):
                VerifiedEventPublisher(root, lambda symbol: self.prices()).publish()

    def test_effective_date_boundary(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.prepare(directory)
            result = VerifiedEventPublisher(root, lambda symbol: self.prices()).publish()
            before = refresh_track_snapshot(root, "forward", "2026-08-17")
            effective = refresh_track_snapshot(root, "forward", "2026-08-18")
            self.assertIn("AVB", before.effective_membership)
            self.assertNotIn("RDDT", before.effective_membership)
            self.assertNotIn("AVB", effective.effective_membership)
            self.assertIn("RDDT", effective.effective_membership)
            self.assertTrue(result["event_id"].startswith("SP500-"))

    def test_forward_pre_activation_reconciliation_is_date_scoped(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.prepare(directory)
            path = root / "data/fw_universe/pre_activation_reconciliations.json"
            path.parent.mkdir(parents=True, exist_ok=True)
            from e1r_engine.universe_versioning.hashing import content_hash
            payload = {
                "track": "forward",
                "status": "CANONICAL_PRE_ACTIVATION_RECONCILIATION",
                "reconciliations": [{
                    "outgoing": "AAA",
                    "incoming": "NEW",
                    "effective_date": "2026-08-05",
                    "source_url": "https://example.invalid/official",
                }],
            }
            payload["content_hash"] = content_hash(payload)
            path.write_text(json.dumps(payload))

            before = refresh_track_snapshot(root, "forward", "2026-08-04")
            effective = refresh_track_snapshot(root, "forward", "2026-08-05")
            self.assertIn("AAA", before.effective_membership)
            self.assertNotIn("NEW", before.effective_membership)
            self.assertNotIn("AAA", effective.effective_membership)
            self.assertIn("NEW", effective.effective_membership)

    def test_identity_preserves_official_and_yahoo_symbols(self):
        with tempfile.TemporaryDirectory() as directory:
            root, _ = self.prepare(directory)
            result = VerifiedEventPublisher(root, lambda symbol: self.prices()).publish()
            event = json.loads((root / result["forward_event_path"]).read_text())
            add = next(row for row in event["identity_mapping_results"] if row["engine_symbol"] == "RDDT")
            self.assertEqual(add["spdj_symbol"], "RDDT")
            self.assertEqual(add["yahoo_symbol"], "RDDT")
            self.assertEqual(add["mapping_status"], "VERIFIED")


if __name__ == "__main__":
    unittest.main()
