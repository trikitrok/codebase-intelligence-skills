# Codebase Architecture

The `codebase-architecture` skill builds an evidence-backed model of a repository’s meaningful system boundaries and runtime shape.

It explains how the major components, actors, state, integrations, and communication paths fit together, while avoiding an unreadable complete dependency graph.

> This is a human-facing usage guide. The authoritative agent behavior is defined in [`skills/codebase-architecture/SKILL.md`](../skills/codebase-architecture/SKILL.md).

## How to use it

Invoke the skill explicitly in your request:

```text
$codebase-architecture Map this system.
```

You can ask for a particular architectural perspective or scope:

```text
$codebase-architecture
Explain the architecture of this repository, including its runtime units, entry points, state ownership, integrations, and dependency direction.
```

```text
$codebase-architecture
Map the order-processing architecture. Show the components involved, how they communicate, where state is stored, and the main cross-boundary flows.
```

```text
$codebase-architecture
Give me an architecture map focused on extension points and the boundaries I should understand before adding a new notification provider.
```

## What it does

The skill selectively inspects:

- Manifests, runtime units, and build boundaries
- Entry points, configuration, registrations, and dependency direction
- Persistence and state ownership
- External integrations and communication mechanisms
- Tests that clarify component boundaries and behavior
- A few representative flows that cross system boundaries

It then explains and verifies:

1. The repository’s architectural context and major components
2. The responsibilities of each meaningful boundary
3. The actors and communication paths between components
4. Where state is owned and how it moves through the system
5. External integrations and their points of contact
6. Dependency direction and important extension points
7. Representative cross-boundary flows
8. Contradictions, uncertainty, and limitations

Diagrams are included when they make the relationships easier to understand. Every material node and edge should be grounded in repository evidence.

## When to use it

Use `codebase-architecture` when you need to understand the system’s structure, boundaries, runtime shape, or dependency direction.

Choose another skill when your goal is narrower or more introductory:

- New to the repository → `codebase-onboarding`
- Learn the whole system progressively → `codebase-conversational-tutorial`
- Follow one execution path → `codebase-trace`
- Understand one subsystem deeply → `codebase-deep-dive`
- Plan a code change → `codebase-change`

Architecture is especially useful before making a cross-cutting change or evaluating where a new component, integration, or extension belongs.

## What it does not do

The skill does not attempt to:

- Generate a complete call graph or dependency graph
- List every file or framework detail
- Replace a focused subsystem deep dive
- Treat inferred architecture as fact without verifying its important nodes and edges

It stops when the context, components, state, flows, boundaries, extensions, contradictions, and uncertainty are sufficiently clear for the requested scope.

## Source and output expectations

- Repository source is treated as read-only unless you explicitly request a change.
- Important architectural claims should be grounded in real paths, symbols, configuration, tests, or repository-native commands.
- Dependency-analysis commands are used only when they resolve a concrete gap.
- The result is normally an architectural explanation in chat, with evidence-backed diagrams where useful.

For the exact analysis rules and stopping criteria, see [`SKILL.md`](../skills/codebase-architecture/SKILL.md).
