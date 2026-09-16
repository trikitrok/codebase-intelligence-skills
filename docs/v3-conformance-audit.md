# Codebase Intelligence V3 Conformance Audit

## Executive assessment

V3 is not conformant with `SPEC-V3.md`.

The Git fallback, basic CSV parsing, bounded schemas, explicit skill policies, and most shared-reference cleanup are present. However, several normative requirements fail in executable Code Maat mode, temporal insufficient-history handling, symlink exclusion, structured error handling, provenance completeness, and migration/documentation accuracy.

The required helper test coverage is substantially incomplete: 7 of 40 areas have meaningful coverage; the remainder are missing or only weakly exercised.

No repository files were modified during the audit itself.

## 1. Normative requirement findings

### PASS — structure and boundaries

- Nine skill directories exist: `skills/*`.
- All nine agent manifests contain `allow_implicit_invocation: false`.
- The helper exists at `shared/scripts/history_candidates.py`.
- Exactly two product subcommands are exposed: `hotspots` and `temporal-coupling`.
- No V2 helper or obsolete shared-reference files remain in the working tree.
- No persistent cache, generic provider registry, evidence ontology, lexical verifier, architecture graph, call graph, or semantic debt classifier remains in the current implementation.
- All skills link to `analysis-basics.md`; only hotspots and coupling link to `history-analysis.md`.
- The helper uses Python standard-library modules plus local Git for built-in analysis.
- The helper does not install, download, or contact remote services.

Evidence: `scripts/validate_suite.py:8-45`, `skills/*/SKILL.md`, `shared/scripts/history_candidates.py:1-18`.

### PASS — basic CLI contract

The parser implements the specified command names and common options, including limits, history bounds, exclusions, rename threshold, output path, provider selection, and Code Maat options.

Evidence: `shared/scripts/history_candidates.py:291-311`.

The JSON-array Code Maat command is passed directly to `subprocess.run`, without a shell.

Evidence: `shared/scripts/history_candidates.py:201-215`.

### FAIL — insufficient-history result handling

Section 14.3 requires an empty candidate list whenever fewer than two eligible commits remain.

The hotspot path enforces this, but temporal coupling does not:

```python
candidates = []
...
for (left,right), shared in pairs.items():
    if shared >= args.min_shared_commits:
        candidates.append(...)
```

Evidence: `shared/scripts/history_candidates.py:162-177`.

Audit probe:

```text
ONE_COMMIT_TEMPORAL 0
[{"paths":["a","b"],"shared_commits":1,...}]
history_quality.limitations = [{"code":"INSUFFICIENT_HISTORY",...}]
```

Thus the helper emits a non-empty temporal result while simultaneously declaring insufficient history.

### FAIL — executable Code Maat filtering and bulk policy

Section 13.2 requires executable mode to apply path, rename, current/deleted, history-window, and bulk policies before producing Code Maat input.

Executable mode writes raw `git log --name-status -z` output directly to the temporary input:

Evidence: `shared/scripts/history_candidates.py:210-215`.

It does not apply the Git canonical touch-set calculation, default exclusions, explicit exclusions, deleted-path policy, or bulk filtering. The executable result also reports zero bulk exclusions regardless of actual history.

A fake executable probe confirmed excluded content enters the Code Maat input:

```text
EXEC_INPUT_HAS_VENDOR True
```

Evidence: `shared/scripts/history_candidates.py:201-242`.

### FAIL — executable Code Maat input format is not demonstrated as Code Maat-compatible

The implementation produces NUL-delimited `--name-status` output:

```python
git(..., "log", "--name-status", "-z", ...)
```

The specification requires Code Maat-compatible Git input using current documented conventions. No deterministic test validates that the generated input is accepted by an actual-compatible executable; the fake executable only accepts the path.

Evidence: `shared/scripts/history_candidates.py:210-212`; missing test area 32.

### FAIL — executable coupling does not preserve optional provider fields

Section 11.3 requires preserving provider-supplied shared revisions, endpoint revisions, and average revisions when available.

Executable coupling mode only requests and parses `entity,coupled,degree` and always emits all support fields as `null`.

Evidence: `shared/scripts/history_candidates.py:233-240`.

It also always uses coupling-only ordering and always emits `CODE_MAAT_SUPPORT_FILTER_UNAVAILABLE`, even if an executable provides optional support columns.

### FAIL — executable coupling ignores `--min-shared-commits`

Because executable mode discards optional shared-support columns, it cannot apply the threshold when support is available.

Evidence: `shared/scripts/history_candidates.py:234-240`; `SPEC-V3.md:1008-1010`.

### FAIL — outside-repository symlinks remain hotspot candidates

The LOC function skips reading an outside symlink, but Git hotspot candidate construction still emits the path with size `0`.

Evidence:

- LOC skip: `shared/scripts/history_candidates.py:47-60`
- candidate construction: `shared/scripts/history_candidates.py:158-166`

Audit probe output included:

```text
LOC_PATHS [..., ("link", 0)]
```

Section 9.7 says outside-resolving symlinks are skipped, not emitted as zero-size candidates.

### FAIL — output-path failures are not structured errors

Section 14.2 requires operational failures to produce one JSON error object on stderr.

An output path pointing to an existing directory raises an uncaught `IsADirectoryError`:

```text
OUTPUT_DIRECTORY 1
IsADirectoryError: [Errno 21] Is a directory ...
```

Evidence: `shared/scripts/history_candidates.py:329-331`.

The error is neither converted to `INVALID_OUTPUT_PATH` nor emitted as structured JSON.

### PARTIAL — result validation

The specification requires minimal result validation, including numeric ranges and normalized paths.

CSV mode validates many inputs, but executable mode does not consistently validate duplicate entities, nonnegative revisions, nonnegative churn components, duplicate coupling pairs, optional support-field ranges, or provider output entities using the dedicated error codes.

Evidence: `shared/scripts/history_candidates.py:219-240`.

There is no general result-validation function.

### PARTIAL — CSV provenance parameters

CSV mode records hashes and explicit excludes, but omits several validity-critical parameters required by Section 12.2:

- `since`;
- `max_commits`;
- `max_changeset_size`;
- `rename_threshold`;
- default exclusions;
- low-sample thresholds;
- analysis-specific settings for hotspot mode.

Evidence: `shared/scripts/history_candidates.py:285`.

### PARTIAL — Code Maat executable history-quality metadata

Executable mode returns the required object shape, but does not calculate actual matched commits, eligible commits, history dates, bulk counts, exclusion counts, rename counts, or shallow state.

Evidence: `shared/scripts/history_candidates.py:231-232`, `:240`.

### PARTIAL — unresolved rename/deletion accounting

Rename chains work for the tested straightforward case, but every historical path absent from the current tree is counted as unresolved:

Evidence: `shared/scripts/history_candidates.py:145-153`.

This conflates ordinary historical deletions with unresolved rename/deletion mappings. No deterministic test distinguishes resolved rename, ordinary deletion, ambiguous rename/copy, and unresolved rename.

### PASS — Git hotspot ranking and ordering

The Git implementation computes revisions from eligible non-bulk touch sets, uses current physical LOC, applies dense ascending ranks, calculates ranks before limiting, and sorts by score, revisions, size, and path.

Evidence: `shared/scripts/history_candidates.py:157-168`.

### PASS — Git temporal formula and ordering

The implementation computes `shared / min(left_revisions, right_revisions)` and sorts by shared commits, coupling, and lexicographic paths.

Evidence: `shared/scripts/history_candidates.py:169-180`.

### PASS — default filtering implementation

The default component list and `.min.js` / `.map` suffix checks are implemented.

Evidence: `shared/scripts/history_candidates.py:18`, `:36-38`.

Broad deterministic coverage of every required exclusion is missing.

### PARTIAL — physical LOC and symlink semantics

The implementation uses byte reads, NUL detection, byte `splitlines()`, and skips outside symlink reads.

Evidence: `shared/scripts/history_candidates.py:47-60`.

The candidate-level symlink issue makes the overall symlink requirement only partial.

### PASS — result-level provenance shape

Provenance is emitted at result level, and candidates do not copy it.

Evidence: `shared/scripts/history_candidates.py:120-123`.

Candidate-level absence is not asserted by tests.

### PARTIAL — exit-code behavior

The intended mapping exists: `0` success, `1` `Failure`, and `2` usage errors.

Evidence: `shared/scripts/history_candidates.py:313-339`.

It is incomplete because uncaught filesystem errors escape as tracebacks, and malformed executable provider values can be classified as usage errors rather than operational/provider failures.

### PASS — explicit Code Maat failure does not silently fall back

Explicit provider failures re-raise instead of invoking Git.

Evidence: `shared/scripts/history_candidates.py:321-328`.

### PASS — automatic Code Maat failure fallback

For `--provider auto`, executable failure falls back to Git and appends `CODE_MAAT_FAILED_FALLBACK_GIT`.

Evidence: `shared/scripts/history_candidates.py:323-328`.

This behavior lacks the required deterministic test.

### PASS — CSV malformed input does not silently fall back

Explicit CSV errors propagate from `csv_provider`.

Evidence: `shared/scripts/history_candidates.py:244-289`.

The existing test checks a hotspot entity mismatch, but not the complete malformed-input matrix.

### PASS — shared references and skill runtime boundaries

The nine skills are concise, independently scoped, and contain stopping criteria and deliverable language.

Evidence: `skills/*/SKILL.md`.

### PARTIAL — Code Maat permission explanation

The references state that permission is required and mention dependencies, local/private processing, and Git fallback.

Evidence: `shared/references/history-analysis.md:16`.

The skills do not explicitly require a permission request containing all five explanation elements from Section 13.5.

### PASS — privacy and mutation behavior

The helper only writes an explicitly requested output path or temporary files. No network or installation behavior exists.

Evidence: `shared/scripts/history_candidates.py:210-242`, `:329-331`.

### PARTIAL — structural validation

` scripts/validate_suite.py` checks many required conditions, but it does not verify that both manifests expose the same nine skills. The root `plugin.json` contains no `skills` declaration, while `.codex-plugin/plugin.json` contains `"skills": "./skills/"`.

Evidence: `plugin.json`, `.codex-plugin/plugin.json`, `scripts/validate_suite.py:12-18`.

It also does not validate result schemas, CLI behavior, or the 40 helper test areas.

### FAIL — current runtime-audit documentation accuracy

`docs/runtime-audit.md` describes the V2 helper, cache, `core.md`, `codebase_intelligence.py`, `cache-status`, and old provider behavior as current implementation.

Examples: `docs/runtime-audit.md:15-30`, `:53-70`, `:234-293`.

Although the specification permits a historical runtime audit, it requires historical documents to clearly describe V2 in the past tense. This document is not clearly labeled as historical and contradicts current README/design documentation.

### PASS/PARTIAL — README and current design documentation

`README.md`, `docs/design.md`, and `docs/validation.md` generally describe the V3 architecture accurately.

However, `docs/validation.md:3` overstates coverage by saying the five tests cover categories that are only weakly or not at all asserted, especially symlink safety, bulk hotspot behavior, fake executable behavior, provider fallback, output files, and exit-code distinctions.

## 2. Required-test coverage matrix

| # | Required test area | Status | Existing test evidence |
|---:|---|---|---|
| 1 | Hotspot Git revision counting | PARTIAL | `test_rename_chain_and_deleted_include` asserts `revisions == 3`; no ordinary revision-count assertion |
| 2 | Physical LOC: blanks, newline, empty, binary, symlink | MISSING | No adequate assertions |
| 3 | Default generated/vendor/build/cache exclusions | PARTIAL | Vendor is indirectly filtered in `test_hotspots_loc_ties_limit_and_provenance`; other required classes absent |
| 4 | Repeatable explicit exclusions | MISSING | No test |
| 5 | Bulk excluded from hotspot revisions | MISSING | No hotspot bulk assertion |
| 6 | Bulk excluded from endpoint revisions and pairs | PASS | `test_temporal_bulk_and_subject_filter` |
| 7 | Bulk ratios and limitation codes | MISSING | Only count is asserted, not ratios/codes |
| 8 | Simple rename | MISSING | Only multi-step rename exists |
| 9 | Multi-step rename chain | PASS | `test_rename_chain_and_deleted_include` |
| 10 | Unresolved/deleted rename | MISSING | No actual unresolved/deleted rename fixture |
| 11 | `--include-deleted` | MISSING | Test name mentions deleted, but no deleted entity behavior is asserted |
| 12 | Dense tie-correct ranks | PARTIAL | One rank assertion; equal/minimum size and all-equal cases absent |
| 13 | Stable hotspot ordering | MISSING | No exact complete ordering assertion |
| 14 | Limit, total, count, truncation | PASS | `test_hotspots_loc_ties_limit_and_provenance` |
| 15 | Temporal shared commits and coupling | PARTIAL | Simple ratio asserted; denominator and endpoint counts not fully tested |
| 16 | Temporal support-first ordering | MISSING | Only one pair exists in the test |
| 17 | Exact subject filtering | PARTIAL | Positive subject case only; no exact-vs-prefix/nonmatch case |
| 18 | Tests remain eligible | MISSING | No test-path fixture |
| 19 | Shallow-history limitation | MISSING | No shallow repository fixture |
| 20 | Insufficient-history empty result | MISSING | Empty Git failure is tested, not insufficient-history success |
| 21 | Low-commit and short-span warnings | MISSING | No limitation-code assertions |
| 22 | Dirty-state and input-scope provenance | MISSING | Mode is tested; dirty state and scopes are not |
| 23 | Empty Git failure | PASS | `test_empty_and_non_git_are_structured_failures` |
| 24 | Non-Git failure | PASS | `test_empty_and_non_git_are_structured_failures` |
| 25 | Missing Git failure | MISSING | No PATH/tool-unavailable fixture |
| 26 | Native revisions/entity-churn CSV parsing | PARTIAL | CSV is parsed, but values and malformed numeric cases are not comprehensively asserted |
| 27 | Coupling CSV and percentage semantics | PASS | `test_csv_semantics_hashes_and_malformed` asserts `75` |
| 28 | CSV duplicate/missing/malformed/range/path failures | MISSING | Only one mismatch case is tested |
| 29 | CSV SHA-256 provenance | PARTIAL | Hash presence asserted, exact digest not checked |
| 30 | Hotspot entity mismatch | PARTIAL | Return code asserted, error code not asserted |
| 31 | CSV unverified-filter/rename limitations | MISSING | No limitation assertions |
| 32 | Fake executable, no shell | MISSING | No fake executable test |
| 33 | Auto-discovered Code Maat failure fallback | MISSING | No test |
| 34 | Explicit Code Maat failure | MISSING | No test |
| 35 | Provider selection order | MISSING | No precedence test |
| 36 | Argument conflicts and validation | MISSING | No dedicated validation tests |
| 37 | Clean JSON stdout with diagnostics | MISSING | No test |
| 38 | Exit codes and structured errors | PARTIAL | Exit 1/error JSON for Git failures only; no exit 2 or provider/output failures |
| 39 | Result-level provenance only | PARTIAL | Result provenance is checked; candidate absence is not |
| 40 | Output file matches stdout | MISSING | No test |

## 3. Implementation defects

1. Temporal coupling returns candidates with fewer than two eligible commits.
2. Executable Code Maat input bypasses required filtering, rename normalization, deleted-path policy, and bulk exclusion.
3. Executable Code Maat input format is not validated as compatible.
4. Executable coupling discards optional support fields and cannot apply support thresholds.
5. Outside-repository symlinks are emitted as zero-size candidates.
6. Output-path failures produce uncaught tracebacks instead of structured JSON.
7. Executable provider parsing lacks the same validation guarantees as CSV mode.
8. CSV provenance omits required validity-critical parameters.
9. Executable history-quality metadata is placeholder-like rather than calculated.
10. Unresolved-history accounting conflates ordinary deletions with unresolved rename mappings.
11. Structural validation does not verify equivalent skill exposure in both manifests.

## 4. Missing tests

The largest missing deterministic protections are:

- shallow repositories;
- insufficient history;
- simple/deleted/ambiguous renames;
- full exclusion matrix;
- symlink safety;
- bulk hotspot behavior;
- fake executable invocation;
- provider-selection precedence;
- automatic and explicit Code Maat failure;
- executable filtering and input construction;
- structured output-path/provider errors;
- exact subject filtering;
- output-file equality;
- support-first ordering with multiple candidates;
- complete CSV validation and provenance.

## 5. Documentation/spec discrepancies

### Documentation defects

- `docs/runtime-audit.md` presents obsolete V2 machinery as current.
- `docs/validation.md` claims broader test coverage than the assertions provide.
- The root `plugin.json` does not visibly expose the nine skills in the same way as `.codex-plugin/plugin.json`.
- Documentation does not describe the executable-mode limitations actually present.

### Intentional/spec-compliant limitations

These are not defects:

- semantic architecture, tutorial, trace, change-impact, static coupling, logical coupling, test coupling, and debt classification remain Codex-guided;
- no generic analyzer framework exists;
- no automatic semantic conclusion is produced from history metrics;
- no real-world semantic evaluation has been claimed.

## 6. Commands run

| Command | Result |
|---|---|
| `make test` | PASS — 5 tests passed |
| `make validate` | PASS |
| `python3 -m py_compile shared/scripts/history_candidates.py scripts/validate_suite.py` | PASS |
| `git diff --check` | PASS |
| `make validate-openai` | FAIL — required `SKILL_VALIDATOR` and `PLUGIN_VALIDATOR` variables are unset |
| `python3 shared/scripts/history_candidates.py --version` | PASS — `3.0.0` |
| Helper `--help` | PASS |
| Temporary one-commit temporal probe | FAIL — returned a candidate despite `INSUFFICIENT_HISTORY` |
| Temporary fake Code Maat executable probe | FAIL — vendor path appeared in executable input |
| Temporary output-directory probe | FAIL — uncaught `IsADirectoryError` |
| Temporary symlink/LOC probe | FAIL — outside symlink emitted as candidate |

No external repositories, Code Maat, Java, Docker, or network dependencies were used.

## 7. Prioritized remediation

### P0 — correctness failures

1. Enforce empty candidates for all analyses when eligible commits `< 2`.
2. Implement executable Code Maat preprocessing through the same canonical Git touch-set policy as Git fallback.
3. Preserve and validate executable coupling support fields.
4. Exclude outside-repository symlinks from candidate construction.
5. Convert output and provider exceptions into stable structured errors.

### P1 — contract completeness

6. Add complete provenance parameters for CSV and executable modes.
7. Separate ordinary deletions from unresolved rename mappings.
8. Validate executable output with the same rules as CSV input.
9. Make structural validation verify both manifests expose the same nine skills.
10. Document executable-mode behavior accurately.

### P2 — deterministic test coverage

11. Add the missing 33 test areas from the matrix, beginning with Code Maat fake-executable behavior, provider ordering/fallback, insufficient history, symlinks, renames, and structured errors.
12. Replace broad category claims in `docs/validation.md` with the exact tests and assertions that actually exist.
13. Mark `docs/runtime-audit.md` explicitly as historical V2 documentation or update it to describe only historical behavior.
