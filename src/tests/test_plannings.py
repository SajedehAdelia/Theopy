import pytest
from src.dispatcher import AgentDispatcher


@pytest.mark.asyncio
async def test_fetch_planning_dashboard_gare():
    """Test the retrieval of the standard planning dashboard."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result = await dispatcher.mcp_client.call_tool(
        "fetch_planning_dashboard_customers", {"customer_name": "Gare"}
    )
    assert "Customer Dashboard Summary" in result
    assert "Pharmacie de la Gare" in result
    assert "Planned: 2h00" in result


@pytest.mark.asyncio
async def test_fetch_planning_dashboard_groupement():
    """Test the retrieval of planning data for complex Groupement architectures."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result = await dispatcher.mcp_client.call_tool(
        "fetch_planning_dashboard_customers", {"customer_name": "Groupement"}
    )
    assert "Méchant Groupement" in result
    assert "Méchante Pharmacie" in result
    assert "Planned: 10h00" in result


@pytest.mark.asyncio
async def test_fetch_planning_dashboard_operators():
    """Test operator dashboard metrics."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result = await dispatcher.mcp_client.call_tool(
        "fetch_planning_dashboard_operators", {"year": 2019, "week": 21}
    )
    assert "Mathieu Onésime" in result
    assert "Christelle Beauchamp" in result
    assert "Done: 4h30" in result
