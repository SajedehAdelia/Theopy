---
title: "Technical Risk Mapping and Incident Monitoring"
project: "Theopy – AI Assistant MVP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2025–2026"
certificate: "RNCP39583 – Expert en développement logiciel"
---

#  Technical Risk Mapping and Incident Monitoring

## 1. Purpose

This document identifies and evaluates **technical and operational risks** for the *Theopy* project.  
It defines **monitoring indicators**, **risk levels**, and **mitigation strategies** to ensure system reliability, data protection, and service continuity.

The objective is to **anticipate incidents**, **minimise impact**, and **maintain secure and stable operation** during the MVP lifecycle.

---

## 2. Risk Evaluation Scale

| Level | Probability | Impact | Description |
|-------|--------------|--------|-------------|
| 🔵 **Low** | Rare, unlikely to occur | Minor service degradation | No data loss, minor delay |
| 🟡 **Medium** | Possible, occurs occasionally | Partial functionality loss | Temporary disruption |
| 🔴 **High** | Likely or recurrent | Critical impact | Data loss or major downtime |

---

## 3. Technical Risk Mapping

| **Risk**  | **Description** | **Impact** | **Probability** | **Indicators** | **Mitigation Measures** |
|-----------|----------------|-------------|-----------------|----------------|--------------------------|
| **Database data loss** | Loss of user or configuration data due to crash or improper shutdown | 🔴 High | 🟡 Medium | Error logs, failed SQLAlchemy commits, missing records | - Automated daily backups <br> - Test restoration weekly <br> - Use PostgreSQL transactions |
| **Flask server downtime** | Service interruption caused by unexpected crash, overload, or Docker failure | 🔴 High | 🟡 Medium | Uptime monitoring, health checks, CI/CD logs | - Docker `HEALTHCHECK` and restart policy <br> - Nginx reverse proxy fallback <br> - Error alerting via email/Slack |
| **Speech recognition (STT) failure** | Whisper/Vosk engine crash or high latency blocking user input | 🟡 Medium | 🟡 Medium | Exception logs, recognition timeout errors | - Implement local fallback (Vosk) <br> - Graceful error handling and retry <br> - Cached responses for common commands |
| **Text-to-speech (TTS) module failure** | gTTS/pyttsx3 service unresponsive or disconnected | 🟡 Medium | 🟡 Medium | Missing audio response, log error rate | - Retry mechanism <br> - Offline fallback (pyttsx3) <br> - Health endpoint for TTS module |
| **API communication failure (Teepy backend)** | Request timeout or authentication failure with Teepy APIs | 🔴 High | 🟡 Medium | HTTP 4xx/5xx logs, timeout alerts | - API retry with exponential backoff <br> - Circuit breaker pattern <br> - Cache for non-critical requests |
| **Security vulnerability** | Token exposure, unauthorised access, or SSL misconfiguration | 🔴 High | 🔵 Low | Security scan results, audit logs | - Enforce HTTPS/TLS 1.2+ <br> - Rotate API tokens regularly <br> - Add authentication middleware |
| **Dependency version break** | Update in Python or external library causes incompatibility | 🟡 Medium | 🟡 Medium | CI pipeline failure, dependency audit logs | - Lock dependencies with `requirements.txt` <br> - Use staging environment for updates <br> - Automated tests before deployment |
| **High CPU or memory usage** | Overload during audio processing or large model inference | 🟡 Medium | 🟡 Medium | System metrics, resource usage >80% | - Optimise STT model load time <br> - Use async tasks <br> - Monitor with Prometheus/Grafana |
| **Network disconnection** | User or server loses connectivity during voice session | 🟡 Medium | 🟡 Medium | Connection timeout logs | - Reconnect automatically <br> - Resume previous session state <br> - Local message caching |
| **NLU misinterpretation** | Wrong intent classification leading to incorrect actions | 🟡 Medium | 🔴 High | Intent error logs, user feedback rate | - Expand training set <br> - Add user clarification prompts <br> - Log and analyse false positives |

---

## 4. Incident Monitoring and Control

| **Category**             | **Monitoring Indicator** | **Tool / Method**            | **Alert Threshold**    |
| ------------------------ | ------------------------ | ---------------------------- | ---------------------- |
| **Server health**        | Uptime %                 | Docker healthcheck / Pingdom | < 99.5% uptime         |
| **API response**         | Response time (ms)       | Flask logs / Grafana         | > 2000 ms              |
| **STT accuracy**         | Word Error Rate (WER)    | STT benchmark logs           | > 15%                  |
| **TTS response time**    | Generation latency (s)   | Flask endpoint logs          | > 3s                   |
| **Database reliability** | Backup validation        | Cron + test restore logs     | Failure detected       |
| **Security**             | Token usage anomalies    | Auth logs / IDS              | Unexpected token reuse |
| **Error rate**           | Exception count per hour | Sentry / Logging system      | > 10/hour              |
| **CPU usage**            | CPU % average            | Prometheus / Docker stats    | > 80% sustained        |

---

## 5. Incident Response Procedure

| **Step**         | **Action**                                  | **Responsible**      | **Documentation**                   |
|------------------|---------------------------------------------|----------------------|-------------------------------------|
| **Detection**    | Incident detected by monitoring or alert    | Developer on duty    | System logs, CI/CD reports          |
| **Notification** | Notify responsible engineer via Slack/email | DevOps or maintainer | Incident log entry                  |
| **Diagnosis**    | Analyse logs and metrics                    | Developer            | Root cause report                   |
| **Resolution**   | Apply fix or rollback                       | Developer / Ops      | Corrective action note              |
| **Validation**   | Confirm fix effectiveness                   | QA                   | Test report                         |
| **Post-mortem**  | Document causes and prevention plan         | Project lead         | Incident report (Notion or Markdown)|

---

## 6. Recommendations

- Maintain **automated backups** and **infrastructure monitoring** to minimise downtime.  
- Use **local fallback modules** for STT/TTS to ensure offline resilience.  
- Integrate **real-time alerting** (Slack/email) for system failures.  
- Run **dependency and security audits** in CI/CD pipelines.  
- Log every incident under `docs/incidents/` for full traceability.


