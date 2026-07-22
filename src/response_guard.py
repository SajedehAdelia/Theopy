import logging
import re

logger = logging.getLogger(__name__)

CLARIFICATION_FALLBACK = (
    "Je n'ai pas pu associer cette demande à une action précise. Pouvez-vous "
    "préciser — par exemple le client, la période, ou le type de données "
    "recherché ?"
)

# Every real MCP tool is named fetch_* or trigger_* (see mcp_server.py / ai_scenarios.py).
# A polished, final answer should never contain a raw identifier like this - whether it's
# wrapped in a JSON blob ({"name": "fetch_inventory", ...}) or narrated in a sentence
# ("Let me call fetch_customer_details tool"). Either shape means the model leaked
# internal plumbing instead of executing the call or giving a real answer.
_TOOL_NAME_PATTERN = re.compile(r"\b(?:fetch|trigger)_[a-z0-9_]+\b")


def _leaks_internal_tool_name(text: str) -> bool:
    return bool(_TOOL_NAME_PATTERN.search(text or ""))


def sanitize_final_answer(text: str) -> str:
    """Guards the final answer returned to the user against leaked tool-call plumbing."""
    if _leaks_internal_tool_name(text):
        logger.warning(
            "Suppressed a leaked tool-call reference from the model: %r", text
        )
        return CLARIFICATION_FALLBACK
    return text
