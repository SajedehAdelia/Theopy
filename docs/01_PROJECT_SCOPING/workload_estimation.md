```yaml
title: "WORKLOAD ESTIMATION"
project: "Theopy – AI Assistant MVP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2025–2026"
certificate: "RNCP39583 – Expert in Software Development"
```

# Workload Estimation

## 1. Methodology
This estimation uses the **Fibonacci sequence** (1, 2, 3, 5, 8, 13, 21) to evaluate the complexity of each User Story or technical task.
- **1 point** ≈ 0.5 Man-Day (MD)
- **Velocity:** Estimated at 10 points per week (part-time project).

## 2. Detailed Estimation

### Phase 1: Research & Setup (Sprint 0)
| ID | Task / User Story | Points | Est. Days |
|----|-------------------|--------|-----------|
| T1 | Define architecture and select tech stack | 8 | 4.0 |
| T2 | Set up Git repo, Docker environment, and CI/CD pipeline | 13 | 6.5 |
| T3 | Research STT/TTS libraries (Whisper, Vosk, pyttsx3) | 8 | 4.0 |
| **Total** | | **29** | **14.5** |

### Phase 2: Core Server Development (Sprint 1-2)
| ID | Task / User Story | Points | Est. Days |
|----|-------------------|--------|-----------|
| US1 | As a dev, I want a basic Flask server with health endpoints | 5 | 2.5 |
| US2 | As a user, I want to authenticate via API token | 8 | 4.0 |
| US3 | As a dev, I want to connect to the Teepy API (mock/real) | 13 | 6.5 |
| US4 | As a dev, I want a database schema for logs and users | 8 | 4.0 |
| **Total** | | **34** | **17.0** |

### Phase 3: Voice & Text Modules (Sprint 3-4)
| ID | Task / User Story | Points | Est. Days |
|----|-------------------|--------|-----------|
| US5 | As a user, I want to send text and get a text reply | 13 | 6.5 |
| US6 | As a user, I want to send an audio file and get a transcript (STT) | 21 | 10.5 |
| US7 | As a user, I want to receive an audio reply (TTS) | 13 | 6.5 |
| US8 | As a dev, I want to implement basic NLU (intent detection) | 21 | 10.5 |
| **Total** | | **68** | **34.0** |

### Phase 4: Integration & Polish (Sprint 5-6)
| ID | Task / User Story | Points | Est. Days |
|----|-------------------|--------|-----------|
| US9 | As a user, I want to stream audio for faster response (WebSocket) | 21 | 10.5 |
| US10 | As a user, I want the assistant to remember my last question | 13 | 6.5 |
| T4 | Write documentation (User & Technical) | 13 | 6.5 |
| T5 | Final testing, bug fixing, and optimization | 21 | 10.5 |
| **Total** | | **68** | **34.0** |

## 3. Summary

| Phase | Total Points | Estimated Man-Days |
|-------|--------------|--------------------|
| 1. Research & Setup | 29 | 14.5 |
| 2. Core Server | 34 | 17.0 |
| 3. Voice & Text Modules | 68 | 34.0 |
| 4. Integration & Polish | 68 | 34.0 |
| **GRAND TOTAL** | **199** | **99.5 Days** |

**Note:** This represents approximately **5 months of full-time work** (based on ~20 working days/month) or **8-10 months of part-time work**.
