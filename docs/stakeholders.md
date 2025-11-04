Project: Teepy — Server AI Assistant (voice-first, no GUI)

Author: Adelia Fathipoursasansara
Date: 21/09/2025

STAKEHOLDER MAP

A short list of the core stakeholders, their role and interest.

1- Theopy Developer / Project Owner (Adelia)

    Role: Implementer, decision-maker for technical choices. Primary responsible for delivery.

    Interest: Deliver a working, well-documented assistant; demonstrate capability.

2- Teepy Product Manager (Adelia)

    Role: Product validation, high-level acceptance, API ownership.

    Interest: Integration that preserves data safety and UX.

3- End Users (Teepy users, Les tiere payant of KOZEA company)

    Role: Consumers of the voice and AI assistant features.

    Interest: Reliable, secure voice control that saves time and makes use much easier.

4- Infrastructure / DevOps (Adelia)

    Role: Deploy and maintain server (MPC server). Ensure continuous delivery/hosting.

    Interest: Secure, observable, scalable systems.

5- LLM / External API Providers (OpenAI, Whisper, TTS vendors)

    Role: Provide models and services.

    Interest: Stable API, predictable costs, usage quotas.

6- QA / Testers (Ynov freinds/ beta users)

    Role: Validate features, spot bugs, measure response latency.

    Interest: A product that "just works" in real usage.

7- Legal / Privacy (if needed later)

    Role: Ensure compliance (GDPR, data retention, PII handling).

    Interest: Minimise risk of data leaks or non-compliance.



### RACI matrix (core tasks — adapt as project grows)


| Task / Deliverable                      | Responsible     | Accountable                | Consulted                 | Informed      |
| --------------------------------------- | --------------- | -------------------------- | ------------------------- | ------------- |
| Define project scope & success criteria | Adelia          | Adelia                     | Ynov Pedagogy             | End users     |
| Create project docs                     | Adelia          | Adelia                     | Adelia                    | Product Owner |
| Repo & project board setup              | Adelia          | Adelia                     | Adelia                    | Product Owner |
| Prototype: STT → LLM → Theopy API       | Adelia          | Adelia                     | DevOps, Ynov freinds      | QA testers    |
| Security & data handling design         | Adelia          | Product Owner(Adelia)      | DevOps,Ynov freinds       | End users     |
| Deployment & infra                      | Adelia          | DevOps                     | DevOps,Ynov freinds       | Product Owner |
| User acceptance testing                 | QA / Beta users | Product Owner(Adelia)      | DevOps, Ynov freinds      | End users     |
