# 🧾 Cahier des Charges — Theopy

**Project Period:** 2025–2026
**Author:** Louis XIV (Adelia Fathipoursasansara)
**Organisation:** Kozea
**Certificate Reference:** RNCP39583 – *Expert en développement logiciel*

---

## 1. Project Overview

**Project Name:** Theopy
**Purpose:** To design and implement an **AI assistant server** that enables **Teepy users to communicate with Teepy using natural voice commands**.

Theopy provides a seamless, conversational interface for Teepy — the professional software testing platform developed by Kozea — allowing users to perform tasks such as launching tests, querying results, managing test environments, and receiving spoken feedback, **without needing to use the graphical interface or terminal commands**.

---

## 2. Context

Kozea’s **Teepy** application is a powerful internal tool for managing and automating software testing workflows. However, its users often perform repetitive or manual tasks through command-line or browser-based interfaces.

To improve accessibility, efficiency, and ease of use, Kozea is developing **Theopy**, a Python-based AI assistant that allows users to **control Teepy by voice**, using natural language understanding (NLU) and speech recognition.

This project also contributes to the larger AI automation strategy within Kozea, aligning with the company’s vision to make complex tools intuitive and human-friendly.

---

## 3. Objectives

1. **Develop an AI assistant server** capable of understanding and executing Teepy-related voice commands.
2. **Integrate speech-to-text and text-to-speech** functionalities for two-way vocal interaction.
3. **Interface seamlessly with Teepy’s backend** via secure APIs.
4. **Provide contextual understanding**, allowing users to perform chained or follow-up voice commands.
5. **Ensure privacy and reliability**, with local or hybrid AI processing to protect sensitive data.

---

## 4. Target Users

* **Teepy end users:** primarily Kozea developers, testers, and product engineers.
* **Project managers and QA engineers:** who need quick summaries or reports via voice.
* **Future Kozea clients:** when Theopy is later exposed as a smart testing companion.

---

## 5. Functional Specifications

### 5.1 Voice Interaction Features

* Speech recognition (STT) using a local or cloud-based model (e.g., Whisper).
* Voice synthesis (TTS) for spoken responses.
* Natural Language Understanding (NLU) to interpret intent and extract relevant entities (e.g., “Fetch me all the invoices”).
* Context awareness (handling follow-up commands such as “and show me the payment”).
* Error handling and graceful fallbacks for unrecognised commands.

### 5.2 Core Voice Commands Examples

| Command (User)                                  | Action (Theopy)                         |
| ----------------------------------------------- | --------------------------------------- |
| “Showme the invoice from 23/10/2024”            | Launches `teepy run all`.               |
| “Show me the latest payments of Madame Debois.” | Queries Teepy’s API for recent results. |
| “How many sessions we have for today?”          | Retrieves and summarises failure count. |
| “Read me the summary.”                          | Reads aloud the summary report.         |
| “Go to Madame Debois's profile”                 | Sends interruption command to Teepy.    |

### 5.3 API and Integration

* REST or WebSocket endpoints exposed by Theopy for:

  * Command parsing
  * Voice transcription
  * Teepy execution requests
  * Result retrieval
* Connection to Teepy via internal secured API (Flask-based communication).

### 5.4 User Interface (Optional)

* Theopy runs as a **server application** (no mobile or desktop GUI).
* Can be triggered from:

  * A **web dashboard microphone button** inside Teepy, or
  * A **voice terminal** CLI mode (`theopy --listen`).

---

## 6. Technical Specifications

| Component              | Technology                             |
| ---------------------- | -------------------------------------- |
| **Language**           | Python 3.11+                           |
| **Framework**          | Flask                                  |
| **ORM / DB**           | SQLAlchemy + SQLite/PostgreSQL         |
| **Speech Recognition** | Whisper / Vosk / SpeechRecognition     |
| **Voice Synthesis**    | pyttsx3 / gTTS                         |
| **AI Understanding**   | NLP or LLM-based intent classification |
| **Testing Framework**  | pytest                                 |
| **Containerisation**   | Docker                                 |
| **Version Control**    | Git (GitHub / GitLab)                  |
| **CI/CD**              | GitHub Actions or GitLab CI            |

---

## 7. Architecture Overview

```
[User Voice] → [Microphone / Web Audio]
       ↓
[Speech-to-Text Engine]
       ↓
[Theopy Flask Server] → [Intent Recognition] → [Teepy API]
       ↓
[Response Formatter]
       ↓
[Text-to-Speech Output → User]
```

Theopy acts as a **middleware AI layer** between user speech and Teepy’s internal APIs.
All communications are authenticated and encrypted.

---

## 8. Non-Functional Requirements

| Category            | Requirement                                                         |
| ------------------- | ------------------------------------------------------------------- |
| **Performance**     | Real-time voice response with max 2s latency for standard commands. |
| **Security**        | Use secure tokens and HTTPS for API calls; anonymise voice logs.    |
| **Scalability**     | Modular architecture allowing future AI model integration.          |
| **Reliability**     | Automatic reconnection for microphone and API streams.              |
| **Privacy**         | Optional offline mode using local speech models (no cloud upload).  |
| **Maintainability** | Clear modular Flask blueprint structure with unit tests.            |
| **Accessibility**   | Support for French and English voice commands.                      |

---

## 9. Deliverables

1. **Theopy Flask server** with full API endpoints.
2. **Speech recognition and synthesis modules.**
3. **AI intent classification module** (simple rule-based → expandable to LLM).
4. **Integration with Teepy API.**
5. **Unit and integration tests.**
6. **Dockerfile + CI pipeline.**
7. **Technical documentation and installation guide.**

---

## 10. Project Timeline (2025–2026)

| Phase                           | Period  | Deliverables                        |
| ------------------------------- | ------- | ----------------------------------- |
| **1. Research & Design**        | Q3 2025 | Architecture, voice tech selection  |
| **2. Core API Development**     | Q4 2025 | Flask server, SQLAlchemy models     |
| **3. Speech & NLU Integration** | Q1 2026 | Voice recognition, intent detection |
| **4. Teepy Integration**        | Q1 2026 | Secure communication with Teepy     |
| **5. Testing & Optimisation**   | Q2 2026 | Unit tests, CI/CD setup             |
| **6. Documentation & Demo**     | Q2 2026 | Deployment guide, presentation      |

---

## 11. Risks and Mitigation

| Risk                        | Mitigation                                                  |
| --------------------------- | ----------------------------------------------------------- |
| High latency from cloud STT | Offer local model fallback (Whisper/Vosk).                  |
| Speech misrecognition       | Implement correction and confirmation prompts.              |
| API changes in Teepy        | Keep abstraction layer between Theopy and Teepy API.        |
| Security concerns           | Use internal access keys and secure communication channels. |

---

## 12. Expected Impact

* Improves Teepy’s **usability** and **accessibility**.
* Increases productivity for developers through hands-free control.
* Strengthens Kozea’s **AI innovation** portfolio.
* Demonstrates advanced software engineering for **RNCP “Expert en développement logiciel.”**
