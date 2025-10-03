# Project brief — Theopy Assistant


## Vision
A voice-first server-side AI assistant that wraps Teepy (and future apps) so users can control the application and complete tasks by speaking naturally. No front-end besides voice input/output; the assistant acts as a middleware that maps natural language to safe API actions.


## Objectives (high level)
- Provide an assistant that can interpret user requests and perform actions in Teepy via its API.
- Achieve an MVP where core flows (create client, list appointments, modify records) work reliably.
- Ensure the assistant is modular so it can be re-used with other apps in future.


## Success criteria (MVP)
- End-to-end flow works: user says a command → STT → assistant extracts intent → server calls Teepy API → assistant confirms action via TTS or text.
- Average response time (STT→Action→TTS) < 3 seconds for common actions (target). Practical target: < 5 seconds.
- Error handling: assistant asks clarifying questions for incomplete commands and logs all actions.
- Basic tests and CI in place; `docs/` contains design and acceptance criteria.


## In-scope (MVP)
- Server-side assistant service (REST/WebSocket) that accepts audio / text and returns audio / text replies.
- Core intent extraction and command routing to Teepy API.
- Authentication between assistant and Teepy (API token / service account).
- Basic logging and audit trail for actions taken.


## Out-of-scope (initial)
- GUI or browser extension.
- Full multi-language support (start with English; add support later).
- Advanced personalisation & user profiles beyond basic mapping.


## Non-functional requirements
- **Security:** store API credentials encrypted, use HTTPS for all communications.
- **Performance:** median intent parsing < 300ms (LLM network latency excluded).
- **Availability:** MVP hosted with a reasonable SLA (e.g., 99% uptime during work hours).
- **Privacy:** do not store audio longer than needed; log textual commands and actions with retention policy.


## Assumptions
- Teepy exposes a stable API that can be called from the assistant server.
- You have permission to use required LLM / STT / TTS services (OpenAI keys, etc.).
- You can host the server (a small cloud VM is sufficient for MVP).


## Risks & Mitigations
- **Risk:** Dependency on paid APIs (cost). **Mitigation:** Measure usage, use local models for dev, set quotas.
- **Risk:** Latency and UX degradation. **Mitigation:** Cache frequent responses, use streaming where possible.
- **Risk:** Security / data leakage. **Mitigation:** Encrypt secrets, limit data retention, implement auth and scopes.


## Metrics / KPIs
- Commands successfully executed (%) — target: 70%+ for MVP.
- Mean time to execute command (seconds).
- Number of clarification loops per session.
- Cost per 1,000 commands (estimate for budget tracking).


## Tech stack (suggested)
- **Language:** Python (FastAPI) or Node.js (Express). FastAPI recommended for quick iteration.
- **STT:** Whisper (local) or OpenAI Whisper API.
- **LLM:** OpenAI (function calling / tool use) or a local LLM during dev.
- **TTS:** Coqui TTS / cloud TTS for higher quality.
- **Orchestration:** LangChain (optional) for tool-calling patterns.
- **Infra:** small cloud VM (DigitalOcean / AWS / GCP), Docker, GitHub Actions for CI.


## Timeline for Sprint 1 (Weeks 1–2)
- **Week 1 (Days 1–5):** Draft stakeholder map, requirements doc, set up repo and project board.
- **Week 2 (Days 6–10):** Review & adjust docs, prepare acceptance criteria for MVP, create initial backlog tickets.


## Acceptance criteria (for Sprint 1)
- `docs/stakeholders.md` and `docs/requirements.md` exist in the repo and are readable.
- Project board created and contains the Sprint 1 cards.
- At least one person (or you) has reviewed and accepted the brief.


## Kanban / Project board (quick setup)
**Columns:** Backlog → To Do → In Progress → In Review → Done


**Suggested cards for Sprint 1:**
- Draft stakeholder map (`docs/stakeholders.md`)
- Create project brief (`docs/requirements.md`)
- Create GitHub repo skeleton + `docs/`
- Setup GitHub project board (or Trello)
- Setup initial CI pipeline stub (linting + tests)
- Kickoff review meeting (end Sprint 1)