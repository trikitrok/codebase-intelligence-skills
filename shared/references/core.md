# Shared analysis contract

Read this reference at the start of every Codebase Intelligence analysis.

## Scope and repository safety

- Resolve the repository root and read applicable `AGENTS.md` files before analysis.
- Treat the target repository as read-only unless the user explicitly asks for implementation. `codebase-change` is planning-only by default.
- Prefer `rg`, `rg --files`, project manifests, Git, and project-native commands. Do not assume a language.
- Never upload private source, history, metadata, or results to a third-party service without explicit user intent and permission.
- Keep generated machine evidence outside the target repository by default. Use the helper's `default-store` result or another user-approved path. Human documentation is separate from evidence/cache data.

## Evidence statuses

Use statuses for material claims when they make uncertainty clearer:

- `VERIFIED`: directly supported by inspected evidence.
- `INFERRED`: strongly suggested but not directly demonstrated.
- `UNKNOWN`: evidence is insufficient.
- `CONTRADICTED`: available evidence conflicts with the claim.

Never present an inference as verified. Never invent a path, symbol, call, import, edge, behavior, historical relationship, or metric.

## Exploration discipline

1. Clarify the subject only when ambiguity would materially change the analysis; otherwise state a narrow assumption and proceed.
2. Inventory the repository cheaply: governing instructions, top-level structure, manifests, entry points, tests, and configuration.
3. Select source-first, tool-first, or evidence-first behavior as directed by the invoking skill.
4. Keep an evidence ledger for material claims: claim, status, repository-relative path, symbol or line where useful, evidence kind, and limitation.
5. Follow contradictions. Executable source is usually stronger than tests, then configuration, runtime/generated evidence, current docs, README, and comments—but assess staleness and dead code rather than applying that order mechanically.
6. Inspect tests when they define behavior, contracts, failure modes, or extension points.

## Source references

Use repository-relative paths and real symbols. Add a line number only after checking it; line numbers are aids, not stable identity. Prefer concise excerpts over source dumps. For multiple repositories, name the repository with each reference.

Before reporting, verify referenced files and important symbols. A lexical symbol check proves only that text occurs; confirm semantic claims by inspecting its definition and relevant callers.

## Tool selection and permission

Inspect languages, manifests, existing configuration, and available commands before recommending anything. Prefer configured project-native tools. If an optional external tool would materially improve the result, explain:

1. the missing capability;
2. the proposed open-source/local provider;
3. why it improves this analysis;
4. installation/runtime dependencies and whether data leaves the machine;
5. the useful fallback.

Then ask permission before installing. If unavailable or declined, use the fallback and state the limitation. Never fabricate the missing metric.

## Verification gate

Read [verification.md](verification.md) before the final verification pass. Report meaningful contradictions and limitations. Recommend another Codebase Intelligence skill when it would add value; do not silently start a separate expensive analysis.

## Output baseline

Lead with the mental model or answer, not a file inventory. Support important conclusions with evidence. Separate observations from interpretations, include uncertainty, and keep the result focused on the requested depth.
