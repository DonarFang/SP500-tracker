"""Deterministic, fail-closed S&P DJI announcement monitor for SA-step-1."""

import hashlib
import html
import io
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple
from urllib.parse import urljoin, urlparse, urlunparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

from .contracts import CandidateChange, SourceDetection


PARSER_VERSION = "SA1-1.0.0"
DEFAULT_LANDING_URL = "https://www.spglobal.com/spdji/en/media-center/news-announcements/"
ALLOWED_HOSTS = {"spglobal.com", "www.spglobal.com"}
ALLOWED_PATH_PREFIX = "/spdji/en/"


class SourceMonitorError(RuntimeError):
    pass


class _LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.links: List[Tuple[str, str]] = []
        self._href: Optional[str] = None
        self._parts: List[str] = []

    def handle_starttag(self, tag: str, attrs: Sequence[Tuple[str, Optional[str]]]) -> None:
        if tag.lower() == "a":
            self._href = dict(attrs).get("href")
            self._parts = []

    def handle_data(self, data: str) -> None:
        if self._href is not None:
            self._parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._parts).strip()))
            self._href = None
            self._parts = []


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_url(url: str) -> str:
    parsed = urlparse(url)
    host = (parsed.hostname or "").lower()
    if parsed.scheme != "https" or host not in ALLOWED_HOSTS:
        raise SourceMonitorError("SOURCE_DOMAIN_NOT_ALLOWED")
    if not parsed.path.startswith(ALLOWED_PATH_PREFIX):
        raise SourceMonitorError("SOURCE_PATH_NOT_ALLOWED")
    return urlunparse(("https", host, parsed.path, "", parsed.query, ""))


def _atomic_write(path: Path, data: bytes, immutable: bool = False) -> None:
    cursor = path.parent
    while not cursor.exists() and cursor != cursor.parent:
        cursor = cursor.parent
    if cursor.is_symlink():
        raise SourceMonitorError("SOURCE_STORAGE_SYMLINK")
    if path.exists():
        if path.is_symlink():
            raise SourceMonitorError("SOURCE_STORAGE_SYMLINK")
        if immutable:
            if path.read_bytes() == data:
                return
            raise SourceMonitorError("IMMUTABLE_SOURCE_CONFLICT")
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".sa1-", suffix=".tmp", dir=str(path.parent))
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, str(path))
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def _normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


def _is_target_title(title: str) -> bool:
    lower = _normalize_text(title).lower()
    if "s&p 500" not in lower:
        return False
    excluded = (
        "equal weight", "scored & screened", "esg", "capped", "consultation",
        "methodology", "buyback", "dividend aristocrats",
    )
    return not any(term in lower for term in excluded)


def _listing_api_url(landing_url: str, landing_data: bytes, page_number: int) -> str:
    text = landing_data.decode("utf-8", errors="replace")
    match = re.search(
        r'data-actionurl=["\'](?P<path>[^"\']*get-pr-news-announcements-solr-json\.dot)["\']',
        text,
        re.I,
    )
    if not match:
        raise SourceMonitorError("OFFICIAL_LISTING_ENDPOINT_NOT_DISCOVERED")
    base = _canonical_url(urljoin(landing_url, match.group("path")))
    return base + "?contentSubType=indexNews&pageNumber=%d" % page_number


def _parse_listing(data: bytes) -> Dict[str, object]:
    text = data.decode("utf-8", errors="replace")
    start = text.find("{")
    if start < 0:
        raise SourceMonitorError("OFFICIAL_LISTING_JSON_INVALID")
    try:
        value = json.loads(text[start:])
    except (TypeError, ValueError) as exc:
        raise SourceMonitorError("OFFICIAL_LISTING_JSON_INVALID") from exc
    if not isinstance(value, dict) or not isinstance(value.get("resultData"), list):
        raise SourceMonitorError("OFFICIAL_LISTING_SCHEMA_INVALID")
    return value


def _extract_pdf_text(data: bytes) -> str:
    try:
        from pypdf import PdfReader  # type: ignore
    except ImportError as exc:
        raise SourceMonitorError("PDF_TEXT_EXTRACTOR_UNAVAILABLE") from exc
    reader = PdfReader(io.BytesIO(data))
    return "\n".join((page.extract_text() or "") for page in reader.pages)


def _extract_document_text(data: bytes, content_type: str) -> str:
    if "pdf" in content_type.lower() or data.startswith(b"%PDF"):
        return _extract_pdf_text(data)
    decoded = data.decode("utf-8", errors="replace")
    decoded = re.sub(r"<script\b[^>]*>.*?</script>", " ", decoded, flags=re.I | re.S)
    decoded = re.sub(r"<style\b[^>]*>.*?</style>", " ", decoded, flags=re.I | re.S)
    return _normalize_text(re.sub(r"<[^>]+>", " ", decoded))


_REPLACE_PATTERN = re.compile(
    r"(?P<add_company>[A-Z][A-Za-z0-9&.,'’()\- ]{1,100}?)\s*"
    r"\((?:NYSE|NASDAQ|NASD|NYSE\s*AMERICAN)\s*:\s*(?P<add_symbol>[A-Z0-9.\-]+)\)\s*"
    r"will\s+replace\s+"
    r"(?P<del_company>[A-Z][A-Za-z0-9&.,'’()\- ]{1,100}?)\s*"
    r"\((?:NYSE|NASDAQ|NASD|NYSE\s*AMERICAN)\s*:\s*(?P<del_symbol>[A-Z0-9.\-]+)\)\s*"
    r"in\s+the\s+S&P\s*500(?P<tail>.{0,220})",
    re.I,
)


def extract_candidates(text: str) -> List[CandidateChange]:
    normalized = _normalize_text(text)
    results: List[CandidateChange] = []
    seen = set()
    for match in _REPLACE_PATTERN.finditer(normalized):
        tail = match.group("tail")
        date_match = re.search(
            r"effective\s+(?P<timing>prior\s+to\s+the\s+(?:opening|open)|after\s+the\s+close)?"
            r"(?:\s+of\s+trading)?(?:\s+on)?\s*(?P<date>(?:Monday|Tuesday|Wednesday|Thursday|Friday),?\s+"
            r"[A-Z][a-z]+\s+\d{1,2}(?:,\s*\d{4})?)",
            tail,
            re.I,
        )
        effective_date = date_match.group("date") if date_match else ""
        timing = date_match.group("timing") if date_match and date_match.group("timing") else ""
        pairs = [
            ("ADD", match.group("add_company"), match.group("add_symbol"), match.group("del_company"), match.group("del_symbol")),
            ("REMOVE", match.group("del_company"), match.group("del_symbol"), match.group("add_company"), match.group("add_symbol")),
        ]
        for action, company, symbol, other_company, other_symbol in pairs:
            key = (action, symbol.upper(), other_symbol.upper())
            if key in seen:
                continue
            seen.add(key)
            results.append(CandidateChange(
                action=action,
                company_name=company.strip(" ,.-"),
                official_symbol=symbol.upper(),
                replaced_company_name=other_company.strip(" ,.-"),
                replaced_official_symbol=other_symbol.upper(),
                effective_date_text=effective_date,
                effective_timing_text=timing,
                evidence_text=match.group(0)[:500],
            ))
    return results


class OfficialSourceMonitor:
    def __init__(
        self,
        repo_root: Path,
        fetch: Optional[Callable[[str], Tuple[bytes, str]]] = None,
        now: Optional[Callable[[], datetime]] = None,
    ) -> None:
        self.repo_root = Path(repo_root).resolve()
        self.root = self.repo_root / "data" / "sp500_source_monitor"
        self.fetch = fetch or self._fetch
        self.now = now or (lambda: datetime.now(timezone.utc))

    @staticmethod
    def _fetch(url: str) -> Tuple[bytes, str]:
        browser_user_agent = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0 Safari/537.36"
        )
        curl = shutil.which("curl")
        if curl:
            with tempfile.TemporaryDirectory(prefix="sa1-fetch-") as temporary:
                body_path = Path(temporary) / "body"
                type_path = Path(temporary) / "content-type"
                command = [
                    curl, "--location", "--fail", "--silent", "--show-error",
                    "--max-time", "60", "--retry", "2", "--retry-delay", "1",
                    "--user-agent", browser_user_agent,
                    "--header", "Accept: text/html,application/json,application/pdf,*/*;q=0.8",
                    "--output", str(body_path),
                    "--write-out", "%{content_type}",
                    url,
                ]
                result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
                if result.returncode == 0 and body_path.is_file():
                    content_type = result.stdout.decode("ascii", errors="replace").strip()
                    return body_path.read_bytes(), content_type or "application/octet-stream"
                curl_code = "SOURCE_CURL_%d" % result.returncode
        else:
            curl_code = "SOURCE_CURL_UNAVAILABLE"

        request = Request(url, headers={
            "User-Agent": browser_user_agent,
            "Accept": "text/html,application/json,application/pdf,*/*;q=0.8",
        })
        last_code = "SOURCE_FETCH_FAILED"
        for attempt in range(3):
            try:
                with urlopen(request, timeout=60) as response:
                    status = getattr(response, "status", 200)
                    if status != 200:
                        raise SourceMonitorError("SOURCE_HTTP_%s" % status)
                    return response.read(), response.headers.get("Content-Type", "application/octet-stream")
            except HTTPError as exc:
                last_code = "SOURCE_HTTP_%s" % exc.code
            except (URLError, TimeoutError, OSError):
                last_code = "SOURCE_NETWORK_FAILED"
            if attempt < 2:
                time.sleep(1 + attempt)
        raise SourceMonitorError(last_code + "+" + curl_code)

    def _write_scan_failure(self, fetched_at: str, code: str, source_url: str) -> Path:
        payload = {
            "status": "SOURCE_HOLD",
            "fetched_at_utc": fetched_at,
            "source_url": source_url,
            "failure_codes": [code],
            "parser_version": PARSER_VERSION,
        }
        stamp = fetched_at.replace(":", "").replace("-", "")
        path = self.root / "scans" / (stamp + "-HOLD.json")
        _atomic_write(path, (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode(), immutable=True)
        _atomic_write(self.root / "state" / "current.json", (json.dumps(payload, sort_keys=True, separators=(",", ":")) + "\n").encode())
        return path

    def run(self, landing_url: str = DEFAULT_LANDING_URL, max_pages: int = 10) -> Dict[str, object]:
        fetched_at = self.now().astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
        try:
            landing_url = _canonical_url(landing_url)
            landing_data, landing_type = self.fetch(landing_url)
            if "html" not in landing_type.lower():
                raise SourceMonitorError("LANDING_CONTENT_TYPE_INVALID")
            if max_pages < 1 or max_pages > 50:
                raise SourceMonitorError("LISTING_PAGE_LIMIT_INVALID")
            targets: Dict[str, Tuple[str, str]] = {}
            listing_hashes: List[str] = []
            listing_rows = 0
            for page_number in range(1, max_pages + 1):
                api_url = _listing_api_url(landing_url, landing_data, page_number)
                listing_data, listing_type = self.fetch(api_url)
                if "json" not in listing_type.lower() and "text" not in listing_type.lower():
                    raise SourceMonitorError("OFFICIAL_LISTING_CONTENT_TYPE_INVALID")
                listing = _parse_listing(listing_data)
                digest = _sha256(listing_data)
                listing_hashes.append(digest)
                _atomic_write(self.root / "listings" / (digest + ".json"), listing_data, immutable=True)
                rows = listing["resultData"]
                listing_rows += len(rows)
                for row in rows:
                    if not isinstance(row, dict):
                        raise SourceMonitorError("OFFICIAL_LISTING_SCHEMA_INVALID")
                    title = _normalize_text(str(row.get("title", "")))
                    href = str(row.get("link", ""))
                    if _is_target_title(title) and href:
                        target = _canonical_url(urljoin(landing_url, href))
                        targets[target] = (title, str(row.get("date", "")))
                pagination = listing.get("pagination", {})
                total_pages = pagination.get("totalPages") if isinstance(pagination, dict) else None
                if not rows or (isinstance(total_pages, int) and page_number >= total_pages):
                    break
            if listing_rows == 0:
                raise SourceMonitorError("OFFICIAL_LISTING_EMPTY")
        except Exception as exc:
            code = str(exc) if isinstance(exc, SourceMonitorError) else "SOURCE_FETCH_FAILED"
            self._write_scan_failure(fetched_at, code, landing_url)
            return {"status": "SOURCE_HOLD", "failure_codes": [code], "detections": 0}

        detections: List[SourceDetection] = []
        failures: List[str] = []
        for source_url, target_metadata in sorted(targets.items()):
            title, published_text = target_metadata
            try:
                data, content_type = self.fetch(source_url)
                digest = _sha256(data)
                source_id = "SPD-JI-" + digest[:20]
                suffix = ".pdf" if ("pdf" in content_type.lower() or data.startswith(b"%PDF")) else ".html"
                raw_relative = "documents/%s/source%s" % (source_id, suffix)
                _atomic_write(self.root / raw_relative, data, immutable=True)
                text = _extract_document_text(data, content_type)
                candidates = extract_candidates(text)
                status = "DETECTED" if candidates else "SOURCE_HOLD"
                failure_codes = [] if candidates else ["TARGET_DOCUMENT_PARSE_INCOMPLETE"]
                detection = SourceDetection(
                    source_id=source_id,
                    source_url=source_url,
                    source_document_sha256=digest,
                    fetched_at_utc=fetched_at,
                    published_text=published_text,
                    title=title,
                    content_type=content_type,
                    parser_version=PARSER_VERSION,
                    status=status,
                    candidates=candidates,
                    failure_codes=failure_codes,
                    raw_document_path=raw_relative,
                )
                payload = (json.dumps(detection.to_dict(), sort_keys=True, separators=(",", ":")) + "\n").encode()
                _atomic_write(self.root / "detections" / source_id / "detection.json", payload, immutable=True)
                detections.append(detection)
                failures.extend(failure_codes)
            except Exception as exc:
                failures.append(str(exc) if isinstance(exc, SourceMonitorError) else "TARGET_FETCH_FAILED")

        status = "PASS_SOURCE_SCAN" if not failures else "SOURCE_HOLD"
        summary = {
            "status": status,
            "fetched_at_utc": fetched_at,
            "landing_url": landing_url,
            "landing_sha256": _sha256(landing_data),
            "target_count": len(targets),
            "listing_row_count": listing_rows,
            "listing_hashes": listing_hashes,
            "detection_count": len(detections),
            "candidate_count": sum(len(item.candidates) for item in detections),
            "source_ids": sorted(item.source_id for item in detections),
            "failure_codes": sorted(set(failures)),
            "parser_version": PARSER_VERSION,
        }
        stamp = fetched_at.replace(":", "").replace("-", "")
        encoded = (json.dumps(summary, sort_keys=True, separators=(",", ":")) + "\n").encode()
        _atomic_write(self.root / "scans" / (stamp + ".json"), encoded, immutable=True)
        _atomic_write(self.root / "state" / "current.json", encoded)
        return summary
