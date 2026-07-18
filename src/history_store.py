import json
import re
import sqlite3
import threading
import time
from pathlib import Path

_DB_PATH = Path(__file__).resolve().parent / "data" / "history.db"
_LOCK = threading.Lock()

RETENTION_SECONDS = 24 * 60 * 60

DOMAIN_KEYWORDS = (
    ("invoice", "Factures"),
    ("planning", "Plannings"),
    ("session", "Sessions"),
    ("reminder", "Relances"),
)

# Matches the "no data" / failure shape of tool results (e.g. "No sessions found for
# this criteria.", "No data returned.", "Error: Session not found.", "Error executing
# tool: ..."). A tool call that didn't actually return real business data shouldn't be
# filed under its domain tab - it never "answered" that domain, so it belongs in Autre.
_EMPTY_OR_ERROR_PATTERN = re.compile(
    r"^(no\b.*\bfound|no data returned|error\b)", re.IGNORECASE
)


def _is_empty_or_error_result(result: str) -> bool:
    return bool(_EMPTY_OR_ERROR_PATTERN.match((result or "").strip()))


def _infer_domain(tool_name: str, result: str) -> str:
    if _is_empty_or_error_result(result):
        return "Autre"
    lowered = tool_name.lower()
    for keyword, label in DOMAIN_KEYWORDS:
        if keyword in lowered:
            return label
    return "Autre"


def _connect() -> sqlite3.Connection:
    """Persisted on disk (not in-memory) so history survives server restarts,
    the dev auto-reloader, and browser page refreshes."""
    _DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL,
            tool_name TEXT NOT NULL,
            arguments TEXT NOT NULL,
            summary TEXT NOT NULL,
            timestamp REAL NOT NULL
        )
        """
    )
    conn.commit()
    return conn


_conn = _connect()


def _prune_locked() -> None:
    cutoff = time.time() - RETENTION_SECONDS
    _conn.execute("DELETE FROM history WHERE timestamp < ?", (cutoff,))
    _conn.commit()


def record(tool_name: str, arguments: dict, result: str) -> None:
    """Append a tool call to the rolling 24h history. Persisted to disk, thread-safe."""
    domain = _infer_domain(tool_name, result)
    summary = (result or "")[:160]

    with _LOCK:
        _conn.execute(
            "INSERT INTO history (domain, tool_name, arguments, summary, timestamp) "
            "VALUES (?, ?, ?, ?, ?)",
            (domain, tool_name, json.dumps(arguments), summary, time.time()),
        )
        _conn.commit()
        _prune_locked()


def get_grouped() -> dict:
    """Return history entries grouped by domain, most recent first, pruned to 24h."""
    with _LOCK:
        _prune_locked()
        rows = _conn.execute(
            "SELECT id, domain, tool_name, arguments, summary, timestamp "
            "FROM history ORDER BY id DESC"
        ).fetchall()

    grouped = {}
    for entry_id, domain, tool_name, arguments_json, summary, timestamp in rows:
        grouped.setdefault(domain, []).append(
            {
                "id": entry_id,
                "domain": domain,
                "tool_name": tool_name,
                "arguments": json.loads(arguments_json),
                "summary": summary,
                "timestamp": timestamp,
            }
        )
    return grouped


def clear() -> None:
    """Testing helper: wipe all recorded history."""
    with _LOCK:
        _conn.execute("DELETE FROM history")
        _conn.commit()
