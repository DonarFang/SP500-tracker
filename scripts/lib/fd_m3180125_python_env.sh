#!/usr/bin/env bash
# FD-M3180125 canonical local Python environment resolver.
#
# Contract:
# - Never hard-code a user-specific venv path.
# - Never install pytest or other dependencies implicitly.
# - Prefer an explicitly supplied FD_M3180125_PYTHON.
# - Otherwise discover a usable interpreter deterministically.
# - pytest is optional unless a task explicitly freezes it as mandatory
#   and a suitable environment is already available.
# - Pure-stdlib validation remains the mandatory local fallback.

set -euo pipefail

fd_python_version_ok() {
  local candidate="$1"
  local min_major="${2:-3}"
  local min_minor="${3:-9}"

  "$candidate" - "$min_major" "$min_minor" <<'PY' >/dev/null 2>&1
import sys
major = int(sys.argv[1])
minor = int(sys.argv[2])
raise SystemExit(0 if sys.version_info >= (major, minor) else 1)
PY
}

fd_resolve_python() {
  local repo="${1:-$(pwd)}"
  local min_major="${2:-3}"
  local min_minor="${3:-9}"
  local candidate=""
  local resolved=""

  local candidates=()

  if [[ -n "${FD_M3180125_PYTHON:-}" ]]; then
    candidates+=("$FD_M3180125_PYTHON")
  fi

  candidates+=(
    "$repo/.venv/bin/python"
    "$repo/venv/bin/python"
    "$repo/.python/bin/python"
  )

  for name in python3.13 python3.12 python3.11 python3.10 python3; do
    if command -v "$name" >/dev/null 2>&1; then
      candidates+=("$(command -v "$name")")
    fi
  done

  candidates+=(
    "/opt/homebrew/bin/python3.13"
    "/opt/homebrew/bin/python3.12"
    "/opt/homebrew/bin/python3.11"
    "/opt/homebrew/bin/python3"
    "/usr/local/bin/python3.13"
    "/usr/local/bin/python3.12"
    "/usr/local/bin/python3.11"
    "/usr/local/bin/python3"
    "/usr/bin/python3"
  )

  local seen="|"
  for candidate in "${candidates[@]}"; do
    [[ -n "$candidate" ]] || continue
    [[ -x "$candidate" ]] || continue

    resolved="$(
      "$candidate" - <<'PY' 2>/dev/null || true
import os, sys
print(os.path.realpath(sys.executable))
PY
    )"
    [[ -n "$resolved" ]] || continue

    if [[ "$seen" == *"|$resolved|"* ]]; then
      continue
    fi
    seen+="$resolved|"

    if fd_python_version_ok "$resolved" "$min_major" "$min_minor"; then
      printf '%s\n' "$resolved"
      return 0
    fi
  done

  printf 'STOP: no Python >= %s.%s found\n' \
    "$min_major" "$min_minor" >&2
  return 1
}

fd_python_has_module() {
  local python_bin="$1"
  local module="$2"

  "$python_bin" - "$module" <<'PY' >/dev/null 2>&1
import importlib.util
import sys
raise SystemExit(
    0 if importlib.util.find_spec(sys.argv[1]) else 1
)
PY
}

fd_report_python_environment() {
  local python_bin="$1"

  "$python_bin" - <<'PY'
import json
import os
import platform
import sys
import importlib.util

print(json.dumps({
    "python_executable": os.path.realpath(sys.executable),
    "python_version": platform.python_version(),
    "pytest_available": (
        importlib.util.find_spec("pytest") is not None
    ),
    "policy": {
        "hard_coded_venv_allowed": False,
        "implicit_dependency_install_allowed": False,
        "pytest_local_hard_gate": False,
        "mandatory_fallback": [
            "py_compile_or_compileall",
            "pure_python_assertions",
            "direct_contract_validation",
        ],
    },
}, indent=2, sort_keys=True))
PY
}

fd_run_pytest_optional() {
  local python_bin="$1"
  shift

  if fd_python_has_module "$python_bin" pytest; then
    "$python_bin" -m pytest "$@"
    return $?
  fi

  printf '%s\n' \
    "TESTS_SKIPPED_PYTEST_UNAVAILABLE"
  printf '%s\n' \
    "This is not a code failure under the canonical local validation contract."
  return 0
}
