# OWASP Top 10 Security Mapping

This document details the security measures implemented in the Theopy project to cover the 10 main security flaws described by the OWASP.

**1. Broken Access Control**
*   **Mitigation:** Every MCP tool call carries the caller's real identity on the protocol's `meta` field (never a tool argument, so the LLM cannot see or influence it). Teepy re-resolves that identity from the database on every call (`_resolve_real_caller()`) and denies by default, with no fallback to an administrator profile. All 32 MCP tools are wrapped in `requires_role()`, each tagged with its allowed roles per business domain; Theopy mirrors this client-side (`src/role_access.py`) as a UX layer only — Teepy's server-side check remains the sole authority.

**2. Cryptographic Failures**
*   **Mitigation:** Sensitive credentials are never hardcoded in the repository. Keys such as `GEMINI_API_KEY` and `POSTGRES_PASSWORD` are managed exclusively through a `.env` file (parsed via `python-dotenv==1.0.0`).

**3. Injection**
*   **Mitigation:** Direct SQL queries are completely avoided. The application uses the `sqlalchemy==2.0.25` ORM (e.g., `select(Invoice).options(selectinload(Invoice.customer))`). SQLAlchemy automatically parameterizes queries and escapes inputs, effectively neutralizing SQL injection attacks.

**4. Insecure Design**
*   **Mitigation:** The architecture strictly separates the AI reasoning layer (Ollama/Gemini) from the ERP data layer (Teepy). The MCP protocol acts as a defined boundary where only specific, whitelisted tools (e.g., `agent_list_invoices`, `agent_pay_invoice`) are exposed, preventing the AI from executing arbitrary backend commands.

**5. Security Misconfiguration**
*   **Mitigation:** Debug mode defaults off (`_debug_mode_enabled()` in `src/app.py`), avoiding an exposed interactive debugger or full stack traces on error in case of incident. It is only activated locally by explicitly setting `FLASK_DEBUG=1` in `.env`.

**6. Vulnerable and Outdated Components**
*   **Mitigation:** All Python dependencies are strictly locked using a `requirements.txt` file (e.g., `Flask==3.0.0`, `requests==2.31.0`). This ensures deterministic builds and prevents the accidental introduction of vulnerable sub-dependencies.

**7. Identification and Authentication Failures**
*   **Mitigation:** `POST /api/theopy/authenticate` validates credentials against real Teepy production accounts (passwords hashed with `pbkdf2_sha512` on the Teepy side). Inactive accounts and the `employee` role (external pharmacy portal users) are rejected — only Kozea staff roles can use Theopy, and no signup path exists in Theopy. Each MCP tool call's `ClientSession` lifecycle is additionally managed by an `AsyncExitStack` to prevent session fixation or leakage at the transport level.

**8. Software and Data Integrity Failures**
*   **Mitigation:** A strict CI/CD pipeline (GitHub Actions) acts as a gatekeeper. Every push and pull request triggers a matrix build across Ubuntu and macOS that runs linters (`flake8`, `black`) and a test suite (`pytest -m "not ai"`). Code cannot be merged if these integrity checks fail.

**9. Security Logging and Monitoring Failures**
*   **Mitigation:** Every login attempt (success, failure, or rejected role) is logged via the standard `logging` module on both Theopy and Teepy, with the password itself never logged. `sentry-sdk[flask]` is a declared dependency reserved for production runtime-exception alerting; it is not yet initialized in `src/app.py` — noted here rather than overstated, since real-time alerting is not active today.

**10. Server-Side Request Forgery (SSRF)**
*   **Mitigation:** The MCP client strictly communicates with a pre-defined endpoint (`TEEPY_MCP_URL=http://teepy-app-1:5001/sse`). The AI model cannot arbitrarily dictate the URL the backend uses to fetch data, neutralizing the risk of internal network scanning.