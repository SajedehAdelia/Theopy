```yaml
title: "TECHNICAL STUDY & ALTERNATIVES"
project: "Theopy – AI Assistant MVP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2025–2026"
certificate: "RNCP39583 – Expert in Software Development"
```

# Technical Study & Alternatives

## 1. Programming Language

### **Choice: Python**
- **Why:** The dominant language for AI, Machine Learning, and NLP (Natural Language Processing). Huge ecosystem (PyTorch, TensorFlow, spaCy, Whisper).
- **Alternative: Node.js**
  - *Pros:* Faster I/O for real-time websockets, same language as frontend.
  - *Cons:* Poor support for local AI model execution; would require calling external Python scripts anyway.
- **Verdict:** **Python** is mandatory for an AI-centric backend.

## 2. Web Framework

### **Choice: Flask**
- **Why:** Lightweight, simple, and flexible. **Consistency with Teepy:** Since Teepy also uses Flask, sharing the same stack reduces context switching and simplifies maintenance for the team.
- **Alternative: Django**
  - *Pros:* Built-in admin, ORM, auth.
  - *Cons:* Too complex for a simple API. Not suitable for an MVP.
- **Alternative: FastAPI**
  - *Pros:* Modern, **Asynchronous (ASGI)** native. Much better performance for handling multiple concurrent audio streams compared to Flask/Django (Synchronous WSGI).
  - *Cons:* Slightly steeper learning curve for async concepts if not familiar.
- **Verdict:** **Flask** chosen for **consistency with Teepy** and simplicity (sufficient for MVP), though **FastAPI** is a strong candidate for v2 to improve concurrency.

## 3. Speech-to-Text (STT) Engine

### **Choice: OpenAI Whisper (Local)**
- **Why:** State-of-the-art accuracy, open-source, runs locally (privacy compliant), handles French well.
- **Alternative: Google Cloud Speech-to-Text / AWS Transcribe**
  - *Pros:* No server load, extremely fast.
  - *Cons:* Paid service, data leaves the server (privacy risk), requires internet.
- **Alternative: Vosk**
  - *Pros:* Very lightweight, fast on CPU.
  - *Cons:* Lower accuracy than Whisper, especially for complex sentences.
- **Verdict:** **Whisper** (Base/Small model) for best balance of accuracy vs privacy.

## 4. Text-to-Speech (TTS) Engine

### **Choice: pyttsx3 / gTTS**
- **Why:** Simple, free. pyttsx3 works offline.
- **Alternative: ElevenLabs / OpenAI TTS**
  - *Pros:* Extremely realistic, emotional voices.
  - *Cons:* Expensive, high latency, cloud-only.
- **Verdict:** **pyttsx3** for MVP (functional), upgrade to AI voice later if budget allows.

## 5. Database

### **Choice: SQLAlchemy (Dev) / PostgreSQL (Prod)**
- **Why:** Relational data (users, logs, permissions) fits SQL well. SQLAlchemy allows switching DBs easily.
- **Alternative: MongoDB**
  - *Pros:* Flexible schema for logs.
  - *Cons:* Overkill for simple structured data; less strict data integrity.
- **Verdict:** **SQL** standard is safer for enterprise integration.

## 6. Architecture Pattern

### **Choice: Modular Monolith (Layered)**
- **Why:** Easier to develop and deploy than microservices for a single team/developer.
- **Alternative: Microservices**
  - *Pros:* Scale STT independently.
  - *Cons:* "Distributed monolith" risk, complex deployment (K8s), network latency overhead.
- **Verdict:** **Modular Monolith** packaged in Docker.
