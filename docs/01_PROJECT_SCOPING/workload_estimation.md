```yaml
title: "WORKLOAD ESTIMATION"
project: "Theopy – AI Assistant MCP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# Workload Estimation

## 1. Methodology

This estimation calculates the required workload in **Man-Days (J/H)** for the initial MVP build. The project is structured around a fast-paced **10-Week Startup Model** (10 Semaines / Modèle Startup). The workload is distributed among three specific technical roles: Lead Backend, Frontend Developer, and DevOps/SecOps.

## 2. Detailed Estimation by Phase

### Phase 1: Scoping & Infra (Weeks 1-2)

*Focus: Architecture definition, repository setup, and initial infrastructure configuration.*

| Module / Functionality | Responsible | Est. Man-Days (J/H) |
| --- | --- | --- |
| Scoping, architecture & project setup (Docker, CI/CD pipelines)

 | Lead Backend

 | 8

 |

### Phase 2: MCP Server (Weeks 3-6)

*Focus: Building the core backend capabilities, database security, and network bridge.*

| Module / Functionality | Responsible | Est. Man-Days (J/H) |
| --- | --- | --- |
| Implementation of FastMCP Server & exposure of ERP tools

 | Lead Backend

 | 15

 |
| Database security (SQLAlchemy configuration, isolated sessions)

 | Lead Backend

 | 10

 |
| Asynchronous network bridge (SSE API development & MCP client)

 | Lead Backend

 | 12

 |

### Phase 3: Front & LLM (Weeks 4-8)

*Focus: AI integration, UI creation, and real-time client synchronization.*

| Module / Functionality | Responsible | Est. Man-Days (J/H) |
| --- | --- | --- |
| LLM Integration (Google Gemini SDK, prompt engineering & JSON routing)

 | Lead Backend

 | 15

 |
| Web Interface (Design & integration of Theopy UI)

 | Dev Front

 | 5

 |
| Real-time synchronization (SSE stream consumption on the client side)

 | Dev Front

 | 15

 |

### Phase 4: Deployment (Weeks 9-10)

*Focus: Finalizing the infrastructure, testing, and release preparation.*

| Module / Functionality | Responsible | Est. Man-Days (J/H) |
| --- | --- | --- |
| Deployment & infrastructure (Hardening inter-container network, VPS)

 | DevOps

 | 8

 |
| Load tests, network debugging (TaskGroup) & final acceptance (UAT)

 | DevOps

 | 4

 |

---

## 3. Workload Summary by Role

| Role | Total Man-Days (J/H) | Equivalent Duration |
| --- | --- | --- |
| **Lead Backend**<br> | 60

 | ~2.5 Months

 |
| **Dev Front**<br> | 20

 | ~1.5 Months

 |
| **DevOps / SecOps**<br> | 12

 | 12 Days (Part-time)

 |
| **GRAND TOTAL**<br> | **92 J/H**<br> | **10 Weeks**<br> |
