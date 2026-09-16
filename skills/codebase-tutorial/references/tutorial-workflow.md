# Tutorial workflow

## Abstraction record

For each core concept keep a working record with a short name, why it exists, responsibility, relevant repository-relative paths/symbols, upstream/downstream relationships, evidence status, and desired teaching depth.

Five is a useful lower target only for repositories with enough substance; do not invent concepts to reach it. Ten is a useful ceiling, not a quota. Merge generic bootstrap, configuration, logging, and framework plumbing unless one is central to the project's purpose.

## Chapter shape

1. The problem and why the concept exists.
2. A concise mental model or apt analogy.
3. Its public boundary and collaborators.
4. A walkthrough grounded in a few short excerpts.
5. Failure or edge behavior where important.
6. Links to prerequisite/next concepts and exact suggested source reading.

Keep a compact running summary so later chapters build on earlier ones. Avoid repeating the architecture overview in every chapter.

## Diagram gate

Use stable node identifiers and human labels. For each edge, record the supporting import, call, registration, message, state access, or configuration. An attractive unsupported diagram is a verification failure.

## Optional artifact layout

When the user requests files, a suitable layout is `index.md`, numbered chapter files, and a small machine-readable concept/evidence index. Validate every internal link. Do not assume this layout when the user requested a single document or chat answer.
