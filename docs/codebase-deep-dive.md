# Codebase Deep Dive

The `codebase-deep-dive` skill explains one focused subsystem or concept in depth, including how it is constructed, how it changes state, how it fails, and how it is tested.

It is intended for questions that are too detailed for a repository overview but broader than tracing one request from trigger to result.

> This is a human-facing usage guide. The authoritative agent behavior is defined in [`skills/codebase-deep-dive/SKILL.md`](../skills/codebase-deep-dive/SKILL.md).

## How to use it

Name the subsystem or concept you want to understand:

```text
$codebase-deep-dive Explain the billing subsystem.
```

You can specify the aspects that matter most:

```text
$codebase-deep-dive
Explain the authentication subsystem, including its API, construction, configuration, callers, state transitions, failure handling, tests, and extension points.
```

```text
$codebase-deep-dive
Take a deep dive into the job queue. Focus on lifecycle, retries, concurrency, persistence, and what happens when a worker fails.
```

```text
$codebase-deep-dive
Explain the pricing engine in depth. Show its boundary, invariants, downstream effects, representative code, and how the tests protect its behavior.
```

## What it does

The skill first defines the subsystem’s boundary and adjacent context. It then investigates:

- Public APIs and construction
- Configuration and callers
- Dependencies and collaborators
- State, lifecycle, invariants, and transitions
- Downstream effects and integrations
- Failure handling, transactions, retries, and concurrency where applicable
- Tests and extension seams

The result typically includes:

1. A focused model of the subsystem
2. A walkthrough of its important internals
3. A representative flow or lifecycle
4. The test model and what it protects
5. Failure behavior and important edge cases
6. Extension and change guidance
7. Evidence and limitations

The investigation expands outward only through verified collaborators, so the explanation remains focused instead of becoming a repository-wide tour.

## When to use it

Use `codebase-deep-dive` when you need to understand one subsystem well enough to modify, debug, review, or extend it safely.

Choose another skill when your goal is broader or narrower:

- New to the repository → `codebase-onboarding`
- Learn the whole system progressively → `codebase-conversational-tutorial`
- Map the system’s structure → `codebase-architecture`
- Follow one execution path → `codebase-trace`
- Plan a code change → `codebase-change`

The key distinction from `codebase-trace` is scope: a trace follows one named behavior end to end, while a deep dive explains the subsystem’s boundary, internals, lifecycle, tests, failures, and extension points.

## What it does not do

The skill does not attempt to:

- Explain every subsystem in the repository
- Produce a complete dependency graph
- Expand into unrelated collaborators without verified relevance
- Replace a focused runtime trace when the question is about one concrete trigger-to-result path

It stops when the subsystem’s boundary, internals, lifecycle, failures, tests, and extension seams are sufficiently understood for the requested scope.

## Source and output expectations

- Repository source is treated as read-only unless you explicitly request a change.
- Important claims should be grounded in real paths, symbols, configuration, tests, or repository-native checks.
- Focused repository-native checks are used only to resolve concrete ambiguity.
- The result is normally a detailed explanation in chat, with flows, excerpts, and evidence where useful.

For the exact analysis rules and stopping criteria, see [`SKILL.md`](../skills/codebase-deep-dive/SKILL.md).
