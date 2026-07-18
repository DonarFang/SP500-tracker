#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "FD-M3180125 Official Forward runner entrypoint. "
            "This entrypoint is intentionally locked until "
            "formal providers and explicit execution authorization "
            "are supplied."
        )
    )

    parser.add_argument(
        "--contract-check",
        action="store_true",
        help=(
            "Verify that the orchestrator module imports and "
            "that Official execution remains locked."
        ),
    )

    parser.add_argument(
        "--execute-official-forward",
        action="store_true",
        help=(
            "Reserved flag. It does not execute until a separately "
            "reviewed production composition root is installed."
        ),
    )

    return parser


def main() -> int:
    args = build_parser().parse_args()

    from e1r_engine.forward_orchestrator import (
        ForwardMarketSnapshotBuilder,
        ForwardRegimeProvider,
        ForwardStrategyInputBuilder,
        OfficialForwardCatchupRunner,
    )

    if args.execute_official_forward:
        print(
            json.dumps(
                {
                    "decision":
                        "HOLD_OFFICIAL_FORWARD_EXECUTION_LOCKED",
                    "reason": (
                        "Production composition root has not been "
                        "authorized. No repository was initialized, "
                        "no commit_day call was made, and no official "
                        "artifact was written."
                    ),
                    "repository_initialized": False,
                    "commit_day_called": False,
                    "official_artifacts_written": False,
                },
                indent=2,
            )
        )
        return 2

    if not args.contract_check:
        print(
            "Use --contract-check. Official execution is locked.",
            file=sys.stderr,
        )
        return 2

    print(
        json.dumps(
            {
                "decision":
                    "PASS_FORWARD_ORCHESTRATOR_CONTRACT_CHECK",
                "components": [
                    ForwardRegimeProvider.__name__,
                    ForwardMarketSnapshotBuilder.__name__,
                    ForwardStrategyInputBuilder.__name__,
                    OfficialForwardCatchupRunner.__name__,
                ],
                "official_forward_execution_locked": True,
                "repository_initialized": False,
                "commit_day_called": False,
                "official_artifacts_written": False,
            },
            indent=2,
        )
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
