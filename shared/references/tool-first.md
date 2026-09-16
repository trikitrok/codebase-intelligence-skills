# Tool-first workflow

Use this workflow for hotspot and coupling investigations.

## Required sequence

1. Read [core.md](core.md) and run repository/tool discovery before source inspection beyond manifests and boundaries.
2. Check whether a compatible evidence store exists and validate it with `cache-status`, naming the intended provider and the same analysis parameters the current request would use. Never reuse a store merely because its filename matches.
3. If valid evidence is missing, use the standard-library Git provider first. Use Code Maat or another provider only when already available/configured or after installation permission.
4. Validate the evidence store. Record shallow or insufficient history; do not turn missing history into zero-valued metrics.
5. Query and rank a small candidate set before reading source. Do not place the entire evidence store in model context.
6. Inspect only the selected candidates, their boundaries, relevant callers/dependencies, and tests.
7. Interpret observations semantically. High change, churn, coupling, or concentrated ownership are candidate signals—not technical-debt conclusions.
8. Verify reported metrics, provider semantics, provenance, paths, and important source claims.

## Helper commands

Resolve the helper relative to the invoked skill as `../../shared/scripts/codebase_intelligence.py`.

```text
python3 <helper> discover --repo <repo>
python3 <helper> default-store --repo <repo>
python3 <helper> cache-status --repo <repo> --store <store> --provider git
python3 <helper> analyze-history --repo <repo> --output <store>
python3 <helper> validate --store <store>
python3 <helper> query --store <store> --type change_frequency --metric revisions --limit 20
python3 <helper> query --store <store> --type temporal_coupling --metric coupling --limit 20
```

For Code Maat CSV:

```text
python3 <helper> adapt-code-maat --repo <repo> --input <csv> --analysis coupling --provider-version <version> --output <store>
python3 <helper> cache-status --repo <repo> --store <store> --provider code-maat --provider-version <current-version> --maat-analysis coupling --input <csv>
```

`cache-status` is an analysis-request check, not a store-only check. For Git, pass the current request's `--since`, `--max-commits`, `--max-changeset-size`, and `--min-shared-commits` values; omitted options deliberately mean the documented defaults. Use those same options for `analyze-history` after a miss. For Code Maat, discover the currently available provider version using that tool's version mechanism and supply the current CSV and analysis. If the optional provider or its version cannot be determined, do not reuse its cache; use the Git fallback or regenerate when the provider is available. Never obtain an expected version from the cached store itself.

The Git fallback calculates coupling as `shared_commits / min(left_revisions, right_revisions)` after excluding changesets larger than the configured cap. Code Maat's percentage degree is preserved as Code Maat semantics and must not be compared as though it were the fallback metric without qualification.

## History quality

Treat shallow history, a very small matching commit count, bulk formatting/import commits, generated files, renames, bots, and monorepo-wide changes as confounders. Adjust parameters only for a stated reason and record them in provenance.
