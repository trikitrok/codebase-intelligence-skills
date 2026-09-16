# Research and prior art

Research was performed on 2026-09-16 before implementation. External projects were inspected as public source/documentation for design research only; they were not cloned or used as test targets.

## Current Codex conventions

The current [OpenAI skill documentation](https://developers.openai.com/codex/skills) establishes:

- one directory per skill with required `SKILL.md` frontmatter fields `name` and `description`;
- optional `scripts/`, `references/`, `assets/`, and `agents/openai.yaml`;
- progressive disclosure from name/description to `SKILL.md` to referenced resources;
- explicit invocation in Codex using `$skill-name` (or `/skills` for discovery);
- repository skill discovery under `.agents/skills`, plus user/admin/system scopes;
- `policy.allow_implicit_invocation: false` for explicit-only skills;
- focused skills, instructions before scripts except for deterministic behavior, and explicit inputs/outputs.

Current guidance recommends a plugin to distribute multiple reusable skills. The [plugin packaging documentation](https://developers.openai.com/plugins/build/plugins) now prefers root `plugin.json` using the portable Agent Plugins schema and continues supporting `.codex-plugin/plugin.json` as a Codex compatibility fallback. This repository includes both.

There is no documented special nested/shared skill mechanism required here. The plugin packages ordinary files, so independent skills link to common plugin resources through relative paths. This keeps shared infrastructure non-user-facing and avoids a fake “shared” skill.

## PocketFlow Codebase Knowledge

The current [PocketFlow Codebase Knowledge repository](https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge) implements a six-stage graph: fetch repository files, identify abstractions, analyze relationships, order chapters, write chapters in a batch, and combine the tutorial. Its source uses integer file indices, asks the model for YAML structures, validates indices/order, teaches with analogies, builds Mermaid output, and carries prior-chapter context into later chapters.

Ideas retained:

- a small set of core abstractions;
- pedagogical ordering and why-before-how;
- real source references and concise excerpts;
- diagrams, progressive chapters, and chapter continuity;
- separate discovery, relationship, ordering, writing, and combination concerns.

Improvements made here:

- targeted source exploration rather than concatenating broad file contents into an abstraction prompt;
- evidence statuses and a claim/evidence ledger;
- semantic verification of diagram edges, not only structured-output validity;
- independently invokable repository capabilities rather than a tutorial-only application;
- local/private-repository defaults without a separate LLM API or GitHub crawl;
- provenance-aware deterministic evidence and candidate filtering.

## rowlando/codebase-tutorial

The current [rowlando/codebase-tutorial repository](https://github.com/rowlando/codebase-tutorial) was inspected directly through its `SKILL.md` and references. It translates the PocketFlow pipeline into one Agent Skill with no separate API key, curates a roughly 15–40 file manifest, emphasizes “essence before scaffolding,” persists intermediate JSON for resumability, carries a running chapter summary, validates indices/order, sanitizes Mermaid labels, and checks internal links.

Useful ideas retained:

- a native Agent Skill can be the reasoning engine;
- strong curation beats exhaustive reading;
- domain essence should dominate generic framework plumbing;
- intermediate artifacts can make a requested large tutorial resumable;
- links and structured indices deserve deterministic checks.

Differences and limitations addressed:

- it is one tutorial skill, whereas this suite separates nine user intents;
- its fetch step still begins by reading each kept file and its abstraction stage can be broad, while this suite defaults to targeted search;
- file-index validity and Mermaid parsing do not prove claims or edges semantically;
- scratch-file reuse lacks the repository HEAD/provider/parameter/schema invalidation contract used here;
- it does not provide shared history evidence, provider adapters, filtering, hotspots, coupling, or general artifact verification;
- its repository predates or omits the current plugin bundle and `agents/openai.yaml` presentation/invocation policy used here.

## Code Maat and behavioral analysis

The [Code Maat project](https://github.com/adamtornhill/code-maat) mines VCS logs for revisions, churn, coupling, ownership/effort, fragmentation, age, messages, and organizational measures. It supports component mappings and machine-readable CSV. Its documentation also stresses history as socio-technical evidence, sensible time windows, changeset filtering, provider-defined coupling percentages, and the heuristic—not absolute—nature of ownership/churn metrics.

This suite therefore treats Code Maat as an optional provider, preserves its metric definition/range, and supplies a small adapter rather than coupling consuming skills to its raw CSV. The default Git provider offers a zero-install subset. Code Maat is not mandatory because it requires a JVM/container, works from prepared logs, can use substantial memory, and may not already be present in a private-repository environment.

Behavioral concepts adopted from Adam Tornhill's published work and Code Maat documentation include hotspot candidate ranking, change frequency plus churn, temporal/logical coupling, ownership concentration, changeset-size filtering, and component mappings. The suite refuses the stronger unsupported leap from a metric to technical debt or bad architecture.
