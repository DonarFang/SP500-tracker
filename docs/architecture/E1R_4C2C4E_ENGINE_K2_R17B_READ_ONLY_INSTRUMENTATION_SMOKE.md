# E1R K2 R17B Trace Instrumentation Architecture

## Runtime switches

- `E1R_TRACE_ENABLED=1`
- `E1R_TRACE_PATH=/path/to/trace.jsonl`

Tracing is disabled by default.

## Test invocation contract

Run from repository root:

`PYTHONPATH="$PWD" python3 -m unittest discover -s tests -p 'test_e1r_trace_smoke.py' -v`

## Safety contract

- Observer-only trace guards.
- No candidate or order mutation.
- No pending-queue mutation.
- No cash or holdings mutation by trace code.
- Canonical JSONL records.
- SHA-256 per record.
- Non-finite floating-point values rejected.

## Equivalence boundary

R17B proves static AST equivalence and helper behavior.
R17B-1 must prove trace-enabled versus trace-disabled strategy and
portfolio equivalence over frozen golden dates.
