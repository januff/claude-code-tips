#!/usr/bin/env python3
"""
Curation script for claude-code-tips database.
Analyzes tweets and populates the tips table with:
- category
- summary
- quality_rating
- tools_mentioned
- commands_mentioned
- code_snippets
"""

import sqlite3
import re
import json
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db"

# Category keywords mapping
CATEGORY_PATTERNS = {
    "context-management": [
        r"/compact", r"/clear", r"context", r"token", r"session",
        r"summariz", r"memory", r"window", r"compaction", r"auto.?compact",
        r"recap", r"handoff", r"hand.?off", r"markdown", r"\.md\b",
        r"CLAUDE\.md", r"progress\.md", r"notes", r"documentation"
    ],
    "planning": [
        r"plan mode", r"shift.?tab", r"spec\.md", r"SPEC", r"interview",
        r"planning", r"architect", r"design", r"blueprint", r"roadmap",
        r"research first", r"before (you|starting)", r"step.?by.?step"
    ],
    "hooks": [
        r"\bhook", r"pre-?commit", r"post-?commit", r"pre-?tool",
        r"\.claude/hooks", r"hook.?config"
    ],
    "subagents": [
        r"subagent", r"sub-?agent", r"spawn", r"parallel agent",
        r"agent swarm", r"multi.?agent", r"TeammateTool", r"swarm"
    ],
    "mcp": [
        r"\bMCP\b", r"model context protocol", r"mcp server",
        r"mcp tool", r"stdio", r"@modelcontextprotocol"
    ],
    "skills": [
        r"/skill", r"\.claude/skills", r"skill\.md", r"slash command",
        r"custom command", r"shortcut"
    ],
    "commands": [
        r"/resume", r"/clear", r"/compact", r"/cost", r"/help",
        r"/doctor", r"/memory", r"/config", r"--resume", r"--chrome",
        r"--dangerously", r"--verbose", r"CLI flag", r"brew install",
        r"pip install", r"npm install", r"uv\b", r"sandbox", r"yolo"
    ],
    "automation": [
        r"automat", r"script", r"batch", r"cron", r"ci/cd",
        r"github action", r"workflow automation", r"headless",
        r"agent sdk", r"agent.?sdk", r"Claude SDK", r"build.*agent",
        r"agentic", r"ComputerUse", r"API\b", r"library", r"clone",
        r"compete", r"merge", r"file watch"
    ],
    "workflow": [
        r"workflow", r"process", r"pattern", r"technique", r"method",
        r"approach", r"strategy", r"productivity", r"efficiency",
        r"prompt", r"prompting", r"trick", r"tip\b", r"how (I|to)",
        r"best practice", r"ratchet", r"iterate", r"loop",
        r"settings", r"config", r"audit", r"security", r"fix",
        r"search", r"stuck", r"hallucination", r"reduce", r"avoid",
        r"readable", r"simple", r"prioritize"
    ],
    "tooling": [
        r"\bLSP\b", r"language server", r"vim", r"neovim", r"cursor",
        r"vscode", r"IDE", r"editor", r"terminal", r"iTerm", r"warp",
        r"obsidian", r"git\b", r"github", r"chrome", r"browser"
    ],
    "meta": [
        r"claude itself", r"anthropic", r"opus", r"sonnet", r"haiku",
        r"think hard", r"ultrathink", r"extended thinking", r"reasoning",
        r"claude code", r"CC\b", r"@alexalbert", r"karpathy", r"blog",
        r"thread", r"write.?up", r"article", r"documentation",
        r"beginner", r"learn", r"getting started", r"try\b.*this"
    ]
}

# Tools/commands extraction patterns
TOOL_PATTERNS = [
    # Slash commands (specific known commands only)
    r"\b(/(?:compact|clear|resume|cost|help|doctor|memory|config|skill|sandbox|debug|tasks))\b",
    # CLI flags
    r"(--[\w-]+)",
    # Tool names (CamelCase with Tool suffix)
    r"(\b[A-Z][a-z]+(?:[A-Z][a-z]+)*Tool\b)",
    # Specific tools
    r"\b(AskUserQuestion(?:Tool)?)\b",
    r"\b(Bash|Read|Write|Edit|Glob|Grep|Task|WebFetch|WebSearch)\b",
    # Features
    r"\b(hooks?|subagents?|skills?|MCP)\b",
]

# Code snippet pattern
CODE_PATTERN = r"```[\s\S]*?```|`[^`]+`"


def classify_category(text: str) -> str:
    """Classify tweet into a category based on content."""
    text_lower = text.lower()

    # Score each category
    scores = {}
    for category, patterns in CATEGORY_PATTERNS.items():
        score = 0
        for pattern in patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            score += len(matches)
        scores[category] = score

    # Return highest scoring category, or 'other' if no matches
    if max(scores.values()) > 0:
        return max(scores, key=scores.get)
    return "other"


def extract_tools(text: str) -> list:
    """Extract tools and commands mentioned in tweet."""
    tools = set()

    for pattern in TOOL_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        tools.update(m.strip() for m in matches if len(m) > 1)

    return sorted(list(tools))


def extract_commands(text: str) -> list:
    """Extract slash commands from tweet."""
    commands = re.findall(r"/\w+", text)
    return sorted(list(set(commands)))


def extract_code_snippets(text: str) -> list:
    """Extract code snippets from tweet."""
    snippets = re.findall(CODE_PATTERN, text)
    return snippets if snippets else []


def calculate_quality_rating(tweet: dict, category: str) -> int:
    """
    Calculate quality rating 1-10 based on:
    - Engagement (likes, reposts)
    - Actionability (presence of specific tools/commands)
    - Content length and specificity
    """
    score = 5  # Base score

    likes = tweet.get('likes', 0) or 0
    reposts = tweet.get('reposts', 0) or 0
    text = tweet.get('text', '')

    # Engagement bonus (up to +3)
    if likes >= 500:
        score += 3
    elif likes >= 100:
        score += 2
    elif likes >= 20:
        score += 1

    # Repost bonus
    if reposts >= 50:
        score += 1

    # Actionability bonus
    if re.search(r"/\w+|--\w+", text):  # Commands/flags
        score += 1
    if re.search(r"```|`[^`]+`", text):  # Code snippets
        score += 1

    # Length/detail bonus
    if len(text) > 300:
        score += 1

    # Category bonus (some categories more actionable)
    if category in ["hooks", "commands", "skills", "automation"]:
        score += 1

    # Cap at 10
    return min(score, 10)


def create_summary(text: str, category: str) -> str:
    """Create a one-sentence summary of the tip."""
    # Clean the text
    text = re.sub(r"https?://\S+", "", text)  # Remove URLs
    text = re.sub(r"@\w+", "", text)  # Remove mentions
    text = text.strip()

    # Get first sentence or first 150 chars
    sentences = re.split(r"[.!?\n]", text)
    first_sentence = sentences[0].strip() if sentences else text[:150]

    # Truncate if too long
    if len(first_sentence) > 200:
        first_sentence = first_sentence[:197] + "..."

    return first_sentence


def is_tip_content(text: str) -> bool:
    """Determine if tweet contains tip-worthy content vs just commentary."""
    text_lower = text.lower()

    # Signs it's tip content
    tip_signals = [
        r"/\w+",  # Slash commands
        r"--\w+",  # CLI flags
        r"claude code",
        r"tip[s]?:",
        r"trick[s]?:",
        r"protip",
        r"you can",
        r"try this",
        r"here's how",
        r"I (use|recommend|suggest)",
        r"game.?changer",
        r"\.claude/",
        r"CLAUDE\.md",
    ]

    for pattern in tip_signals:
        if re.search(pattern, text_lower):
            return True

    # Check for minimal actionable content
    return len(text) > 50


def process_tweets(conn: sqlite3.Connection, batch_size: int = 50):
    """Process all tweets and insert into tips table."""
    cursor = conn.cursor()

    # Get all tweets
    cursor.execute("""
        SELECT id, handle, text, likes, reposts, views, engagement_score
        FROM tweets
        ORDER BY likes DESC
    """)
    tweets = cursor.fetchall()

    print(f"Processing {len(tweets)} tweets...")

    # Stats
    category_counts = {}
    processed = 0
    skipped = 0
    tip_number = 1

    for row in tweets:
        tweet_id, handle, text, likes, reposts, views, engagement = row
        tweet = {
            'id': tweet_id,
            'handle': handle,
            'text': text or '',
            'likes': likes,
            'reposts': reposts,
            'views': views,
            'engagement': engagement
        }

        # Classify
        category = classify_category(tweet['text'])
        category_counts[category] = category_counts.get(category, 0) + 1

        # Extract
        tools = extract_tools(tweet['text'])
        commands = extract_commands(tweet['text'])
        code_snippets = extract_code_snippets(tweet['text'])

        # Calculate quality
        quality = calculate_quality_rating(tweet, category)

        # Create summary
        summary = create_summary(tweet['text'], category)

        # Determine if curated (has substantial tip content)
        is_curated = is_tip_content(tweet['text']) and quality >= 5

        # Insert into tips
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO tips (
                    tweet_id, tip_number, category, summary, is_curated,
                    quality_rating, tools_mentioned, commands_mentioned,
                    code_snippets
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                tweet_id,
                tip_number if is_curated else None,
                category,
                summary,
                1 if is_curated else 0,
                quality,
                json.dumps(tools) if tools else None,
                json.dumps(commands) if commands else None,
                json.dumps(code_snippets) if code_snippets else None
            ))

            if is_curated:
                tip_number += 1
            processed += 1

        except Exception as e:
            print(f"Error processing tweet {tweet_id}: {e}")
            skipped += 1

    conn.commit()

    print(f"\nProcessed: {processed}, Skipped: {skipped}")
    print(f"\nCategory distribution:")
    for cat, count in sorted(category_counts.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    # Report curated stats
    cursor.execute("SELECT COUNT(*) FROM tips WHERE is_curated = 1")
    curated_count = cursor.fetchone()[0]
    print(f"\nCurated tips: {curated_count}")

    cursor.execute("SELECT AVG(quality_rating) FROM tips")
    avg_quality = cursor.fetchone()[0]
    print(f"Average quality rating: {avg_quality:.1f}")


def main():
    print(f"Opening database: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)

    try:
        process_tweets(conn)
    finally:
        conn.close()

    print("\nDone!")


if __name__ == "__main__":
    main()
