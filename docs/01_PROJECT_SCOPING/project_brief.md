
```yaml

title: "PROJECT BRIEF"
project: "Theopy – AI Assistant MVP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2025–2026"
certificate: "RNCP39583 – Expert in Software Development"

```

## 1. Project Overview

**Project Name:** Theopy
**Purpose:** To design and implement an **AI assistant MVP server** that enables **Teepy users to interact with Teepy naturally — by voice or by text**.

Theopy allows users to **speak or type commands** to control Teepy, receive information, perform actions, and get spoken or written feedback — all in a fluid, conversational way.

This assistant simplifies daily work on Teepy for people who prefer to communicate rather than navigate menus or forms. It supports both **voice** and **text** input modes.

---

## 2. Context

Kozea’s **Teepy** application is a collaborative communication and management tool used by professionals such as healthcare workers, assistants, and teams to manage their everyday tasks, appointments, and exchanges with clients and colleagues.

However, some users find manual navigation and data entry repetitive, especially when switching between multiple interfaces or devices.

To improve comfort, efficiency, and accessibility, Kozea is developing **Theopy**, a **Python-based AI assistant** that connects directly to Teepy and allows users to **speak or type naturally** to perform their daily actions.

Theopy fits within Kozea’s broader innovation strategy: bringing **AI and voice technologies** into real-world professional tools to make them more intuitive and human.

---

## 3. Objectives

1. **Develop an AI assistant server** that listens to users’ voice or reads their text commands.
2. **Translate those commands into Teepy actions**, such as checking schedules, sending messages, or reading notifications.
3. **Provide two communication modes:**

   * **Voice**: the user speaks, Theopy answers by voice.
   * **Text**: the user writes, Theopy replies in chat.
4. **Integrate natural language understanding (NLU)** to interpret user intent in French.
5. **Ensure smooth integration with Teepy’s existing backend** via secure internal APIs.
6. **Prioritise data privacy and reliability**, offering the possibility to run locally or hybrid.

---

## 4. Target Users

* **Teepy end users:** professionals (especially in healthcare, communication, and insurance worker roles) who use Teepy daily.
* **Kozea’s client organisations:** Pharmacies and offices where staff members want faster, easier access to Teepy features.
* **Accessibility users:** individuals who may prefer or need voice interaction for comfort or inclusivity.

---

## 5. Functional Specifications

### 5.1 Communication Modes


**Voice Mode** --> Users talk naturally to Theopy. It listens, interprets, executes the corresponding Teepy action, and responds 
                   by  voice.           
            
**Text Mode**  --> Users type their request. Theopy interprets it and replies in text within a chat-style    
                      interface.                      

Both modes rely on the same backend intelligence and processing logic.

---

### 5.2 Example Commands

  | User Command                        | Theopy Action                                           |
  | ----------------------------------- | ------------------------------------------------------- |
  | “Show me today’s appointments.”     | Retrieves appointments from Teepy and reads them aloud. |
  | “Send a message to Doctor Martin.”  | Opens the Teepy messaging API and sends the message.    |
  | “What are my unread notifications?” | Lists recent notifications and reads a short summary.   |
  | “Write this down for tomorrow.”     | Adds a note or reminder into the Teepy workspace.       |
  | “Read my last message.”             | Reads out the latest message received.                  |

---

### 5.3 System Capabilities

* **Speech-to-Text (STT):** Converts user voice input into text (using Whisper, Vosk, or SpeechRecognition).
* **Text-to-Speech (TTS):** Generates natural spoken replies (using pyttsx3 or gTTS).
* **Natural Language Understanding (NLU):** Interprets user intent in French to determine the correct action.
* **Conversation Memory:** Keeps short-term context (e.g., “and tomorrow?” after a first question).
* **Error Handling:** Politely requests clarification if the instruction is unclear.

---

## 6. Technical Specifications

| Component              | Technology                               |
| ---------------------- | ---------------------------------------- |
| **Language**           | Python 3.11+                             |
| **Framework**          | Flask                                    |
| **ORM / DB**           | SQLAlchemy + SQLite/PostgreSQL           |
| **Speech Recognition** | Whisper / Vosk / SpeechRecognition       |
| **Voice Synthesis**    | pyttsx3 / gTTS                           |
| **Text Interaction**   | REST API / WebSocket                     |
| **NLU Engine**         | spaCy / rule-based intent classification |
| **Containerisation**   | Docker                                   |
| **Version Control**    | Git (GitHub / GitLab)                    |
| **CI/CD**              | GitHub Actions or GitLab CI              |

---

## 7. Architecture Overview

```
                                        ┌───────────────────────────────┐
                                        │  User (Voice or Text Input)   │
                                        └──────────────┬────────────────┘
                                                       │
                                     ┌─────────────────┴──────────────────┐
                                     │         Theopy Flask Server        │
                                     │------------------------------------│
                                     │  • Speech-to-Text (STT)            │
                                     │  • Natural Language Understanding  │
                                     │  • Command Processor               │
                                     │  • Teepy API Connector             │
                                     │  • Text-to-Speech (TTS)            │
                                     └─────────────────┬──────────────────┘
                                                       │
                                                   [Teepy API]
                                                       │
                                                   [Teepy Server]
```

Theopy acts as an **intelligent intermediary** that interprets user intent (spoken or written), calls the correct Teepy service, and provides a clear and natural response.

---

## 8. Non-Functional Requirements

| Category            | Requirement                                                        |
| ------------------- | ------------------------------------------------------------------ |
| **Performance**     | Real-time voice and text response (<2 seconds for common actions). |
| **Security**        | HTTPS and secure API tokens for internal communication.            |
| **Reliability**     | Automatic reconnection if microphone or network drops.             |
| **Scalability**     | Modular structure for future AI and language extensions.           |
| **Privacy**         | Option for local/offline processing without cloud dependency.      |
| **Maintainability** | Modular Flask Blueprints and well-documented codebase.             |
| **Accessibility**   | Full support for French and English voice commands.                |

---

## 9. Deliverables

1. **Flask-based Theopy MVP server** with both voice and text communication.
2. **Speech recognition and synthesis modules.**
3. **Natural language understanding (NLU) engine.**
4. **Secure integration with Teepy API.**
5. **Text chat and voice interaction interfaces.**
6. **Testing, CI/CD, and Docker deployment.**
7. **User and technical documentation.**

---

## 10. Project Timeline (2025–2026)

| Phase                               | Period  | Deliverables                                         |
| ----------------------------------- | ------- | ---------------------------------------------------- |
| **1. Research & Design**            | Q3 2025 | Architecture, tech stack, NLU & voice tech selection |
| **2. Core Server Setup**            | Q4 2025 | Flask base, endpoints, authentication                |
| **3. Voice & Text Modules**         | Q1 2026 | STT, TTS, and text chat interfaces                   |
| **4. Integration with Teepy**       | Q1 2026 | Secure API connection and commands mapping           |
| **5. Testing & Optimisation**       | Q2 2026 | Tests, performance tuning, CI/CD setup               |
| **6. Documentation & Presentation** | Q2 2026 | Final report and MVP demo                            |

---

## 11. Risks and Mitigation

| Risk                      | Mitigation                                             |
| ------------------------- | ------------------------------------------------------ |
| Voice model latency       | Provide local offline STT/TTS fallback.                |
| Misunderstanding commands | Add clarification prompts or suggestions.              |
| Teepy API changes         | Abstract communication layer for flexibility.          |
| Privacy concerns          | Store no voice logs and use encrypted communication.   |
| Limited time              | Prioritise MVP scope: voice + text loop working first. |

---

## 12. Expected Impact

* Simplifies Teepy for everyday users through **natural voice and text interaction**.
* Reduces time spent navigating menus or typing commands manually.
* Enhances accessibility and inclusivity for all users.
* Strengthens Kozea’s image as an **innovator in AI and usability**.
* Serves as a demonstrative project for the RNCP39583 *Expert en développement logiciel* certification.

---

**This document serves as the official Cahier des Charges for the 2025–2026 Theopy MVP Project.**

