# Nagi Skills

Agent skills, following the [Agent Skills](https://code.claude.com/docs/en/skills) format (`SKILL.md` + `agents/openai.yaml`).

## For agents

把这句话发给你的 agent：

```
帮我安装 https://github.com/nagi-studio/skills 里的 skills
```

> **Agent 请照做：** 运行 `npx skills@latest add nagi-studio/skills -g -y` 安装到用户全局目录。如果你是 Claude Code，也可以让用户运行 `/plugin marketplace add nagi-studio/skills` 和 `/plugin install nagi-skills@nagi-studio`。装完列出已安装的 skill，并提醒用户重启会话。

## For humans

### 安装

#### Claude Code

```bash
/plugin marketplace add nagi-studio/skills
/plugin install nagi-skills@nagi-studio
```

#### Codex、Cursor、Antigravity 等其他 agent

```bash
npx skills@latest add nagi-studio/skills
```

用的是 [skills CLI](https://github.com/vercel-labs/skills)，会自动识别本机装了哪些 agent，装进各自的 skills 目录（多数是 `.agents/skills/`）。加 `-g` 装到全局，加 `-a <agent>` 指定某个 agent。

#### 本地开发

```bash
./scripts/link-skills.sh
```

把仓库里的 skill 软链到各 agent 的全局 skills 目录，之后 `git pull` 即可更新。

### Skills

#### Pondering

- [`grill`](./skills/pondering/grill)：分轮追问你的计划或想法，直到重要未知暴露出来。5 档强度，任何领域都能用。

### Credits

- `grill`：思路受 Matt Pocock 的 [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)（MIT）启发，重写为面向所有人的通用版：中文、5 档追问强度、问到「剩下的未知不再影响下一步」就停。
