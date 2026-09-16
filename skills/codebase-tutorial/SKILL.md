---
name: codebase-tutorial
description: Create a progressive, evidence-backed tutorial that teaches a repository through its core abstractions, real source references, and verified diagrams. Use for a multi-chapter learning guide; use codebase-onboarding for a faster orientation.
---

# Codebase Tutorial

Teach the repository as a sequence of concepts rather than files.

## Start

Read [core conventions](../../shared/references/core.md), the [source-first workflow](../../shared/references/source-first.md), and [tutorial guidance](references/tutorial-workflow.md). Resolve requested audience, focus, target, and output location. If no artifact is requested, present the tutorial in chat; do not create files merely because this skill can.

## Workflow

1. Curate approximately 5–10 core abstractions. Prefer the project's distinctive domain or mechanism over generic scaffolding.
2. Map each abstraction to verified files and symbols, then establish primary relationships.
3. Order concepts pedagogically: purpose and foundations before mechanisms and dependents. Explain why before how.
4. Write progressive chapters using analogies only where they genuinely help, short verified excerpts, cross-links, and suggested reading.
5. Include a Mermaid overview when useful. Verify every meaningful edge against source, configuration, or tests.
6. Audit unsupported claims, paths, symbols, links, and omission of major concepts.

Do not read every matching source file or reproduce PocketFlow's whole-repository prompt approach. Persist intermediate artifacts only when the user asks for generated documentation or the run is large enough that resumability justifies them; keep scratch evidence outside the target repository by default.

Finish with the tutorial, a reading order, and explicit limitations. Recommend `$codebase-verify` for a later independent audit rather than running it silently.
