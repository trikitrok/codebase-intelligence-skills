# Diagramming

Create a diagram only when visual structure materially improves the explanation.
Do not create a diagram merely to restate a simple list or relationship.

When a diagram is useful, use the `mermaid-diagram` skill as the visualization
layer. The calling analysis skill remains the source of truth; do not delegate
repository discovery or analysis to the diagramming skill.

Provide only the verified findings needed for the diagram, including as
applicable:

- the purpose and intended audience;
- entities, components, actors, states, or runtime units;
- verified relationships and their direction;
- ordering or sequencing;
- boundaries and groupings;
- relevant inputs, outputs, or transitions;
- verified evidence artifacts when useful;
- contradictions, uncertainty, and intentionally omitted relationships that
  affect interpretation.

Preserve repository terminology and identifiers where they improve precision.
Do not add unverified information to make a diagram appear complete.

The `mermaid-diagram` skill owns diagram-type selection, visual structure,
Mermaid syntax, layout, rendering, and visual validation.