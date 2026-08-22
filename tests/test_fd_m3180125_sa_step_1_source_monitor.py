import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from e1r_engine.source_automation.monitor import (
    OfficialSourceMonitor,
    SourceMonitorError,
    _canonical_url,
    _is_target_title,
    extract_candidates,
)


LANDING = "https://www.spglobal.com/spdji/en/media-center/news-announcements/"
TARGET = "https://www.spglobal.com/spdji/en/documents/indexnews/announcements/example/change.html"
API = "https://www.spglobal.com/spdji/en/util/redesign/press-room/get-pr-news-announcements-solr-json.dot?contentSubType=indexNews&pageNumber=1"
LANDING_BYTES = b'<div data-actionurl="/spdji/en/util/redesign/press-room/get-pr-news-announcements-solr-json.dot"></div>'
TEXT = (
    "Reddit Inc. (NYSE: RDDT) will replace AvalonBay Communities Inc. "
    "(NYSE: AVB) in the S&P 500 effective prior to the opening of trading "
    "on Tuesday, August 18, 2026."
)


class SA1ContractTests(unittest.TestCase):
    def test_official_url_allowed(self):
        self.assertEqual(_canonical_url(LANDING), LANDING)

    def test_non_https_rejected(self):
        with self.assertRaises(SourceMonitorError):
            _canonical_url(LANDING.replace("https", "http", 1))

    def test_foreign_domain_rejected(self):
        with self.assertRaises(SourceMonitorError):
            _canonical_url("https://example.com/spdji/en/x")

    def test_wrong_official_path_rejected(self):
        with self.assertRaises(SourceMonitorError):
            _canonical_url("https://www.spglobal.com/other")

    def test_target_title_selected(self):
        self.assertTrue(_is_target_title("Reddit Set to Join S&P 500"))

    def test_derivative_index_excluded(self):
        self.assertFalse(_is_target_title("S&P 500 Equal Weight Index Rebalance"))
        self.assertFalse(_is_target_title("S&P 500 Methodology Consultation"))

    def test_replace_pair_extracted(self):
        candidates = extract_candidates(TEXT)
        self.assertEqual([(x.action, x.official_symbol) for x in candidates], [("ADD", "RDDT"), ("REMOVE", "AVB")])

    def test_official_symbol_preserved(self):
        candidates = extract_candidates(TEXT.replace("RDDT", "BRK.B"))
        self.assertEqual(candidates[0].official_symbol, "BRK.B")

    def test_effective_semantics_preserved_as_text(self):
        candidate = extract_candidates(TEXT)[0]
        self.assertEqual(candidate.effective_date_text, "Tuesday, August 18, 2026")
        self.assertIn("prior to the opening", candidate.effective_timing_text.lower())

    def _monitor(self, root, rows, target_bytes, fail_target=False, landing_bytes=LANDING_BYTES):
        def fetch(url):
            if url == LANDING:
                return landing_bytes, "text/html"
            if url == API:
                return json.dumps({"pagination": {"totalPages": 1}, "resultData": rows}).encode(), "application/json"
            if url == TARGET and not fail_target:
                return target_bytes, "text/html"
            raise SourceMonitorError("SOURCE_FETCH_FAILED")
        return OfficialSourceMonitor(
            Path(root), fetch=fetch,
            now=lambda: datetime(2026, 8, 22, 12, 0, tzinfo=timezone.utc),
        )

    def test_scan_persists_raw_and_detection(self):
        page = ('<a href="%s">Reddit Set to Join S&amp;P 500</a>' % TARGET).encode()
        with tempfile.TemporaryDirectory() as root:
            result = self._monitor(root, [{"title": "Reddit Set to Join S&P 500", "link": TARGET, "date": "Aug 13, 2026"}], TEXT.encode()).run(max_pages=1)
            self.assertEqual(result["status"], "PASS_SOURCE_SCAN")
            self.assertEqual(result["candidate_count"], 2)
            files = list((Path(root) / "data/sp500_source_monitor/documents").glob("*/source.html"))
            self.assertEqual(len(files), 1)
            self.assertEqual(files[0].read_bytes(), TEXT.encode())

    def test_repeat_scan_is_idempotent(self):
        page = ('<a href="%s">Reddit Set to Join S&amp;P 500</a>' % TARGET).encode()
        with tempfile.TemporaryDirectory() as root:
            monitor = self._monitor(root, [{"title": "Reddit Set to Join S&P 500", "link": TARGET, "date": "Aug 13, 2026"}], TEXT.encode())
            first = monitor.run(max_pages=1)
            second = monitor.run(max_pages=1)
            self.assertEqual(first["source_ids"], second["source_ids"])
            self.assertEqual(len(list((Path(root) / "data/sp500_source_monitor/detections").glob("*/detection.json"))), 1)

    def test_successful_listing_without_target_is_no_change(self):
        with tempfile.TemporaryDirectory() as root:
            result = self._monitor(root, [{"title": "Unrelated Index News", "link": "/spdji/en/x"}], b"").run(max_pages=1)
            self.assertEqual(result["status"], "PASS_SOURCE_SCAN")
            self.assertEqual(result["candidate_count"], 0)

    def test_missing_official_endpoint_is_hold(self):
        with tempfile.TemporaryDirectory() as root:
            result = self._monitor(root, [], b"", landing_bytes=b"<html></html>").run(max_pages=1)
            self.assertEqual(result["status"], "SOURCE_HOLD")
            self.assertIn("OFFICIAL_LISTING_ENDPOINT_NOT_DISCOVERED", result["failure_codes"])

    def test_target_fetch_failure_is_hold(self):
        page = ('<a href="%s">Reddit Set to Join S&amp;P 500</a>' % TARGET).encode()
        with tempfile.TemporaryDirectory() as root:
            result = self._monitor(root, [{"title": "Reddit Set to Join S&P 500", "link": TARGET}], b"", fail_target=True).run(max_pages=1)
            self.assertEqual(result["status"], "SOURCE_HOLD")
            self.assertIn("SOURCE_FETCH_FAILED", result["failure_codes"])

    def test_parse_incomplete_is_hold(self):
        page = ('<a href="%s">Reddit Set to Join S&amp;P 500</a>' % TARGET).encode()
        with tempfile.TemporaryDirectory() as root:
            result = self._monitor(root, [{"title": "Reddit Set to Join S&P 500", "link": TARGET}], b"S&P 500 announcement without parseable rows").run(max_pages=1)
            self.assertEqual(result["status"], "SOURCE_HOLD")
            self.assertIn("TARGET_DOCUMENT_PARSE_INCOMPLETE", result["failure_codes"])

    def test_detection_contains_no_provider_symbol(self):
        page = ('<a href="%s">Reddit Set to Join S&amp;P 500</a>' % TARGET).encode()
        with tempfile.TemporaryDirectory() as root:
            self._monitor(root, [{"title": "Reddit Set to Join S&P 500", "link": TARGET}], TEXT.encode()).run(max_pages=1)
            path = next((Path(root) / "data/sp500_source_monitor/detections").glob("*/detection.json"))
            payload = json.loads(path.read_text())
            self.assertNotIn("provider_symbol", json.dumps(payload))

    def test_no_uv_or_track_artifacts_written(self):
        page = ('<a href="%s">Reddit Set to Join S&amp;P 500</a>' % TARGET).encode()
        with tempfile.TemporaryDirectory() as root:
            self._monitor(root, [{"title": "Reddit Set to Join S&P 500", "link": TARGET}], TEXT.encode()).run(max_pages=1)
            self.assertFalse((Path(root) / "data/fw_universe").exists())
            self.assertFalse((Path(root) / "data/live_universe").exists())


if __name__ == "__main__":
    unittest.main()
