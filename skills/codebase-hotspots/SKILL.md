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
2. Select a suitable hotspot provider. Prefer an available, approved Code Maat analysis and normalize its provider-defined revisions/entity-churn hotspot evidence. Otherwise use the dependency-free Git + current tracked LOC fallback. Never install Code Maat or another provider without the shared permission flow.
3. Reuse provenance-valid evidence or generate observations for change frequency, size/churn, temporal coupling, and ownership. Rank candidates with `rank-hotspots`; explain provider semantics and do not mix differently defined metrics as equivalent.
4. Remove obvious generated/vendor/build/cache noise and account for bulk commits, renames, repository age, shallow history, and changeset caps. The fallback LOC proxy counts physical lines, including blank lines, in current tracked text files; a final newline does not add a line.
5. Inspect the selected source, boundaries, callers, and tests for excessive responsibility, complex flow, duplication, broad change surface, fragile/missing tests, repeated fixes, configuration burden, boundary leakage, or expected healthy change.
6. Treat defect/fix patterns only as evidence when commit classification is reliable; commit-message keywords alone are weak evidence.

## Deliver

Separate candidates into:

- strong technical-debt evidence;
- maintenance hotspots worth investigating;
- high-change areas that appear healthy;
- insufficient-evidence candidates.

For each significant candidate, include historical observations with provider semantics, selective source evidence, interpretation, evidence status, maintenance implication, and uncertainty. A fallback hotspot score is the product of descending within-set ranks for revisions and LOC; Code Maat ranking uses its revisions and absolute entity-churn definitions. Do not recommend a rewrite from metrics alone.

Run the shared verification pass. Suggest `$codebase-coupling` for unexplained co-change or `$codebase-deep-dive` for a focused subsystem; do not invoke them silently.
