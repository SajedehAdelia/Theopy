from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from src.mcp_client import TeepyMCPClient


@pytest.fixture(autouse=True)
def inject_mcp_simulator():
    """Shadows conftest's autouse fixture of the same name: that one replaces
    call_tool() with a scripted double, but this file tests the real
    call_tool()/get_available_tools() implementation directly."""
    yield


def _fake_tool(name):
    return SimpleNamespace(
        name=name, description="desc", inputSchema={"type": "object", "properties": {}}
    )


@pytest.mark.asyncio
async def test_call_tool_passes_theopy_user_id_as_meta():
    client = TeepyMCPClient()
    client._session = AsyncMock()
    client._session.call_tool.return_value = SimpleNamespace(
        content=[SimpleNamespace(text="Result text")]
    )
    client.current_user_id = 100

    await client.call_tool("fetch_customer_company", {"customer_name": "Gare"})

    client._session.call_tool.assert_called_once_with(
        "fetch_customer_company",
        {"customer_name": "Gare"},
        meta={"theopy_user_id": 100},
    )


@pytest.mark.asyncio
async def test_call_tool_with_no_user_id_sends_no_meta():
    """Defense in depth: if a turn somehow runs with no logged-in user_id set,
    the call must NOT silently claim an identity - Teepy denies calls with no
    meta by default, which is the correct outcome here."""
    client = TeepyMCPClient()
    client._session = AsyncMock()
    client._session.call_tool.return_value = SimpleNamespace(
        content=[SimpleNamespace(text="Result text")]
    )

    await client.call_tool("fetch_customer_company", {"customer_name": "Gare"})

    client._session.call_tool.assert_called_once_with(
        "fetch_customer_company", {"customer_name": "Gare"}, meta=None
    )


@pytest.mark.asyncio
async def test_get_available_tools_filters_by_current_user_role():
    client = TeepyMCPClient()
    client._session = AsyncMock()
    client._session.list_tools.return_value = SimpleNamespace(
        tools=[
            _fake_tool("fetch_customer_company"),
            _fake_tool("fetch_sessions_list"),
        ]
    )
    client.current_user_role = "operator"

    tools = await client.get_available_tools()

    assert [tool["name"] for tool in tools] == ["fetch_sessions_list"]


@pytest.mark.asyncio
async def test_get_available_tools_with_no_role_returns_nothing():
    client = TeepyMCPClient()
    client._session = AsyncMock()
    client._session.list_tools.return_value = SimpleNamespace(
        tools=[_fake_tool("fetch_customer_company")]
    )

    tools = await client.get_available_tools()

    assert tools == []
