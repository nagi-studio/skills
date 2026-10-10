# Nagi Skills

**中文** · [English](./README.en.md)

## 安装

把这句话发给你的 agent：

```
帮我安装 https://github.com/nagi-studio/skills 里的 skills
```

> **Agent 请照做：** 运行 `npx skills@latest add nagi-studio/skills -g -y` 安装到用户全局目录。如果你是 Claude Code，也可以让用户运行 `/plugin marketplace add nagi-studio/skills` 和 `/plugin install nagi-skills@nagi-studio`。装完列出已安装的 skill，并提醒用户重启会话。

自己装：

```bash
npx skills@latest add nagi-studio/skills -g
```

用的是 [skills CLI](https://github.com/vercel-labs/skills)，会自动识别本机装了哪些 agent（Claude Code、Codex、Cursor、Antigravity 等），装进各自的 skills 目录。`-g` 表示装到全局，所有项目都能用；去掉它就只装进当前项目。加 `-a <agent>` 可以指定某个 agent。

<details>
<summary>Claude Code 也可以用插件装</summary>

```bash
/plugin marketplace add nagi-studio/skills
/plugin install nagi-skills@nagi-studio
```

</details>

## 更新

装好的 skill 不会自己跟着仓库更新，仓库有新版本时手动跑一次：

```bash
npx skills@latest update grill -g
```

`grill` 换成要更新的 skill 名；不写名字会更新本机所有全局 skill，不只是这个仓库的。

<details>
<summary>用 Claude Code 插件装的</summary>

在终端里运行：

```bash
claude plugin marketplace update nagi-studio
claude plugin update nagi-skills@nagi-studio
```

已经开着的会话运行 `/reload-plugins`，或者重启。

</details>

## Skills

### Pondering

- [`grill`](./skills/pondering/grill)：分轮追问你的计划或想法，直到重要未知暴露出来。5 档强度，任何领域都能用。[📺 视频](https://www.bilibili.com/video/BV1irHx6dEEf)
  - 来源：思路受 Matt Pocock 的 [grilling](https://github.com/mattpocock/skills/tree/main/skills/productivity/grilling)（MIT）启发，重写为面向所有人的通用版：中文、5 档追问强度、问到「剩下的未知不再影响下一步」就停。

## 维护

```bash
./scripts/link-skills.sh
```

把仓库里的 skill 直接软链到各 agent 的全局 skills 目录，之后在仓库里 `git pull` 即可更新，不经过上面的更新命令。新增 skill 的约定见 [AGENTS.md](./AGENTS.md)。
