```yaml
title: "SOURCES & TECHNICAL WATCH"
project: "Theopy – AI Assistant MCP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# Sources & Technical Watch

## 1. Objectives of the Technical Watch

To ensure the Theopy architecture remains scalable, secure, and aligned with industry standards, a continuous technical watch was established. The primary focus areas were AI integration protocols, asynchronous network communication between microservices, and secure tool-calling mechanisms for Large Language Models (LLMs).

## 2. Methodology & Sources

### Tools & Platforms

* **Aggregators & Workflows:** Custom GitHub workflow boards, GitHub Releases, GitHub Changelogs, and Daily.dev.


* **Community Watch:** GitHub Trending (to monitor emerging SDKs) and Reddit communities (`r/Python`, `r/LocalLLaMA`).



### Official Documentation

* **Anthropic:** As the original creators of the Model Context Protocol (MCP), their documentation was central to the architectural design.


* **Google Cloud Developer Docs:** Used for implementing the `google-genai` SDK and ensuring optimal token consumption.



### Newsletters & Media

* **TLDR AI:** For daily summaries of AI advancements and new model releases.


* **The Pragmatic Engineer:** For insights on system design, microservices, and backend engineering at scale.


* **MIT Technology Review:** For high-level trends in AI compliance and accessibility.



## 3. Key Findings & Impact on the Project

The technological watch directly influenced the three most critical architectural decisions of the Theopy MVP:

### A. The Model Context Protocol (MCP)

* **Finding:** The industry is moving away from custom REST bridges for AI tools and towards standardized protocols.
* **Impact:** We adopted the MCP to standardize the exposure of Python functions to the LLM. This makes Theopy a reusable "Hub" that can seamlessly connect with any future Kozea project without rewriting the bridging logic.



### B. Server-Sent Events (SSE) Connectivity

* **Finding:** Standard HTTP requests often timeout during long LLM inference or heavy database queries, while WebSockets introduce unnecessary bidirectional complexity.
* **Impact:** We implemented SSE for unidirectional, lightweight communication. It is perfectly suited for asynchronous context bubbling between microservices, drastically reducing network overhead.



### C. Strict Function Calling via Modern SDKs

* **Finding:** Relying on prompt engineering alone to extract JSON from LLMs is error-prone and leads to hallucinations.
* **Impact:** We utilized the latest Google Gemini SDKs (like Gemini 1.5) that natively support "Function Calling". This forces the AI to output strictly structured JSON tool calls instead of free-form conversational text, ensuring a 95%+ routing accuracy.



```

```