# Evidence contract v1

The evidence store is a JSON object containing `schema_version`, `store_kind`, common `provenance`, repository metadata, limitations, and an `observations` array. Every observation repeats the provenance needed for standalone interpretation.

```json
{
  "schema_version": 1,
  "type": "temporal_coupling",
  "subject": {
    "type": "file_pair",
    "paths": ["src/a.ts", "src/b.ts"]
  },
  "metrics": {
    "shared_commits": 8,
    "coupling": 0.67,
    "metric_definition": "shared_commits / min(left_revisions, right_revisions)"
  },
  "provenance": {
    "provider": "codebase-intelligence-git",
    "provider_version": "0.1.0",
    "analyzer_version": "0.1.0",
    "repository_id": "...",
    "repository_head": "...",
    "dirty": false,
    "working_tree_fingerprint": "...",
    "shallow": false,
    "input_scope": "committed_history",
    "parameters": {
      "since": null,
      "max_commits": null,
      "max_changeset_size": 30,
      "min_shared_commits": 2
    },
    "generated_at": "2026-09-16T00:00:00+00:00"
  }
}
```

## Initial types

- `change_frequency`: commit/revision counts.
- `churn`: added/deleted/absolute line counts.
- `temporal_coupling`: co-change observations and provider-defined coupling.
- `ownership`: author counts or contribution concentration.
- `complexity`, `static_dependency`, and `test_coverage`: reserved for adapters that preserve a provider's definitions and units.

Subjects are repository, component, directory, file, symbol, file pair, or component pair. File paths, including both sides of file pairs, are normalized repository-relative identifiers: absolute paths, backslashes, `.` segments, and `..` traversal are invalid. Components require repository evidence such as build modules, manifests, explicit configuration, or inspected source boundaries; never aggregate arbitrary directory names as architecture without labeling the inference.

## Observation boundary

Store raw or quantitative observations and provider classifications. Do not store Codebase Intelligence conclusions such as `technical_debt: true`, `bad_architecture`, or `should_refactor`. Those require selective source inspection and contextual reasoning.

## Provenance and validity

All observations identify provider, provider version, repository identity and HEAD, parameters, input scope, and generation time. Dirty state and a working-tree fingerprint are recorded.

Evidence v1 deliberately repeats the complete store provenance on every observation so an extracted observation remains interpretable. Validation therefore requires exact equality between observation and store provenance. Repository metadata must also agree with the store's repository identity, HEAD, dirty state, working-tree fingerprint, and shallow-history state. Contradictory copies are corruption, not an alternate source of truth.

- `committed_history` evidence is valid only for the same repository identity, HEAD, provider/version, analyzer version, schema, parameters, and provider inputs. A dirty working tree alone does not invalidate it because it did not consume working files.
- Evidence whose scope includes the working tree must also match dirty state and fingerprint.
- Incompatible schema versions are rejected; recompute or write an explicit migration rather than silently interpreting them.

Raw provider output may be retained separately when useful for debugging, but it is not loaded into model context by default.

## Provider adapters

Adapters parse provider output, validate required fields and repository-relative subjects, preserve units/ranges/definitions, attach provenance, and fail clearly on malformed data. They do not make architectural judgments. Consumers query evidence capabilities, not provider-specific prose.

Provider independence is intentionally small today: the Git producer and Code Maat CSV adapter share this envelope, validation, query path, and provider-specific request checks. Adding another provider remains an explicit adapter plus a corresponding cache-request branch that can determine its current version and validity-critical inputs. There is no provider registry or generic plugin framework.
