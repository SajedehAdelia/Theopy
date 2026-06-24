import pytest
from unittest.mock import AsyncMock, patch
from src.app import app


@pytest.fixture
def client():
    """Setup a test client for the Flask application."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test the DevOps supervision endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy", "service": "Theopy-Agent"}


def test_index_endpoint(client):
    """Test that the main chat interface loads successfully."""
    response = client.get("/")
    assert response.status_code == 200
    # Check that the Jinja template rendered our title
    assert b"Theopy AI" in response.data


def test_ask_endpoint_missing_message(client):
    """Test that the API correctly rejects empty requests with a 400 Bad Request."""
    response = client.post("/ask", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "No message provided"}


@patch("src.app.AgentDispatcher")
def test_ask_endpoint_success(MockDispatcher, client):
    """Test the successful routing of a user message to the AI Dispatcher."""
    mock_instance = MockDispatcher.return_value

    # Because app.py wraps the call in asyncio.run(), the mock MUST be an AsyncMock
    mock_instance.handle_user_input = AsyncMock(
        return_value="Here is the table of sessions you requested."
    )

    response = client.post(
        "/ask", json={"message": "Fetch sessions for Pharmacie de la gare"}
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "response": "Here is the table of sessions you requested."
    }
    mock_instance.handle_user_input.assert_called_once_with(
        "Fetch sessions for Pharmacie de la gare"
    )


@patch("src.app.AgentDispatcher")
def test_ask_endpoint_server_error(MockDispatcher, client):
    """Test the 500 Internal Server Error fallback when the AI brain crashes."""
    mock_instance = MockDispatcher.return_value

    # Simulate a fatal crash inside the dispatcher or network bridge
    mock_instance.handle_user_input.side_effect = Exception(
        "Simulated connection crash"
    )

    response = client.post("/ask", json={"message": "Trigger a crash"})

    assert response.status_code == 500
    assert response.get_json() == {"error": "I'm having trouble connecting right now."}
