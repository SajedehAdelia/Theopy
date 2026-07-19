from src.role_access import TOOL_ALLOWED_ROLES, filter_tools_for_role

TOOLS = [
    {"name": "fetch_customer_company"},
    {"name": "fetch_sessions_list"},
    {"name": "trigger_generate_invoices"},
]


def test_filter_tools_for_role_keeps_only_allowed_tools():
    # commercial: allowed on customers, not on sessions or admin-only invoicing.
    result = filter_tools_for_role(TOOLS, "commercial")

    assert [tool["name"] for tool in result] == ["fetch_customer_company"]


def test_filter_tools_for_role_administrator_sees_everything_mapped():
    result = filter_tools_for_role(TOOLS, "administrator")

    assert {tool["name"] for tool in result} == {
        "fetch_customer_company",
        "fetch_sessions_list",
        "trigger_generate_invoices",
    }


def test_filter_tools_for_role_operator_gets_sessions_only():
    result = filter_tools_for_role(TOOLS, "operator")

    assert [tool["name"] for tool in result] == ["fetch_sessions_list"]


def test_filter_tools_for_role_none_role_returns_nothing():
    assert filter_tools_for_role(TOOLS, None) == []


def test_filter_tools_for_role_unmapped_tool_name_is_excluded():
    result = filter_tools_for_role(
        [{"name": "some_future_tool_nobody_mapped_yet"}], "administrator"
    )

    assert result == []


def test_every_mapped_tool_has_at_least_one_role():
    for tool_name, roles in TOOL_ALLOWED_ROLES.items():
        assert roles, f"{tool_name} maps to an empty role tuple"
