---
name: codebase-change
description: Investigate how a requested repository change would likely be implemented, with verified impact, inferred impact, risks, migrations, and tests. Planning-only unless the user explicitly asks to modify code.
---

# Codebase Change

Plan a requested change against the current implementation. Do not edit code unless the user explicitly expands the request to implementation.

## Start

Read [core conventions](../../shared/references/core.md) and the [source-first workflow](../../shared/references/source-first.md). Restate the desired behavior and relevant compatibility constraints; ask only if a missing product decision would materially change the plan.

## Analyze

1. Trace current behavior and identify the architectural boundary and extension points.
2. Locate affected APIs, schemas, persistence, configuration, events/jobs, clients, tests, generated artifacts, and operational behavior.
3. Separate directly verified impact from likely/inferred impact.
4. Consider compatibility, rollout, data migration/backfill, failure modes, side effects, observability, and rollback where applicable.
5. Prefer the smallest coherent implementation sequence that respects repository conventions.
6. Identify decisions the implementer must make; do not hide ambiguity inside a confident file list.

## Deliver

Provide current behavior, proposed approach, affected files/symbols grouped by responsibility, contract/data implications, test plan, ordered implementation steps, risks, and open decisions. Cite evidence for current behavior and verified impact. Do not claim a file must change solely because its name looks related.

Verify references and impact paths. Recommend a focused `$codebase-trace` or `$codebase-deep-dive` if additional analysis would materially reduce uncertainty.
