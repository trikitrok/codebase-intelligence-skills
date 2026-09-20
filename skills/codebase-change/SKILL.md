---
name: codebase-change
description: Plan a requested repository change using verified and inferred impact.
---
# Codebase change
Read [analysis basics](../../shared/references/analysis-basics.md). This skill is planning-only unless implementation is explicitly requested. Restate behavior and compatibility constraints, ask only for a materially missing product decision, trace current behavior, and inspect affected APIs, schemas, persistence, configuration, events/jobs, clients, generated boundaries, operations, callers, fixtures, and tests. Separate verified from inferred impact and consider compatibility, rollout, migration, failure, observability, and rollback. Stop when current behavior, extension point, impacts, ordered implementation/test plan, risks, and open decisions are covered. Do not edit or claim completeness.

When current behavior, proposed structure, change impact, migration, or rollout
would be clearer visually, read
[diagramming](../../shared/references/diagramming.md) and provide the verified
current structure and behavior, proposed changes, affected components and
relationships, boundaries, compatibility constraints, migration or rollout
steps, and uncertainty. Clearly distinguish verified current behavior from
planned or inferred future behavior.
