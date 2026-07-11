# E1R K2 R17B Read-Only Instrumentation Smoke

Decision: PASS_READ_ONLY_INSTRUMENTATION_SMOKE

## Scope

- Added all 11 frozen observer-only trace hooks.
- Trace is disabled by default.
- No full 5Y run was performed.
- No golden-date backtest was performed.

## Environment corrections

1. System Python did not provide pytest.
2. Direct test-file execution did not include the repository root in
   Python's module path.
3. Final validation uses standard-library unittest discovery from the
   repository root with `PYTHONPATH` explicitly set.

## Static equivalence

The original `run_stateful_simulation` AST equals the instrumented AST
after removing trace-only guard blocks:

`True`

## Validation

- Python compile: PASS
- Standard-library unittest: PASS
- Disabled tracing writes no file: PASS
- Enabled tracing writes one canonical JSONL record: PASS
- SHA-256 verification: PASS
- Eleven trace hooks inserted exactly once: PASS

## Next stage

4C-2C-4E-ENGINE-K2-R17B-1-GOLDEN-DATE-TRACE-EQUIVALENCE-SMOKE
