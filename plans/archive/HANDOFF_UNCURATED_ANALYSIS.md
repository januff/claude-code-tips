# Handoff: Analyze Uncurated Tweets + Engagement Deltas

**Created by:** Claude.ai (Opus 4.5)
**Date:** 2025-12-29
**Status:** 📋 READY FOR EXECUTION
**Code word:** context-first

---

## Purpose

Two analyses:

1. **Engagement Delta** — Compare original curation metrics (Dec 26) with current metrics (Dec 29) to find tips that are "heating up"
2. **Uncurated Review** — Analyze the 237 tweets not in the original 109 to find hidden gems, especially Obsidian-related tips

---

## Part 1: Engagement Delta Analysis

### Data Sources

**Original metrics:** `tips/full-thread.md`
```markdown
### 1. The Handoff Technique
**Author:** @zeroxBigBoss
**Engagement:** 3 replies | 2 reposts | 160 likes | 9K views
```

**Current metrics:** `tweets` table
```sql
SELECT likes, reposts, replies, views FROM tweets WHERE id = ?
```

### Implementation

Create `scripts/engagement_delta.py`:

```python
#!/usr/bin/env python3
"""
Compare engagement metrics between original curation (Dec 26) and current (Dec 29).
Identifies tips with unusual growth.
"""

import re
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "claude_code_tips.db"
FULL_THREAD_PATH = Path(__file__).parent.parent / "tips" / "full-thread.md"


def parse_original_engagement(filepath):
    """Extract engagement metrics from full-thread.md."""
    content = filepath.read_text()
    tips = {}
    
    # Pattern: ### N. Title\n**Author:** @handle\n**Tip:**...\n**Engagement:** X replies | Y reposts | Z likes | W views
    pattern = r'### (\d+)\. (.+?)\n\*\*Author:\*\* @(\w+).*?\*\*Engagement:\*\* (.+?)(?=\n---|\n###|\Z)'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        tip_num = int(match.group(1))
        title = match.group(2).strip()
        handle = match.group(3).lower()
        engagement_str = match.group(4).strip()
        
        # Parse engagement: "3 replies | 2 reposts | 160 likes | 9K views"
        metrics = {'replies': 0, 'reposts': 0, 'likes': 0, 'views': 0}
        
        for part in engagement_str.split('|'):
            part = part.strip().lower()
            if 'repl' in part:
                metrics['replies'] = parse_number(part)
            elif 'repost' in part:
                metrics['reposts'] = parse_number(part)
            elif 'like' in part:
                metrics['likes'] = parse_number(part)
            elif 'view' in part:
                metrics['views'] = parse_number(part)
            elif 'bookmark' in part:
                metrics['bookmarks'] = parse_number(part)
        
        tips[tip_num] = {
            'title': title,
            'handle': handle,
            'original': metrics
        }
    
    return tips


def parse_number(s):
    """Parse '9K' -> 9000, '1.2M' -> 1200000, '160' -> 160."""
    match = re.search(r'([\d.]+)\s*([KMB])?', s, re.IGNORECASE)
    if not match:
        return 0
    
    num = float(match.group(1))
    suffix = (match.group(2) or '').upper()
    
    multipliers = {'K': 1000, 'M': 1000000, 'B': 1000000000}
    return int(num * multipliers.get(suffix, 1))


def get_current_metrics(conn):
    """Get current metrics for curated tips."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT t.tip_number, tw.likes, tw.reposts, tw.replies, tw.views, tw.id
        FROM tips t
        JOIN tweets tw ON t.tweet_id = tw.id
        WHERE t.is_curated = 1
    """)
    
    metrics = {}
    for row in cursor.fetchall():
        metrics[row[0]] = {
            'likes': row[1],
            'reposts': row[2],
            'replies': row[3],
            'views': row[4],
            'tweet_id': row[5]
        }
    
    return metrics


def calculate_deltas(original, current):
    """Calculate engagement changes."""
    deltas = []
    
    for tip_num, orig_data in original.items():
        if tip_num not in current:
            continue
        
        curr = current[tip_num]
        orig = orig_data['original']
        
        likes_delta = curr['likes'] - orig['likes']
        views_delta = curr['views'] - orig['views']
        
        # Calculate percentage growth
        likes_pct = (likes_delta / orig['likes'] * 100) if orig['likes'] > 0 else 0
        views_pct = (views_delta / orig['views'] * 100) if orig['views'] > 0 else 0
        
        deltas.append({
            'tip_number': tip_num,
            'title': orig_data['title'],
            'handle': orig_data['handle'],
            'likes_orig': orig['likes'],
            'likes_now': curr['likes'],
            'likes_delta': likes_delta,
            'likes_pct': likes_pct,
            'views_orig': orig['views'],
            'views_now': curr['views'],
            'views_delta': views_delta,
            'views_pct': views_pct,
        })
    
    return deltas


def main():
    conn = sqlite3.connect(DB_PATH)
    
    # Parse original engagement
    original = parse_original_engagement(FULL_THREAD_PATH)
    print(f"📖 Parsed {len(original)} tips with original engagement")
    
    # Get current metrics
    current = get_current_metrics(conn)
    print(f"📊 Found {len(current)} curated tips in DB")
    
    # Calculate deltas
    deltas = calculate_deltas(original, current)
    
    # Sort by likes growth percentage
    deltas.sort(key=lambda x: x['likes_pct'], reverse=True)
    
    print("\n🔥 TOP ENGAGEMENT GROWTH (by likes % increase):\n")
    print(f"{'#':<4} {'Title':<40} {'Likes':<20} {'Views':<20}")
    print(f"{'':4} {'':<40} {'Orig→Now (Δ%)':<20} {'Orig→Now (Δ%)':<20}")
    print("-" * 90)
    
    for d in deltas[:20]:
        likes_str = f"{d['likes_orig']}→{d['likes_now']} (+{d['likes_pct']:.0f}%)"
        views_str = f"{d['views_orig']}→{d['views_now']} (+{d['views_pct']:.0f}%)"
        print(f"#{d['tip_number']:<3} {d['title'][:38]:<40} {likes_str:<20} {views_str:<20}")
    
    # Also show absolute growth leaders
    deltas.sort(key=lambda x: x['likes_delta'], reverse=True)
    
    print("\n\n📈 TOP ABSOLUTE GROWTH (by likes added):\n")
    print(f"{'#':<4} {'Title':<40} {'Likes Added':<15} {'Now Total':<10}")
    print("-" * 75)
    
    for d in deltas[:15]:
        print(f"#{d['tip_number']:<3} {d['title'][:38]:<40} +{d['likes_delta']:<14} {d['likes_now']:<10}")
    
    conn.close()


if __name__ == "__main__":
    main()
```

### Expected Output

```
🔥 TOP ENGAGEMENT GROWTH (by likes % increase):

#    Title                                    Likes                Views
     ...                                      Orig→Now (Δ%)        Orig→Now (Δ%)
------------------------------------------------------------------------------------------
#47  Use Subagents for Extra Session Time    1→15 (+1400%)        903→2500 (+177%)
#83  Parallel Tasks for Multiple Files       1→12 (+1100%)        144→890 (+518%)
...
```

---

## Part 2: Uncurated Tweet Analysis

### Query: Find Uncurated Tweets

```sql
-- High-engagement uncurated tweets
SELECT 
    tw.handle, 
    tw.text, 
    tw.likes, 
    tw.views,
    tw.url,
    tw.posted_at
FROM tweets tw
LEFT JOIN tips t ON tw.id = t.tweet_id
WHERE t.id IS NULL
ORDER BY tw.likes DESC;
```

### Implementation

Create `scripts/analyze_uncurated.py`:

```python
#!/usr/bin/env python3
"""
Analyze uncurated tweets to find hidden gems.
Groups by topic, highlights Obsidian-related content.
"""

import sqlite3
from pathlib import Path
from collections import defaultdict

DB_PATH = Path(__file__).parent.parent / "claude_code_tips.db"

# Keywords for topic detection
TOPIC_KEYWORDS = {
    'obsidian': ['obsidian', 'vault', 'markdown note', 'pkm'],
    'context': ['context', 'compact', 'session', 'clear', 'window', 'token'],
    'subagents': ['subagent', 'sub agent', 'parallel', 'orchestrat'],
    'skills': ['skill', 'mcp', 'plugin', 'tool', 'custom'],
    'planning': ['plan', 'architect', 'spec', 'design first'],
    'prompting': ['prompt', 'ask', 'tell claude', 'instruct'],
    'git': ['git', 'commit', 'branch', 'worktree', 'diff'],
    'documentation': ['document', 'md file', 'markdown', 'readme', 'claude.md'],
    'hooks': ['hook', 'trigger', 'automat'],
}


def detect_topics(text):
    """Detect topics from tweet text."""
    text_lower = text.lower()
    topics = []
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            topics.append(topic)
    
    return topics if topics else ['uncategorized']


def get_uncurated_tweets(conn):
    """Get all tweets not in tips table."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            tw.id, tw.handle, tw.text, tw.likes, tw.views, tw.url, tw.posted_at
        FROM tweets tw
        LEFT JOIN tips t ON tw.id = t.tweet_id
        WHERE t.id IS NULL
        ORDER BY tw.likes DESC
    """)
    
    return cursor.fetchall()


def main():
    conn = sqlite3.connect(DB_PATH)
    
    tweets = get_uncurated_tweets(conn)
    print(f"📊 Found {len(tweets)} uncurated tweets\n")
    
    # Group by detected topic
    by_topic = defaultdict(list)
    obsidian_tweets = []
    
    for tweet in tweets:
        id_, handle, text, likes, views, url, posted_at = tweet
        topics = detect_topics(text)
        
        tweet_data = {
            'id': id_,
            'handle': handle,
            'text': text,
            'likes': likes,
            'views': views,
            'url': url,
            'posted_at': posted_at,
            'topics': topics
        }
        
        for topic in topics:
            by_topic[topic].append(tweet_data)
        
        if 'obsidian' in topics:
            obsidian_tweets.append(tweet_data)
    
    # Report: Obsidian-specific (user requested)
    print("=" * 80)
    print("🟣 OBSIDIAN-RELATED TWEETS (User Priority)")
    print("=" * 80)
    
    if obsidian_tweets:
        for t in sorted(obsidian_tweets, key=lambda x: x['likes'], reverse=True):
            print(f"\n@{t['handle']} ({t['likes']} likes)")
            print(f"  {t['text'][:200]}...")
            print(f"  {t['url']}")
    else:
        print("  No Obsidian-specific tweets found in uncurated set.")
    
    # Report: Top uncurated by engagement
    print("\n" + "=" * 80)
    print("🔥 TOP 30 UNCURATED BY ENGAGEMENT")
    print("=" * 80)
    
    for i, tweet in enumerate(tweets[:30], 1):
        id_, handle, text, likes, views, url, posted_at = tweet
        topics = detect_topics(text)
        topic_str = ', '.join(topics)
        
        print(f"\n{i}. @{handle} — {likes} likes, {views} views")
        print(f"   Topics: [{topic_str}]")
        print(f"   {text[:150]}...")
        print(f"   {url}")
    
    # Report: Topic distribution
    print("\n" + "=" * 80)
    print("📊 TOPIC DISTRIBUTION IN UNCURATED")
    print("=" * 80)
    
    topic_counts = [(topic, len(tweets)) for topic, tweets in by_topic.items()]
    topic_counts.sort(key=lambda x: x[1], reverse=True)
    
    for topic, count in topic_counts:
        avg_likes = sum(t['likes'] for t in by_topic[topic]) / count if count > 0 else 0
        print(f"  {topic:<20} {count:>3} tweets  (avg {avg_likes:.1f} likes)")
    
    # Export for review
    output_path = Path(__file__).parent.parent / "analysis" / "uncurated_review.md"
    output_path.parent.mkdir(exist_ok=True)
    
    with open(output_path, 'w') as f:
        f.write("# Uncurated Tweet Review\n\n")
        f.write(f"Generated: 2025-12-29\n")
        f.write(f"Total uncurated: {len(tweets)}\n\n")
        
        f.write("## Obsidian-Related\n\n")
        for t in obsidian_tweets:
            f.write(f"- **@{t['handle']}** ({t['likes']} likes): {t['text'][:100]}... [link]({t['url']})\n")
        
        f.write("\n## Top 50 by Engagement\n\n")
        for i, tweet in enumerate(tweets[:50], 1):
            id_, handle, text, likes, views, url, posted_at = tweet
            f.write(f"{i}. **@{handle}** ({likes} likes): {text[:100]}... [link]({url})\n")
    
    print(f"\n✅ Exported to {output_path}")
    
    conn.close()


if __name__ == "__main__":
    main()
```

---

## Expected Insights

### Engagement Delta
- Tips that went "viral" in the 3 days since curation
- Early tips that are still gaining traction
- Tips that plateaued (low growth)

### Uncurated Analysis
- High-engagement tips missed in original curation
- Obsidian-specific techniques (user priority)
- Topic clusters in new tips
- Potential "second wave" of 50-100 tips worth adding

---

## Success Criteria

1. ✅ Engagement delta report showing growth leaders
2. ✅ Uncurated tweets ranked by engagement
3. ✅ Obsidian-related tweets surfaced
4. ✅ Topic distribution analysis
5. ✅ Export to `analysis/uncurated_review.md` for human review

---

## Execution

```bash
# Run engagement delta analysis
python scripts/engagement_delta.py

# Run uncurated analysis
python scripts/analyze_uncurated.py
```

---

## Post-Analysis Questions

After running these scripts, consider:

1. Which tips had the biggest engagement surge? Why?
2. Are there high-quality tips in the uncurated set that should be added?
3. Are there Obsidian patterns worth adopting?
4. Should we create a "v2 curation" with the best uncurated tips?

---

*This handoff follows the pattern from Tip #1. Fresh instance has full context.*
