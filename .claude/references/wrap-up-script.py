"""
Wrap-up script: Updates STATUS.json with live database stats and latest commit info.
Used by the /wrap-up command.
"""
import json, sqlite3, subprocess, datetime, os

os.chdir(os.path.expanduser("~/Development/claude-code-tips"))
db = sqlite3.connect('data/claude_code_tips_v2.db')

stats = {
    'tweets': db.execute("SELECT COUNT(*) FROM tweets").fetchone()[0],
    'vault_notes': len([f for f in os.listdir('Claude Code Tips') if f.endswith('.md') and not f.startswith('_')]) if os.path.isdir('Claude Code Tips') else 0,
    'threads_scraped': len([f for f in os.listdir('data/threads') if f.endswith('.json')]) if os.path.isdir('data/threads') else 0,
    'thread_replies_in_db': db.execute("SELECT COUNT(*) FROM tweets WHERE is_reply = 1").fetchone()[0],
    'links_resolved': db.execute("SELECT COUNT(*) FROM links WHERE expanded_url IS NOT NULL").fetchone()[0]
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

# Preserve active_task if it exists (from /task-plan command)
if "active_task" in existing:
    status["active_task"] = existing["active_task"]

with open('STATUS.json', 'w') as f:
    json.dump(status, f, indent=2)

db.close()
print(f"STATUS.json updated — {stats['tweets']} tweets, {stats['vault_notes']} vault notes, commit {sha}")
