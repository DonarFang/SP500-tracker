"""Append-only, track-isolated, atomic JSON storage."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from .contracts import MembershipEvent, MembershipSnapshot
from .hashing import canonical_json_bytes, content_hash


class StorageBoundaryError(RuntimeError):
    pass


class TrackStorage:
    def __init__(self, repo_root: Path, track: str) -> None:
        if track not in {"forward", "live"}:
            raise StorageBoundaryError("track must be explicit")
        self.repo_root = Path(repo_root).resolve()
        self.track = track
        stem = "fw" if track == "forward" else "live"
        self.data_root = self.repo_root / "data" / (stem + "_universe")
        self.export_root = self.repo_root / "exports" / "official" / "FD-M3180125-SP500-TOP3-engine" / track / "universe"

    def _assert_path(self, path: Path) -> None:
        lexical_parent = Path(os.path.abspath(str(path.parent)))
        allowed = [
            Path(os.path.abspath(str(self.data_root))),
            Path(os.path.abspath(str(self.export_root))),
        ]
        if not any(lexical_parent == root or root in lexical_parent.parents for root in allowed):
            raise StorageBoundaryError("cross-track or non-whitelisted path")
        cursor = path.parent
        while cursor != self.repo_root:
            if cursor.exists() and cursor.is_symlink():
                raise StorageBoundaryError("symlink in storage path")
            cursor = cursor.parent

    def atomic_write(self, path: Path, value: Any, immutable: bool = False) -> None:
        self._assert_path(path)
        if path.exists():
            if path.is_symlink():
                raise StorageBoundaryError("refusing symlink target")
            if immutable:
                existing = path.read_bytes()
                desired = canonical_json_bytes(value) + b"\n"
                if existing == desired:
                    return
                raise StorageBoundaryError("immutable artifact conflict")
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix=".uv-", suffix=".tmp", dir=str(path.parent))
        try:
            with os.fdopen(fd, "wb") as handle:
                handle.write(canonical_json_bytes(value) + b"\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, str(path))
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def write_baseline(self, payload: Dict[str, Any]) -> Path:
        path = self.export_root / "baseline" / "LEGACY_BASELINE_PRESERVED.json"
        self.atomic_write(path, payload, immutable=True)
        return path

    def append_event(self, event: MembershipEvent) -> Path:
        path = self.data_root / "events" / event.event_id / ("revision-%03d.json" % event.revision)
        self.atomic_write(path, event.to_dict(), immutable=True)
        return path

    def publish_snapshot(self, snapshot: MembershipSnapshot) -> Path:
        payload = snapshot.to_dict()
        if payload["content_hash"] != snapshot.content_hash:
            raise StorageBoundaryError("snapshot hash mismatch")
        snapshot_path = self.data_root / "snapshots" / (snapshot.snapshot_id + ".json")
        self.atomic_write(snapshot_path, payload, immutable=True)
        pointer = {"snapshot_id": snapshot.snapshot_id, "content_hash": snapshot.content_hash}
        self.atomic_write(self.data_root / "state" / "current.json", pointer)
        return snapshot_path

    def load_events(self) -> List[dict]:
        root = self.data_root / "events"
        if not root.exists():
            return []
        result = []
        for path in sorted(root.glob("*/revision-*.json")):
            result.append(json.loads(path.read_text(encoding="utf-8")))
        return result

    def current_pointer(self) -> Optional[dict]:
        path = self.data_root / "state" / "current.json"
        return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
