---
name: codebase-onboarding
description: Build a fast, evidence-backed mental model of an unfamiliar repository for a competent developer. Use for project orientation and productivity guidance; use codebase-tutorial for a chaptered teaching guide or codebase-deep-dive for one subsystem.
---

# Codebase Onboarding

Orient a developer without turning the result into a file inventory.

## Start

Read [core conventions](../../shared/references/core.md) and the [source-first workflow](../../shared/references/source-first.md). Treat the target as read-only.

## Analyze

1. Establish what the project does from executable source, manifests, configuration, tests, and then documentation.
2. Build a small repository map around system boundaries and responsibilities, not every directory.
3. Identify entry points, core abstractions, major control/data flows, state and persistence, external systems, configuration, and extension points.
4. Inspect build, test, lint, run, and local-development configuration. Do not run mutating setup or install missing dependencies without permission.
5. Select a shallow-to-medium source reading order that teaches the project efficiently.
6. Reconcile material documentation/source disagreement and label uncertainty.

## Deliver

Include:

- purpose and one-paragraph mental model;
- repository/system map with evidence;
- entry points and one or two representative flows;
- state, integrations, configuration, tests, and development workflow;
- extension points and common change locations;
- a prioritized source reading order;
- evidence limitations or contradictions.

Use a compact diagram only when it clarifies relationships. Perform the shared verification pass before reporting. Recommend `$codebase-architecture`, `$codebase-trace`, or `$codebase-deep-dive` for follow-up rather than silently expanding scope.
