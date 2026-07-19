from unittest.mock import Mock, patch

import pytest
import requests

from src.auth import TeepyAuthError, authenticate_with_teepy


@patch("src.auth.requests.post")
def test_authenticate_with_teepy_success(mock_post):
    mock_post.return_value = Mock(
        status_code=200,
        json=Mock(
            return_value={
                "user_id": 100,
                "login": "slamotte",
                "name": "Sylvie Lamotte",
                "role": "administrator",
            }
        ),
    )

    profile = authenticate_with_teepy("slamotte", "test")

    assert profile == {
        "user_id": 100,
        "login": "slamotte",
        "name": "Sylvie Lamotte",
        "role": "administrator",
    }
    mock_post.assert_called_once()
    _args, kwargs = mock_post.call_args
    assert kwargs["json"] == {"login": "slamotte", "password": "test"}


@patch("src.auth.requests.post")
def test_authenticate_with_teepy_invalid_credentials_raises(mock_post):
    mock_post.return_value = Mock(
        status_code=401, json=Mock(return_value={"error": "Invalid credentials"})
    )

    with pytest.raises(TeepyAuthError, match="Invalid credentials"):
        authenticate_with_teepy("slamotte", "wrong")


@patch("src.auth.requests.post")
def test_authenticate_with_teepy_employee_rejected_raises(mock_post):
    mock_post.return_value = Mock(
        status_code=403,
        json=Mock(return_value={"error": "This account cannot access Theopy."}),
    )

    with pytest.raises(TeepyAuthError, match="This account cannot access Theopy."):
        authenticate_with_teepy("mgarcia", "test")


@patch("src.auth.requests.post")
def test_authenticate_with_teepy_network_failure_propagates(mock_post):
    mock_post.side_effect = requests.ConnectionError("boom")

    with pytest.raises(requests.ConnectionError):
        authenticate_with_teepy("slamotte", "test")
