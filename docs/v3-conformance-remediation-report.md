# V3 Conformance Remediation Report

Date: 2026-09-16

## Outcome

The V3 implementation was remediated against `SPEC-V3.md`. All deterministic requirements covered by the specification are implemented and tested locally. No architecture change or specification weakening was made.

## Audit finding dispositions

| Audit finding | Disposition |
|---|---|
| Insufficient-history behavior | Fixed. Hotspots and temporal coupling now emit empty candidates when fewer than two eligible commits remain. |
| Executable Code Maat filtering and bulk policy | Fixed. Executable input uses canonical preprocessing for exclusions, history bounds, rename/current/deleted policy, and bulk commits. |
| Executable Code Maat input format | Fixed. Input uses the documented bracketed commit-header and numstat convention; fake executable tests inspect it. |
| Optional executable coupling support fields | Fixed. Shared revisions, endpoint revisions, and average revisions are preserved and validated. |
| `--min-shared-commits` with Code Maat | Fixed. The threshold applies when shared support exists; otherwise the required limitation is emitted. |
| Outside-repository symlink exclusion | Fixed. Such paths are omitted from hotspot candidates. |
| Structured operational/provider/output errors | Fixed. Failures emit one bounded JSON error object on stderr with stable codes. |
| Complete provenance | Fixed. History bounds, thresholds, exclusions, analysis settings, provider identity, and CSV hashes are recorded. |
| Executable-provider output validation | Fixed. Executable and CSV results share validation for paths, duplicates, numeric ranges, entities, and pairs. |
| Deletion versus unresolved rename accounting | Fixed. Ordinary deletions are not counted as unresolved renames; unresolved rename/deletion mappings are reported separately. |
| Plugin manifest parity and structural validation | Fixed. Both manifests expose `./skills/`, and validation checks equivalent exposure. |
| V2 runtime audit labeling | Fixed. `docs/runtime-audit.md` is explicitly labeled historical V2 documentation. |
| Validation documentation accuracy | Fixed. `docs/validation.md` documents the actual deterministic suite, exact 40-area coverage, and external-runtime limits. |

## Files changed for remediation

- `shared/scripts/history_candidates.py`
- `tests/test_history_candidates.py`
- `scripts/validate_suite.py`
- `plugin.json`
- `docs/validation.md`
- `docs/runtime-audit.md`

## Deterministic 40-area test matrix

| Areas | Exact test and assertions |
|---|---|
| 1, 12–14 | `test_hotspot_count_rank_order_limit_and_provenance`: revision counts, dense ranks, stable order, totals, truncation, result-level provenance. |
| 2 | `test_physical_loc_and_symlink_safety`: blanks, final-newline behavior, empty files, binary exclusion, outside symlink exclusion. |
| 3–4, 18 | `test_default_and_explicit_filters_keep_tests`: default generated/vendor/build/cache exclusions, repeatable explicit globs, test-path eligibility. |
| 5–7 | `test_bulk_excludes_hotspot_and_temporal_metrics`: hotspot and temporal exclusion, endpoint support, bulk ratios, limitation codes. |
| 8–11 | `test_rename_deletion_and_include_deleted`: simple and multi-step rename mapping, ordinary deletion, unresolved deleted rename, `--include-deleted`. |
| 15–17 | `test_temporal_formula_order_and_exact_subject`: shared counts, endpoint revisions, coupling formula, support-first ordering, exact subjects. |
| 19–21 | `test_history_quality_limitations_and_empty_insufficient`: shallow, insufficient, low-sample, and short-span limitations. |
| 22, 39 | `test_provenance_dirty_scope_and_parameters`: dirty state, input scope, validity-critical parameters, no candidate-level provenance. |
| 23–25 | `test_operational_git_failures_are_structured`: empty Git, non-Git, and missing Git errors. |
| 26–31 | `test_csv_validation_support_semantics_hashes_and_filters`: native CSV parsing, percentage/support semantics, malformed/duplicate/range/path failures, SHA-256 provenance, entity mismatch, imported limitations. |
| 32–35, 37 | `test_executable_filtering_support_and_provider_behavior`: fake executable, filtered input, optional support and threshold, direct no-shell invocation, automatic fallback, explicit failure, provider precedence, clean stdout. |
| 36, 38 | `test_argument_and_structured_output_errors`: argument conflicts, usage exit code 2, structured output-path failure. |
| 40 | `test_output_file_matches_stdout`: explicit output content matches stdout. |

The 40 areas are covered by 13 deterministic test functions. Tests use only temporary local Git repositories and temporary fake executables; they do not require Code Maat, Java, Docker, network access, or external repositories.

## Commands and exact results

| Command | Result |
|---|---|
| `make test` | PASS — 13 tests passed. |
| `make validate` | PASS — nine skills, manifests, links, reference loading, and contracted machinery validated. |
| `python3 -m py_compile shared/scripts/history_candidates.py scripts/validate_suite.py` | PASS. |
| `git diff --check` | PASS. |
| `python3 shared/scripts/history_candidates.py --version` | PASS — `3.0.0`. |
| `python3 shared/scripts/history_candidates.py --help` | PASS — only `hotspots` and `temporal-coupling` product commands exposed. |
| `make validate-openai` | Not available — `SKILL_VALIDATOR` and `PLUGIN_VALIDATOR` are unset. This is an unavailable external validation configuration, not an implementation failure. |

## Remaining requirements and limitations

No deterministic V3 requirement remains classified as `FAIL`, `PARTIAL`, `MISSING`, or `NOT TESTED`.

The following remain intentionally outside local deterministic validation:

- execution against a real Code Maat release and Java runtime;
- validation in real external repositories;
- network, Docker, or installation behavior;
- real-world semantic-quality evaluation of the nine skills.

These are user-validation activities explicitly permitted by `SPEC-V3.md`; the implementation does not claim to have performed them.

## Specification deviations

None identified. `SPEC-V3.md` remains normative and unchanged.
