# Codex 停用与回滚命令

在确认清理清单后按需查阅。动手修改 `$CODEX_HOME/config.toml`（默认 `~/.codex/config.toml`）前，先备份为 `config.toml.bak.<YYYY-MM-DD>`。

- **停用 MCP**：在 `[mcp_servers.<name>]` 下设 `enabled = false`。
- **停用 Plugin**：在 `[plugins."<id>"]` 下设 `enabled = false`（回退：改回 `true`）。
- **停用本地 Skill**：
  - 配置停用：在 `config.toml` 追加 `[[skills.config]]` 条目（`path = "..."`, `enabled = false`）；
  - 或把目录移入 `~/.agents/.checkup-trash/<YYYY-MM-DD>/`（回退：`mv` 回原路径）。
- **清理孤儿 Hook 信任记录**：确认对应插件缓存目录为空或不存在后，删除 `[hooks.state."<plugin>:..."]` 段落（回退：用备份的 `config.toml.bak.*` 还原）。
- **改完核对**：用 `python3 -c 'import tomllib, pathlib; tomllib.loads(pathlib.Path("~/.codex/config.toml").expanduser().read_text())'` 校验 TOML 语法无误，再复跑 `audit.py`。
