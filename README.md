# Codebase Intelligence

Codebase Intelligence is a local/private plugin of nine explicitly invoked Codex Agent Skills for repository understanding, investigation, verification, and change planning. Codex performs semantic inspection; the bundled helper only bounds historical hotspot and temporal-coupling candidates.

| Goal | Invocation |
|---|---|
| Orient | `$codebase-onboarding Orient me to this repository.` |
| Learn | `$codebase-conversational-tutorial Teach me how this repository works.` |
| Architecture | `$codebase-architecture Map this system.` |
| Trace | `$codebase-trace Trace POST /api/orders.` |
| Deep dive | `$codebase-deep-dive Explain the billing subsystem.` |
| Plan | `$codebase-change Plan adding idempotency.` |
| Hotspots | `$codebase-hotspots Investigate maintenance hotspots.` |
| Coupling | `$codebase-coupling Analyze coupling around billing.` |
| Verify | `$codebase-verify Audit docs/architecture.md.` |

## Choose a skill

- New to the repository → `codebase-onboarding`
- Learn the whole system progressively → `codebase-conversational-tutorial`
- Map the system’s structure → `codebase-architecture`
- Follow one execution path → `codebase-trace`
- Understand one subsystem deeply → `codebase-deep-dive`
- Plan a code change → `codebase-change`
- Investigate maintenance hotspots → `codebase-hotspots`
- Investigate change coupling and hidden dependencies → `codebase-coupling`
- Check claims or documentation against the code → `codebase-verify`

## Human-facing guides

- [Codebase Onboarding](docs/codebase-onboarding.md) — what it does and how to orient yourself in a repository
- [Codebase Conversational Tutorial](docs/codebase-conversational-tutorial.md) — what it does and how to learn a repository progressively
- [Codebase Architecture](docs/codebase-architecture.md) — what it does and how to map system structure
- [Codebase Trace](docs/codebase-trace.md) — what it does and how to follow one execution path
- [Codebase Deep Dive](docs/codebase-deep-dive.md) — what it does and how to understand one subsystem deeply
- [Codebase Change](docs/codebase-change.md) — what it does and how to plan a repository change
- [Codebase Hotspots](docs/codebase-hotspots.md) — what it does and how to investigate history-based maintenance candidates
- [Codebase Coupling](docs/codebase-coupling.md) — what it does and how to investigate visible and hidden relationships
- [Codebase Verify](docs/codebase-verify.md) — what it does and how to audit technical claims against the code

All skills are explicitly invoked. Analysis is source-grounded, local, and read-only by default. History-based skills can use optional Code Maat or the built-in Git fallback; see the relevant human-facing guides for details.

Run `make test` and `make validate`. See [design](docs/design.md), [validation](docs/validation.md), and [v3-architecture](docs/v3-architecture.md). `SPEC-V3.md` is normative; `SPEC.md` is historical V2.

Licensed under the [MIT License](LICENSE).
