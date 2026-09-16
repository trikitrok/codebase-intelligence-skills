# Verification pass

Perform a concrete verification pass before reporting.

## Deterministic facts

- Confirm every referenced path exists and remains inside the repository.
- Confirm named symbols exist; then inspect definitions/callers before claiming semantics.
- Check imports, registrations, routes, calls, schemas, configuration keys, and test names with repository search or project-native analysis.
- Validate evidence stores and provenance before quoting metrics.
- Confirm Git-history limitations, parameters, provider version, units, ranges, and metric definition.
- Re-run a narrow query when evidence may have changed during the analysis.

The helper accepts a JSON array such as `[{'path': 'src/a.py', 'symbol': 'run'}]` (using valid JSON double quotes) through `verify-references`. Its symbol result is explicitly lexical, so it cannot prove a call edge or runtime behavior.

## Semantic claims

- Trace each important transition through actual source, configuration, framework registration, or tests.
- Distinguish reachable behavior from dead/example/generated code.
- Inspect tests where they define behavior or contradict implementation.
- Label strong but indirect conclusions `INFERRED`; leave unresolved claims `UNKNOWN`.

## Diagrams

Verify every meaningful node and edge. Keep edge labels concrete (`calls`, `publishes`, `reads`, `writes`, `constructs`). Remove decorative edges that imply unsupported relationships. If an edge is inferred, say so adjacent to the diagram or in its legend.

## Completeness

Revisit the user's question and the repository map. Check that no major entry point, state boundary, external integration, failure path, or relevant test family was accidentally omitted. This is a bounded coverage review, not a reason to read unrelated source.
