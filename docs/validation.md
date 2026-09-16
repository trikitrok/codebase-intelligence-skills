# Validation record

Validation was limited to this repository and small temporary fixtures created under `tests/`. No external repository was cloned, downloaded, or analyzed as a test target.

## Automated checks

`make test` runs 20 test methods covering:

1. Git change-frequency, churn, ownership, and temporal-coupling normalization.
2. Evidence-schema validation and metric-definition retention.
3. The public cache CLI requiring an analysis provider and automatically comparing the Git request's parameters.
4. Git+LOC hotspot fallback, deterministic physical-LOC semantics, irrelevant-path exclusions, and change-frequency/size ranking.
5. LOC-input cache invalidation with a dirty working tree and invalidation after a new commit.
6. Analyzer-version and schema-version invalidation.
7. Code Maat version changes supplied by the current request, refusal to fall back to a cached version, and CSV/analysis parameter invalidation.
8. Code Maat native revisions/entity-churn hotspot composition without fallback LOC.
9. Observation/store provenance equality and repository-metadata consistency corruption failures.
10. Repository-relative file and file-pair subjects, including rejection by the Code Maat adapter.
11. Shallow and insufficient-history limitations.
12. An empty Git repository failure.
13. Code Maat coupling conversion and malformed CSV failure.
14. Deterministic query/filter/limit behavior.
15. Valid, missing, and escaping path/reference checks.
16. Unsupported language fallback and available/missing tool discovery.
17. Nested manifest discovery for monorepos.

`make validate` checks both plugin manifests, the exact nine-skill set, frontmatter names/descriptions, explicit-only policies, local Markdown links in skill entrypoints, and unfinished scaffold placeholders.

## Failure-path coverage

| Required path | Validation |
|---|---|
| Recommended tool available/absent | Tool discovery is tested with controlled available and missing commands. |
| User declines installation | Instruction-level fallback and permission policy is structurally reviewed; no installer exists to bypass it. |
| Insufficient/shallow history | Both limitations are fixture-tested. |
| Dirty working tree | Recorded and tested as a cache miss for Git+LOC evidence because current source is an input. |
| Repository without history | Empty Git repository failure is tested. |
| Unsupported language | Unknown-extension discovery and standard-library Git+LOC fallback are tested/documented. |
| Malformed provider output | Code Maat CSV failure is tested. |
| Provider, analyzer, parameter, provider-input, schema changes | Cache invalidation is tested through provider-specific analysis requests. |
| Corrupt provenance or repository subjects | Store/observation disagreement, repository metadata disagreement, and invalid file/file-pair paths are tested. |

No bundled path installs optional tools, so “declined” and “missing” converge on the documented language-independent fallback rather than separate executable branches.

## External development-time validators

`make validate` is fully checked in and does **not** claim to run OpenAI's development-environment validators. When those external scripts are installed, they can be incorporated reproducibly by supplying their paths:

```text
make validate-openai SKILL_VALIDATOR=/path/to/quick_validate.py PLUGIN_VALIDATOR=/path/to/validate_plugin.py
```

That target runs `quick_validate.py` against every skill and `validate_plugin.py` against this plugin root. The scripts are not vendored here, so their availability and behavior are development-environment checks rather than guarantees of the repository's normal `make validate` workflow.

For the 2026-09-16 verification recorded here, the target was run with the locally installed OpenAI validators: all nine skill validations and the plugin validation passed.

## Problems found and resulting changes

- The first fixture run failed on Python without `str.removeprefix`; parsing was changed to slicing for broader compatibility.
- A “non-Git directory” fixture under this repository inherited the parent Git root. It was replaced with an empty standalone Git repository inside the test directory, accurately testing Git-without-history while respecting the no-outside-test-repository constraint.
- Current official docs prefer portable root `plugin.json` while retaining `.codex-plugin/plugin.json`; the portable manifest was added without removing the compatibility fallback.

## Not validated here

No claim is made that semantic outputs are high quality on real repositories. Manual evaluation should cover multiple repository sizes and ecosystems, monorepos, shallow clones, unusual histories, generated-heavy repositories, stale architecture documents, and ambiguous runtime/framework wiring.
