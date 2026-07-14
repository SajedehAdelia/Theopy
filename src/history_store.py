import itertools
import re
import threading
import time

_LOCK = threading.Lock()
_HISTORY = []
_ID_COUNTER = itertools.count(1)

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


def _prune_locked() -> None:
    cutoff = time.time() - RETENTION_SECONDS
    while _HISTORY and _HISTORY[0]["timestamp"] < cutoff:
        _HISTORY.pop(0)


def record(tool_name: str, arguments: dict, result: str) -> None:
    """Append a tool call to the rolling 24h history. Thread-safe."""
    entry = {
        "id": next(_ID_COUNTER),
        "domain": _infer_domain(tool_name, result),
        "tool_name": tool_name,
        "arguments": arguments,
        "summary": (result or "")[:160],
        "timestamp": time.time(),
    }
    with _LOCK:
        _HISTORY.append(entry)
        _prune_locked()


def get_grouped() -> dict:
    """Return history entries grouped by domain, most recent first, pruned to 24h."""
    with _LOCK:
        _prune_locked()
        snapshot = list(_HISTORY)

    grouped = {}
    for entry in reversed(snapshot):
        grouped.setdefault(entry["domain"], []).append(entry)
    return grouped


def clear() -> None:
    """Testing helper: wipe all recorded history."""
    with _LOCK:
        _HISTORY.clear()
