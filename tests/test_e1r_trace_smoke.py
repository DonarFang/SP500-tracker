from __future__ import annotations

import hashlib
import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.engine.e1r_trace import (
    canonical_json_bytes,
    emit_trace,
    trace_enabled,
)


class E1RTraceSmokeTest(unittest.TestCase):
    def test_trace_disabled_is_noop(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "disabled.jsonl"

            env = {
                "E1R_TRACE_PATH": str(output),
            }

            with patch.dict(
                os.environ,
                env,
                clear=True,
            ):
                self.assertFalse(trace_enabled())
                emit_trace(
                    "TP_DISABLED",
                    value=1,
                )

            self.assertFalse(output.exists())

    def test_enabled_writes_canonical_hash(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "enabled.jsonl"

            env = {
                "E1R_TRACE_ENABLED": "1",
                "E1R_TRACE_PATH": str(output),
            }

            with patch.dict(
                os.environ,
                env,
                clear=True,
            ):
                emit_trace(
                    "TP_TEST",
                    signal_date="2026-07-11",
                    symbol="AAPL",
                    candidate_order=["B", "A"],
                    nested={
                        "z": 1,
                        "a": 2,
                    },
                )

            rows = output.read_text(
                encoding="utf-8"
            ).splitlines()

            self.assertEqual(len(rows), 1)

            record = json.loads(rows[0])
            record_hash = record.pop(
                "record_hash"
            )

            expected_hash = hashlib.sha256(
                canonical_json_bytes(record)
            ).hexdigest()

            self.assertEqual(
                record_hash,
                expected_hash,
            )

            self.assertEqual(
                record["trace_point_id"],
                "TP_TEST",
            )

            self.assertEqual(
                record["candidate_order"],
                ["B", "A"],
            )

    def test_rejects_non_finite_float(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            output = Path(tmpdir) / "nan.jsonl"

            env = {
                "E1R_TRACE_ENABLED": "1",
                "E1R_TRACE_PATH": str(output),
            }

            with patch.dict(
                os.environ,
                env,
                clear=True,
            ):
                with self.assertRaises(ValueError):
                    emit_trace(
                        "TP_TEST",
                        value=float("nan"),
                    )

            self.assertFalse(output.exists())

    def test_set_is_canonically_sorted(self):
        payload = {
            "values": {"B", "A", "C"},
        }

        encoded = canonical_json_bytes(
            payload
        ).decode("utf-8")

        self.assertEqual(
            encoded,
            '{"values":["A","B","C"]}',
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
