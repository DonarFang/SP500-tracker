"""Fail-closed SA-step-2 verification; it never creates Membership Events."""

import hashlib
import json
import math
import os
import re
import tempfile
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence


VERIFIER_VERSION = "SA2-1.0.0"
SYMBOL_RE = re.compile(r"^[A-Z0-9][A-Z0-9.\-]{0,14}$")
DATE_RE = re.compile(
    r"^(Monday|Tuesday|Wednesday|Thursday|Friday),?\s+"
    r"(January|February|March|April|May|June|July|August|September|October|November|December)\s+"
    r"(\d{1,2})(?:,\s*(\d{4}))?$",
    re.I,
)


class VerificationError(RuntimeError):
    pass


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def _atomic_write(path: Path, data: bytes, immutable: bool = False) -> None:
    cursor = path.parent
    while not cursor.exists() and cursor != cursor.parent:
        cursor = cursor.parent
    if cursor.is_symlink() or (path.exists() and path.is_symlink()):
        raise VerificationError("VERIFICATION_STORAGE_SYMLINK")
    if path.exists() and path.stat().st_nlink != 1:
        raise VerificationError("VERIFICATION_STORAGE_HARDLINK")
    if immutable and path.exists():
        if path.read_bytes() == data:
            return
        raise VerificationError("IMMUTABLE_VERIFICATION_CONFLICT")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".sa2-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, str(path))
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _effective_date(text: str, published_text: str) -> str:
    match = DATE_RE.match(text.strip())
    if not match:
        raise VerificationError("EFFECTIVE_DATE_UNRESOLVED")
    try:
        published = parsedate_to_datetime(published_text)
    except (TypeError, ValueError, OverflowError) as exc:
        raise VerificationError("PUBLISHED_DATE_UNRESOLVED") from exc
    year = int(match.group(4) or published.year)
    parsed = datetime.strptime(
        "%s %s %s" % (match.group(2), match.group(3), year), "%B %d %Y"
    ).date()
    if parsed.strftime("%A").lower() != match.group(1).lower():
        raise VerificationError("EFFECTIVE_WEEKDAY_MISMATCH")
    if parsed < published.date():
        raise VerificationError("EFFECTIVE_DATE_BEFORE_PUBLICATION")
    return parsed.isoformat()


class SymbolResolver:
    def __init__(self, mapping_path: Path) -> None:
        payload = json.loads(Path(mapping_path).read_text(encoding="utf-8"))
        if payload.get("schema_version") != "1.0" or payload.get("provider") != "Yahoo Finance":
            raise VerificationError("PROVIDER_MAPPING_SCHEMA_INVALID")
        self.mapping_hash = _sha256(_canonical_json(payload))
        self.rows: Dict[str, Dict[str, Any]] = {}
        yahoo_seen = set()
        for row in payload.get("non_identity_mappings", []):
            required = {
                "security_id", "spdj_symbol", "engine_symbol", "yahoo_symbol",
                "exchange", "share_class", "currency", "valid_from", "status",
                "evidence", "evidence_sha256",
            }
            if not required.issubset(row) or row.get("status") != "ACTIVE":
                raise VerificationError("PROVIDER_MAPPING_ROW_INVALID")
            if _sha256(row["evidence"].encode()) != row["evidence_sha256"]:
                raise VerificationError("PROVIDER_MAPPING_EVIDENCE_HASH_INVALID")
            official = row["spdj_symbol"]
            yahoo = row["yahoo_symbol"]
            if official in self.rows or yahoo in yahoo_seen or official == yahoo:
                raise VerificationError("PROVIDER_MAPPING_CONFLICT")
            if not SYMBOL_RE.match(official) or not SYMBOL_RE.match(yahoo):
                raise VerificationError("PROVIDER_MAPPING_SYMBOL_INVALID")
            self.rows[official] = dict(row)
            yahoo_seen.add(yahoo)

    def resolve(self, official_symbol: str, effective_date: Optional[str] = None) -> Dict[str, Any]:
        symbol = official_symbol.strip().upper()
        if not SYMBOL_RE.match(symbol):
            raise VerificationError("OFFICIAL_SYMBOL_INVALID")
        if symbol in self.rows:
            row = dict(self.rows[symbol])
            if effective_date and (
                effective_date < row["valid_from"]
                or (row.get("valid_to") and effective_date > row["valid_to"])
            ):
                raise VerificationError("PROVIDER_MAPPING_NOT_DATE_VALID")
            row["mapping_mode"] = "EXPLICIT_EVIDENCED"
            return row
        return {
            "security_id": None,
            "spdj_symbol": symbol,
            "engine_symbol": symbol,
            "yahoo_symbol": symbol,
            "exchange": None,
            "share_class": None,
            "currency": "USD",
            "valid_from": None,
            "valid_to": None,
            "status": "PENDING_PROVIDER_CONFIRMATION",
            "evidence": "Identity mapping confirmed only if Yahoo price probe passes",
            "evidence_sha256": None,
            "mapping_mode": "IDENTITY_PENDING_PROBE",
        }


def _valid_prices(rows: Sequence[Dict[str, Any]]) -> bool:
    for row in rows:
        close = row.get("close")
        date = row.get("date")
        if (
            isinstance(date, str) and re.match(r"^\d{4}-\d{2}-\d{2}$", date)
            and isinstance(close, (int, float)) and math.isfinite(float(close))
            and float(close) > 0
        ):
            return True
    return False


class SourceVerifier:
    def __init__(
        self,
        repo_root: Path,
        provider_probe: Callable[[str], Sequence[Dict[str, Any]]],
        now: Optional[Callable[[], datetime]] = None,
    ) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.output_root = self.repo_root / "data" / "sp500_source_verification"
        self.provider_probe = provider_probe
        self.now = now or (lambda: datetime.now(timezone.utc))
        self.resolver = SymbolResolver(
            self.repo_root / "config" / "sp500_source_automation" / "provider_symbol_map.json"
        )

    def _accepted_verification(self, source_id: str) -> Optional[Dict[str, Any]]:
        root = self.output_root / "verifications" / source_id
        if not root.is_dir() or root.is_symlink():
            return None
        accepted = []
        for path in sorted(root.glob("SA2-*.json")):
            if path.is_symlink() or not path.is_file() or path.stat().st_nlink != 1:
                raise VerificationError("VERIFICATION_STORAGE_LINK_UNSAFE")
            try:
                payload = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as exc:
                raise VerificationError("EXISTING_VERIFICATION_INVALID") from exc
            if (
                payload.get("source_id") == source_id
                and payload.get("status") == "VERIFIED_NO_EVENT"
                and payload.get("provider") == "Yahoo Finance"
                and payload.get("provider_mapping_sha256") == self.resolver.mapping_hash
                and payload.get("membership_event_created") is False
                and payload.get("price_data_written") is False
                and payload.get("production_invoked") is False
            ):
                accepted.append(payload)
        if not accepted:
            return None
        def semantic(value: Dict[str, Any]) -> Dict[str, Any]:
            entries = []
            for row in value.get("entries", []):
                identity = row.get("identity", {})
                entries.append({
                    "action": row.get("action"),
                    "company_name": row.get("company_name"),
                    "status": row.get("status"),
                    "spdj_symbol": identity.get("spdj_symbol"),
                    "engine_symbol": identity.get("engine_symbol"),
                    "yahoo_symbol": identity.get("yahoo_symbol"),
                    "mapping_mode": identity.get("mapping_mode"),
                    "mapping_status": identity.get("status"),
                    "currency": identity.get("currency"),
                })
            return {
                "source_id": value.get("source_id"),
                "status": value.get("status"),
                "effective_date": value.get("effective_date"),
                "provider": value.get("provider"),
                "provider_mapping_sha256": value.get("provider_mapping_sha256"),
                "entries": entries,
                "membership_event_created": value.get("membership_event_created"),
                "price_data_written": value.get("price_data_written"),
                "production_invoked": value.get("production_invoked"),
            }

        canonical = _canonical_json(semantic(accepted[0]))
        if any(_canonical_json(semantic(value)) != canonical for value in accepted[1:]):
            raise VerificationError("CONFLICTING_ACCEPTED_VERIFICATIONS")
        return min(accepted, key=lambda value: (str(value.get("verified_at_utc", "")), str(value.get("verification_id", ""))))

    def verify_detection(self, detection_path: Path) -> Dict[str, Any]:
        detection_path = Path(detection_path).resolve()
        failures: List[str] = []
        entries: List[Dict[str, Any]] = []
        try:
            detection = json.loads(detection_path.read_text(encoding="utf-8"))
            source_id = detection["source_id"]
            if detection.get("status") != "DETECTED" or not source_id.startswith("SPD-JI-"):
                raise VerificationError("DETECTION_NOT_ELIGIBLE")
            accepted = self._accepted_verification(source_id)
            if accepted is not None:
                _atomic_write(self.output_root / "state" / "current.json", _canonical_json(accepted))
                return accepted
            if not str(detection.get("source_url", "")).startswith("https://press.spglobal.com/"):
                raise VerificationError("OFFICIAL_SOURCE_AUTHORITY_INVALID")
            raw = self.repo_root / "data" / "sp500_source_monitor" / detection["raw_document_path"]
            if not raw.is_file() or raw.is_symlink() or raw.stat().st_nlink != 1:
                raise VerificationError("RAW_SOURCE_DOCUMENT_INVALID")
            if _sha256(raw.read_bytes()) != detection.get("source_document_sha256"):
                raise VerificationError("RAW_SOURCE_HASH_MISMATCH")
            candidates = detection.get("candidates")
            if not isinstance(candidates, list) or len(candidates) != 2:
                raise VerificationError("CHANGE_PAIR_INCOMPLETE")
            actions = {row.get("action") for row in candidates}
            if actions != {"ADD", "REMOVE"}:
                raise VerificationError("CHANGE_PAIR_ACTION_INVALID")
            add = next(row for row in candidates if row["action"] == "ADD")
            remove = next(row for row in candidates if row["action"] == "REMOVE")
            if (
                add.get("replaced_official_symbol") != remove.get("official_symbol")
                or remove.get("replaced_official_symbol") != add.get("official_symbol")
            ):
                raise VerificationError("CHANGE_PAIR_NOT_RECIPROCAL")
            if add.get("official_symbol") == remove.get("official_symbol"):
                raise VerificationError("CHANGE_PAIR_IDENTITY_CONFLICT")
            if any(not row.get("company_name") for row in candidates):
                raise VerificationError("COMPANY_IDENTITY_INCOMPLETE")
            dates = {
                _effective_date(row.get("effective_date_text", ""), detection.get("published_text", ""))
                for row in candidates
            }
            if len(dates) != 1:
                raise VerificationError("EFFECTIVE_DATE_CONFLICT")
            effective_date = next(iter(dates))
            if any("prior to the opening" not in row.get("effective_timing_text", "").lower() for row in candidates):
                raise VerificationError("EFFECTIVE_TIMING_UNRESOLVED")
            for row in candidates:
                official = row.get("official_symbol", "")
                mapping = None
                try:
                    mapping = self.resolver.resolve(official, effective_date)
                    prices = list(self.provider_probe(mapping["yahoo_symbol"]))
                    if not _valid_prices(prices):
                        raise VerificationError("YAHOO_PRICE_UNAVAILABLE")
                    mapping["status"] = "VERIFIED"
                    mapping["probe_bar_count"] = len(prices)
                    mapping["price_evidence_sha256"] = _sha256(_canonical_json(prices))
                    mapping["probe_latest_date"] = max(
                        row["date"] for row in prices
                        if isinstance(row.get("date"), str)
                    )
                    entries.append({
                        "action": row["action"],
                        "company_name": row.get("company_name", ""),
                        "identity": mapping,
                        "status": "VERIFIED",
                        "failure_codes": [],
                    })
                except Exception as exc:
                    code = str(exc) if isinstance(exc, VerificationError) else "YAHOO_PROVIDER_PROBE_FAILED"
                    failures.append("%s:%s" % (official or "UNKNOWN", code))
                    entries.append({
                        "action": row.get("action"),
                        "company_name": row.get("company_name", ""),
                        "official_symbol": official,
                        "attempted_yahoo_symbol": (
                            mapping.get("yahoo_symbol") if mapping else None
                        ),
                        "status": "ENTRY_QUARANTINE",
                        "failure_codes": [code],
                        "manual_action": (
                            "Confirm the security identity and Yahoo Finance symbol; "
                            "then add or correct an evidenced, date-valid mapping and rerun SA-step-2."
                        ),
                    })
        except Exception as exc:
            source_id = locals().get("source_id", "UNKNOWN")
            effective_date = None
            code = str(exc) if isinstance(exc, VerificationError) else "DETECTION_SCHEMA_INVALID"
            failures.append(code)

        status = "VERIFIED_NO_EVENT" if not failures else "VERIFICATION_HOLD"
        payload = {
            "schema_version": "1.0",
            "verifier_version": VERIFIER_VERSION,
            "status": status,
            "source_id": source_id,
            "verified_at_utc": self.now().astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "effective_date": effective_date,
            "provider": "Yahoo Finance",
            "provider_mapping_sha256": self.resolver.mapping_hash,
            "entries": entries,
            "failure_codes": sorted(set(failures)),
            "manual_intervention_required": bool(failures),
            "membership_event_created": False,
            "price_data_written": False,
            "production_invoked": False,
        }
        digest = _sha256(_canonical_json(payload))
        payload["verification_id"] = "SA2-" + digest[:20]
        data = _canonical_json(payload)
        _atomic_write(
            self.output_root / "verifications" / source_id / (payload["verification_id"] + ".json"),
            data,
            immutable=True,
        )
        _atomic_write(self.output_root / "state" / "current.json", data)
        if failures:
            _atomic_write(self.output_root / "alerts" / (payload["verification_id"] + ".json"), data, immutable=True)
        return payload

    def run_all(self) -> Dict[str, Any]:
        root = self.repo_root / "data" / "sp500_source_monitor" / "detections"
        selected = []
        seen = set()
        duplicate_count = 0
        for path in sorted(root.glob("*/detection.json")):
            value = json.loads(path.read_text(encoding="utf-8"))
            rows = [
                {
                    "action": row.get("action"),
                    "company_name": row.get("company_name"),
                    "official_symbol": row.get("official_symbol"),
                    "replaced_company_name": row.get("replaced_company_name"),
                    "replaced_official_symbol": row.get("replaced_official_symbol"),
                    "effective_date_text": row.get("effective_date_text"),
                    "effective_timing_text": row.get("effective_timing_text"),
                }
                for row in value.get("candidates", [])
            ]
            key = _sha256(_canonical_json({
                "source_url": value.get("source_url"),
                "published_text": value.get("published_text"),
                "title": value.get("title"),
                "candidates": rows,
            }))
            if key in seen:
                duplicate_count += 1
                continue
            seen.add(key)
            selected.append(path)
        results = [self.verify_detection(path) for path in selected]
        status = "PASS_SA2_VERIFICATION" if results and all(x["status"] == "VERIFIED_NO_EVENT" for x in results) else "HOLD_SA2_VERIFICATION"
        return {
            "status": status,
            "semantic_change_count": len(results),
            "duplicate_detection_count": duplicate_count,
            "verification_count": len(results),
            "results": results,
        }
