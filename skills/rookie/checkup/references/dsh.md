# DSH 停用与回滚命令

在确认清理清单后按需查阅。动手修改 `$DSH_HOME/profiles/<profile>/package.json` 或 `cordis.patch.yml`（默认 `~/.dsh`）前，先各自备份为 `*.bak.<YYYY-MM-DD>`。

- **停用 / 移除插件**：运行 `dsh plugin --profile <profile> remove <包名>`，或从 `package.json` 的 `dsh.profile.bundles` 与 `dependencies` 中移除对应项（回退：用备份恢复或 `dsh plugin --profile <profile> add <包名>`）。
- **停用 MCP**：在 `cordis.patch.yml` 中注释或移除对应 `@deepseek-ai/dsh-mcp-client` 的 `insert` 项（保留注释便于随时取消注释恢复）。
- **移走本地 Skill**：把目录移入 `~/.agents/.checkup-trash/<YYYY-MM-DD>/`（回退：`mv` 回原路径）。
- **改完核对**：对非 `desktop` profile 跑 `dsh --profile <profile> --dump-config` 确认无新增报错，再复跑 `audit.py`。
