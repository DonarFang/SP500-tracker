"""Observer-only E1R canonical JSONL trace writer.

Default state is disabled. This module must never mutate strategy inputs.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
from datetime import date, datetime
from pathlib import Path
from typing import Any


TRACE_SCHEMA_VERSION = "1.0"
_ENABLED_ENV = "E1R_TRACE_ENABLED"
_PATH_ENV = "E1R_TRACE_PATH"


def trace_enabled() -> bool:
    return os.getenv(_ENABLED_ENV, "").strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


def _normalize(value: Any) -> Any:
    if value is None or isinstance(value, (str, bool, int)):
        return value

    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("E1R trace rejects NaN/Infinity")
        return value

    if isinstance(value, (date, datetime)):
        return value.isoformat()

    if isinstance(value, dict):
        return {
            str(key): _normalize(item)
            for key, item in sorted(
                value.items(),
                key=lambda pair: str(pair[0]),
            )
        }

    if isinstance(value, (list, tuple)):
        return [_normalize(item) for item in value]

    if isinstance(value, set):
        normalized = [_normalize(item) for item in value]
        return sorted(
            normalized,
            key=lambda item: json.dumps(
                item,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
                allow_nan=False,
            ),
        )

    raise TypeError(
        "Unsupported E1R trace type: "
        f"{type(value).__name__}"
    )


def canonical_json_bytes(payload: dict[str, Any]) -> bytes:
    return json.dumps(
        _normalize(payload),
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


def emit_trace(
    trace_point_id: str,
    **payload: Any,
) -> None:
    if not trace_enabled():
        return

    output_value = os.getenv(_PATH_ENV, "").strip()
    if not output_value:
        raise RuntimeError(
            "E1R_TRACE_PATH is required when tracing is enabled"
        )

    record = {
        "trace_schema_version": TRACE_SCHEMA_VERSION,
        "trace_point_id": trace_point_id,
        **payload,
    }

    record_hash = hashlib.sha256(
        canonical_json_bytes(record)
    ).hexdigest()

    final_record = {
        **record,
        "record_hash": record_hash,
    }

    output = Path(output_value)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("ab") as handle:
        handle.write(canonical_json_bytes(final_record))
        handle.write(b"\n")
