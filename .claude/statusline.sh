#!/usr/bin/env python3
"""Claude Code status line for claude-code-tips project.

Line 1: Project pulse — handoff, tweets, enrichment, last wrap-up
Line 2: Session mechanics — git, context, chrome, agents

Reads STATUS.json + DB on every refresh for live project state.
"""
import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path


def run(cmd, cwd=None):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=2, cwd=cwd,
                           env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"})
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


def relative_time(iso_str):
    try:
        # Strip timezone for parsing, assume UTC-ish
        clean = iso_str.split("+")[0].split("Z")[0].rstrip(".")
        if "T" in clean:
            dt = datetime.fromisoformat(clean).replace(tzinfo=timezone.utc)
        else:
            return ""
        diff = (datetime.now(timezone.utc) - dt).total_seconds()
        if diff < 60:
            return "now"
        elif diff < 3600:
            return f"{int(diff // 60)}m ago"
        elif diff < 86400:
            return f"{int(diff // 3600)}h ago"
        else:
            return f"{int(diff // 86400)}d ago"
    except Exception:
        return ""


def days_since(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
        diff = (datetime.now(timezone.utc) - dt).total_seconds()
        return f"{int(diff // 86400)}d"
    except Exception:
        return ""


def main():
    inp = json.loads(sys.stdin.read())
    cwd = inp.get("workspace", {}).get("project_dir") or inp.get("workspace", {}).get("current_dir", "")
    remaining = inp.get("context_window", {}).get("remaining_percentage")
    agent_name = inp.get("agent", {}).get("name", "")

    if not cwd:
        cwd = os.getcwd()

    status_path = Path(cwd) / "STATUS.json"
    db_path = Path(cwd) / "data" / "claude_code_tips_v2.db"

    # ── Line 1: Project Pulse ──
    handoff = "none"
    updated_rel = ""
    tweet_count = ""
    fetch_age = ""
    kw_pct = summary_pct = media_pct = ""

    if status_path.exists():
        try:
            status = json.loads(status_path.read_text())
            at = status.get("active_task")
            if at and isinstance(at, dict) and at.get("handoff"):
                h = at["handoff"].split("/")[-1]
                h = h.removeprefix("HANDOFF_").removesuffix(".md")
                handoff = h

            updated_at = status.get("updated_at", "")
            if updated_at:
                updated_rel = relative_time(updated_at)

            last_fetch = (status.get("key_dates") or {}).get("last_bookmark_fetch", "")
            if last_fetch:
                fetch_age = days_since(last_fetch)
        except Exception:
            pass

    if db_path.exists():
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            c = conn.cursor()
            tweets = c.execute("SELECT count(*) FROM tweets").fetchone()[0]
            tips = c.execute("SELECT count(*) FROM tips").fetchone()[0]
            kw = c.execute("SELECT count(*) FROM tips WHERE primary_keyword IS NOT NULL").fetchone()[0]
            summ = c.execute("SELECT count(*) FROM tips WHERE holistic_summary IS NOT NULL").fetchone()[0]
            media = c.execute("SELECT count(DISTINCT tweet_id) FROM media").fetchone()[0]
            conn.close()

            tweet_count = str(tweets)
            if tips > 0:
                kw_pct = str(kw * 100 // tips)
                summary_pct = str(summ * 100 // tips)
            if tweets > 0:
                media_pct = str(media * 100 // tweets)
        except Exception:
            pass

    parts1 = []
    parts1.append(handoff)
    if tweet_count:
        t = f"{tweet_count}tw"
        if fetch_age:
            t += f" (fetch: {fetch_age})"
        parts1.append(t)
    if kw_pct:
        parts1.append(f"kw:{kw_pct}% sum:{summary_pct}% med:{media_pct}%")
    if updated_rel:
        parts1.append(f"wrap: {updated_rel}")

    line1 = " | ".join(parts1)

    # ── Line 2: Session Mechanics ──
    git_info = ""
    if run(["git", "rev-parse", "--git-dir"], cwd=cwd):
        branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd)
        dirty = ""
        if run(["git", "diff-index", "HEAD", "--"], cwd=cwd) is not None:
            check = subprocess.run(
                ["git", "diff-index", "--quiet", "HEAD", "--"],
                capture_output=True, cwd=cwd, timeout=2,
                env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
            )
            if check.returncode != 0:
                dirty = "*"

        upstream = run(["git", "rev-parse", "--abbrev-ref", "@{upstream}"], cwd=cwd)
        ab = ""
        if upstream:
            ahead = run(["git", "rev-list", "--count", f"{upstream}..HEAD"], cwd=cwd)
            behind = run(["git", "rev-list", "--count", f"HEAD..{upstream}"], cwd=cwd)
            if ahead and int(ahead) > 0:
                ab += f"+{ahead}"
            if behind and int(behind) > 0:
                ab += f"-{behind}"

        git_info = f"{branch}{dirty}"
        if ab:
            git_info += f" {ab}"

    ctx = ""
    if remaining is not None:
        used = 100 - int(remaining)
        ctx = f"ctx:{used}%"

    # Chrome — quick heuristic check
    chrome = "chrome:off"
    try:
        r = subprocess.run(["pgrep", "-f", "claude.*chrome"], capture_output=True, timeout=1)
        if r.returncode == 0:
            chrome = "chrome:on"
    except Exception:
        pass

    # Agents
    agents = "solo"
    if agent_name:
        agents = f"agent:{agent_name}"

    parts2 = []
    if git_info:
        parts2.append(git_info)
    if ctx:
        parts2.append(ctx)
    parts2.append(chrome)
    parts2.append(agents)

    line2 = " | ".join(parts2)

    print(f"{line1}\n{line2}", end="")


if __name__ == "__main__":
    main()
