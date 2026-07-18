# OWASP Top 10 Security Mapping

This document details the security measures implemented in the Theopy project to cover the 10 main security flaws described by the OWASP.

**1. Broken Access Control**
*   **Mitigation:** The routing bridge securely injects the Flask Context and database sessions using the `@agent_tool` decorator. Database access is strictly scoped using dedicated credentials (`POSTGRES_USER=te`, `POSTGRES_DB=t`) injected via environment variables, preventing unauthorized horizontal or vertical privilege escalation.

**2. Cryptographic Failures**
*   **Mitigation:** Sensitive credentials are never hardcoded in the repository. Keys such as `GEMINI_API_KEY` and `POSTGRES_PASSWORD` are managed exclusively through a `.env` file (parsed via `python-dotenv==1.0.0`).

**3. Injection**
*   **Mitigation:** Direct SQL queries are completely avoided. The application uses the `sqlalchemy==2.0.25` ORM (e.g., `select(Invoice).options(selectinload(Invoice.customer))`). SQLAlchemy automatically parameterizes queries and escapes inputs, effectively neutralizing SQL injection attacks.

**4. Insecure Design**
*   **Mitigation:** The architecture strictly separates the AI reasoning layer (Ollama/Gemini) from the ERP data layer (Teepy). The MCP protocol acts as a defined boundary where only specific, whitelisted tools (e.g., `agent_list_invoices`, `agent_pay_invoice`) are exposed, preventing the AI from executing arbitrary backend commands.

**5. Security Misconfiguration**
*   **Mitigation:** Debugging modes are strictly controlled. While `FLASK_DEBUG` may be used in the Teepy Makefile for local development, it is explicitly excluded from the Theopy production environment. 

**6. Vulnerable and Outdated Components**
*   **Mitigation:** All Python dependencies are strictly locked using a `requirements.txt` file (e.g., `Flask==3.0.0`, `requests==2.31.0`). This ensures deterministic builds and prevents the accidental introduction of vulnerable sub-dependencies.

**7. Identification and Authentication Failures**
*   **Mitigation:** Interactions with the Teepy backend rely on established authentication. Within the MCP framework, the server establishes a dedicated `ClientSession` with a strict lifecycle managed by an `AsyncExitStack` to prevent session fixation or leakage.

**8. Software and Data Integrity Failures**
*   **Mitigation:** A strict CI/CD pipeline (GitHub Actions) acts as a gatekeeper. Every push and pull request triggers a matrix build across Ubuntu and macOS that runs linters (`flake8`, `black`) and a test suite (`pytest -m "not ai"`). Code cannot be merged if these integrity checks fail.

**9. Security Logging and Monitoring Failures**
*   **Mitigation:** The system implements standard error stream logging (`sys.stderr`), and is integrated with `sentry-sdk[flask]==1.40.0` to capture, monitor, and alert on active runtime exceptions and potential breaches in real-time.

**10. Server-Side Request Forgery (SSRF)**
*   **Mitigation:** The MCP client strictly communicates with a pre-defined endpoint (`TEEPY_MCP_URL=http://teepy-app-1:5001/sse`). The AI model cannot arbitrarily dictate the URL the backend uses to fetch data, neutralizing the risk of internal network scanning.