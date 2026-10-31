# Nagi Skills

**中文** · [English](./README.en.md)

配套《Re:从零开始的AI学习》，每个 skill 都有一期视频讲为什么这么做。[📺 合集](https://space.bilibili.com/312249633/lists/8719249?type=season)

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

装好的 skill 不会自己跟着仓库更新。仓库有新版本时，把这句话发给你的 agent：

```
帮我更新 https://github.com/nagi-studio/skills 里的 skills
```

> **Agent 请照做：** 对这个仓库里已安装的每个 skill 运行 `npx skills@latest update <skill 名> -g -y`。如果用户是用 Claude Code 插件装的，运行 `claude plugin marketplace update nagi-studio` 和 `claude plugin update nagi-skills@nagi-studio`。更新完提醒用户重启会话。

自己更新：

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

### Rookie

适合刚开始用 agent 做东西的新手。这三个其实是练脑子的：装不装 skill 不重要，重要的是把这套想法记在脑子里——先比方案再动手、要证据不要「做好了」、交差前对着清单做减法。记住了，换什么 agent、装不装这几个 skill，你都会这样要求它。

- [`architect`](./skills/rookie/architect)：需求清楚之后，比较两三套技术方案并推荐一套。按你管得过来的程度排序，每套写明你得自己管哪些密钥和权限。接着 grill 的决策记录往下做。[📺 视频](https://www.bilibili.com/video/BV1TtpL6SEvg)
- [`prove-it`](./skills/rookie/prove-it)：让 agent 拿证据交差，而不是一句「做好了」：交差前跑测试、在真浏览器里点一遍并截图；同一个错被纠正第二次，就把它变成下次一犯就报错的检查；顺手清理三种垃圾测试。
  - 来源：「把错误变成会报错的检查」这个思路来自 Poteto 的 [correct](https://github.com/cursor/plugins/tree/main/pstack/skills/correct)；三种垃圾测试的判断参考了 Matt Pocock 的 [tdd](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)；浏览器里点一遍再截图的做法，来自 [Voyager](https://github.com/voyager-crew/voyager) 专用的 [verify-in-browser](https://github.com/voyager-crew/voyager/blob/main/.agents/skills/verify-in-browser/SKILL.md)，改写成了任何网页项目都能用的通用版。
<!-- TODO: 下面是 taste 版本的旧介绍，按 de-slop 重写后再放出来
- [`de-slop`](./skills/rookie/de-slop)：给做好的界面去 AI 味。agent 先截图，桌面和手机各一张，再对着清单一条条查：多余的小字和标签、渐变发光、正文里的 emoji（换成现成图标库）、套娃卡片、太多种字号；改完再截图，直到每条都过。你纠正过的地方写进 `DESIGN.md`，同一个意见不用说第二遍。
  - 来源：挑组件库和做动画，直接读 Emil Kowalski 的 [pick-ui-library](https://github.com/emilkowalski/skills/tree/main/skills/pick-ui-library) 和 [animate](https://github.com/emilkowalski/skills/tree/main/skills/animate)；去 AI 味的清单参考了 [@dingyi](https://x.com/dingyi/status/2115790005423734818) 整理的 AI 味前端特征；logo 流程参考了 [logo-design-skill](https://github.com/kaankiziltug/logo-design-skill) 和 [@Kubai087](https://x.com/Kubai087/status/2115674219602452656) 讲的 AI 图标为什么显得廉价。
-->

## 维护

```bash
./scripts/link-skills.sh
```

把仓库里的 skill 直接软链到各 agent 的全局 skills 目录，之后在仓库里 `git pull` 即可更新，不经过上面的更新命令。新增 skill 的约定见 [AGENTS.md](./AGENTS.md)。
