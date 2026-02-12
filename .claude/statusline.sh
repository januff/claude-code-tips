#!/usr/bin/env python3
"""Claude Code status line for claude-code-tips project.

Three-line display per statusline-spec.md:
  Line 1: Project Pulse — project name, handoff, tweets, enrichment, wrap-up
  Line 2: Session Mechanics — model, thinking, context, git, agents
  Line 3: Rotating Quote — random high-signal tweet from DB
"""
import json
import os
import re
import sqlite3
import subprocess
import sys
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
        clean = iso_str.split("+")[0].split("Z")[0].rstrip(".")
        if "T" not in clean:
            return ""
        dt = datetime.fromisoformat(clean).replace(tzinfo=timezone.utc)
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
    if not cwd:
        cwd = os.getcwd()

    ctx_info = inp.get("context_window", {})
    model_info = inp.get("model", {})
    agent_info = inp.get("agent", {})

    status_path = Path(cwd) / "STATUS.json"
    db_path = Path(cwd) / "data" / "claude_code_tips_v2.db"

    # ── Line 1: Project Pulse ──────────────────────────────────
    handoff = "\U0001f4cb none"
    updated_rel = ""
    tweet_str = "\U0001f426 ??"
    enrich_str = "enriched: ??/??/??"

    if status_path.exists():
        try:
            status = json.loads(status_path.read_text())
            at = status.get("active_task")
            if at and isinstance(at, dict):
                desc = at.get("description", "")
                plan = at.get("plan", "")
                if desc:
                    # Truncate long descriptions
                    label = desc[:30] + "..." if len(desc) > 30 else desc
                    handoff = f"\U0001f4cb {label}"
                elif plan:
                    h = plan.split("/")[-1]
                    h = h.removeprefix("TASK_PLAN").removesuffix(".md").strip("-_ ")
                    handoff = f"\U0001f4cb {h}" if h else "\U0001f4cb active"

            updated_at = status.get("updated_at", "")
            if updated_at:
                updated_rel = relative_time(updated_at)

            last_fetch = (status.get("key_dates") or {}).get("last_bookmark_fetch", "")
            fetch_age = days_since(last_fetch) if last_fetch else ""
        except Exception:
            fetch_age = ""
    else:
        fetch_age = ""

    if db_path.exists():
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            c = conn.cursor()
            tweets = c.execute("SELECT count(*) FROM tweets").fetchone()[0]
            tips = c.execute("SELECT count(*) FROM tips").fetchone()[0]
            kw = c.execute("SELECT count(*) FROM tips WHERE primary_keyword IS NOT NULL").fetchone()[0]
            summ = c.execute("SELECT count(*) FROM tips WHERE holistic_summary IS NOT NULL").fetchone()[0]
            media_analyzed = c.execute(
                "SELECT count(*) FROM media WHERE workflow_summary IS NOT NULL OR vision_description IS NOT NULL"
            ).fetchone()[0]
            media_total = c.execute("SELECT count(*) FROM media").fetchone()[0]
            conn.close()

            age_part = f" ({fetch_age})" if fetch_age else ""
            tweet_str = f"\U0001f426 {tweets}{age_part}"

            kw_pct = str(kw * 100 // tips) if tips > 0 else "??"
            sum_pct = str(summ * 100 // tips) if tips > 0 else "??"
            med_pct = str(media_analyzed * 100 // media_total) if media_total > 0 else "??"
            enrich_str = f"enriched: {kw_pct}/{sum_pct}/{med_pct}"
        except Exception:
            pass

    parts1 = ["claude-code-tips", handoff, tweet_str, enrich_str]
    if updated_rel:
        parts1.append(f"wrapped: {updated_rel}")
    line1 = " | ".join(parts1)

    # ── Line 2: Session Mechanics ──────────────────────────────
    # Model
    model_id = model_info.get("id", "")
    if "opus" in model_id:
        model_name = "opus-4.6"
    elif "sonnet" in model_id:
        model_name = "sonnet-4.5"
    elif "haiku" in model_id:
        model_name = "haiku-4.5"
    elif model_info.get("display_name"):
        model_name = model_info["display_name"].lower()
    else:
        model_name = "??"

    # Context
    remaining = ctx_info.get("remaining_percentage")
    ctx = f"ctx {100 - int(remaining)}%" if remaining is not None else ""

    # Git
    git_info = "\U0001f33f ??"
    if run(["git", "rev-parse", "--git-dir"], cwd=cwd):
        branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=cwd) or "??"
        # Clean/dirty
        check = subprocess.run(
            ["git", "diff-index", "--quiet", "HEAD", "--"],
            capture_output=True, cwd=cwd, timeout=2,
            env={**os.environ, "GIT_OPTIONAL_LOCKS": "0"}
        )
        if check.returncode != 0:
            # Count dirty files
            diff_out = run(["git", "diff-index", "--name-only", "HEAD", "--"], cwd=cwd)
            count = len(diff_out.splitlines()) if diff_out else 0
            dirty = f"+{count}" if count > 0 else "dirty"
        else:
            dirty = "clean"

        # Ahead/behind
        upstream = run(["git", "rev-parse", "--abbrev-ref", "@{upstream}"], cwd=cwd)
        ahead_str = ""
        if upstream:
            ahead = run(["git", "rev-list", "--count", f"{upstream}..HEAD"], cwd=cwd)
            if ahead and int(ahead) > 0:
                ahead_str = f" ahead {ahead}"

        git_info = f"\U0001f33f {branch} {dirty}{ahead_str}"

    # Agents
    agent_name = agent_info.get("name", "")
    agents = f"agent:{agent_name}" if agent_name else "solo"

    parts2 = [model_name]
    if ctx:
        parts2.append(ctx)
    parts2.append(git_info)
    parts2.append(agents)
    line2 = " | ".join(parts2)

    # ── Line 3: Rotating Quote ─────────────────────────────────
    fallback = '\U0001f4ac "Verification is the most important tip" \u2014 @bcherny'
    line3 = fallback

    if db_path.exists():
        try:
            conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
            c = conn.cursor()
            row = c.execute("""
                SELECT text, handle
                FROM tweets
                WHERE likes > 500
                  AND text IS NOT NULL
                  AND LENGTH(text) < 200
                  AND LENGTH(text) > 20
                ORDER BY RANDOM()
                LIMIT 1
            """).fetchone()
            conn.close()

            if row:
                text, handle = row
                # Strip URLs
                text = re.sub(r'https?://\S+', '', text).strip()
                # Flatten newlines
                text = re.sub(r'\s*\n\s*', ' ', text).strip()
                # Truncate at word boundary
                if len(text) > 100:
                    text = text[:97].rsplit(' ', 1)[0] + "\u2026"
                if text:
                    at = f"@{handle}" if not handle.startswith("@") else handle
                    line3 = f'\U0001f4ac "{text}" \u2014 {at}'
        except Exception:
            pass

    print(f"{line1}\n{line2}\n{line3}", end="")


if __name__ == "__main__":
    main()
