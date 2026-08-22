#!/usr/bin/env python3
"""Execute the frozen 119 UV-step-2/Calendar/UV-step-3/4 tests without pytest."""

import importlib.util
import inspect
from pathlib import Path
import re
import sys
import tempfile
import types
import unittest


sys.dont_write_bytecode = True


class Raises:
    def __init__(self, expected, match=None):
        self.expected = expected
        self.match = match
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, traceback):
        if exc_type is None:
            raise AssertionError("expected %r to be raised" % (self.expected,))
        if not issubclass(exc_type, self.expected):
            return False
        if self.match is not None and re.search(self.match, str(exc)) is None:
            raise AssertionError("exception %r does not match %r" % (str(exc), self.match))
        return True


class MonkeyPatch:
    def __init__(self):
        self._undo = []
    def setattr(self, target, name, value):
        old = getattr(target, name)
        self._undo.append((target, name, old))
        setattr(target, name, value)
    def undo(self):
        for target, name, old in reversed(self._undo):
            setattr(target, name, old)


pytest_module = types.ModuleType("pytest")
pytest_module.raises = lambda expected, match=None: Raises(expected, match)
sys.modules["pytest"] = pytest_module


def _forbidden_strategy_call(*args, **kwargs):
    raise AssertionError("UV tests called a production strategy dependency")


def install_capture_stubs_if_needed():
    """Permit isolated UV tests only when the captured legacy package is absent."""
    try:
        import engine  # noqa: F401
        return
    except ModuleNotFoundError:
        pass
    engine_package = types.ModuleType("engine")
    engine_package.__path__ = []
    leader_module = types.ModuleType("engine.leader_ranking")
    leader_module.leader_score = _forbidden_strategy_call
    trade_module = types.ModuleType("engine.trade_decision")
    trade_module.is_broken_trend = _forbidden_strategy_call
    trade_module.trade_action = _forbidden_strategy_call
    sys.modules["engine"] = engine_package
    sys.modules["engine.leader_ranking"] = leader_module
    sys.modules["engine.trade_decision"] = trade_module

    class ForbiddenProductionDependency:
        def __init__(self, *args, **kwargs):
            _forbidden_strategy_call(*args, **kwargs)

    core_stub = types.ModuleType("e1r_engine.core")
    core_stub.E1RCoreEngine = ForbiddenProductionDependency
    signal_stub = types.ModuleType("e1r_engine.uptrend_signal_adapter")
    signal_stub.UptrendSignalAdapter = ForbiddenProductionDependency
    sys.modules["e1r_engine.core"] = core_stub
    sys.modules["e1r_engine.uptrend_signal_adapter"] = signal_stub

FILES = (
    "test_fd_m3180125_universe_contracts.py",
    "test_fd_m3180125_universe_events.py",
    "test_fd_m3180125_universe_identity.py",
    "test_fd_m3180125_universe_isolation.py",
    "test_fd_m3180125_universe_resolver.py",
    "test_fd_m3180125_universe_zero_history_impact.py",
    "test_fd_m3180125_live_calendar.py",
    "test_fd_m3180125_universe_shadow_contract.py",
    "test_fd_m3180125_universe_shadow_forward.py",
    "test_fd_m3180125_universe_shadow_live.py",
    "test_fd_m3180125_universe_shadow_isolation.py",
    "test_fd_m3180125_universe_shadow_zero_impact.py",
    "test_fd_m3180125_universe_production_contract.py",
    "test_fd_m3180125_universe_production_gate.py",
    "test_fd_m3180125_universe_production_forward.py",
    "test_fd_m3180125_universe_production_live.py",
    "test_fd_m3180125_universe_production_isolation.py",
    "test_fd_m3180125_universe_production_zero_impact.py",
)


def load_module(path, index):
    name = "uv4_test_%02d" % index
    spec = importlib.util.spec_from_file_location(name, str(path))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: run_119_pure_assertions.py REPO_OR_STAGE_ROOT")
    root = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(root))
    sys.path.insert(0, str(root / "src"))
    install_capture_stubs_if_needed()
    modules = [load_module(root / "tests" / name, index) for index, name in enumerate(FILES)]
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    for module in modules:
        suite.addTests(loader.loadTestsFromModule(module))
    result = unittest.TestResult()
    suite.run(result)
    total = result.testsRun
    failures = [(str(test), trace) for test, trace in result.failures + result.errors]
    function_count = 0
    for module in modules:
        for name, function in sorted(vars(module).items()):
            if not name.startswith("test_") or not inspect.isfunction(function):
                continue
            function_count += 1
            monkeypatch = MonkeyPatch()
            try:
                with tempfile.TemporaryDirectory(prefix="uv4-test-") as directory:
                    fixtures = {"tmp_path": Path(directory), "monkeypatch": monkeypatch}
                    function(**{parameter: fixtures[parameter] for parameter in inspect.signature(function).parameters})
            except Exception:
                import traceback
                failures.append((module.__name__ + "." + name, traceback.format_exc()))
            finally:
                monkeypatch.undo()
            total += 1
    print("unittest_tests=%d" % result.testsRun)
    print("function_tests=%d" % function_count)
    print("total_tests=%d" % total)
    if failures:
        print("failed=%d" % len(failures))
        for name, trace in failures:
            print("FAIL", name)
            print(trace)
        return 1
    if total != 119:
        print("FAIL expected 119 tests, got %d" % total)
        return 2
    print("PASS_UV_STEP_4_119_OF_119")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
