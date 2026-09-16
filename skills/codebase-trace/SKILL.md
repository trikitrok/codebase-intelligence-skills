---
name: codebase-trace
description: Trace one named behavior from concrete trigger to result.
---
# Codebase trace
Read [analysis basics](../../shared/references/analysis-basics.md). Resolve the named route, command, event, job, UI action, API, or test; ask only if materially different matches make selection unsafe. Follow registration, dispatch, transformations, decisions, dependencies, state, external calls, side effects, and result. Inspect relevant error, retry, transaction, concurrency, and authorization paths. Record verified `from symbol → mechanism → to symbol` hops and verify them. Stop at the observable result or terminal side effect without broadening to unrelated internals. Deliver the concise trace, alternate paths, and a sequence diagram when useful, labeling runtime gaps.
