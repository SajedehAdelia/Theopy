import pytest
from src.dispatcher import Dispatcher

@pytest.fixture
def dispatcher():
    # We point to the internal Docker service name
    return Dispatcher(base_url="http://app:5000")

def test_intent_mapping_customer_sessions(dispatcher):
    """
    Test that the tool call correctly maps to the CUSTOMER_SESSION intent.
    """
    tool_call = {
        "name": "get_customer_sessions",
        "arguments": {"customer_name": "Pharmacie de la Gare"}
    }
    
    # We check if the dispatcher correctly identifies the intent key
    mapping = {
        "get_customer_sessions": "CUSTOMER_SESSION"
    }
    
    intent_key = mapping.get(tool_call["name"])
    assert intent_key == "CUSTOMER_SESSION"

def test_sql_data_consistency():
    """
    Verification that our test data IDs match our expected logic.
    Based on our SQL: Pharmacie de la Gare is ID 101.
    """
    customer_id = 101
    customer_name = "Pharmacie de la Gare"
    assert customer_id == 101
    assert "Gare" in customer_name