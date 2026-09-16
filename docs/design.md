# Design decisions

## Package, not a mega-skill

The suite is a plugin with nine independent skill entrypoints. Explicit-only `agents/openai.yaml` policies enforce the specification's user-controlled composition. Root `plugin.json` follows the current portable format; `.codex-plugin/plugin.json` supports existing Codex ingestion.

## Shared files, not a shared skill

Substantial policy and mechanics live under `shared/`. Each skill reads only the core and strategy/provider references it needs. The shared layer is not invokable, has no `SKILL.md`, and does not compete in skill discovery.

## One small deterministic CLI

A standard-library CLI was chosen over many copied scripts or a framework. Subcommands share repository identity, provenance, schema validation, JSON I/O, and failure handling. The tool records observations; skills own semantic interpretation.

Hotspot discovery is capability-oriented: available/approved Code Maat revisions and entity-churn analyses are the preferred behavioral provider; the zero-install fallback combines Git change frequency with a tracked physical-LOC proxy. Code Maat support is an adapter, not a dependency, and no ecosystem-specific complexity analyzer is required for baseline hotspots. Ecosystem tools extend capabilities through the same observation envelope when their definitions and units are preserved.

## Evidence store and cache

One JSON store contains observations and provenance, and cache reuse is simply validated store reuse. This avoids two representations. Store-level provenance supports cheap checks; every observation repeats provenance so it remains interpretable if extracted.

Because Evidence v1 repeats provenance, store validation requires each observation's copy to exactly match the store copy and requires repository metadata to agree with both. Cache validation accepts a provider-specific analysis request rather than optional expected fields: Git parameters are always constructed, while Code Maat requires a currently discovered version, analysis, and hashed CSV input.

The repository identifier hashes the origin URL when present or the root commit otherwise, so moving a clone does not inherently invalidate history evidence. HEAD, provider and analyzer versions, parameters, schema, and analysis inputs do. Dirty state is recorded, but only invalidates evidence that consumed working-tree content; Git+LOC hotspot evidence does. Code Maat adapter provenance also hashes its raw CSV input.

Provider independence is implemented as two small producers/adapters sharing the evidence envelope, validator, and query interface. New providers are extension points requiring an explicit adapter and provider-specific cache-request validation. A registry, generic provider SDK, and dynamic plugin framework are deliberately not implemented.

## Component boundaries

The deterministic layer does not infer architecture from folders. Component aggregation remains downstream of manifests/build modules, explicit mappings, architecture configuration, source evidence, or user input. This avoids turning convenient directory names into asserted system design.

## Verification

The common verification reference combines deterministic checks with semantic review. The helper's reference verifier intentionally describes its symbol result as lexical. Skills must inspect definitions/callers for semantic claims and individually verify diagram edges.

## Tool installation and privacy

No command installs a tool. Skills must discover first, explain capability/value/dependencies/data handling, request permission, and retain a useful fallback. All bundled processing is local; no connector or remote service is required.

## Deliberate non-features

- no generic AST ontology or graph database;
- no bundled complexity formula pretending to work across languages;
- no automatic technical-debt label;
- no automatic component inference from directory depth;
- no silent chaining between skills;
- no generated human report mixed into the evidence cache.
