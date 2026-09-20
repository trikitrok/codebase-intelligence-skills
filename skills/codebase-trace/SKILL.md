---
name: codebase-trace
description: Trace one named behavior from concrete trigger to result.
---
# Codebase trace
Read [analysis basics](../../shared/references/analysis-basics.md). Resolve the named route, command, event, job, UI action, API, or test; ask only if materially different matches make selection unsafe. Follow registration, dispatch, transformations, decisions, dependencies, state, external calls, side effects, and result. Inspect relevant error, retry, transaction, concurrency, and authorization paths. Record verified `from symbol → mechanism → to symbol` hops and verify them. Stop at the observable result or terminal side effect without broadening to unrelated internals. Deliver the concise trace and alternate paths, labeling runtime gaps.

When ordered interactions, branching, asynchronous behavior, or cross-boundary
execution would be clearer visually, read
[diagramming](../../shared/references/diagramming.md) and provide the verified
actors, `from symbol → mechanism → to symbol` hops, interaction order,
transformations, decisions and branches, state changes, external calls, side
effects, relevant error/retry/concurrency paths, inputs/outputs, runtime gaps,
and uncertainty.
