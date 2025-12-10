```yaml
title: "SOURCES & WATCH STRATEGY"
project: "Theopy – AI Assistant MVP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2025–2026"
certificate: "RNCP39583 – Expert in Software Development"
```

# Sources & Watch Strategy (Veille Technologique)

## 1. Documentation Sources

### Core Technologies
- **Python:** [docs.python.org](https://docs.python.org/3/) - Official reference.
- **Flask:** [flask.palletsprojects.com](https://flask.palletsprojects.com/) - For API structure and patterns.
- **SQLAlchemy:** [docs.sqlalchemy.org](https://docs.sqlalchemy.org/) - Database ORM best practices.

### AI & Speech
- **OpenAI Whisper:** [github.com/openai/whisper](https://github.com/openai/whisper) - Model usage and updates.
- **Vosk:** [alphacephei.com/vosk](https://alphacephei.com/vosk/) - Offline alternative research.
- **Hugging Face:** [huggingface.co](https://huggingface.co/) - Exploring new models and datasets for French NLU.

### Architecture & DevOps
- **Docker:** [docs.docker.com](https://docs.docker.com/) - Containerisation best practices.
- **GitHub Actions:** [docs.github.com/en/actions](https://docs.github.com/en/actions) - CI/CD workflow documentation.
- **12-Factor App:** [12factor.net](https://12factor.net/) - Methodology for building SaaS apps.

## 2. Watch Strategy (Veille)

### Objectives
- Stay updated on **LLM and STT advancements** (models get smaller and faster every month).
- Monitor **security vulnerabilities** in Python dependencies.
- Follow **Kozea internal updates** regarding Teepy API changes.

### Tools & Channels

| Channel | Source | Frequency | Focus |
|---------|--------|-----------|-------|
| **Newsletters** | TLDR AI, Python Weekly | Weekly | General trends, new libraries |
| **Social** | Twitter/X (AI influencers), LinkedIn | Daily | Quick news, demos of new tech |
| **Code** | GitHub Trending (Python) | Weekly | Discovering new open-source tools |
| **Communities** | Reddit r/LocalLLaMA, r/Python | Ad-hoc | Troubleshooting, hardware discussions |
| **Security** | GitHub Dependabot | Real-time | Security patches for repo dependencies |

### Recent Findings 
- *Discovery:* **Distil-Whisper** offers 6x speedup over standard Whisper with minimal accuracy loss. -> *Action:* Added to technical roadmap for performance optimisation.
- *Discovery:* **FastAPI** gaining market share over Flask. -> *Action:* Noted for potential future migration if async needs grow.
