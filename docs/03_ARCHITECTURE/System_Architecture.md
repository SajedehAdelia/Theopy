```yaml

title: "SYSTEM ARCHITECTURE"
project: "Theopy – AI Assistant MVP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2025–2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# System Architecture


This document describes the architecture of **THEOPY** (voice-first + text-enabled server-side AI assistant).
It explains the data flows, components, failure modes, scaling, and deployment notes for both **voice** and **text** processing.

The design aims for a modular, testable, and secure middleware that maps natural language (voice/text) to safe **Teepy API** actions.

---

## High-Level Architecture

### ASCII Overview

```
                                           User (microphone / browser chat / CLI)
                                                            │
                                                      [Ingress API]
                                                   (REST / WebSocket)
                                                            │
                             ┌──────────────────────────────┴────────────────────────────────────┐
                             │                         THEOPY Server                             │
                             │  ┌────────────┐   ┌────────────┐   ┌─────────────┐   ┌─────────┐  │
                             │  │  STT / ASR │   │   NLU &    │   │  Intent &   │   │ TTS /   │  │
                             │  │(audio->txt)│──▶│  Parsing   │──▶│ Router/Exec │──▶│Synthesis│  │
                             │  └────────────┘   └────────────┘   └─────────────┘   └─────────┘  │
                             │        ▲                 │                │                 │     │
                             │        │                 ▼                │                 │     │
                             │  (audio stream)   ┌────────────┐          │                 │     │
                             │                   │Conversation│◀─────────┘                 │     │
                             │                   │  Memory    │                            │     │
                             │                   └────────────┘                            │     │
                             │                       │   ▲                                 │     │
                             │                       │   │                                 │     │
                             │                   ┌───┴───┴──┐                              │     │
                             │                   │Teepy API │◀────────── External Calls ───┘     │
                             │                   └──────────┘                                    │
                             └───────────────────────────────────────────────────────────────────┘
                                                           │
                                        Monitoring / Logging / Auth / DB / Admin
```

## Components & Responsibilities

### 1. Ingress API

* **Type:** REST endpoints + WebSocket for streaming audio and bi-directional conversation.
* **Responsibilities:**

  * Accept audio blobs / streaming audio
  * Accept text messages
  * Authenticate requests (API token, JWT)
  * Forward to appropriate pipeline (voice/text)
  * Send responses (audio or text)
* **Example Endpoints:**

  * `POST /v1/voice` — upload audio file (sync)
  * `WS /v1/stream` — bi-directional streaming
  * `POST /v1/chat` — text command/reply
  * `GET /health` — healthcheck

---

### 2. STT / ASR (Speech-to-Text)

* **Role:** Transform audio into text.
* **Options:** Whisper API
* **Behaviour:**

  * Provide partial transcripts for streaming.
  * Return final transcript for intent parsing.
* **Fallbacks:** Local Vosk model on failure.

---

### 3. Text Preprocessor

* **Role:** Normalise text (trim, lowercase, remove filler, basic punctuation).
* **Used by:** both STT and text messages → unified pipeline.

---

### 4. NLU / Intent Extractor

* **Role:** Extract intent, entities, and confidence.
* **Approach:** Rule-based + spaCy + optional LLM fallback.
* **Output Example:**

  ```json
  { "intent": "create_client", "entities": { "name": "John Doe" }, "confidence": 0.92 }
  ```

---

### 5. Intent Router & Validator

* **Role:** Validate intents, check permissions, and prepare Teepy API calls.
* **Patterns:** Circuit breaker, exponential backoff, caching.
* **Safety:** Field validation + allow-list for sensitive ops.

---

### 6. Teepy API Connector

* **Role:** Handle HTTP calls, authentication, and response transformation.
* **Resilience:** Retries, timeouts, rate limits.

---

### 7. Response Builder

* **Role:** Build user-friendly replies.
* **Modes:** Text-only or text + audio.
* **Example:** “Created client John Doe for 2025-11-11 at 14:00.”

---

### 8. TTS (Text-to-Speech)

* **Role:** Convert reply text to audio.
* **Options:** pyttsx3, Coqui, or cloud TTS.
* **Fallback:** Return text-only reply on failure.

---

### 9. Conversation Memory

* **Role:** Keep short-term session context.
* **Persistence:** Redis for scalability (text-only).

---

### 10. Logging, Monitoring, Audit

* **Logging:** Structured JSON with timing + request IDs.
* **Monitoring:** Prometheus + Grafana dashboards.
* **Alerting:** Pager/Slack/email for high error rates.

---

### 11. Auth & Secrets

* **Secrets:** Vault / AWS Secrets Manager / GPG `.env`.
* **Authentication:** Service tokens (Theopy↔Teepy).

---

## Eco-Design & Green IT Strategy

Theopy is designed with a **frugal computing** approach to minimize its carbon footprint and energy consumption:

* **Model Quantization:** We use **quantized AI models** (Whisper/spaCy) to reduce CPU cycles and memory usage by up to 4x, significantly lowering energy consumption during inference.
* **Trigger-Based Processing:** High-power processing is only activated upon voice detection (VAD), ensuring the server remains in a low-power state when idle.
* **Resource Optimization:** Docker containerization ensures the application only requests necessary resources, allowing for high-efficiency hosting with low Power Usage Effectiveness (PUE).
* **Intelligent Caching:** A caching layer for common intents avoids redundant AI inference cycles for identical user queries.

---

## Digital Accessibility (RGAA & OPQUAST)

While voice interaction is a primary accessibility feature, the system adheres to formal digital standards:

* **RGAA (Référentiel Général d’Amélioration de l’Accessibilité):** The web interface complies with RGAA 4.1. This includes keyboard-only navigation for all actions and proper ARIA labels so screen readers can interpret real-time AI responses.
* **OPQUAST Compliance:** We follow Web Quality Assurance rules to ensure a predictable user experience.
  * **Rule #74:** All voice-generated content is accompanied by a text alternative.
  * **Rule #101:** Users are always provided with a visual status indicator (e.g., "Theopy is listening...") to maintain context and control.

---

## Voice vs Text Flow

### Voice (Streaming, Low Latency)

1. Client opens WS `/v1/stream`.
2. STT returns partial transcripts.
3. NLU detects intents early.
4. Router validates + calls Teepy API.
5. Response Builder formats reply.
6. TTS synthesises and streams audio.
7. Memory updated + logs emitted.

### Text (Synchronous)

1. Client `POST /v1/chat`.
2. Text Preprocessor normalises input.
3. NLU extracts intent.
4. Router validates + executes.
5. Response returned (text or audio).
6. Memory + logs updated.

**Key design:** Same NLU + Intent Router for both voice and text.

---

## Failure Modes & Fallbacks

| Failure            | Fallback                        |
| ------------------ | ------------------------------- |
| STT timeout        | Local STT or ask user to resend |
| NLU low confidence | Clarification prompt            |
| Teepy API error    | Retry (3x, exponential backoff) |
| TTS failure        | Text-only reply                 |
| High CPU/memory    | Queue or reject input           |

---

## Deployment & Scaling

* **Containerisation:** Docker (main, STT, TTS).
* **Orchestration:** Docker Compose (MVP) → Kubernetes (prod).
* **Storage:** PostgreSQL (audit/config), Redis (sessions).
* **CI/CD:** GitHub Actions → lint, tests, build, deploy.
* **Env vars:**

  ```
  THEOPY_ENV=staging
  TEEPY_API_URL=https://api.teepy.io
  TEEPY_API_TOKEN=secret
  STT_MODE=local|cloud
  TTS_MODE=local|cloud
  ```

---

## Observability & KPIs

| Metric                   | Target                  |
| ------------------------ | ----------------------- |
| Latency (STT→Action→TTS) | < 3s (goal), < 5s (MVP) |
| Command success rate     | ≥ 70%                   |
| Clarification loop rate  | ≤ 1 per session         |
| Uptime                   | ≥ 99%                   |
| STT WER                  | ≤ 15%                   |

---

## Testing Strategy

* **Unit Tests:** Preprocessing, router, Teepy mock.
* **Integration:** Mocked API + synthetic audio.
* **End-to-End:** Full voice flow on staging.
* **Load Tests:** Concurrent STT streams.
* **Security:** Static analysis + token leak detection.( Needs checking with Julien and kozea group  )

