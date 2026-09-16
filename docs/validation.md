# V3 validation

`make test` runs the deterministic helper suite in `tests/test_history_candidates.py`. It constructs only temporary local Git repositories and fake Code Maat executables. The suite maps all 40 normative helper areas in `SPEC-V3.md` to assertions covering Git history, physical LOC, filtering, bulk quality, renames/deletions, ranking, temporal coupling, provenance, errors, CSV validation, executable invocation/fallback, structural output, and explicit output files.

`make validate` checks the exact nine skills, frontmatter, explicit-only policies, equivalent portable/compatibility manifest skill exposure, local links, shared-reference loading, obsolete V2 references/commands, and unfinished placeholders.

The manual instruction review confirms bounded scope, distinct adjacent skills, source-first behavior, permission-gated optional tooling, semantic (not lexical) verification, and that historical candidates are not conclusions. Real Code Maat, Java, Docker, network access, external repositories, and real-world semantic evaluation are intentionally not run; actual Code Maat runtime compatibility and validation in a target repository remain user validation activities.

## Deterministic 40-area matrix

| Areas | Exact test and assertion |
|---|---|
| 1, 12–14 | `test_hotspot_count_rank_order_limit_and_provenance`: revision counts, dense ranks, ordering, totals, truncation, result-level provenance. |
| 2 | `test_physical_loc_and_symlink_safety`: blanks, final-newline behavior, empty, binary exclusion, outside symlink exclusion. |
| 3–4, 18 | `test_default_and_explicit_filters_keep_tests`: all default path classes, repeatable globs, test-path eligibility. |
| 5–7 | `test_bulk_excludes_hotspot_and_temporal_metrics`: hotspot/temporal exclusion, endpoint support, ratios, limitation codes. |
| 8–11 | `test_rename_deletion_and_include_deleted`: multi-step rename/current mapping, ordinary deletion accounting, deleted-policy result. |
| 15–17 | `test_temporal_formula_order_and_exact_subject`: shared counts, endpoint revisions, coupling, support ordering, exact subject matching. |
| 19–21 | `test_history_quality_limitations_and_empty_insufficient`: shallow, insufficient, low-sample, and short-span limitations. |
| 22, 39 | `test_provenance_dirty_scope_and_parameters`: dirty state, input scope, validity-critical parameters, no candidate provenance. |
| 23–25 | `test_operational_git_failures_are_structured`: empty Git, non-Git, and missing Git errors. |
| 26–31 | `test_csv_validation_support_semantics_hashes_and_filters`: native CSV metrics, percentage/support fields, validation failures, SHA-256, mismatch code, imported limitations. |
| 32–35, 37 | `test_executable_filtering_support_and_provider_behavior`: fake executable, filtered input, optional support and threshold, direct command execution, auto fallback, explicit failure, CSV-before-command precedence, clean stdout. |
| 36, 38 | `test_argument_and_structured_output_errors`: conflicts, usage exit 2, operational structured output-path error. |
| 40 | `test_output_file_matches_stdout`: explicit output content equals stdout. |
