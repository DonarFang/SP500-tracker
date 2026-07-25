from pathlib import Path

import pytest

from e1r_engine.live_repository import (
    LiveDailyRepository,
    LiveRepositoryError,
)


def test_daily_commit_is_idempotent_and_conflict_safe(tmp_path: Path) -> None:
    repo = LiveDailyRepository(tmp_path / "live")
    first = repo.commit(
        market_date="2026-07-27",
        payload={"value": 1},
    )
    second = repo.commit(
        market_date="2026-07-27",
        payload={"value": 1},
    )
    assert first == second

    with pytest.raises(LiveRepositoryError):
        repo.commit(
            market_date="2026-07-27",
            payload={"value": 2},
        )


def test_equity_history_is_append_only_by_date(tmp_path: Path) -> None:
    repo = LiveDailyRepository(tmp_path / "live")
    repo.append_equity_point(
        market_date="2026-07-27",
        payload={"total_equity": "100000"},
    )
    repo.append_equity_point(
        market_date="2026-07-27",
        payload={"total_equity": "100000"},
    )

    with pytest.raises(LiveRepositoryError):
        repo.append_equity_point(
            market_date="2026-07-27",
            payload={"total_equity": "100001"},
        )
