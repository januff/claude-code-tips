# Handoff: Reconcile Curated Tips with Raw Tweets

**Created by:** Claude.ai (Opus 4.5)
**Date:** 2025-12-29
**Status:** 📋 READY FOR EXECUTION
**Code word:** context-first

---

## Purpose

Match the 109 curated tips from `tips/full-thread.md` with raw tweets in `claude_code_tips.db`, creating entries in the `tips` table with `is_curated = 1` and category assignments.

---

## The Reconciliation Challenge

**Problem:** The curated tips don't have tweet IDs. We must match by:
1. **Author handle** (exact match: `@zeroxBigBoss` → `@zeroxBigBoss`)
2. **Text similarity** (fuzzy match: curated summary → raw tweet text)

**Why this is tricky:**
- Curated tips are often summaries/paraphrases, not verbatim quotes
- Some authors have multiple tweets in the thread
- Handle format may vary (`@username` vs `username`)

---

## Input Files

### 1. Curated Tips Source
**File:** `tips/full-thread.md`
**Count:** 109 tips
**Format:**
```markdown
### 1. The Handoff Technique
**Author:** @zeroxBigBoss
**Tip:** Generate a prompt for handing off work to another AI agent...
**Engagement:** 3 replies | 2 reposts | 160 likes | 9K views
```

### 2. Category Mappings Source
**File:** `tips/grouped-tips.md`
**Format:**
```markdown
## Context & Session Management

**The Handoff** (@zeroxBigBoss) — Generate a self-contained prompt...
```

**Category mappings (grouped-tips.md → tip_categories):**
| Section Header | DB Category |
|----------------|-------------|
| Context & Session Management | context |
| Planning & Workflow | planning |
| Documentation & Memory | documentation |
| Custom Skills & Tools | skills |
| Prompting Techniques | prompting |
| Subagents & Parallel Work | subagents |
| Integration & External Tools | integration |
| Code Quality & Review | code_quality |
| Session & Environment Setup | context |
| Specialized Techniques | skills |

### 3. Raw Tweets Source
**Database:** `claude_code_tips.db`
**Table:** `tweets` (343 records)
**Key fields:** `id`, `handle`, `text`, `url`

---

## Matching Strategy

### Step 1: Parse full-thread.md
Extract from each tip:
- `tip_number` (1-109)
- `author_handle` (normalize: strip @, lowercase)
- `tip_text` (the **Tip:** content)
- `tip_title` (e.g., "The Handoff Technique")

### Step 2: Parse grouped-tips.md for categories
Build mapping: `(author_handle, tip_name) → category`

### Step 3: Match against tweets table
For each curated tip:

```python
# First: exact handle match
cursor.execute("""
    SELECT id, handle, text FROM tweets 
    WHERE LOWER(REPLACE(handle, '@', '')) = ?
""", (normalized_handle,))
candidates = cursor.fetchall()

# If single match: done
if len(candidates) == 1:
    return candidates[0]

# If multiple matches: use text similarity
# Find best match using fuzzy string matching
best_match = max(candidates, key=lambda t: similarity(tip_text, t['text']))
```

### Step 4: Create tips table entries
```python
cursor.execute("""
    INSERT INTO tips (tweet_id, tip_number, category, summary, is_curated, notes)
    VALUES (?, ?, ?, ?, 1, ?)
""", (matched_tweet_id, tip_number, category, tip_title, "Matched from full-thread.md"))
```

---

## Implementation Script

Create `scripts/reconcile_curated_tips.py`:

```python
#!/usr/bin/env python3
"""
Reconcile curated tips from full-thread.md with raw tweets in SQLite.
Creates entries in tips table with is_curated=1.

Created: 2025-12-29
Source: plans/HANDOFF_RECONCILE_TIPS.md
"""

import re
import sqlite3
from pathlib import Path
from difflib import SequenceMatcher

DB_PATH = Path(__file__).parent.parent / "claude_code_tips.db"
FULL_THREAD_PATH = Path(__file__).parent.parent / "tips" / "full-thread.md"
GROUPED_TIPS_PATH = Path(__file__).parent.parent / "tips" / "grouped-tips.md"


def parse_full_thread(filepath):
    """Parse full-thread.md to extract tips."""
    content = filepath.read_text()
    tips = []
    
    # Pattern to match each tip block
    pattern = r'### (\d+)\. (.+?)\n\*\*Author:\*\* @(\w+)\n\*\*Tip:\*\* (.+?)(?=\n\*\*Engagement|\n---|\n###|\Z)'
    
    for match in re.finditer(pattern, content, re.DOTALL):
        tips.append({
            'number': int(match.group(1)),
            'title': match.group(2).strip(),
            'handle': match.group(3).lower(),
            'text': match.group(4).strip()
        })
    
    return tips


def parse_category_mappings(filepath):
    """Parse grouped-tips.md to extract category assignments."""
    content = filepath.read_text()
    mappings = {}
    
    # Category header to DB name mapping
    category_map = {
        'Context & Session Management': 'context',
        'Planning & Workflow': 'planning',
        'Documentation & Memory': 'documentation',
        'Custom Skills & Tools': 'skills',
        'Prompting Techniques': 'prompting',
        'Subagents & Parallel Work': 'subagents',
        'Integration & External Tools': 'integration',
        'Code Quality & Review': 'code_quality',
        'Session & Environment Setup': 'context',
        'Specialized Techniques': 'skills',
    }
    
    current_category = None
    
    for line in content.split('\n'):
        # Check for category header
        if line.startswith('## '):
            header = line[3:].strip()
            current_category = category_map.get(header)
        
        # Check for tip entry: **Tip Name** (@handle)
        if current_category and line.startswith('**') and '(@' in line:
            match = re.search(r'\(@(\w+)\)', line)
            if match:
                handle = match.group(1).lower()
                mappings[handle] = current_category
    
    return mappings


def similarity(a, b):
    """Calculate string similarity ratio."""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


def find_matching_tweet(cursor, tip, threshold=0.3):
    """Find the best matching tweet for a curated tip."""
    # Get all tweets from this author
    cursor.execute("""
        SELECT id, handle, text, url FROM tweets 
        WHERE LOWER(REPLACE(handle, '@', '')) = ?
    """, (tip['handle'],))
    
    candidates = cursor.fetchall()
    
    if not candidates:
        return None, "No tweets from this author"
    
    if len(candidates) == 1:
        return candidates[0], "Single author match"
    
    # Multiple tweets from same author - use text similarity
    best_match = None
    best_score = 0
    
    for candidate in candidates:
        score = similarity(tip['text'], candidate[2])  # candidate[2] is text
        if score > best_score:
            best_score = score
            best_match = candidate
    
    if best_score >= threshold:
        return best_match, f"Best text match (score: {best_score:.2f})"
    else:
        return best_match, f"Low confidence match (score: {best_score:.2f})"


def reconcile(dry_run=False):
    """Main reconciliation process."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Parse sources
    tips = parse_full_thread(FULL_THREAD_PATH)
    categories = parse_category_mappings(GROUPED_TIPS_PATH)
    
    print(f"📖 Parsed {len(tips)} curated tips")
    print(f"📂 Parsed {len(categories)} category mappings")
    
    matched = 0
    unmatched = 0
    low_confidence = 0
    
    for tip in tips:
        tweet, match_type = find_matching_tweet(cursor, tip)
        category = categories.get(tip['handle'], 'uncategorized')
        
        if tweet is None:
            print(f"❌ #{tip['number']} {tip['title']} (@{tip['handle']}): {match_type}")
            unmatched += 1
            continue
        
        if "Low confidence" in match_type:
            print(f"⚠️  #{tip['number']} {tip['title']} (@{tip['handle']}): {match_type}")
            low_confidence += 1
        else:
            print(f"✅ #{tip['number']} {tip['title']} (@{tip['handle']}): {match_type}")
            matched += 1
        
        if not dry_run:
            # Insert into tips table
            cursor.execute("""
                INSERT OR REPLACE INTO tips 
                (tweet_id, tip_number, category, summary, is_curated, notes)
                VALUES (?, ?, ?, ?, 1, ?)
            """, (
                tweet[0],  # id
                tip['number'],
                category,
                tip['title'],
                f"Matched from full-thread.md. {match_type}"
            ))
    
    if not dry_run:
        conn.commit()
    
    print(f"\n📊 Results:")
    print(f"   ✅ Matched: {matched}")
    print(f"   ⚠️  Low confidence: {low_confidence}")
    print(f"   ❌ Unmatched: {unmatched}")
    print(f"   Total: {len(tips)}")
    
    conn.close()
    
    return matched, low_confidence, unmatched


if __name__ == "__main__":
    import sys
    
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("🔍 DRY RUN - no changes will be made\n")
    
    reconcile(dry_run=dry_run)
```

---

## Execution

### Step 1: Dry run to see matches
```bash
cd ~/path/to/claude-code-tips
python scripts/reconcile_curated_tips.py --dry-run
```

### Step 2: Review output
- Check ❌ unmatched tips (may need manual investigation)
- Check ⚠️ low confidence matches (may be wrong author tweets)

### Step 3: Execute reconciliation
```bash
python scripts/reconcile_curated_tips.py
```

### Step 4: Verify
```bash
sqlite3 claude_code_tips.db "SELECT COUNT(*) FROM tips WHERE is_curated = 1"
# Should return: ~109 (minus any unmatched)
```

---

## Expected Issues

### Authors with multiple tweets
Some authors have more than one reply in the thread. The script uses text similarity to pick the best match, but may need manual review.

### Handle variations
The curated tips use `@username` format. Script normalizes both sources.

### Missing authors
Some tweets may have been deleted or from accounts now suspended. These will show as unmatched.

---

## Post-Reconciliation Queries

After reconciliation, useful queries:

```sql
-- Curated tips by category
SELECT category, COUNT(*) FROM tips 
WHERE is_curated = 1 
GROUP BY category ORDER BY COUNT(*) DESC;

-- Tips not yet categorized
SELECT t.id, t.handle, t.text 
FROM tweets t
LEFT JOIN tips tip ON t.id = tip.tweet_id
WHERE tip.id IS NULL
LIMIT 20;

-- All curated tips with engagement
SELECT tip.tip_number, tip.summary, tw.handle, tw.likes, tw.views
FROM tips tip
JOIN tweets tw ON tip.tweet_id = tw.id
WHERE tip.is_curated = 1
ORDER BY tw.likes DESC;
```

---

## Success Criteria

1. ✅ 90%+ of 109 tips matched (expect ~100+)
2. ✅ Category assignments populated from grouped-tips.md
3. ✅ `tips` table has `is_curated = 1` entries
4. ⚠️ Manual review list for low-confidence matches

---

## Optional: Second Pass for Remaining 234 Tweets

After curated tips are reconciled, the remaining 234 tweets (343 - 109) are "uncurated" — they exist in the thread but weren't in the original manual curation.

Future task: Review uncurated tweets for additional tips worth adding.

```sql
-- Find uncurated tweets with high engagement
SELECT t.handle, t.text, t.likes, t.views, t.url
FROM tweets t
LEFT JOIN tips tip ON t.id = tip.tweet_id  
WHERE tip.id IS NULL
ORDER BY t.likes DESC
LIMIT 30;
```

---

*This handoff follows the pattern from Tip #1. Fresh instance has full context.*
