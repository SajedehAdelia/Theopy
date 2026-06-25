import pytest
from src.app import app


@pytest.fixture
def client():
    """Configures the app for testing and returns a clean test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Global safe environment for all tests. Runs automatically."""
    monkeypatch.setenv("TEEPY_PATH", "/mock/path/to/teepy")
    monkeypatch.setenv("GEMINI_MODEL_ID", "gemini-mock-model")
    monkeypatch.delenv("USE_LOCAL_LLM", raising=False)
