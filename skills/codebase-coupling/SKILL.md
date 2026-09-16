---
name: codebase-coupling
description: Explain temporal, static, logical/domain, and test coupling with selective inspection.
---
# Codebase coupling
Read [analysis basics](../../shared/references/analysis-basics.md) and [history analysis](../../shared/references/history-analysis.md). Anchor a named subject or choose a small meaningful scope. Run `history_candidates.py temporal-coupling`, review quality, and select a bounded set. Inspect imports, calls, interfaces, models/state/configuration, messages, schemas, duplicated knowledge, fixtures, mocks, and coordinated tests; use configured dependency analysis only for a concrete gap. Compare temporal, static, logical, and test relationships and classify each as expected, potentially hidden, or unclear. Stop before an exhaustive graph or subsystem deep dive. Report endpoints, `S/T/L/X`, provider evidence, source/test evidence, status, implication, and uncertainty. Temporal coupling is not automatically a defect.
