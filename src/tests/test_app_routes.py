from unittest.mock import AsyncMock, patch

from src import history_store
from src.auth import TeepyAuthError


def test_health_endpoint(client):
    """Test the DevOps supervision endpoint. Never gated behind login - Docker
    needs to reach it before anyone has authenticated."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy", "service": "Theopy-Agent"}


def test_index_redirects_to_login_when_not_authenticated(client):
    response = client.get("/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_index_endpoint(logged_in_client):
    """Test that the main chat interface loads successfully once logged in."""
    response = logged_in_client.get("/")
    assert response.status_code == 200
    # Check that the Jinja template rendered our title
    assert b"Theopy" in response.data


def test_ask_endpoint_requires_login(client):
    response = client.post("/ask", json={"message": "Hello"})
    assert response.status_code == 401
    assert response.get_json() == {"error": "Non authentifié."}


def test_ask_endpoint_missing_message(logged_in_client):
    """Test that the API correctly rejects empty requests with a 400 Bad Request."""
    response = logged_in_client.post("/ask", json={})
    assert response.status_code == 400
    assert response.get_json() == {"error": "Aucun message fourni."}


@patch("src.app.AgentDispatcher")
def test_ask_endpoint_success(MockAgentDispatcher, logged_in_client):
    """Test the successful routing of a user message to the AI Dispatcher.

    src.app now creates one AgentDispatcher per logged-in user_id (not a
    single shared instance), so we patch the AgentDispatcher class itself -
    _get_dispatcher_for() will hand back MockAgentDispatcher.return_value.
    """
    mock_dispatcher = MockAgentDispatcher.return_value
    # Because app.py wraps the call in asyncio.run(), the mock MUST be an AsyncMock
    mock_dispatcher.handle_user_input = AsyncMock(
        return_value="Here is the table of sessions you requested."
    )

    response = logged_in_client.post(
        "/ask", json={"message": "Fetch sessions for Pharmacie de la gare"}
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "response": "Here is the table of sessions you requested."
    }
    mock_dispatcher.handle_user_input.assert_called_once_with(
        "Fetch sessions for Pharmacie de la gare", 100, "administrator"
    )


@patch("src.app.AgentDispatcher")
def test_ask_endpoint_server_error(MockAgentDispatcher, logged_in_client):
    """Test the 500 Internal Server Error fallback when the AI brain crashes."""
    mock_dispatcher = MockAgentDispatcher.return_value
    mock_dispatcher.handle_user_input = AsyncMock(
        side_effect=Exception("Simulated connection crash")
    )

    response = logged_in_client.post("/ask", json={"message": "Trigger a crash"})

    assert response.status_code == 500
    assert response.get_json() == {
        "error": "Un problème de connexion est survenu. Veuillez réessayer."
    }


def test_history_endpoint_requires_login(client):
    response = client.get("/history")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_history_endpoint_empty_by_default(logged_in_client):
    """Test that /history returns an empty object when nothing was recorded."""
    history_store.clear()
    response = logged_in_client.get("/history")
    assert response.status_code == 200
    assert response.get_json() == {}


def test_history_endpoint_returns_grouped_domains(logged_in_client):
    """Test that /history exposes recorded tool calls grouped by business domain."""
    history_store.clear()
    history_store.record(
        "fetch_all_invoices_list",
        {"customer_name": "Gare"},
        "Invoices List: ...",
        user_id=100,
    )

    response = logged_in_client.get("/history")

    assert response.status_code == 200
    data = response.get_json()
    assert "Factures" in data
    assert data["Factures"][0]["tool_name"] == "fetch_all_invoices_list"


def test_history_endpoint_does_not_return_another_users_entries(logged_in_client):
    """logged_in_client is user_id=100 - a call recorded under a different
    user_id must never show up in this user's /history."""
    history_store.clear()
    history_store.record(
        "fetch_all_invoices_list", {}, "someone else's invoice call", user_id=999
    )

    response = logged_in_client.get("/history")

    assert response.status_code == 200
    assert response.get_json() == {}


def test_login_page_loads(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"Se connecter" in response.data


def test_login_already_authenticated_redirects_to_index(logged_in_client):
    response = logged_in_client.get("/login")
    assert response.status_code == 302
    assert response.headers["Location"] == "/"


def test_login_missing_fields(client):
    response = client.post("/login", data={"login": "slamotte"})
    assert response.status_code == 400
    assert "Identifiant et mot de passe requis." in response.get_data(as_text=True)


@patch("src.app.authenticate_with_teepy")
def test_login_success_sets_session(mock_authenticate, client):
    mock_authenticate.return_value = {
        "user_id": 100,
        "login": "slamotte",
        "name": "Sylvie Lamotte",
        "role": "administrator",
    }

    response = client.post("/login", data={"login": "slamotte", "password": "test"})

    assert response.status_code == 302
    assert response.headers["Location"] == "/"
    mock_authenticate.assert_called_once_with("slamotte", "test")

    with client.session_transaction() as flask_session:
        assert flask_session["user_id"] == 100
        assert flask_session["login"] == "slamotte"
        assert flask_session["name"] == "Sylvie Lamotte"
        assert flask_session["role"] == "administrator"


@patch("src.app.authenticate_with_teepy")
def test_login_invalid_credentials(mock_authenticate, client):
    mock_authenticate.side_effect = TeepyAuthError("Invalid credentials")

    response = client.post("/login", data={"login": "slamotte", "password": "wrong"})

    assert response.status_code == 401
    # Teepy's raw error is English - the login page must show the French
    # translation instead, never the untranslated string.
    assert "Identifiant ou mot de passe incorrect." in response.get_data(as_text=True)
    assert "Invalid credentials" not in response.get_data(as_text=True)
    with client.session_transaction() as flask_session:
        assert "user_id" not in flask_session


@patch("src.app.authenticate_with_teepy")
def test_login_employee_role_rejected_shows_french_message(mock_authenticate, client):
    mock_authenticate.side_effect = TeepyAuthError("This account cannot access Theopy.")

    response = client.post("/login", data={"login": "mgarcia", "password": "test"})

    assert response.status_code == 401
    assert "Ce compte ne peut pas accéder à Theopy." in response.get_data(as_text=True)


@patch("src.app.authenticate_with_teepy")
def test_login_unmapped_teepy_error_passes_through_unchanged(mock_authenticate, client):
    """Defense in depth: an error message Teepy might add later, not yet in
    the translation table, should still reach the user rather than vanish."""
    mock_authenticate.side_effect = TeepyAuthError("Some new error Teepy added")

    response = client.post("/login", data={"login": "slamotte", "password": "test"})

    assert response.status_code == 401
    assert "Some new error Teepy added" in response.get_data(as_text=True)


@patch("src.app.authenticate_with_teepy")
def test_login_teepy_unreachable(mock_authenticate, client):
    import requests

    mock_authenticate.side_effect = requests.ConnectionError("boom")

    response = client.post("/login", data={"login": "slamotte", "password": "test"})

    assert response.status_code == 503
    assert "Impossible de contacter Teepy." in response.get_data(as_text=True)


def test_logout_clears_session(logged_in_client):
    response = logged_in_client.get("/logout")

    assert response.status_code == 302
    assert response.headers["Location"] == "/login"
    with logged_in_client.session_transaction() as flask_session:
        assert "user_id" not in flask_session


@patch("src.app.AgentDispatcher")
def test_logout_discards_dispatcher(MockAgentDispatcher, logged_in_client):
    """Logging out must free the per-user dispatcher (closing its MCP
    connection and dropping conversation history), not leave it cached under
    that user_id for whoever logs in next."""
    from src.app import _dispatchers

    mock_dispatcher = MockAgentDispatcher.return_value
    mock_dispatcher.handle_user_input = AsyncMock(return_value="ok")
    mock_dispatcher.shutdown = AsyncMock()

    logged_in_client.post("/ask", json={"message": "hi"})
    assert 100 in _dispatchers

    logged_in_client.get("/logout")

    assert 100 not in _dispatchers
    mock_dispatcher.shutdown.assert_called_once()
