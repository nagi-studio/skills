---
name: checkup
description: 体检并清理 Codex 和 DSH 已安装的 skill、MCP、plugin 和 hook（统计近 30 天调用次数、常驻上下文开销与失效配置）。用在定期清理吃灰扩展、怀疑上下文变臃肿，或用户说 checkup、体检、清理插件或 skill 时；Claude Code 直接用官方 /doctor。
---

## 0. 客户端分流

在 Claude Code 中运行、且用户未要求顺查 Codex 或 DSH 时，直接引导用户运行官方 `/doctor` 检查吃灰扩展与上下文开销，本技能结束。

## 1. 跑只读日志统计

**DSH 会话日志是 `session.v4.jsonl.zstd`，脚本必须能解 zstd**，否则全部会话被跳过、所有 Skill 被误判成吃灰。三种解压来源任一即可（脚本按此顺序探测）：

```bash
python -c "import sys;print(sys.version)"     # 3.14+ 自带 compression.zstd
pip install zstandard                          # 3.11~3.13 装这个（清华源对该 wheel 会 403，换 aliyun）
zstd --version                                 # 或者装 zstd CLI
```

输出里 `"zstd": "none"` 且 `"skipped_zst" > 0` → 立刻停下装解压能力，别看统计结果。

在用户当前项目根目录，用本技能目录下脚本的**绝对路径**运行：

```bash
python3 <本技能目录>/scripts/audit.py --agent all --days 30
```

只查单个客户端时，把 `--agent` 换成 `codex` 或 `dsh`。

硬闸门：出现以下任一情况，立刻停止并告知用户日志格式/环境有问题，避免把正常扩展误判为吃灰——
`schema_unrecognized: true`（扫了会话却识别到 0 条事件）、`zstd_missing_gate: true`（有压缩日志但解不开）。

完成标准：确认扫描天数、会话数、跳过压缩日志数为 0、`schema_unrecognized` 与 `zstd_missing_gate` 均为 `false`。

## 2. 读本地配置补齐静态盘点

小配置文件直接读取，比脚本硬解析更稳：
- **Codex**：读 `~/.codex/config.toml`（核对 `[mcp_servers.*]`、`[plugins.*]`、`[hooks.state.*]` 是否指向已不存在或空缓存插件）；需要细分每块常驻开销时跑 `codex debug prompt-input "hi"`。
- **DSH**：读 `~/.dsh/profiles/*/package.json`（找出在 `dependencies` 中但不在 `dsh.profile.bundles` 里的包）
  和 `cordis.patch.yml`（MCP 挂载）。**先看 patch 里有没有 `insert` 项**：自建插件常用 patch 挂载、
  不进 bundles，这种是正常挂载，不要判成「已装未挂载」。非 `desktop` profile 跑 `dsh --profile <name> --dump-config` 检查配置报错。

完成标准：配置清单与脚本用量统计对齐，静态异常全部列出。

## 3. 出精简体检单

只把**被标记的项**放进表格，其余正常项汇总为一句总数（避免刷屏）：

| 类型 | 名称 | 近 N 天命中 | 最近使用 | 常驻开销 | 建议 |
|---|---|---|---|---|---|

按三类高优先项置顶：
1. **吃灰大户**：近 N 天 0 次命中、但常驻占上下文的 Skill / MCP / Plugin。
2. **预算告警**：Codex `host_skills.usage.tokens` 接近或顶到 `10,000` 上限，或工具 schema 全量注入过大。
   DSH 看 `overhead.request_header`：`mcp_schema_chars > 20000` 报 MCP 超标；
   若 `mcp_attribution` 为 `unavailable_bare_names`（新版 DSH 把 bridge 工具写成裸名，没有 `mcp__` 前缀，按 server 归因失效），
   改看 `tools_schema_chars` 总量 > 20000，并在表里注明「归因不可用，按总量判」。
3. **失效 / 孤儿配置**：已删插件残留的 Hook 信任记录、无法加载的 bundle、已装未挂载依赖、同名重复 Skill。

0 次命中不等于没用：只靠用户手敲才会用的（如发版、部署类 Skill）、几个月才用一次的，先在表里标出来问用户，不直接列进清理清单。

口径要求：日志不记录调用的项（Hook 触发、DSH 按 profile 拆分）如实标为 `仅静态盘点`；Codex 的脚本读文件命中标为 `启发式`。需要顺手精简 `AGENTS.md` 或项目规则时，提示用户用同组的 `tidy` skill。

完成标准：末尾给出编号的待确认清理清单，等待用户回复编号再改。

## 4. 可逆停用（确认后再改）

收到用户确认的编号后，按需只读对应参考文件里的停用与回滚命令后再执行：
- Codex：[`references/codex.md`](references/codex.md)
- DeepSeek Harness（DSH）：[`references/dsh.md`](references/dsh.md)

优先用配置开关停用；确需移走本地 Skill 目录时，移入 `~/.agents/.checkup-trash/<YYYY-MM-DD>/` 并写明还原路径。改完复跑一次 `audit.py` 核对结果。

完成标准：每项改动都附带回退路径，复跑脚本无新增报错。

## 5. 交差

```
范围：<Codex / DSH>，近 N 天（扫 M 个会话，跳过 K 个压缩日志）
发现：吃灰 X 项 · 预算告警 Y 项 · 失效配置 Z 项（正常项共 W 项）
已执行：<逐项改动与回退路径；只读模式写「无，待确认」>
常驻开销：<改动前 → 改动后；未改动写当前值>
仅静态盘点：<如 Hook 清单>
```
