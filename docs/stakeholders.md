Project: Teepy — Server AI Assistant (voice-first, no GUI)

Author: Adelia Fathipoursasansara
Date: 21/09/2025

STAKEHOLDER MAP

A short list of the core stakeholders, their role and interest.

1- Theopy Developer / Project Owner (Adelia)

    Role: Implementer, decision-maker for technical choices. Primary responsible for delivery.

    Interest: Deliver a working, well-documented assistant; demonstrate capability.

2- AI Assistant (GPT/Assistant)

    Role: Project co-pilot — help with design, docs, code snippets, tests and reviews.

    Interest: Assist and speed up delivery.

3- Teepy Product Manager (Adelia)

    Role: Product validation, high-level acceptance, API ownership.

    Interest: Integration that preserves data safety and UX.

4- End Users (Teepy users, Les tiere payant of KOZEA company)

    Role: Consumers of the voice and AI assistant features.

    Interest: Reliable, secure voice control that saves time and makes use much easier.

5- Infrastructure / DevOps (Adelia)

    Role: Deploy and maintain server (MPC server). Ensure continuous delivery/hosting.

    Interest: Secure, observable, scalable systems.

6- LLM / External API Providers (OpenAI, Whisper, TTS vendors)

    Role: Provide models and services.

    Interest: Stable API, predictable costs, usage quotas.

7- QA / Testers (freinds/ beta users)

    Role: Validate features, spot bugs, measure response latency.

    Interest: A product that "just works" in real usage.

8- Legal / Privacy (if needed later)

    Role: Ensure compliance (GDPR, data retention, PII handling).

    Interest: Minimise risk of data leaks or non-compliance.



### RACI matrix (core tasks — adapt as project grows)


| Task / Deliverable                      | Responsible     | Accountable   | Consulted                 | Informed      |
| --------------------------------------- | --------------- | ------------- | ------------------------- | ------------- |
| Define project scope & success criteria | Adelia          | Adelia        | Product Owner, Assistant  | End users     |
| Create project docs                     | Adelia          | Adelia        | Assistant                 | Product Owner |
| Repo & project board setup              | Adelia          | Adelia        | Assistant                 | Product Owner |
| Prototype: STT → LLM → Theopy API       | Adelia          | Adelia        | Assistant, Product Owner  | QA testers    |
| Security & data handling design         | Adelia          | Product Owner | Legal / DevOps, Assistant | End users     |
| Deployment & infra                      | DevOps / Adelia | DevOps        | Assistant                 | Product Owner |
| User acceptance testing                 | QA / Beta users | Product Owner | Adelia, Assistant         | End users     |