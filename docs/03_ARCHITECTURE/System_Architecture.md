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



### 3. Intelligence Layer (Google Gemini API)

* **Role:** The external Large Language Model (LLM) engine.


* **Tech Stack:** `google-genai` SDK.


* **Responsibility:** Performs strict "Function Calling". It translates the natural language prompt into a structured JSON tool call (e.g., triggering `agent_invoices_summary`). It later synthesizes the raw database results into a human-readable reply.



### 4. Teepy Backend (MCP Server)

* **Role:** The ERP application exposing its business intelligence securely.


* **Tech Stack:** Python 3, Flask, FastMCP Server.


* **Responsibility:** Validates the tool request, establishes a secure database context, and executes the business logic.



### 5. Database

* **Role:** The core enterprise data storage.


* **Tech Stack:** PostgreSQL, SQLAlchemy ORM.


* **Responsibility:** Ensures all queries are parameterized and safe. The AI never has direct SQL generation access, eliminating context leakage risks.



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