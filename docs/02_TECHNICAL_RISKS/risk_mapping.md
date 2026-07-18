```yaml
title: "TECHNICAL RISK MAPPING AND INCIDENT MONITORING"
project: "Theopy – AI Assistant MCP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# Technical Risk Mapping and Incident Monitoring

## 1. Purpose

This document identifies and evaluates **technical and operational risks** for the *Theopy* project, specifically adapted for its Hub & Spoke MCP architecture.
It defines **monitoring indicators**, **risk levels**, and **mitigation strategies** to ensure system reliability, data protection, and service continuity.

The objective is to **anticipate incidents**, **minimise impact**, and **maintain secure and stable operation** during the MCP Server lifecycle.

---

## 2. Risk Evaluation Scale

| Level | Probability | Impact | Description |
| --- | --- | --- | --- |
| 🔵 **Low** | Rare, unlikely to occur | Minor service degradation | No data loss, minor delay |
| 🟡 **Medium** | Possible, occurs occasionally | Partial functionality loss | Temporary disruption |
| 🔴 **High** | Likely or recurrent | Critical impact | Data loss or major downtime |

---

## 3. Technical Risk Mapping

Based on the architectural audit, the following specific risks have been identified:

| **Risk** | **Description** | **Probability** | **Impact** | **Mitigation Measures** |
| --- | --- | --- | --- | --- |
| **Infrastructure: Port Conflicts** | Network port conflicts between different local containers.

 | 🔴 High

 | 🔵 Low

 | Strict mapping via Docker and creation of an isolated network bridge for inter-container communication.

 |
| **Network: SSE Disconnection** | The Server-Sent Events (SSE) asynchronous stream drops during long LLM inference or inactivity. | 🔴 High

 | 🟡 Medium

 | Implement robust client-side reconnection logic and proper `AsyncExitStack` teardowns in `dispatcher.py`. |
| **AI Hallucination** | The LLM misinterprets the prompt and generates a malformed tool call or hallucinates financial data.

 | 🔴 High

 | 🔴 High

 | Force strict Function Calling (JSON routing) via the Google Gemini SDK. Ensure zero direct SQL access for the AI.

 |
| **Vendor Lock-in (Dependency)** | Being trapped with a single AI provider, making it difficult to switch if pricing or APIs change.

 | 🟡 Medium | 🟡 Medium | Keep all business intelligence in Teepy. Theopy acts strictly as an interchangeable router.

 |
| **Security: Credential Leak** | Leakage of API keys or database credentials leading to unauthorized access.

 | 🔵 Low

 | 🔴 High

 | Dynamic environment injection (`.env`). Theopy and Teepy will refuse to start if keys are missing (Fail-Fast).

 |
| **External: Google SSL Updates** | Sudden changes to Google API SSL certificates breaking the SDK connection. | 🔵 Low

 | 🔵 Low

 | Lock SDK versions via `requirements.txt` and monitor Google Cloud developer announcements.

 |

---

## 4. Incident Monitoring and Control (KPIs)

To validate the architecture, these specific indicators are monitored:

| **Category** | **Monitoring Indicator** | **Tool / Method** | **Alert Threshold / Target** |
| --- | --- | --- | --- |
| **AI Performance** | AI Response Time

 | Flask logs / Sentry | > 4 seconds

 |
| **Routing Quality** | Routing Accuracy (Function Calling)

 | Testing Suite / Logs | < 95% accuracy

 |
| **Software Integrity** | Unit Test Coverage

 | Pytest / CI Pipeline | < 80% coverage

 |
| **Security** | SQL Context Leakage

 | SQLAlchemy Logs / IDS | Any leakage detected (Target: Zero)

 |
| **System Stability** | Exception count | `sentry-sdk[flask]` | > 5 unhandled exceptions/hour |
| **Network** | SSE Connection Drops | Nginx / Docker logs | > 10 drops per session |

---

## 5. Incident Response Procedure

| **Step** | **Action** | **Responsible** | **Documentation** |
| --- | --- | --- | --- |
| **Detection** | Incident detected by Sentry alert, CI failure, or user report | Lead Backend | System logs, GitHub Actions reports |
| **Diagnosis** | Analyse the SSE streams, tool calls, and PostgreSQL locks | Lead Backend | Root cause analysis |
| **Resolution** | Apply fix (e.g., update `AsyncMock` in tests, rollback container) | Lead Backend / DevOps | Commit message / Changelog |
| **Validation** | Run the Pytest suite locally and in CI to confirm resolution | DevOps | Test coverage report |
| **Post-mortem** | Document the bug and the correction plan for RNCP validation | Project Owner | `Plan_de_correction.md` |

---

## 6. Recommendations

* **Fail-Fast Initialization:** Maintain strict `.env` validation on startup to prevent insecure boots.


* **Network Isolation:** Never expose the MCP ports publicly; rely exclusively on the Docker internal bridge for Teepy-Theopy communication.


* **LLM Agnosticism:** Ensure all new tools added to Teepy follow standard MCP schemas so the LLM engine can be swapped without code refactoring.


* **Error Tracking:** Rely on `sentry-sdk` to automatically catch asynchronous `TaskGroup` crashes and SSE timeout errors.