```yaml
title: "INCIDENT REPORT — ASYNCIO TASKGROUP TEARDOWN CRASH"
project: "Theopy – AI Assistant MCP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# Incident Report — Asyncio TaskGroup Teardown Crash

This report instantiates the generic Incident Response Procedure defined in [`risk_mapping.md`](../02_TECHNICAL_RISKS/risk_mapping.md#5-incident-response-procedure) against one real incident, and traces its correctif through to deployment.

## 1. Anomaly consignment (fiche de consignation)

| Field | Detail |
| --- | --- |
| **Date observed** | June 2026, during local development of the FastMCP SSE transport (following commit `f73f777`) |
| **Component** | `src/dispatcher.py` — `AgentDispatcher.handle_user_input`, in interaction with `src/mcp_client.py` (`TeepyMCPClient`, SSE-based) |
| **Symptom** | Exception raised during request teardown: `RuntimeError: Attempted to exit cancel scope in a different task than it was entered in` |
| **When it occurred** | After a normal `/ask` request completed and its answer was returned — the crash happened during the asyncio event loop's own cleanup, not during the AI response itself, which made it easy to miss in casual testing (the user-facing response looked fine) |
| **How to reproduce** | Send a request through `/ask` (triggering `AgentDispatcher.handle_user_input`) and let the process return without the SSE-based MCP client being explicitly closed before `asyncio.run()` tears down its event loop |
| **Environment** | Reproducible consistently once the SSE transport replaced the original STDIO transport (STDIO connections didn't hold an open cancel scope the way the SSE client's context manager did) |

## 2. Diagnosis

Root cause: `TeepyMCPClient` holds an open `anyio`/`asyncio` cancel scope for the duration of its SSE connection. Before this fix, nothing guaranteed `mcp_client.close()` ran *inside* the same async context that opened the connection — the event loop could start unwinding (at the end of `asyncio.run()`) while the client's cancel scope was still open, and asyncio refuses to exit a cancel scope from a different task/loop context than the one that entered it. This is a structural consequence of switching from STDIO to SSE transport (commit `f73f777`), which is what surfaced the bug.

## 3. Resolution (correctif)

Fixed in commit [`97906eb`](../../.git) ("Implement local LLM support (Ollama), fix async teardown, and stabilize test suite"), 2026-06-24. `AgentDispatcher.handle_user_input` now wraps the AI call in a `try/finally`:

```python
async def handle_user_input(self, text: str) -> str:
    if not self.brain:
        await self.initialize()
    try:
        logger.info("Processing user request...")
        final_answer = await self.brain.process_user_request(text)
        return final_answer
    finally:
        if hasattr(self, "mcp_client") and self.mcp_client:
            await self.mcp_client.close()
```

This guarantees the MCP client's cancel scope is closed inside the same async context that owns it, before the surrounding event loop starts tearing down — regardless of whether `process_user_request` succeeded or raised.

## 4. Validation

- `src/tests/test_dispatcher.py` and `src/tests/test_app_routes.py` were both expanded in the same commit (44 and 84 lines changed respectively) using `AsyncMock` and `monkeypatch` specifically to exercise the new dual-brain routing and the `finally`-block teardown path, rather than relying on the old (crash-prone) implicit cleanup.
- `.github/workflows/ci.yml` re-ran the full lint + pytest matrix (`ubuntu-latest` and `macos-latest`, Python 3.11) on push, confirming no regression on either OS.
- Documented the same day in [`docs/CHANGELOG.md`](../CHANGELOG.md) under `[1.2.0] - 2026-06-24`.

## 5. Deployment

Theopy has no separate CD pipeline (see [`dependency_update_process.md`](dependency_update_process.md) for why deployment stays manual): the fix reached the running container the same way any other merged change does — `make upgrade`, i.e. `docker compose build` against the updated source, `docker compose up -d` to restart the container on the new image, followed by `make lint-flake8` to confirm the rebuild didn't break style compliance. The `/health` endpoint and Sentry's exception count KPI (`> 5 unhandled exceptions/hour`, per `risk_mapping.md` §4) are the post-deploy signals that would have caught a regression had the fix not held.
