# Codebase Trace

The `codebase-trace` skill follows one named behavior through a repository, from its concrete trigger to its observable result or terminal side effect.

It is useful when you know what behavior you care about but need to understand how that behavior is registered, dispatched, transformed, authorized, persisted, and completed.

> This is a human-facing usage guide. The authoritative agent behavior is defined in [`skills/codebase-trace/SKILL.md`](../skills/codebase-trace/SKILL.md).

## How to use it

Name the route, command, event, job, UI action, API, or test you want followed:

```text
$codebase-trace Trace POST /api/orders.
```

Other useful requests include:

```text
$codebase-trace
Trace what happens when a user submits the checkout form, from the UI action to the final persistence or error result.
```

```text
$codebase-trace
Follow the nightly invoice job from scheduling through processing, retries, and completion.
```

```text
$codebase-trace
Trace the `CreateSubscription` command, including authorization, validation, transaction boundaries, external calls, and failure paths.
```

The behavior should be specific enough to identify one concrete path. If several materially different matches exist, clarify the target rather than assuming the wrong one.

## What it does

The skill follows the selected behavior through:

1. Registration and the concrete trigger
2. Dispatch and routing
3. Transformations and decisions
4. Dependencies and state changes
5. External calls and side effects
6. The observable result or terminal side effect

It also inspects relevant error handling, retries, transactions, concurrency, and authorization paths. The explanation records verified hops in the form:

```text
from symbol → mechanism → to symbol
```

When useful, it includes a sequence diagram and identifies alternate paths or runtime gaps that cannot be verified statically.

## What the result looks like

A useful trace normally explains:

- The initial trigger and entry point
- The symbols and mechanisms traversed in order
- Important decisions and data transformations
- State ownership and persistence effects
- External systems or integrations involved
- Success, failure, retry, authorization, and alternate paths
- The final observable result
- Any runtime behavior that remains uncertain

The trace stays focused on the named behavior and stops at its result. It does not expand into an unrelated architecture tour or exhaustive subsystem analysis.

## When to use it

Use `codebase-trace` when you need to answer a question like “What happens when this event occurs?” or “How does this request reach that result?”

Choose another skill when your goal is broader or differently scoped:

- New to the repository → `codebase-onboarding`
- Learn the whole system progressively → `codebase-conversational-tutorial`
- Map the system’s structure → `codebase-architecture`
- Understand one subsystem deeply → `codebase-deep-dive`
- Plan a code change → `codebase-change`

Tracing is especially useful for debugging, reviewing an unfamiliar feature, checking documentation against implementation, or preparing a focused change.

## Source and output expectations

- Repository source is treated as read-only unless you explicitly request a change.
- Claims should be grounded in real paths, symbols, configuration, tests, or verified repository relationships.
- Static evidence should be distinguished from runtime behavior that cannot be confirmed from the repository.
- The result is normally a concise trace in chat, with a sequence diagram when it materially improves understanding.

For the exact analysis rules and stopping criteria, see [`SKILL.md`](../skills/codebase-trace/SKILL.md).
