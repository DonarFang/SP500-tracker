#!/usr/bin/env python3
"""Contract-level entry point for an unactivated Live dry run.

The caller must supply a concrete Engine composition. This script does not
invent a market-data provider or activate the opening date.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--runtime-root",
        default=(
            "exports/official/"
            "FD-M3180125-SP500-TOP3-engine/live"
        ),
    )
    parser.add_argument(
        "--initialize-unactivated",
        action="store_true",
    )
    args = parser.parse_args()

    from e1r_engine.live_persistence import LiveRuntimeRepository

    repository = LiveRuntimeRepository(Path(args.runtime_root))

    if args.initialize_unactivated:
        repository.initialize_unactivated()
        print(
            json.dumps(
                {
                    "decision": (
                        "PASS_LIVE_RUNTIME_INITIALIZED_UNACTIVATED"
                    ),
                    "runtime_root": str(
                        Path(args.runtime_root)
                    ),
                    "opening_activated": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    raise SystemExit(
        "STOP: production Engine/data composition must be supplied by "
        "the later accepted Live workflow; opening remains unactivated"
    )


if __name__ == "__main__":
    raise SystemExit(main())
