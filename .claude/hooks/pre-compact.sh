#!/bin/bash
# Pre-compact hook: Updates STATUS.json before context compaction.
# Runs the wrap-up script directly (lightweight — avoids DB-heavy queries
# beyond what wrap-up-script.py already does).
#
# Hook event: PreCompact
# Matcher: (none — fires on both manual and auto compaction)

cd "$CLAUDE_PROJECT_DIR" || exit 0

# Run the wrap-up script to update STATUS.json with latest stats and commit info
python .claude/references/wrap-up-script.py 2>/dev/null

# Stage STATUS.json so it's captured before compaction
git add STATUS.json 2>/dev/null

exit 0
