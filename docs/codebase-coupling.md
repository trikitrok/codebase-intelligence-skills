# Codebase Coupling

The `codebase-coupling` skill explains how parts of a repository are related, including relationships that are visible in source code and relationships that emerge from how the code evolves.

It is designed to distinguish expected relationships from potentially hidden or unclear dependencies without treating coupling metrics as automatic proof of a design problem.

> This is a human-facing usage guide. The authoritative agent behavior is defined in [`skills/codebase-coupling/SKILL.md`](../skills/codebase-coupling/SKILL.md).

## How to use it

Name a file, module, subsystem, or small area to investigate:

```text
$codebase-coupling Find and explain hidden coupling around billing.
```

You can ask for a specific comparison or concern:

```text
$codebase-coupling
Analyze the coupling between the order service and payment service. Compare change history, static dependencies, shared domain concepts, and coordinated tests.
```

```text
$codebase-coupling
Use Code Maat if available and investigate whether these files are unexpectedly changed together: src/orders/Order.ts and src/pricing/Pricing.ts.
```

```text
$codebase-coupling
Investigate coupling across the customer boundary. Focus on hidden dependencies in messages, schemas, configuration, duplicated knowledge, fixtures, and tests.
```

For the strongest history-based analysis, we recommend installing [Code Maat](code-maat.md). If you prefer not to install it, the skill still works with the local Git fallback and source-level inspection.

## What it does

The skill investigates four complementary relationship types:

- **Temporal/evolutionary coupling** — files or modules that tend to change together in version-control history.
- **Static coupling** — visible relationships such as imports, calls, interfaces, and direct dependencies.
- **Logical/domain coupling** — shared business knowledge or concepts that may appear through models, messages, schemas, configuration, or duplicated rules even without a direct code dependency.
- **Test coupling** — coordinated relationships between production code, tests, fixtures, mocks, and test data.

It then:

1. Anchors the analysis to a named subject or small meaningful scope.
2. Runs bounded temporal-coupling analysis and reviews its history quality.
3. Selects a bounded set of temporal pairs or source-defined relationships.
4. Inspects relevant source, configuration, models, messages, schemas, fixtures, mocks, and tests.
5. Compares historical relationships with visible static, domain, and test relationships.
6. Classifies relationships as `expected`, `potentially hidden`, or `unclear`.
7. Reports endpoints, provider evidence, source/test evidence, implications, uncertainty, and limitations.

The result is an explanation of meaningful relationships, not an exhaustive coupling graph.

## Why change history matters

Two modules can be coupled even when neither imports the other. If they repeatedly change together, they may share an implicit dependency such as duplicated business knowledge, a shared protocol, a string-based convention, or an architectural boundary that is difficult to see in the source.

The reverse can also be healthy: production code and its tests often change together for exactly the right reason. Temporal coupling is therefore evidence to interpret, not a defect label.

## Recommended provider: Code Maat

Code Maat is recommended for the strongest temporal-coupling analysis because it provides provider-defined change-coupling observations from version-control history. The skill still compares those observations with source-level relationships, so Code Maat does not replace semantic inspection.

If you prefer not to install Code Maat, the skill works with the repository’s bounded, rename-aware Git co-change analysis. The Git fallback may produce different metrics, so the provider, definitions, history quality, and limitations should remain visible in the result.

See the [Code Maat guide](code-maat.md) for installation options, integration notes, and provider trade-offs.

## When to use it

Use `codebase-coupling` when you want to understand why parts of a repository evolve together or where hidden dependencies may exist.

Choose another skill when your goal is different:

- Investigate maintenance candidates → `codebase-hotspots`
- Map the system’s structure → `codebase-architecture`
- Understand one subsystem deeply → `codebase-deep-dive`
- Follow one execution path → `codebase-trace`
- Plan a specific code change → `codebase-change`
- Check claims or documentation against the code → `codebase-verify`

Coupling analysis is especially useful when a change crosses an unexpected boundary, when modules seem to co-evolve, or when the source structure does not explain the maintenance work developers observe.

## What it does not do

The skill does not attempt to:

- Build an exhaustive static or temporal dependency graph
- Treat high coupling as automatically bad
- Compute static, logical/domain, or test coupling from metrics alone
- Classify technical debt or architectural quality without source evidence
- Expand into an unrelated subsystem deep dive

It stops at a bounded set of meaningful relationships and reports when temporal history is insufficient.

## Source and output expectations

- Repository source and history are treated as read-only unless you explicitly request a change.
- Code Maat is recommended but optional; Git fallback remains available.
- Installing or configuring an external provider requires explicit user permission.
- Important relationships should be supported by provider, source, configuration, or test evidence.
- The result is normally a bounded coupling analysis in chat, with uncertainty and limitations clearly stated.

For the exact analysis rules and stopping criteria, see [`SKILL.md`](../skills/codebase-coupling/SKILL.md).
