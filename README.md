# Theopy AI

Theopy is a professional AI assistant gateway designed for Teepy (Kozea). It streamlines workflows by helping Kozea manage invoices and tiers-payant processes efficiently. Built with modern, scalable technologies, Theopy provides both a user-friendly web interface and a robust API backed by Google's Gemini models.

---

## 🚀 Features

- **AI Chatbot Gateway:** Seamlessly interact with Google's Gemini AI (`gemini-2.5-flash`) via the core REST API (`/v1/chat`).
- **Web Interface:** Dynamic, responsive UI rendered via Jinja2 templates (`/`).
- **Voice Functionality:** Integrated Speech-to-Text (`src/speech_to_text.py`) capturing user audio for transcription.
- **Frontend Asset Pipeline:** Automated compiling of Sass to CSS on startup.
- **DevOps Ready:** Fully containerized with Docker, featuring an integrated `/health` DevOps monitoring endpoint.
- **Automated Testing:** Unit testing configuration available via `pytest`.

## 🛠️ Technology Stack

- **Backend:** Python 3, Flask, Werkzeug
- **AI Integration:** Google Generative AI (Gemini API)
- **Frontend:** HTML5, Jinja2, SCSS/Sass
- **Voice Recognition:** SpeechRecognition, PyAudio
- **Infrastructure:** Docker, Docker Compose, Make

## 📋 Prerequisites

To run this project, make sure you have the following installed on your system:
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- `make` (for running local automation commands)
- (Optional) Python 3.10+ if running locally without Docker.

---

## ⚙️ Local Setup (Virtual Environment)

Before running the project locally, set up a local virtual environment to isolate your dependencies and avoid "Externally Managed Environment" errors.

1. **Create and Activate the Environment**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Configure Environment Variables**
Create a `.env` file in the root directory:
```text
GEMINI_API_KEY=your_key_here
```
*(Optional)* Add `MIC_INDEX=` if you need to point PyAudio to a specific default microphone index for the speech-to-text integration.

---

## 🐳 Running with Docker

The easiest way to run the full Theopy system is via Docker. This ensures all services (Flask, AI logic, etc.) run in a consistent environment.

| Action | Command |
| --- | --- |
| **Start System** | `make docker-up` |
| **Stop System** | `make docker-down` |
| **View Logs** | `make logs` |
| **Run Tests** | `make test` |
| **Reset/Clean** | `make docker-clean` |

---

## 🗂️ Project Structure

```text
Theopy/
├── src/
│   ├── static/          # Sass/CSS styling and static web assets
│   ├── templates/       # Jinja2 HTML templates for the UI
│   ├── tests/           # Pytest definitions 
│   ├── app.py           # Main Flask application and Gemini AI logic
│   └── speech_to_text.py# Voice interaction handling script
├── Dockerfile           # Container blueprint
├── docker-compose.yml   # Multi-container orchestration (Theopy service)
├── Makefile             # Make targets for development lifecycle
├── requirements.txt     # Python dependencies
└── .env                 # Application SECRETS & Environment variables
```

## 🎙️ Speech to Text Setup

If utilizing the local microphone:
1. When running under Docker, audio hardware pass-through requires specific configuration (`--device /dev/snd` for Linux, or PulseAudio forwarding for macOS).
2. Check `src/speech_to_text.py` if no mics are found. Run it manually locally to verify default inputs.

---

## 🤝 Development Workflow

### Creating a New Feature

We use a Gitflow-inspired branching model. To start a new feature:

```bash
make git-feature name=your-feature-name
```

### Accessing the Container

If you need to run commands manually inside the running container:

```bash
make docker-exec
```
