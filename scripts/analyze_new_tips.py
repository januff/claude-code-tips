#!/usr/bin/env python3
"""
Analyze new tips against existing knowledge base using LLM classification.

Sends each tweet to Gemini with project context for intelligent categorization.
Cross-references against LEARNINGS.md, PROGRESS.md, and hall-of-fake needs.

Categorizes each tip:
- ACT_NOW     — genuinely new, directly applicable to current work (should be rare)
- EXPERIMENT  — interesting technique, worth investigating
- NOTED       — good to know, no action needed
- NOISE       — low-signal for our specific workflow

Usage:
    python scripts/analyze_new_tips.py                      # Analyze since last run
    python scripts/analyze_new_tips.py --since 2026-02-10   # Analyze since specific date
    python scripts/analyze_new_tips.py --ids 123,456,789    # Analyze specific tweet IDs
    python scripts/analyze_new_tips.py --dry-run             # Preview without producing output
    python scripts/analyze_new_tips.py --no-llm              # Engagement-only heuristic (no API key needed)

Output: JSON to stdout (or --output file) with structured analysis per tip.
"""

import argparse
import json
import os
import sqlite3
import sys
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

# Project root
ROOT = Path(__file__).parent.parent

# Load environment variables from .env file
load_dotenv(ROOT / ".env")
DB_PATH = ROOT / "data" / "claude_code_tips_v2.db"
PROJECT_CONTEXT_PATH = ROOT / ".claude" / "references" / "project-context-for-analysis.md"
HOF_STATUS_PATH = ROOT / ".." / "Hall of Fake" / "STATUS.json"


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


def classify_with_gemini(client, tweet: dict, project_context: str, hof_context: str) -> dict:
    """Classify a single tip using Gemini LLM.

    Returns a dict with category, reason, relevance, proposed_action.
    Falls back to NOTED with error reason on failure.
    """
    handle = tweet.get("handle", "unknown")
    display_name = tweet.get("display_name", "")
    likes = tweet.get("likes", 0)
    reposts = tweet.get("reposts", 0)
    views = tweet.get("views", 0)
    text = tweet.get("text", "")
    summary = tweet.get("holistic_summary", "")
    keywords = tweet.get("keywords_json", "[]")
    card_url = tweet.get("card_url", "")

    card_line = f"\nLinked URL: {card_url}" if card_url else ""

    prompt = f"""You are classifying a Claude Code tip for a daily briefing.

PROJECT CONTEXT:
{project_context}
{hof_context}
TWEET TO CLASSIFY:
Author: @{handle} ({display_name})
Likes: {likes} | Reposts: {reposts} | Views: {views}
Text: {text}
Summary: {summary}
Keywords: {keywords}{card_line}

Classify this tip into exactly one category:
- ACT_NOW: Genuinely new technique that's directly applicable to our active work. Should be rare.
- EXPERIMENT: Interesting technique worth investigating, or relevant to something we're building.
- NOTED: Good to know but no action needed. Includes updates on things we already use.
- NOISE: Low signal for our specific workflow.

Return JSON only (no markdown):
{{"category": "ACT_NOW|EXPERIMENT|NOTED|NOISE", "reason": "1-2 sentence explanation", "relevance": ["specific connections to our project"], "proposed_action": "what to do, or null"}}"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
        )

        text_resp = response.text.strip()

        # Handle markdown-wrapped JSON
        if text_resp.startswith("```"):
            text_resp = text_resp.split("\n", 1)[1]
            text_resp = text_resp.rsplit("```", 1)[0]

        parsed = json.loads(text_resp)

        # Unwrap if API wrapped in list
        if isinstance(parsed, list) and len(parsed) > 0:
            parsed = parsed[0]

        # Validate category
        valid_categories = {"ACT_NOW", "EXPERIMENT", "NOTED", "NOISE"}
        if parsed.get("category") not in valid_categories:
            parsed["category"] = "NOTED"
            parsed["reason"] = f"Invalid category returned, defaulting to NOTED. Original: {parsed.get('reason', '')}"

        # Ensure all fields exist
        parsed.setdefault("reason", "")
        parsed.setdefault("relevance", [])
        parsed.setdefault("proposed_action", None)

        return parsed

    except json.JSONDecodeError as e:
        print(f"  JSON parse error for {tweet.get('id')}: {e}", file=sys.stderr)
        # Try to extract category from raw text
        text_upper = (text_resp or "").upper()
        for cat in ["ACT_NOW", "EXPERIMENT", "NOTED", "NOISE"]:
            if cat in text_upper:
                return {
                    "category": cat,
                    "reason": f"Extracted from malformed response (JSON parse failed)",
                    "relevance": [],
                    "proposed_action": None,
                }
        return {
            "category": "NOTED",
            "reason": "Classification failed — review manually",
            "relevance": [],
            "proposed_action": None,
        }
    except Exception as e:
        print(f"  API error for {tweet.get('id')}: {e}", file=sys.stderr)
        return {
            "category": "NOTED",
            "reason": f"Classification failed ({type(e).__name__}) — review manually",
            "relevance": [],
            "proposed_action": None,
        }


def classify_engagement_only(tweet: dict) -> dict:
    """Simple engagement-only heuristic for --no-llm mode."""
    likes = tweet.get("likes", 0)

    if likes >= 2000:
        return {
            "category": "EXPERIMENT",
            "reason": f"Very high engagement ({likes} likes) — no LLM classification",
            "relevance": ["high community engagement"],
            "proposed_action": "Review manually — LLM classification was skipped",
        }
    elif likes >= 500:
        return {
            "category": "NOTED",
            "reason": f"Moderate engagement ({likes} likes) — no LLM classification",
            "relevance": [],
            "proposed_action": None,
        }
    else:
        return {
            "category": "NOISE",
            "reason": f"Low engagement ({likes} likes) — no LLM classification",
            "relevance": [],
            "proposed_action": None,
        }


def analyze_tips(tweets: list[dict], classifier_fn) -> dict:
    """Analyze a list of tweets using the provided classifier function.

    Returns structured analysis with categories dict and summary.
    """
    categories = {
        "ACT_NOW": [],
        "EXPERIMENT": [],
        "NOTED": [],
        "NOISE": [],
    }

    for i, tweet in enumerate(tweets):
        print(
            f"  [{i + 1}/{len(tweets)}] @{tweet.get('handle', '?')} "
            f"({tweet.get('likes', 0)} likes): "
            f"{(tweet.get('text') or '')[:50]}...",
            file=sys.stderr,
        )

        classification = classifier_fn(tweet)

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
            }
            if top_tweet
            else None,
        },
    }


def main():
    parser = argparse.ArgumentParser(
        description="Analyze new tips using Gemini LLM classification"
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
        "--output",
        "-o",
        type=Path,
        help="Write analysis JSON to file (default: stdout)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be analyzed without producing output",
    )
    parser.add_argument(
        "--no-llm",
        action="store_true",
        help="Use engagement-only heuristic (no API key needed)",
    )

    args = parser.parse_args()

    if not args.db.exists():
        print(f"Error: Database not found at {args.db}", file=sys.stderr)
        return 1

    # Parse tweet IDs if provided
    tweet_ids = None
    if args.ids:
        tweet_ids = [tid.strip() for tid in args.ids.split(",") if tid.strip()]

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
            print(
                f"  {t['id']} | {t.get('likes', 0)} likes | "
                f"@{t.get('handle', '?')} | {(t.get('text') or '')[:60]}..."
            )
        if len(tweets) > 20:
            print(f"  ... and {len(tweets) - 20} more")
        print(f"\nMode: {'engagement-only (--no-llm)' if args.no_llm else 'Gemini LLM classification'}")
        return 0

    # Set up classifier
    if args.no_llm:
        print("Using engagement-only heuristic (--no-llm)", file=sys.stderr)
        classifier_fn = classify_engagement_only
    else:
        # Initialize Gemini client
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print(
                "Error: GOOGLE_API_KEY environment variable required. "
                "Use --no-llm for engagement-only heuristic.",
                file=sys.stderr,
            )
            return 1

        from google import genai

        client = genai.Client(api_key=api_key)

        # Load project context
        project_context = load_text_file(PROJECT_CONTEXT_PATH)
        if not project_context:
            print(
                "Warning: project-context-for-analysis.md not found, "
                "classification will lack project awareness",
                file=sys.stderr,
            )

        # Load hall-of-fake context
        hof_status = load_json_file(HOF_STATUS_PATH)
        hof_context = ""
        if hof_status:
            hof_desc = ""
            active = hof_status.get("active_task", {})
            if isinstance(active, dict) and active.get("description"):
                hof_desc = active["description"]
            hof_issues = hof_status.get("known_issues", [])
            if hof_desc or hof_issues:
                hof_context = "\nCROSS-PROJECT (hall-of-fake sibling repo):\n"
                if hof_desc:
                    hof_context += f"Active task: {hof_desc}\n"
                if hof_issues:
                    hof_context += f"Known issues: {'; '.join(hof_issues[:3])}\n"

        def classifier_fn(tweet):
            result = classify_with_gemini(client, tweet, project_context, hof_context)
            time.sleep(0.5)  # Rate limit — match enrichment scripts
            return result

    # Run analysis
    print(f"Analyzing {len(tweets)} tweets...", file=sys.stderr)
    result = analyze_tips(tweets, classifier_fn)

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
