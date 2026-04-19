#!/usr/bin/env python3
"""Extract rich data from claude_code_tips_v2.db for infographic visualizations."""

import json
import sqlite3
import os

DB_PATH = "/Users/joeyanuff-m2/Development/claude-code-tips/data/claude_code_tips_v2.db"
OUT_DIR = "/Users/joeyanuff-m2/Development/claude-code-tips/assets/visualizations/data"

# Source filter: all bookmark sources (exclude thread/reply extraction)
BOOKMARK_FILTER = "t.source NOT IN ('thread_extraction', 'reply_extraction')"

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def dict_rows(cursor):
    return [dict(row) for row in cursor.fetchall()]

# =============================================================================
# Task 1: Rich category data
# =============================================================================
def extract_categories():
    conn = get_conn()

    # Get category summaries
    cats = dict_rows(conn.execute("""
        SELECT tips.llm_category, COUNT(*) as cnt, SUM(tweets.likes) as total_likes
        FROM tips JOIN tweets ON tips.tweet_id = tweets.id
        WHERE tips.llm_category IS NOT NULL AND tweets.source NOT IN ('thread_extraction', 'reply_extraction')
        GROUP BY tips.llm_category
        ORDER BY cnt DESC
    """))

    # Get category descriptions
    cat_descs = {}
    for row in conn.execute("SELECT name, description FROM tip_categories"):
        cat_descs[row["name"]] = row["description"]

    results = []
    for cat in cats:
        name = cat["llm_category"]

        # Top 5 tweets
        top_tweets = dict_rows(conn.execute("""
            SELECT t.text, t.handle, t.display_name, t.likes, t.posted_at,
                   tips.one_liner, tips.holistic_summary, tips.primary_keyword
            FROM tips JOIN tweets t ON tips.tweet_id = t.id
            WHERE tips.llm_category = ? AND t.source NOT IN ('thread_extraction', 'reply_extraction')
            ORDER BY t.likes DESC LIMIT 5
        """, (name,)))

        results.append({
            "category": name,
            "count": cat["cnt"],
            "total_likes": cat["total_likes"],
            "description": cat_descs.get(name),
            "top_tweets": top_tweets
        })

    conn.close()

    with open(os.path.join(OUT_DIR, "categories_rich.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"Task 1: {len(results)} categories written")
    for r in results:
        print(f"  {r['category']}: {r['count']} tips, {r['total_likes']} likes, {len(r['top_tweets'])} top tweets")

# =============================================================================
# Task 2: Rich author profiles
# =============================================================================
def extract_voices():
    conn = get_conn()

    team_handles = {'bcherny', 'trq212', 'lydiahallie', 'felixrieseberg', 'alexalbert__'}

    # Get all authors ranked by bookmarks
    all_authors = dict_rows(conn.execute("""
        SELECT t.handle, t.display_name, COUNT(*) as bookmarks,
               SUM(t.likes) as total_likes, AVG(t.likes) as avg_likes
        FROM tweets t
        WHERE t.source NOT IN ('thread_extraction', 'reply_extraction')
        GROUP BY t.handle
        ORDER BY bookmarks DESC, total_likes DESC
        LIMIT 30
    """))

    # Build final list: team members first, then top 20 community
    team_authors = [a for a in all_authors if a["handle"] in team_handles]
    community_authors = [a for a in all_authors if a["handle"] not in team_handles][:20]

    # Check if any team members weren't in top 30
    found_handles = {a["handle"] for a in all_authors}
    for h in team_handles - found_handles:
        row = dict_rows(conn.execute("""
            SELECT t.handle, t.display_name, COUNT(*) as bookmarks,
                   SUM(t.likes) as total_likes, AVG(t.likes) as avg_likes
            FROM tweets t
            WHERE t.source NOT IN ('thread_extraction', 'reply_extraction') AND t.handle = ?
            GROUP BY t.handle
        """, (h,)))
        if row:
            team_authors.extend(row)

    results = []
    for author in team_authors + community_authors:
        handle = author["handle"]
        is_team = handle in team_handles

        # Top 5 tweets
        top_tweets = dict_rows(conn.execute("""
            SELECT t.text, t.likes, t.posted_at, tips.one_liner,
                   tips.primary_keyword, tips.holistic_summary
            FROM tweets t
            LEFT JOIN tips ON tips.tweet_id = t.id
            WHERE t.handle = ? AND t.source NOT IN ('thread_extraction', 'reply_extraction')
            ORDER BY t.likes DESC LIMIT 5
        """, (handle,)))

        # Top 3 categories
        top_cats = dict_rows(conn.execute("""
            SELECT tips.llm_category, COUNT(*) as cnt
            FROM tips JOIN tweets t ON tips.tweet_id = t.id
            WHERE t.handle = ? AND t.source NOT IN ('thread_extraction', 'reply_extraction') AND tips.llm_category IS NOT NULL
            GROUP BY tips.llm_category
            ORDER BY cnt DESC LIMIT 3
        """, (handle,)))

        results.append({
            "handle": handle,
            "display_name": author["display_name"],
            "is_team": is_team,
            "bookmarks": author["bookmarks"],
            "total_likes": author["total_likes"],
            "avg_likes": round(author["avg_likes"], 1) if author["avg_likes"] else 0,
            "top_tweets": top_tweets,
            "top_categories": [c["llm_category"] for c in top_cats]
        })

    conn.close()

    with open(os.path.join(OUT_DIR, "voices_rich.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)

    team_count = sum(1 for r in results if r["is_team"])
    community_count = len(results) - team_count
    print(f"Task 2: {len(results)} authors ({team_count} team, {community_count} community)")
    for r in results[:5]:
        print(f"  @{r['handle']}: {r['bookmarks']} bookmarks, {r['total_likes']} likes")

# =============================================================================
# Task 3: Principle enrichment
# =============================================================================
def extract_principles():
    conn = get_conn()

    principles = {
        "Watch, then adopt": {
            "description": "Observe techniques in practice before integrating them into your workflow",
            "searches": ["wait OR observe OR stability OR careful OR patience", "adopt OR integrate OR gradually"]
        },
        "Freshness": {
            "description": "Keep instructions and context current; stale information degrades output",
            "searches": ["fresh OR stale OR outdated OR timestamp", "current OR date OR update"]
        },
        "Review conferences": {
            "description": "Periodically step back to review the big picture and reassess direction",
            "searches": ["step OR back OR review OR picture", "reassess OR reflect OR retrospective"]
        },
        "Don't reinvent": {
            "description": "Search for existing solutions before building from scratch",
            "searches": ["existing OR reinvent OR scratch", "search OR community OR package OR library"]
        }
    }

    results = []
    for principle_name, info in principles.items():
        exemplar_tweets = []
        seen_ids = set()

        for search_term in info["searches"]:
            try:
                rows = dict_rows(conn.execute("""
                    SELECT t.text, t.handle, t.likes, tips.one_liner, t.id
                    FROM tweets_fts fts
                    JOIN tweets t ON fts.id = t.id
                    JOIN tips ON tips.tweet_id = t.id
                    WHERE tweets_fts MATCH ?
                    AND t.source NOT IN ('thread_extraction', 'reply_extraction')
                    ORDER BY t.likes DESC LIMIT 5
                """, (search_term,)))

                for row in rows:
                    if row["id"] not in seen_ids and len(exemplar_tweets) < 3:
                        seen_ids.add(row["id"])
                        exemplar_tweets.append({
                            "text": row["text"],
                            "handle": row["handle"],
                            "likes": row["likes"],
                            "one_liner": row["one_liner"]
                        })
            except Exception as e:
                print(f"  FTS search failed for '{search_term}': {e}")

        results.append({
            "principle": principle_name,
            "description": info["description"],
            "exemplar_tweets": exemplar_tweets
        })

    conn.close()

    with open(os.path.join(OUT_DIR, "principles_rich.json"), "w") as f:
        json.dump(results, f, indent=2, default=str)

    print(f"Task 3: {len(results)} principles")
    for r in results:
        print(f"  '{r['principle']}': {len(r['exemplar_tweets'])} exemplar tweets")

# =============================================================================
if __name__ == "__main__":
    extract_categories()
    print()
    extract_voices()
    print()
    extract_principles()
    print("\nDone! All files written.")
