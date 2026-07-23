```yaml
title: "SYSTEM ARCHITECTURE"
project: "Theopy – AI Assistant MCP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# System Architecture

This document describes the finalized architecture of **Theopy**. The design has transitioned from a legacy REST/WebSocket monolith to a highly secure, modular **"Hub & Spoke" architecture** using the Model Context Protocol (MCP).

The system acts as an intelligent natural language routing engine, ensuring the AI reasoning layer is strictly decoupled from the core Teepy ERP business logic.

---

## High-Level Architecture (Hub & Spoke)

### Sequence & Data Flow Diagram

```text
User 
 │ (Prompt: e.g., "Factures Pharmacie 2019")
 ▼
[ Theopy UI (Browser) ]
 │
 ▼
[ Theopy Agent (MCP Client) ] ──(Prompt + List of Tools)──▶ [ Google Gemini API ]
 │                            ◀──(Intent Detected: JSON)──
 │
 ├──(HTTP SSE Request)────────────────────────────────────▶ [ Teepy (MCP Server) ]
 │                                                               │
 │                                                               ├──(Secure SQL)──▶ [ PostgreSQL ]
 │                                                               ◀──(Raw Data)────
 ◀──(Return data via SSE stream)─────────────────────────────────┘
 │
 ├──(Provide ERP data to LLM)─────────────────────────────▶ [ Google Gemini API ]
 │                            ◀──(Synthesized Text Reply)──
 ▼
[ Theopy UI ] (Displays Result)

```

---

## Components & Responsibilities

### 1. Theopy UI (Front-End)

* **Role:** The browser-based interface where the user inputs natural language commands.


* **Tech Stack:** HTML5, CSS3, Vanilla JavaScript, and Jinja2 templates.


* **Responsibility:** Capture user intent and consume asynchronous Server-Sent Events (SSE) to display real-time updates.



### 2. Theopy Agent (MCP Client)

* **Role:** The autonomous AI gateway and orchestrator.


* **Tech Stack:** Python 3, Flask, FastRTC/FastMCP Client.


* **Responsibility:** Receives the user prompt, communicates with the LLM to determine the required tools, and routes the execution to the appropriate external MCP server.



### 3. Intelligence Layer (Gemini / Ollama — dual brain)

* **Role:** The LLM reasoning engine. Two interchangeable brains are supported: Google Gemini (cloud, default) and Ollama (`llama3.1`, local, cost-free).


* **Tech Stack:** `google-genai` SDK for Gemini; `OllamaBrain` talks to a local Ollama server through an OpenAI-compatible endpoint (`http://host.docker.internal:11434/v1`).


* **Responsibility:** Performs strict "Function Calling". It translates the natural language prompt into a structured JSON tool call (e.g., triggering `agent_invoices_summary`). It later synthesizes the raw database results into a human-readable reply. The `USE_LOCAL_LLM` environment variable toggles which brain `dispatcher.py` instantiates, with no change required to the routing logic or downstream components.



### 4. Teepy Backend (MCP Server)

* **Role:** The ERP application exposing its business intelligence securely.


* **Tech Stack:** Python 3, Flask, FastMCP Server.


* **Responsibility:** Validates the tool request, establishes a secure database context, and executes the business logic.



### 5. Database

* **Role:** The core enterprise data storage.


* **Tech Stack:** PostgreSQL, SQLAlchemy ORM.


* **Responsibility:** Ensures all queries are parameterized and safe. The AI never has direct SQL generation access, eliminating context leakage risks.



### 6. Authentication & Access Control (RBAC)

* **Role:** Gates every user session and every MCP tool call behind a real identity.


* **Tech Stack:** `src/auth.py` and `src/role_access.py` on the Theopy side; `requires_role()` and `_resolve_real_caller()` on the Teepy side (sole authority).


* **Responsibility:** `POST /api/theopy/authenticate` validates credentials against real Teepy production accounts; inactive accounts and the `employee` role are rejected, with no signup path in Theopy. Every MCP tool call carries the caller's real identity on the protocol's `meta` field — never a tool argument, so the LLM can neither see nor influence it. Teepy re-resolves that identity from the database on every single call and denies by default, with no fallback to an administrator profile. Theopy's `role_access.py` mirrors the same role map client-side as a UX layer only.



---

## Inter-Service Communication

* **Server-Sent Events (SSE):** Communication between the Theopy MCP Client and the Teepy MCP Server is handled entirely via SSE. This unidirectional protocol is lightweight, avoids timeout issues common with standard REST requests during LLM inference, and is highly efficient for asynchronous context bubbling.


* **LLM Agnosticism:** Because communication is standardized via MCP, the LLM engine (Gemini) can be swapped transparently without modifying the Teepy ERP code.



---

## Eco-Design & Environmental Impact

Theopy is designed with software sobriety, aligning with sustainable IT practices:

* **Compute Delegation:** Instead of hosting highly energy-intensive GPU servers locally 24/7, Theopy delegates the heavy AI calculation "on-demand" via the Google Gemini API.


* **Network Efficiency:** The use of SSE maintains a single, lightweight connection. This eliminates network polling, drastically reducing bandwidth and CPU load compared to legacy architectures.


* **Infrastructure Sobriety:** Deployment relies on lightweight Docker containers, optimizing the use of VPS hardware resources compared to full virtual machines.



---

## Digital Accessibility (A11y)

The system adheres to formal digital standards to ensure inclusivity:

* **RGAA (Référentiel Général d’Amélioration de l’Accessibilité):** The web interface utilizes semantic HTML5 and proper ARIA labels so screen readers can interpret real-time AI responses generated in the Jinja2 templates.
* **OPQUAST Compliance:** Users are always provided with visual status indicators when the SSE stream is active or the AI is "thinking," ensuring a predictable and controlled user experience.

---

## Failure Modes & Security Mitigations

| Risk | Mitigation |
| --- | --- |
| **Direct SQL Injection by AI** | Strict routing. The AI only outputs JSON tool requests. SQLAlchemy handles all data escaping securely.

 |
| **Port Conflicts** | Strict Docker mapping and the creation of an isolated network bridge for inter-container communication.

 |
| **Credential Leaks** | Dynamic injection of `.env` files. Both servers implement Fail-Fast logic and refuse to boot if keys are missing.

 |
| **Vendor Lock-in** | Business intelligence remains strictly in Teepy. Theopy acts only as an interchangeable router.

 |
| **Unauthorized MCP Tool Access** | Deny-by-default `requires_role()` on every Teepy tool, plus real-identity re-resolution via `_resolve_real_caller()` on the `meta` field (never LLM-visible). `role_access.py` mirrors this client-side as UX only.

 |
| **Weak / Stale Credentials** | Real authentication against Teepy production accounts (`POST /api/theopy/authenticate`); inactive accounts and the `employee` role are rejected; no signup path exists in Theopy.

 |

---

## Observability & KPIs

To validate the deployment, the architecture must strictly achieve the following metrics:

| Metric | Target |
| --- | --- |
| **AI Response Time** | < 4 seconds

 |
| **Routing Accuracy (Function Calling)** | > 95%

 |
| **Unit Test Coverage** | 80% minimum

 |
| **SQL Context Leakage** | Zero

 |

Measured 2026-07-23 (`coverage run -m pytest src/ -m "not ai"`, same scope as CI): **75%** on business logic (`--omit src/tests/*`), **89%** including test files. Core routing/auth/access-control modules (`app.py`, `auth.py`, `dispatcher.py`, `history_store.py`, `response_guard.py`, `role_access.py`) sit at 95-100%. The three modules below the 80% target (`gemini_client.py` 38%, `ollama_client.py` 22%, `mcp_client.py` 64%) are the external LLM/network integration clients whose `ai`-marked tests hit a real paid API and are intentionally excluded from this scope (see CI protocol above) — not an untested gap in business logic.