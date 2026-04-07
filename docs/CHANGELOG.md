[v0.1.0] - 2026-03-19
### Added
- Modular API structure for Invoices and Sessions.
- Docker external network bridge for Teepy/Theopy communication.

### Fixed
- NameResolutionError by aligning Docker Compose service names.
- Apple Silicon (ARM) compatibility via linux/amd64 platform flag.

[v0.2.0] - 2026-03-27
### Added
- AI Router for intent classification and tool execution.
- Dispatcher module for routing requests to Teepy services.
- Gemini Coordinator for AI-driven decision making.

### Removed
Deprecated /v1/chat endpoint to ensure a single, secure entry point via /ask

[v0.3.0] - 2026-04-07
### Added
- **AI Orchestration**: Integrated `GeminiCoordinator` and `Dispatcher` into the main application flow (`/ask` route).
- **Tool Logic**: Defined virtual tools in `intent_definitions.py` for automated pharmacy session management.
- **Testing Suite**: Created professional Pytest modules (`test_dispatcher.py`, `test_app_routes.py`) using real SQL development data.
- **Supervision**: Implemented a `/health` endpoint for DevOps monitoring and service validation.

### Changed
- **Refactoring**: Consolidated redundant AI logic in `app.py` to ensure single-responsibility and security.
- **Cleanup**: Purged legacy voice templates and placeholder tests to reduce technical debt.

### Removed
- Deprecated `test_gemini_connection.py` and `test_placeholder.py`.
- Legacy `voice_test.html` and `test.wav` audio samples.