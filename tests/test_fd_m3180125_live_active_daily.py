import ast
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def test_active_live_workflow_contract():
    workflow=(ROOT/".github/workflows/live-track-daily.yml").read_text()
    runner=(ROOT/"scripts/run_fd_m3180125_live_daily.py").read_text()
    production=(ROOT/"src/e1r_engine/live_production.py").read_text()
    ast.parse(runner); ast.parse(production)
    assert "cron: '30 0,2,4,8 * * 2-6'" in workflow
    assert "workflow_dispatch:" in workflow
    assert "workflow_run:" not in workflow
    assert "resolve_fd_m3180125_latest_completed_session.py" in workflow
    assert "--expected-latest-market-date" in workflow
    assert 'steps.latest_session.outputs.date' in workflow
    assert "commit_active_daily" in production
    assert "ACTIVE_RECOMMENDATION_ONLY" in production
    assert "commit_active_daily" in runner
    assert "PASS_LIVE_ACTIVE_NO_NEW_DATE" in runner
    assert "for run_market_date in pending_dates" in runner


def test_active_runner_never_uses_unactivated_composition():
    runner = (
        ROOT / "scripts/run_fd_m3180125_live_daily.py"
    ).read_text()
    composition = (
        ROOT / "src/e1r_engine/live_composition.py"
    ).read_text()

    assert "compose_active_live_production" in runner
    assert "compose_unactivated_live_production" not in runner

    tree = ast.parse(composition)
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }
    active = functions["compose_active_live_production"]
    active_source = ast.get_source_segment(
        composition,
        active,
    )
    assert active_source is not None
    assert "initialize_unactivated=False" in active_source
    assert "load_official_live_opening" in active_source


def test_active_and_unactivated_lifecycles_are_separate():
    composition = (
        ROOT / "src/e1r_engine/live_composition.py"
    ).read_text()
    tree = ast.parse(composition)
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, ast.FunctionDef)
    }

    unactivated = ast.get_source_segment(
        composition,
        functions["compose_unactivated_live_production"],
    )
    active = ast.get_source_segment(
        composition,
        functions["compose_active_live_production"],
    )

    assert unactivated is not None
    assert active is not None
    assert "LiveOpeningState()" in unactivated
    assert "initialize_unactivated=True" in unactivated
    assert "load_official_live_opening" not in unactivated
    assert "load_official_live_opening" in active
    assert "initialize_unactivated=False" in active


def test_active_commit_passes_reconciliation_as_of_date_v2() -> None:
    production = (
        ROOT / "src/e1r_engine/live_production.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(production)

    active = None
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.FunctionDef)
            and node.name == "commit_active_daily"
        ):
            active = node
            break

    assert active is not None

    calls = [
        node
        for node in ast.walk(active)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "reconcile_recommendations"
        )
    ]

    assert len(calls) == 1

    keywords = {
        keyword.arg: keyword.value
        for keyword in calls[0].keywords
        if keyword.arg is not None
    }

    assert ast.unparse(
        keywords["as_of_date"]
    ) == "result.market_date"
