# Analysis basics

1. Resolve the repository root and read applicable repository instructions before analysis.
2. Treat the target repository as read-only unless the user explicitly requests implementation.
3. `codebase-change` is planning-only by default.
4. Prefer targeted `rg`, manifests, configuration, tests, Git, and repository-native commands.
5. Do not assume a programming language or framework.
6. Clarify scope only when choosing incorrectly would materially invalidate the result; otherwise state a narrow assumption and proceed.
7. Use selective source inspection rather than broad source ingestion.
8. Use `VERIFIED`, `INFERRED`, `UNKNOWN`, and `CONTRADICTED` when they clarify material uncertainty.
9. Never invent paths, symbols, calls, imports, relationships, behavior, metrics, or history.
10. Use repository-relative paths and real symbols in user-facing evidence.
11. A lexical match proves occurrence only; semantic claims require inspection of definitions, callers, configuration, or tests.
12. Follow material contradictions between source, tests, configuration, generated/runtime evidence, and documentation.
13. Observations are not conclusions.
14. Verify important paths, symbols, transitions, relationships, metric definitions, limitations, and diagram edges before reporting.
15. Never upload private source, history, metadata, or results without explicit user intent and permission.
16. Never install or configure an external tool without explicit permission.
17. Recommend another Codebase Intelligence skill rather than silently starting a separate expensive analysis.
18. Lead with the requested mental model or answer rather than a file inventory.
