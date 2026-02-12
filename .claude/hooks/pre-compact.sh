#!/bin/bash
# Pre-compact hook: Updates STATUS.json before context compaction.
# Runs the wrap-up script directly (lightweight — avoids DB-heavy queries
# beyond what wrap-up-script.py already does).
#
# Hook event: PreCompact
# Matcher: (none — fires on both manual and auto compaction)

LOGFILE="${CLAUDE_PROJECT_DIR:-.}/.claude/hooks/pre-compact.log"

log() {
  echo "[$(date -u '+%Y-%m-%dT%H:%M:%SZ')] $*" >> "$LOGFILE"
}

log "PRE-COMPACT FIRED — trigger=${1:-unknown} session=${CLAUDE_SESSION_ID:-??} tokens_stdin=$(wc -c < /dev/stdin 2>/dev/null || echo n/a)"

cd "$CLAUDE_PROJECT_DIR" || { log "ERROR: cd failed"; exit 0; }

# Run the wrap-up script to update STATUS.json with latest stats and commit info
if python3 .claude/references/wrap-up-script.py >> "$LOGFILE" 2>&1; then
  log "wrap-up-script.py succeeded"
else
  log "wrap-up-script.py failed (exit $?)"
fi

# Stage STATUS.json so it's captured before compaction
git add STATUS.json 2>/dev/null
log "STATUS.json staged, done"

exit 0
