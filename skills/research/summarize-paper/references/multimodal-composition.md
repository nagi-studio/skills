# Multimodal Composition

Build a coordinated reading experience from four complementary modalities:

- Prose: causal reasoning, interpretation, uncertainty, and transitions.
- LaTeX: mathematical objectives, derivations, constraints, dimensions, and boundary cases.
- Original paper images: empirical evidence from figures, tables, tasks, ablations, and failures.
- Explanatory UI: interactive reconstruction of mechanisms, parameter effects, comparisons, geometry, or stepwise dynamics.

Prose is the spine. The other modalities must clarify or test a specific part of that spine. Never let a UI replace the surrounding reasoning, formulas, or original evidence.

## Composition Budget

Use these as flexible balance targets across a hinge point, not rigid quotas:

- Prose and technical explanation: roughly 40–55%.
- Equations and symbol interpretation: roughly 10–20%.
- Original figures or tables: roughly 15–25%.
- Explanatory or interactive visual support: roughly 15–25%.

Adjust for the paper. A theoretical paper may need more mathematics; a systems paper may need more diagrams and evidence tables. Avoid allowing any single modality to dominate the whole reading unless the user explicitly requests it.

## Per-Hinge-Point Pattern

Use the smallest subset that serves the current question:

1. State the current conceptual question in prose.
2. Explain the causal mechanism and necessary background.
3. Introduce the relevant formula and define symbols nearby.
4. Show one original figure or table when empirical evidence is being revealed.
5. Add at most one focused explanatory UI when manipulation materially improves understanding.
6. Return to prose to interpret the evidence, state limitations, and ask the next prediction.

Do not force all four modalities into every turn. Avoid galleries, dashboards, duplicated summaries, and multiple competing interactions.

## Original Figures

- Render and crop the original PDF page instead of relying only on extracted text.
- Show the fewest panels needed to answer the current question.
- Place the image next to the paragraph that interprets it.
- State what question the figure answers and what it does not establish.
- Preserve axes, units, uncertainty, captions, and relevant boundary conditions.
- Treat original figures as `【论文原文】` evidence.

## Mathematics

- Use display LaTeX for important equations.
- Define every symbol close to the equation.
- Explain the transformation in words immediately after it.
- Check tensor or vector dimensions when they matter.
- Test a simple example and a boundary case.
- Skip algebra that does not change the reader's mental model.

## Explanatory UI

Build an explanatory UI for adjustable parameters, state transitions, geometry, stepwise mechanisms, or comparisons that benefit from active exploration.

The UI itself is always plain self-contained HTML, CSS, and JavaScript with no external dependencies. Only the delivery channel is host-specific. Pick the first available option:

1. Inline rendering, when the host supports it: the `visualize` skill on Codex, the `Artifact` tool on Claude Code, or the equivalent inline-HTML mechanism of the current harness.
2. Temporary file fallback: write one self-contained `.html` file to a temporary directory, then open it and tell the user the path.
3. Static fallback, when neither is available: an inline SVG, a Markdown comparison table, or an annotated crop of the original figure. Never drop the explanation because interaction is unavailable.

Do not name a specific host skill in the reading itself, and never assume `visualize` exists before checking.

- Give each UI one dominant explanatory question.
- Make the first state useful without interaction.
- Keep current state, notation, units, and selected values visible.
- Use controls that map directly to the paper's variables or experimental conditions.
- Keep sourced and illustrative values visibly distinct.
- Label the UI `【解释性重构】` and cite its source equation, figure, table, page, or section.
- Never hide an essential claim exclusively behind interaction.
- Never create a dashboard that attempts to summarize the whole paper.

Whichever channel is used, retain the normal Markdown prose, LaTeX, and original images before and after the UI. Do not emit only the visualization unless the user explicitly asked for a visual-only deliverable.

Interpret phrases such as `整体都要 visualize`, `多用交互图`, or `可视化地讲` as requests for visual support throughout the reading. They do not override the prose, formula, original-evidence, or guided-interaction contracts.

## ADHD-Friendly Coordination

- Use one dominant question per turn or visual.
- Reveal complexity in meaningful chunks.
- Keep definitions and symbols near the marks they explain.
- Use stable labels and encodings across turns.
- Provide visible re-entry landmarks and a compact current-state marker.
- Avoid split attention: do not make the reader compare a distant equation, figure, and explanation.
- Use motion only to reveal a mechanism or state transition; never loop decorative animation.
- Preserve technical depth. Reduce extraneous cognitive load, not information content.
