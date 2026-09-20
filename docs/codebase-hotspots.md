# Codebase Hotspots

The `codebase-hotspots` skill finds and investigates a bounded set of maintenance candidates using version-control history and current source evidence.

It helps answer questions such as: “Which parts of this repository deserve maintenance attention, and what does the source code suggest about why?”

> This is a human-facing usage guide. The authoritative agent behavior is defined in [`skills/codebase-hotspots/SKILL.md`](../skills/codebase-hotspots/SKILL.md).

## How to use it

Ask the skill to investigate maintenance hotspots:

```text
$codebase-hotspots Investigate maintenance hotspots in this repository.
```

You can narrow the scope or ask for a particular kind of interpretation:

```text
$codebase-hotspots
Find the most important maintenance hotspots in the billing area. Separate strong debt evidence from healthy high-change code and insufficient evidence.
```

```text
$codebase-hotspots
Investigate the repository’s top hotspots over the last six months. Explain the history quality, likely confounders, relevant source evidence, and recommended follow-up.
```

```text
$codebase-hotspots
Use Code Maat if it is available; otherwise use the local Git fallback. Do not classify a hotspot as technical debt from metrics alone.
```

## What it does

The skill:

1. Runs the bounded history analysis with the automatic provider selection.
2. Reviews history quality and limitations.
3. Selects only a bounded subset of candidates for semantic investigation.
4. Inspects the selected candidates’ history, source, boundaries, callers, and tests.
5. Looks for confounders such as bulk commits, generated code, migrations, formatting changes, shallow history, or low sample sizes.
6. Classifies each candidate as one of:
   - strong debt evidence;
   - investigation-worthy;
   - healthy high-change; or
   - insufficient evidence.
7. Reports observations, source evidence, implications, uncertainty, and limitations.

The analysis does not reconstruct an unbounded ranking of the entire repository.

## What a hotspot means

A hotspot is a candidate identified from change history and code size or churn. It is a signal for investigation, not a diagnosis.

High activity can be healthy—for example, a central feature under active development—or it can point toward duplicated knowledge, unstable boundaries, or expensive maintenance. The skill must inspect the code and tests before drawing a semantic conclusion.

## Recommended provider: Code Maat

For the strongest history-based analysis, we recommend installing [Code Maat](code-maat.md). It provides provider-defined revision and churn observations that complement the skill’s semantic inspection of source code, boundaries, callers, and tests.

Code Maat is optional. If you prefer not to install it, the skill still works using the repository’s bounded, rename-aware Git fallback. You do not need an external provider to use `codebase-hotspots`.

The two providers do not produce identical metrics. In this repository, Code Maat hotspot churn is absolute entity churn (`added + deleted`), while the Git fallback uses current physical lines of code together with revision history. Results must therefore be interpreted with their provider and metric definitions attached.

See the [Code Maat guide](code-maat.md) for installation options, integration notes, and the trade-offs between the providers.

## When to use it

Use `codebase-hotspots` when you want evidence-led maintenance candidates from the repository’s evolution.

Choose another skill when your question is different:

- Investigate change coupling and hidden dependencies → `codebase-coupling`
- Check claims or documentation against the code → `codebase-verify`
- Plan a specific code change → `codebase-change`
- Understand one subsystem deeply → `codebase-deep-dive`
- Learn the repository before choosing an investigation area → `codebase-onboarding`

Hotspots are especially useful as a starting point for maintenance investigation, not as an automatic technical-debt report.

## Source and output expectations

- Repository source and history are treated as read-only unless you explicitly request a change.
- Code Maat is recommended for the strongest history-based analysis, but Git fallback remains available if you prefer not to install it.
- Installing or configuring an external provider requires explicit user permission.
- Metrics alone never establish that a candidate is defective or technical debt.
- History quality, provider, metric definitions, confounders, uncertainty, and limitations should be reported.
- The result is normally a bounded investigation in chat, not a permanent ranking or cache.

For the exact analysis rules and stopping criteria, see [`SKILL.md`](../skills/codebase-hotspots/SKILL.md).
