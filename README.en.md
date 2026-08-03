# Nagi Skills

[中文](./README.md) · **English**

The agent skills Nagi Studio actually uses every day, straight out of the `.agents` directory.

They share one standard: no hand-waving. When reading a paper, say which line came from the paper and which one is a guess. When doing work, don't call it done until you've actually run it. Anything that turns out to be worth keeping ends up here, so this repo keeps growing.

Every skill follows the [Agent Skills](https://code.claude.com/docs/en/skills) format (`SKILL.md` + `agents/openai.yaml`), so it works in Claude Code, Codex, and any compatible harness.

## Install

### Claude Code

```bash
/plugin marketplace add nagi-studio/skills
/plugin install nagi-skills@nagi-studio
```

### Codex and other agents

```bash
npx skills@latest add nagi-studio/skills
```

### Manual / local development

```bash
./scripts/link-skills.sh
```

Symlinks every skill in the repo into `~/.claude/skills` and `~/.agents/skills`. After that, `git pull` is all it takes to update.

## Skills

### Research

- **[summarize-paper](./skills/research/summarize-paper/SKILL.md)** — Close reading for papers. Three routes: `Quick Report` (is it worth reading), `Guided Deep Taste` (walks you through predicting, checking, and absorbing it — the default), and `Deep Report` (one full report in a single pass). Throughout, it keeps "the paper itself / related work / reasonable inference / uncertain guess" apart, uses the original figures and tables as evidence, and renders LaTeX in a focused explanatory UI.

- **[adhd-friendly](./skills/productivity/adhd-friendly/SKILL.md)** — An ADHD-friendly output style that cuts cognitive load and the cost of getting started. The agent does the work and you just sign off: answer first, nothing is "done" until it's been tested, anything you need to eyeball gets opened rather than handed to you as a path, whatever can be finished in one go gets finished, and three failed rounds on the same problem means stop and question the assumption. For reports and experiment write-ups it carries a separate [wording table](./skills/productivity/adhd-friendly/references/wording.md): standard terminology, no invented metaphors standing in for terms, no colloquialisms, no anthropomorphism. That table is adapted from [this post by @wzenus](https://x.com/wzenus/status/2084252510458630477).

## Also worth having

Not from this repo — third-party skills used alongside these every day:

- **[tw93/Waza](https://github.com/tw93/Waza)** — Engineering habits as skills: `check` (review / pre-release once-over), `hunt` (find the root cause before touching anything), `think` (work out an approach), `write` (drafts, minus the AI smell), `read`, `learn`, `health`. Triggers in both Chinese and English.
- **[greensock/gsap-skills](https://github.com/greensock/gsap-skills)** — Official GSAP animation skills, split by core / timeline / scrolltrigger / react, loaded as needed when writing frontend animation.
- **[op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)** — Strips the AI smell out of Chinese writing, checking against Wikipedia's list of AI writing tells one by one.
- **[mattpocock/skills](https://github.com/mattpocock/skills)** — Engineering-process skills (TDD, code review, domain modelling, spec/ticket). This repo's directory layout follows it.

## Maintenance

Conventions live in [AGENTS.md](./AGENTS.md).

## License

MIT
