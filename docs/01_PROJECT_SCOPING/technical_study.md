```yaml
title: "TECHNICAL STUDY & ALTERNATIVES"
project: "Theopy – AI Assistant MCP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# Technical Study & Alternatives

## 1. Architectural Patterns

### **Choice: "Hub & Spoke" Architecture via MCP**

* **Why:** Theopy becomes an autonomous, central AI agent, while Teepy exposes its business intelligence securely through its own Model Context Protocol (MCP) server. This decoupled approach is highly secure and readies the infrastructure for future investments, allowing any future company application to integrate simply by exposing an MCP server.


* **Alternative 1: AI Agent Coupled to ERP Code**
* *Pros:* Easy and fast to prototype.


* *Cons:* Unusable for any other projects within the company ecosystem, creating monolithic technical debt. *(Rejected)*




* **Alternative 2: Direct SQL Generation by AI**
* *Pros:* Extremely fast data retrieval.
* *Cons:* Introduces a critical security risk with the potential for irreversible data destruction if the AI generates malicious or flawed queries. *(Rejected)*




* **Verdict:** **Hub & Spoke MCP** is the only viable solution for a secure, scalable enterprise architecture.



## 2. Inter-Service Communication

### **Choice: Server-Sent Events (SSE)**

* **Why:** SSE provides a unidirectional, lightweight data stream that is perfect for asynchronous context bubbling between microservices. It eliminates the heavy CPU and network overhead associated with continuous HTTP polling.


* **Alternative: WebSockets or Standard HTTP REST**
* *Pros:* WebSockets offer bidirectional real-time communication; REST is universally understood.
* *Cons:* WebSockets introduce unnecessary state management complexity for simple data retrieval. Standard REST requests are prone to timeouts during long LLM inference phases.


* **Verdict:** **SSE** optimally balances performance and simplicity for the MCP data streams.



## 3. AI SDK & Inference Engine

### **Choice: LLM Agnosticism (Google Gemini SDK as MVP)**

* **Why:** The architecture is designed to be fully LLM agnostic. By standardizing tool definitions, the system allows transparent switching between AI engines (e.g., Gemini, ChatGPT, Claude) without touching the core business code of the applications. The MVP utilizes the `google-genai` SDK to leverage native "Function Calling," ensuring the AI outputs strictly formatted JSON tools rather than free-form conversational text.


* **Alternative: Hardcoded Prompt Engineering & Legacy LLMs**
* *Pros:* Avoids dependency on the latest beta SDKs.
* *Cons:* High risk of "hallucinations" and severe routing inaccuracies.




* **Verdict:** **LLM Agnosticism via modern SDKs** guarantees a routing precision greater than 95%.



## 4. Backend Framework & Database

### **Choice: Python 3, Flask, PostgreSQL, and SQLAlchemy**

* **Why:** The initial technical audit revealed that the Teepy ERP already possesses a highly mature infrastructure using these specific technologies. Reusing the Python 3 / Flask stack ensures seamless developer context switching, while SQLAlchemy provides robust, parameterized security against SQL injections.


* **Alternative: Node.js / Express**
* *Pros:* High asynchronous I/O performance.
* *Cons:* Fragments the company's tech stack and limits access to Python's dominant AI ecosystem.


* **Verdict:** **Python/Flask** is retained to align perfectly with the existing enterprise stack.



## 5. Infrastructure & Deployment

### **Choice: Docker, Docker Compose, Linux, and GNU Make**

* **Why:** Creating a completely independent infrastructure for Theopy (its own Docker containers, CI/CD pipelines, and unit test base) isolates it from the ERP's legacy code. Docker Compose allows for the creation of an isolated network bridge specifically for secure inter-container communication, mitigating port conflicts. Furthermore, strict containerization ensures consistent builds across different local development environments, seamlessly bridging deployments from macOS/Apple Silicon laptops directly to Linux VPS production servers.


* **Alternative: Bare Metal or Full Virtual Machines (VMs)**
* *Pros:* Complete OS-level control.
* *Cons:* High environmental footprint and resource waste.




* **Verdict:** **Docker Containerization** ensures infrastructure sobriety, security, and portability.