# Tool-first workflow

Use this workflow for hotspot and coupling investigations.

## Required sequence

1. Read [core.md](core.md) and run repository/tool discovery before source inspection beyond manifests and boundaries.
2. Check whether a compatible evidence store exists and validate it with `cache-status`, naming the intended provider and the same analysis parameters the current request would use. Never reuse a store merely because its filename matches.
3. If valid hotspot evidence is missing, use a suitable available/configured Code Maat capability first. If it is unavailable, unsuitable, or declined, use the standard-library Git + LOC fallback. Use installation only after the shared permission flow.
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
python3 <helper> rank-hotspots --store <store> --limit 20
```

For Code Maat CSV:

```text
python3 <helper> adapt-code-maat --repo <repo> --input <csv> --analysis coupling --provider-version <version> --output <store>
python3 <helper> adapt-code-maat --repo <repo> --input <revisions.csv> --churn-input <entity-churn.csv> --analysis hotspots --provider-version <version> --output <store>
python3 <helper> cache-status --repo <repo> --store <store> --provider code-maat --provider-version <current-version> --maat-analysis coupling --input <csv>
```

`cache-status` is an analysis-request check, not a store-only check. For Git, pass the current request's `--since`, `--max-commits`, `--max-changeset-size`, and `--min-shared-commits` values; omitted options deliberately mean the documented defaults. Use those same options for `analyze-history` after a miss. For Code Maat, discover the currently available provider version using that tool's version mechanism and supply the current CSV and analysis. If the optional provider or its version cannot be determined, do not reuse its cache; use the Git fallback or regenerate when the provider is available. Never obtain an expected version from the cached store itself.

The Git fallback calculates hotspot candidates from change frequency plus current tracked physical LOC. It ranks each axis within the candidate set and multiplies the descending ranks; it does not use an ecosystem-specific complexity analyzer. Its coupling remains `shared_commits / min(left_revisions, right_revisions)` after excluding changesets larger than the configured cap. Code Maat revisions, entity churn, and percentage coupling are preserved as Code Maat semantics and must not be compared as though they were fallback metrics without qualification.

## History quality

Treat shallow history, a very small matching commit count, bulk formatting/import commits, generated files, renames, bots, and monorepo-wide changes as confounders. Adjust parameters only for a stated reason and record them in provenance.
