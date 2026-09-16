---
name: codebase-trace
description: Trace one named behavior through actual repository entry points, dispatch, business logic, dependencies, persistence, side effects, and result. Use for focused request/job/event flows, not broad architecture.
---

# Codebase Trace

Follow one requested behavior end to end and stay on that path.

## Start

Read [core conventions](../../shared/references/core.md) and the [source-first workflow](../../shared/references/source-first.md). If several plausible behaviors match, ask one concise question only when choosing incorrectly would invalidate the trace.

## Trace

1. Locate the concrete trigger: route, command, event, job, UI action, public API, or test.
2. Follow registration and dispatch into business logic.
3. Track transformations, decisions, dependencies, state reads/writes, external calls, side effects, and response/result.
4. Inspect error, retry, transaction, concurrency, and authorization paths when they affect the requested behavior.
5. Use tests to confirm transitions and edge behavior.
6. Record every important hop as `from symbol → mechanism → to symbol` with evidence. Do not bridge gaps with framework assumptions.

## Deliver

Lead with a concise trace. Add a Mermaid sequence diagram when it makes ordering or actors clearer, then annotate important steps with files/symbols and explain alternate/error paths. Mark runtime-dependent or unresolved transitions `INFERRED` or `UNKNOWN`.

Verify each important transition and every sequence-diagram message. Recommend `$codebase-deep-dive` if a subsystem deserves broader analysis.
