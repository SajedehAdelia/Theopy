import pytest
from src.dispatcher import AgentDispatcher
from src.tests.mocks.ai_scenarios import mcp_simulator


@pytest.mark.asyncio
async def test_fetch_sessions_list_match():
    """Test retrieving historic sessions by date."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result = await dispatcher.mcp_client.call_tool(
        "fetch_sessions_list", {"start": "2019-05-20"}
    )
    assert "Session ID: 100" in result
    assert "Session ID: 101" in result


@pytest.mark.asyncio
async def test_fetch_sessions_list_empty():
    """Test safe handling when no sessions exist for a date."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result = await dispatcher.mcp_client.call_tool(
        "fetch_sessions_list", {"start": "2030-01-01"}
    )
    assert "No sessions found" in result


@pytest.mark.asyncio
async def test_multi_step_session_flow():
    """Tests the Start -> Add -> Close multi-step state machine."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    # Strict isolation
    mcp_simulator.active_session_id = None
    mcp_simulator.lines_added = 0

    result_start = await dispatcher.mcp_client.call_tool(
        "trigger_start_session", {"operator_id": 1, "contract_line_id": 2}
    )
    assert "Session 999 started" in result_start

    result_add = await dispatcher.mcp_client.call_tool(
        "trigger_add_session_line", {"intervention_id": 999, "data_json": "{}"}
    )
    assert "Line 1 added" in result_add

    result_close = await dispatcher.mcp_client.call_tool(
        "trigger_close_session", {"intervention_id": 999, "data_json": "{}"}
    )
    assert "successfully closed with 1 lines" in result_close
