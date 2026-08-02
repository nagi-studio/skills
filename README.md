# Nagi Skills

**中文** · [English](./README.en.md)

Nagi Studio 每天在用的 agent skills，直接从 `.agents` 目录里搬出来的。

共同的标准只有一条：不许含糊。读论文要分得清哪句是原文、哪句是推断；干活要实测过才能说做完。写出来好用的就往这儿放，所以这个仓库会一直长。

Skills 遵循 [Agent Skills](https://code.claude.com/docs/en/skills) 格式（`SKILL.md` + `agents/openai.yaml`），在 Claude Code、Codex 以及任何兼容 harness 上都能用。

## 安装

### Claude Code

```bash
/plugin marketplace add nagi-studio/skills
/plugin install nagi-skills@nagi-studio
```

### Codex 及其他 agent

```bash
npx skills@latest add nagi-studio/skills
```

### 手动 / 本地开发

```bash
./scripts/link-skills.sh
```

把仓库里所有 skill 软链到 `~/.claude/skills` 和 `~/.agents/skills`，之后 `git pull` 即可更新。

## Skills

### Research

- **[summarize-paper](./skills/research/summarize-paper/SKILL.md)** — 论文精读。三条路线：`Quick Report`（值不值得读）、`Guided Deep Taste`（带你逐步预测、验证、吃透，默认）、`Deep Report`（一次性完整报告）。全程区分「论文原文 / 相关文献 / 合理推断 / 不确定猜测」，用原图原表当证据，配 LaTeX 和聚焦的解释性 UI。

### Productivity

- **[adhd-friendly](./skills/productivity/adhd-friendly/SKILL.md)** — ADHD 友好的输出风格，减轻认知负荷和启动成本。把 agent 当执行方、自己只做验收：结论先行、实测过才说做完、需要人工验收的产物直接打开而不是甩路径、能做的一次做完、卡住三轮就止损。

## 顺手推荐

这些不是本仓库的，是日常一起在用的第三方 skills：

- **[tw93/Waza](https://github.com/tw93/Waza)** — 把工程习惯做成 skill：`check`（review / 发布前体检）、`hunt`（先定位根因再改）、`think`（出方案）、`write`（写稿去 AI 味）、`read`、`learn`、`health`。中英文触发词都覆盖。
- **[greensock/gsap-skills](https://github.com/greensock/gsap-skills)** — GSAP 官方动画 skills，按 core / timeline / scrolltrigger / react 等拆开，写前端动画时按需加载。
- **[op7418/Humanizer-zh](https://github.com/op7418/Humanizer-zh)** — 去中文 AI 味，按维基百科的「AI 写作特征」逐条检测和修。
- **[mattpocock/skills](https://github.com/mattpocock/skills)** — 工程流程 skills（TDD、code review、领域建模、spec/ticket），本仓库的目录结构也是参照它的。

## 维护

约定写在 [AGENTS.md](./AGENTS.md)。

## License

MIT
