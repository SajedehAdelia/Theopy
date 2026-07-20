# Changelog

## [1.5.0] - 2026-07-19
### Authentication & Role-Based Access Control
* **Security:** Introduced `POST /api/theopy/authenticate` on the Teepy side, validating credentials against real production accounts. Inactive accounts and the `employee` role (external pharmacy portal users) are rejected - only Kozea staff roles can use Theopy. No signup path exists in Theopy.
* **Security:** Replaced blanket-admin MCP context with `_resolve_real_caller()`, which re-resolves the real calling user from the database on every single tool call, using an identity carried on the MCP protocol's `meta` field (never a tool argument, so the LLM can never see or influence it). No valid identity, unknown user, or inactive user results in denial, with no fallback to admin.
* **Added:** `requires_role()` decorator applied to all 32 existing MCP tools, each tagged with its allowed roles per business domain (invoices, customers, plannings, sessions, reminders); invoice generation restricted to `administrator` only.
* **Added:** `src/auth.py`, `/login` and `/logout` routes, and session gating on `/`, `/ask`, and `/history` in Theopy.
* **Added:** Client-side tool-list filtering by role (`src/role_access.py`) as a UX layer - Teepy's server-side check remains the sole authority.
* **Fixed:** Theopy previously reused a single global `AgentDispatcher` for every request regardless of who was logged in, leaking one user's conversation history and cached tool list into another user's session. Replaced with one dispatcher per logged-in user, torn down on logout.
* **Changed:** Settings sidebar "Compte" section now shows the real logged-in name/role; "Déconnexion" is a working logout link instead of a disabled placeholder.
* **Tests:** Added 26 tests on the Teepy side (auth endpoint + role enforcement, verified against a real seeded database via a genuine MCP client/server round trip) and 35+ new tests on the Theopy side (auth, session gating, dispatcher isolation, role filtering).

## [1.4.0] - 2026-07-18
### Frontend UX Overhaul
* **Added:** Settings sidebar (left) with Compte, Affichage, Déconnexion, and connected-MCP-project sections.
* **Changed:** Moved the 24h history sidebar from left to right, alongside the new settings sidebar.
* **Added:** Search bar in the history sidebar - searches across every domain, not just the active tab, sorted most-recent-first.
* **Added:** Recalling a history entry now shows the original question first (faded), then the answer, in the same order as a live exchange.
* **Added:** `frontend-tests/` with a Node built-in test-runner suite for the search/selection logic (`history-logic.js`), wired into `make check` via a new `test-js` target.

## [1.3.0] - 2026-07-07
### RNCP Certification Dossier & Architecture Documentation
* **Docs:** Completely overhauled `System_Architecture.md` and `requirements.md` to formally reflect the transition to the FastMCP "Hub & Spoke" model and Server-Sent Events (SSE) data streams.
* **Docs:** Added `OWASP_mapping.md` to formally document security measures mitigating the OWASP Top 10 vulnerabilities.
* **Docs:** Updated `project_brief.md`, `SWOT.md`, `PESTEL.md`, and `technical_study.md` to align with the final MVP capabilities, LLM Agnosticism, and the 10-week execution timeline.
* **Docs:** Revised `cost_estimation.md` and `workload_estimation.md` to reflect the actual J/H (Man-Days) utilized and accurate ROI projections.
* **Docs:** Expanded `risk_mapping.md` to include specific MCP/SSE operational risks, CI/CD pipeline dependencies, and incident response KPIs.

## [1.2.0] - 2026-06-24
### Local AI Integration & Async Stabilization
* **Added:** `ollama_client.py` to support local, cost-free LLM inference via Ollama (`llama3.1`) for development and privacy-first deployments.
* **Added:** Environment variable toggle (`USE_LOCAL_LLM`) in `dispatcher.py` to dynamically switch between the Gemini Cloud Brain and the Ollama Local Brain.
* **Changed:** Updated AI system instructions in `gemini_client.py` to strictly enforce Markdown table formatting for data list responses, improving UI rendering.
* **Fixed:** Resolved `asyncio` TaskGroup teardown crashes by explicitly closing the FastMCP SSE bridge in a `finally` block within the dispatcher.
* **Fixed:** Refactored Pytest suite (`test_dispatcher.py`, `test_app_routes.py`) with `AsyncMock` and `monkeypatch` to support the new dual-brain initialization and eliminate `TypeError` during async assertions.

## [1.1.0] - 2026-06-18
### FastMCP SSE Integration & Asynchronous Stability
* **Changed:** Transitioned FastMCP client and server communication from STDIO to Server-Sent Events (SSE) transport for robust inter-container networking.
* **Fixed:** Resolved fatal `asyncio` Event Loop collisions in Flask by isolating the `AgentDispatcher` instantiation inside the `/ask` route using `asyncio.run()`.
* **Fixed:** Eliminated `google-genai` SDK `ValueError` crashes by explicitly injecting the `GEMINI_API_KEY` into the `genai.Client` constructor for strict Docker environment compatibility.
* **Fixed:** Corrected Docker DNS routing (`Name or service not known`) and `ConnectError` failures by mapping `TEEPY_MCP_URL` directly to `http://teepy-app-1:5001/sse`.
* **Infra:** Integrated the FastMCP server directly into the main Teepy ERP container, securely piggybacking on the S6-overlay to inherit the Python virtual environment and PostgreSQL database context.

## [1.0.0] - 2026-05-10
### Architecture Overhaul: Agentic Transformation
* **Added:** `mcp_client.py` to establish direct, secure STDIO connections to the Teepy ERP backend.
* **Added:** `gemini_client.py` integrating the modern `google-genai` SDK with full Tool Calling (ReAct loop) capabilities.
* **Added:** `dispatcher.py` to act as the asynchronous manager between the Web UI and the AI Brain.
* **Changed:** Completely removed legacy REST API bridging. Theopy no longer queries the database directly.
* **Security:** Migrated all hardcoded API keys, paths, and model IDs to strict `.env` variables (`GEMINI_API_KEY`, `TEEPY_PATH`, `GEMINI_MODEL_ID`).
* **Removed:** Deprecated `intent_definitions.py` and old mock databases, as routing is now handled autonomously by the LLM.

## [0.3.0] - 2026-04-07
### Orchestration & Supervision
* **Added:** Integrated `GeminiCoordinator` and `Dispatcher` into the main application flow (`/ask` route).
* **Added:** Defined virtual tools in `intent_definitions.py` for automated pharmacy session management.
* **Added:** Created professional Pytest modules (`test_dispatcher.py`, `test_app_routes.py`) using real SQL development data.
* **Added:** Implemented a `/health` endpoint for DevOps monitoring and service validation.
* **Changed:** Consolidated redundant AI logic in `app.py` to ensure single-responsibility and security.
* **Removed:** Purged legacy voice templates, `test_gemini_connection.py`, `test_placeholder.py`, and placeholder tests to reduce technical debt.

## [0.2.0] - 2026-03-27
### Routing Foundations
* **Added:** AI Router for intent classification and tool execution.
* **Added:** Dispatcher module for routing requests to Teepy services.
* **Added:** Gemini Coordinator for AI-driven decision making.
* **Removed:** Deprecated `/v1/chat` endpoint to ensure a single, secure entry point via `/ask`.

## [0.1.0] - 2026-03-19
### Initial Setup
* **Added:** Modular API structure for Invoices and Sessions.
* **Added:** Docker external network bridge for Teepy/Theopy communication.
* **Fixed:** `NameResolutionError` by aligning Docker Compose service names.
* **Fixed:** Apple Silicon (ARM) compatibility via `linux/amd64` platform flag.