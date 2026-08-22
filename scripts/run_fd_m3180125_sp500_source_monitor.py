#!/usr/bin/env python3
"""Run SA-step-1 official-source monitoring only."""

import argparse
import json
import sys
from pathlib import Path

from e1r_engine.source_automation.monitor import DEFAULT_LANDING_URL, OfficialSourceMonitor


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--landing-url", default=DEFAULT_LANDING_URL)
    parser.add_argument("--max-pages", type=int, default=10)
    args = parser.parse_args()
    result = OfficialSourceMonitor(Path(args.repo_root)).run(args.landing_url, max_pages=args.max_pages)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["status"] == "PASS_SOURCE_SCAN" else 2


if __name__ == "__main__":
    sys.exit(main())
