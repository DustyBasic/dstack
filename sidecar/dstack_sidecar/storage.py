"""
storage.py -- storage abstractions for the sidecar.

v0.1 ships with in-memory storage as the default. Adopters can subclass
Storage or provide a drop-in replacement for persistent backends (SQLite,
Redis, claude-mem adapter, etc.).

See skills/fractal_mem_cache/reference/claude_mem-adapter.md for claude-mem
integration guidance.

Rights: All rights reserved. Source-available for review and evaluation.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Iterable, List, Optional


class Storage(ABC):
    """Abstract storage interface for observation persistence.

    The sidecar's MemCache uses in-memory dicts by default. For persistence
    across process boundaries, implement this interface and pass an instance
    to MemCache (or wire it up in your own adapter layer).

    The v0.1 MemCache does not yet call into Storage -- it operates on its
    own in-memory dicts. Storage is here as the extension point for adopters
    who need to persist observations beyond process lifetime.
    """

    @abstractmethod
    def put(self, key: str, value: Dict[str, Any]) -> None:
        """Persist a single observation by key."""
        ...

    @abstractmethod
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """Retrieve a single observation by key; return None if not found."""
        ...

    @abstractmethod
    def iter_all(self) -> Iterable[Dict[str, Any]]:
        """Iterate all stored observations."""
        ...

    @abstractmethod
    def delete(self, key: str) -> None:
        """Remove an observation. NOTE: T0-tier observations must not be
        deleted in a fractal_mem_cache-compliant adopter -- T0 is
        append-only. This method exists for T2/T1 eviction and for
        adopter-specific management only."""
        ...

    @abstractmethod
    def size(self) -> int:
        """Return the count of stored observations."""
        ...


class InMemoryStorage(Storage):
    """Default in-memory storage. Dictionary-backed; no persistence.

    Usable for development, testing, and short-lived process use cases.
    Not suitable for production agents that need continuity across restarts.
    """

    def __init__(self):
        self._data: Dict[str, Dict[str, Any]] = {}

    def put(self, key: str, value: Dict[str, Any]) -> None:
        self._data[key] = value

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        return self._data.get(key)

    def iter_all(self) -> Iterable[Dict[str, Any]]:
        return iter(self._data.values())

    def delete(self, key: str) -> None:
        self._data.pop(key, None)

    def size(self) -> int:
        return len(self._data)


class SQLiteStorage(Storage):
    """Skeleton SQLite storage. v0.1 stub.

    Provides the Storage interface over a local SQLite database. Adopters
    who need persistence can instantiate this with a file path. The schema
    is minimal -- one table, one JSON-encoded payload per row.

    For production claude-mem integration, use claude-mem's own storage
    and wire it via the claude-mem-adapter guidance in the skill docs
    rather than bolting this SQLite schema on top.
    """

    def __init__(self, db_path: str):
        import sqlite3
        import json
        self._sqlite3 = sqlite3
        self._json = json
        self._db_path = db_path
        self._conn = sqlite3.connect(db_path)
        self._conn.execute(
            "CREATE TABLE IF NOT EXISTS observations ("
            " key TEXT PRIMARY KEY, "
            " payload TEXT NOT NULL, "
            " created_at REAL NOT NULL"
            ")"
        )
        self._conn.commit()

    def put(self, key: str, value: Dict[str, Any]) -> None:
        import time
        self._conn.execute(
            "INSERT OR REPLACE INTO observations (key, payload, created_at) VALUES (?, ?, ?)",
            (key, self._json.dumps(value), time.time()),
        )
        self._conn.commit()

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        cur = self._conn.execute(
            "SELECT payload FROM observations WHERE key = ?",
            (key,),
        )
        row = cur.fetchone()
        if row is None:
            return None
        return self._json.loads(row[0])

    def iter_all(self) -> Iterable[Dict[str, Any]]:
        cur = self._conn.execute("SELECT payload FROM observations")
        for row in cur:
            yield self._json.loads(row[0])

    def delete(self, key: str) -> None:
        self._conn.execute(
            "DELETE FROM observations WHERE key = ?",
            (key,),
        )
        self._conn.commit()

    def size(self) -> int:
        cur = self._conn.execute("SELECT COUNT(*) FROM observations")
        return int(cur.fetchone()[0])

    def close(self) -> None:
        self._conn.close()
