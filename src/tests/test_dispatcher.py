import pytest
from unittest.mock import AsyncMock, patch
from src.dispatcher import AgentDispatcher

@pytest.fixture
def mock_env(monkeypatch):
    monkeypatch.setenv("TEEPY_PATH", "/mock/path/to/teepy")
    monkeypatch.setenv("GEMINI_MODEL_ID", "gemini-mock-model")

@pytest.mark.asyncio
@patch("src.dispatcher.TeepyMCPClient") 
@patch("src.dispatcher.TheopyBrain")   
async def test_dispatcher_initialization(MockBrain, MockClient, mock_env):
    """Test that the dispatcher connects to MCP and initializes the Brain.""" 
    mock_client_instance = MockClient.return_value
    mock_client_instance.connect = AsyncMock()

    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    mock_client_instance.connect.assert_called_once()
    MockBrain.assert_called_once_with(mock_client_instance)
    assert dispatcher.brain is not None

@pytest.mark.asyncio
@patch("src.dispatcher.TeepyMCPClient")
@patch("src.dispatcher.TheopyBrain")
async def test_dispatcher_handle_user_input(MockBrain, MockClient, mock_env):
    """Test that the dispatcher correctly routes user text to the AI Brain."""
    mock_brain_instance = MockBrain.return_value
    mock_brain_instance.process_user_request = AsyncMock(return_value="Mocked AI response")

    dispatcher = AgentDispatcher()
    
    dispatcher.brain = mock_brain_instance

    result = await dispatcher.handle_user_input("Show me invoices.")

    mock_brain_instance.process_user_request.assert_called_once_with("Show me invoices.")
    assert result == "Mocked AI response"