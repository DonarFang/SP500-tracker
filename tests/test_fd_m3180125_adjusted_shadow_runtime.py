"""Pure-stdlib acceptance tests for the Parity-step-2 Shadow runtime repair."""

from datetime import date, datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from build_fd_m3180125_live_adjusted_shadow import (  # noqa: E402
    AdjustedShadowBuildError,
    _history_start_path,
    _production_catalogue,
    build_adjusted_shadow,
    latest_completed_session,
)
from e1r_engine.live_calendar import load_live_trading_calendar  # noqa: E402


CALENDAR = ROOT / "config/live_calendar/us_equity_calendar_v1.0.json"


def _row(day: str):
    return {
        "date": day,
        "open": 10.0,
        "high": 11.0,
        "low": 9.0,
        "close": 10.5,
        "volume": 100.0,
    }


def _legacy(root: Path, symbols):
    root.mkdir(parents=True)
    for symbol in symbols:
        (root / (symbol + ".json")).write_text(
            json.dumps([_row("2026-08-20")]), encoding="utf-8"
        )


class RetryProvider:
    def __init__(self, shadow_root: Path):
        self.calls = []
        self.shadow_root = shadow_root

    def fetch_many(self, requests, *, attempt):
        self.calls.append([item.symbol for item in requests])
        if attempt == 1:
            return {
                "AAA": [_row("2026-08-20"), _row("2026-08-21")]
            }, {
                "SPX": {
                    "attempt": 1,
                    "code": "SINGLE_SYMBOL_EXCEPTION",
                    "exception_type": "RuntimeError",
                    "message": "temporary provider failure",
                }
            }
        assert not self.shadow_root.exists()
        return {
            "SPX": [_row("2026-08-20"), _row("2026-08-21")]
        }, {}


class RaisingProvider:
    def fetch(self, **kwargs):
        raise RuntimeError("429 provider rate limit")


class AdjustedShadowRuntimeTests(unittest.TestCase):
    def test_official_shadow_membership_reconciliations_are_exact(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            legacy = base / "live_prices"
            snapshots = base / "snapshots"
            state = base / "state.json"
            members = ["CTRA", "EA"] + ["S%03d" % index for index in range(489)]
            _legacy(legacy, tuple(members) + tuple(("SPX", "NDX", "SOX", "VIX")))
            snapshots.mkdir()
            (snapshots / "LIVE-CURRENT.json").write_text(
                json.dumps({
                    "snapshot_id": "LIVE-CURRENT",
                    "track": "live",
                    "status": "EFFECTIVE",
                    "effective_membership": members,
                }),
                encoding="utf-8",
            )
            state.write_text(json.dumps({"snapshot_id": "LIVE-CURRENT"}), encoding="utf-8")
            catalogue = _production_catalogue(
                legacy_root=legacy,
                state_path=state,
                snapshot_root=snapshots,
            )
            self.assertEqual(len(catalogue), 495)
            self.assertIn("VEEV", catalogue)
            self.assertIn("FERG", catalogue)
            self.assertNotIn("CTRA", catalogue)
            self.assertNotIn("EA", catalogue)
            self.assertEqual(_history_start_path(legacy, "VEEV"), legacy / "CTRA.json")
            self.assertEqual(_history_start_path(legacy, "FERG"), legacy / "EA.json")

    def test_latest_completed_session_before_monday_close_is_friday(self):
        calendar = load_live_trading_calendar(CALENDAR)
        actual = latest_completed_session(
            as_of_utc=datetime(2026, 8, 24, 12, 0, tzinfo=timezone.utc),
            calendar=calendar,
        )
        self.assertEqual(actual, date(2026, 8, 21))

    def test_latest_completed_session_after_monday_cutoff_is_monday(self):
        calendar = load_live_trading_calendar(CALENDAR)
        actual = latest_completed_session(
            as_of_utc=datetime(2026, 8, 24, 23, 0, tzinfo=timezone.utc),
            calendar=calendar,
        )
        self.assertEqual(actual, date(2026, 8, 24))

    def test_latest_completed_session_on_weekend_is_friday(self):
        calendar = load_live_trading_calendar(CALENDAR)
        actual = latest_completed_session(
            as_of_utc=datetime(2026, 8, 23, 16, 0, tzinfo=timezone.utc),
            calendar=calendar,
        )
        self.assertEqual(actual, date(2026, 8, 21))

    def test_retry_requests_only_unresolved_and_promotes_once(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            legacy = base / "live_prices"
            shadow = base / "live_prices_adjusted_v1" / "live_prices"
            _legacy(legacy, ("AAA", "SPX"))
            provider = RetryProvider(shadow)
            result = build_adjusted_shadow(
                legacy_root=legacy,
                shadow_root=shadow,
                end_date=date(2026, 8, 21),
                provider=provider,
                symbols=("AAA", "SPX"),
                max_attempts=2,
                retry_delay_seconds=0,
            )
            self.assertEqual(provider.calls, [["AAA", "SPX"], ["SPX"]])
            self.assertEqual(result["decision"], "PASS_PARITY_STEP_2_ADJUSTED_SHADOW_BUILT")
            self.assertEqual(sorted(path.stem for path in shadow.glob("*.json")), ["AAA", "SPX"])

    def test_failure_preserves_previous_shadow_and_exact_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            legacy = base / "live_prices"
            shadow = base / "live_prices_adjusted_v1" / "live_prices"
            _legacy(legacy, ("AAA",))
            shadow.mkdir(parents=True)
            marker = shadow / "previous.json"
            marker.write_text("previous-shadow", encoding="utf-8")
            with self.assertRaises(AdjustedShadowBuildError) as caught:
                build_adjusted_shadow(
                    legacy_root=legacy,
                    shadow_root=shadow,
                    end_date=date(2026, 8, 21),
                    provider=RaisingProvider(),
                    symbols=("AAA",),
                    max_attempts=2,
                    retry_delay_seconds=0,
                )
            evidence = caught.exception.evidence
            self.assertEqual(marker.read_text(encoding="utf-8"), "previous-shadow")
            self.assertEqual(evidence["unavailable_symbols"], ["AAA"])
            self.assertEqual(len(evidence["failure_evidence"]["AAA"]), 2)
            self.assertEqual(
                evidence["failure_evidence"]["AAA"][-1]["message"],
                "429 provider rate limit",
            )

    def test_stale_required_index_is_fail_closed(self):
        class StaleProvider:
            def fetch(self, **kwargs):
                return [_row("2026-08-20")]

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            legacy = base / "live_prices"
            shadow = base / "live_prices_adjusted_v1" / "live_prices"
            _legacy(legacy, ("SPX",))
            with self.assertRaises(AdjustedShadowBuildError) as caught:
                build_adjusted_shadow(
                    legacy_root=legacy,
                    shadow_root=shadow,
                    end_date=date(2026, 8, 21),
                    provider=StaleProvider(),
                    symbols=("SPX",),
                    max_attempts=1,
                    retry_delay_seconds=0,
                )
            code = caught.exception.evidence["failure_evidence"]["SPX"][0]["code"]
            self.assertTrue(code.startswith("REQUIRED_INDEX_LATEST_DATE_MISMATCH"), code)

    def test_stale_ordinary_symbol_is_recorded_but_not_fabricated(self):
        class StaleProvider:
            def fetch(self, **kwargs):
                return [_row("2026-08-20")]

        with tempfile.TemporaryDirectory() as directory:
            base = Path(directory)
            legacy = base / "live_prices"
            shadow = base / "live_prices_adjusted_v1" / "live_prices"
            _legacy(legacy, ("AAA",))
            result = build_adjusted_shadow(
                legacy_root=legacy,
                shadow_root=shadow,
                end_date=date(2026, 8, 21),
                provider=StaleProvider(),
                symbols=("AAA",),
                max_attempts=1,
                retry_delay_seconds=0,
            )
            self.assertEqual(result["ordinary_stale_symbols"], ["AAA"])
            rows = json.loads((shadow / "AAA.json").read_text(encoding="utf-8"))
            self.assertEqual(rows[-1]["date"], "2026-08-20")

    def test_workflow_preserves_failure_evidence_before_fail_gate(self):
        workflow = (ROOT / ".github/workflows/live-track-daily.yml").read_text(encoding="utf-8")
        upload = workflow.index("name: Preserve adjusted Shadow evidence")
        gate = workflow.index("name: Enforce adjusted Shadow result")
        self.assertLess(upload, gate)
        self.assertIn("actions/upload-artifact@v4", workflow)
        self.assertIn("--as-of-utc", workflow)
        self.assertNotIn("--end-date", workflow)

    def test_cli_writes_evidence_even_for_preflight_exception(self):
        with tempfile.TemporaryDirectory() as directory:
            evidence = Path(directory) / "evidence.json"
            environment = dict(os.environ)
            environment["PYTHONPATH"] = str(ROOT / "src") + ":" + str(ROOT)
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts/build_fd_m3180125_live_adjusted_shadow.py"),
                    "--calendar-path",
                    str(Path(directory) / "missing-calendar.json"),
                    "--evidence-path",
                    str(evidence),
                ],
                cwd=ROOT,
                env=environment,
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(result.returncode, 1)
            payload = json.loads(evidence.read_text(encoding="utf-8"))
            self.assertEqual(
                payload["decision"],
                "HOLD_PARITY_STEP_2_ADJUSTED_SHADOW_EXCEPTION",
            )
            self.assertEqual(payload["exception_type"], "LiveCalendarError")

    def test_push_does_not_run_active_live(self):
        workflow = (ROOT / ".github/workflows/live-track-daily.yml").read_text(encoding="utf-8")
        active_condition = "github.event_name == 'schedule' || (github.event_name == 'workflow_dispatch'"
        self.assertGreaterEqual(workflow.count(active_condition), 2)


if __name__ == "__main__":
    unittest.main()
