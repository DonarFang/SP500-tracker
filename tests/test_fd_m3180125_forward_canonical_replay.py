from __future__ import annotations

import ast
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "replay_fd_m3180125_forward_canonical.py"


def _source() -> str:
    return SCRIPT.read_text(encoding="utf-8")


class ForwardCanonicalReplayContractTests(unittest.TestCase):
    def test_forward_only_and_frozen_at_boundary(self) -> None:
        source = _source()
        self.assertIn('FIRST_FORWARD_DATE = "2026-06-17"', source)
        self.assertIn('SEED_DATE = "2026-06-16"', source)
        self.assertNotIn("data/live_prices", source)
        self.assertNotIn("compose_active_live_production", source)
        self.assertNotIn("src/engine/backtest.py", source)
        self.assertIn("allow_official_write=True", source)

    def test_requires_single_step_and_rejects_sim_end(self) -> None:
        source = _source()
        self.assertIn('metadata.get("single_step_decision") is not True', source)
        self.assertIn('metadata.get("external_strategy_inputs") is not False', source)
        self.assertIn('"SIM_END" in path.read_text', source)
        self.assertIn('"sim_end_replayed": False', source)

    def test_has_no_network_or_process_mutation_calls(self) -> None:
        tree = ast.parse(_source())
        forbidden = {
            "urlopen", "requests", "unlink", "rmtree", "replace", "rename"
        }
        calls = {
            node.func.attr
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
        }
        self.assertFalse(calls & forbidden)
