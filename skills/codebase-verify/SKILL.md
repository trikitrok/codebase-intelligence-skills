---
name: codebase-verify
description: Audit technical claims and diagrams against the current repository without silently rewriting them.
---
# Codebase verify
Read [analysis basics](../../shared/references/analysis-basics.md). Obtain the artifact and scope, extract atomic material claims and meaningful diagram nodes/edges, and classify claim types. Apply filesystem, `rg`, Git, or a bounded history-helper check first; inspect definitions, callers, configuration, tests, and reachability for semantic claims. Investigate contradictions and classify each `VERIFIED`, `INFERRED`, `UNKNOWN`, or `CONTRADICTED`. Do not use or recreate a lexical verification helper. Stop when every material claim is classified, contradictions explained, and blind spots stated. Deliver an audit summary, discrepancy table, invalid nodes/edges, scope, and limitations without rewriting the artifact.

When the verification result itself would be clearer visually, read
[diagramming](../../shared/references/diagramming.md) and provide only the
verified entities, relationships, execution paths, boundaries, contradictions,
invalid nodes or edges, and uncertainty relevant to the audit.

Do not use the diagramming skill to silently repair or replace the artifact
being verified. A corrected diagram is a separate output and should be produced
only when explicitly requested.
