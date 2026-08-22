import hashlib
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from e1r_engine.source_automation.verification import SourceVerifier, SymbolResolver, VerificationError


TEXT = b"official evidence"


def mapping_payload(rows=None):
    return {"schema_version": "1.0", "provider": "Yahoo Finance", "non_identity_mappings": rows or []}


class SA2Tests(unittest.TestCase):
    def prepare(self, root, add="RDDT", remove="AVB", date="Tuesday, August 18", mapping=None):
        root = Path(root)
        map_path = root / "config/sp500_source_automation/provider_symbol_map.json"
        map_path.parent.mkdir(parents=True)
        map_path.write_text(json.dumps(mapping or mapping_payload()))
        source_id = "SPD-JI-test"
        raw = root / "data/sp500_source_monitor/documents" / source_id / "source.html"
        raw.parent.mkdir(parents=True)
        raw.write_bytes(TEXT)
        detection = {
            "source_id": source_id, "source_url": "https://press.spglobal.com/test",
            "source_document_sha256": hashlib.sha256(TEXT).hexdigest(),
            "published_text": "Thu, 13 Aug 2026 18:12:00 -0400", "status": "DETECTED",
            "raw_document_path": "documents/%s/source.html" % source_id,
            "candidates": [
                {"action": "ADD", "company_name": "New", "official_symbol": add,
                 "replaced_official_symbol": remove, "effective_date_text": date,
                 "effective_timing_text": "prior to the opening"},
                {"action": "REMOVE", "company_name": "Old", "official_symbol": remove,
                 "replaced_official_symbol": add, "effective_date_text": date,
                 "effective_timing_text": "prior to the opening"},
            ],
        }
        path = root / "data/sp500_source_monitor/detections" / source_id / "detection.json"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(detection))
        return path

    def verifier(self, root, probe=lambda symbol: [{"date": "2026-08-21", "close": 10.0}]):
        return SourceVerifier(Path(root), probe, now=lambda: datetime(2026, 8, 22, tzinfo=timezone.utc))

    def test_real_pair_identity_mapping_passes(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root)
            result = self.verifier(root).verify_detection(path)
            self.assertEqual(result["status"], "VERIFIED_NO_EVENT")
            self.assertEqual([x["identity"]["yahoo_symbol"] for x in result["entries"]], ["RDDT", "AVB"])

    def test_missing_year_uses_publication_year(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root)
            result = self.verifier(root).verify_detection(path)
            self.assertEqual(result["effective_date"], "2026-08-18")

    def test_explicit_non_identity_mapping(self):
        row = {"security_id": "x", "spdj_symbol": "BRK.B", "engine_symbol": "BRK.B", "yahoo_symbol": "BRK-B",
               "exchange": "NYSE", "share_class": "B", "currency": "USD", "valid_from": "1996-05-09",
               "valid_to": None, "status": "ACTIVE", "evidence": "e", "evidence_sha256": hashlib.sha256(b"e").hexdigest()}
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root, add="BRK.B", mapping=mapping_payload([row]))
            result = self.verifier(root).verify_detection(path)
            self.assertEqual(result["entries"][0]["identity"]["yahoo_symbol"], "BRK-B")
            self.assertEqual(result["entries"][0]["identity"]["mapping_mode"], "EXPLICIT_EVIDENCED")

    def test_no_unrestricted_punctuation_guess(self):
        with tempfile.TemporaryDirectory() as root:
            calls = []
            path = self.prepare(root, add="BRK.B")
            self.verifier(root, lambda symbol: calls.append(symbol) or []).verify_detection(path)
            self.assertEqual(calls[0], "BRK.B")

    def test_provider_failure_quarantines_and_alerts(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root)
            result = self.verifier(root, lambda symbol: []).verify_detection(path)
            self.assertEqual(result["status"], "VERIFICATION_HOLD")
            self.assertTrue(result["manual_intervention_required"])
            self.assertTrue(all(x["status"] == "ENTRY_QUARANTINE" for x in result["entries"]))
            self.assertEqual(result["entries"][0]["attempted_yahoo_symbol"], "RDDT")
            self.assertIn("Confirm the security identity", result["entries"][0]["manual_action"])
            self.assertEqual(len(list((Path(root) / "data/sp500_source_verification/alerts").glob("*.json"))), 1)

    def test_invalid_close_quarantines(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root)
            result = self.verifier(root, lambda symbol: [{"date": "2026-08-21", "close": 0}]).verify_detection(path)
            self.assertEqual(result["status"], "VERIFICATION_HOLD")

    def test_hash_mismatch_holds(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root)
            payload = json.loads(path.read_text())
            payload["source_document_sha256"] = "0" * 64
            path.write_text(json.dumps(payload))
            result = self.verifier(root).verify_detection(path)
            self.assertIn("RAW_SOURCE_HASH_MISMATCH", result["failure_codes"])

    def test_nonreciprocal_pair_holds(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root)
            payload = json.loads(path.read_text())
            payload["candidates"][1]["replaced_official_symbol"] = "WRONG"
            path.write_text(json.dumps(payload))
            result = self.verifier(root).verify_detection(path)
            self.assertIn("CHANGE_PAIR_NOT_RECIPROCAL", result["failure_codes"])

    def test_weekday_mismatch_holds(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root, date="Monday, August 18")
            result = self.verifier(root).verify_detection(path)
            self.assertIn("EFFECTIVE_WEEKDAY_MISMATCH", result["failure_codes"])

    def test_event_and_price_flags_always_false(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root)
            result = self.verifier(root).verify_detection(path)
            self.assertFalse(result["membership_event_created"])
            self.assertFalse(result["price_data_written"])
            self.assertFalse(result["production_invoked"])

    def test_idempotent_immutable_output(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root)
            verifier = self.verifier(root)
            self.assertEqual(verifier.verify_detection(path), verifier.verify_detection(path))

    def test_mapping_conflict_rejected(self):
        row = {"security_id": "x", "spdj_symbol": "BRK.B", "engine_symbol": "BRK.B", "yahoo_symbol": "BRK-B",
               "exchange": "NYSE", "share_class": "B", "currency": "USD", "valid_from": "1996-05-09",
               "status": "ACTIVE", "evidence": "e", "evidence_sha256": hashlib.sha256(b"e").hexdigest()}
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "map.json"
            path.write_text(json.dumps(mapping_payload([row, row])))
            with self.assertRaises(VerificationError):
                SymbolResolver(path)

    def test_mapping_evidence_hash_rejected(self):
        row = {"security_id": "x", "spdj_symbol": "BRK.B", "engine_symbol": "BRK.B", "yahoo_symbol": "BRK-B",
               "exchange": "NYSE", "share_class": "B", "currency": "USD", "valid_from": "1996-05-09",
               "status": "ACTIVE", "evidence": "e", "evidence_sha256": "0" * 64}
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "map.json"
            path.write_text(json.dumps(mapping_payload([row])))
            with self.assertRaises(VerificationError):
                SymbolResolver(path)

    def test_mapping_date_validity_enforced(self):
        row = {"security_id": "x", "spdj_symbol": "BRK.B", "engine_symbol": "BRK.B", "yahoo_symbol": "BRK-B",
               "exchange": "NYSE", "share_class": "B", "currency": "USD", "valid_from": "2027-01-01",
               "status": "ACTIVE", "evidence": "e", "evidence_sha256": hashlib.sha256(b"e").hexdigest()}
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root, add="BRK.B", mapping=mapping_payload([row]))
            result = self.verifier(root).verify_detection(path)
            self.assertIn("BRK.B:PROVIDER_MAPPING_NOT_DATE_VALID", result["failure_codes"])

    def test_run_all_verifies_duplicate_semantics_once(self):
        with tempfile.TemporaryDirectory() as root:
            first = self.prepare(root)
            value = json.loads(first.read_text())
            second_id = "SPD-JI-test-duplicate"
            second_raw = Path(root) / "data/sp500_source_monitor/documents" / second_id / "source.html"
            second_raw.parent.mkdir(parents=True)
            second_raw.write_bytes(TEXT)
            value["source_id"] = second_id
            value["raw_document_path"] = "documents/%s/source.html" % second_id
            second = Path(root) / "data/sp500_source_monitor/detections" / second_id / "detection.json"
            second.parent.mkdir(parents=True)
            second.write_text(json.dumps(value))
            calls = []
            result = self.verifier(root, lambda symbol: calls.append(symbol) or [{"date": "2026-08-21", "close": 10.0}]).run_all()
            self.assertEqual(result["status"], "PASS_SA2_VERIFICATION")
            self.assertEqual(result["semantic_change_count"], 1)
            self.assertEqual(result["duplicate_detection_count"], 1)
            self.assertEqual(calls, ["RDDT", "AVB"])

    def test_accepted_verification_is_reused_without_provider_probe(self):
        with tempfile.TemporaryDirectory() as root:
            path = self.prepare(root)
            first_calls = []
            first = self.verifier(
                root,
                lambda symbol: first_calls.append(symbol) or [{"date": "2026-08-21", "close": 10.0}],
            ).verify_detection(path)
            second_calls = []
            second = self.verifier(
                root,
                lambda symbol: second_calls.append(symbol) or [{"date": "2026-08-22", "close": 11.0}],
            ).verify_detection(path)
            self.assertEqual(second, first)
            self.assertEqual(first_calls, ["RDDT", "AVB"])
            self.assertEqual(second_calls, [])
            files = list((Path(root) / "data/sp500_source_verification/verifications/SPD-JI-test").glob("*.json"))
            self.assertEqual(len(files), 1)

    def test_workflow_run_connects_sa1_to_sa2(self):
        root = Path(__file__).resolve().parents[1]
        text = (root / ".github/workflows/sp500-source-verification-daily.yml").read_text()
        self.assertIn("workflow_run:", text)
        self.assertIn("S&P 500 Official Source Monitor", text)
        self.assertIn("workflow_run.conclusion == 'success'", text)
        self.assertNotIn("schedule:", text)
        self.assertNotIn("data/sp500_source_monitor/detections/**", text)
        self.assertNotIn("data/sp500_source_verification/**", text)


if __name__ == "__main__":
    unittest.main()
