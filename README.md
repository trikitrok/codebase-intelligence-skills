# Codebase Intelligence

Codebase Intelligence is a plugin containing nine independently invokable Codex Agent Skills for understanding, investigating, verifying, and planning changes to software repositories.

The suite uses deterministic tools to establish cheap facts and narrow the search space, then uses Codex for architecture, intent, behavior, and interpretation. Its central evidence rule is: **observations are not conclusions**.

## Quick reference

| Goal | Invocation |
|---|---|
| Become productive in an unfamiliar project | `$codebase-onboarding Orient me to this repository.` |
| Learn through a structured guide | `$codebase-tutorial Teach me how this repository works.` |
| Understand the system architecture | `$codebase-architecture Map this system's architecture.` |
| Follow one behavior | `$codebase-trace Trace POST /api/orders end to end.` |
| Understand one subsystem deeply | `$codebase-deep-dive Explain the billing subsystem.` |
| Plan a modification | `$codebase-change Plan adding idempotency to webhook processing.` |
| Find maintenance/debt candidates | `$codebase-hotspots Investigate maintenance hotspots.` |
| Explain hidden/change coupling | `$codebase-coupling Analyze coupling around billing.` |
| Audit documentation or claims | `$codebase-verify Audit docs/architecture.md against the source.` |

All skills are configured for explicit invocation. They do not silently switch into another expensive skill.

## Installation and discovery

This repository is a portable plugin package (`plugin.json`) with a supported Codex compatibility manifest (`.codex-plugin/plugin.json`). Current Codex/ChatGPT plugin installation uses a personal or repository marketplace. Point a marketplace entry named `codebase-intelligence` at this plugin directory, or copy the directory below the marketplace's plugin root, then restart the local client. See the current [OpenAI plugin packaging and local installation guide](https://developers.openai.com/plugins/build/plugins).

For a repository marketplace, place this package at `$REPO_ROOT/plugins/codebase-intelligence` and add this entry to `$REPO_ROOT/.agents/plugins/marketplace.json` (preserving any existing entries):

```json
{
  "name": "codebase-intelligence",
  "source": {"source": "local", "path": "./plugins/codebase-intelligence"},
  "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
  "category": "Developer Tools"
}
```

That object belongs in the marketplace's `plugins` array. Personal installation follows the same marketplace model at `~/.agents/plugins/marketplace.json`; use the official guide for the current personal plugin-root convention.

For development without plugin packaging, Codex also discovers standalone skills from `.agents/skills` at repository, parent, and user scopes. Copy or symlink individual folders from `skills/` there if only selected capabilities are wanted. The plugin form is preferred for the complete suite because current guidance recommends plugins for bundles of multiple reusable skills.

After installation, use `$codebase-onboarding`, `$codebase-coupling`, and the other names shown above. In Codex CLI or the IDE extension, typing `$` or using `/skills` exposes installed skills.

## Architecture

```text
explicitly invoked skill
        │
        ├── shared core + relevant strategy only
        │
        ├── source-first ───── targeted source/test inspection
        │
        ├── tool-first ─────── deterministic evidence → query/rank → source
        │
        └── evidence-first ─── claims → cheap checks → targeted source
                                  │
                                  ▼
                          concrete verification
                                  │
                                  ▼
                         evidence-backed report
```

Each skill has its own `SKILL.md` and explicit-only `agents/openai.yaml`. Shared, non-user-facing infrastructure lives under `shared/`:

- `references/core.md`: safety, evidence statuses, source references, tool permission, and output baseline.
- `references/source-first.md`: targeted semantic exploration.
- `references/tool-first.md`: provenance-aware evidence generation, filtering, and investigation.
- `references/evidence-contract.md`: schema v1, provider and cache semantics.
- `references/verification.md`: deterministic and semantic verification gates.
- `references/tool-providers.md`: capability-oriented language/ecosystem extension points.
- `scripts/codebase_intelligence.py`: standard-library deterministic CLI.

References are loaded progressively. Architecture does not load Code Maat details; tutorial does not load temporal-coupling mechanics; tool-first skills do not load tutorial-writing guidance.

## Analysis strategies

Source-first skills (`onboarding`, `tutorial`, `architecture`, `trace`, `deep-dive`, `change`) inspect manifests and boundaries, form a provisional map, and expand through verified callers, registrations, configuration, tests, and runtime relationships. Heavy history analysis is not a default.

Tool-first skills (`hotspots`, `coupling`) discover the repository and providers, validate or generate normalized evidence, query/rank a bounded candidate set, and only then inspect source. A metric is a lead, not a verdict.

Evidence-first verification extracts atomic claims, chooses the cheapest reliable check for each, and then inspects only the source required to classify the claim.

## Evidence statuses

- `VERIFIED`: directly supported by inspected evidence.
- `INFERRED`: strongly suggested but not directly demonstrated.
- `UNKNOWN`: insufficient evidence.
- `CONTRADICTED`: available evidence conflicts with the claim.

Material claims carry paths, symbols, tests, configuration, history/tool evidence, or an explicit limitation. The suite tells agents not to invent paths, symbols, edges, runtime behavior, or metrics.

## Deterministic helper

The helper depends only on Python's standard library and local Git. It never installs tools or changes the analyzed repository.

```bash
python3 shared/scripts/codebase_intelligence.py discover --repo /path/to/repo
python3 shared/scripts/codebase_intelligence.py repo-meta --repo /path/to/repo
python3 shared/scripts/codebase_intelligence.py analyze-history --repo /path/to/repo --output /tmp/evidence.json
python3 shared/scripts/codebase_intelligence.py validate --store /tmp/evidence.json
python3 shared/scripts/codebase_intelligence.py cache-status --repo /path/to/repo --store /tmp/evidence.json --provider git
python3 shared/scripts/codebase_intelligence.py query --store /tmp/evidence.json --type temporal_coupling --metric coupling --limit 12
```

Other commands calculate a default ephemeral store path, adapt Code Maat CSV for supported analyses, and verify repository-relative paths plus lexical symbol occurrences. Run `--help` for the complete interface.

### Git fallback observations

The built-in provider emits:

- change frequency as commits touching a file;
- added, deleted, and absolute line churn;
- distinct-author and primary-author contribution observations;
- temporal coupling as `shared_commits / min(left_revisions, right_revisions)`.

The fallback excludes changesets above a configurable cap from pair generation, disables rename detection, records binary revisions separately, and flags shallow or insufficient history. These choices and all analysis parameters are recorded in provenance.

### Code Maat

Code Maat is optional, never installed silently, and not required for a useful analysis. The adapter currently normalizes `revisions`, `entity-churn`, `authors`, and `coupling` CSV. It preserves Code Maat coupling as a percentage with provider-defined semantics instead of pretending it is equivalent to the Git fallback ratio. Code Maat requires a JVM or container and may have significant memory cost; its current project documentation should be checked before recommending installation.

Code Maat cache checks require its current discovered version, current CSV input, and analysis name. If the optional tool or version cannot be determined, its existing evidence is not reused; the Git fallback remains available.

## Evidence contract

Evidence v1 uses a deliberately small JSON envelope:

```json
{
  "schema_version": 1,
  "type": "change_frequency",
  "subject": {"type": "file", "path": "src/billing/invoice.ts"},
  "metrics": {"revisions": 83, "unit": "commits_touching_file"},
  "provenance": {
    "provider": "codebase-intelligence-git",
    "provider_version": "0.1.0",
    "analyzer_version": "0.1.0",
    "repository_id": "...",
    "repository_head": "...",
    "dirty": false,
    "working_tree_fingerprint": "...",
    "shallow": false,
    "input_scope": "committed_history",
    "parameters": {
      "since": null,
      "max_commits": null,
      "max_changeset_size": 30,
      "min_shared_commits": 2
    },
    "generated_at": "2026-09-16T00:00:00+00:00"
  }
}
```

Initial types are `change_frequency`, `churn`, `temporal_coupling`, and `ownership`; the schema recognizes `complexity`, `static_dependency`, and `test_coverage` for future adapters that preserve provider semantics. It does not encode judgments such as “bad architecture” or “should refactor.”

Stores are plain JSON, so providers and future investigation skills share an internal API without a database. The query command filters and ranks before observations enter model context.

## Cache and provenance

The evidence store is also the cache: there is no competing cache representation. By default the helper proposes a machine-local path under `/tmp/codebase-intelligence/<repository-id>/evidence-v1.json`; callers may choose another approved path.

Validity is based on inputs, not age:

- all stores require schema v1, the same repository identity and HEAD, provider/version, analyzer version, and parameters;
- `committed_history` evidence remains valid across dirty working-tree changes because those files were not inputs;
- working-tree analyses must also match dirty state and the content-sensitive working-tree fingerprint;
- provider-version, parameter, schema, repository, or relevant input changes invalidate reuse.

`cache-status` requires the intended provider. Its provider-specific request options construct the expected parameters and inputs, so the normal workflow cannot silently omit parameter checking or treat a cached provider version as the current version. File subjects are validated as normalized repository-relative identifiers, and observation provenance must exactly match store provenance.

Shallow history remains valid evidence about the available commits but carries a limitation; it is not silently treated as complete history.

## Ecosystem extensions and fallbacks

`discover` inventories source extensions, common manifests, and available commands. Skills first look for project-configured tooling. Capability-oriented candidates include dependency analyzers, complexity tools, coverage providers, and architecture-rule tools for Python, JS/TS, Java/Kotlin, Go, Rust, .NET, C/C++, Ruby, PHP, and Swift.

If an optional tool is missing, the skill explains the capability, value, dependencies, privacy characteristics, and fallback, then asks permission before installation. If declined, the suite falls back to Git, repository structure, `rg`/`grep`, manifests, project configuration, tests, and selective source inspection. Unsupported or unusual languages still receive this core workflow; unavailable metrics are reported as unavailable, never fabricated.

## Verification

Every skill performs a concrete final pass. Depending on the analysis, it checks:

- paths and symbols;
- calls, imports, registrations, routes, schemas, and configuration;
- trace transitions and failure paths;
- history provenance, parameters, metric definitions, and limitations;
- tests defining relevant behavior;
- every meaningful diagram node/edge;
- unsupported inferences and accidentally omitted major concepts.

The lexical reference checker is deliberately modest: it proves a symbol string occurs, not that a semantic call edge or runtime relationship exists.

## Privacy

All bundled analysis is local and offline. No source, history, metadata, or result is uploaded. Skills require explicit intent and permission before using a provider that transmits repository data. Evidence/cache output stays outside the target repository by default.

## Validation

Run:

```bash
make test
make validate
```

Tests create small temporary Git fixtures under `tests/` and remove them afterward. They cover history/churn/coupling/ownership normalization, filtering, Code Maat adaptation and malformed output, path/symbol checks, shallow and insufficient history, dirty-tree behavior, HEAD/provider/analyzer/parameter/schema invalidation, missing Git history, unusual languages, nested manifests, and available/absent tool discovery.

No external repository was cloned or used for testing. The semantic quality of the nine skills on real repositories remains a deliberate manual validation step.

## Limitations

- No general multi-language AST/call-graph engine is bundled. Static relationships use configured ecosystem tools or targeted source inspection.
- Complexity and coverage require existing/project-approved providers; their schema types are ready, but this release does not invent replacement metrics.
- The Git parser disables rename detection and is optimized for ordinary repository-relative paths; pathological filenames containing tabs/newlines may require a provider adapter.
- Author identity follows Git author names and can be distorted by aliases, bots, rebases, squashes, or incomplete history.
- Component aggregation remains semantic/manual unless repository boundaries or an explicit mapping support it.
- Real-world semantic quality and token behavior have not been evaluated outside this repository.

Research notes and the prior-art comparison are in [docs/research.md](docs/research.md). Design rationale is in [docs/design.md](docs/design.md), and the exact validation record is in [docs/validation.md](docs/validation.md).
