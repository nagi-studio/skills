# 日志格式与手动统计

`audit.py` 的闸门触发时读；查的是脚本不认识的 harness 时，从「找日志」开始读。这里记的是脚本写成时（`VERIFIED_WITH` 里的版本）的格式，当作地图，以真实日志为准：先抽样认清当前格式，再写临时代码统计。

## 补解压能力

DSH 日志是 zstd 压缩的（`session.v4.jsonl.zstd`）。以下任一可用即可，脚本按此顺序探测：

```bash
python3 -c "from compression import zstd"   # Python 3.14+ 自带
zstd --version                              # 或装 zstd CLI（macOS brew / Linux apt / Windows scoop）
python3 -m pip install zstandard            # 或在 3.11–3.13 上装这个
```

装好后重跑 `audit.py`；`zstd_missing_gate` 为 `false`、`unreadable_logs` 为 0 就回到 SKILL.md 第 1 步继续。

## 找日志

脚本只认 Codex 和 DSH。别的 harness 先找到它把会话存在哪：

1. 找以 harness 命名的数据目录：先看 `~/.<名字>`，再看当前系统的应用数据目录。名字对不上时，按 mtime 找最近一周有写入的目录。
2. 在里面找会话记录。同一个 harness 的 IDE 和 CLI 常常各存一份，都要找。数据库只读打开，harness 可能正开着它。protobuf、加密等读不出内容的，放弃日志统计，交差单写「日志不可读，仅静态盘点」。
3. 配置分全局和项目两层：全局的在数据目录里，项目的在用户当前项目目录里，两层都要找。

完成标准：找到了会话文件并能读出内容；或者确认读不了，已经改成只做静态盘点。

## 重新认格式

1. **找最新的会话文件**：Codex、DSH 按下文的路径，其他 harness 用「找日志」找到的目录，取 mtime 最新的一个。
2. **数记录类型**：JSONL 逐行统计顶层 `type`（Codex 再加 `payload.type`）；SQLite 列出每张表的行数和字段。Codex、DSH 再对照下文，看哪些类型是新出现的、哪些是脚本认的但不见了。
3. **用已知调用反查**：挑一个你确定最近用过的 skill 或 MCP，在日志里搜它的名字（压缩的先解压，SQLite 用 `LIKE` 查文本字段），看它落在哪种事件、哪个字段。这就是新格式的调用记录位置。
4. **写临时统计**：用 Python 写，放 scratchpad 目录，只读日志、不改任何东西。按记录里的时间戳筛近 N 天（文件 mtime 新的会话里也有旧记录），按会话去重计数并记最后使用日期，口径和 `audit.py` 输出对齐（调用次数、会话数、最近一天）。

完成标准：skill 和 MCP 各用一个已知调用核对过，统计里它的次数大于 0；哪一类找不到已知调用，那一类整类标 `用量未知`。交差单「范围」一行写明「手动统计」和发现的格式变化。

## Codex

- **位置**：`$CODEX_HOME/sessions/YYYY/MM/DD/rollout-*.jsonl`（默认 `~/.codex`），不压缩。
- **行结构**：`{"timestamp", "type", "payload"}`。
- **MCP 调用**：`type=event_msg`、`payload.type=item_completed`、`payload.item.type=McpToolCall`；`item.server` 是 server 名，`item.status` 判失败，`item.pluginId` 归到插件。
- **Skill 调用**：
  - 显式：`type=response_item`、`payload.role=user` 的文本里含 `<skill><name>…</name>`。
  - 启发式：shell 类调用（`function_call` 的 `exec_command` / `shell`，或 `item_completed` 里的 `CommandExecution`）用 `cat` / `sed -n` 等读了 `<name>/SKILL.md`。
- **常驻开销**：任意层级里的 `host_skills.usage`，取最新一条；细分各块跑 `codex debug prompt-input "hi"`。

## DSH

- **位置**：`$DSH_HOME/sessions/<项目>/session-<id>/session.v4.jsonl.zstd`（默认 `~/.dsh`），跳过 `.lock`。
- **行结构**：`{"time", "type", "data"}`。
- **工具调用**：`type=tool/call`，`data.name` 是工具名。
  - `name=skill` 时 `data.arguments.name` 是模型自己调的 skill（`arguments` 可能是 JSON 字符串）。
  - MCP 工具老版本带 `mcp__<server>__` 前缀；新版 bridge 工具是裸名（`read`、`edit`、`pwsh`），按前缀归不到 server。要拆到 server，对照 `cordis.patch.yml` 里各 MCP 的 `insert` 项和 server 暴露的工具名。
- **用户手动调 skill**：`type=user/message` 的文本里含 `<skill_content name="…">`。
- **常驻开销**：`type=request/header` 的 `data.header.tools`（工具 schema 全量）取最新一条；`user/message` 里含 `<available_skills>` 的那段是 skill 目录的大小。
