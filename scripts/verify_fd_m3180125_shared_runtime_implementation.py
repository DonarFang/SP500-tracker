#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any


ENGINE_ID = "FD-M3180125-SP500-TOP3-engine"
IMPLEMENTATION_VERSION = "1.0.0"

ROOT = Path(__file__).resolve().parents[1]

RUNTIME_FILE = (
    ROOT / "src/e1r_engine/forward_runtime.py"
)

TEST_FILE = (
    ROOT
    / "tests"
    / "test_fd_m3180125_shared_runtime_implementation.py"
)

CONTRACT_ROOT = (
    ROOT
    / "exports"
    / "official"
    / ENGINE_ID
    / "forward"
    / "shared_runtime_contract"
)

OUTPUT_ROOT = (
    ROOT
    / "exports"
    / "official"
    / ENGINE_ID
    / "forward"
    / "shared_runtime_implementation"
)

DECISION_PATH = (
    OUTPUT_ROOT
    / "STEP2_OFFICIAL_SHARED_RUNTIME_IMPLEMENTATION_DECISION.json"
)

README_PATH = (
    OUTPUT_ROOT
    / "OFFICIAL_SHARED_RUNTIME_IMPLEMENTATION.md"
)

MANIFEST_PATH = OUTPUT_ROOT / "manifest.json"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def write_json(
    path: Path,
    value: Any,
) -> None:
    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    path.write_text(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )


def git_head() -> str:
    return subprocess.check_output(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
    ).strip()


def main() -> None:
    contract = json.loads(
        (
            CONTRACT_ROOT
            / "official_shared_runtime_contract.json"
        ).read_text(encoding="utf-8")
    )

    contract_decision = json.loads(
        (
            CONTRACT_ROOT
            / "STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FREEZE_DECISION.json"
        ).read_text(encoding="utf-8")
    )

    assert contract["contract_status"] == "FROZEN"
    assert (
        contract_decision["decision"]
        == "PASS_STEP2_OFFICIAL_SHARED_RUNTIME_CONTRACT_FROZEN"
    )

    required_classes = [
        "ForwardSeedLoader",
        "ForwardDatePlanner",
        "ForwardMarketDataAdapter",
        "CanonicalDailyDecisionRouter",
        "PendingOrderLedger",
        "T1ExecutionEngine",
        "ForwardAccountRepository",
        "ForwardDailyCommitter",
        "OfficialForwardArtifactWriter",
    ]

    runtime_source = RUNTIME_FILE.read_text(
        encoding="utf-8"
    )

    missing = [
        class_name
        for class_name in required_classes
        if f"class {class_name}" not in runtime_source
    ]

    assert not missing, missing
    assert "SIM_END_LIQUIDATION" not in runtime_source
    assert "run_stateful_simulation(" not in runtime_source

    decision = {
        "engine_id": ENGINE_ID,
        "step": (
            "STEP2_OFFICIAL_SHARED_RUNTIME_IMPLEMENTATION"
        ),
        "decision": (
            "PASS_STEP2_OFFICIAL_SHARED_RUNTIME_IMPLEMENTATION"
        ),
        "implementation_version": (
            IMPLEMENTATION_VERSION
        ),
        "three_step_plan": {
            "step_1": "COMPLETE",
            "step_2": "IMPLEMENTATION_COMPLETE_FORWARD_NOT_RUN",
            "step_3": "NOT_STARTED",
            "additional_steps_created": False,
        },
        "frozen_prerequisites": {
            "engine_development": "COMPLETE",
            "canonical_5y_backtest": "PASS",
            "uptrend": "COMPLETE",
            "sideways": "COMPLETE",
            "shared_runtime_contract": "FROZEN",
        },
        "implemented_modules": required_classes,
        "source_files": {
            str(RUNTIME_FILE.relative_to(ROOT)): {
                "sha256": sha256_file(
                    RUNTIME_FILE
                )
            },
            str(TEST_FILE.relative_to(ROOT)): {
                "sha256": sha256_file(
                    TEST_FILE
                )
            },
        },
        "contract_sha256": sha256_file(
            CONTRACT_ROOT
            / "official_shared_runtime_contract.json"
        ),
        "strategy_logic_changed": False,
        "engine_redeveloped": False,
        "canonical_5y_backtest_rerun": False,
        "real_forward_run_performed": False,
        "legacy_oos_state_mutated": False,
        "dashboard_step3_started": False,
        "runtime_commit_at_generation": git_head(),
        "next_action_within_step_2": (
            "Validate the implemented Shared Runtime with "
            "the frozen Forward Seed and a non-mutating "
            "synthetic/dry-run acceptance before the first "
            "official Forward commit."
        ),
    }

    write_json(DECISION_PATH, decision)

    README_PATH.write_text(
        "\n".join(
            [
                "# FD-M3180125-SP500-TOP3-engine",
                "",
                "## Official Shared Runtime Implementation",
                "",
                "Decision:",
                "",
                "```text",
                (
                    "PASS_STEP2_OFFICIAL_SHARED_RUNTIME_"
                    "IMPLEMENTATION"
                ),
                "```",
                "",
                "This implementation remains inside Step 2 "
                "of the fixed three-step plan.",
                "",
                "Implemented runtime boundaries:",
                "",
                *[
                    f"- `{class_name}`"
                    for class_name in required_classes
                ],
                "",
                "Frozen safeguards:",
                "",
                "- No UPTREND strategy change.",
                "- No SIDEWAYS strategy change.",
                "- No Engine redevelopment.",
                "- No Canonical 5Y backtest rerun.",
                "- No real Forward run.",
                "- No legacy OOS state mutation.",
                "- No Dashboard Step 3 work.",
                "- No SIM_END liquidation in Forward.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    manifest = {
        "schema_version": IMPLEMENTATION_VERSION,
        "engine_id": ENGINE_ID,
        "artifact_type": (
            "OFFICIAL_SHARED_RUNTIME_IMPLEMENTATION"
        ),
        "decision": decision["decision"],
        "artifacts": {
            DECISION_PATH.name: {
                "sha256": sha256_file(
                    DECISION_PATH
                )
            },
            README_PATH.name: {
                "sha256": sha256_file(
                    README_PATH
                )
            },
            str(RUNTIME_FILE.relative_to(ROOT)): {
                "sha256": sha256_file(
                    RUNTIME_FILE
                )
            },
            str(TEST_FILE.relative_to(ROOT)): {
                "sha256": sha256_file(
                    TEST_FILE
                )
            },
        },
    }

    write_json(MANIFEST_PATH, manifest)

    print(
        json.dumps(
            {
                "decision": decision["decision"],
                "implementation_root": str(
                    OUTPUT_ROOT.relative_to(ROOT)
                ),
                "runtime_sha256": sha256_file(
                    RUNTIME_FILE
                ),
                "test_sha256": sha256_file(
                    TEST_FILE
                ),
                "decision_sha256": sha256_file(
                    DECISION_PATH
                ),
                "readme_sha256": sha256_file(
                    README_PATH
                ),
                "manifest_sha256": sha256_file(
                    MANIFEST_PATH
                ),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
