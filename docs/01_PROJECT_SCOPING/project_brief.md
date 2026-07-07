```yaml
title: "PROJECT BRIEF"
project: "Theopy – AI Assistant MVP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

## 1. Project Overview

**Project Name:** Theopy
**Purpose:** To design and implement an **intelligent natural language routing engine** that enables users to interact with the Teepy ERP seamlessly.

Theopy allows users to use simple, natural sentences to query, manipulate, and utilize the ERP database to retrieve complex data (e.g., an accounting summary) in under 5 seconds.

---

## 2. Context

Kozea’s **Teepy** application is a collaborative management tool. Currently, manual data retrieval—such as searching for specific pharmacy invoices from past years—is laborious and requires multiple clicks and filters. This repetitive task load reduces back-office lunch breaks by 50% and limits the time available for high-value tasks.

To solve this, Kozea is developing **Theopy**. Instead of integrating AI directly into the legacy code (which poses severe security risks), Theopy acts as an independent, autonomous AI agent. It uses a modern "Hub & Spoke" architecture via the Model Context Protocol (MCP) to securely interact with Teepy.

The strategic objective is to restore availability and well-being (QVT) to employees by automating simple interactions with the Teepy software.

---

## 3. Target Users & Stakeholders

* **End Users:** Back-office teams (e.g., accounting, billing) who require rapid data extraction.


* **Sponsor (Management):** Aims to optimize internal processes and create a scalable AI architecture that can be pitched to future investors.


* **Technical Team:** Developers who require secure integration without disrupting the Teepy legacy code, utilizing a modular vision for future projects.



---

## 4. Technical Specifications

The architecture is entirely decoupled, making the LLM engine interchangeable (Gemini, Claude, etc.) without altering the core business applications.

| Component | Technology |
| --- | --- |
| **Front-end** | HTML5 / CSS3, Vanilla JavaScript, Jinja2 template engine

 |
| **Back-end** | Python 3, Flask framework

 |
| **Database & Modeling** | PostgreSQL, SQLAlchemy ORM

 |
| **AI & Protocols** | Google Gemini SDK (`google-genai`), FastMCP (Model Context Protocol), SSE (Server-Sent Events) network streams

 |
| **Infra & Environment** | Docker & Docker Compose, Linux, GNU Make

 |

---

## 5. Architecture Overview

The project relies on a secure **"Hub & Spoke" architecture**:

1. The user sends a prompt via the UI.
2. Theopy (MCP Client) sends the prompt and the list of available tools to the Google Gemini API.


3. Gemini detects the intent and returns a JSON Tool Call.


4. Theopy executes an HTTP SSE request to the Teepy backend (MCP Server).


5. Teepy runs a secured SQL query via SQLAlchemy, fetches the raw data, and streams it back via SSE.


6. Theopy feeds the ERP data back to the LLM, which synthesizes a natural language response for the user.



---

## 6. Success Indicators (KPIs)

To validate the MVP, the following metrics must be achieved:

* **AI Response Time:** < 4 seconds.


* **Routing Accuracy (Function Calling):** > 95%.


* **Unit Test Coverage:** 80%.


* **Security:** Zero SQL context leakage.



---

## 7. Deliverables

By the end of the project, the following assets will be delivered to validate the RNCP39583 software expertise requirements:

1. Complete source code of the Theopy agent.


2. Integrated Teepy MCP Server.


3. Fully operational CI/CD pipelines.



---

## 8. Environmental Impact

Theopy is designed with software sobriety in mind:

* **Compute Delegation:** Heavy AI processing is delegated on-demand to the Google Gemini API, avoiding energy-intensive 24/7 local GPU servers.


* **Network Efficiency:** Server-Sent Events (SSE) maintain a single, lightweight connection, eliminating CPU-heavy polling.


* **Infrastructure Sobriety:** Lightweight Docker containerization optimizes VPS hardware usage compared to full virtual machines.



---

## 9. Project Timeline: 10-Week Startup Model

The project is executed in a highly focused 10-week sprint, divided into overlapping phases:

* **Phase 1: Scoping & Infra (Weeks 1-2 | Jun 21 - Jul 05)**

* Architecture definition & Repo setup (Back/Front).


* AWS/VPS & Docker configuration.




* **Phase 2: MCP Server (Weeks 3-6 | Jul 05 - Aug 02)**

* FastMCP & ERP Tools implementation.


* PostgreSQL session security.


* SSE sync API development.




* **Phase 3: Front & LLM (Weeks 4-8 | Jul 12 - Aug 16)**

* UI interface creation.


* Gemini SDK integration & AI Routing.


* Client-side SSE consumption.




* **Phase 4: Deployment (Weeks 9-10 | Aug 02 - Aug 16)**

* Network hardening & CI/CD pipeline.


* End-to-End (E2E) testing & error management.


* User Acceptance Testing (UAT) & V1 Release.