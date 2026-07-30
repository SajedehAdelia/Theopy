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
    try:
        conn.execute("ALTER TABLE history ADD COLUMN question TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists - safe to ignore (idempotent migration).
    try:
        conn.execute("ALTER TABLE history ADD COLUMN user_id INTEGER")
    except sqlite3.OperationalError:
        pass  # Column already exists - safe to ignore (idempotent migration).
    try:
        conn.execute("ALTER TABLE history ADD COLUMN full_answer TEXT")
    except sqlite3.OperationalError:
        pass  # Column already exists - safe to ignore (idempotent migration).
    conn.commit()
    return conn


_conn = _connect()


def _prune_locked() -> None:
    cutoff = time.time() - RETENTION_SECONDS
    _conn.execute("DELETE FROM history WHERE timestamp < ?", (cutoff,))
    _conn.commit()


def record(
    tool_name: str,
    arguments: dict,
    result: str,
    question: str = None,
    user_id: int = None,
) -> None:
    """Append a tool call to the rolling 24h history. Persisted to disk, thread-safe.
    `question` is the original natural-language message that triggered this tool
    call, so the UI can show "what you asked" alongside "what came back". `user_id`
    is the logged-in Theopy user this call belongs to - get_grouped() only ever
    returns a caller's own entries, so different users never see each other's
    history."""
    domain = _infer_domain(tool_name, result)
    summary = (result or "")[:160]

    with _LOCK:
        _conn.execute(
            "INSERT INTO history (domain, tool_name, arguments, summary, timestamp, question, user_id) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                domain,
                tool_name,
                json.dumps(arguments),
                summary,
                time.time(),
                question,
                user_id,
            ),
        )
        _conn.commit()
        _prune_locked()


def get_grouped(user_id: int) -> dict:
    """Return this user's own history entries grouped by domain, most recent
    first, pruned to 24h. Entries recorded before user_id existed (NULL) are
    never matched by the `= ?` comparison, so they're excluded for everyone
    rather than attributed to the wrong person."""
    with _LOCK:
        _prune_locked()
        rows = _conn.execute(
            "SELECT id, domain, tool_name, arguments, summary, timestamp, question, full_answer "
            "FROM history WHERE user_id = ? ORDER BY id DESC",
            (user_id,),
        ).fetchall()

    grouped = {}
    for (
        entry_id,
        domain,
        tool_name,
        arguments_json,
        summary,
        timestamp,
        question,
        full_answer,
    ) in rows:
        grouped.setdefault(domain, []).append(
            {
                "id": entry_id,
                "domain": domain,
                "tool_name": tool_name,
                "arguments": json.loads(arguments_json),
                "summary": summary,
                "timestamp": timestamp,
                "question": question,
                "full_answer": full_answer,
            }
        )
    return grouped


FINAL_ANSWER_ATTACH_WINDOW_SECONDS = 30


def attach_final_answer(user_id: int, question: str, full_answer: str) -> None:
    """Attach the guarded, LLM-synthesized answer actually shown to the user
    to the row(s) this turn just recorded (one per tool call it made), so
    recalling from history renders the same Markdown table as the live
    answer instead of the raw pre-synthesis tool text stored in `summary`.

    Scoped to a short recent window and keyed on (user_id, question) so it
    can never touch an older, identical question asked earlier within the
    same 24h retention period. Best-effort and silent: if the turn made no
    tool calls (nothing recorded to attach to), this is a no-op - history
    is a convenience side-effect, not the source of truth for the answer."""
    if not question:
        return
    cutoff = time.time() - FINAL_ANSWER_ATTACH_WINDOW_SECONDS
    with _LOCK:
        _conn.execute(
            "UPDATE history SET full_answer = ? "
            "WHERE user_id = ? AND question = ? AND full_answer IS NULL AND timestamp >= ?",
            (full_answer, user_id, question, cutoff),
        )
        _conn.commit()


def clear() -> None:
    """Testing helper: wipe all recorded history."""
    with _LOCK:
        _conn.execute("DELETE FROM history")
        _conn.commit()
