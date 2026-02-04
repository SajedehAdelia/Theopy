import pytest
from src.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_gemini_connection(client):
    """
    PROF MODE: This tests the FULL path:
    Request -> Flask Route -> get_ai_response() -> Gemini API -> Response
    """
    test_message = {"message": "Say exactly the word 'THEOPY-ONLINE'"}
    response = client.post('/v1/chat', json=test_message)
    assert response.status_code == 200
    assert response.json == {"reply": "THEOPY-ONLINE", "status": "success"}
