import os

import requests

TEEPY_API_URL = os.getenv("TEEPY_API_URL", "http://teepy-app-1:5000")


class TeepyAuthError(Exception):
    """Raised when Teepy rejects the login/password or the account can't use
    Theopy (wrong credentials, inactive account, employee role)."""


def authenticate_with_teepy(login: str, password: str) -> dict:
    """POST credentials to Teepy's dedicated /api/theopy/authenticate endpoint
    and return the caller's profile (user_id, login, name, role) on success.

    Raises TeepyAuthError with Teepy's own message on a 400/401/403 response.
    Network/connection failures propagate as requests.RequestException - the
    caller is expected to tell that apart from bad credentials.
    """
    response = requests.post(
        f"{TEEPY_API_URL}/api/theopy/authenticate",
        json={"login": login, "password": password},
        timeout=5,
    )

    if response.status_code == 200:
        return response.json()

    error_message = response.json().get("error", "Authentication failed.")
    raise TeepyAuthError(error_message)
