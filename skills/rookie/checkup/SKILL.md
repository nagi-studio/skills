---
name: checkup
description: 体检并清理 agent harness 已安装的 skill、MCP、plugin 和 hook（统计近 30 天调用次数、常驻上下文开销与失效配置）：Codex、DSH 有现成脚本，Cursor、Antigravity 等其他 harness 现场找日志统计。用在定期清理吃灰扩展、怀疑上下文变臃肿，或用户说 checkup、体检、清理插件或 skill 时；Claude Code 直接用官方 /doctor。
---

## 0. 客户端分流

先认清这次查哪个 harness：用户点名的那个，没点名就是你自己正跑在里面的那个。

- **Claude Code**：用户没要求顺查别的 harness 时，引导用户运行官方 `/doctor` 检查吃灰扩展与上下文开销，本技能结束。
- **Codex、DSH**：走第 1 步的脚本。
- **其他 harness**（Cursor、Antigravity、WorkBuddy……）：脚本不认识它们，读 [`references/log-formats.md`](references/log-formats.md)，从「找日志」一节开始手动统计，读完再接第 2 步。

## 1. 跑只读日志统计

在用户当前项目根目录，用本技能目录下脚本的**绝对路径**运行：

```bash
python3 "<本技能目录>/scripts/audit.py" --agent all --days 30
```

只查单个客户端时，把 `--agent` 换成 `codex` 或 `dsh`。

脚本是快速通道，只认得 `verified_with` 那个版本的日志格式；客户端一升级，格式就可能变。出现下面任一**闸门**，这次的统计不可信，别拿它出结论，改走手动统计：读 [`references/log-formats.md`](references/log-formats.md)，读完再继续。
- `schema_unrecognized: true`：扫了会话却识别到 0 条事件。
- `skill_usage_unverified: true`：装了 skill，却一次 skill 调用都没认出来。
- `zstd_missing_gate: true` 或 `unreadable_logs > 0`：有日志没读到，先按 log-formats.md 补解压能力再重跑。
- `version`（Codex 还有 `log_versions`，即窗口内日志的写入版本）比 `verified_with` 新，且结果和常识对不上：比如你知道常用的 skill 或 MCP 显示 0 次。

完成标准：扫描天数、会话数确认过，`skipped_zst` 和 `unreadable_logs` 为 0，闸门都没触发；触发过的，手动统计已经按 log-formats.md 的完成标准核对过。

## 2. 读本地配置补齐静态盘点

小配置文件直接读取，比脚本硬解析更稳：
- **Codex**：读 `~/.codex/config.toml`（核对 `[mcp_servers.*]`、`[plugins.*]`、`[hooks.state.*]` 是否指向已不存在或空缓存插件）；需要细分每块常驻开销时跑 `codex debug prompt-input "hi"`。
- **DSH**：读 `~/.dsh/profiles/*/package.json`（找出在 `dependencies` 中但不在 `dsh.profile.bundles` 里的包）
  和 `cordis.patch.yml`（MCP 挂载）。**先看 patch 里有没有 `insert` 项**：自建插件常用 patch 挂载、
  不进 bundles，这种是正常挂载，不要判成「已装未挂载」。非 `desktop` profile 跑 `dsh --profile <name> --dump-config` 检查配置报错。
- **其他 harness**：配置和日志通常在同一个数据目录里，找日志时已经找到；读其中的 skill 目录、MCP 配置（如 `mcp.json`）、插件目录和设置文件，核对是否指向已不存在的路径。

完成标准：配置清单与脚本用量统计对齐，静态异常全部列出。

## 3. 出精简体检单

只把**被标记的项**放进表格，其余正常项汇总为一句总数（避免刷屏）：

| 类型 | 名称 | 近 N 天命中 | 最近使用 | 常驻开销 | 建议 |
|---|---|---|---|---|---|

按三类高优先项置顶：
1. **吃灰大户**：近 N 天 0 次命中、但常驻占上下文的 Skill / MCP / Plugin。
2. **预算告警**：Codex `host_skills.usage.tokens` 接近或顶到 `10,000` 上限，或工具 schema 全量注入过大。
   DSH 看 `overhead.request_header` 的 `budget_warnings`：`tool_schema_total_over_20k` 是工具 schema 总量超标，`mcp_schema_over_20k` 是带 `mcp__` 前缀的 MCP 超标。
   内置工具和新版 bridge 工具都是裸名，`mcp_attribution` 不论是 `prefix_partial` 还是 `unavailable_bare_names`，按 server 拆开的数都只是下限，表里注明「按 server 归因不全」。
3. **失效 / 孤儿配置**：已删插件残留的 Hook 信任记录、无法加载的 bundle、已装未挂载依赖、同名重复 Skill。

日志覆盖不到的类型（比如这个 harness 的日志里找不到任何 skill 调用记录），整类标 `用量未知`，不进吃灰，也不算进正常项。

0 次命中不等于没用：只靠用户手敲才会用的（如发版、部署类 Skill）、几个月才用一次的，先在表里标出来问用户，不直接列进清理清单。

口径要求：日志不记录调用的项（Hook 触发、DSH 按 profile 拆分）如实标为 `仅静态盘点`；Codex 的脚本读文件命中标为 `启发式`。需要顺手精简 `AGENTS.md` 或项目规则时，提示用户用同组的 `tidy` skill。

完成标准：末尾给出编号的待确认清理清单，等待用户回复编号再改。

## 4. 可逆停用（确认后再改）

收到用户确认的编号后，按需只读对应参考文件里的停用与回滚命令后再执行：
- Codex：[`references/codex.md`](references/codex.md)
- DeepSeek Harness（DSH）：[`references/dsh.md`](references/dsh.md)
- 其他 harness：改配置文件前先备份成 `*.bak.<YYYY-MM-DD>`，回退就是还原备份。

优先用配置开关停用；确需移走本地 Skill 目录时，移入 `~/.agents/.checkup-trash/<YYYY-MM-DD>/` 并写明还原路径。改完按第 1 步走过的同一条路（脚本或手动统计）复跑一次，再确认 harness 读到的配置已经变了。

完成标准：每项改动都附带回退路径，复跑统计无新增报错。

## 5. 交差

```
范围：<harness>，近 N 天（扫 M 个会话，跳过 K 个压缩日志；走了手动统计的写明原因和格式变化）
发现：吃灰 X 项 · 预算告警 Y 项 · 失效配置 Z 项（正常项共 W 项）
已执行：<逐项改动与回退路径；只读模式写「无，待确认」>
常驻开销：<改动前 → 改动后；未改动写当前值>
仅静态盘点：<如 Hook 清单>
```
