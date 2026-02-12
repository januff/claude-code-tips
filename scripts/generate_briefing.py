#!/usr/bin/env python3
"""
Generate a morning briefing from tip analysis output.

Takes the JSON analysis from analyze_new_tips.py and formats it as a readable
markdown morning report with tip summaries, engagement metrics, proposed actions,
and context links.

Usage:
    python scripts/generate_briefing.py --analysis analysis.json
    python scripts/generate_briefing.py --analysis analysis.json --output analysis/daily/
    python scripts/generate_briefing.py --analysis analysis.json --dry-run

    # Pipeline usage (stdin):
    python scripts/analyze_new_tips.py --since 2026-02-10 | python scripts/generate_briefing.py

Output: Markdown briefing saved to analysis/daily/YYYY-MM-DD-briefing.md
"""

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "claude_code_tips_v2.db"
DEFAULT_OUTPUT_DIR = ROOT / "analysis" / "daily"

# Category display config
CATEGORY_CONFIG = {
    "ACT_NOW": {"icon": "[!!]", "label": "Act Now", "color": "high-signal"},
    "EXPERIMENT": {"icon": "[?]", "label": "Experiment Candidate", "color": "interesting"},
    "NOTED": {"icon": "[i]", "label": "Noted", "color": "informational"},
    "NOISE": {"icon": "[-]", "label": "Low Signal", "color": "skip"},
}


def get_db_stats(db_path: Path) -> dict:
    """Get current database statistics for the briefing header."""
    if not db_path.exists():
        return {}

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    stats = {}
    try:
        row = conn.execute("SELECT COUNT(*) as n FROM tweets").fetchone()
        stats["total_tweets"] = row["n"]

        row = conn.execute(
            "SELECT COUNT(*) as n FROM tips WHERE holistic_summary IS NOT NULL"
        ).fetchone()
        stats["enriched"] = row["n"]

        row = conn.execute(
            "SELECT COUNT(DISTINCT parent_tweet_id) as n FROM thread_replies"
        ).fetchone()
        stats["threads"] = row["n"]

        row = conn.execute("SELECT COUNT(*) as n FROM thread_replies").fetchone()
        stats["replies"] = row["n"]

        row = conn.execute(
            "SELECT COUNT(*) as n FROM links WHERE llm_summary IS NOT NULL"
        ).fetchone()
        stats["links_summarized"] = row["n"]
    except Exception:
        pass
    finally:
        conn.close()

    return stats


def format_tip_entry(entry: dict, verbose: bool = True) -> list[str]:
    """Format a single tip entry as markdown lines."""
    lines = []
    likes = entry.get("likes", 0)
    author = entry.get("author", "unknown")
    keyword = entry.get("primary_keyword", "")
    one_liner = entry.get("one_liner", "")
    text_preview = entry.get("text_preview", "")
    reason = entry.get("reason", "")
    action = entry.get("proposed_action")
    relevance = entry.get("relevance", [])
    tweet_id = entry.get("tweet_id", "")

    # Title line with engagement
    keyword_display = f" `{keyword}`" if keyword else ""
    lines.append(f"- **@{author}** ({likes:,} likes){keyword_display}")

    # Summary or text preview
    display_text = one_liner or text_preview
    if display_text:
        lines.append(f"  {display_text}")

    if verbose:
        # Classification reason
        if reason:
            lines.append(f"  *Why:* {reason}")

        # Proposed action
        if action:
            lines.append(f"  *Action:* {action}")

        # Relevance matches (compact)
        if relevance:
            rel_str = ", ".join(relevance[:3])
            if len(relevance) > 3:
                rel_str += f" (+{len(relevance) - 3} more)"
            lines.append(f"  *Matches:* {rel_str}")

    # Link to tweet
    if tweet_id:
        lines.append(f"  [View tweet](https://x.com/i/status/{tweet_id})")

    lines.append("")  # blank line between entries
    return lines


def generate_briefing(analysis: dict, db_path: Path = DB_PATH, verbose: bool = True) -> str:
    """Generate a markdown briefing from analysis data.

    Args:
        analysis: The JSON analysis dict from analyze_new_tips.py
        db_path: Path to the SQLite database for stats
        verbose: Include detailed per-tip reasons and actions

    Returns:
        Formatted markdown string
    """
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")

    categories = analysis.get("categories", {})
    summary = analysis.get("summary", {})
    tweet_count = analysis.get("tweet_count", 0)

    # Get DB stats for header
    stats = get_db_stats(db_path)

    lines = []

    # --- Header ---
    lines.append(f"# Morning Briefing: {date_str}")
    lines.append("")
    lines.append(f"*Generated {date_str} at {time_str}*")
    lines.append("")

    # --- Quick Summary ---
    lines.append("## Summary")
    lines.append("")
    lines.append(f"Analyzed **{tweet_count}** new tips.")
    lines.append("")

    act_now = summary.get("act_now_count", 0)
    experiment = summary.get("experiment_count", 0)
    noted = summary.get("noted_count", 0)
    noise = summary.get("noise_count", 0)

    lines.append("| Category | Count |")
    lines.append("|----------|------:|")
    lines.append(f"| {CATEGORY_CONFIG['ACT_NOW']['icon']} Act Now | **{act_now}** |")
    lines.append(f"| {CATEGORY_CONFIG['EXPERIMENT']['icon']} Experiment | {experiment} |")
    lines.append(f"| {CATEGORY_CONFIG['NOTED']['icon']} Noted | {noted} |")
    lines.append(f"| {CATEGORY_CONFIG['NOISE']['icon']} Noise | {noise} |")
    lines.append("")

    # Top engagement callout
    top = summary.get("top_engagement")
    if top:
        lines.append(
            f"> Top signal: **@{top['author']}** with {top['likes']:,} likes "
            f"([view](https://x.com/i/status/{top['tweet_id']}))"
        )
        lines.append("")

    # --- Database Stats ---
    if stats:
        lines.append("## Database State")
        lines.append("")
        lines.append("| Metric | Value |")
        lines.append("|--------|------:|")
        if "total_tweets" in stats:
            lines.append(f"| Total tweets | {stats['total_tweets']:,} |")
        if "enriched" in stats:
            lines.append(f"| Enriched (summaries) | {stats['enriched']:,} |")
        if "threads" in stats:
            lines.append(f"| Threads scraped | {stats['threads']:,} |")
        if "replies" in stats:
            lines.append(f"| Thread replies | {stats['replies']:,} |")
        if "links_summarized" in stats:
            lines.append(f"| Links summarized | {stats['links_summarized']:,} |")
        lines.append("")

    # --- ACT NOW section ---
    act_now_entries = categories.get("ACT_NOW", [])
    if act_now_entries:
        lines.append("## [!!] Act Now")
        lines.append("")
        lines.append("High-signal tips directly applicable to current work.")
        lines.append("")
        for entry in act_now_entries:
            lines.extend(format_tip_entry(entry, verbose=verbose))
    elif tweet_count > 0:
        lines.append("## [!!] Act Now")
        lines.append("")
        lines.append("*No high-priority tips today.*")
        lines.append("")

    # --- EXPERIMENT section ---
    experiment_entries = categories.get("EXPERIMENT", [])
    if experiment_entries:
        lines.append("## [?] Experiment Candidates")
        lines.append("")
        lines.append("Interesting techniques worth investigating.")
        lines.append("")
        for entry in experiment_entries:
            lines.extend(format_tip_entry(entry, verbose=verbose))

    # --- NOTED section (compact) ---
    noted_entries = categories.get("NOTED", [])
    if noted_entries:
        lines.append("## [i] Noted")
        lines.append("")
        lines.append("Good to know, no immediate action needed.")
        lines.append("")
        # Noted section is always compact
        for entry in noted_entries[:10]:  # Limit to 10 in briefing
            keyword_display = f" `{entry.get('primary_keyword', '')}`" if entry.get("primary_keyword") else ""
            one_liner = entry.get("one_liner", entry.get("text_preview", "")[:80])
            lines.append(
                f"- @{entry.get('author', '?')} ({entry.get('likes', 0)} likes){keyword_display} — {one_liner}"
            )
        if len(noted_entries) > 10:
            lines.append(f"- *...and {len(noted_entries) - 10} more*")
        lines.append("")

    # --- NOISE section (minimal) ---
    noise_entries = categories.get("NOISE", [])
    if noise_entries:
        lines.append("## [-] Noise")
        lines.append("")
        lines.append(f"*{len(noise_entries)} low-signal tips skipped.*")
        lines.append("")

    # --- Proposed Actions Summary ---
    all_actions = []
    for cat in ["ACT_NOW", "EXPERIMENT"]:
        for entry in categories.get(cat, []):
            if entry.get("proposed_action"):
                all_actions.append(
                    f"- [{CATEGORY_CONFIG[cat]['icon']}] {entry['proposed_action']} "
                    f"(@{entry.get('author', '?')}, {entry.get('likes', 0)} likes)"
                )

    if all_actions:
        lines.append("## Proposed Actions")
        lines.append("")
        lines.extend(all_actions)
        lines.append("")

    # --- Footer ---
    lines.append("---")
    lines.append("")
    lines.append(
        f"*Analysis: {tweet_count} tweets | "
        f"Context: LEARNINGS.md + PROGRESS.md"
        f"{' + Hall-of-Fake STATUS.json' if analysis.get('hof_available') else ''}*"
    )
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Generate morning briefing from tip analysis"
    )
    parser.add_argument(
        "--analysis", "-a",
        type=Path,
        help="Path to analysis JSON file (from analyze_new_tips.py). If omitted, reads stdin.",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory for briefing (default: analysis/daily/)",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DB_PATH,
        help="Path to tips database (for stats)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print briefing to stdout instead of writing file",
    )
    parser.add_argument(
        "--compact",
        action="store_true",
        help="Use compact format (skip detailed per-tip reasons)",
    )
    parser.add_argument(
        "--filename",
        type=str,
        help="Override output filename (default: YYYY-MM-DD-briefing.md)",
    )

    args = parser.parse_args()

    # Load analysis data
    if args.analysis:
        if not args.analysis.exists():
            print(f"Error: Analysis file not found: {args.analysis}", file=sys.stderr)
            return 1
        analysis = json.loads(args.analysis.read_text())
    else:
        # Try reading from stdin
        if sys.stdin.isatty():
            print(
                "Error: No --analysis file provided and no data on stdin.\n"
                "Usage: python scripts/generate_briefing.py --analysis analysis.json\n"
                "   or: python scripts/analyze_new_tips.py | python scripts/generate_briefing.py",
                file=sys.stderr,
            )
            return 1
        analysis = json.loads(sys.stdin.read())

    # Generate briefing
    briefing = generate_briefing(
        analysis,
        db_path=args.db,
        verbose=not args.compact,
    )

    if args.dry_run:
        print(briefing)
        return 0

    # Write to file
    date_str = datetime.now().strftime("%Y-%m-%d")
    filename = args.filename or f"{date_str}-briefing.md"
    output_path = args.output / filename

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(briefing)

    print(f"Briefing written to {output_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
