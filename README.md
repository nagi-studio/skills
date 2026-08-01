# Nagi Skill

Nagi Studio 的 agent skills。两条线：**研究阅读**（把读论文当成有证据纪律的研究工作，而不是通用摘要），和**输出风格**（让 agent 干活、你只做验收）。

Skills 遵循 [Agent Skills](https://code.claude.com/docs/en/skills) 格式（`SKILL.md` + `agents/openai.yaml`），在 Claude Code、Codex 以及任何兼容 harness 上都能用。

## 安装

### Claude Code

```bash
/plugin marketplace add nagi-studio/Nagi-Skill
/plugin install nagi-skills@nagi-studio
```

### Codex 及其他 agent

```bash
npx skills@latest add nagi-studio/Nagi-Skill
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

## 维护

约定写在 [AGENTS.md](./AGENTS.md)。

## License

MIT
