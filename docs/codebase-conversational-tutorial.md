# Codebase Conversational Tutorial

The `codebase-conversational-tutorial` skill teaches you how a repository works through a progressive explanation of its most important concepts and source code.

It is designed for understanding the system’s distinctive mechanisms—not for producing an exhaustive inventory of every directory and file.

> This is a human-facing usage guide. The authoritative agent behavior is defined in [`skills/codebase-conversational-tutorial/SKILL.md`](../skills/codebase-conversational-tutorial/SKILL.md).

## How to use it

Invoke the skill explicitly in your request:

```text
$codebase-conversational-tutorial Teach me how this repository works.
```

You can add the audience, focus, and preferred format to make the tutorial more useful:

```text
$codebase-conversational-tutorial
Teach me this repository as a competent TypeScript developer.
```

```text
$codebase-conversational-tutorial
Give me a beginner-friendly tutorial focused on the authentication flow.
```

```text
$codebase-conversational-tutorial
Explain the core domain model first, then show how a request moves through the system.
Use a diagram only if it clarifies the relationships.
```

If you do not specify these preferences, the skill assumes a competent developer, a balanced repository-wide focus, and a conversational answer in chat.

## What it does

The skill:

1. Reconnoiters the repository and identifies its important entry points and boundaries.
2. Curates a small set of genuine core concepts.
3. Verifies each concept against real source files, symbols, configuration, and tests.
4. Explains relationships between the concepts.
5. Orders the explanation from purpose and foundations toward implementation and dependants.
6. Includes relevant excerpts, edge behavior, reading guidance, or diagrams when they improve understanding.
7. Calls out limitations and unresolved uncertainty instead of presenting guesses as facts.

The result is normally delivered directly in the conversation. It does not create documentation files unless you explicitly request an artifact.

## Choosing a focus

A broad request gives you a balanced mental model of the repository. A focused request gives one area more depth while preserving enough surrounding context to understand it:

```text
$codebase-conversational-tutorial
Teach me the billing subsystem, including its callers, state transitions, tests, and failure paths.
```

```text
$codebase-conversational-tutorial
Walk me through the lifecycle of a submitted order from the HTTP request to persistence.
```

## When to use another skill

- Use `codebase-onboarding` for a fast overall orientation, development workflow, and reading order.
- Use `codebase-trace` to follow one named behavior from its trigger to its result.
- Use `codebase-deep-dive` to understand one subsystem in greater detail.
- Use `codebase-architecture` for a repository-wide architecture map.

The conversational tutorial can provide context for these narrower analyses, but it should not replace them when the request is specifically about one trace, subsystem, or architecture audit.

## Source and output expectations

- Repository source is treated as read-only unless you explicitly request a change.
- Claims should be grounded in real paths, symbols, configuration, tests, or other repository evidence.
- The tutorial is adaptive rather than a fixed chapter-generation pipeline.
- Output is chat by default; persistent files are created only when you explicitly request an artifact.

For the exact analysis rules and stopping criteria, see [`SKILL.md`](../skills/codebase-conversational-tutorial/SKILL.md).
