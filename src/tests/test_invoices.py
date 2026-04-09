import pytest
from src.app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_invoice_real_database_flow(client):
    payload = {"message": "Show me the invoices for Pharmacie de la Gare"}
    response = client.post('/ask', json=payload)

    assert response.status_code == 200
    
    data = response.get_json()
    
    assert data["action"] == "DISPLAY_DATA"
    assert data["intent"] == "get_invoice_summary"
    
    invoice_list = data["data"]["invoices"]
    
    available_dates = [inv['date'] for inv in invoice_list]
    assert "2019-02-01" in available_dates
    assert "2023-01-15" in available_dates

    invoice_2019 = next(inv for inv in invoice_list if inv["date"] == "2019-02-01")
    assert invoice_2019["total_with_taxes"] == "927.00"
    
    print("Logic Check: Summary dates and totals match the database state.")