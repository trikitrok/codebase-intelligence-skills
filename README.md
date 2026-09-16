# Codebase Intelligence

Codebase Intelligence is a local/private plugin of nine explicitly invoked Codex Agent Skills for repository understanding, investigation, verification, and change planning. Codex performs semantic inspection; the bundled helper only bounds historical hotspot and temporal-coupling candidates.

| Goal | Invocation |
|---|---|
| Orient | `$codebase-onboarding Orient me to this repository.` |
| Learn | `$codebase-tutorial Teach me how this repository works.` |
| Architecture | `$codebase-architecture Map this system.` |
| Trace | `$codebase-trace Trace POST /api/orders.` |
| Deep dive | `$codebase-deep-dive Explain the billing subsystem.` |
| Plan | `$codebase-change Plan adding idempotency.` |
| Hotspots | `$codebase-hotspots Investigate maintenance hotspots.` |
| Coupling | `$codebase-coupling Analyze coupling around billing.` |
| Verify | `$codebase-verify Audit docs/architecture.md.` |

Every skill is explicit-only. Source-oriented skills use targeted manifests, configuration, tests, Git, and selective source inspection. Hotspots and coupling first run `python3 shared/scripts/history_candidates.py hotspots` or `temporal-coupling`; results are bounded observations and require semantic source/test inspection. Code Maat is preferred only with valid supplied CSV, an explicit JSON-array command, or an exact `code-maat` executable. Otherwise Git is used: hotspot size is current physical LOC and temporal coupling is shared eligible commits divided by the smaller endpoint revision count. Code Maat entity churn and percentage coupling retain their provider-specific meanings.

History quality reports shallow, insufficient, low-sample, short-span, bulk, exclusion, and rename limitations. Generated/vendor/build/cache paths and explicit patterns are filtered. No candidate is automatically classified as debt or defective. There is no implicit cache, default result path, generic provider/evidence framework, analyzer graph, or lexical semantic verifier.

Bundled processing is standard-library-only, local, offline, and read-only except for an explicitly requested output path. Code Maat is optional; installation or configuration always requires explicit permission and never happens in the helper.

Run `make test` and `make validate`. See [design](docs/design.md), [validation](docs/validation.md), and [v3-architecture](docs/v3-architecture.md). `SPEC-V3.md` is normative; `SPEC.md` is historical V2.
