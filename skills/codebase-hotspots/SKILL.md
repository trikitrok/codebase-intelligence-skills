---
name: codebase-hotspots
description: Rank and investigate maintenance or technical-debt candidates using Git-history evidence plus selective source inspection. Use for hotspots; never equate frequent change or churn with debt.
---

# Codebase Hotspots

Use deterministic observations to find a small candidate set, then inspect source before interpreting it.

## Start

Read [core conventions](../../shared/references/core.md), the [tool-first workflow](../../shared/references/tool-first.md), the [evidence contract](../../shared/references/evidence-contract.md), and [provider selection](../../shared/references/tool-providers.md).

## Analyze

1. Discover repository ecosystems, configured tools, Git availability, history depth, and existing valid evidence.
2. Reuse provenance-valid evidence or generate Git fallback observations for change frequency, churn, temporal coupling, and ownership. Never install Code Maat or another provider without the shared permission flow.
3. Query/rank candidates deterministically. Explain ranking criteria and avoid mixing differently defined metrics as equivalent.
4. Remove obvious generated/vendor/fixture noise and account for bulk commits, renames, repository age, shallow history, and changeset caps.
5. Inspect the selected source, boundaries, callers, and tests for excessive responsibility, complex flow, duplication, broad change surface, fragile/missing tests, repeated fixes, configuration burden, boundary leakage, or expected healthy change.
6. Treat defect/fix patterns only as evidence when commit classification is reliable; commit-message keywords alone are weak evidence.

## Deliver

Separate candidates into:

- strong technical-debt evidence;
- maintenance hotspots worth investigating;
- high-change areas that appear healthy;
- insufficient-evidence candidates.

For each significant candidate, include historical observations with provider semantics, selective source evidence, interpretation, evidence status, maintenance implication, and uncertainty. Do not recommend a rewrite from metrics alone.

Run the shared verification pass. Suggest `$codebase-coupling` for unexplained co-change or `$codebase-deep-dive` for a focused subsystem; do not invoke them silently.
