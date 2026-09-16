---
name: codebase-hotspots
description: Find and semantically investigate bounded maintenance candidates from history.
---
# Codebase hotspots
Read [analysis basics](../../shared/references/analysis-basics.md) and [history analysis](../../shared/references/history-analysis.md). Run `history_candidates.py hotspots` with `auto` unless a provider is requested. Review history quality, then selectively inspect only a bounded subset of candidates, their history, source, boundaries, callers, and tests. Investigate confounders and classify candidates as strong debt evidence, investigation-worthy, healthy high-change, or insufficient evidence. Never label a candidate debt from metrics alone. Stop at the bounded set and do not reconstruct an unbounded ranking. Report provider-defined observations, semantic evidence, status, implications, uncertainty, and limitations.
