import pytest
from src.dispatcher import AgentDispatcher
from src.tests.mocks.ai_scenarios import mcp_simulator


@pytest.mark.asyncio
async def test_fetch_reminders_list_all():
    """Test fetching the full historic list of reminders."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result = await dispatcher.mcp_client.call_tool(
        "fetch_reminders_list", {"pending_only": False}
    )
    assert "All historic reminders" in result


@pytest.mark.asyncio
async def test_treat_reminder_flow():
    """Test that treating a reminder removes it from the pending view."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    # Reset simulator state
    mcp_simulator.treated_reminders.clear()

    # Step 1: Verify both 100 and 101 are pending
    pending_initial = await dispatcher.mcp_client.call_tool(
        "fetch_reminders_list", {"pending_only": True}
    )
    assert "ID: 100" in pending_initial
    assert "ID: 101" in pending_initial

    # Step 2: The AI treats reminder 100
    treat_result = await dispatcher.mcp_client.call_tool(
        "trigger_treat_reminder", {"reminder_id": 100, "treat": True}
    )
    assert "Success: Reminder 100 marked as Treated." in treat_result

    # Step 3: Fetch pending again, verify 100 is gone but 101 remains
    pending_final = await dispatcher.mcp_client.call_tool(
        "fetch_reminders_list", {"pending_only": True}
    )
    assert "ID: 101" in pending_final
    assert "ID: 100" not in pending_final
