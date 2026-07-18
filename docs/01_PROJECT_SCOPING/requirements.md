```yaml
title: "REQUIREMENTS & SPECIFICATIONS"
project: "Theopy – AI Assistant MCP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# THEOPY: Requirements & Specifications

## Vision

Theopy is an intelligent natural language routing engine. It acts as an autonomous AI agent that integrates with the Teepy ERP (and future applications) so users can retrieve complex data and trigger actions using simple, natural sentences. Theopy relies on a decoupled "Hub & Spoke" architecture via the Model Context Protocol (MCP), ensuring the AI layer remains strictly separated from the ERP's core business logic.

## Objectives (High Level)

* Automate simple interactions with the Teepy software to free up human time and improve Quality of Life at Work (QVT).


* Implement a decoupled architecture where Teepy exposes its "business intelligence" via its own MCP server, and Theopy acts as an interchangeable routing agent.


* Ensure LLM Agnosticism: The architecture must allow transparent switching between different AI engines (Gemini, Claude, local LLMs) without modifying the business applications' code.



## Success Criteria & KPIs (MVP)

To validate the architecture and the MVP, the following strict metrics must be met:

* **AI Response Time:** < 4 seconds.


* **Routing Accuracy (Function Calling):** > 95%.


* **Unit Test Coverage:** 80%.


* **Security:** Zero SQL context leakage.



## In-Scope (MVP)

* Implementation of a FastMCP server within the Teepy backend to securely expose ERP tools.


* Asynchronous network bridge using Server-Sent Events (SSE) for unidirectional, lightweight data streaming.


* Integration of the Google Gemini SDK (`google-genai`) to force the generation of JSON tool calls instead of free conversational text.


* Database security utilizing SQLAlchemy and isolated sessions.


* A front-end interface (Theopy UI) capable of consuming real-time SSE streams.



## Out-of-Scope (Initial)

* **Direct SQL Generation by AI:** Giving the AI direct, unrestricted access to the database to generate SQL queries is explicitly rejected due to critical security risks and the potential for data destruction.


* **Coupling AI to Legacy Code:** Embedding the AI logic directly inside the Teepy codebase (rejected as it is unusable for other company projects).



## Non-Functional Requirements

* **Security & Secrets:** Strict dynamic environment injection via `.env`. Both Theopy and Teepy must refuse to start if keys are missing (Fail-Fast behavior).


* **Network Isolation:** Strict port mapping via Docker and the creation of an isolated network bridge for inter-container communication.


* **Efficiency:** Use of SSE to eliminate network polling, drastically reducing bandwidth and CPU load.



## Risks & Mitigations

* **Risk (Infrastructure):** Network port conflicts between local containers.


* **Mitigation:** Strict Docker mapping and an isolated network bridge.




* **Risk (Security):** Leakage of API keys or database credentials.


* **Mitigation:** Dynamic environment injection with Fail-Fast startup.




* **Risk (Vendor Lock-in):** Being trapped with a single AI provider.


* **Mitigation:** Business intelligence remains in Teepy; Theopy is an interchangeable router.




* **Risk (Data Accuracy):** AI hallucinations generating false financial data.


* **Mitigation:** Strict Function Calling and zero direct SQL access.





## Tech Stack

* **Front-end:** HTML5 / CSS3, Vanilla JavaScript, Jinja2 templates.


* **Back-end:** Python 3, Flask framework.


* **Database:** PostgreSQL, SQLAlchemy ORM.


* **AI & Protocols:** Google Gemini SDK (`google-genai`), FastMCP (Model Context Protocol), SSE (Server-Sent Events) network streams.


* **Infrastructure:** Docker & Docker Compose, Linux, GNU Make.