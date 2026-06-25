import pytest
from unittest.mock import AsyncMock, patch
from src.dispatcher import AgentDispatcher


@pytest.mark.asyncio
@patch("src.dispatcher.TeepyMCPClient")
@patch("src.gemini_client.GeminiBrain")
async def test_dispatcher_initialization_gemini(MockGeminiBrain, MockClient, mock_env):
    """Test that the dispatcher initializes the Gemini Brain when local LLM is off."""
    mock_client_instance = MockClient.return_value
    mock_client_instance.connect = AsyncMock()

    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    mock_client_instance.connect.assert_called_once()
    MockGeminiBrain.assert_called_once_with(mock_client_instance)
    assert dispatcher.brain is not None


@pytest.mark.asyncio
@patch("src.dispatcher.TeepyMCPClient")
@patch("src.ollama_client.OllamaBrain")
async def test_dispatcher_initialization_ollama(
    MockOllamaBrain, MockClient, monkeypatch
):
    """Test that the dispatcher initializes the Ollama Brain when the toggle is active."""
    monkeypatch.setenv("USE_LOCAL_LLM", "1")

    mock_client_instance = MockClient.return_value
    mock_client_instance.connect = AsyncMock()

    dispatcher = AgentDispatcher()
    await dispatcher.initialize()

    mock_client_instance.connect.assert_called_once()
    MockOllamaBrain.assert_called_once_with(mock_client_instance)
    assert dispatcher.brain is not None


@pytest.mark.asyncio
@patch("src.dispatcher.TeepyMCPClient")
async def test_dispatcher_handle_user_input(MockClient, mock_env):
    """Test that the dispatcher correctly routes user text and cleans up connections."""
    mock_client_instance = MockClient.return_value
    mock_client_instance.close = AsyncMock()

    mock_brain_instance = AsyncMock()
    mock_brain_instance.process_user_request = AsyncMock(
        return_value="Mocked AI response"
    )

    dispatcher = AgentDispatcher()
    dispatcher.mcp_client = mock_client_instance
    dispatcher.brain = mock_brain_instance

    result = await dispatcher.handle_user_input("Show me invoices.")

    mock_brain_instance.process_user_request.assert_called_once_with(
        "Show me invoices."
    )
    mock_client_instance.close.assert_called_once()  # Ensure cleanup happened
    assert result == "Mocked AI response"
