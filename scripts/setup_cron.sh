#!/bin/bash
# =============================================================================
# Autonomous Bookmark Monitor — Cron Setup Guide
# =============================================================================
#
# This script documents how to set up the daily bookmark monitor as a cron job.
# It does NOT modify your crontab automatically — review and run manually.
#
# Prerequisites:
#   1. Python 3.11+ with dependencies (google-genai, requests, beautifulsoup4, python-dotenv)
#   2. GOOGLE_API_KEY set in .env or environment
#   3. Chrome running with active Twitter/X session (for fetch step)
#   4. claude CLI in PATH (optional — only needed for Chrome-based fetch)
#
# =============================================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "  Autonomous Bookmark Monitor — Cron Setup"
echo "=========================================="
echo ""
echo "Project directory: $PROJECT_DIR"
echo ""

# --- Check prerequisites ---
echo "Checking prerequisites..."
echo ""

# Python
if command -v python3 &>/dev/null; then
    PYTHON=$(command -v python3)
    echo "  [OK] Python3: $PYTHON ($(python3 --version 2>&1))"
else
    echo "  [FAIL] Python3 not found"
    exit 1
fi

# Check key Python packages
for pkg in google.genai requests bs4 dotenv; do
    if python3 -c "import $pkg" 2>/dev/null; then
        echo "  [OK] Python package: $pkg"
    else
        echo "  [WARN] Python package missing: $pkg"
        echo "         Install with: pip install google-genai requests beautifulsoup4 python-dotenv"
    fi
done

# GOOGLE_API_KEY
if [ -f "$PROJECT_DIR/.env" ]; then
    if grep -q "GOOGLE_API_KEY" "$PROJECT_DIR/.env"; then
        echo "  [OK] GOOGLE_API_KEY found in .env"
    else
        echo "  [WARN] GOOGLE_API_KEY not found in .env"
    fi
else
    echo "  [WARN] .env file not found at $PROJECT_DIR/.env"
fi

# claude CLI (optional)
if command -v claude &>/dev/null; then
    echo "  [OK] claude CLI: $(command -v claude)"
else
    echo "  [INFO] claude CLI not found — fetch step will be skipped"
    echo "         Install: https://docs.anthropic.com/en/docs/claude-code"
fi

# Database
if [ -f "$PROJECT_DIR/data/claude_code_tips_v2.db" ]; then
    echo "  [OK] Database: data/claude_code_tips_v2.db"
else
    echo "  [FAIL] Database not found"
fi

echo ""

# --- Show cron entry ---
echo "=========================================="
echo "  Recommended Cron Entry"
echo "=========================================="
echo ""
echo "Add this to your crontab (crontab -e):"
echo ""
echo "  # ──────────────────────────────────────────────────────────"
echo "  # Autonomous Bookmark Monitor — runs daily at 7:00 AM"
echo "  # Fetches new bookmarks, enriches, analyzes, generates briefing"
echo "  # ──────────────────────────────────────────────────────────"
echo "  0 7 * * * cd $PROJECT_DIR && $PYTHON scripts/daily_monitor.py --skip-fetch 2>&1 >> logs/monitor.log"
echo ""
echo "To include Chrome-based fetch (requires active Chrome session):"
echo ""
echo "  0 7 * * * cd $PROJECT_DIR && $PYTHON scripts/daily_monitor.py 2>&1 >> logs/monitor.log"
echo ""
echo "To run fetch via Claude Code CLI (most autonomous):"
echo ""
echo "  # Step 1: Fetch bookmarks via Claude Code + Chrome"
echo "  0 7 * * * cd $PROJECT_DIR && claude --chrome -p 'Run /fetch-bookmarks' 2>&1 >> logs/fetch.log"
echo "  # Step 2: Enrich + analyze + brief (30 min after fetch)"
echo "  30 7 * * * cd $PROJECT_DIR && $PYTHON scripts/daily_monitor.py --skip-fetch 2>&1 >> logs/monitor.log"
echo ""

# --- Mac wake schedule ---
echo "=========================================="
echo "  Keep Mac Awake for Cron"
echo "=========================================="
echo ""
echo "macOS sleeps by default, which prevents cron from running."
echo "Options:"
echo ""
echo "  1. Wake schedule (recommended):"
echo "     sudo pmset repeat wakeorpoweron MTWRFSU 06:55:00"
echo ""
echo "     This wakes the Mac at 6:55 AM every day, giving it time to"
echo "     be ready for the 7:00 AM cron job."
echo ""
echo "  2. Prevent sleep during work hours:"
echo "     sudo pmset repeat wakeorpoweron MTWRF 06:55:00 sleep MTWRF 22:00:00"
echo ""
echo "  3. Check current schedule:"
echo "     pmset -g sched"
echo ""
echo "  4. Remove schedule:"
echo "     sudo pmset repeat cancel"
echo ""

# --- Chrome auth notes ---
echo "=========================================="
echo "  Chrome Auth (Twitter/X)"
echo "=========================================="
echo ""
echo "The fetch step requires Chrome to be logged into x.com."
echo ""
echo "Auth tokens expire periodically. When this happens:"
echo ""
echo "  1. Open Chrome and navigate to x.com"
echo "  2. Log in if needed — tokens auto-refresh on page load"
echo "  3. The next pipeline run will capture fresh tokens"
echo ""
echo "If auth is expired when the pipeline runs:"
echo "  - The fetch step will fail gracefully"
echo "  - The pipeline continues with analysis of existing data"
echo "  - The briefing still generates (just without new tweets)"
echo "  - Check logs/monitor.log for details"
echo ""
echo "Token refresh workflow:"
echo "  1. Pipeline logs 'auth failed' in morning briefing"
echo "  2. User opens Chrome, visits x.com (auto-refreshes tokens)"
echo "  3. User runs: python scripts/daily_monitor.py"
echo "     (or waits for next morning's cron)"
echo ""

# --- Log rotation ---
echo "=========================================="
echo "  Log Management"
echo "=========================================="
echo ""
echo "Logs are written to:"
echo "  analysis/daily/YYYY-MM-DD-pipeline-HHMM.log  (per-run detail)"
echo "  logs/monitor.log                              (cron output)"
echo ""
echo "Rotate cron log monthly:"
echo "  0 0 1 * * mv $PROJECT_DIR/logs/monitor.log $PROJECT_DIR/logs/monitor-\$(date +\\%Y-\\%m).log"
echo ""

# --- Create logs directory ---
mkdir -p "$PROJECT_DIR/logs"
echo "  [OK] logs/ directory created"
echo ""

# --- Quick test ---
echo "=========================================="
echo "  Quick Test"
echo "=========================================="
echo ""
echo "Run a dry-run to verify everything works:"
echo ""
echo "  cd $PROJECT_DIR"
echo "  python scripts/daily_monitor.py --dry-run"
echo ""
echo "Run without fetch (safest for testing):"
echo ""
echo "  python scripts/daily_monitor.py --skip-fetch --skip-enrichment"
echo ""
echo "Done. Review output above and add cron entry when ready."
