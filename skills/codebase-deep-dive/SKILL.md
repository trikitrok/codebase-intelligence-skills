---
name: codebase-deep-dive
description: Explain one repository subsystem or concept in depth, including boundary, internals, lifecycle, state, callers, failures, concurrency, tests, and extension points. Use when the subject is already focused.
---

# Codebase Deep Dive

Develop a deep, bounded understanding of one subsystem or concept.

## Start

Read [core conventions](../../shared/references/core.md) and the [source-first workflow](../../shared/references/source-first.md). Define the subject boundary and adjacent context; do not expand to unrelated areas.

## Analyze

Inspect as relevant:

- responsibility and public boundary/API;
- internal model and implementation;
- construction, lifecycle, state, and invariants;
- callers, dependencies, and downstream effects;
- failure handling, transactions, retries, and concurrency;
- tests and test seams;
- extension points and important design decisions;
- edge cases and source/documentation contradictions.

Work inward from the public boundary and outward only through verified collaborators. Explain why the design exists when evidence supports it; otherwise label intent as inferred.

## Deliver

Give a focused mental model, boundary map, lifecycle/flow, implementation walkthrough, failure/concurrency behavior, tests, and extension guidance. Cite actual paths and symbols. Verify the public boundary, key callers, state transitions, and diagram edges before reporting.
