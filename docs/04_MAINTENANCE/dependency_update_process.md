```yaml
title: "DEPENDENCY UPDATE PROCESS"
project: "Theopy – AI Assistant MCP Server"
author: "Adelia Fathipoursasansara"
organisation: "Kozea"
period: "2026"
certificate: "RNCP39583 – Expert in Software Development"

```

# Dependency Update Process

## 1. Scope

This process covers every third-party package pinned in [`requirements.txt`](../../requirements.txt) (19 packages, all version-pinned — Flask, sentry-sdk, google-genai, mcp, pytest, etc.), which is the sole dependency manifest for the project (single Python service, no separate frontend package manager beyond the JS test runner already covered by `npm`).

## 2. Mechanism

Updates are applied through the `make upgrade` target defined in the [`Makefile`](../../Makefile):

```
upgrade:
	$(DOCKER_COMPOSE) build          # rebuild the image against the current requirements.txt
	$(DOCKER_COMPOSE) up -d          # restart the containers on the new image
	$(MAKE) lint-flake8              # confirm the upgrade didn't break style compliance
```

A version bump in `requirements.txt` is committed like any other code change, then `make upgrade` rebuilds the Docker image from a clean `pip install`, restarts the running container, and re-lints to catch anything the new version broke. The full test/lint matrix in [`.github/workflows/ci.yml`](../../.github/workflows/ci.yml) (Ubuntu + macOS, Python 3.11) then re-validates the change on every push, so a dependency bump that breaks a test is caught before merge, not after.

## 3. Trigger and frequency

Two update paths coexist:

- **Feature-driven, ad hoc**: a dependency is added or bumped when a new capability needs it — e.g. `sentry-sdk[flask]` was added alongside the Sentry integration, `mcp` and `httpx-sse` when the project moved to the FastMCP SSE transport. Applied via `make upgrade` as described above.
- **Scheduled detection via Dependabot** ([`.github/dependabot.yml`](../../.github/dependabot.yml)): checks `requirements.txt` and the GitHub Actions workflow files once a month and opens pull requests for anything outdated. The grouping is deliberately modeled on the manual process already used on Teepy at Kozea: minor/patch bumps are grouped into a single PR (merged together as one commit if nothing breaks), while major bumps stay isolated one-per-PR so a breaking major version can be held back or investigated without blocking the rest — the same logic as the monthly backend/frontend update rotation used in production on Teepy, scaled down to a solo maintainer.

## 4. Review and merge discipline

Each monthly Dependabot batch is reviewed manually before merge, following the same decision rule used on Teepy: CI (lint + full test matrix) is the gate. If a bump passes, it merges — minor/patch bumps together, majors individually. If a bump breaks CI, that specific update is held back (the PR stays open, un-merged) rather than merged and fixed reactively — the rest of the batch is unaffected since majors and minor/patch groups are already isolated from each other.

## 4. Safety net

Because `make upgrade` re-lints and CI re-runs the full test suite on every push regardless of what changed, a dependency update that introduces a regression is caught the same way any other code regression would be — there is no separate/weaker validation path for dependency changes versus feature changes.
