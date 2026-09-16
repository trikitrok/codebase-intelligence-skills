---
name: codebase-coupling
description: Discover and explain static, temporal, domain/logical, and test coupling using normalized evidence and selective source inspection. Use for hidden or change coupling; temporal coupling is not automatically bad design.
---

# Codebase Coupling

Compare coupling signals, then explain important relationships in repository context.

## Start

Read [core conventions](../../shared/references/core.md), the [tool-first workflow](../../shared/references/tool-first.md), the [evidence contract](../../shared/references/evidence-contract.md), and [provider selection](../../shared/references/tool-providers.md).

## Analyze

1. Discover repository boundaries and available/configured providers without broadly reading source.
2. Validate/reuse temporal-coupling evidence or generate it with the Git fallback. Query a bounded set by shared commits and coupling strength.
3. Obtain static relationships from a configured provider when available; otherwise inspect targeted imports, calls, interfaces, messages, shared state/configuration, and APIs.
4. Inspect selected pairs for domain rules, duplicated knowledge/constants/validation, schema assumptions, implicit contracts, shared fixtures/mocks, and coordinated production/test changes.
5. Compare static and temporal evidence. Prioritize strong temporal relationships not explained by static or domain boundaries, but do not presume they are defects.
6. Aggregate to components only when boundaries are supported by manifests, modules, architecture configuration, source, or user-provided mapping. Label inferred boundaries.

## Deliver

For meaningful relationships report endpoints, coupling types (`S`, `T`, `L`, `X`), historical and source evidence, likely explanation, architectural status (`expected`, `potentially hidden`, `unclear`), evidence status, and maintenance implication.

Use a compact coupling matrix when it improves comparison. Every non-empty cell and diagram edge must trace to evidence. State metric definitions and avoid huge file-pair lists.

Run the shared verification pass. Suggest `$codebase-deep-dive` for a suspicious subsystem rather than silently expanding the analysis.
