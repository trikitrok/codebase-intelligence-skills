# Source-first workflow

Use this workflow for onboarding, tutorials, architecture, behavior traces, deep dives, and change planning.

1. Start with cheap structure: instructions, manifests, entry points, public interfaces, tests, build/run configuration, and repository-native documentation.
2. Form a provisional map, clearly marked as provisional.
3. Search for the requested concepts and symbols. Read only files needed to establish boundaries, control/data flow, state, integrations, and tests.
4. Expand outward through verified callers, imports, registrations, routes, messages, schemas, and configuration. Do not sweep the entire repository by default.
5. Maintain a compact evidence ledger while reasoning.
6. Reconcile source with tests and documentation; report significant disagreement.
7. Verify references, flow transitions, and diagram edges before reporting.

Do not run history or heavyweight static analysis unless the question needs it. A dependency graph can support architecture reasoning but cannot substitute for system boundaries, runtime communication, state ownership, or intent.

For large repositories, split discovery into bounded searches by component or question. Bring only summaries and specific evidence back into the working context; do not inject whole files or giant inventories when targeted excerpts suffice.
