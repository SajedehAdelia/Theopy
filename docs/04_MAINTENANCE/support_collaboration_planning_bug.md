```yaml
title: "SUPPORT COLLABORATION — CUSTOMER PLANNING LOOKUP LEAKING RAW DATA"
project: "Theopy – AI Assistant MCP Server (Teepy integration)"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# Support Collaboration — Customer Planning Lookup Leaking Raw Data

## 1. Context of the report

Around 15–16 June 2026, Theopy was handed to Annabelle Nicvert, UX designer at Kozea, for hands-on testing ahead of wider rollout. Asking the assistant for a specific customer's planning sometimes returned a raw JSON blob instead of a natural-language or table answer — an internal data structure leaking straight into what a pharmacy customer could see, which made it urgent to fix rather than a cosmetic issue.

While reproducing Annabelle's report, a second, deeper bug surfaced: asking for one customer's planning could return **every** customer's planning at once — the actual root cause of the raw-data leak (see §3).

## 2. Diagnosis

Two independent layers were involved, each contributing to the visible symptom:

- **Data layer (Teepy MCP tool)**: `agent_dashboard_customers()` in [`teepy/routes/theopy/planning.py`](../../../teepy/routes/theopy/planning.py) had no `customer_name` parameter at all before this point — every call returned the full customer dashboard, unfiltered. A request scoped to one pharmacy therefore came back as a large, unscoped result set.
- **Presentation layer (Theopy)**: the system prompt in `gemini_client.py` instructed the model to *"Do not output raw JSON or markdown tables to the user, just speak naturally"* — a soft, non-structural instruction. It held up for small results, but gave the model no safe structured fallback once the result set was large and unscoped, and it leaked the tool's raw JSON instead of narrating it.

## 3. Resolution

Fixed in two commits, one day apart:

- **[`e72e2ce8`](https://github.com/Kozea/teepy/commit/e72e2ce8984671a165b948265f603a9ff0c7dd19) (Teepy, 2026-06-18)** — added a `customer_name` parameter to `agent_dashboard_customers()` with an `ILIKE` (case-insensitive, partial-match) filter, so a planning lookup is properly scoped to the requested customer instead of returning everyone.
- **[`993bac5`](https://github.com/SajedehAdelia/Theopy/commit/993bac5982a6177ace21e8a4c20e361b008f5e11) (Theopy, 2026-06-19)** — changed the system prompt from *"do not output raw JSON or markdown tables, just speak naturally"* to explicitly requiring a Markdown table for any list-shaped tool result, removing the ambiguous "speak naturally" fallback that broke down on large results. Paired with matching CSS/template work (`style.sass`, `theopy-chat.html.jinja2`) so the table renders cleanly in the chat UI.

The data layer was fixed first (removing the actual cause of oversized results), and the presentation layer the next day (removing the failure mode entirely, so even a future unscoped result would render as a table, never raw JSON).

## 4. Contribution of the different stakeholders

- **Annabelle Nicvert (UX designer)** — acted as the first real tester outside development, surfaced the customer-facing symptom (raw JSON visible) that automated tests had not caught, since unit tests exercised the query logic with already-scoped fixtures.
- **Developer (self)** — reproduced the report, diagnosed that the visible symptom (raw JSON) was a downstream effect of a separate, unscoped-query bug, and delivered fixes on both sides of the Theopy↔Teepy boundary: the query fix in Teepy's MCP tool layer, and the presentation-layer fix in Theopy's own prompt instructions.

## 5. Follow-up

Both fixes were then formalized as tracked issues/documentation rather than left as undocumented hotfixes, consistent with the incident-consignment process in [`incident_taskgroup_teardown.md`](incident_taskgroup_teardown.md).
