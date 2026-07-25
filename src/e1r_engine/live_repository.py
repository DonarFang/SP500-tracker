"""Independent persistence for Live daily results."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
from typing import Mapping


class LiveRepositoryError(ValueError):
    pass


def canonical_json(payload: Mapping[str, object]) -> bytes:
    return (
        json.dumps(
            payload,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            default=str,
        )
        + "\n"
    ).encode("utf-8")


class LiveDailyRepository:
    def __init__(self, root: Path) -> None:
        self.root = Path(root)

    def commit(
        self,
        *,
        market_date: str,
        payload: Mapping[str, object],
    ) -> str:
        body = canonical_json(payload)
        digest = hashlib.sha256(body).hexdigest()
        target = self.root / "daily" / market_date / "daily_result.json"

        if target.exists():
            existing = target.read_bytes()
            if existing == body:
                return digest
            raise LiveRepositoryError(
                f"conflicting Live daily commit for {market_date}"
            )

        target.parent.mkdir(parents=True, exist_ok=True)
        temporary = target.with_suffix(".tmp")
        temporary.write_bytes(body)
        os.replace(temporary, target)
        return digest

    def append_equity_point(
        self,
        *,
        market_date: str,
        payload: Mapping[str, object],
    ) -> None:
        path = self.root / "history" / "equity_curve.json"
        path.parent.mkdir(parents=True, exist_ok=True)

        rows = []
        if path.exists():
            rows = json.loads(path.read_text(encoding="utf-8"))
            if not isinstance(rows, list):
                raise LiveRepositoryError("equity history must be a list")

        existing = [
            row
            for row in rows
            if isinstance(row, dict)
            and row.get("market_date") == market_date
        ]

        normalized = dict(payload)
        normalized["market_date"] = market_date

        if existing:
            if existing[0] == normalized:
                return
            raise LiveRepositoryError(
                f"conflicting Live equity point for {market_date}"
            )

        rows.append(normalized)
        rows.sort(key=lambda row: str(row["market_date"]))
        path.write_text(
            json.dumps(
                rows,
                ensure_ascii=False,
                indent=2,
                sort_keys=True,
                default=str,
            )
            + "\n",
            encoding="utf-8",
        )
