---
name: codebase-verify
description: Audit an existing technical explanation, architecture document, tutorial, diagram, or claim against the current repository. Classify material claims as verified, inferred, unknown, or contradicted without rewriting unless requested.
---

# Codebase Verify

Audit the supplied artifact or claims against current repository evidence.

## Start

Read [core conventions](../../shared/references/core.md), the [evidence contract](../../shared/references/evidence-contract.md) when metrics are claimed, and the [verification procedure](../../shared/references/verification.md). Obtain the artifact text/path and repository scope. Do not silently rewrite it.

## Audit

1. Extract atomic material claims. Ignore purely stylistic prose.
2. Classify claim type: existence, symbol/API, static relationship, runtime flow, architectural boundary/independence, metric/history, or intent.
3. Apply the cheapest reliable check first: path/symbol verification, targeted search, evidence-store provenance/query, then source/test inspection.
4. For diagrams, enumerate nodes and meaningful edges; verify each separately. A valid Mermaid parse does not verify semantics.
5. Investigate conflicting source, tests, configuration, runtime/generated evidence, and documentation rather than choosing silently.
6. Assign `VERIFIED`, `INFERRED`, `UNKNOWN`, or `CONTRADICTED` with evidence and a concise rationale.

## Deliver

Lead with an audit summary and the highest-impact discrepancies. Include a compact claim table with claim, status, evidence, and corrective note; group repetitive low-risk checks. For diagrams, report invalid nodes/edges explicitly. State scope and blind spots.

Do not turn absence of a lexical match into proof that semantic behavior is absent. Do not fix the artifact unless requested. If the artifact is stale, suggest a focused follow-up skill rather than starting it.
