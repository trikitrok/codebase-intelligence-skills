# Codebase Intelligence — Specification

## 1. Purpose

Design and implement a reusable suite of Codex Agent Skills called **Codebase Intelligence**.

The suite helps developers understand, investigate, verify, and plan changes to software repositories.

This is **not one large skill with multiple modes**.

It is a **collection of independently invokable, specialized skills** that share conventions, deterministic infrastructure, evidence formats, scripts, and supporting resources where appropriate.

The suite should be optimized for:

1. Accuracy.
2. Evidence-backed conclusions.
3. Token economy.
4. Deterministic analysis where appropriate.
5. Selective source inspection.
6. Explicit user control.
7. Language independence with ecosystem-specific enhancements.
8. Composability.
9. Graceful fallback when external tools are unavailable.
10. Reproducibility.
11. Privacy and suitability for private repositories.
12. Progressive disclosure of instructions and analysis.

This repository contains the **implementation of the Codebase Intelligence skill suite**.

It is **not itself a target repository for Codebase Intelligence analysis**.

Do not confuse building the analyzer with running the completed analyzer against this repository.

Real-world evaluation of the completed skills against external repositories will be performed separately by the user.

---

# 2. Research Current Conventions First

Before designing or writing the skills, research the current environment and conventions.

## 2.1 Codex and Agent Skills

Inspect current official OpenAI/Codex Agent Skills documentation available to you.

Determine:

* Current Agent Skills directory conventions.
* `SKILL.md` requirements.
* Frontmatter requirements.
* How supporting files are loaded.
* How progressive disclosure works.
* How explicitly invoking a skill works.
* Recommended locations for scripts and references.
* Whether and how multiple skills can share resources.
* Whether nested/shared skill infrastructure is supported.
* Current skill installation/discovery conventions.
* Current recommendations for keeping skill context small.
* Any relevant Codex-specific capabilities for repository inspection, shell execution, scripts, and tool use.

Prefer current official documentation over assumptions in this specification.

If current Codex conventions suggest a better physical layout than examples in this document, follow the current conventions while preserving the architectural intent described here.

Explain important deviations in the final implementation report.

## 2.2 Existing Work

Inspect the following projects for ideas and prior art.

### PocketFlow Codebase Knowledge

https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge

Study its approach to:

* repository exploration
* identifying abstractions
* ordering concepts
* tutorial generation
* diagrams
* source references
* pedagogical explanation

Do not blindly reproduce its implementation.

### codebase-tutorial

https://github.com/rowlando/codebase-tutorial

Inspect its current implementation directly.

Do not assume what it contains based on descriptions elsewhere.

Identify:

* useful ideas
* differences from PocketFlow
* current Agent Skill conventions it demonstrates
* limitations
* opportunities for improvement

### Code Maat

https://github.com/adamtornhill/code-maat

Study relevant behavioral/evolutionary analysis capabilities, particularly:

* change frequency
* churn
* temporal/evolutionary coupling
* contributor/ownership patterns
* historical analysis

Code Maat is a potential **provider of analysis capabilities**, not a mandatory dependency.

## 2.3 Behavioral Code Analysis

Where relevant, investigate established behavioral/evolutionary code-analysis techniques associated with Adam Tornhill's work, including concepts such as:

* hotspots
* temporal coupling
* change frequency
* churn
* complexity combined with change history
* ownership and knowledge concentration
* evolutionary relationships

Do not automatically implement every possible technique as a separate skill.

The initial suite should remain focused.

---

# 3. Fundamental Analysis Principle

The fundamental principle of this suite is:

> **Do not spend LLM tokens deriving information that a deterministic tool can obtain reliably and economically.**

Do not apply this dogmatically.

Use deterministic tools where they improve:

* accuracy
* reproducibility
* token economy
* coverage
* quantitative analysis
* filtering
* ranking
* verification

Use Codex where semantic understanding is required:

* architecture
* intent
* conceptual boundaries
* explaining why code exists
* interpreting suspicious relationships
* understanding domain behavior
* evaluating evidence
* synthesizing findings
* investigating anomalies
* understanding implementation decisions
* planning changes

Deterministic analysis should generally **reduce the search space for Codex**, not attempt to replace semantic reasoning.

A useful conceptual model is:

```text
Repository
    │
    ├── Git/history tools
    ├── static analysis
    ├── project-native tooling
    └── deterministic helpers
             │
             ▼
      Structured evidence
             │
        filter / rank
             │
             ▼
           Codex
     semantic analysis
             │
             ▼
       verification
             │
             ▼
          report
```

However, source-first skills may bypass much of this pipeline when direct semantic repository exploration is more appropriate.

---

# 4. Skill Suite

Create the following independently invokable skills.

## Understanding

* `codebase-onboarding`
* `codebase-tutorial`
* `codebase-architecture`
* `codebase-trace`
* `codebase-deep-dive`

## Change

* `codebase-change`

## Investigation

* `codebase-hotspots`
* `codebase-coupling`
* `codebase-verify`

Do **not** implement these as modes of one large `codebase` skill.

The user should explicitly invoke the capability they want.

Use the current idiomatic Codex mechanism for explicit skill invocation.

Document invocation examples for every skill.

---

# 5. Shared Infrastructure

Avoid duplicating substantial instructions, schemas, or scripts between skills.

Determine the best currently supported way for skills to share:

* repository discovery conventions
* evidence conventions
* source-reference conventions
* verification procedures
* tool discovery
* tool-selection policy
* installation permission policy
* evidence schema
* evidence storage
* cache/provenance logic
* deterministic analysis scripts
* provider adapters

Shared infrastructure should **not become a user-facing skill** unless current Codex architecture genuinely requires it.

Prefer reusable supporting resources and scripts consumed by specialized skills.

Optimize shared infrastructure for **progressive disclosure and token economy**.

A skill should not load detailed instructions for unrelated analyses.

For example:

* `codebase-architecture` should not need detailed Code Maat instructions.
* `codebase-hotspots` should not need tutorial-writing instructions.
* `codebase-tutorial` should not need temporal-coupling implementation details.

---

# 6. Three Analysis Strategies

The suite uses three broad analysis strategies.

## 6.1 Source-First

Used primarily by:

* `codebase-onboarding`
* `codebase-tutorial`
* `codebase-architecture`
* `codebase-trace`
* `codebase-deep-dive`
* `codebase-change`

Typical pipeline:

```text
repository
    ↓
targeted repository exploration
    ↓
identify relevant source
    ↓
inspect implementation
    ↓
build evidence
    ↓
semantic analysis
    ↓
verification
    ↓
output
```

Do not unnecessarily run heavyweight static/history analysis for these skills.

Architecture in particular should **not be reduced to a dependency graph**.

## 6.2 Tool-First

Used primarily by:

* `codebase-hotspots`
* `codebase-coupling`

Typical pipeline:

```text
repository
    ↓
deterministic analysis
    ↓
structured evidence
    ↓
rank/filter candidates
    ↓
selective source inspection
    ↓
semantic interpretation
    ↓
verification
    ↓
output
```

Codex should generally not read large portions of the repository before deterministic analysis has narrowed the search space unless necessary.

## 6.3 Evidence-First

Used primarily by:

* `codebase-verify`

Typical pipeline:

```text
existing claims/document/diagram
    ↓
extract verifiable claims
    ↓
deterministic checks where possible
    ↓
targeted source inspection
    ↓
evidence classification
    ↓
identify discrepancies
    ↓
verified report
```

---

# 7. Evidence Status Model

All skills should use a consistent evidence-status model where useful.

Important claims may be classified as:

### VERIFIED

Directly supported by inspected evidence.

### INFERRED

Strongly suggested by evidence but not directly demonstrated.

### UNKNOWN

Insufficient evidence.

### CONTRADICTED

Available evidence contradicts the claim.

Do not present `INFERRED` findings as `VERIFIED` facts.

Do not invent:

* files
* symbols
* APIs
* calls
* imports
* architectural relationships
* runtime behavior
* historical relationships
* metrics

---

# 8. Evidence Sources

Important claims should be associated with evidence such as:

* repository path
* symbol/function/class
* source behavior
* test evidence
* configuration
* Git-history evidence
* deterministic-tool output
* project manifests
* build configuration
* runtime/generated evidence where available

When evidence conflicts, investigate the discrepancy.

A useful default ordering is:

1. Current executable source.
2. Tests.
3. Configuration.
4. Generated/runtime evidence.
5. Current documentation.
6. README.
7. Comments.

Do not apply this ordering blindly.

For example:

* source may contain dead code
* tests may be stale
* configuration may be unused
* documentation may describe intended rather than actual behavior

Report meaningful contradictions.

---

# 9. Verification

Every skill must perform an appropriate verification pass.

Verification should check, where relevant:

* referenced files exist
* referenced symbols exist
* imports/calls exist
* architectural relationships have evidence
* execution traces have evidence
* historical metrics came from valid repository history
* Mermaid edges correspond to supported relationships
* documentation was not blindly trusted
* inferred claims are labeled
* tests were inspected where relevant
* significant concepts were not accidentally omitted

Do not implement verification merely as:

> Double-check your answer.

Use repository access, shell commands, deterministic scripts, static analysis, or other available mechanisms where useful.

Prefer deterministic verification for deterministic facts.

---

# 10. Tool Policy

The suite may use external deterministic tools.

Prefer tools that are:

1. Open source.
2. Mature.
3. Maintained.
4. Deterministic/reproducible.
5. Capable of machine-readable output.
6. Local/offline where practical.
7. Suitable for private repositories.
8. Useful enough to justify their installation and runtime cost.

## 10.1 Tool Discovery

Before recommending installation:

1. Inspect the repository.
2. Identify languages and ecosystems.
3. Inspect project manifests and configuration.
4. Detect tools already available.
5. Prefer tools already used by the repository.
6. Determine which analysis capabilities are missing.

## 10.2 Permission Before Installation

Never silently install external tools.

If a useful tool is missing:

1. Explain which tool is recommended.
2. Explain what capability it provides.
3. Explain why it would materially improve this analysis.
4. Explain relevant installation/runtime dependencies.
5. Ask for permission.

If permission is granted, install/configure the tool if appropriate.

If permission is denied, fall back gracefully.

The skill must remain useful without optional tools.

Conceptually:

```text
Need capability
      │
      ▼
Suitable tool available?
      │
   yes ───────────────→ use it
      │
     no
      ▼
Would an external OSS tool
materially improve analysis?
      │
   yes
      ▼
Explain tool + reason
      │
      ▼
Ask permission
   │          │
  yes         no
   │          │
install     fallback
   │          │
   └─────┬────┘
         ▼
      analysis
```

---

# 11. Language-Independent Core

All skills must have a reasonable language-independent fallback.

Available primitives may include:

* `git`
* repository tree
* `find`
* `rg` / `grep`
* manifests
* file metadata
* build/test configuration
* selective Codex source inspection

Do not assume any particular programming language.

---

# 12. Ecosystem-Specific Tool Recommendation

After detecting repository languages and ecosystems, skills may recommend appropriate open-source analysis tools.

Potential capabilities include:

* dependency analysis
* complexity
* duplication
* dead code
* static analysis
* architecture rules
* test coverage
* security/static checks
* code ownership
* Git-history analysis

Do not hardcode arbitrary tools merely because they are popular.

Research suitable current tools.

Prefer project-native tooling where possible.

Tool recommendations should be **capability-oriented**.

For example:

```text
required capability:
    complexity analysis

available provider:
    <ecosystem-specific tool>
```

rather than designing the skill around one particular complexity tool.

---

# 13. Machine-Readable Evidence Contract

Investigation-oriented parts of the Codebase Intelligence suite must share a small, machine-readable evidence contract.

## 13.1 Purpose

Deterministic tools should not primarily communicate with Codex through human-oriented prose or arbitrary raw output.

Prefer:

```text
deterministic tool
      ↓
small deterministic adapter
      ↓
normalized evidence
      ↓
evidence store/cache
      ↓
filtering / ranking / reuse
      ↓
selective Codex investigation
```

This contract acts as an internal API between:

* deterministic tools
* adapters
* caches
* investigation skills
* verification logic

The goal is to reduce:

* repeated parsing
* repeated analysis
* tool-specific prompt instructions
* unnecessary source inspection
* unnecessary token consumption

## 13.2 Keep the Contract Small

Do not attempt to model every possible software-engineering concept.

Start with evidence types required by the implemented skills.

Likely initial evidence types include:

* `change_frequency`
* `churn`
* `temporal_coupling`
* `complexity`
* `ownership`
* `static_dependency`
* `test_coverage`

Add others only when justified by an actual capability.

Avoid creating a large ontology or framework prematurely.

## 13.3 Common Evidence Envelope

Define a versioned evidence schema.

A conceptual starting point is:

```json
{
  "schema_version": 1,
  "type": "...",
  "subject": {},
  "metrics": {},
  "provenance": {}
}
```

This exact schema is not mandatory if implementation/testing reveals a better design.

However, every deterministic observation should communicate at least:

* what was observed
* what repository entity or entities it concerns
* quantitative/raw evidence where applicable
* where the evidence came from
* enough provenance to determine validity

## 13.4 Subjects

Evidence should identify its subject explicitly.

Possible subject types include:

* repository
* component
* directory
* file
* symbol
* file pair
* component pair

Example:

```json
{
  "type": "change_frequency",
  "subject": {
    "type": "file",
    "path": "src/billing/invoice.ts"
  },
  "metrics": {
    "revisions": 83
  }
}
```

Another example:

```json
{
  "type": "temporal_coupling",
  "subject": {
    "type": "file_pair",
    "paths": [
      "src/orders/order.ts",
      "src/billing/invoice.ts"
    ]
  },
  "metrics": {
    "shared_commits": 31,
    "coupling": 0.72
  }
}
```

Use stable repository-relative identifiers where practical.

## 13.5 Provenance Is Mandatory

Every evidence observation must contain enough provenance to answer:

> Where did this fact come from?

and:

> Is this evidence still valid for the current repository state?

Relevant provenance may include:

* provider/tool
* provider version
* repository identity
* Git HEAD
* dirty working-tree state
* relevant file hashes
* analysis parameters
* generation timestamp
* analysis/schema version

Example:

```json
{
  "schema_version": 1,
  "type": "temporal_coupling",
  "subject": {
    "type": "file_pair",
    "paths": [
      "src/orders/order.ts",
      "src/billing/invoice.ts"
    ]
  },
  "metrics": {
    "shared_commits": 31,
    "coupling": 0.72
  },
  "provenance": {
    "provider": "code-maat",
    "provider_version": "...",
    "repository_head": "a84f391",
    "dirty": false,
    "parameters": {
      "...": "..."
    }
  }
}
```

Do not blindly require every possible provenance field for every analysis.

Define validity according to the inputs on which that evidence depends.

## 13.6 Observation vs Interpretation

The evidence contract should primarily contain **observations**.

Good:

```text
revisions = 83
churn = 4773
complexity = 47
shared_commits = 31
temporal_coupling = 0.72
```

Bad:

```text
technical_debt = true
architecture_quality = bad
should_refactor = true
problematic_component = true
```

Those are semantic interpretations.

Maintain this boundary:

```text
DETERMINISTIC OBSERVATION
          ↓
    evidence contract
          ↓
   filtering/ranking
          ↓
selective source inspection
          ↓
    Codex reasoning
          ↓
 semantic interpretation
```

A deterministic tool may emit its own classifications when that is part of the tool's defined output, but preserve them as **tool output**, not Codebase Intelligence conclusions.

## 13.7 Provider Independence

Skills should consume evidence capabilities rather than depend directly on one tool.

Example:

```text
        Historical Analysis
                │
       ┌────────┴────────┐
       │                 │
   Code Maat        Git fallback
       │                 │
       └────────┬────────┘
                ↓
       normalized evidence
                ↓
       codebase-coupling
```

Both providers should produce semantically compatible evidence where possible.

For example, Code Maat and a local Git-history adapter might both provide `temporal_coupling`.

The consuming skill should not require substantially different reasoning merely because the provider changed.

## 13.8 Preserve Metric Semantics

Do not normalize metrics in ways that change their meaning.

If two tools define `coupling`, `complexity`, `churn`, or another metric differently, preserve those definitions.

Record where necessary:

* provider
* metric definition
* parameters
* units
* range

Do not pretend differently defined metrics are directly equivalent.

Provider-independent evidence means compatible semantics, not merely identical field names.

## 13.9 Evidence Store

Design a lightweight evidence store capable of holding valid normalized observations.

Conceptually:

```text
             deterministic analysis
                      │
                      ▼
                Evidence Store
                      │
          ┌───────────┼───────────┐
          ▼           ▼           ▼
       hotspots    coupling    future skills
```

The evidence store should allow a skill to determine things such as:

* Do valid temporal-coupling observations already exist?
* Is complexity evidence available for these candidates?
* Which provider produced an observation?
* Is the observation stale?

Do not require a database unless there is a compelling reason.

Simple structured files may be preferable.

## 13.10 Cross-Skill Reuse

Valid evidence should be reusable between skills.

For example, `codebase-hotspots` may generate:

* change frequency
* churn
* temporal coupling
* ownership

Later, `codebase-coupling` should reuse valid temporal-coupling evidence rather than recompute it.

Never reuse evidence merely because a file with the expected name exists.

Validate provenance first.

## 13.11 Query and Filter Before Source Inspection

The evidence layer should support cheap filtering and ranking before Codex reads source.

Example:

```text
4,000 source files
       ↓
deterministic metrics
       ↓
candidate ranking
       ↓
12 interesting files
       ↓
Codex inspects those files
```

This is one of the principal token-economy mechanisms of the suite.

Do not dump huge evidence datasets into Codex context.

Prefer deterministic querying, filtering, and aggregation first.

## 13.12 Component-Level Aggregation

Raw evidence may exist at file level while a skill needs subsystem-level reasoning.

Where useful:

```text
file observations
      ↓
directory/component mapping
      ↓
component observations
```

Do not invent architectural components solely from directory names.

Component boundaries should come from evidence such as:

* repository structure
* build/module definitions
* manifests
* architecture configuration
* source inspection
* explicit user-provided boundaries

Label inferred boundaries appropriately.

## 13.13 Evidence and Verification

The evidence contract should support verification.

For example:

```text
Claim:
Billing and Reporting are temporally coupled.

        ↓

locate temporal-coupling evidence
        ↓
validate provenance
        ↓
inspect metric/provider semantics
        ↓
confirm or reject claim
```

For deterministic claims, prefer deterministic evidence over asking Codex to reconstruct the fact from scratch.

## 13.14 Raw Output Retention

Where useful and reasonably inexpensive, retain or reference the raw tool output from which normalized evidence was derived.

This can help with:

* debugging adapters
* verifying normalization
* understanding unusual metrics
* reproducing analyses

Do not put large raw outputs into Codex context unless necessary.

Normalized evidence should normally be sufficient.

## 13.15 Schema Versioning

The evidence contract must be versioned.

Adapters, caches, and skills should detect incompatible schema versions.

Do not silently interpret incompatible evidence.

Prefer simple migration or recomputation over complex compatibility machinery at this stage.

## 13.16 Deterministic Adapters

Implement small deterministic adapters where useful.

Example:

```text
Code Maat CSV
      ↓
Code Maat adapter
      ↓
Evidence v1
```

or:

```text
git log
   ↓
Git-history adapter
   ↓
Evidence v1
```

Adapters should:

* parse tool output
* preserve metric semantics
* attach provenance
* validate required fields
* produce normalized evidence
* fail clearly on malformed or unexpected output

Adapters should not perform semantic architectural judgment.

## 13.17 Evidence Contract Acceptance Criteria

The evidence architecture is successful if:

1. Investigation skills do not need to understand arbitrary raw tool output.
2. Multiple providers can supply compatible evidence types.
3. Tool-specific metric semantics are preserved.
4. Evidence contains enough provenance to validate reuse.
5. Stale evidence is not silently consumed.
6. Skills can reuse evidence generated by other skills.
7. Large evidence datasets can be filtered without injecting all of them into Codex context.
8. Deterministic observations remain distinct from LLM interpretations.
9. New tools can be integrated primarily by writing adapters.
10. New investigation skills can consume existing evidence without requiring changes to every provider.
11. The schema remains deliberately small and understandable.
12. The implementation does not become a framework larger than the problem it solves.

---

# 14. Cache and Provenance

Deterministic analyses may be cached.

However:

> **Never use cached analysis without validating its provenance.**

The cache/provenance implementation must integrate with the machine-readable evidence contract.

Treat the evidence store and cache as related concepts:

```text
Evidence Store
    = observations + provenance

Cache
    = mechanism allowing valid observations to be reused
```

Do not create separate competing representations for cached analysis and normalized evidence.

Cache metadata should contain enough information to determine validity.

Consider:

* repository identity
* Git HEAD
* dirty working tree
* relevant file hashes where appropriate
* provider/tool name
* provider/tool version
* analysis parameters
* schema version
* generation time

Different analyses may have different invalidation requirements.

For example, Git-history evidence for committed history at `HEAD` may remain valid while static-analysis evidence can be invalidated by uncommitted source changes.

Design cache validity around **input provenance**, not merely age.

Prefer ephemeral cache/evidence storage.

Do not unnecessarily modify or pollute the target repository.

Generated human documentation should remain separate from machine-analysis cache.

---

# 15. Cross-Skill Composition

Skills may identify opportunities for another skill.

However:

> **Do not silently switch into another expensive analysis.**

Recommend the relevant skill to the user.

Examples:

`codebase-hotspots` discovers unexplained temporal coupling:

> This relationship may warrant `codebase-coupling`.

`codebase-coupling` identifies a suspicious subsystem:

> `codebase-deep-dive` can investigate this subsystem.

`codebase-architecture` identifies potentially stale architecture documentation:

> `codebase-verify` can audit that document.

The user decides whether to invoke the additional skill.

---

# 16. codebase-onboarding

## Goal

Help a competent developer become productive in an unfamiliar repository quickly.

Focus on:

* what the project does
* repository map
* architecture mental model
* core abstractions
* entry points
* important data/control flows
* persistence/state
* external systems
* configuration
* tests
* development workflow
* important extension points
* suggested source reading order

Prefer mental models over file listings.

Do not attempt exhaustive source analysis unless necessary.

Optimize for useful shallow-to-medium understanding.

This is primarily a **source-first** skill.

---

# 17. codebase-tutorial

## Goal

Generate a progressive, developer-friendly tutorial inspired by the best ideas in PocketFlow Codebase Knowledge.

Inspect PocketFlow before implementation.

Retain useful ideas such as:

* identifying approximately 5–10 core abstractions
* teaching concepts rather than files
* pedagogical ordering
* explaining WHY before HOW
* analogies where useful
* real file/symbol references
* concise code excerpts
* Mermaid diagrams
* cross-links
* progressive chapters
* suggested source reading order

Improve the workflow with:

* evidence tracking
* explicit source verification
* diagram verification
* unsupported-claim detection

Do not blindly reproduce PocketFlow's implementation.

This is primarily a **source-first** skill.

---

# 18. codebase-architecture

## Goal

Develop an evidence-backed mental model of the system architecture.

Analyze:

* system boundaries
* components/subsystems
* entry points
* dependencies
* communication patterns
* state/data stores
* external integrations
* major data/control flows
* architectural boundaries
* extension points

Use source-first semantic exploration.

Do not assume static dependency graphs equal architecture.

Static tools may support the analysis where useful, but should not dominate the reasoning.

Use diagrams where they improve understanding.

Verify meaningful diagram edges.

---

# 19. codebase-trace

## Goal

Trace a specific behavior through the implementation.

Examples:

* authentication
* `POST /api/orders`
* webhook processing
* background-job execution

Trace where relevant:

```text
entry point
    ↓
dispatch/routing
    ↓
business logic
    ↓
dependencies
    ↓
persistence/external systems
    ↓
side effects
    ↓
response/result
```

Reference actual files and symbols.

Verify each important transition.

Sequence diagrams are encouraged when appropriate.

Stay focused on the requested behavior.

---

# 20. codebase-deep-dive

## Goal

Understand one subsystem or concept in depth.

Analyze where relevant:

* responsibility
* public boundary/API
* internal implementation
* lifecycle
* state
* callers
* dependencies
* downstream effects
* failure handling
* concurrency
* tests
* extension points
* important design decisions
* edge cases

Stay focused on the requested subsystem.

Do not unnecessarily analyze unrelated repository areas.

---

# 21. codebase-change

## Goal

Determine how a requested change would likely be implemented.

Do **not modify code unless explicitly requested**.

Analyze:

* current behavior
* relevant architecture
* extension points
* affected files/symbols
* likely changes
* API/schema implications
* persistence implications
* compatibility concerns
* tests
* migration concerns
* side effects
* risks
* implementation sequence

Clearly distinguish:

* verified impact
* likely/inferred impact

This skill should help the user plan and understand a change before implementation.

---

# 22. codebase-hotspots

## Goal

Identify likely technical-debt and maintenance hotspots using repository-history analysis plus selective source inspection.

This is primarily **tool-first**.

When available and appropriate, consider Code Maat or equivalent behavioral/evolutionary analysis.

Useful signals include:

* change frequency
* churn
* complexity
* temporal coupling
* contributor patterns
* ownership concentration
* defect/fix patterns where reliable evidence exists
* frequently co-changing components

Important:

> **Frequent change does not imply technical debt.**

Historical analysis identifies **candidates**.

Codex must selectively inspect candidate source before interpreting why a candidate may be problematic.

Investigate possible causes such as:

* excessive responsibility
* high coupling
* unclear boundaries
* duplicated logic
* complex control flow
* large change surface
* fragile tests
* missing tests
* repeated fixes
* configuration complexity
* legacy compatibility
* boundary violations
* ownership/knowledge concentration

Do not recommend rewrites solely from quantitative metrics.

Prefer ranking/filtering candidates before source inspection.

Output should distinguish among:

* strong technical-debt evidence
* maintenance hotspots worth investigating
* high-change areas that appear healthy
* insufficient-evidence candidates

For significant candidates, report where useful:

* historical evidence
* source evidence
* why it may be a hotspot
* evidence status
* possible maintenance implication
* confidence/uncertainty

---

# 23. codebase-coupling

## Goal

Discover and explain coupling using static, evolutionary, logical/domain, and test evidence.

This is primarily **tool-first**.

Analyze where relevant:

1. Static coupling.
2. Temporal/evolutionary coupling.
3. Logical/domain coupling.
4. Test coupling.

## 23.1 Static Coupling

May include:

* imports
* calls
* inheritance
* interface implementation
* shared models
* shared configuration
* shared state
* APIs
* messages/events

## 23.2 Temporal Coupling

Use Code Maat or equivalent Git-history analysis where useful.

Identify files/components that repeatedly change together.

Treat this as evidence requiring investigation, not proof of bad design.

## 23.3 Static vs Temporal Coupling

Pay particular attention to mismatches.

Example:

```text
Static:

Orders ───→ Pricing


Temporal:

Orders ←──→ Pricing
Orders ←──→ Reporting
```

Orders/Pricing may be expected.

Orders/Reporting deserves investigation if the source architecture does not explain the relationship.

## 23.4 Hidden Coupling

Investigate unexplained temporal coupling for:

* duplicated knowledge
* duplicated constants
* duplicated validation
* duplicated business rules
* implicit contracts
* schema assumptions
* architectural leakage
* missing abstractions
* cross-module coordination

Do not assume hidden coupling is necessarily problematic.

## 23.5 Test Coupling

Consider relationships introduced or revealed through:

* shared fixtures
* mocks
* integration setup
* test helpers
* coordinated production/test changes

## 23.6 Component-Level Analysis

Prefer meaningful subsystem/component analysis over huge file-pair lists where possible.

Aggregate evidence according to actual repository boundaries.

Do not invent components solely for convenience.

## 23.7 Coupling Evidence

For important relationships, capture where useful:

* component/file A
* component/file B
* coupling type
* historical evidence
* source evidence
* likely explanation
* architectural status:

  * expected
  * potentially hidden
  * unclear
* evidence status
* maintenance implications

## 23.8 Coupling Matrix

When useful, produce a compact matrix such as:

```text
             Auth  Users  Billing  Reporting

Auth           -    S/T      -        -
Users         S/T    -       -        -
Billing        -     -       -        T
Reporting      -     -       T        -
```

Legend:

* `S` = static
* `T` = temporal
* `L` = logical/domain
* `X` = test

Use combinations where appropriate.

Every meaningful coupling edge must have evidence.

---

# 24. codebase-verify

## Goal

Audit an existing explanation, architecture document, tutorial, diagram, or technical claim against the current repository.

Extract material claims.

For each claim determine where appropriate:

* `VERIFIED`
* `INFERRED`
* `UNKNOWN`
* `CONTRADICTED`

Use deterministic checks where possible.

Examples:

```text
"Class X exists"
    ↓
deterministic source/symbol check
```

```text
"Module A imports B"
    ↓
deterministic/static check
```

```text
"Request flows from A to B to C"
    ↓
source inspection / call tracing
```

```text
"These modules are architecturally independent"
    ↓
semantic investigation
```

For diagrams, verify nodes and meaningful edges.

Report contradictions clearly.

Do not silently rewrite the artifact unless requested.

---

# 25. Tool-First Token Economy

For `codebase-hotspots` and `codebase-coupling` especially, avoid:

```text
read thousands of source files
        ↓
ask Codex to infer patterns
        ↓
discover candidates
```

Prefer:

```text
deterministic repository analysis
        ↓
machine-readable evidence
        ↓
deterministic query/filter/rank
        ↓
small relevant evidence set
        ↓
selective source inspection
        ↓
semantic reasoning
```

Do not inject complete raw analysis outputs or entire evidence datasets into Codex context when deterministic filtering can narrow them first.

Use Codex tokens where they provide the highest marginal value.

---

# 26. Deterministic Helpers

Create helper scripts where deterministic checks materially improve accuracy or token economy.

Potential responsibilities include:

* repository metadata
* Git-history extraction
* cache validation
* normalized tool-output conversion
* evidence-schema validation
* reference verification
* symbol/path validation
* analysis provenance
* candidate ranking
* evidence querying/filtering

Do not over-engineer.

Do not unnecessarily reproduce mature open-source tools.

Small adapters around established tools are preferable to implementing complex analysis from scratch.

---

# 27. Security and Privacy

Assume repositories may be private.

Prefer local tools.

Do not upload source to external services without explicit user intent and permission.

When recommending tools, identify whether they require sending:

* source code
* repository metadata
* Git history
* analysis results

to an external service.

Prefer offline/open-source alternatives where practical.

---

# 28. Output Style

Assume the user is a competent developer unless requested otherwise.

Prefer:

* mental models
* diagrams
* evidence
* relevant source paths
* relevant symbols
* concise excerpts
* actionable explanations

Avoid:

* giant file inventories
* dumping source
* unsupported architectural narratives
* generic software-engineering advice unrelated to evidence
* pretending quantitative metrics imply semantic conclusions

---

# 29. Validation Scope

Validate the implementation of the skill suite itself.

Do **not** clone, download, or obtain external repositories for testing.

Do **not** create test repositories outside this project.

The user will perform real-world evaluation of the completed skills separately against repositories of their choosing.

## 29.1 In-Repository Validation

Where deterministic infrastructure needs testing, create small, purpose-built fixtures or temporary repositories within the project's test environment.

Examples include testing:

* Git-history extraction
* temporal-coupling calculations
* churn calculations
* evidence normalization
* evidence-schema validation
* provenance recording
* cache reuse
* cache invalidation
* dirty-working-tree handling
* shallow-history detection
* malformed tool output
* provider adapters
* fallback behavior
* path/reference verification

Fixtures should be:

* small
* deterministic
* purpose-built
* easy to understand
* reproducible

Do not create large artificial codebases merely to simulate real-world skill usage.

## 29.2 Skill Structure Validation

Validate where possible that:

* every requested skill exists
* every skill follows current Codex Agent Skills conventions
* supporting references/scripts resolve correctly
* progressive disclosure is used appropriately
* unrelated instructions are not unnecessarily duplicated
* shared infrastructure is accessible as intended
* invocation documentation is correct

## 29.3 Validation Limits

Do not claim that the semantic quality of:

* `codebase-onboarding`
* `codebase-tutorial`
* `codebase-architecture`
* `codebase-trace`
* `codebase-deep-dive`
* `codebase-change`
* `codebase-hotspots`
* `codebase-coupling`
* `codebase-verify`

has been validated on real-world repositories unless such testing was actually performed.

Explicitly identify real-world repository evaluation as a remaining manual validation step.

---

# 30. Deterministic Failure-Path Testing

Where applicable to infrastructure implemented in this repository, test behavior for:

1. Recommended tool available.
2. Recommended tool absent.
3. User declines optional tool installation.
4. Insufficient Git history.
5. Shallow Git history.
6. Dirty working tree.
7. Repository without Git history.
8. Unsupported or unusual language.
9. Malformed external-tool output.
10. Provider/tool version change.
11. Evidence schema mismatch.

The implementation should degrade gracefully.

Never fabricate unavailable metrics.

Tests should not require fetching external repositories.

---

# 31. Cache Invalidation Testing

Where caching is implemented, test:

1. Analysis at commit A.
2. Reuse at commit A.
3. Repository moves to commit B.
4. Evidence invalidates where appropriate.
5. Dirty working-tree changes.
6. Tool-version changes.
7. Analysis-parameter changes.
8. Evidence-schema changes.

Document the invalidation model.

---

# 32. Documentation

Create documentation for the suite covering:

* purpose
* installation
* skill list
* invocation
* examples
* source-first vs tool-first vs evidence-first analysis
* evidence statuses
* deterministic-tooling philosophy
* machine-readable evidence contract
* optional tool installation
* fallbacks
* caching/provenance
* privacy
* limitations

Include a quick-reference section conceptually similar to:

```text
Want to understand the project?
    → codebase-onboarding

Want a structured learning guide?
    → codebase-tutorial

Want the system architecture?
    → codebase-architecture

Want to follow one behavior?
    → codebase-trace

Want to understand one subsystem deeply?
    → codebase-deep-dive

Want to plan a modification?
    → codebase-change

Want to find maintenance/technical-debt candidates?
    → codebase-hotspots

Want to understand hidden/change coupling?
    → codebase-coupling

Want to check documentation/claims against reality?
    → codebase-verify
```

Use the actual invocation syntax supported by current Codex conventions.

---

# 33. Extensibility

Design the suite so additional investigation skills can be added later.

Potential future capabilities might include:

* `codebase-knowledge`
* `codebase-complexity-trends`
* `codebase-code-age`
* `codebase-defects`
* `codebase-dependencies`
* `codebase-dead-code`
* `codebase-duplication`
* `codebase-test-health`
* `codebase-boundaries`
* `codebase-debt`

Do **not** implement these merely because they are listed here.

They demonstrate that the architecture should be extensible.

Avoid premature abstraction.

Future skills should be able to reuse existing evidence types where appropriate.

For example, a future knowledge/ownership analysis might reuse:

* ownership evidence
* change-frequency evidence
* temporal-coupling evidence

rather than building an independent analysis pipeline from scratch.

---

# 34. Overall Acceptance Criteria

The implementation is successful if:

1. Each requested capability is an independently invokable skill.
2. Skills do not unnecessarily load unrelated instructions.
3. Shared infrastructure avoids significant duplication.
4. Source-first skills primarily use semantic repository exploration.
5. Tool-first skills use deterministic analysis to reduce unnecessary Codex source inspection.
6. Missing optional tools do not make the suite unusable.
7. External tools are never silently installed.
8. Tool recommendations are explained before requesting permission.
9. Language-independent fallbacks exist.
10. Ecosystem-specific tooling can improve analysis.
11. Cached results cannot silently become stale.
12. Important claims are evidence-backed.
13. Verification can catch invalid source references.
14. Diagrams should not contain unsupported meaningful edges.
15. Hotspot metrics are not automatically labeled technical debt.
16. Temporal coupling is not automatically labeled bad architecture.
17. Skills recommend complementary skills rather than silently invoking expensive additional analyses.
18. Private repositories can be analyzed without requiring source upload to third-party services.
19. The suite is designed for both unfamiliar-repository exploration and investigation of actively maintained repositories.
20. The implementation follows current Codex Agent Skills conventions.
21. Investigation skills share a versioned machine-readable evidence contract.
22. Deterministic observations remain separate from semantic conclusions.
23. Tool adapters preserve provenance and metric semantics.
24. Valid evidence can be reused across skills.
25. Evidence can be deterministically filtered before large datasets enter Codex context.
26. Adding a new analysis provider generally requires an adapter rather than rewriting consuming skills.
27. Adding a new investigation skill can reuse existing evidence types without requiring changes to existing providers.
28. The evidence contract remains small and understandable.
29. Shared infrastructure does not become an unnecessary framework.
30. Real-world semantic validation is clearly left to subsequent user testing rather than falsely claimed.

---

# 35. Critical Final Review

After implementation, perform a critical review.

Specifically look for:

* instructions that waste tokens
* duplicated instructions
* excessive source reading
* unnecessary LLM reasoning that could be deterministic
* deterministic analysis that harms semantic accuracy
* fragile tool assumptions
* stale-cache risks
* missing provenance
* overly broad skills
* opportunities for progressive disclosure
* unsupported claims
* installation friction
* overly complicated evidence schemas
* unnecessary framework-building
* tool-specific assumptions leaking into consuming skills
* large deterministic outputs unnecessarily entering Codex context

Improve the implementation before presenting it.

---

# 36. Final Deliverable

When finished, provide:

1. Final file/directory tree.
2. Explanation of the architecture.
3. List of all created skills.
4. Invocation example for every skill.
5. Shared-infrastructure explanation.
6. Evidence-contract design.
7. Deterministic tools used or recommended and why.
8. Language-independent fallback behavior.
9. Ecosystem-specific extension mechanism.
10. Cache/provenance strategy.
11. Verification strategy.
12. In-repository tests performed.
13. Problems discovered during validation.
14. Changes made as a result of validation.
15. Known limitations.
16. Manual real-world tests the user should perform next.
17. Comparison with:

    * PocketFlow Codebase Knowledge
    * `rowlando/codebase-tutorial`
18. Important design decisions the user should review.
19. Suggestions for the next three highest-value additions to the suite.

Do **not** implement those suggested future additions yet.

---

# 37. Implementation Attitude

Treat this as building a reusable developer tool, not as generating a collection of prompt files.

Follow this sequence:

```text
RESEARCH
   ↓
DESIGN
   ↓
IMPLEMENT
   ↓
VALIDATE
   ↓
CRITIQUE
   ↓
REVISE
   ↓
DOCUMENT
```

Do not stop after producing plausible-looking `SKILL.md` files.

The final result should exploit the complementary strengths of:

```text
deterministic tools
        +
Git history
        +
static analysis
        +
targeted source inspection
        +
Codex semantic reasoning
        +
evidence-backed verification
```

while minimizing unnecessary token consumption.

The central architectural principle remains:

> **Use deterministic analysis to cheaply establish facts and narrow the search space. Use Codex where semantic understanding adds value.**

And the central evidence principle is:

> **Observations are not conclusions.**

A high change frequency is an observation.

Strong temporal coupling is an observation.

High complexity is an observation.

Low coverage is an observation.

Whether those observations indicate technical debt, an architectural problem, healthy complexity, or an expected relationship requires appropriate investigation and evidence.

Build the suite accordingly.

