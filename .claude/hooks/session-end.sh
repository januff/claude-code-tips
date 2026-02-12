#!/bin/bash
# Session-end hook: Safety net to update STATUS.json if it wasn't updated this session.
# Only runs the wrap-up script if STATUS.json is stale (not updated in the last 5 minutes,
# suggesting no wrap-up happened recently).
#
# Hook event: SessionEnd
# Matcher: (none — fires on all exit reasons)

cd "$CLAUDE_PROJECT_DIR" || exit 0

STATUS_FILE="STATUS.json"

if [ ! -f "$STATUS_FILE" ]; then
  exit 0
fi

# Check if STATUS.json was modified in the last 5 minutes (likely already wrapped up)
if [ "$(uname)" = "Darwin" ]; then
  # macOS: find files modified within the last 5 minutes
  RECENT=$(find "$STATUS_FILE" -mmin -5 2>/dev/null)
else
  # Linux
  RECENT=$(find "$STATUS_FILE" -mmin -5 2>/dev/null)
fi

if [ -z "$RECENT" ]; then
  # STATUS.json is stale — run minimal wrap-up
  python .claude/references/wrap-up-script.py 2>/dev/null
  git add STATUS.json 2>/dev/null
fi

exit 0
