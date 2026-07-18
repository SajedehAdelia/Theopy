import pytest
from src.dispatcher import AgentDispatcher


@pytest.mark.asyncio
async def test_fetch_invoices_list_gare():
    """Test retrieving invoices filtered for Pharmacie de la Gare."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result = await dispatcher.mcp_client.call_tool(
        "fetch_all_invoices_list", {"customer_name": "Gare"}
    )
    assert "Invoices List:" in result
    assert "Invoice ID: 101" in result
    assert "Pharmacie de la Gare" in result


@pytest.mark.asyncio
async def test_fetch_invoices_list_soleil():
    """Test retrieving invoices filtered for Pharmacie du Soleil."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result = await dispatcher.mcp_client.call_tool(
        "fetch_all_invoices_list", {"customer_name": "Soleil"}
    )
    assert "Invoice ID: 102" in result
    assert "Pharmacie du Soleil" in result
    assert "Gare" not in result


@pytest.mark.asyncio
async def test_fetch_invoices_list_empty():
    """Test safe handling when the AI searches for a non-existent pharmacy."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result = await dispatcher.mcp_client.call_tool(
        "fetch_all_invoices_list", {"customer_name": "Inconnue"}
    )
    assert "No invoices found for this criteria." in result


@pytest.mark.asyncio
async def test_mark_invoice_status():
    """Test state mutation for paying an invoice."""
    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    result_paid = await dispatcher.mcp_client.call_tool(
        "fetch_mark_invoice_status", {"invoice_id": 101, "is_paid": True}
    )
    assert "Success: Invoice 101 has been marked as Paid." in result_paid
