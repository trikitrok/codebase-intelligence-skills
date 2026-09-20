---
name: codebase-deep-dive
description: Explain one focused subsystem or concept in depth.
---
# Codebase deep dive
Read [analysis basics](../../shared/references/analysis-basics.md). Define the subject boundary and adjacent context. Locate its API, construction, configuration, callers, dependencies, state, and tests, then inspect lifecycle, invariants, transitions, downstream effects, failure handling, transactions, retries, concurrency, and extension seams as applicable. Expand outward only through verified collaborators and run focused repository-native checks only for concrete ambiguity. Stop when boundary, internals, lifecycle, failures, tests, and extensions are understood. Deliver the focused model, walkthrough, flow, test model, guidance, evidence, and limitations.

When subsystem structure, lifecycle, internal flows, state transitions, failure
paths, or concurrency would be clearer visually, read
[diagramming](../../shared/references/diagramming.md) and provide the verified
subsystem components, boundaries, relationships, lifecycle, flows, states and
transitions, dependencies, relevant failure or retry paths, concurrency or
transaction boundaries, and uncertainty.
