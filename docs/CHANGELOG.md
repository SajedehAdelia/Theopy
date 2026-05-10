# Changelog

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