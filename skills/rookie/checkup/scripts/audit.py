#!/usr/bin/env python3
"""Read-only log counter & resident overhead probe for Codex and DSH.

Stdlib only (Python 3.11+; zstd via Python 3.14+ compression.zstd, `zstd` CLI, or optional `zstandard`).
Outputs compact JSON (< 3 KB typical). Static config parsing stays in SKILL.md.

This is a fast path, not the source of truth: it only knows the log formats of the
client versions in VERIFIED_WITH. When a gate trips, SKILL.md switches the agent to
references/log-formats.md and an ad-hoc count.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

try:
    import tomllib
except ImportError:
    tomllib = None  # type: ignore[assignment]

try:
    from compression import zstd as _stdlib_zstd
except ImportError:
    _stdlib_zstd = None

try:  # pip install zstandard — 覆盖 Python 3.11~3.13（compression.zstd 只在 3.14+）
    import zstandard as _zstandard
except ImportError:
    _zstandard = None

HOME = Path.home()
ZSTD_BIN = shutil.which("zstd")

# Client versions whose log formats this script was last checked against.
VERIFIED_WITH = {"codex": "0.170.0", "dsh": "0.2.2-rc.5"}


def client_version(binary: str) -> str | None:
    exe = shutil.which(binary)
    if not exe:
        return None
    try:
        res = subprocess.run([exe, "--version"], capture_output=True, timeout=5, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    out = (res.stdout or res.stderr).decode("utf-8", errors="ignore").strip().splitlines()
    return out[0] if res.returncode == 0 and out else None

# Read-only shell commands counted for Codex heuristic SKILL.md reads (avoids rg/sed edit noise).
READ_CMD_RE = re.compile(r"(?:^|[;&|(]\s*)(?:cat|head|tail|less|bat|nl|sed\s+-n|awk|type|gc|Get-Content)\b", re.I)
SKILL_TAG_RE = re.compile(r"<skill>\s*<name>([^<]+)</name>")
SKILL_PATH_RE = re.compile(r"([A-Za-z0-9._-]+)[/\\]+SKILL\.md\b")
DSH_SKILL_CONTENT_RE = re.compile(r'<skill_content\s+name="([^"]+)"')


def iso_day(ts: float | int | None) -> str | None:
    if not ts:
        return None
    ts = ts / 1000.0 if ts > 1e12 else float(ts)
    return dt.datetime.fromtimestamp(ts, tz=dt.timezone.utc).strftime("%Y-%m-%d")


def to_epoch(val: Any) -> float | None:
    if isinstance(val, (int, float)):
        return val / 1000.0 if val > 1e12 else float(val)
    if isinstance(val, str) and val:
        try:
            return dt.datetime.fromisoformat(val.replace("Z", "+00:00")).timestamp()
        except ValueError:
            return None
    return None


def read_log(path: Path) -> tuple[str | None, str | None]:
    """Return (text, problem); problem is None, "no_decompressor" or "unreadable"."""
    if path.suffix.lower() not in (".zst", ".zstd"):
        try:
            return path.read_text(encoding="utf-8", errors="ignore"), None
        except OSError:
            return None, "unreadable"
    if not (_stdlib_zstd or ZSTD_BIN or _zstandard):
        return None, "no_decompressor"
    if _stdlib_zstd is not None:
        try:
            return _stdlib_zstd.decompress(path.read_bytes()).decode("utf-8", errors="ignore"), None
        except Exception:
            pass
    if ZSTD_BIN:
        try:
            res = subprocess.run([ZSTD_BIN, "-dc", str(path)], capture_output=True, timeout=30, check=False)
            if res.returncode == 0:
                return res.stdout.decode("utf-8", errors="ignore"), None
        except (OSError, subprocess.TimeoutExpired):
            pass
    if _zstandard is not None:
        try:
            with open(path, "rb") as fh, _zstandard.ZstdDecompressor().stream_reader(fh) as reader:
                return reader.read().decode("utf-8", errors="ignore"), None
        except Exception:
            pass
    return None, "unreadable"


def scan_skill_dirs(dirs: list[Path]) -> tuple[dict[str, int], list[str]]:
    """Return ({skill_name: desc_chars}, [duplicate_names]). Only reads active dirs."""
    seen_real: set[Path] = set()
    skills: dict[str, int] = {}
    dups: set[str] = set()
    for root in dirs:
        if not root.exists():
            continue
        for md in sorted(root.rglob("SKILL.md")):
            if "node_modules" in md.parts or ".checkup-trash" in md.parts or ".system" in md.parts:
                continue
            real = md.resolve() if md.exists() else md
            if real in seen_real:
                continue
            seen_real.add(real)
            txt = md.read_text(encoding="utf-8", errors="ignore")
            name, desc, hidden = md.parent.name, "", False
            fm = re.match(r"^---\s*\n([\s\S]*?)\n---", txt)
            if fm:
                nm = re.search(r"^name:\s*(.+)$", fm.group(1), re.M)
                dm = re.search(r"^description:\s*(.+)$", fm.group(1), re.M)
                if nm:
                    name = nm.group(1).strip().strip("\"'")
                if dm:
                    desc = dm.group(1).strip().strip("\"'")
                hidden = bool(re.search(r"^disable-model-invocation:\s*true\b", fm.group(1), re.M | re.I))
            if name in skills:
                dups.add(name)
            skills[name] = 0 if hidden else len(desc)
    return skills, sorted(dups)


def active_codex_skill_dirs(codex_home: Path) -> list[Path]:
    """User + shared dirs + latest version dir of *enabled* plugins only."""
    dirs = [codex_home / "skills", HOME / ".agents" / "skills"]
    cfg_p = codex_home / "config.toml"
    cache = codex_home / "plugins" / "cache"
    if cfg_p.exists() and cache.exists() and tomllib is not None:
        try:
            cfg = tomllib.loads(cfg_p.read_text(encoding="utf-8", errors="ignore"))
            for pid, pdata in (cfg.get("plugins") or {}).items():
                if not isinstance(pdata, dict) or not pdata.get("enabled", True) or "@" not in pid:
                    continue
                pname, mkt = pid.split("@", 1)
                pdir = cache / mkt / pname
                if pdir.is_dir():
                    vers = sorted((v for v in pdir.iterdir() if v.is_dir()), key=lambda x: x.stat().st_mtime)
                    if vers:
                        dirs.append(vers[-1])
        except Exception:
            pass
    return dirs


def audit_codex(days: int) -> dict[str, Any]:
    home = Path(os.environ.get("CODEX_HOME", str(HOME / ".codex"))).expanduser()
    if not home.exists():
        return {"installed": False}

    cutoff = time.time() - days * 86400
    sessions_root = home / "sessions"
    scanned = skipped = unreadable = recognized = 0
    log_versions: set[str] = set()
    mcp: dict[str, list[Any]] = {}  # name -> [calls, set(sessions), last_ts, failed]
    plugin_mcp: dict[str, list[Any]] = {}  # pid -> [calls, last_ts]
    sk_explicit: dict[str, list[Any]] = {}  # name -> [set(sessions), last_ts]
    sk_read: dict[str, list[Any]] = {}  # name -> [set(sessions), last_ts]
    host_skills_usage: dict[str, Any] | None = None
    usage_ts = 0.0

    files = sorted(
        ((p.stat().st_mtime, p) for p in sessions_root.rglob("rollout-*") if p.is_file() and p.stat().st_mtime >= cutoff),
        key=lambda x: x[0],
    ) if sessions_root.exists() else []

    for mt, p in files:
        text, problem = read_log(p)
        if problem == "no_decompressor":
            skipped += 1
            continue
        if problem:
            unreadable += 1
            continue
        if not text:
            continue
        scanned += 1
        sid = p.name
        for line in text.splitlines():
            if not any(k in line for k in ('"McpToolCall"', "<skill>", "SKILL.md", '"host_skills"', '"session_meta"')):
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = to_epoch(obj.get("timestamp")) or mt
            et, pl = obj.get("type"), obj.get("payload") or {}
            if et == "session_meta" and pl.get("cli_version"):
                log_versions.add(str(pl["cli_version"]))
            if ts < cutoff:  # a recently touched file can still hold old events
                continue

            if et == "event_msg" and pl.get("type") == "item_completed":
                it = pl.get("item") or {}
                if it.get("type") == "McpToolCall":
                    recognized += 1
                    srv = str(it.get("server") or "unknown")
                    rec = mcp.setdefault(srv, [0, set(), 0.0, 0])
                    rec[0] += 1
                    rec[1].add(sid)
                    rec[2] = max(rec[2], ts)
                    if str(it.get("status") or "").lower() in ("failed", "error"):
                        rec[3] += 1
                    pid = it.get("pluginId") or it.get("plugin_id")
                    if pid:
                        pr = plugin_mcp.setdefault(str(pid), [0, 0.0])
                        pr[0] += 1
                        pr[1] = max(pr[1], ts)
                elif it.get("type") == "CommandExecution":
                    cmd = str(it.get("command") or "")
                    if "SKILL.md" in cmd and READ_CMD_RE.search(cmd):
                        recognized += 1
                        for m in SKILL_PATH_RE.finditer(cmd):
                            rec = sk_read.setdefault(m.group(1), [set(), 0.0])
                            rec[0].add(sid)
                            rec[1] = max(rec[1], ts)

            elif et == "response_item":
                if pl.get("role") == "user":
                    for c in (pl.get("content") or []):
                        t = c.get("text") if isinstance(c, dict) else ""
                        if t and "<skill>" in t:
                            for m in SKILL_TAG_RE.finditer(t):
                                recognized += 1
                                rec = sk_explicit.setdefault(m.group(1).strip(), [set(), 0.0])
                                rec[0].add(sid)
                                rec[1] = max(rec[1], ts)
                elif pl.get("type") == "function_call" and pl.get("name") in ("exec_command", "shell", "shell_command"):
                    cmd = str(pl.get("arguments") or "")
                    if "SKILL.md" in cmd and READ_CMD_RE.search(cmd):
                        recognized += 1
                        for m in SKILL_PATH_RE.finditer(cmd):
                            rec = sk_read.setdefault(m.group(1), [set(), 0.0])
                            rec[0].add(sid)
                            rec[1] = max(rec[1], ts)

            if '"host_skills"' in line and '"usage"' in line and ts >= usage_ts:
                stack = [obj]
                while stack:
                    cur = stack.pop()
                    if isinstance(cur, dict):
                        hs = cur.get("host_skills")
                        if isinstance(hs, dict) and isinstance(hs.get("usage"), dict):
                            host_skills_usage, usage_ts = hs["usage"], ts
                            recognized += 1
                            break
                        stack.extend(cur.values())
                    elif isinstance(cur, list):
                        stack.extend(cur)

    active_skills, dups = scan_skill_dirs(active_codex_skill_dirs(home))
    used_names = set(sk_explicit) | set(sk_read)
    unused_active = sorted(
        ((n, ch) for n, ch in active_skills.items() if n not in used_names and ch > 0),
        key=lambda x: -x[1],
    )

    return {
        "installed": True,
        "version": client_version("codex"),
        "verified_with": VERIFIED_WITH["codex"],
        "log_versions": sorted(log_versions),
        "sessions_scanned": scanned,
        "skipped_zst": skipped,
        "unreadable_logs": unreadable,
        "recognized_events": recognized,
        "schema_unrecognized": scanned >= 5 and recognized == 0,
        "skill_usage_unverified": bool(active_skills) and (scanned == 0 or not used_names),
        "host_skills_usage": host_skills_usage,
        "active_skills_count": len(active_skills),
        "duplicate_skills": dups,
        "skills_used_fmt": "[explicit_sessions, read_sessions_heuristic, last_day]",
        "skills_used": {
            n: [
                len(sk_explicit[n][0]) if n in sk_explicit else 0,
                len(sk_read[n][0]) if n in sk_read else 0,
                iso_day(max(sk_explicit[n][1] if n in sk_explicit else 0, sk_read[n][1] if n in sk_read else 0)),
            ]
            for n in sorted(used_names)
        },
        "unused_active_skills_count": len(unused_active),
        "unused_active_top15": [f"{n}({ch}c)" for n, ch in unused_active[:15]],
        "mcp_used": {
            k: {"calls": v[0], "sessions": len(v[1]), "failed": v[3], "last": iso_day(v[2])}
            for k, v in sorted(mcp.items())
        },
        "plugin_mcp_used": {k: {"calls": v[0], "last": iso_day(v[1])} for k, v in sorted(plugin_mcp.items())},
    }


def audit_dsh(days: int) -> dict[str, Any]:
    home = Path(os.environ.get("DSH_HOME", str(HOME / ".dsh"))).expanduser()
    if not home.exists():
        return {"installed": False}

    cutoff = time.time() - days * 86400
    sessions_root = home / "sessions"
    scanned = skipped = unreadable = recognized = 0
    mcp: dict[str, list[Any]] = {}  # server -> [calls, set(sessions), last_ts]
    sk_user: dict[str, list[Any]] = {}  # name -> [set(sessions), last_ts]
    sk_model: dict[str, list[Any]] = {}  # name -> [set(sessions), last_ts]
    header_overhead: dict[str, Any] | None = None
    hdr_ts = 0.0
    catalog_chars: int | None = None
    cat_ts = 0.0

    files = sorted(
        ((p.stat().st_mtime, p) for p in sessions_root.rglob("session*.jsonl*") if p.is_file() and p.suffix != ".lock" and p.stat().st_mtime >= cutoff),
        key=lambda x: x[0],
    ) if sessions_root.exists() else []

    for mt, p in files:
        text, problem = read_log(p)
        if problem == "no_decompressor":
            skipped += 1
            continue
        if problem:
            unreadable += 1
            continue
        if not text:
            continue
        scanned += 1
        sid = p.parent.name
        for line in text.splitlines():
            if not any(k in line for k in ('"tool/call"', '"request/header"', "<skill_content", "<available_skills>")):
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            ts = to_epoch(obj.get("time")) or mt
            et, data = obj.get("type"), obj.get("data") or {}

            if et in ("tool/call", "user/message") and ts < cutoff:
                if "<available_skills>" not in line:
                    continue

            if et == "tool/call":
                recognized += 1
                tname = str(data.get("name") or "")
                if tname == "skill":
                    raw_args = data.get("arguments")
                    sname = None
                    if isinstance(raw_args, str):
                        try:
                            sname = json.loads(raw_args).get("name")
                        except json.JSONDecodeError:
                            pass
                    elif isinstance(raw_args, dict):
                        sname = raw_args.get("name")
                    if sname:
                        rec = sk_model.setdefault(str(sname), [set(), 0.0])
                        rec[0].add(sid)
                        rec[1] = max(rec[1], ts)
                elif tname.startswith("mcp__"):
                    srv = tname.split("__", 2)[1]
                    rec = mcp.setdefault(srv, [0, set(), 0.0])
                    rec[0] += 1
                    rec[1].add(sid)
                    rec[2] = max(rec[2], ts)

            elif et == "user/message":
                for c in (data.get("content") or []):
                    t = c.get("text") if isinstance(c, dict) else ""
                    if not t:
                        continue
                    if "<skill_content" in t:
                        for m in DSH_SKILL_CONTENT_RE.finditer(t):
                            recognized += 1
                            rec = sk_user.setdefault(m.group(1).strip(), [set(), 0.0])
                            rec[0].add(sid)
                            rec[1] = max(rec[1], ts)
                    if "<available_skills>" in t and ts >= cat_ts:
                        catalog_chars, cat_ts = len(t), ts
                        recognized += 1

            elif et == "request/header" and ts >= hdr_ts:
                tools = (data.get("header") or {}).get("tools")
                if isinstance(tools, list):
                    mcp_tools = [t for t in tools if isinstance(t, dict) and str(t.get("name") or "").startswith("mcp__")]
                    total_chars = len(json.dumps(tools, ensure_ascii=False)) if tools else 0
                    # DSH 新版把 bridge 提供的工具（dsh_host 等）写成裸名，没有 mcp__ 前缀，
                    # 按前缀归因会得到 0 —— 这时只能拿总量判预算，并明确告知归因不可用。
                    # Built-in tools are always bare, so bare names can hide MCP tools even when some
                    # carry the prefix; the total is the only number that never under-reports.
                    attribution = "no_tools" if not tools else ("prefix_partial" if mcp_tools else "unavailable_bare_names")
                    mcp_chars = len(json.dumps(mcp_tools, ensure_ascii=False)) if mcp_tools else 0
                    header_overhead = {
                        "tools_count": len(tools),
                        "tools_schema_chars": total_chars,
                        "mcp_tools_count": len(mcp_tools),
                        "mcp_schema_chars": mcp_chars,
                        "mcp_attribution": attribution,
                        "budget_warnings": (
                            (["mcp_schema_over_20k"] if mcp_chars > 20000 else [])
                            + (["tool_schema_total_over_20k"] if total_chars > 20000 else [])
                        ),
                        "observed": iso_day(ts),
                    }
                    hdr_ts = ts
                    recognized += 1

    cwd = Path.cwd()
    active_skills, dups = scan_skill_dirs([cwd / ".dsh/skills", cwd / ".agents/skills", home / "skills", HOME / ".agents/skills"])
    used_names = set(sk_user) | set(sk_model)
    unused_active = sorted(
        ((n, ch) for n, ch in active_skills.items() if n not in used_names and ch > 0),
        key=lambda x: -x[1],
    )

    return {
        "installed": True,
        "version": client_version("dsh"),
        "verified_with": VERIFIED_WITH["dsh"],
        "sessions_scanned": scanned,
        "skipped_zst": skipped,
        "unreadable_logs": unreadable,
        "zstd_available": bool(_stdlib_zstd or ZSTD_BIN or _zstandard),
        # 有压缩日志却被跳过 → 统计不可信，必须报警而不是把扩展判成吃灰
        "zstd_missing_gate": skipped > 0 and not (_stdlib_zstd or ZSTD_BIN or _zstandard),
        "recognized_events": recognized,
        "schema_unrecognized": scanned >= 5 and recognized == 0,
        "skill_usage_unverified": bool(active_skills) and (scanned == 0 or not used_names),
        "overhead": {"request_header": header_overhead, "skill_catalog_chars": catalog_chars},
        "active_skills_count": len(active_skills),
        "duplicate_skills": dups,
        "skills_used_fmt": "[user_sessions, model_sessions, last_day]",
        "skills_used": {
            n: [
                len(sk_user[n][0]) if n in sk_user else 0,
                len(sk_model[n][0]) if n in sk_model else 0,
                iso_day(max(sk_user[n][1] if n in sk_user else 0, sk_model[n][1] if n in sk_model else 0)),
            ]
            for n in sorted(used_names)
        },
        "unused_active_skills_count": len(unused_active),
        "unused_active_top15": [f"{n}({ch}c)" for n, ch in unused_active[:15]],
        "mcp_used": {k: {"calls": v[0], "sessions": len(v[1]), "last": iso_day(v[2])} for k, v in sorted(mcp.items())},
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Compact read-only session usage & overhead audit for Codex/DSH")
    ap.add_argument("--agent", choices=("codex", "dsh", "all"), default="all")
    ap.add_argument("--days", type=int, default=30)
    args = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")  # Windows consoles/redirects default to a legacy code page
    out: dict[str, Any] = {
        "days": args.days,
        "zstd": "stdlib" if _stdlib_zstd else ("cli" if ZSTD_BIN else ("zstandard" if _zstandard else "none")),
    }
    if args.agent in ("codex", "all"):
        out["codex"] = audit_codex(args.days)
    if args.agent in ("dsh", "all"):
        out["dsh"] = audit_dsh(args.days)
    print(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
