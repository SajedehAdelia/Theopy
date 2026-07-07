```yaml
title: "PESTEL ANALYSIS"
project: "Theopy – AI Assistant MVP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

## PESTEL Analysis for Theopy

This complements the SWOT by mapping **macro-environmental factors** that may impact the project.

| Factor | Opportunities | Threats |
| --- | --- | --- |
| **Political** | - Government support for AI innovation and digital transformation.<br>

<br>- Policies encouraging accessibility in workplaces. | - Strict data protection laws (GDPR, CNIL regulations) affecting data transmission and prompt logging.

 |
| **Economic** | - High proven ROI potential: amortizing CAPEX in ~5.1 months by saving 10 mins/day per user.

<br>

<br>- Positioning Kozea's infrastructure as an easily pitchable asset for future fundraising.

 | - Budget constraints in client organisations may limit the adoption of premium AI features.<br>

<br>- Economic downturns could slow tech investments. |
| **Social** | - Substantially improves Quality of Life at Work (QVT) by liberating time from repetitive data extraction tasks.

<br>

<br>- Restores lost personal time (e.g., recovering 50% of lunch breaks previously lost to support calls).

 | - Resistance to change from users accustomed to traditional interface navigation.<br>

<br>- Frustration if the AI misinterprets complex business intents. |
| **Technological** | - The Model Context Protocol (MCP) standardizes AI communication, allowing the agent to be reused across all Kozea apps.

<br>

<br>- LLM Agnosticism (Hub & Spoke architecture) allows switching between Gemini, Claude, or local models without rewriting business logic.

<br>

<br>- Server-Sent Events (SSE) provide lightweight, asynchronous data streams.

 | - Evolving AI APIs may introduce breaking changes to the `google-genai` SDK.<br>

<br>- Risk of "vendor lock-in" if overly dependent on a single AI provider (mitigated by the agnostic architecture).

 |
| **Environmental** | - **Compute Delegation:** Delegating heavy LLM calculations to Google Gemini API avoids running highly energy-intensive GPU servers 24/7 locally.

<br>

<br>- **Network Efficiency:** SSE eliminates continuous network polling, drastically reducing bandwidth and CPU load.

<br>

<br>- **Infrastructure Sobriety:** Docker containers optimize hardware usage compared to full VMs.

 | - Reliance on massive external cloud providers (Google) inherently carries a carbon footprint for every API call made. |
| **Legal** | - Strict SQL data isolation guarantees that the AI cannot directly access or corrupt the legacy database.

<br>

<br>- Architecture respects strict production constraints identified during the initial legal and technical audit.

 | - Intellectual property issues regarding data used to train or prompt the LLM.<br>

<br>- High compliance complexity if dealing with sensitive healthcare data (HDS certification). |

```

```