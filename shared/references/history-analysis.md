# History analysis

Hotspots and coupling use `shared/scripts/history_candidates.py` relative to either skill:

```text
python3 shared/scripts/history_candidates.py hotspots [options]
python3 shared/scripts/history_candidates.py temporal-coupling [options]
```

`auto` selects valid supplied CSV, an explicit command, an exact `code-maat` executable, then Git. Git fallback uses bounded, rename-aware co-change history and current tracked physical LOC. Candidates are bounded observations, not semantic conclusions; inspect selected source and tests.

Git hotspot revisions count eligible non-bulk commits touching a path. Size is current physical LOC (blank lines count; final newline does not add a line). Score is the product of normalized ascending dense ranks for revisions and size. Git temporal coupling is shared eligible commits divided by the smaller endpoint revision count, with unit `ratio`. Code Maat hotspot size is absolute entity churn (`added + deleted`), and Code Maat coupling preserves provider `degree` as a percentage; neither is equivalent to the Git metrics.

Results include provider/version/mode, HEAD, dirty and input scope, parameters, bounded totals, and history-quality fields. Limitations may include shallow, insufficient, low-sample, short-span, bulk, unresolved-rename, and imported-input warnings. Bulk, rename, shallow-history, low-sample, generated/vendor, construction/import, bot, formatting, and migration confounders require selective interpretation; commit messages alone do not classify them.

Code Maat is optional and local/private. Do not install or configure it without explicit permission explaining its value, dependencies, data handling, and Git fallback. The helper has no cache, registry, generic provider SDK, or remote service.
