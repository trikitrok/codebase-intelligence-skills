---
name: codebase-architecture
description: "Develop an evidence-backed architectural mental model of a repository: boundaries, components, communication, state, integrations, and major flows. Use for system architecture, not a raw dependency graph or one behavior trace."
---

# Codebase Architecture

Explain the system's meaningful boundaries and runtime shape.

## Start

Read [core conventions](../../shared/references/core.md) and the [source-first workflow](../../shared/references/source-first.md).

## Analyze

1. Identify deployable/runtime boundaries, entry points, build modules, and external actors.
2. Derive components from manifests, configuration, registrations, source responsibilities, and tests. Label boundaries inferred from structure.
3. Trace major communication patterns and data/control flows.
4. Locate state ownership, persistence, caches, queues/events, external integrations, and cross-cutting mechanisms.
5. Identify public/internal boundaries and extension points, plus important dependency direction.
6. Use static dependency evidence only to support semantic architecture; do not equate imports with architecture.

## Deliver

Provide the system context, component responsibilities, communication and state model, representative flows, boundaries/extension points, and evidence-backed diagrams where useful. Attach evidence or an explicit inference to every meaningful diagram edge. Report discrepancies with architecture documentation.

Verify important paths, symbols, relationships, and diagram edges. Suggest `$codebase-trace` for one runtime behavior or `$codebase-verify` for a document audit instead of starting those analyses.
