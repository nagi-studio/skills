---
name: summarize-paper
description: "Read and analyze academic papers through Quick Report, Guided Deep Taste, or one-shot Deep Report. Default requests such as 深入理解, 深度品味, 吃透, or 带我读 to an interactive, prediction-led deep reading that interleaves prose, LaTeX, original paper figures, and focused explanatory UI. Use Deep Report only when the user explicitly requests a complete one-shot analysis, review, or non-interactive report. Use with PDFs, arXiv pages, URLs, local files, paper titles, or BibTeX."
---

# Summarize Paper

## Core Contract

Treat paper reading as evidence-led research study, not generic summarization. Read the paper directly, separate facts from inference, connect mechanisms to evidence, and choose both a reading depth and a delivery style.

### Select the route

- Use `Quick Report` for `快速阅读`, `快速了解`, `概览`, `简要总结`, `值不值得读`, and equivalent requests.
- Use `Guided Deep Taste` for `深入理解`, `深度品味`, `吃透`, `真正理解`, `带我读`, `一起读`, `边读边想`, `step by step`, and equivalent requests. This is the default for any deep request that does not explicitly request a report.
- Use `Deep Report` only for explicit one-shot cues such as `一次性`, `完整报告`, `直接给出全部结论`, `不要互动`, `审稿报告`, or equivalent wording.
- If no depth cue appears, default to `Quick Report`.
- Begin immediately when the route is clear. Do not ask the user to reconfirm it.
- Allow the user to switch routes at any time with `guided`, `report`, `skip`, `deeper`, or equivalent natural language.

Read the selected route completely before responding:

- Guided Deep Taste: [references/guided-deep-taste.md](references/guided-deep-taste.md)
- Deep Report: [references/deep-report.md](references/deep-report.md)
- Any deep reading, visual request, or ADHD-friendly reading: [references/multimodal-composition.md](references/multimodal-composition.md)

## Research Workflow

1. Identify the paper from the PDF, arXiv ID, URL, title, BibTeX, or local path.
2. Read the paper directly according to the selected route. Never substitute a thread, blog post, abstract-only view, or third-party summary for the paper.
3. For PDFs or visually dense papers, render and inspect key pages. Crop the few original figures or tables that answer concrete reader questions.
4. For Deep routes, read the full paper privately before teaching or reporting, including relevant appendices, limitations, qualitative evidence, failure cases, ablations, and theoretical details.
5. Inspect official code, project pages, benchmark definitions, cited work, or intellectual ancestry when they materially affect framing, implementation, novelty, or evidence.
6. Build a compact source map before writing:
   - Paper claims: what the target paper explicitly states.
   - Literature claims: what external primary sources establish.
   - Evidence-based inferences: conclusions justified by evidence but not directly claimed.
   - Uncertain guesses: plausible but unverified interpretations.
7. Write in the user's language. For Chinese users, write natural Chinese while preserving precise English technical terms where useful.

## Source Discipline

Strictly distinguish:

- `论文原文`: explicit claims or evidence from the target paper.
- `相关文献`: claims from cited papers, official code, benchmarks, or other primary sources.
- `合理推断`: conclusions inferred from evidence but not directly stated.
- `不确定猜测`: hypotheses that remain speculative.

Never present inference as fact. Mark mixed-source claims inline with `【论文原文】`, `【相关文献】`, `【合理推断】`, or `【不确定猜测】`. Cite web sources with links. Cite a local PDF by filename plus page, section, figure, table, or equation whenever possible.

Treat original paper figures and tables as evidence. Label generated diagrams and interactive views `【解释性重构】`; cite the source figure, table, equation, page, or section used to derive them.

## Quick Report

Answer four questions efficiently: What problem does the paper address? What does it claim? What is the strongest evidence? Is it worth more attention?

Read the abstract, introduction, conclusion, method overview, central figures or tables, limitations, and enough appendix material to verify the central claim. Verify at least one central comparison and the strongest relevant baseline.

Use this compact structure:

1. `研究问题与价值`
2. `核心 claim`
3. `方法 intuition`
4. `关键证据`: use `claim -> experiment -> result -> judgment`
5. `主要限制`
6. `是否值得深读`

Do not automatically add full derivations, reconstructed thought paths, a reproduction program, or a follow-up proposal.

## Multimodal Non-Negotiables

- Use prose as the reasoning spine.
- Use LaTeX for mathematical precision.
- Use original paper images as empirical evidence.
- Use explanatory UI only to externalize a difficult mechanism, comparison, parameter effect, geometry, or stepwise process.
- Never replace a deep reading with a visualization-only dashboard.
- Explanatory UI is always plain self-contained HTML. Deliver it inline when the host supports it, otherwise as a temporary `.html` file, otherwise as a static SVG, table, or annotated figure crop.
- Interpret `整体 visualize` as “use visual support throughout the reading,” unless the user explicitly requests a visual-only deliverable.
- Keep each UI focused on one dominant question and place it between the prose, formula, and evidence it supports.
- Do not force every modality into every turn. Use the smallest balanced combination that preserves depth and reduces cognitive load.

## Writing Style

Use LaTeX display math for objectives, losses, constraints, variable definitions, and derivations. Define symbols near their first use, check dimensions and boundary cases, and explain what each transformation buys.

Use Andrej Karpathy as the technical-naturalness anchor and Kaiming He as the structural-clarity anchor. Start from a concrete problem, expose the failure mode, state the mechanism cleanly, and use evidence only where it changes the judgment. Do not imitate either writer's exact voice.

Prefer short topic sentences, concrete failure modes, mechanistic explanations, explicit uncertainty, and stable terminology. Avoid empty praise, promotional language, rhetorical over-formatting, and presenting the contribution as obvious before reconstructing why it became plausible.
