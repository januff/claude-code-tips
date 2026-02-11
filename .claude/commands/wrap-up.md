# Wrap Up Session

**MANDATORY** at the end of every Claude Code session. Updates STATUS.json with live data.

## What This Command Does

1. Queries the database for current stats
2. Reads the latest git commit
3. Updates STATUS.json with fresh numbers
4. Stages and commits STATUS.json
5. Reports what changed

## Implementation

Run this Python script:

```python
import json, sqlite3, subprocess, datetime, os

os.chdir(os.path.expanduser("~/Development/claude-code-tips"))
db = sqlite3.connect('data/claude_code_tips_v2.db')

stats = {
    'tweets': db.execute("SELECT COUNT(*) FROM tweets").fetchone()[0],
    'vault_notes': len([f for f in os.listdir('Claude Code Tips') if f.endswith('.md') and not f.startswith('_')]) if os.path.isdir('Claude Code Tips') else 0,
    'threads_scraped': db.execute("SELECT COUNT(DISTINCT conversation_id) FROM tweets WHERE conversation_id IS NOT NULL AND conversation_id != tweet_id").fetchone()[0],
    'total_replies': db.execute("SELECT COUNT(*) FROM tweets WHERE in_reply_to_tweet_id IS NOT NULL").fetchone()[0],
    'links_resolved': db.execute("SELECT COUNT(*) FROM links WHERE resolved_url IS NOT NULL").fetchone()[0]
}

sha = subprocess.check_output(['git', 'log', '-1', '--format=%h']).decode().strip()
msg = subprocess.check_output(['git', 'log', '-1', '--format=%s']).decode().strip()
date = subprocess.check_output(['git', 'log', '-1', '--format=%aI']).decode().strip()

# Load existing STATUS.json to preserve recent_changes and known_issues
existing = {}
if os.path.exists('STATUS.json'):
    with open('STATUS.json') as f:
        existing = json.load(f)

status = {
    "updated_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    "updated_by": "claude-code",
    "last_commit": {"sha": sha, "message": msg, "date": date},
    "stats": stats,
    "recent_changes": existing.get("recent_changes", []),
    "known_issues": existing.get("known_issues", []),
    "key_dates": existing.get("key_dates", {})
}

with open('STATUS.json', 'w') as f:
    json.dump(status, f, indent=2)

db.close()
print(f"✅ STATUS.json updated — {stats['tweets']} tweets, {stats['vault_notes']} vault notes, commit {sha}")
```

After updating STATUS.json, stage and commit:

```bash
git add STATUS.json
git commit -m "chore: wrap-up — update STATUS.json"
```

## When to Add to recent_changes

If you made substantive changes this session (new features, bug fixes, data operations), update the `recent_changes` array in STATUS.json BEFORE the wrap-up commit. Keep the list to 5-7 items, removing the oldest entries as new ones are added.

## When to Update known_issues

If you fixed a known issue, remove it. If you discovered a new one, add it.

## When to Update key_dates

Update `last_bookmark_fetch` after running `/fetch-bookmarks`. Update `last_vault_export` after running `export_tips.py`.
