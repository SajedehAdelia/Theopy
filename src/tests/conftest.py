import pytest
from src.app import _dispatchers, app
from unittest.mock import AsyncMock
from src.tests.mocks.ai_scenarios import mock_call_tool


@pytest.fixture
def client():
    """Configures the app for testing and returns a clean test client."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def logged_in_client(client):
    """A test client with an already-logged-in Theopy session (administrator),
    for routes gated behind login_required."""
    with client.session_transaction() as flask_session:
        flask_session["user_id"] = 100
        flask_session["login"] = "slamotte"
        flask_session["name"] = "Sylvie Lamotte"
        flask_session["role"] = "administrator"
    return client


@pytest.fixture(autouse=True)
def reset_dispatchers():
    """_dispatchers is a module-level dict keyed by user_id, shared across
    requests in the real app - clear it between tests so a mocked dispatcher
    from one test is never reused (and returned stale) by the next."""
    _dispatchers.clear()
    yield
    _dispatchers.clear()


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    """Global safe environment for all tests. Runs automatically."""
    monkeypatch.setenv("TEEPY_PATH", "/mock/path/to/teepy")
    monkeypatch.setenv("GEMINI_MODEL_ID", "gemini-mock-model")
    monkeypatch.setenv("GEMINI_API_KEY", "dummy-test-api-key-12345")
    monkeypatch.delenv("USE_LOCAL_LLM", raising=False)


@pytest.fixture(autouse=True)
def inject_mcp_simulator(monkeypatch):
    """
    Automatically replaces the real MCP network call with our deterministic simulator.
    This ensures CI runs instantly and safely.
    """

    async def async_mock_call_tool(self, tool_name: str, arguments: dict):
        return mock_call_tool(tool_name, arguments)

    monkeypatch.setattr("src.mcp_client.TeepyMCPClient.call_tool", async_mock_call_tool)

    monkeypatch.setattr("src.mcp_client.TeepyMCPClient.connect", AsyncMock())
    monkeypatch.setattr("src.mcp_client.TeepyMCPClient.close", AsyncMock())
