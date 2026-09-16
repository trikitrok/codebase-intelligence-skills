# Codebase Intelligence V3 — Implementation Specification

## 1. Status and purpose

This document is the normative implementation specification for Codebase Intelligence V3.

The accepted architecture is defined in `docs/v3-architecture.md`. This specification translates that architecture into implementation requirements. It does not reopen the architectural decisions recorded there.

V3 is a collection of nine explicitly invoked Codex Agent Skills. Codex performs semantic repository understanding. A single narrow deterministic helper performs only the historical preprocessing that materially improves hotspot and temporal-coupling analysis.

The implementation must optimize for:

1. useful semantic understanding;
2. bounded and reproducible historical candidate discovery;
3. selective source inspection;
4. token economy;
5. honest uncertainty;
6. local/private analysis by default;
7. predictable explicit invocation;
8. minimal implementation and maintenance surface.

### 1.1 Normative language

The terms **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, and **MAY** are normative.

- **MUST** and **MUST NOT** define acceptance requirements.
- **SHOULD** and **SHOULD NOT** define strong defaults that may be departed from only for a documented concrete reason.
- **MAY** identifies intentional implementation flexibility.

### 1.2 Product invariant

The V3 product invariant is:

```text
repository
    ↓
cheap deterministic analysis where it materially helps
    ↓
small relevant evidence/candidate set
    ↓
selective Codex source inspection
    ↓
semantic reasoning
    ↓
verification
    ↓
evidence-backed output
```

Deterministic observations are candidate signals, not semantic conclusions.

## 2. Fixed architecture

V3 MUST contain:

- nine explicit Agent Skills;
- one concise shared analysis contract;
- one history-analysis reference used only by hotspots and coupling;
- one deterministic history helper used only for hotspot and temporal-coupling candidate generation;
- structural validation and focused deterministic tests.

V3 MUST NOT introduce:

- an implicit persistent cache;
- a generic provider registry or plugin framework;
- a generic ecosystem/tool-discovery framework;
- a generic tool-recommendation framework;
- a generic Evidence v1 observation ontology;
- speculative evidence types;
- a lexical verification helper;
- an architecture graph generator;
- a call-graph generator;
- a subsystem, concept, or impact analyzer;
- automatic technical-debt or architectural-quality classification.

The nine public skill names and their explicit invocation behavior are stable public product contracts.

## 3. Required repository layout

The final V3 repository MUST have this relevant structure:

```text
.
├── plugin.json
├── .codex-plugin/
│   └── plugin.json
├── README.md
├── SPEC.md
├── SPEC-V3.md
├── docs/
│   ├── design.md
│   ├── research.md
│   ├── runtime-audit.md
│   ├── v3-architecture.md
│   └── validation.md
├── skills/
│   ├── codebase-onboarding/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── codebase-tutorial/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── codebase-architecture/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── codebase-trace/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── codebase-deep-dive/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── codebase-change/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── codebase-hotspots/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   ├── codebase-coupling/
│   │   ├── SKILL.md
│   │   └── agents/openai.yaml
│   └── codebase-verify/
│       ├── SKILL.md
│       └── agents/openai.yaml
├── shared/
│   ├── references/
│   │   ├── analysis-basics.md
│   │   └── history-analysis.md
│   └── scripts/
│       └── history_candidates.py
├── scripts/
│   └── validate_suite.py
└── tests/
    ├── test_history_candidates.py
    └── test_suite_structure.py
```

Equivalent splitting of the two test files MAY be used when it improves readability. The production/helper and shared-reference structure MUST remain as shown.

The final V3 tree MUST NOT retain obsolete V2 shared references or the V2 helper after the Contract migration gate has passed.

Every `agents/openai.yaml` MUST contain:

```yaml
policy:
  allow_implicit_invocation: false
```

The portable and compatibility plugin manifests MUST continue to expose the same plugin and nine skills.

## 4. Runtime responsibility model

V3 uses four kinds of runtime work:

### 4.1 Codex semantic reasoning

Codex is responsible for:

- selecting meaningful source and tests;
- understanding architecture, behavior, intent, boundaries, and domain concepts;
- interpreting historical candidates;
- distinguishing healthy change from maintenance risk;
- investigating static, logical/domain, and test coupling;
- extracting and classifying claims;
- planning changes;
- constructing explanations and diagrams;
- semantic verification.

### 4.2 Deterministic built-in/local operations

Codex may use local primitives such as:

- `rg` and `rg --files`;
- filesystem inspection;
- Git commands;
- manifests and configuration;
- `shared/scripts/history_candidates.py`.

These operations establish cheap facts or bound candidate sets. They MUST NOT be presented as semantic proof beyond what they actually establish.

### 4.3 Optional external tool

Code Maat is the only externally named analysis tool in the V3 architecture. It is preferred for behavioral hotspot and temporal-coupling analysis when it is concretely available and appropriate.

No other external analyzer is part of the V3 product architecture.

### 4.4 Repository-native operations

Codex MAY run a command already configured by the target repository when it answers a concrete evidence gap, for example a focused test, type check, schema validator, build-description command, or configured dependency rule.

Repository-native operations MUST NOT be run merely because an ecosystem commonly has such a tool.

## 5. Shared references

### 5.1 `shared/references/analysis-basics.md`

This is the only shared reference loaded by all nine skills.

It MUST be concise and self-contained. It MUST NOT require another shared reference to supply generally applicable behavior.

It MUST contain the following rules:

1. Resolve the repository root and read applicable repository instructions before analysis.
2. Treat the target repository as read-only unless the user explicitly requests implementation.
3. `codebase-change` is planning-only by default.
4. Prefer targeted `rg`, manifests, configuration, tests, Git, and repository-native commands.
5. Do not assume a programming language or framework.
6. Clarify scope only when choosing incorrectly would materially invalidate the result; otherwise state a narrow assumption and proceed.
7. Use selective source inspection rather than broad source ingestion.
8. Use these statuses when they clarify material uncertainty:
   - `VERIFIED`;
   - `INFERRED`;
   - `UNKNOWN`;
   - `CONTRADICTED`.
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

The file MUST NOT contain:

- Code Maat invocation details;
- evidence-store or cache procedures;
- a generic ecosystem tool catalogue;
- tutorial-only pedagogy;
- repeated per-skill output templates.

### 5.2 `shared/references/history-analysis.md`

Only `codebase-hotspots` and `codebase-coupling` MUST load this reference during ordinary invocation.

It MUST contain:

1. The concrete helper path relative to either skill.
2. The `hotspots` and `temporal-coupling` command forms.
3. Provider selection:
   - Code Maat when concretely available;
   - Git fallback otherwise.
4. The meaning of bounded candidates.
5. History-quality fields and limitation codes.
6. Bulk, rename, shallow-history, low-sample, generated/vendor, construction/import, bot, formatting, and migration confounders.
7. Git hotspot metric definitions.
8. Git temporal-coupling metric definitions.
9. The requirement to preserve Code Maat metric semantics.
10. The rule that candidates require selective source/test inspection.
11. External-tool permission and local/private processing rules.

It MUST NOT contain:

- generic provider abstractions;
- unrelated ecosystem tools;
- cache instructions;
- generic evidence types;
- semantic technical-debt or architectural classifications.

### 5.3 Loading rules

- Every skill MUST directly link to and read `analysis-basics.md`.
- `codebase-hotspots` and `codebase-coupling` MUST additionally link to and read `history-analysis.md`.
- No other skill loads `history-analysis.md` by default.
- Tutorial-specific guidance MUST be contained in `skills/codebase-tutorial/SKILL.md`.
- Verification-specific claim-audit behavior MUST be contained in `skills/codebase-verify/SKILL.md`.
- Shared references MUST NOT link in a way that creates indirect loading of irrelevant workflows.

## 6. Skill contracts

Each skill MUST contain a focused description, input/scope expectations, runtime steps, stopping criteria, deliverable requirements, and boundaries. Each skill MUST remain independently understandable after loading `analysis-basics.md` and, where applicable, `history-analysis.md`.

### 6.1 `codebase-onboarding`

#### Purpose

Orient a competent developer to an unfamiliar repository quickly without producing a directory inventory or a full architecture audit.

#### Runtime flow

1. Resolve the root and applicable instructions.
2. Inspect top-level structure, manifests, configuration, entry points, tests, and documented development commands.
3. Infer the project purpose and provisional runtime/repository boundaries.
4. Selectively inspect source to identify central abstractions, state, integrations, configuration, extension points, and common change locations.
5. Trace one or two representative flows.
6. Inspect repository-native run/test/build/lint configuration; run a safe command only when it materially confirms the workflow.
7. Choose a shallow-to-medium source reading order.
8. Reconcile material source/documentation disagreement.
9. Verify cited paths, symbols, and representative relationships.

#### Stopping criteria

Stop when the answer can explain:

- what the project does;
- its meaningful boundaries;
- its primary entry points;
- one or two representative flows;
- state, integrations, and configuration;
- how developers run and test it;
- where to read next and where common changes belong.

Do not expand into exhaustive architecture, a full tutorial, or a deep subsystem analysis.

#### Required output

- concise purpose and mental model;
- small repository/system map;
- entry points and representative flows;
- state, integrations, configuration, tests, and development workflow;
- extension/change locations;
- prioritized reading order;
- contradictions and limitations.

### 6.2 `codebase-tutorial`

#### Purpose

Teach the repository progressively through its core concepts rather than through its directory tree.

#### Runtime flow

1. Use the requested audience, focus, and format; otherwise assume a competent developer and chat output.
2. Perform cheap repository reconnaissance.
3. Curate a small set of genuine core concepts. Five to ten is guidance, not a quota.
4. Map every selected concept to verified source, symbols, configuration, or tests.
5. Establish primary concept relationships.
6. Order concepts pedagogically: purpose before implementation and foundations before dependants.
7. Explain each concept using a few relevant excerpts or references, failure/edge behavior where useful, and suggested reading.
8. Use analogies only where they materially improve understanding.
9. Use diagrams only where relationships benefit from them.
10. Verify paths, symbols, excerpts, internal links, and diagram edges.

#### Stopping criteria

Stop when:

- the selected concepts explain the repository’s distinctive core mechanism;
- each concept has verified source evidence;
- dependencies between chapters are understandable;
- major concepts relevant to the requested scope are not omitted;
- additional concepts would mostly add framework scaffolding or unrelated detail.

Do not invent concepts to reach a count and do not persist artifacts unless the user requests files or the run is unusually large and resumability is justified.

#### Required output

- progressive tutorial;
- overview diagram when useful;
- verified source references;
- reading order;
- explicit limitations.

### 6.3 `codebase-architecture`

#### Purpose

Build an evidence-backed model of meaningful system boundaries and runtime shape.

#### Runtime flow

1. Inspect manifests, deployable/runtime units, entry points, configuration, registrations, persistence, and tests.
2. Infer components from responsibilities and runtime/build boundaries, not arbitrary directory depth.
3. Identify actors, communication mechanisms, state ownership, external integrations, cross-cutting behavior, dependency direction, and extension points.
4. Trace a small number of representative cross-boundary flows.
5. Use an already configured repository-native dependency or architecture command only for a concrete unresolved relationship.
6. Distinguish static imports from meaningful architectural relationships.
7. Verify every material diagram node and edge.

#### Stopping criteria

Stop when the answer covers:

- system context;
- meaningful components and responsibilities;
- communication and state;
- external integrations;
- representative flows;
- public/internal boundaries and extension points;
- important uncertainty or documentation disagreement.

Do not expand into a complete dependency graph or trace every behavior.

#### Required output

- system context;
- component and responsibility model;
- communication/state model;
- representative flows;
- boundary and extension-point guidance;
- evidence-backed diagrams where useful;
- contradictions and limitations.

### 6.4 `codebase-trace`

#### Purpose

Trace one named behavior from concrete trigger to result.

#### Runtime flow

1. Resolve the requested behavior. Ask one concise question only if several materially different behaviors match.
2. Locate the concrete route, command, event, job, UI action, public API, or defining test.
3. Follow registration and dispatch into business logic.
4. Track transformations, decisions, dependencies, state reads/writes, external calls, side effects, and result.
5. Inspect error, retry, transaction, concurrency, and authorization paths when they affect the requested behavior.
6. Use tests and configuration to confirm transitions.
7. Record each important hop as `from symbol → mechanism → to symbol`.
8. Verify each important transition and every sequence-diagram message.

#### Stopping criteria

Stop at the observable result or terminal side effect after covering all branches that materially change the requested behavior. Do not broaden into unrelated subsystem internals or whole-system architecture.

#### Required output

- concise end-to-end trace;
- sequence diagram when useful;
- annotated important steps with paths/symbols;
- relevant alternate/error paths;
- `INFERRED` or `UNKNOWN` labels for unresolved runtime-dependent transitions.

### 6.5 `codebase-deep-dive`

#### Purpose

Explain one already-focused subsystem or concept in depth.

#### Runtime flow

1. Define the subject boundary and adjacent context.
2. Locate its responsibility, public API, construction, configuration, callers, dependencies, state, and tests.
3. Inspect internal model, lifecycle, invariants, state transitions, downstream effects, failure handling, transactions, retries, concurrency, and extension points as applicable.
4. Expand outward only through verified collaborators.
5. Run a focused repository-native test or diagnostic only when behavior remains materially ambiguous.
6. Verify the public boundary, key callers, state transitions, and diagrams.

#### Stopping criteria

Stop when the subject’s public boundary, internals, lifecycle, state, important collaborators, failure behavior, tests, and extension seams are understood. Do not continue into unrelated adjacent areas.

#### Required output

- focused mental model;
- boundary map;
- lifecycle/flow;
- implementation walkthrough;
- failure and concurrency behavior where relevant;
- test model;
- extension guidance;
- evidence and limitations.

### 6.6 `codebase-change`

#### Purpose

Plan how a requested change should be implemented against the current repository. It is planning-only unless the user explicitly requests implementation.

#### Runtime flow

1. Restate the desired behavior and known compatibility constraints.
2. Ask only when a missing product decision would materially change the plan.
3. Trace current behavior and identify the responsible boundary and extension points.
4. Locate affected APIs, schemas, persistence, configuration, events/jobs, clients, tests, generated boundaries, and operations.
5. Search definitions, callers, registrations, fixtures, and contracts for direct impact evidence.
6. Use repository-native test discovery, type checking, schema validation, or build commands only when they resolve a concrete impact question.
7. Separate verified impact from likely/inferred impact.
8. Consider compatibility, rollout, data migration/backfill, failure modes, side effects, observability, and rollback where applicable.
9. Produce the smallest coherent implementation sequence consistent with repository conventions.

#### Stopping criteria

Stop when the plan identifies current behavior, the proposed extension point, verified and likely impacts, contract/data implications, tests, migration/rollout concerns, risks, and unresolved product decisions. Do not claim impact completeness and do not edit code without explicit authorization.

#### Required output

- current behavior;
- proposed approach;
- affected files/symbols grouped by responsibility;
- verified versus inferred impact;
- contract/data/operational implications;
- ordered implementation and test plan;
- risks and open decisions.

### 6.7 `codebase-hotspots`

#### Purpose

Use behavioral history to discover a small candidate set and then inspect source to determine whether candidates indicate debt, expected change, or insufficient evidence.

#### Runtime flow

1. Resolve repository instructions and history scope.
2. Read `history-analysis.md`.
3. Run `history_candidates.py hotspots` with provider `auto` unless the user requests a concrete provider.
4. Prefer Code Maat when concretely available; otherwise use Git + current physical LOC.
5. Review history-quality metadata before interpreting candidates.
6. If history is insufficient, state that clearly. Do not invent a ranking or silently replace behavioral hotspots with a different analysis.
7. Inspect a bounded subset of returned candidates, their history, source, boundaries, callers, and tests.
8. Investigate responsibility, control flow, duplication, change surface, boundary leakage, test fragility, repeated fixes, compatibility burden, and healthy expected change.
9. Run repository-native tests or coverage only for a concrete candidate question.
10. Classify each reported candidate semantically.
11. Verify metric definitions, parameters, provider, limitations, paths, and source claims.

#### Stopping criteria

Stop after:

- the bounded candidate set has been reviewed;
- the significant candidates selected for reporting have been semantically classified;
- obvious history confounders have been addressed;
- further inspection would amount to an independent deep dive or coupling analysis.

The skill MUST NOT inspect every returned candidate when fewer candidates answer the question. It MUST NOT exceed the helper’s bounded output by reconstructing an unbounded list.

#### Required output

Separate findings into:

- strong technical-debt evidence;
- maintenance hotspots worth investigating;
- high-change areas that appear healthy;
- insufficient-evidence candidates.

For each significant candidate include provider-defined history observations, relevant source/test evidence, interpretation, status, implication, and uncertainty.

### 6.8 `codebase-coupling`

#### Purpose

Explain temporal/evolutionary, static, logical/domain, and test coupling without building analyzers for conceptual symmetry.

#### Runtime flow

1. Resolve the requested scope. Keep a named subject anchored; for a broad request identify only a small number of meaningful boundaries.
2. Read `history-analysis.md`.
3. Run `history_candidates.py temporal-coupling`, using `--subject` for a named file when appropriate.
4. Prefer Code Maat when concretely available; otherwise use Git co-change analysis.
5. Review history-quality metadata and limitations.
6. If temporal history is insufficient, report that. Continue with targeted static/logical/test inspection only when the user’s request remains answerable from source.
7. Select a bounded set of temporal pairs or a bounded source-defined scope.
8. Inspect imports, calls, interfaces, shared models/state/configuration, messages, schemas, duplicated knowledge, fixtures, mocks, and coordinated production/test behavior.
9. Use an already configured repository-native dependency analyzer only for a concrete unresolved static relationship.
10. Compare temporal evidence with visible static, domain, and test relationships.
11. Classify reported relationships as `expected`, `potentially hidden`, or `unclear`.
12. Verify every reported relationship and matrix/diagram edge.

#### Stopping criteria

Stop when the bounded selected relationships have been explained across the relevant coupling types and further work would require a separate subsystem deep dive. Do not attempt an exhaustive repository-wide coupling graph.

#### Required output

For every significant relationship report:

- endpoints;
- applicable coupling types: `S`, `T`, `L`, `X`;
- provider-defined temporal evidence where present;
- source/test evidence;
- likely explanation;
- architectural status;
- evidence status;
- maintenance implication and uncertainty.

A compact matrix MAY be used when it improves comparison. Every non-empty cell requires evidence.

### 6.9 `codebase-verify`

#### Purpose

Audit an existing technical artifact or set of claims against the current repository without silently rewriting it.

#### Runtime flow

1. Obtain the artifact and repository scope.
2. Extract atomic material claims and meaningful diagram nodes/edges. Ignore stylistic prose.
3. Classify each claim as existence, symbol/API, static relationship, runtime flow, architectural boundary/independence, metric/history, or intent.
4. Apply the cheapest reliable check first: filesystem, `rg`, Git, or a bounded history-helper rerun when a historical metric requires it.
5. Inspect definitions, callers, configuration, tests, and reachability for semantic claims.
6. Use a repository-native build/test/type/schema command only when a concrete claim requires it.
7. Investigate conflicting evidence rather than silently choosing one source.
8. Classify each claim as `VERIFIED`, `INFERRED`, `UNKNOWN`, or `CONTRADICTED`.
9. Verify diagram nodes and meaningful edges separately.

The skill MUST NOT use or recreate a lexical verification helper. Batching ordinary `rg` or filesystem checks is allowed.

#### Stopping criteria

Stop when every material claim in scope is classified or explicitly grouped with equivalent low-risk claims, all high-impact contradictions are explained, and blind spots are stated.

#### Required output

- audit summary;
- highest-impact discrepancies;
- compact claim/status/evidence/corrective-note table;
- invalid diagram nodes/edges where present;
- scope and blind spots.

## 7. Deterministic helper boundary

### 7.1 Location and dependencies

The helper MUST be implemented at:

```text
shared/scripts/history_candidates.py
```

The built-in Git paths MUST use only the Python standard library and local Git.

Code Maat is optional and external. The helper MUST NOT download, install, or configure it.

### 7.2 Responsibilities

The helper MUST:

- resolve a Git repository root;
- inspect repository HEAD, dirty state, and shallow state;
- parse bounded Git history;
- detect and resolve renames where unambiguous;
- filter generated/vendor/build/cache paths;
- exclude bulk commits;
- calculate history-quality metadata;
- count current tracked physical LOC for Git hotspots;
- calculate Git hotspot candidates;
- calculate Git temporal-coupling candidates;
- run or import the two concrete Code Maat analyses;
- validate normalized paths and provider fields;
- rank, sort, and limit candidates before JSON reaches Codex;
- emit one of the two schemas in Section 12.

The helper MUST NOT:

- inspect source semantics;
- classify technical debt;
- classify architectural quality;
- compute static, logical/domain, or test coupling;
- discover ecosystems or generic tools;
- recommend tools;
- manage providers through a registry;
- persist an implicit cache;
- create generic observations;
- verify arbitrary source references;
- generate reports or diagrams.

### 7.3 Stable interface boundary

The stable machine interface is:

- the CLI defined in Section 8;
- the JSON result schemas defined in Section 12;
- exit behavior defined in Section 14.

Internal Python functions, classes, and modules are implementation details and MUST NOT be documented as a public provider SDK.

## 8. `history_candidates.py` CLI contract

### 8.1 Commands

The helper MUST expose exactly two product commands:

```text
python3 shared/scripts/history_candidates.py hotspots [options]
python3 shared/scripts/history_candidates.py temporal-coupling [options]
```

Standard `--help` and `--version` behavior is allowed and does not count as an analysis command.

### 8.2 Common options

Both commands MUST support:

| Option | Default | Contract |
|---|---:|---|
| `--repo PATH` | `.` | Resolve through `git rev-parse --show-toplevel`. |
| `--provider {auto,git,code-maat}` | `auto` | Select the concrete history path. |
| `--limit N` | `20` | Integer from 1 through 100; bounds returned candidates. |
| `--since VALUE` | unset | Passed to Git as the history lower bound. |
| `--max-commits N` | unset | Positive integer limiting matched commits. |
| `--max-changeset-size N` | `30` | Positive integer; commits with more relevant paths are excluded. |
| `--rename-threshold N` | `50` | Git rename-similarity percentage from 1 through 100. |
| `--exclude PATTERN` | repeatable | Additional case-sensitive POSIX-style full-path glob. |
| `--low-sample-commits N` | `20` | Positive integer controlling a non-fatal warning. |
| `--low-sample-days N` | `30` | Non-negative integer controlling a non-fatal short-span warning. |
| `--output PATH` | unset | Also write the emitted JSON to this explicit path. No default path exists. |
| `--code-maat-command JSON` | unset | JSON array forming a concrete executable/JAR command prefix. |
| `--code-maat-version VALUE` | unset | Explicit provider version when it cannot be discovered reliably. |

`--code-maat-command` MUST be parsed as a JSON array of non-empty strings and executed without a shell. Examples:

```text
--code-maat-command '["code-maat"]'
--code-maat-command '["java", "-jar", "/opt/code-maat.jar"]'
```

The helper MUST reject shell strings and MUST NOT execute the value through `sh -c`, `bash -c`, or an equivalent shell.

If `--output` is supplied, the helper MUST write the same complete JSON result that it writes to standard output. The write SHOULD be atomic. No result is persisted unless `--output` is explicitly supplied.

### 8.3 Hotspot-only options

`hotspots` MUST support:

| Option | Contract |
|---|---|
| `--code-maat-revisions-csv PATH` | Native revisions CSV input. |
| `--code-maat-churn-csv PATH` | Native entity-churn CSV input. |

Both CSV options MUST be supplied together. Supplying only one is an argument error.

### 8.4 Temporal-coupling-only options

`temporal-coupling` MUST support:

| Option | Default | Contract |
|---|---:|---|
| `--min-shared-commits N` | `2` | Positive Git fallback threshold. |
| `--subject PATH` | repeatable | Return only pairs containing at least one exact normalized subject path. |
| `--include-deleted` | false | Permit deleted historical entities in results. |
| `--code-maat-coupling-csv PATH` | unset | Native coupling CSV input. |

Subjects MUST be repository-relative paths. A subject outside the repository or containing traversal is an argument error.

### 8.5 Provider selection

For `--provider auto`, provider selection MUST occur in this order:

1. Valid analysis-specific Code Maat CSV options explicitly supplied by the caller.
2. A valid explicit `--code-maat-command`.
3. An exact `code-maat` executable on `PATH`.
4. Git fallback.

The helper MUST NOT probe unrelated executables, jars, containers, package managers, or ecosystem tools.

For `--provider git`:

- the Git path MUST be used;
- Code Maat-specific options MUST be rejected as conflicting input.

For `--provider code-maat`:

- valid CSV input, an explicit command, or an exact `code-maat` executable on `PATH` is required;
- absence or failure is an error, not a silent Git fallback.

### 8.6 Output and ordering

- Successful commands MUST emit exactly one JSON object to standard output.
- Diagnostic logging MUST go to standard error and MUST NOT corrupt JSON stdout.
- JSON object member order is not significant.
- Candidate array order is significant and MUST follow Sections 10 and 11.
- The helper MUST calculate ranks and totals before applying `--limit`.

## 9. Common Git history model

### 9.1 Repository state

The helper MUST determine:

- canonical repository root;
- current `HEAD`;
- dirty state including tracked and untracked changes;
- shallow-repository state;
- Git version;
- matched commit count and date span.

An empty Git repository has no analyzable history and MUST produce the structured operational error defined in Section 14.

### 9.2 Tracked current paths

For ordinary hotspot analysis and default coupling analysis, current entities are the paths returned by `git ls-files` after filtering.

The helper MUST:

- normalize separators to `/` in output;
- reject absolute paths, NULs, `.` subjects, and `..` traversal;
- avoid following a tracked symlink outside the repository when reading LOC;
- skip binary files for LOC;
- include tests unless excluded by ordinary generated/vendor rules or explicit patterns.

Untracked files MUST NOT receive history metrics or LOC candidates.

### 9.3 Default path filtering

Paths containing any of these case-insensitive complete path components MUST be excluded by default:

```text
.cache
.venv
__pycache__
build
cache
coverage
dist
generated
node_modules
target
vendor
venv
```

Files ending case-insensitively in these suffixes MUST also be excluded:

```text
.min.js
.map
```

The implementation MAY add a very small number of equally obvious generated/build artifacts only when tests and documentation identify the addition. It MUST NOT evolve into an ecosystem detector.

Every `--exclude` pattern is applied case-sensitively to the normalized full repository-relative path using documented POSIX-style glob semantics.

The result MUST record the effective default exclusions, explicit patterns, and excluded path count.

### 9.4 Rename handling

Git history MUST be read with rename detection enabled using the configured similarity threshold.

The implementation MUST process enough name-status information to build rename chains from historical names to current canonical paths. For a chain such as `A → B → C`, touches to `A` and `B` MUST contribute to current path `C` when the chain is unambiguous.

Requirements:

- a rename commit counts as one touch of the canonical entity, not two;
- ambiguous rename/copy relationships MUST NOT be guessed;
- current-path mappings MUST be preferred;
- deleted entities are excluded by default;
- `temporal-coupling --include-deleted` MAY retain an unresolved deleted entity under its normalized historical path;
- unresolved rename/deletion counts MUST be reported;
- unresolved history MUST produce a limitation when it can materially affect results.

The implementation MAY choose the exact internal parsing strategy. It SHOULD use NUL-delimited Git output so spaces and tabs do not corrupt parsing.

### 9.5 Commit touch sets

For each matched commit, the helper MUST construct a unique set of relevant canonical paths after:

1. path normalization;
2. rename mapping;
3. default path filtering;
4. explicit exclusions;
5. current/deleted entity policy.

Multiple changes to the same canonical path in one commit count as one touch.

### 9.6 Bulk commits

A commit is a bulk commit when its relevant canonical touch set contains more paths than `--max-changeset-size`.

Bulk commits MUST be excluded from:

- hotspot revision counts;
- hotspot Code Maat executable input;
- endpoint revision counts used by Git temporal coupling;
- Git temporal co-change pair generation;
- Code Maat executable coupling input.

Bulk commits MUST remain visible in history-quality metadata.

The result MUST report:

- number of bulk commits excluded;
- number of relevant file touches excluded;
- ratio of excluded commits to matched commits;
- ratio of excluded relevant touches to all relevant touches.

If either ratio is at least `0.5`, the result MUST include `HIGH_BULK_EXCLUSION`.

The helper MUST NOT infer from commit messages that a commit is construction, formatting, migration, generated, or a defect fix. Codex investigates those meanings selectively.

### 9.7 Physical LOC

The Git hotspot fallback MUST count physical lines in current tracked text files after filtering.

Definition:

- read bytes without decoding;
- skip files containing NUL bytes;
- count records returned by byte-oriented `splitlines()`;
- blank lines count;
- a final newline does not create an additional line;
- empty files have zero LOC;
- symlinks that resolve outside the repository are skipped.

LOC is a pragmatic current size proxy. The helper and skills MUST NOT call it cyclomatic or cognitive complexity.

## 10. Hotspot algorithm

### 10.1 Git fallback observations

For every eligible current tracked text file:

- `revisions` is the number of eligible non-bulk commits whose canonical touch set contains the file;
- `size` is current physical LOC as defined in Section 9.7.

Files with zero eligible revisions MUST NOT become candidates. Files may have zero LOC.

### 10.2 Code Maat observations

For Code Maat hotspots:

- `revisions` is the provider-defined revisions value;
- `size` is provider-defined absolute entity churn, calculated from `added + deleted`;
- the unit and definition MUST remain explicitly Code Maat-specific;
- Code Maat churn MUST NOT be described as LOC or as equivalent to the Git size proxy.

Every retained entity MUST have both a revisions row and an entity-churn row. Missing or duplicate required entities are malformed provider input.

### 10.3 Tie-correct ranking

Ranking is performed across the entire eligible candidate set before limiting.

For each axis independently:

1. Collect the distinct values and sort them ascending.
2. Assign each distinct value a one-based ascending dense position.
3. Normalize as:

```text
normalized_rank = dense_position / number_of_distinct_values
```

Therefore:

- the maximum value has rank `1.0`;
- equal values receive equal ranks;
- the minimum value has rank `1 / distinct_value_count` rather than zero;
- if all values are equal, every value has rank `1.0`.

For every candidate:

```text
score = revision_rank * size_rank
```

This score ranks candidates only. It is not a technical-debt score.

### 10.4 Candidate ordering

Hotspot candidates MUST be sorted by:

1. score descending;
2. revisions descending;
3. size descending;
4. path ascending.

Only the first `--limit` candidates are emitted.

## 11. Temporal-coupling algorithm

### 11.1 Git fallback observations

For each eligible non-bulk commit:

1. Increment the revision count of every path in its canonical touch set.
2. Generate every unordered pair of distinct paths in that set.
3. Increment the shared-commit count for each pair once.

Pairs with fewer than `--min-shared-commits` are removed.

For each retained pair:

```text
coupling = shared_commits / min(left_revisions, right_revisions)
```

Git coupling requirements:

- range: `0.0` through `1.0` inclusive;
- unit: `ratio`;
- `left_revisions` and `right_revisions` use the same eligible non-bulk commit population as `shared_commits`;
- paths are stored lexicographically in the pair for deterministic identity;
- test paths remain eligible;
- a `--subject` filter retains a pair when either endpoint exactly matches any supplied subject.

### 11.2 Git candidate ordering

Git temporal candidates MUST be sorted by:

1. `shared_commits` descending;
2. `coupling` descending;
3. left path ascending;
4. right path ascending.

This deliberately prioritizes support over a perfect ratio based on very few commits.

### 11.3 Code Maat observations

For Code Maat coupling:

- `coupling` is the provider-defined `degree`;
- range is `0` through `100` inclusive;
- unit is `percent`;
- it MUST NOT be divided by 100 or presented as equivalent to Git coupling;
- provider-supplied `shared-revisions`, endpoint revisions, and average revisions MUST be preserved when available;
- missing optional support fields MUST be represented as `null` in the bounded result.

Code Maat candidates with provider-supplied shared support MUST be ordered by:

1. shared revisions descending;
2. coupling descending;
3. paths ascending.

If shared support is absent, order by:

1. coupling descending;
2. paths ascending.

The result MUST state which ordering was used.

`--min-shared-commits` applies only when shared support is available. If imported Code Maat output lacks shared support, the helper MUST NOT pretend that threshold was applied and MUST emit `CODE_MAAT_SUPPORT_FILTER_UNAVAILABLE`.

## 12. Bounded result schemas

### 12.1 General rules

The V3 bounded history schema is not Evidence v1 and MUST NOT be described as a generic evidence store.

Both result kinds MUST contain:

```json
{
  "schema_version": 1,
  "result_kind": "codebase-intelligence-history-candidates",
  "analysis": "hotspots or temporal_coupling",
  "provenance": {},
  "history_quality": {},
  "metric_definitions": {},
  "total_candidates": 0,
  "candidate_count": 0,
  "truncated": false,
  "candidates": []
}
```

Requirements:

- `candidate_count` equals the length of `candidates`.
- `candidate_count` never exceeds the requested limit.
- `total_candidates` is the eligible count before the limit.
- `truncated` is true exactly when `total_candidates > candidate_count`.
- provenance appears only at result level.
- candidates MUST NOT repeat provenance.
- semantic conclusions MUST NOT appear in the result.

### 12.2 Provenance object

`provenance` MUST contain:

```json
{
  "provider": {
    "name": "git or code-maat",
    "version": "non-empty version string",
    "mode": "built-in, executable, or csv"
  },
  "repository_head": "Git object id",
  "working_tree_dirty": false,
  "input_scope": "committed_history or committed_history+working_tree",
  "parameters": {},
  "generated_at": "RFC 3339 UTC timestamp"
}
```

Provider values:

- Git fallback: `name=git`, `mode=built-in`.
- Executed Code Maat: `name=code-maat`, `mode=executable`.
- Imported Code Maat CSV: `name=code-maat`, `mode=csv`.

`input_scope` values:

- Git hotspots: `committed_history+working_tree` because LOC reads current tracked files.
- Git temporal coupling: `committed_history`.
- Code Maat executable: `committed_history`.
- Code Maat CSV: `committed_history` with input hashes and unverified-input limitations.

`parameters` MUST record all validity-critical settings actually used, including:

- `since`;
- `max_commits`;
- `max_changeset_size`;
- `rename_threshold`;
- effective default exclusions;
- explicit excludes;
- `limit`;
- low-sample thresholds;
- analysis-specific thresholds/subjects/deleted policy;
- Code Maat analysis names and command identity where applicable;
- `input_sha256` values for imported CSV.

The result MUST NOT contain a repository ID invented solely for cache addressing, a working-tree fingerprint, or a cache path.

### 12.3 History-quality object

`history_quality` MUST contain:

```json
{
  "shallow": false,
  "matched_commits": 0,
  "eligible_commits": 0,
  "history_start": null,
  "history_end": null,
  "active_days": 0,
  "bulk_commits_excluded": 0,
  "bulk_file_touches_excluded": 0,
  "bulk_commit_ratio": 0.0,
  "bulk_touch_ratio": 0.0,
  "paths_excluded": 0,
  "renames_detected": 0,
  "renames_resolved": 0,
  "renames_unresolved": 0,
  "limitations": []
}
```

Each limitation MUST be:

```json
{
  "code": "STABLE_MACHINE_CODE",
  "message": "concise human-readable explanation"
}
```

An optional `details` object MAY contain small supporting counts. It MUST NOT contain raw commit lists or unbounded output.

Required limitation codes where applicable:

- `SHALLOW_HISTORY`;
- `INSUFFICIENT_HISTORY`;
- `LOW_SAMPLE_COMMITS`;
- `SHORT_HISTORY_SPAN`;
- `BULK_COMMITS_EXCLUDED`;
- `HIGH_BULK_EXCLUSION`;
- `UNRESOLVED_RENAMES`;
- `CODE_MAAT_INPUT_FILTERS_UNVERIFIED`;
- `CODE_MAAT_RENAME_HANDLING_UNVERIFIED`;
- `CODE_MAAT_SUPPORT_FILTER_UNAVAILABLE`;
- `CODE_MAAT_FAILED_FALLBACK_GIT`.

Rules:

- `SHALLOW_HISTORY` is emitted whenever Git reports a shallow repository.
- `INSUFFICIENT_HISTORY` is emitted when fewer than two eligible commits remain. Candidate output MUST then be empty.
- `LOW_SAMPLE_COMMITS` is emitted when eligible commits are below `--low-sample-commits`.
- `SHORT_HISTORY_SPAN` is emitted when `active_days` is below `--low-sample-days` and at least two eligible commits exist.
- `BULK_COMMITS_EXCLUDED` is emitted when any bulk commit is excluded.
- `HIGH_BULK_EXCLUSION` follows Section 9.6.
- Warnings are observations about evidence quality, not proof that results are useless.

### 12.4 Hotspot result

`analysis` MUST equal `hotspots`.

`metric_definitions` MUST contain:

```json
{
  "revisions": {
    "unit": "commits_touching_file or Code Maat revisions",
    "definition": "provider-specific definition"
  },
  "size": {
    "name": "physical_loc or absolute_entity_churn",
    "unit": "physical_lines or lines",
    "definition": "provider-specific definition"
  },
  "revision_rank": {
    "range": [0, 1],
    "definition": "normalized ascending dense rank; maximum is 1"
  },
  "size_rank": {
    "range": [0, 1],
    "definition": "normalized ascending dense rank; maximum is 1"
  },
  "score": {
    "range": [0, 1],
    "definition": "revision_rank multiplied by size_rank; candidate ranking only"
  }
}
```

Each hotspot candidate MUST be:

```json
{
  "path": "normalized/repository-relative/path",
  "revisions": 1,
  "size": 1,
  "revision_rank": 1.0,
  "size_rank": 1.0,
  "score": 1.0
}
```

### 12.5 Temporal-coupling result

`analysis` MUST equal `temporal_coupling`.

`metric_definitions` MUST contain:

```json
{
  "shared_commits": {
    "unit": "commits or null",
    "definition": "provider-specific support definition"
  },
  "coupling": {
    "unit": "ratio or percent",
    "range": [0, 1],
    "definition": "provider-specific definition"
  },
  "ordering": "human-readable provider-specific ordering"
}
```

For Code Maat the coupling range MUST be `[0, 100]` and unit `percent`.

Each temporal candidate MUST be:

```json
{
  "paths": ["left/path", "right/path"],
  "shared_commits": 2,
  "left_revisions": 4,
  "right_revisions": 3,
  "coupling": 0.6666666666666666,
  "average_revisions": null
}
```

For Code Maat, support and revision fields MAY be `null` only when the provider output does not contain them. For Git, they MUST be integers.

## 13. Code Maat integration

### 13.1 Concrete availability

Code Maat is concretely available only when one of these is true:

1. The caller supplies valid analysis-specific CSV input.
2. The caller supplies a valid explicit `--code-maat-command`.
3. An exact executable named `code-maat` is present on `PATH`.

The helper MUST NOT search the filesystem for jars, inspect Docker images, query package registries, or infer availability from Java alone.

### 13.2 Executable mode

Executable mode MUST:

1. Create a temporary working directory outside the target repository.
2. Produce Code Maat-compatible Git input using current documented Code Maat conventions.
3. Apply path, rename, current/deleted-entity, history-window, and bulk-commit policies before or while producing the input.
4. Invoke only the required analyses:
   - hotspot: revisions and entity churn;
   - temporal coupling: coupling.
5. Capture machine-readable CSV.
6. determine the Code Maat version from a reliable version mechanism or require `--code-maat-version`;
7. parse and validate output;
8. remove temporary files at the end of the command;
9. avoid writing to the target repository.

The exact flags used to invoke Code Maat MAY follow the current supported version at implementation time. They MUST be isolated to a dedicated Code Maat integration function and covered by tests using a fake executable. This flexibility does not permit a generic provider layer.

### 13.3 CSV mode

Native CSV requirements:

- revisions CSV required columns: `entity`, `n-revs`;
- entity-churn CSV required columns: `entity`, `added`, `deleted`;
- coupling CSV required columns: `entity`, `coupled`, `degree`;
- optional coupling columns: `average-revs`, `shared-revisions`, `entity-revisions`, `coupled-revisions`.

CSV mode MUST:

- require `--code-maat-version` because the provider version cannot be trusted from the file itself;
- calculate SHA-256 for every supplied CSV;
- validate headers, required values, numeric conversion, ranges, duplicates, and normalized repository-relative paths;
- filter hotspot entities to current tracked eligible paths;
- filter temporal entities to current paths unless `--include-deleted` is set;
- preserve metric units and ranges;
- emit `CODE_MAAT_INPUT_FILTERS_UNVERIFIED` because the helper cannot prove how the external CSV’s source log was filtered;
- emit `CODE_MAAT_RENAME_HANDLING_UNVERIFIED` because rename preprocessing of imported CSV cannot be proven.

Malformed explicit CSV MUST fail. It MUST NOT silently fall back to Git.

### 13.4 Provider failure and fallback

When `--provider auto` selected an automatically discovered `code-maat` executable and that executable is unavailable at execution time, exits unsuccessfully, or emits malformed output:

- the helper MUST fall back to Git;
- the Git result MUST include `CODE_MAAT_FAILED_FALLBACK_GIT` with a concise reason;
- raw provider output MUST NOT enter the candidate JSON.

When Code Maat was explicitly requested through `--provider code-maat`, explicit CSV, or explicit command input, failure MUST be returned to the caller. Explicit user input MUST not be silently ignored.

### 13.5 Installation and data handling

The helper MUST NOT install Code Maat or any dependency.

The skills MUST request permission before installing or configuring Code Maat. The request MUST explain:

- the missing evidence capability;
- why Code Maat would materially improve this analysis;
- runtime/install dependencies;
- local versus remote data handling;
- the Git fallback.

V3 MUST NOT require a remote Code Maat service or transmit repository data.

## 14. Error and fallback behavior

### 14.1 Exit codes

The CLI MUST use:

- `0`: a structurally valid result was emitted, including valid results with limitations or zero candidates;
- `1`: operational/provider/data failure;
- `2`: command-line usage error.

### 14.2 Error object

For exit code `1`, standard error MUST contain one JSON object:

```json
{
  "error": {
    "code": "STABLE_ERROR_CODE",
    "message": "concise human-readable explanation"
  }
}
```

Optional bounded `details` MAY be included. Source contents, raw history, credentials, and full provider output MUST NOT be emitted.

Required error codes where applicable:

- `NOT_A_GIT_REPOSITORY`;
- `NO_GIT_HISTORY`;
- `GIT_UNAVAILABLE`;
- `GIT_COMMAND_FAILED`;
- `INVALID_REPOSITORY_PATH`;
- `INVALID_OUTPUT_PATH`;
- `CODE_MAAT_UNAVAILABLE`;
- `CODE_MAAT_VERSION_UNKNOWN`;
- `CODE_MAAT_COMMAND_FAILED`;
- `MALFORMED_CODE_MAAT_CSV`;
- `INVALID_CODE_MAAT_ENTITY`;
- `INCONSISTENT_CODE_MAAT_HOTSPOT_INPUTS`;
- `RESULT_VALIDATION_FAILED`.

### 14.3 Insufficient history

Insufficient, shallow, short, or bulk-dominated history is not an operational failure when a Git repository and HEAD exist.

The helper MUST return exit `0` with:

- an empty candidate list when fewer than two eligible commits remain;
- appropriate history-quality limitations;
- complete provenance and metric definitions.

The skills MUST not interpret empty history results as zero coupling, zero debt, or a healthy repository.

### 14.4 Skill fallbacks

- Hotspots: if neither Code Maat nor Git history can produce evidence, report that behavioral hotspot analysis is unavailable. Do not substitute static complexity or subjective file-size ranking without clearly describing it as a different analysis.
- Coupling: if temporal evidence is unavailable, the skill MAY still perform bounded static, logical/domain, and test-coupling inspection when the user’s subject supplies a meaningful source scope.
- Source-understanding skills: if a repository-native command is unavailable, continue through targeted source/config/test inspection and state the limitation.
- Verify: inability to prove a claim results in `UNKNOWN`, not an invented fallback metric or relationship.

## 15. Privacy, mutation, and installation rules

### 15.1 Local/private default

All bundled processing MUST be local and offline.

V3 MUST NOT upload:

- source code;
- Git history;
- repository metadata;
- candidate results;
- generated reports.

### 15.2 Repository mutation

Analysis skills MUST NOT deliberately edit tracked source, configuration, history, or documentation in the target repository.

The helper MAY write only:

- temporary files in a system temporary directory;
- an explicitly requested `--output` path.

There is no default output or cache path.

Repository-native commands MAY create their ordinary ephemeral/ignored artifacts only when the command is already configured, non-destructive, and relevant to a concrete evidence gap. If a command may materially mutate the repository, services, databases, or external state, Codex MUST ask before running it.

### 15.3 External installation/configuration

No skill or helper may silently:

- install a package;
- download a binary or jar;
- pull a container image;
- alter repository configuration;
- enable a remote service;
- transmit repository data.

Permission must be explicit and specific to the proposed action.

## 16. Verification requirements

### 16.1 Common verification

Before final output, every skill MUST:

1. Revisit the user’s requested scope.
2. Confirm referenced paths exist.
3. Confirm named symbols occur, then inspect definitions/callers before claiming semantics.
4. Verify important imports, calls, registrations, routes, schemas, messages, configuration, and tests as applicable.
5. Distinguish reachable behavior from examples, generated code, stale code, or dead code where evidence permits.
6. Label unresolved semantic claims `INFERRED` or `UNKNOWN`.
7. Report material contradictions.
8. Check that no major concept within the bounded requested scope was accidentally omitted.

There MUST be no shared lexical-reference script. Direct filesystem checks and `rg` MAY be batched by Codex.

### 16.2 History verification

Hotspot and coupling outputs MUST verify:

- provider and provider mode;
- provider version;
- repository HEAD and dirty/shallow state;
- history window and parameters;
- metric definition, unit, and range;
- candidate limit and truncation;
- limitations and confounders;
- current existence of reported paths unless deleted entities were explicitly requested.

Metrics MUST be quoted using the provider’s definition. Code Maat percentage coupling MUST not be restated as the Git fallback ratio.

### 16.3 Semantic candidate verification

Historical candidates MUST be inspected in source and tests before the skill makes claims about:

- technical debt;
- hidden coupling;
- excessive responsibility;
- boundary leakage;
- missing abstractions;
- fragile tests;
- repeated defects;
- ownership or knowledge risk;
- refactoring need.

### 16.4 Diagrams

Every meaningful node and edge in a diagram MUST correspond to inspected source, configuration, tests, or explicitly labeled inference.

A valid Mermaid parse is not semantic verification.

## 17. Testing requirements

### 17.1 General constraints

Tests MUST be local, deterministic, and network-free.

Tests MUST NOT:

- clone or download external repositories;
- require Code Maat, Java, Docker, or another optional tool;
- depend on a developer’s global Git configuration;
- write persistent state outside the test temporary area.

Small temporary Git repositories MUST be constructed during tests and removed afterward.

### 17.2 Helper test coverage

Automated tests MUST cover at least:

1. Hotspot Git revision counting.
2. Physical LOC, including blank lines, final newline behavior, empty files, binaries, and symlink safety.
3. Default generated/vendor/build/cache exclusions.
4. Repeatable explicit exclusion patterns.
5. Bulk commits excluded from hotspot revisions.
6. Bulk commits excluded from endpoint revisions and coupling pairs.
7. Bulk quality ratios and limitation codes.
8. A simple rename.
9. A multi-step rename chain.
10. An unresolved/deleted rename.
11. `--include-deleted` behavior.
12. Dense tie-correct hotspot ranks.
13. Stable hotspot ordering.
14. Candidate limit, total, count, and truncation.
15. Git temporal shared-commit and coupling calculations.
16. Temporal support-first ordering.
17. Exact subject filtering.
18. Tests remaining eligible as ordinary paths.
19. Shallow-history limitation.
20. Insufficient-history empty result.
21. Low-commit and short-span warnings.
22. Dirty-state and input-scope provenance.
23. Empty Git repository failure.
24. Non-Git repository failure.
25. Missing Git failure.
26. Code Maat native revisions/entity-churn CSV parsing.
27. Code Maat coupling CSV parsing and percentage semantics.
28. Code Maat duplicate, missing, malformed, out-of-range, and invalid-path failures.
29. CSV SHA-256 provenance.
30. Code Maat hotspot input entity mismatch.
31. CSV-mode unverified-filter and rename limitations.
32. A fake Code Maat executable invocation without a shell.
33. Automatic discovered-Code-Maat failure falling back to Git.
34. Explicit Code Maat failure not falling back.
35. Provider selection order.
36. Argument conflict and validation behavior.
37. JSON stdout remaining clean when diagnostics are emitted.
38. Exit codes and structured error objects.
39. Result-level provenance only, with no candidate-level copies.
40. Output-file content matching stdout.

### 17.3 Structural suite tests

Structural validation MUST verify:

- exact nine-skill set;
- valid skill frontmatter names and descriptions;
- explicit-only `openai.yaml` policy for every skill;
- portable and compatibility plugin manifests;
- all local Markdown links from skills and shared references;
- every skill links to `analysis-basics.md`;
- only hotspots and coupling link to `history-analysis.md` during ordinary startup;
- no obsolete V2 shared-reference link remains;
- no obsolete helper command is documented or invoked;
- no unfinished scaffold placeholder remains.

### 17.4 Instruction-level review

Automated tests cannot establish semantic output quality. Before V3 is declared complete, perform and document a manual review that confirms:

- each skill’s scope and stopping rule is clear;
- adjacent skills remain distinguishable;
- no skill implies nonexistent deterministic machinery;
- hotspot candidates are never automatically labeled debt;
- temporal coupling is never automatically labeled a defect;
- repository-native tools are tied to concrete gaps;
- optional-tool installation requires permission;
- the final documentation accurately describes actual runtime behavior.

Real-world semantic evaluation remains a separate user validation activity and MUST NOT be claimed unless performed.

## 18. Migration requirements from V2

Migration MUST follow Expand → Migrate → Contract. Each phase has a blocking gate.

### 18.1 Pre-migration inventory

Before Expand, the implementation session MUST search for every consumer of:

- `shared/scripts/codebase_intelligence.py`;
- `discover`;
- `repo-meta`;
- `default-store`;
- `analyze-history`;
- `validate`;
- `cache-status`;
- `query`;
- `rank-hotspots`;
- `adapt-code-maat`;
- `verify-references`;
- `core.md`;
- `source-first.md`;
- `tool-first.md`;
- `tool-providers.md`;
- `evidence-contract.md`;
- `verification.md`;
- `tutorial-workflow.md`;
- generic evidence type names and cache terminology.

The inventory MUST include skills, tests, scripts, README, design/validation docs, and manifests where applicable.

### 18.2 Expand phase

Expand MUST:

1. Add `shared/scripts/history_candidates.py` without removing the V2 helper.
2. Add the bounded result schema and its focused tests.
3. Add `analysis-basics.md` and `history-analysis.md` alongside V2 references.
4. Add characterization fixtures for bulk construction commits, sparse history, renames, generated paths, ranking ties, candidate limits, and malformed Code Maat output.
5. Keep all existing V2 skill callers and commands operational.
6. Preserve all nine public skill names and manifests.

Expand gate:

- the V2 test/validation suite still passes;
- the V3 helper test suite passes independently;
- both old and new internal interfaces are available;
- no skill has been partially migrated to an incomplete contract.

### 18.3 Migrate phase

Migrate MUST proceed in bounded steps:

1. Migrate `codebase-hotspots` to `history_candidates.py hotspots`.
2. Validate its instruction flow and bounded result handling.
3. Migrate `codebase-coupling` to `history_candidates.py temporal-coupling`.
4. Validate temporal fallback plus semantic static/logical/test inspection.
5. Migrate all skills to `analysis-basics.md`.
6. Ensure only hotspots and coupling load `history-analysis.md`.
7. Fold tutorial guidance into `codebase-tutorial/SKILL.md`.
8. Move verify-specific instructions into `codebase-verify/SKILL.md`.
9. Update tests and documentation with each migrated caller.

During Migrate:

- V2 and V3 helper paths MAY coexist;
- migrated skills MUST NOT call V2 commands;
- unmigrated skills MUST remain functional until their migration step;
- public skill intent and explicit invocation behavior MUST remain stable;
- exact historical rankings may change because V3 deliberately fixes bulk handling, renames, and ties. These are intended behavior changes, not compatibility failures.

Migrate gate:

- all nine skills use the V3 shared-reference structure;
- hotspots and coupling use only V3 helper commands;
- repository-wide search finds no production skill caller of the V2 helper or references;
- all relevant tests pass;
- manual instruction review passes.

### 18.4 Contract phase

Only after the Migrate gate passes, Contract MUST:

1. Remove `shared/scripts/codebase_intelligence.py`.
2. Remove obsolete shared references:
   - `core.md`;
   - `source-first.md`;
   - `tool-first.md`;
   - `tool-providers.md`;
   - `evidence-contract.md`;
   - `verification.md`.
3. Remove `skills/codebase-tutorial/references/tutorial-workflow.md` and its now-empty directory if applicable.
4. Replace V2 infrastructure tests with focused V3 tests.
5. Remove cache, generic provider, generic evidence, discovery, query, and lexical-verifier documentation.
6. Update validation scripts for the final tree.
7. Run repository-wide searches for every obsolete command, type, and reference.
8. Run all tests and validation.

Contract gate:

- zero production/test/documentation consumers of removed V2 machinery remain, except clearly labeled historical documents such as the runtime audit and V2 specification;
- no compatibility wrapper remains without a documented external consumer;
- the complete final V3 test and validation suite passes;
- all nine skills remain installable and explicit-only;
- README and current design/validation documentation describe V3, not V2.

### 18.5 Historical documents

- `SPEC.md` MAY remain as the historical V2 specification but SHOULD be clearly identified as superseded by `SPEC-V3.md` for current implementation.
- `docs/runtime-audit.md` MUST remain as historical design evidence.
- `docs/v3-architecture.md` MUST remain as the accepted architectural rationale.
- Historical documents do not count as stale callers when they clearly describe V2 in the past tense.

## 19. Documentation requirements

### 19.1 README

The README MUST document:

- product purpose;
- the nine skills and invocation examples;
- explicit-only behavior;
- source-inspection versus history-candidate workflows;
- Code Maat preference and concrete availability rules;
- Git + LOC hotspot fallback;
- Git temporal-coupling fallback;
- bounded candidate semantics;
- history-quality limitations;
- provider-specific metric definitions;
- absence of implicit persistent caching;
- local/private defaults;
- installation/configuration permission rule;
- limitations and non-goals;
- development test and validation commands.

It MUST NOT claim:

- nine deterministic analyzers;
- automatic architecture, call, subsystem, concept, or impact analysis;
- generic ecosystem analysis;
- provider independence beyond Git and Code Maat;
- generic Evidence v1 support;
- cached evidence reuse;
- automatic Code Maat discovery beyond the concrete rules in this specification;
- semantic verification by lexical matching.

### 19.2 Design documentation

Current design documentation MUST explain:

- why seven skills are Codex-guided source workflows;
- why deterministic machinery is confined to historical candidates;
- why static/logical/test coupling remains semantic;
- why the generic evidence store, cache, discovery, and provider layers were removed;
- why store-level provenance is sufficient;
- why observations remain separate from conclusions.

### 19.3 Validation documentation

`docs/validation.md` MUST list:

- automated helper cases actually run;
- structural checks actually run;
- Code Maat behavior tested through CSV fixtures/fake executables;
- known untested external-runtime paths;
- manual instruction review performed;
- explicit statement of whether real-world semantic evaluation occurred.

### 19.4 CLI documentation

The helper’s `--help`, shared history reference, and README examples MUST agree on:

- command names;
- option names and defaults;
- provider selection;
- exit behavior;
- result limits;
- output-file behavior;
- metric definitions.

## 20. Explicit non-goals

V3 deliberately does not automate:

- semantic architecture discovery;
- architectural boundary inference through a deterministic graph;
- general static dependency graphs;
- call graphs or runtime tracing;
- subsystem detection;
- tutorial concept detection or ordering;
- impact completeness;
- logical/domain coupling detection;
- test-coupling detection;
- technical-debt classification;
- defect/fix classification from commit messages;
- ownership/knowledge analysis by default;
- ecosystem-specific complexity analysis;
- generic test coverage analysis;
- claim extraction through a deterministic artifact parser;
- Mermaid semantic verification;
- generic external-tool discovery or recommendation;
- remote/SaaS analysis;
- silent installation;
- implicit evidence persistence;
- provider SDKs, registries, or dynamic plugins;
- future evidence types without an implemented producer and consumer.

The absence of these capabilities MUST NOT be described as incomplete V3 implementation.

## 21. V3 acceptance criteria

V3 is complete only when all of the following are true:

1. Exactly nine requested skills exist.
2. Every skill is explicitly invoked only.
3. Plugin manifests remain valid.
4. Every skill loads the concise shared analysis contract.
5. Only hotspots and coupling ordinarily load the history-analysis reference.
6. Tutorial guidance is inside the tutorial skill.
7. Verify behavior is inside the verify skill and uses no lexical helper.
8. Source-understanding skills rely on targeted Codex inspection, not invented deterministic analyzers.
9. `history_candidates.py` exposes only hotspot and temporal-coupling analysis commands, aside from help/version.
10. The Git hotspot fallback uses eligible change frequency plus current physical LOC.
11. Code Maat hotspot results preserve revisions/entity-churn semantics.
12. Git temporal coupling uses shared eligible commits divided by the smaller endpoint revision count.
13. Code Maat coupling preserves provider percentage semantics.
14. Code Maat is preferred only when concretely available.
15. `auto` falls back to Git when Code Maat is absent.
16. Explicit malformed or failed Code Maat input is not silently ignored.
17. Bulk commits are excluded from both hotspot and temporal calculations.
18. Rename chains are handled where unambiguous and limitations are reported otherwise.
19. Generated/vendor/build/cache noise and explicit patterns are filtered.
20. Shallow, insufficient, low-sample, short-span, and bulk-dominated histories are surfaced.
21. Candidate results are deterministically ordered and bounded.
22. Ranking ties are handled correctly.
23. Result provenance is store-level only.
24. No generic evidence ontology or speculative evidence types remain.
25. No implicit persistent cache or default result path remains.
26. No generic provider framework remains.
27. No generic ecosystem/tool-discovery or recommendation framework remains.
28. No lexical reference verifier remains.
29. No architecture, call-graph, subsystem, concept, or impact analyzer is introduced.
30. Static, logical/domain, and test coupling use targeted semantic investigation.
31. Repository-native tools are used only for concrete evidence gaps.
32. External installation/configuration always requires explicit permission.
33. Bundled processing is local/private by default.
34. Skills do not deliberately mutate target repositories.
35. Historical candidates are never automatically labeled debt or bad architecture.
36. Every material conclusion receives semantic verification or an uncertainty label.
37. Required helper and structural tests pass.
38. Repository-wide search confirms no current caller of obsolete V2 machinery.
39. Current README/design/validation documentation describes actual V3 behavior.
40. Historical V2 documents are clearly distinguishable from current V3 instructions.
41. No claim is made that real-world semantic quality was validated unless that evaluation actually occurred.

## 22. Required interpretations of accepted proposal ambiguities

The accepted architecture intentionally left several implementation details open. This specification makes the following narrow interpretations so a fresh implementation session can proceed deterministically:

### 22.1 Numeric defaults

The proposal required bounded results, configurable bulk handling, rename handling, and low-sample warnings but did not choose exact values. This specification uses:

- candidate limit: `20`;
- maximum changeset size: `30` relevant paths;
- minimum shared commits: `2`;
- rename similarity: `50%`;
- low-sample commit warning: fewer than `20` eligible commits;
- short-span warning: fewer than `30` active days;
- high bulk-exclusion warning: at least `50%` of commits or relevant touches.

These values are implementation defaults, not semantic truth. Validity-critical values are overridable where specified and MUST be recorded in provenance.

### 22.2 Dense-rank formula

The proposal required tie-correct percentile/dense ranking but did not choose a formula. This specification uses normalized ascending dense position divided by the number of distinct values. This gives tied values equal rank, the maximum rank `1.0`, and avoids zeroing every candidate on an axis with a minimum value.

### 22.3 Code Maat executable configuration

The proposal allowed a configured wrapper/executable or JAR command without defining a safe command representation. This specification uses a JSON string array executed without a shell and also recognizes an exact `code-maat` executable on `PATH`.

The exact Code Maat flags may follow the supported version at implementation time because the proposal intentionally did not pin a Code Maat release. The required analyses, preprocessing, outputs, and bounded result semantics are fixed.

### 22.4 Imported Code Maat history quality

The proposal required history-quality metadata but user-supplied CSV does not prove how its source log handled bulk commits or renames. This specification computes local repository history metadata and explicitly marks imported-filter and rename handling as unverified rather than pretending equivalence.

### 22.5 Repository-native command side effects

The proposal permits repository-native operations while requiring analysis to be read-only. This specification interprets that as forbidding deliberate tracked/source mutation while allowing ordinary configured commands to create bounded ephemeral or ignored artifacts. Commands with material or uncertain side effects require permission.

No other architectural interpretation is introduced by this specification.
