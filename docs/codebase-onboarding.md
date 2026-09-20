# Codebase Onboarding

The `codebase-onboarding` skill gives you a fast, evidence-backed mental model of an unfamiliar repository so you can start working in it with confidence.

It focuses on practical orientation: what the system is for, where it starts, how its main workflows operate, how it is developed and tested, and where future changes are likely to belong.

> This is a human-facing usage guide. The authoritative agent behavior is defined in [`skills/codebase-onboarding/SKILL.md`](../skills/codebase-onboarding/SKILL.md).

## How to use it

Invoke the skill explicitly in your request:

```text
$codebase-onboarding Orient me to this repository.
```

You can add context about your role, goals, or the area where you expect to work:

```text
$codebase-onboarding
I am new to this Python repository. Explain its purpose, entry points, development commands, tests, and the best reading order.
```

```text
$codebase-onboarding
I need to add a billing feature. Show me the relevant boundaries, representative flows, extension points, and files where changes probably belong.
```

```text
$codebase-onboarding
Give me a concise orientation to this repository. Include the system map, one representative workflow, how to run and test it, and any important contradictions or unknowns.
```

## What it does

The skill selectively inspects:

- Repository purpose and top-level structure
- Manifests, configuration, entry points, and boundaries
- Central abstractions, state, integrations, and extension points
- Development commands and tests
- One or two representative workflows

It then verifies the important paths and symbols and explains:

1. The repository’s purpose and boundaries
2. Its main entry points and representative flows
3. The system map and important state or integrations
4. How developers run, test, and work with the repository
5. Where common changes and extensions belong
6. A prioritized reading order
7. Contradictions, uncertainty, and limitations

The result is a concise orientation, not an exhaustive file inventory or a full architecture audit.

## When to use it

Use `codebase-onboarding` when you are new to a repository or need enough context to plan your next task.

Choose another skill when the request is narrower:

- Learn the whole system progressively → `codebase-conversational-tutorial`
- Map the system’s structure in detail → `codebase-architecture`
- Follow one execution path → `codebase-trace`
- Understand one subsystem deeply → `codebase-deep-dive`
- Plan a code change → `codebase-change`

Onboarding is usually the best first step when you do not yet know which part of the repository matters.

## Source and output expectations

- Repository source is treated as read-only unless you explicitly request a change.
- Important claims should be grounded in real paths, symbols, configuration, tests, or repository-native commands.
- The exploration is selective and stops once the repository’s purpose, boundaries, workflows, change locations, and reading order are clear.
- The skill should distinguish verified facts from inferences and unresolved unknowns.

For the exact analysis rules and stopping criteria, see [`SKILL.md`](../skills/codebase-onboarding/SKILL.md).
