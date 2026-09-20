# Codebase Change

The `codebase-change` skill plans a requested repository change using verified and inferred impact from the existing codebase.

It is designed to answer “what needs to change, where, in what order, and with what risks?” before implementation begins.

> This is a human-facing usage guide. The authoritative agent behavior is defined in [`skills/codebase-change/SKILL.md`](../skills/codebase-change/SKILL.md).

## How to use it

Describe the change you want planned:

```text
$codebase-change Plan adding idempotency to the order-submission endpoint.
```

Include compatibility or operational constraints when they matter:

```text
$codebase-change
Plan replacing the legacy payment provider. Preserve the current API, support a gradual rollout, and include migration, observability, failure, and rollback considerations.
```

```text
$codebase-change
Plan adding email notifications when an invoice is paid. Identify the right extension point, affected events and jobs, configuration, tests, retry behavior, and any open product decisions.
```

```text
$codebase-change
Plan this schema change for a live system. Keep existing clients compatible and explain the rollout and rollback sequence.
```

## What it does

The skill:

1. Restates the requested behavior and compatibility constraints.
2. Traces the current behavior before proposing changes.
3. Identifies the appropriate extension point or affected boundaries.
4. Inspects affected APIs, schemas, persistence, configuration, events, jobs, clients, generated boundaries, operations, callers, fixtures, and tests as applicable.
5. Separates verified impact from inferred impact.
6. Considers compatibility, rollout, migration, failure handling, observability, and rollback.
7. Produces an ordered implementation and test plan.
8. Records risks and materially missing decisions.

The plan should explain the current behavior, affected areas, intended change, implementation sequence, verification strategy, risks, and open decisions.

## Important behavior

This skill is planning-only by default. It does not edit the repository or implement the change unless you explicitly request implementation as part of your task.

It asks a clarifying question only when a missing product or compatibility decision could materially change the plan. Otherwise, it states a narrow assumption and proceeds.

The plan should not claim completeness. It should identify the evidence inspected and make remaining uncertainty visible.

## When to use it

Use `codebase-change` before implementing a non-trivial feature, refactor, migration, integration, or behavior change.

Choose another skill when you need a different kind of analysis first:

- New to the repository → `codebase-onboarding`
- Learn the whole system progressively → `codebase-conversational-tutorial`
- Map the system’s structure → `codebase-architecture`
- Follow one execution path → `codebase-trace`
- Understand one subsystem deeply → `codebase-deep-dive`
- Check existing claims or documentation against the code → `codebase-verify`

You can combine them: for example, use onboarding to understand the repository, deep dive to understand the affected subsystem, then use `codebase-change` to produce the implementation plan.

## What it considers

Depending on the requested change, the plan may cover:

- Public APIs and callers
- Data models, schemas, and persistence
- Configuration and deployment boundaries
- Events, jobs, queues, and external integrations
- Generated code and client contracts
- Fixtures, mocks, and tests
- Compatibility and migration strategy
- Failure modes, retries, transactions, and rollback
- Observability and operational readiness

The investigation remains scoped to the requested change and stops when current behavior, extension points, impact, ordered implementation and test steps, risks, and open decisions are clear.

## Source and output expectations

- Repository source is treated as read-only unless implementation is explicitly requested.
- Claims should be grounded in real paths, symbols, configuration, tests, or repository-native evidence.
- Verified and inferred impact should be clearly distinguished.
- The result is normally a structured implementation plan in chat, not a code change.

For the exact analysis rules and stopping criteria, see [`SKILL.md`](../skills/codebase-change/SKILL.md).
