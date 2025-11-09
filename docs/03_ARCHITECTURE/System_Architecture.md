---
title: "System Architecture"
project: "Theopy – AI Assistant MVP Server"
author: "Adelia Fathipoursasansara (Louis XIV)"
organisation: "Kozea"
period: "2025–2026"
certificate: "RNCP39583 – Expert in Software Development"
---

# System Architecture

## Purpose

This document describes the architecture of **THEOPY** (voice-first + text-enabled server-side AI assistant).  
It explains the data flows, components, failure modes, scaling and deployment notes for both **voice** and **text** processing.

The design aims for a modular, testable and secure middleware that maps natural language (voice/text) to safe Teepy API actions.

---

## High-level architecture (ASCII + Mermaid)

### High-level ASCII


User (microphone / browser chat / CLI)
│
[Ingress API]
(REST / WebSocket)
│
┌─────┴─────────────────────────────────────────────────────────┐
│                         THEOPY Server                         │
│  ┌────────────┐   ┌────────────┐   ┌────────────┐   ┌───────┐ │
│  │  STT / ASR │   │   NLU &   │   │  Intent &  │   │ TTS / │ │
│  │(audio->txt)│──▶│  Parsing  │──▶│ Router/Exec │──▶│ Synthesis│ │
│  └────────────┘   └────────────┘   └────────────┘   └───────┘ │
│        ▲                 │                │                │ │
│        │                 ▼                │                │ │
│  (audio stream)   ┌────────────┐          │                │ │
│                   │Conversation│◀─────────┘                │ │
│                   │  Memory    │                           │ │
│                   └────────────┘                           │ │
│                       │   ▲                                │ │
│                       │   │                                │ │
│                   ┌───┴───┴──┐                             │ │
│                   │Teepy API │◀────────── External Calls ──┘ │
│                   └──────────┘                               │
└──────────────────────────────────────────────────────────────┘
│
Monitoring / Logging / Auth / DB / Admin

````
---

## Components & responsibilities

### 1. Ingress API

* **Type:** REST endpoints + WebSocket for streaming audio and bi-directional conversation.
* **Responsibilities:** accept audio blobs / streaming audio, accept text messages, authenticate requests (API token, JWT), forward to appropriate pipeline (voice / text), send responses (audio file or text message).
* **Endpoints (examples):**

  * `POST /v1/voice` — upload audio file (sync)
  * `WS /v1/stream` — bi-directional streaming for low-latency STT and TTS
  * `POST /v1/chat` — send text command, receive text reply
  * `GET /health` — healthcheck
* **Notes:** Use chunked transfer or streaming for low-latency voice; include request IDs for tracing.

### 2. STT / ASR (Speech-to-Text)

* **Role:** transform audio into text.
* **Options:** Whisper (local/inference), Vosk for local offline, or Whisper API (cloud).
* **Behaviour:**

  * Provide partial transcripts for streaming mode (progressive interpretation).
  * Return final transcript for exact intent parsing.
* **Fallbacks:** If cloud STT fails, fallback to a local model (Vosk).

### 3. Text Preprocessor

* **Role:** Normalise raw text (trim, lowercase, remove filler, simple punctuation handling), detect language, basic sanitisation.
* **Used by:** both STT outputs and user text messages — *unified pipeline* to avoid behavioural drift between voice and text.

### 4. NLU / Intent Extractor

* **Role:** Extract intent, slots/entities, and confidence score.
* **Approach:** Initially rule-based + spaCy for entities; optional LLM function-calling for ambiguous intents.
* **Outputs:** `{ intent: "create_client", entities: {...}, confidence: 0.92 }`
* **Clarification:** If confidence < threshold (e.g. 0.6), produce a clarification prompt rather than performing an action.

### 5. Intent Router & Validator

* **Role:** Validate extracted intent against Teepy capability, check user permissions/scopes, prepare API call (idempotency tokens).
* **Patterns:** Circuit breaker for repeated failures, retry with exponential backoff for transient errors, caching for read calls.
* **Safety:** Validate fields before calling Teepy; apply allow-list for sensitive operations.

### 6. Teepy API Connector

* **Role:** Encapsulate HTTP calls to Teepy, handle authentication (service account / API token), transform responses to a unified format.
* **Resilience:** Retries, timeouts (configurable), rate-limiting safeguards.
* **Audit:** Log every outgoing call with request ID and response summary (no raw audio).

### 7. Response Builder

* **Role:** Build human-friendly textual replies and short spoken templates.
* **Modes:** Text-only reply or text + audio response.
* **Example:** "Created client John Doe for appointment on 2025-11-11 at 14:00."

### 8. TTS (Text-to-Speech)

* **Role:** Convert reply text into audio for voice responses.
* **Options:** pyttsx3 (local), Coqui TTS (local/cloud), cloud TTS for high quality.
* **Fallback:** If TTS fails, return text response only and log incident.

### 9. Conversation Memory

* **Role:** Keep short-term context (session-level): previous intent, last referenced entities, confirmation states.
* **Persistence:** In-memory per session (Redis for scaling), do not store audio; store textual context with retention policy.

### 10. Logging, Monitoring, Audit

* **Logging:** Structured logs (JSON) with request_id, user_id, stage timings (STT, NLU, intent routing, Teepy call, TTS).
* **Monitoring:** Prometheus metrics + Grafana dashboards for latency, error rates, CPU/memory, STT WER trends.
* **Alerting:** Pager/Slack/email on error thresholds (e.g. >10 exceptions/hour, >5% failed commands).

### 11. Auth & Secrets

* **Secrets:** Store API tokens encrypted (Vault, AWS Secrets Manager, or GPG-encrypted `.env` for MVP).
* **Authentication:** Service account token between THEOPY and Teepy; user authentication passed through proxy (if required).

---

## Voice vs Text flow (sequence)

### Voice (streaming) — low latency

1. Client opens WS to `/v1/stream` and streams audio chunks.
2. STT returns partial transcripts; NLU consumes partial transcripts for early intent detection (optimistic).
3. On final transcript, NLU produces definitive intent + entities.
4. Intent Router validates and calls Teepy API.
5. Response Builder creates text reply.
6. TTS synthesises audio and sends back via WS (or the server streams audio progressively).
7. Conversation Memory updated; logs emitted.

### Text (chat) — synchronous

1. Client `POST /v1/chat` with text message.
2. Text Preprocessor normalises text.
3. NLU extracts intent & confidence.
4. Intent Router validates and executes Teepy API calls.
5. Response Builder returns text reply immediately (optionally triggers TTS).
6. Conversation Memory updated; logs emitted.

**Key design decision:** *Use the same NLU + Intent Router pipeline for both voice and text.* This guarantees consistent behaviour.

---

## Failure modes & fallbacks

* **STT timeout or cloud failure:** fallback to local STT or request user to re-send audio; log incident and continue in text mode if available.
* **NLU low confidence:** prompt user with a clarification question instead of acting.
* **Teepy API 5xx / timeout:** retry with exponential backoff (3 attempts); if still failing, report temporary failure and queue the action if it’s idempotent.
* **TTS failure:** return text reply only and log the failure.
* **High resource usage:** reject or queue large audio inputs; scale worker pool horizontally.

---

## Deployment & scaling notes

* **Containerisation:** Docker images for THEOPY main service, STT worker, TTS worker.
* **Orchestration:** Docker Compose for MVP; Kubernetes for production scaling (horizontal autoscaling for STT/TTS workers).
* **DB / Storage:** small PostgreSQL for audit logs & config; Redis for session memory and queues.
* **Health checks:** `/health` and internal `/_internal/health` endpoints for each service; Docker `HEALTHCHECK` in containers.
* **CI/CD:** GitHub Actions for lint, unit tests, integration tests, build image and deploy to staging.
* **Environment variables:** use `THEOPY_ENV`, `TEEPY_API_URL`, `TEEPY_API_TOKEN`, `STT_MODE=local|cloud`, `TTS_MODE=local|cloud`.
* **Secrets:** Do *not* store plain secrets in repo; use secret manager in CI.

---

## Observability & KPIs (operational)

* **Latency (STT→Action→TTS/Text):** target median < 3s (goal), acceptable < 5s for MVP.
* **Command success rate:** target ≥ 70% for MVP.
* **Clarification loop rate:** average ≤ 1 per session.
* **Uptime:** ≥ 99% during working hours (MVP target).
* **WER (STT):** track and keep under 15% for common vocabularies.

---

## Testing strategy

* **Unit tests** for small modules (preprocessing, router, Teepy connector mock).
* **Integration tests** with mocked Teepy API, synthetic audio files (test.wav included).
* **End-to-end tests** for voice flow using local STT/TTS in a staging environment.
* **Load testing** for concurrency on STT workers (simulate N parallel connections).
* **Security tests:** dependency scanning, static analysis, token leak tests.

---



