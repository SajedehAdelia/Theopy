import pytest
from src.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_ask_no_message(client):
    response = client.post('/ask', json={})
    assert response.status_code == 400


def test_teepy_connection(client):
    response = client.post('/ask', json={"message": "Show sessions for Pharmacie de la Gare"})
    assert response.status_code == 200
    assert "DISPLAY_DATA" in response.json["action"]