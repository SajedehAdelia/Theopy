```yaml
title: "IMPROVEMENT RECOMMENDATIONS"
project: "Theopy – AI Assistant MCP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# Improvement Recommendations

Recommendations below are derived from the KPI table in [`risk_mapping.md`](../02_TECHNICAL_RISKS/risk_mapping.md#4-incident-monitoring-and-control-kpis) and from a fresh coverage run against the current codebase, not from generic best practice — each one ties back to a measured indicator.

## 1. Split test coverage reporting: fast suite vs. AI suite

**Observation.** A full coverage run (`coverage run -m pytest -m "not ai"`) currently measures **89% overall**, with core business-logic modules at or near 100% (`auth.py`, `history_store.py`, `response_guard.py`, `role_access.py`, `system_prompt.py`), but the two LLM-client modules far lower: `gemini_client.py` at **38%** and `ollama_client.py` at **22%**.

**Analysis.** This is not neglect — those two modules are covered by tests marked `ai`, which are deliberately excluded from the default suite (`pytest -m "not ai"`, the one CI runs on every push) because they call real model APIs and would add cost and latency to every push. The 75–89% figure already documented in `risk_mapping.md` §4 blends both realities into one number, which understates how well-tested the AI-calling code actually is and overstates the risk.

**Recommendation.** Report the two suites separately (e.g. `coverage-fast` and `coverage-ai` as two lines in the KPI table instead of one blended figure), and add a **scheduled nightly CI job** that runs the `ai`-marked suite against real APIs — catching model/prompt regressions without slowing down every PR. Estimated cost: one small GitHub Actions cron job (`schedule:` trigger), no new tooling. Estimated gain: accurate visibility into the two modules that currently look the weakest but may not be, plus earlier detection of AI-side regressions (prompt drift, SDK breaking changes) that the fast suite structurally cannot catch.

## 2. Cover `mcp_client.py`'s error/retry paths

**Observation.** `src/mcp_client.py` sits at **64%** coverage on the fast suite, with the gaps concentrated in the connection/error-handling branches (lines 37–57, 62, 81, 95, 105–116 — roughly the SSE connect/retry/close paths).

**Analysis.** This is the module the incident in [`incident_taskgroup_teardown.md`](incident_taskgroup_teardown.md) came from — its failure modes (connection drop, teardown ordering) are exactly the untested branches. `risk_mapping.md` already tracks "SSE Connection Drops" as a KPI (`> 10 drops per session`), but nothing in the test suite currently exercises that path directly.

**Recommendation.** Add targeted unit tests for `TeepyMCPClient`'s connect failure, close-during-error, and reconnect paths using the existing `AsyncMock` pattern already established in `test_dispatcher.py`. Estimated effort: half a day, no new infrastructure. Estimated gain: the module most exposed to production incidents becomes the one most protected against regressions, closing the exact gap the last real incident came from.

## 3. Automate dependency detection (implemented)

**Observation.** Prior to this analysis, all 19 pinned dependencies were updated manually, triggered either by new feature needs or occasional proactive compatibility passes (e.g. the Flask/Werkzeug bump for Python 3.11) — nothing surfaced outdated or vulnerable packages on its own.

**Action taken.** Added [`.github/dependabot.yml`](../../.github/dependabot.yml), scoped to `requirements.txt` and to the GitHub Actions workflow files, checking monthly. Update PRs are grouped by risk (minor/patch bundled, majors isolated) to mirror the review discipline already used in production on Teepy — see [`dependency_update_process.md`](dependency_update_process.md) §3–4 for the full merge policy. This closes the original gap (security patches depending on someone noticing them) while keeping the human review/hold-back decision that the batching model relies on.

## 4. Automate deployment (CD) via a self-hosted runner — planned, not yet implemented

**Observation.** Per [`dependency_update_process.md`](dependency_update_process.md) and the deployment note in [`incident_taskgroup_teardown.md`](incident_taskgroup_teardown.md) §5, Theopy is currently deployed manually: `make upgrade` is run by hand on each tiers-payant workstation that uses it day to day. This is real deployment to real users, but it depends on someone remembering to run it after every merge.

**Design.** The next step is a self-hosted GitHub Actions runner installed directly on the machine(s) running Theopy, avoiding any need to expose SSH or open ports to the internet — the runner dials out to GitHub rather than being dialed into. Concretely:
1. Install and register the GitHub Actions runner agent on the target machine (`./config.sh`, using a registration token from the repo's Settings → Actions → Runners), labeled `self-hosted`.
2. Add a `deploy` job to a new `.github/workflows/cd.yml`, triggered `on: push: branches: [main]`, gated with `needs: build` so it only runs once the existing CI job (lint + tests) is green.
3. That job runs on the target machine itself: `git pull`, `docker compose build`, `docker compose up -d` — the same sequence `make upgrade` already performs by hand.
4. A final `curl -f http://localhost:8000/health` step confirms the new container came up healthy; a failure here fails the job and triggers the same notification path already relied on for CI failures.

**Why this option over the alternatives.** An SSH-based deploy step would need the machine reachable from GitHub's cloud runners (a VPN or port-forward), which isn't available on a workstation sitting on Kozea's internal network. A registry-plus-auto-updater approach (e.g. Watchtower) would remove the CI-as-gate checkpoint entirely, updating on a timer rather than only after tests pass — inconsistent with the hold-if-broken discipline already used for dependency updates (§1 above) and on Teepy in production.

**Status — deliberately not yet implemented, for a specific security reason.** GitHub itself warns against self-hosted runners on public repositories:

> "Using self-hosted runners in public repositories is not recommended. Forks of your public repository can potentially run dangerous code on your self-hosted runner by creating a pull request."

Theopy's repository is currently public so the RNCP jury can review the code. A self-hosted runner on a public repo would let anyone open a pull request from a fork and execute arbitrary code on whichever machine the runner is installed on — an unacceptable risk on a workstation used in production. The correct sequencing is: keep the repository public through the certification review, then set the repository to private and implement the self-hosted runner described above, once the fork-PR attack surface no longer applies. This is not a missing step so much as a step correctly held until its precondition (a private repository) is met.
