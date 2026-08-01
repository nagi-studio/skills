# Agent 维护约定

这个仓库存放 Nagi Studio 的 agent skills。改动它时遵守下面的约定。

## 目录结构

```
skills/<category>/<skill-name>/
  SKILL.md              # 必需。frontmatter 只放 name + description
  agents/openai.yaml    # 必需。Codex 等 harness 的展示信息与调用策略
  references/*.md       # 可选。按需加载的长流程，SKILL.md 里用相对链接指向
```

`skills/<category>/` 下的每个目录只要含 `SKILL.md` 就会被 `scripts/link-skills.sh` 链出去。

## SKILL.md 规则

- frontmatter 只有 `name`（kebab-case，和目录名一致）和 `description`。
- `description` 要写清**什么时候用**，包含用户可能说的原话触发词（中英文都列），因为模型靠它决定是否调用。
- 正文用祈使句写给 agent 看，不是写给人看的文档。
- 单文件超过约 500 行就拆到 `references/`，主文件只留路由和不可协商的规则。
- 引用 reference 时写相对路径链接，并明确说「读完再回复」。

## agents/openai.yaml 规则

```yaml
interface:
  display_name: "Human Readable Name"
  short_description: "一句话说明"
  default_prompt: "可选，用户点按钮时的默认输入"
policy:
  allow_implicit_invocation: false # 只在「必须用户显式调用」时加
```

## 新增 skill 后

1. 把路径加进 `.claude-plugin/plugin.json` 的 `skills` 数组。
2. 在 `README.md` 的对应分类下加一行说明。
3. 提 PR 前先跑一遍 `./scripts/link-skills.sh`，在真实任务上试用过再合并。

## 隐私

skill 内容会公开。提交前确认没有个人姓名、邮箱、本地绝对路径、机构内部信息、token 或 API key。
