#!/usr/bin/env python3
"""Build the versioned adjusted Live price store without activating it.

The production path is fail-closed. It downloads Yahoo-adjusted history in
bounded batches, retries only unresolved symbols, records exact per-symbol
failure evidence, and promotes a complete staging directory only after every
required symbol reaches the same completed US trading session.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import date, datetime, time as wall_time, timedelta, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile
import time
from typing import Dict, Mapping, Optional, Sequence, Tuple
from zoneinfo import ZoneInfo

from e1r_engine.live_calendar import LiveTradingCalendar, load_live_trading_calendar
from update_fd_m3180125_live_prices import _valid_provider_row


LEGACY_ROOT = Path("data/live_prices")
SHADOW_ROOT = Path("data/live_prices_adjusted_v1/live_prices")
EVIDENCE_PATH = Path(
    "exports/official/FD-M3180125-SP500-TOP3-engine/live/automation/"
    "parity/current_adjusted_shadow.json"
)
CALENDAR_PATH = Path("config/live_calendar/us_equity_calendar_v1.0.json")
EXCLUDED_STOCK_SYMBOLS = frozenset({"QQQ", "SOXX", "VIXY"})
INDEX_PROVIDER_SYMBOLS = {
    "SPX": "^GSPC",
    "NDX": "^NDX",
    "SOX": "^SOX",
    "VIX": "^VIX",
}
LIVE_UNIVERSE_STATE = Path("data/live_universe/state/current.json")
LIVE_UNIVERSE_SNAPSHOTS = Path("data/live_universe/snapshots")
EXPECTED_STOCK_COUNT = 491
EXPECTED_TOTAL_COUNT = EXPECTED_STOCK_COUNT + len(INDEX_PROVIDER_SYMBOLS)
SHADOW_MEMBERSHIP_RECONCILIATIONS = {
    "CTRA": {
        "replacement": "VEEV",
        "effective_date": "2026-05-07",
        "source_url": (
            "https://press.spglobal.com/2026-04-30-"
            "Veeva-Systems-Set-to-Join-S-P-500"
        ),
    },
    "EA": {
        "replacement": "FERG",
        "effective_date": "2026-08-05",
        "source_url": (
            "https://press.spglobal.com/2026-07-31-"
            "Ferguson-Enterprises-Set-to-Join-S-P-500-and-"
            "ADI-Global-Distribution-to-Join-S-P-SmallCap-600"
        ),
    },
}
MARKET_TIMEZONE = ZoneInfo("America/New_York")
COMPLETED_SESSION_CUTOFF = wall_time(18, 0)


def _atomic_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    body = (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_bytes(body)
    os.replace(temporary, path)


def _catalogue(legacy_root: Path) -> Tuple[str, ...]:
    symbols = tuple(
        sorted(
            path.stem.upper()
            for path in legacy_root.glob("*.json")
            if path.stem.upper() not in EXCLUDED_STOCK_SYMBOLS
        )
    )
    if not symbols:
        raise RuntimeError("legacy Live catalogue is empty")
    return symbols


def _production_catalogue(
    *, legacy_root: Path, state_path: Path, snapshot_root: Path
) -> Tuple[str, ...]:
    state = json.loads(state_path.read_text(encoding="utf-8"))
    snapshot_id = str(state.get("snapshot_id", ""))
    if not snapshot_id:
        raise RuntimeError("Live Universe current snapshot_id missing")
    snapshot = json.loads(
        (snapshot_root / (snapshot_id + ".json")).read_text(encoding="utf-8")
    )
    if snapshot.get("snapshot_id") != snapshot_id:
        raise RuntimeError("Live Universe snapshot identity mismatch")
    if snapshot.get("track") != "live" or snapshot.get("status") != "EFFECTIVE":
        raise RuntimeError("Live Universe snapshot is not effective")
    membership = snapshot.get("effective_membership")
    if not isinstance(membership, list) or not all(
        isinstance(symbol, str) and symbol for symbol in membership
    ):
        raise RuntimeError("Live Universe effective_membership invalid")
    raw_stocks = set(membership) - set(EXCLUDED_STOCK_SYMBOLS)
    stocks = set(raw_stocks)
    for outgoing, contract in SHADOW_MEMBERSHIP_RECONCILIATIONS.items():
        incoming = str(contract["replacement"])
        if outgoing in stocks:
            if incoming in stocks:
                raise RuntimeError(
                    "Live adjusted shadow reconciliation overlap: "
                    + outgoing
                    + ","
                    + incoming
                )
            stocks.remove(outgoing)
            stocks.add(incoming)
    stocks = sorted(stocks)
    if len(stocks) != EXPECTED_STOCK_COUNT:
        raise RuntimeError(
            "Live adjusted shadow stock count mismatch: "
            "expected=%d, actual=%d" % (EXPECTED_STOCK_COUNT, len(stocks))
        )
    required = tuple(sorted(set(stocks) | set(INDEX_PROVIDER_SYMBOLS)))
    missing = [symbol for symbol in required if not _history_start_path(legacy_root, symbol).is_file()]
    if missing:
        raise RuntimeError(
            "Live adjusted shadow legacy inputs missing: " + ",".join(missing)
        )
    return required


def _history_start_path(legacy_root: Path, symbol: str) -> Path:
    direct = legacy_root / (symbol + ".json")
    if direct.is_file():
        return direct
    for outgoing, contract in SHADOW_MEMBERSHIP_RECONCILIATIONS.items():
        if contract["replacement"] == symbol:
            return legacy_root / (outgoing + ".json")
    return direct


def _first_date(path: Path) -> date:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list) or not payload:
        raise RuntimeError("missing legacy history: %s" % path)
    return date.fromisoformat(str(payload[0]["date"]))


def latest_completed_session(
    *, as_of_utc: datetime, calendar: LiveTradingCalendar
) -> date:
    """Return the latest session safely considered complete at the as-of time."""
    if as_of_utc.tzinfo is None:
        raise ValueError("as_of_utc must be timezone-aware")
    local = as_of_utc.astimezone(MARKET_TIMEZONE)
    candidate = local.date()
    if not (
        calendar.is_session(candidate)
        and local.time().replace(tzinfo=None) >= COMPLETED_SESSION_CUTOFF
    ):
        candidate -= timedelta(days=1)
    while not calendar.is_session(candidate):
        candidate -= timedelta(days=1)
    return candidate


@dataclass(frozen=True)
class FetchRequest:
    symbol: str
    provider_symbol: str
    start_date: date
    end_date: date


def _error_record(
    *, attempt: int, code: str, error: Optional[BaseException] = None
) -> Dict[str, object]:
    message = code if error is None else str(error).strip() or code
    return {
        "attempt": attempt,
        "code": code,
        "exception_type": None if error is None else type(error).__name__,
        "message": message[:2000],
    }


def _rows_from_frame(
    frame: object, *, request: FetchRequest, multi_symbol: bool
) -> Sequence[Mapping[str, object]]:
    if frame is None or getattr(frame, "empty", True):
        return []
    selected = frame
    columns = getattr(frame, "columns", None)
    if multi_symbol and getattr(columns, "nlevels", 1) > 1:
        selected = None
        for level in range(columns.nlevels):
            values = set(str(value) for value in columns.get_level_values(level))
            if request.provider_symbol in values:
                selected = frame.xs(
                    request.provider_symbol, axis=1, level=level, drop_level=True
                )
                break
        if selected is None:
            return []
    elif multi_symbol:
        return []

    rows = []
    for index, source_row in selected.iterrows():

        def scalar(name: str) -> object:
            try:
                value = source_row[name]
            except (KeyError, TypeError):
                return None
            if hasattr(value, "iloc"):
                try:
                    value = value.iloc[0]
                except (IndexError, TypeError):
                    return None
            return value

        normalized = _valid_provider_row(
            market_date=index,
            open_value=scalar("Open"),
            high_value=scalar("High"),
            low_value=scalar("Low"),
            close_value=scalar("Close"),
            volume_value=scalar("Volume"),
        )
        if normalized is None:
            continue
        row_date = date.fromisoformat(str(normalized["date"]))
        if request.start_date <= row_date <= request.end_date:
            rows.append(normalized)
    return rows


class YahooAdjustedBatchProvider:
    """Bounded Yahoo batch fetch with exact single-symbol fallback errors."""

    def __init__(
        self,
        *,
        batch_size: int = 20,
        batch_pause_seconds: float = 1.0,
        threads: int = 4,
    ) -> None:
        if batch_size < 1 or threads < 1:
            raise ValueError("batch_size and threads must be positive")
        self.batch_size = batch_size
        self.batch_pause_seconds = batch_pause_seconds
        self.threads = threads

    def _single(self, request: FetchRequest) -> Sequence[Mapping[str, object]]:
        import yfinance as yf

        frame = yf.Ticker(request.provider_symbol).history(
            start=request.start_date.isoformat(),
            end=(request.end_date + timedelta(days=1)).isoformat(),
            interval="1d",
            auto_adjust=True,
            actions=False,
            raise_errors=True,
        )
        return _rows_from_frame(frame, request=request, multi_symbol=False)

    def fetch_many(
        self, requests: Sequence[FetchRequest], *, attempt: int
    ) -> Tuple[Dict[str, Sequence[Mapping[str, object]]], Dict[str, Dict[str, object]]]:
        import yfinance as yf

        results: Dict[str, Sequence[Mapping[str, object]]] = {}
        errors: Dict[str, Dict[str, object]] = {}
        ordered = list(requests)
        for offset in range(0, len(ordered), self.batch_size):
            chunk = ordered[offset : offset + self.batch_size]
            provider_symbols = [item.provider_symbol for item in chunk]
            try:
                frame = yf.download(
                    provider_symbols,
                    start=min(item.start_date for item in chunk).isoformat(),
                    end=(max(item.end_date for item in chunk) + timedelta(days=1)).isoformat(),
                    interval="1d",
                    auto_adjust=True,
                    actions=False,
                    progress=False,
                    threads=min(self.threads, len(chunk)),
                    group_by="ticker",
                )
                for request in chunk:
                    rows = _rows_from_frame(
                        frame, request=request, multi_symbol=len(chunk) > 1
                    )
                    if rows:
                        results[request.symbol] = rows
            except Exception as error:
                for request in chunk:
                    errors[request.symbol] = _error_record(
                        attempt=attempt,
                        code="BATCH_EXCEPTION",
                        error=error,
                    )

            unresolved = [item for item in chunk if item.symbol not in results]
            for request in unresolved:
                try:
                    rows = self._single(request)
                except Exception as error:
                    errors[request.symbol] = _error_record(
                        attempt=attempt,
                        code="SINGLE_SYMBOL_EXCEPTION",
                        error=error,
                    )
                    continue
                if rows:
                    results[request.symbol] = rows
                    errors.pop(request.symbol, None)
                else:
                    errors[request.symbol] = _error_record(
                        attempt=attempt,
                        code="EMPTY_OR_INVALID_ROWS",
                    )
            if (
                offset + self.batch_size < len(ordered)
                and self.batch_pause_seconds > 0
            ):
                time.sleep(self.batch_pause_seconds)
        return results, errors


class AdjustedShadowBuildError(RuntimeError):
    def __init__(self, evidence: Mapping[str, object]) -> None:
        self.evidence = dict(evidence)
        unavailable = self.evidence.get("unavailable_symbols", [])
        super().__init__("HOLD_ADJUSTED_SHADOW_UNAVAILABLE: " + ",".join(unavailable))


def _validate_rows(
    rows: Sequence[Mapping[str, object]], *, start_date: date, target_market_date: date
) -> Optional[str]:
    if not rows:
        return "EMPTY_OR_INVALID_ROWS"
    try:
        dates = [date.fromisoformat(str(row["date"])) for row in rows]
    except (KeyError, TypeError, ValueError):
        return "INVALID_ROW_DATE"
    if dates != sorted(set(dates)):
        return "NONCANONICAL_ROW_DATES"
    if dates[0] < start_date or dates[0] > start_date + timedelta(days=7):
        return "FIRST_DATE_COVERAGE_MISMATCH expected_from=%s actual=%s" % (
            start_date.isoformat(),
            dates[0].isoformat(),
        )
    if dates[-1] > target_market_date:
        return "LATEST_DATE_AFTER_TARGET expected_at_most=%s actual=%s" % (
            target_market_date.isoformat(),
            dates[-1].isoformat(),
        )
    return None


def _fetch_attempt(
    provider: object,
    requests: Sequence[FetchRequest],
    *,
    attempt: int,
) -> Tuple[Dict[str, Sequence[Mapping[str, object]]], Dict[str, Dict[str, object]]]:
    fetch_many = getattr(provider, "fetch_many", None)
    if callable(fetch_many):
        return fetch_many(requests, attempt=attempt)

    results: Dict[str, Sequence[Mapping[str, object]]] = {}
    errors: Dict[str, Dict[str, object]] = {}
    for request in requests:
        try:
            rows = provider.fetch(
                provider_symbol=request.provider_symbol,
                start_date=request.start_date,
                end_date=request.end_date,
            )
        except Exception as error:
            errors[request.symbol] = _error_record(
                attempt=attempt,
                code="PROVIDER_EXCEPTION",
                error=error,
            )
            continue
        if rows:
            results[request.symbol] = rows
        else:
            errors[request.symbol] = _error_record(
                attempt=attempt,
                code="EMPTY_OR_INVALID_ROWS",
            )
    return results, errors


def _promote_complete_shadow(staging_root: Path, shadow_root: Path) -> None:
    shadow_root.parent.mkdir(parents=True, exist_ok=True)
    backup = shadow_root.parent / (".%s.previous" % shadow_root.name)
    if backup.exists():
        shutil.rmtree(backup)
    had_previous = shadow_root.exists()
    if had_previous:
        os.replace(shadow_root, backup)
    try:
        os.replace(staging_root, shadow_root)
    except Exception:
        if had_previous and backup.exists() and not shadow_root.exists():
            os.replace(backup, shadow_root)
        raise
    if backup.exists():
        shutil.rmtree(backup)


def build_adjusted_shadow(
    *,
    legacy_root: Path,
    shadow_root: Path,
    end_date: date,
    provider: object,
    symbols: Optional[Sequence[str]] = None,
    max_attempts: int = 3,
    retry_delay_seconds: float = 20.0,
    as_of_utc: Optional[datetime] = None,
) -> Dict[str, object]:
    allowed_roots = {
        ("live_prices_adjusted_v1", "live_prices"),
        ("forward_prices_adjusted_v1", "fw_prices"),
    }
    if (shadow_root.parent.name, shadow_root.name) not in allowed_roots:
        raise RuntimeError("adjusted shadow root name mismatch")
    catalogue = tuple(symbols) if symbols is not None else _catalogue(legacy_root)
    if max_attempts < 1:
        raise ValueError("max_attempts must be positive")

    shadow_root.parent.mkdir(parents=True, exist_ok=True)
    staging_root: Optional[Path] = Path(
        tempfile.mkdtemp(prefix=".adjusted-shadow-", dir=str(shadow_root.parent))
    )
    pending = list(catalogue)
    hashes: Dict[str, str] = {}
    latest_dates: Dict[str, str] = {}
    failures: Dict[str, list] = {symbol: [] for symbol in catalogue}
    attempt_summaries = []
    started_at = datetime.now(timezone.utc)
    try:
        for attempt in range(1, max_attempts + 1):
            requests = [
                FetchRequest(
                    symbol=symbol,
                    provider_symbol=INDEX_PROVIDER_SYMBOLS.get(symbol, symbol),
                    start_date=_first_date(_history_start_path(legacy_root, symbol)),
                    end_date=end_date,
                )
                for symbol in pending
            ]
            results, provider_errors = _fetch_attempt(
                provider, requests, attempt=attempt
            )
            unresolved = []
            for request in requests:
                rows = list(results.get(request.symbol, []))
                validation_error = _validate_rows(
                    rows,
                    start_date=request.start_date,
                    target_market_date=end_date,
                )
                if validation_error is not None:
                    unresolved.append(request.symbol)
                    failures[request.symbol].append(
                        provider_errors.get(request.symbol)
                        or _error_record(attempt=attempt, code=validation_error)
                    )
                    continue
                actual_latest = str(rows[-1]["date"])
                if (
                    request.symbol in INDEX_PROVIDER_SYMBOLS
                    and actual_latest != end_date.isoformat()
                ):
                    unresolved.append(request.symbol)
                    failures[request.symbol].append(
                        _error_record(
                            attempt=attempt,
                            code="REQUIRED_INDEX_LATEST_DATE_MISMATCH "
                            "expected=%s actual=%s"
                            % (end_date.isoformat(), actual_latest),
                        )
                    )
                    continue
                assert staging_root is not None
                target = staging_root / (request.symbol + ".json")
                _atomic_json(target, rows)
                hashes[request.symbol] = hashlib.sha256(
                    target.read_bytes()
                ).hexdigest()
                latest_dates[request.symbol] = actual_latest
            attempt_summaries.append(
                {
                    "attempt": attempt,
                    "requested": len(requests),
                    "resolved": len(requests) - len(unresolved),
                    "remaining": len(unresolved),
                    "unavailable_symbols": sorted(unresolved),
                }
            )
            pending = unresolved
            if not pending:
                break
            if attempt < max_attempts and retry_delay_seconds > 0:
                time.sleep(retry_delay_seconds * attempt)

        completed_at = datetime.now(timezone.utc)
        common = {
            "schema_version": "1.1",
            "price_mode": "ADJUSTED_SHADOW_NOT_ACTIVE",
            "auto_adjust": True,
            "symbol_count": len(catalogue),
            "stock_symbol_count": len(set(catalogue) - set(INDEX_PROVIDER_SYMBOLS)),
            "index_symbol_count": len(set(catalogue) & set(INDEX_PROVIDER_SYMBOLS)),
            "excluded_stock_symbols": sorted(EXCLUDED_STOCK_SYMBOLS),
            "membership_reconciliations": [
                {
                    "outgoing": outgoing,
                    **contract,
                }
                for outgoing, contract in sorted(
                    SHADOW_MEMBERSHIP_RECONCILIATIONS.items()
                )
                if contract["replacement"] in catalogue
                and outgoing not in catalogue
            ],
            "latest_requested_date": end_date.isoformat(),
            "latest_market_date": end_date.isoformat(),
            "data_status": "CURRENT" if not pending else "HOLD",
            "catalogue_changed": False,
            "shadow_catalogue_reconciled": any(
                contract["replacement"] in catalogue
                and outgoing not in catalogue
                for outgoing, contract in SHADOW_MEMBERSHIP_RECONCILIATIONS.items()
            ),
            "unavailable_symbols": sorted(pending),
            "ordinary_stale_symbols": sorted(
                symbol
                for symbol, latest in latest_dates.items()
                if symbol not in INDEX_PROVIDER_SYMBOLS
                and latest < end_date.isoformat()
            ),
            "symbol_latest_dates": latest_dates,
            "attempts": attempt_summaries,
            "failure_evidence": {
                symbol: failures[symbol] for symbol in sorted(pending)
            },
            "started_at": started_at.isoformat(),
            "completed_at": completed_at.isoformat(),
            "as_of_utc": (
                as_of_utc.astimezone(timezone.utc).isoformat()
                if as_of_utc is not None
                else None
            ),
            "file_hashes": hashes,
        }
        if pending:
            raise AdjustedShadowBuildError(
                {
                    **common,
                    "decision": "HOLD_PARITY_STEP_2_ADJUSTED_SHADOW_UNAVAILABLE",
                    "successful_symbol_count": len(hashes),
                }
            )

        assert staging_root is not None
        files = sorted(path.stem for path in staging_root.glob("*.json"))
        if files != sorted(catalogue):
            raise RuntimeError("adjusted shadow staging catalogue mismatch")
        _promote_complete_shadow(staging_root, shadow_root)
        staging_root = None
        return {
            **common,
            "decision": "PASS_PARITY_STEP_2_ADJUSTED_SHADOW_BUILT",
            "successful_symbol_count": len(hashes),
        }
    finally:
        if staging_root is not None and staging_root.exists():
            shutil.rmtree(staging_root)


def _parse_as_of_utc(value: str) -> datetime:
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        raise ValueError("--as-of-utc must include a timezone")
    return parsed.astimezone(timezone.utc)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-root", type=Path, default=LEGACY_ROOT)
    parser.add_argument("--shadow-root", type=Path, default=SHADOW_ROOT)
    parser.add_argument("--as-of-utc", default=datetime.now(timezone.utc).isoformat())
    parser.add_argument("--calendar-path", type=Path, default=CALENDAR_PATH)
    parser.add_argument("--evidence-path", type=Path, default=EVIDENCE_PATH)
    parser.add_argument("--batch-size", type=int, default=20)
    parser.add_argument("--max-attempts", type=int, default=3)
    parser.add_argument(
        "--accepted-production",
        action="store_true",
        help="Publish accepted adjusted-price evidence for ACTIVE Live.",
    )
    args = parser.parse_args()

    as_of_utc: Optional[datetime] = None
    target_session: Optional[date] = None
    try:
        as_of_utc = _parse_as_of_utc(args.as_of_utc)
        target_session = latest_completed_session(
            as_of_utc=as_of_utc,
            calendar=load_live_trading_calendar(args.calendar_path),
        )
        symbols = _production_catalogue(
            legacy_root=args.legacy_root,
            state_path=LIVE_UNIVERSE_STATE,
            snapshot_root=LIVE_UNIVERSE_SNAPSHOTS,
        )
        result = build_adjusted_shadow(
            legacy_root=args.legacy_root,
            shadow_root=args.shadow_root,
            # The values are established inside this guarded block.
            end_date=target_session,
            provider=YahooAdjustedBatchProvider(batch_size=args.batch_size),
            symbols=symbols,
            max_attempts=args.max_attempts,
            as_of_utc=as_of_utc,
        )
    except AdjustedShadowBuildError as error:
        result = error.evidence
        _atomic_json(args.evidence_path, result)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 1
    except Exception as error:
        result = {
            "schema_version": "1.1",
            "decision": "HOLD_PARITY_STEP_2_ADJUSTED_SHADOW_EXCEPTION",
            "price_mode": (
                "ADJUSTED_ACCEPTED"
                if args.accepted_production
                else "ADJUSTED_SHADOW_NOT_ACTIVE"
            ),
            "as_of_utc": None if as_of_utc is None else as_of_utc.isoformat(),
            "target_market_date": (
                None if target_session is None else target_session.isoformat()
            ),
            "exception_type": type(error).__name__,
            "message": (str(error).strip() or repr(error))[:4000],
        }
        _atomic_json(args.evidence_path, result)
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 1

    if args.accepted_production:
        result = {
            **result,
            "decision": "PASS_LIVE_ADJUSTED_PRICE_LIBRARY_BUILT",
            "price_mode": "ADJUSTED_ACCEPTED",
            "production_activation": True,
        }
    _atomic_json(args.evidence_path, result)
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
