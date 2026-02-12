#!/usr/bin/env python3
"""
Analyze new tips against existing knowledge base (LEARNINGS.md, PROGRESS.md).

Cross-references new tweets against:
- LEARNINGS.md — techniques we're watching or using
- plans/PROGRESS.md — adoption status of techniques
- Hall-of-fake STATUS.json — cross-project needs (if available)

Categorizes each tip:
- ACT_NOW     — high-signal, directly applicable to current work
- EXPERIMENT  — interesting technique, worth a spike
- NOTED       — good to know, no action needed
- NOISE       — low-signal, skip

Usage:
    python scripts/analyze_new_tips.py                      # Analyze since last run
    python scripts/analyze_new_tips.py --since 2026-02-10   # Analyze since specific date
    python scripts/analyze_new_tips.py --ids 123,456,789    # Analyze specific tweet IDs
    python scripts/analyze_new_tips.py --dry-run             # Preview without writing output

Output: JSON to stdout (or --output file) with structured analysis per tip.
"""

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime
from pathlib import Path


# Project root
ROOT = Path(__file__).parent.parent
DB_PATH = ROOT / "data" / "claude_code_tips_v2.db"
LEARNINGS_PATH = ROOT / "LEARNINGS.md"
PROGRESS_PATH = ROOT / "plans" / "PROGRESS.md"
HOF_STATUS_PATH = ROOT / ".." / "Hall of Fake" / "STATUS.json"

# Engagement thresholds for signal classification
HIGH_ENGAGEMENT_LIKES = 500
MEDIUM_ENGAGEMENT_LIKES = 100

# Keywords and patterns that indicate high relevance to our workflow
WORKFLOW_KEYWORDS = {
    "act_now": [
        # Things we actively use
        "claude.md", "handoff", "delegation", "obsidian", "sqlite",
        "playwriter", "mcp", "bookmark", "export", "vault",
        # Things we're actively building
        "cron", "monitor", "pipeline", "enrichment", "briefing",
        "pre-compact", "hook", "wrap-up", "daily-summary",
        # Active project needs
        "skills", "slash command", "commands/",
    ],
    "experiment": [
        # Things in PROGRESS.md as PENDING
        "subagent", "parallel claude", "ralph wiggum", "compaction",
        "posttooluseooks", "auto-accept", "permissions",
        "teleport", "verify", "code-simplifier",
        # Interesting techniques
        "agent sdk", "codex", "cross-model", "review",
        "gemini", "openrouter", "token budget",
    ],
    "watch": [
        # Things in LEARNINGS.md "Watching" section
        "beads", "agent mail", "agent swarm", "voice", "stt",
        "lsp", "language server",
    ],
}


def load_text_file(path: Path) -> str:
    """Load a text file, returning empty string if not found."""
    try:
        return path.read_text(encoding="utf-8")
    except (FileNotFoundError, OSError):
        return ""


def load_json_file(path: Path) -> dict:
    """Load a JSON file, returning empty dict if not found."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return {}


def extract_adopted_techniques(progress_text: str) -> set[str]:
    """Extract technique names that are ADOPTED from PROGRESS.md."""
    adopted = set()
    for line in progress_text.splitlines():
        if "ADOPTED" in line and "|" in line:
            # Extract tip name from table row: | Tip Name | Status | ...
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                tip_name = parts[1].strip("* ").lower()
                if tip_name and tip_name != "tip" and tip_name != "status":
                    adopted.add(tip_name)
    return adopted


def extract_pending_techniques(progress_text: str) -> set[str]:
    """Extract technique names that are PENDING from PROGRESS.md."""
    pending = set()
    for line in progress_text.splitlines():
        if "PENDING" in line and "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 2:
                tip_name = parts[1].strip("* ").lower()
                if tip_name and tip_name != "tip" and tip_name != "status":
                    pending.add(tip_name)
    return pending


def extract_learnings_sections(learnings_text: str) -> dict[str, list[str]]:
    """Parse LEARNINGS.md into sections with their technique keywords."""
    sections = {
        "daily": [],
        "experimenting": [],
        "try_next": [],
        "watching": [],
    }
    current_section = None
    for line in learnings_text.splitlines():
        lower = line.lower().strip()
        if "techniques we use daily" in lower:
            current_section = "daily"
        elif "experimenting with" in lower:
            current_section = "experimenting"
        elif "techniques to try next" in lower:
            current_section = "try_next"
        elif "watching" in lower and "not yet convinced" in lower:
            current_section = "watching"
        elif current_section and line.startswith("### "):
            # Extract technique name from heading
            technique = line.lstrip("# ").strip().lower()
            sections[current_section].append(technique)
    return sections


def get_new_tweets(
    db_path: Path,
    since: str | None = None,
    tweet_ids: list[str] | None = None,
) -> list[dict]:
    """Fetch new tweets from the database.

    If tweet_ids is provided, fetch those specific tweets.
    If since is provided, fetch tweets extracted after that date.
    Otherwise, use the last 24 hours.
    """
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    if tweet_ids:
        placeholders = ",".join("?" for _ in tweet_ids)
        query = f"""
            SELECT
                t.id, t.text, t.handle, t.display_name, t.likes, t.views,
                t.reposts, t.replies, t.posted_at, t.extracted_at,
                t.card_url, t.card_title,
                tp.primary_keyword, tp.holistic_summary, tp.one_liner,
                tp.llm_category, tp.keywords_json
            FROM tweets t
            LEFT JOIN tips tp ON t.id = tp.tweet_id
            WHERE t.id IN ({placeholders})
            ORDER BY t.likes DESC
        """
        rows = conn.execute(query, tweet_ids).fetchall()
    else:
        since_clause = since or datetime.now().strftime("%Y-%m-%d")
        query = """
            SELECT
                t.id, t.text, t.handle, t.display_name, t.likes, t.views,
                t.reposts, t.replies, t.posted_at, t.extracted_at,
                t.card_url, t.card_title,
                tp.primary_keyword, tp.holistic_summary, tp.one_liner,
                tp.llm_category, tp.keywords_json
            FROM tweets t
            LEFT JOIN tips tp ON t.id = tp.tweet_id
            WHERE t.extracted_at >= ?
            ORDER BY t.likes DESC
        """
        rows = conn.execute(query, (since_clause,)).fetchall()

    tweets = [dict(row) for row in rows]
    conn.close()
    return tweets


def classify_tip(
    tweet: dict,
    adopted: set[str],
    pending: set[str],
    learnings_sections: dict[str, list[str]],
    hof_needs: list[str],
) -> dict:
    """Classify a single tip into ACT_NOW / EXPERIMENT / NOTED / NOISE.

    Returns a dict with:
    - category: one of ACT_NOW, EXPERIMENT, NOTED, NOISE
    - reason: why this classification was chosen
    - relevance: list of matching context (technique names, project needs)
    - proposed_action: what to do about it (if any)
    """
    text_lower = (tweet.get("text") or "").lower()
    keyword = (tweet.get("primary_keyword") or "").lower()
    summary = (tweet.get("holistic_summary") or "").lower()
    likes = tweet.get("likes") or 0
    keywords_json = tweet.get("keywords_json") or "[]"

    try:
        keywords = json.loads(keywords_json)
    except (json.JSONDecodeError, TypeError):
        keywords = []

    all_text = f"{text_lower} {keyword} {summary} {' '.join(k.lower() for k in keywords)}"

    relevance = []
    reasons = []

    # Check against act_now keywords (things we actively use or build)
    act_now_matches = [
        kw for kw in WORKFLOW_KEYWORDS["act_now"] if kw in all_text
    ]
    if act_now_matches:
        relevance.extend([f"workflow match: {m}" for m in act_now_matches])

    # Check against experiment keywords
    experiment_matches = [
        kw for kw in WORKFLOW_KEYWORDS["experiment"] if kw in all_text
    ]
    if experiment_matches:
        relevance.extend([f"experiment match: {m}" for m in experiment_matches])

    # Check against PROGRESS.md pending techniques
    pending_matches = [
        tech for tech in pending
        if any(word in all_text for word in tech.split() if len(word) > 3)
    ]
    if pending_matches:
        relevance.extend([f"pending in PROGRESS.md: {m}" for m in pending_matches])
        reasons.append("matches pending technique")

    # Check against adopted techniques (lower priority — we already use these)
    adopted_matches = [
        tech for tech in adopted
        if any(word in all_text for word in tech.split() if len(word) > 3)
    ]
    if adopted_matches:
        relevance.extend([f"already adopted: {m}" for m in adopted_matches])

    # Check against LEARNINGS.md sections
    for section, techniques in learnings_sections.items():
        for tech in techniques:
            tech_words = [w for w in tech.split() if len(w) > 3]
            if any(w in all_text for w in tech_words):
                relevance.extend([f"LEARNINGS/{section}: {tech}"])

    # Check against hall-of-fake needs
    hof_matches = [need for need in hof_needs if need.lower() in all_text]
    if hof_matches:
        relevance.extend([f"hall-of-fake need: {m}" for m in hof_matches])
        reasons.append("relevant to hall-of-fake")

    # --- Classification logic ---

    # ACT_NOW: high engagement + directly relevant to active work
    if likes >= HIGH_ENGAGEMENT_LIKES and act_now_matches:
        return {
            "category": "ACT_NOW",
            "reason": f"High engagement ({likes} likes) + directly relevant to active workflow",
            "relevance": relevance,
            "proposed_action": f"Review and consider integrating: {', '.join(act_now_matches[:3])}",
        }

    # ACT_NOW: matches pending technique in PROGRESS.md with decent engagement
    if pending_matches and likes >= MEDIUM_ENGAGEMENT_LIKES:
        return {
            "category": "ACT_NOW",
            "reason": f"Matches pending technique with {likes} likes",
            "relevance": relevance,
            "proposed_action": f"This may help with: {', '.join(pending_matches[:3])}",
        }

    # EXPERIMENT: interesting technique or moderate engagement with some relevance
    if experiment_matches and likes >= MEDIUM_ENGAGEMENT_LIKES:
        return {
            "category": "EXPERIMENT",
            "reason": f"Experiment-worthy technique with {likes} likes",
            "relevance": relevance,
            "proposed_action": f"Consider spiking: {', '.join(experiment_matches[:3])}",
        }

    if likes >= HIGH_ENGAGEMENT_LIKES and relevance:
        return {
            "category": "EXPERIMENT",
            "reason": f"High engagement ({likes} likes) with some relevance",
            "relevance": relevance,
            "proposed_action": "Review for potential adoption",
        }

    # High engagement alone is worth noting even without keyword match
    if likes >= HIGH_ENGAGEMENT_LIKES:
        return {
            "category": "EXPERIMENT",
            "reason": f"Very high engagement ({likes} likes) — community signal",
            "relevance": relevance or ["high community engagement"],
            "proposed_action": "Read and evaluate — community strongly validates this",
        }

    # NOTED: some relevance but lower engagement, or adopted technique update
    if relevance and likes >= 10:
        return {
            "category": "NOTED",
            "reason": f"Some relevance ({likes} likes)",
            "relevance": relevance,
            "proposed_action": None,
        }

    if adopted_matches:
        return {
            "category": "NOTED",
            "reason": "Update on already-adopted technique",
            "relevance": relevance,
            "proposed_action": None,
        }

    # NOISE: low engagement, no relevance
    return {
        "category": "NOISE",
        "reason": f"Low signal ({likes} likes, no keyword matches)",
        "relevance": relevance or [],
        "proposed_action": None,
    }


def analyze_tips(
    tweets: list[dict],
    adopted: set[str],
    pending: set[str],
    learnings_sections: dict[str, list[str]],
    hof_needs: list[str],
) -> dict:
    """Analyze a list of tweets and return structured analysis.

    Returns:
    {
        "analyzed_at": ISO timestamp,
        "tweet_count": N,
        "categories": {
            "ACT_NOW": [...],
            "EXPERIMENT": [...],
            "NOTED": [...],
            "NOISE": [...]
        },
        "summary": {
            "act_now_count": N,
            "experiment_count": N,
            "noted_count": N,
            "noise_count": N,
            "top_engagement": {...}
        }
    }
    """
    categories = {
        "ACT_NOW": [],
        "EXPERIMENT": [],
        "NOTED": [],
        "NOISE": [],
    }

    for tweet in tweets:
        classification = classify_tip(
            tweet, adopted, pending, learnings_sections, hof_needs
        )

        entry = {
            "tweet_id": tweet["id"],
            "author": tweet.get("handle", "unknown"),
            "likes": tweet.get("likes", 0),
            "text_preview": (tweet.get("text") or "")[:120],
            "primary_keyword": tweet.get("primary_keyword"),
            "one_liner": tweet.get("one_liner"),
            "category": classification["category"],
            "reason": classification["reason"],
            "relevance": classification["relevance"],
            "proposed_action": classification["proposed_action"],
        }

        categories[classification["category"]].append(entry)

    # Sort each category by likes descending
    for cat in categories:
        categories[cat].sort(key=lambda x: x.get("likes", 0), reverse=True)

    # Find top engagement across all
    all_entries = []
    for cat_entries in categories.values():
        all_entries.extend(cat_entries)

    top_tweet = max(all_entries, key=lambda x: x.get("likes", 0)) if all_entries else None

    return {
        "analyzed_at": datetime.now().isoformat(),
        "tweet_count": len(tweets),
        "categories": categories,
        "summary": {
            "act_now_count": len(categories["ACT_NOW"]),
            "experiment_count": len(categories["EXPERIMENT"]),
            "noted_count": len(categories["NOTED"]),
            "noise_count": len(categories["NOISE"]),
            "top_engagement": {
                "tweet_id": top_tweet["tweet_id"],
                "likes": top_tweet["likes"],
                "author": top_tweet["author"],
            } if top_tweet else None,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze new tips against LEARNINGS.md and PROGRESS.md"
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Analyze tweets extracted since this date (YYYY-MM-DD). Default: today",
    )
    parser.add_argument(
        "--ids",
        type=str,
        help="Comma-separated tweet IDs to analyze",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DB_PATH,
        help="Path to tips database",
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        help="Write analysis JSON to file (default: stdout)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be analyzed without producing output",
    )

    args = parser.parse_args()

    if not args.db.exists():
        print(f"Error: Database not found at {args.db}", file=sys.stderr)
        return 1

    # Parse tweet IDs if provided
    tweet_ids = None
    if args.ids:
        tweet_ids = [tid.strip() for tid in args.ids.split(",") if tid.strip()]

    # Load context files
    learnings_text = load_text_file(LEARNINGS_PATH)
    progress_text = load_text_file(PROGRESS_PATH)

    adopted = extract_adopted_techniques(progress_text)
    pending = extract_pending_techniques(progress_text)
    learnings_sections = extract_learnings_sections(learnings_text)

    # Load hall-of-fake needs (skip gracefully if not available)
    hof_status = load_json_file(HOF_STATUS_PATH)
    hof_needs = []
    if hof_status:
        # Extract any known_issues or active tasks as "needs"
        hof_needs = hof_status.get("known_issues", [])
        active = hof_status.get("active_task", {})
        if isinstance(active, dict) and active.get("description"):
            hof_needs.append(active["description"])

    # Fetch tweets
    tweets = get_new_tweets(args.db, since=args.since, tweet_ids=tweet_ids)

    if not tweets:
        print("No new tweets found to analyze.", file=sys.stderr)
        result = {
            "analyzed_at": datetime.now().isoformat(),
            "tweet_count": 0,
            "categories": {"ACT_NOW": [], "EXPERIMENT": [], "NOTED": [], "NOISE": []},
            "summary": {
                "act_now_count": 0,
                "experiment_count": 0,
                "noted_count": 0,
                "noise_count": 0,
                "top_engagement": None,
            },
        }
        if args.output:
            args.output.write_text(json.dumps(result, indent=2))
        else:
            print(json.dumps(result, indent=2))
        return 0

    if args.dry_run:
        print(f"Would analyze {len(tweets)} tweets:")
        for t in tweets[:20]:
            print(f"  {t['id']} | {t.get('likes', 0)} likes | @{t.get('handle', '?')} | {(t.get('text') or '')[:60]}...")
        print(f"\nContext loaded:")
        print(f"  Adopted techniques: {len(adopted)}")
        print(f"  Pending techniques: {len(pending)}")
        print(f"  LEARNINGS sections: {sum(len(v) for v in learnings_sections.values())} techniques")
        print(f"  Hall-of-fake needs: {len(hof_needs)}")
        return 0

    # Run analysis
    result = analyze_tips(tweets, adopted, pending, learnings_sections, hof_needs)

    # Output
    output_json = json.dumps(result, indent=2, ensure_ascii=False)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(output_json)
        print(f"Analysis written to {args.output}", file=sys.stderr)
    else:
        print(output_json)

    # Print summary to stderr
    s = result["summary"]
    print(
        f"\nAnalysis complete: {result['tweet_count']} tweets — "
        f"ACT_NOW: {s['act_now_count']}, "
        f"EXPERIMENT: {s['experiment_count']}, "
        f"NOTED: {s['noted_count']}, "
        f"NOISE: {s['noise_count']}",
        file=sys.stderr,
    )

    return 0


if __name__ == "__main__":
    sys.exit(main())
