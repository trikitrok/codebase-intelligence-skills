# Codebase Verify

The `codebase-verify` skill audits technical claims and diagrams against the current repository without silently rewriting the artifact being audited.

It is useful when you want to know whether documentation, architecture notes, runbooks, diagrams, or other technical material still matches the code.

> This is a human-facing usage guide. The authoritative agent behavior is defined in [`skills/codebase-verify/SKILL.md`](../skills/codebase-verify/SKILL.md).

## How to use it

Give the skill the artifact and, when useful, the scope of the audit:

```text
$codebase-verify Audit docs/architecture.md against the current repository.
```

You can focus the audit on a particular kind of claim:

```text
$codebase-verify
Check this API documentation against the current routes, handlers, schemas, authorization rules, and tests. Report every material discrepancy without editing the document.
```

```text
$codebase-verify
Audit the architecture diagram in docs/system.md. Verify each meaningful node and edge against registrations, imports, runtime flows, configuration, and tests.
```

```text
$codebase-verify
Check this deployment runbook against the current configuration and repository-native commands. Separate verified facts, inferences, unknowns, and contradictions.
```

The artifact can be a Markdown document, diagram, configuration explanation, API description, runbook, or another technical document available in the workspace.

## What it does

The skill:

1. Obtains the artifact and audit scope.
2. Extracts material claims and meaningful diagram nodes and edges.
3. Classifies each claim, such as an existence claim, API/symbol claim, static relationship, runtime flow, architectural boundary, history/metric claim, or intent claim.
4. Uses targeted filesystem searches, `rg`, Git, and bounded repository helpers where appropriate.
5. Inspects definitions, callers, configuration, tests, and reachability for semantic claims.
6. Investigates contradictions between the artifact, source, tests, configuration, history, and runtime-related evidence.
7. Classifies each material claim as:
   - `VERIFIED` — supported by current repository evidence;
   - `INFERRED` — a reasonable interpretation that is not directly established;
   - `UNKNOWN` — not verifiable from the available evidence; or
   - `CONTRADICTED` — current evidence conflicts with the claim.
8. Reports an audit summary, discrepancy table, invalid nodes or edges, scope, blind spots, and limitations.

## What the result looks like

A useful audit normally includes:

- The artifact and repository scope examined
- A claim-by-claim status
- Evidence such as paths, symbols, callers, configuration, tests, or history
- Explanations for contradictions and discrepancies
- Invalid or unsupported diagram nodes and edges
- Unverified assumptions and blind spots
- Limitations, including runtime behavior that cannot be proven statically

The audit preserves the original artifact. It reports what should be corrected without rewriting the source document for you.

## When to use it

Use `codebase-verify` when you already have a technical artifact or claim set and need to check whether it remains accurate.

Choose another skill when your goal is to understand or change the repository instead:

- New to the repository → `codebase-onboarding`
- Learn the whole system progressively → `codebase-conversational-tutorial`
- Map the system’s structure → `codebase-architecture`
- Follow one execution path → `codebase-trace`
- Understand one subsystem deeply → `codebase-deep-dive`
- Plan a repository change → `codebase-change`

Verification can also be a useful follow-up after an architecture map, trace, tutorial, or change plan has been written.

## What it does not do

The skill does not:

- Silently rewrite or “fix” the audited artifact
- Treat a lexical match as proof of semantic correctness
- Invent evidence for claims that cannot be verified
- Use or recreate a generic lexical verification helper
- Claim that static inspection proves runtime behavior when it does not

It stops once every material claim is classified, contradictions are explained, and important blind spots are stated.

## Source and output expectations

- Repository source is treated as read-only unless you explicitly request a change.
- Claims should be checked against current repository evidence rather than filenames or documentation alone.
- Material uncertainty should be labeled explicitly as `INFERRED`, `UNKNOWN`, or `CONTRADICTED` where appropriate.
- The result is normally an audit report in chat; the original artifact remains unchanged.

For the exact analysis rules and stopping criteria, see [`SKILL.md`](../skills/codebase-verify/SKILL.md).
