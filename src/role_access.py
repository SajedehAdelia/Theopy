"""Client-side mirror of Teepy's mcp_tools/*.py `_ALLOWED_ROLES` tuples.

This is a UX nicety only, not a security boundary: Teepy's own requires_role()
re-checks every call server-side regardless of what's filtered here, so this
map drifting out of sync creates a UX gap (a tool shown that gets denied, or
hidden when it would have been allowed), never a security gap. Keep it in
sync by hand whenever a tool is added, removed, or reassigned on the Teepy side.
"""

TOOL_ALLOWED_ROLES: dict[str, tuple[str, ...]] = {
    # invoices.py
    "fetch_all_invoices_list": ("administrator", "manager", "commercial"),
    "fetch_global_invoice_summary": ("administrator", "manager", "commercial"),
    "fetch_pending_unit_lines": ("administrator", "manager", "commercial"),
    "fetch_mark_invoice_status": ("administrator", "manager", "commercial"),
    "fetch_single_invoice": ("administrator", "manager", "commercial"),
    "trigger_generate_invoices": ("administrator",),
    # customers.py
    "fetch_customers_list": ("administrator", "manager", "commercial"),
    "fetch_single_customer": ("administrator", "manager", "commercial"),
    "fetch_customer_company": ("administrator", "manager", "commercial"),
    "fetch_customer_360": ("administrator", "manager", "commercial"),
    # plannings.py
    "fetch_planning_dashboard_operators": ("administrator", "manager", "operator"),
    "fetch_planning_operators": ("administrator", "manager", "operator"),
    "fetch_planning_dashboard_customers": ("administrator", "manager", "operator"),
    # sessions.py
    "fetch_sessions_list": ("administrator", "manager", "operator", "contractor"),
    "fetch_customer_sessions": ("administrator", "manager", "operator", "contractor"),
    "trigger_start_session": ("administrator", "manager", "operator", "contractor"),
    "fetch_edit_session": ("administrator", "manager", "operator", "contractor"),
    "fetch_current_session": ("administrator", "manager", "operator", "contractor"),
    "fetch_session_lines": ("administrator", "manager", "operator", "contractor"),
    "fetch_session_line_details": (
        "administrator",
        "manager",
        "operator",
        "contractor",
    ),
    "trigger_add_session_line": (
        "administrator",
        "manager",
        "operator",
        "contractor",
    ),
    "trigger_edit_session_line": (
        "administrator",
        "manager",
        "operator",
        "contractor",
    ),
    "fetch_monthly_summary": ("administrator", "manager", "operator", "contractor"),
    "trigger_close_session": ("administrator", "manager", "operator", "contractor"),
    "trigger_letters_add": ("administrator", "manager", "operator", "contractor"),
    "fetch_letter_pdf": ("administrator", "manager", "operator", "contractor"),
    "fetch_preview_pdf": ("administrator", "manager", "operator", "contractor"),
    "fetch_attachment_pdf": ("administrator", "manager", "operator", "contractor"),
    # reminders.py
    "fetch_reminders_list": ("administrator", "manager", "commercial"),
    "trigger_add_reminder": ("administrator", "manager", "commercial"),
    "trigger_edit_reminder": ("administrator", "manager", "commercial"),
    "trigger_treat_reminder": ("administrator", "manager", "commercial"),
}


def filter_tools_for_role(tools: list[dict], role: str | None) -> list[dict]:
    """Keep only the tools this role is allowed to use. A tool missing from
    TOOL_ALLOWED_ROLES (a forgotten update) or a missing role is excluded by
    default - deny-by-default, matching Teepy's own requires_role()."""
    if role is None:
        return []
    return [tool for tool in tools if role in TOOL_ALLOWED_ROLES.get(tool["name"], ())]
