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