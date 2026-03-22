#!/usr/bin/env python3
"""
Session Digest Script
Extracts human messages and key assistant responses from Claude Code JSONL session files.
Generates readable markdown digests for project memory.

Usage:
    python scripts/digest_sessions.py                    # Digest all sessions
    python scripts/digest_sessions.py --session UUID      # Digest one session
    python scripts/digest_sessions.py --since 2026-03-01  # Sessions after date
    python scripts/digest_sessions.py --interactive-only   # Skip scheduled task sessions
"""

import json
import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

SESSIONS_DIR = Path.home() / ".claude/projects/-Users-joeyanuff-m2-Development-claude-code-tips"
OUTPUT_DIR = Path(__file__).parent.parent / "analysis" / "session-digests"


def extract_text_from_content(content):
    """Extract readable text from message content (str or list of blocks)."""
    if isinstance(content, str):
        return content.strip()
    elif isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    text = block.get("text", "").strip()
                    if text:
                        texts.append(text)
                elif block.get("type") == "tool_use":
                    tool = block.get("name", "unknown")
                    inp = block.get("input", {})
                    # Summarize tool calls concisely
                    if tool == "Bash":
                        cmd = inp.get("command", "")[:100]
                        texts.append(f"[Tool: Bash] `{cmd}`")
                    elif tool == "Read":
                        texts.append(f"[Tool: Read] {inp.get('file_path', '?')}")
                    elif tool == "Write":
                        texts.append(f"[Tool: Write] {inp.get('file_path', '?')}")
                    elif tool == "Edit":
                        texts.append(f"[Tool: Edit] {inp.get('file_path', '?')}")
                    elif tool in ("Grep", "Glob"):
                        texts.append(f"[Tool: {tool}] {inp.get('pattern', '?')}")
                    elif tool == "Agent":
                        texts.append(f"[Tool: Agent] {inp.get('description', '?')}")
                    elif tool == "WebFetch":
                        texts.append(f"[Tool: WebFetch] {inp.get('url', '?')[:80]}")
                    elif tool == "WebSearch":
                        texts.append(f"[Tool: WebSearch] {inp.get('query', '?')[:80]}")
                    else:
                        texts.append(f"[Tool: {tool}]")
                elif block.get("type") == "tool_result":
                    pass  # Skip tool results (too verbose)
        return "\n".join(texts)
    return ""


def is_scheduled_task(messages):
    """Check if session was a scheduled task (not interactive)."""
    if not messages:
        return False
    first_msg = messages[0]
    content = extract_text_from_content(first_msg.get("message", {}).get("content", ""))
    return "<scheduled-task" in content or "<command-message>fetch-bookmarks</command-message>" in content


def digest_session(filepath):
    """Parse a JSONL session file and extract the conversation."""
    messages = []
    session_id = filepath.stem
    first_timestamp = None

    with open(filepath) as fh:
        for line in fh:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue

            if not first_timestamp and "timestamp" in d:
                first_timestamp = d["timestamp"]

            msg_type = d.get("type", "")
            if msg_type not in ("user", "assistant"):
                continue

            message = d.get("message", {})
            role = message.get("role", msg_type)
            content = extract_text_from_content(message.get("content", ""))
            timestamp = d.get("timestamp", "")

            if content:
                messages.append({
                    "role": role,
                    "content": content,
                    "timestamp": timestamp,
                })

    return {
        "session_id": session_id,
        "first_timestamp": first_timestamp,
        "messages": messages,
        "is_scheduled": is_scheduled_task(messages),
    }


def format_digest(session_data, verbose=False):
    """Format a session digest as markdown."""
    lines = []
    sid = session_data["session_id"]
    ts = session_data["first_timestamp"]
    date_str = ts[:10] if ts else "unknown"
    messages = session_data["messages"]
    is_sched = session_data["is_scheduled"]

    human_msgs = [m for m in messages if m["role"] == "user"]
    assistant_msgs = [m for m in messages if m["role"] == "assistant"]

    lines.append(f"## Session: {date_str}")
    lines.append(f"- **ID:** `{sid}`")
    lines.append(f"- **Resume:** `claude --resume {sid}`")
    lines.append(f"- **Messages:** {len(human_msgs)} human, {len(assistant_msgs)} assistant")
    lines.append(f"- **Type:** {'Scheduled task' if is_sched else 'Interactive'}")
    lines.append("")

    if not verbose:
        # Summary mode: just human messages, trimmed
        lines.append("### Human Messages")
        lines.append("")
        for i, m in enumerate(human_msgs):
            content = m["content"]
            # Strip system reminders and command caveats
            content = _clean_content(content)
            if not content.strip():
                continue
            # Trim very long messages
            if len(content) > 500:
                content = content[:500] + "..."
            ts_short = m["timestamp"][11:16] if len(m["timestamp"]) > 16 else ""
            lines.append(f"**[{i+1}]** {ts_short}")
            lines.append(content)
            lines.append("")
    else:
        # Verbose mode: full conversation
        lines.append("### Conversation")
        lines.append("")
        for m in messages:
            content = _clean_content(m["content"])
            if not content.strip():
                continue
            role_label = "**Joey:**" if m["role"] == "user" else "**Claude:**"
            if len(content) > 1000 and not verbose:
                content = content[:1000] + "..."
            lines.append(f"{role_label}")
            lines.append(content)
            lines.append("")

    return "\n".join(lines)


def _clean_content(text):
    """Remove system reminders, command caveats, and other noise."""
    # Remove system reminders
    import re
    text = re.sub(r'<system-reminder>.*?</system-reminder>', '', text, flags=re.DOTALL)
    text = re.sub(r'<local-command-caveat>.*?</local-command-caveat>', '', text, flags=re.DOTALL)
    text = re.sub(r'<command-message>.*?</command-message>', '', text, flags=re.DOTALL)
    text = re.sub(r'<command-name>.*?</command-name>', '', text, flags=re.DOTALL)
    text = re.sub(r'<command-args>.*?</command-args>', '', text, flags=re.DOTALL)
    text = re.sub(r'<scheduled-task[^>]*>.*?</scheduled-task>', '', text, flags=re.DOTALL)
    text = re.sub(r'<local-command-stdout>.*?</local-command-stdout>', '[/cost output]', text, flags=re.DOTALL)
    text = re.sub(r'<task-notification>.*?</task-notification>', '[task notification]', text, flags=re.DOTALL)
    text = re.sub(r'Full transcript available at:.*', '', text)
    # Strip ANSI escape codes
    text = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', text)
    # Clean up whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def main():
    parser = argparse.ArgumentParser(description="Digest Claude Code session files")
    parser.add_argument("--session", help="Digest a specific session by UUID")
    parser.add_argument("--since", help="Only sessions after this date (YYYY-MM-DD)")
    parser.add_argument("--interactive-only", action="store_true", help="Skip scheduled task sessions")
    parser.add_argument("--verbose", action="store_true", help="Include assistant messages")
    parser.add_argument("--output", choices=["stdout", "files", "combined"], default="combined",
                        help="Output mode: stdout, individual files, or combined markdown")
    args = parser.parse_args()

    # Find session files
    session_files = sorted(SESSIONS_DIR.glob("*.jsonl"))

    if args.session:
        session_files = [f for f in session_files if args.session in f.stem]
        if not session_files:
            print(f"No session found matching: {args.session}")
            sys.exit(1)

    # Parse all sessions
    sessions = []
    for f in session_files:
        try:
            data = digest_session(f)
            if data["messages"]:  # Skip empty sessions
                sessions.append(data)
        except Exception as e:
            print(f"Error parsing {f.name}: {e}", file=sys.stderr)

    # Filter
    if args.since:
        sessions = [s for s in sessions if (s["first_timestamp"] or "") >= args.since]

    if args.interactive_only:
        sessions = [s for s in sessions if not s["is_scheduled"]]

    # Sort by timestamp
    sessions.sort(key=lambda s: s["first_timestamp"] or "")

    print(f"Found {len(sessions)} sessions", file=sys.stderr)

    if args.output == "stdout":
        for s in sessions:
            print(format_digest(s, verbose=args.verbose))
            print("\n---\n")

    elif args.output == "files":
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        for s in sessions:
            date = (s["first_timestamp"] or "unknown")[:10]
            outfile = OUTPUT_DIR / f"{date}_{s['session_id'][:8]}.md"
            outfile.write_text(format_digest(s, verbose=args.verbose))
            print(f"Wrote {outfile}")

    elif args.output == "combined":
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        outfile = OUTPUT_DIR / "all_sessions_digest.md"
        lines = [
            "# Claude Code Session Digests",
            "",
            f"> Generated: {datetime.now().isoformat()[:19]}",
            f"> Sessions: {len(sessions)}",
            f"> Source: `{SESSIONS_DIR}`",
            "",
            "---",
            "",
        ]
        for s in sessions:
            lines.append(format_digest(s, verbose=args.verbose))
            lines.append("\n---\n")

        outfile.write_text("\n".join(lines))
        print(f"Wrote {outfile} ({len(sessions)} sessions)")


if __name__ == "__main__":
    main()
