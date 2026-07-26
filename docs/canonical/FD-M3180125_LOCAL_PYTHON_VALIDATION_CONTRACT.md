# FD-M3180125 Local Python Validation Contract

```text
STATUS: CANONICAL
SCOPE: LOCAL DEVELOPMENT AND VALIDATION
```

## 1. Historical fact

The macOS Command Line Tools interpreter has repeatedly been observed as:

```text
/Library/Developer/CommandLineTools/usr/bin/python3
Python 3.9.6
pytest unavailable
```

The resulting error is:

```text
No module named pytest
```

This is an environment fact, not an Engine failure.

## 2. Frozen rule

Local scripts must not:

```text
hard-code a user-specific virtualenv path
assume pytest is installed
install pytest implicitly
treat missing pytest as a source-code failure
```

Local scripts must use:

```text
scripts/lib/fd_m3180125_python_env.sh
```

to resolve an available interpreter.

## 3. Mandatory local validation

The mandatory local validation baseline is:

```text
py_compile or compileall
pure Python assertions
direct contract validation
AST/source-boundary validation where appropriate
```

## 4. Optional pytest

pytest may run only when:

```text
the resolved interpreter already provides pytest
```

If unavailable, the script must record:

```text
TESTS_SKIPPED_PYTEST_UNAVAILABLE
```

and continue when all frozen non-pytest hard gates pass.

Missing pytest must not be represented as:

```text
test failure
Engine failure
Adapter failure
architecture failure
```

## 5. CI

GitHub Actions may use its explicitly provisioned Python version and install
declared runtime/test dependencies inside the isolated CI job.

The CI environment does not change the local rule above.

## 6. Usage

```bash
source scripts/lib/fd_m3180125_python_env.sh

PYTHON_BIN="$(fd_resolve_python "$PWD" 3 9)"
fd_report_python_environment "$PYTHON_BIN"

"$PYTHON_BIN" -m py_compile path/to/file.py

fd_run_pytest_optional "$PYTHON_BIN" -q tests/target_test.py
```
