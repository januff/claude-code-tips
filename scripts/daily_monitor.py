#!/usr/bin/env python3
"""
Autonomous Daily Bookmark Monitor — Orchestrator

Runs the full daily pipeline:
  1. Fetch new bookmarks (Chrome auth -> GraphQL -> SQLite)
  2. Enrichment pipeline (keywords, summaries, links)
  3. Analysis (compare new tips against LEARNINGS.md, PROGRESS.md)
  4. Generate morning briefing
  5. Deliver briefing to analysis/daily/
  6. Update STATUS.json

Design principles:
  - Graceful degradation: if Chrome auth fails, skip fetch but still analyze
  - Error isolation: each step can fail independently
  - Idempotent: safe to re-run (enrichment scripts skip already-processed items)
  - Rate limits: respects Gemini and Twitter GraphQL rate limits
  - Logging: all output goes to analysis/daily/ log file

Usage:
    python scripts/daily_monitor.py                    # Full pipeline
    python scripts/daily_monitor.py --skip-fetch       # Skip bookmark fetch (analyze existing)
    python scripts/daily_monitor.py --skip-enrichment  # Skip enrichment (analyze as-is)
    python scripts/daily_monitor.py --dry-run          # Preview what would run
    python scripts/daily_monitor.py --since 2026-02-10 # Override "since" date for analysis

Environment:
    GOOGLE_API_KEY — Required for enrichment steps (Gemini)
    Chrome with Twitter auth — Required for fetch step (skipped gracefully if unavailable)
"""

import argparse
import json
import os
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta
from io import StringIO
from pathlib import Path


# Project paths
ROOT = Path(__file__).parent.parent
SCRIPTS = ROOT / "scripts"
DB_PATH = ROOT / "data" / "claude_code_tips_v2.db"
STATUS_PATH = ROOT / "STATUS.json"
ANALYSIS_DIR = ROOT / "analysis" / "daily"
LOGS_DIR = ROOT / "logs"

# Enrichment scripts (in pipeline order)
ENRICHMENT_SCRIPTS = [
    {"name": "keywords", "script": SCRIPTS / "enrich_keywords.py", "requires_api": True},
    {"name": "summaries", "script": SCRIPTS / "enrich_summaries.py", "requires_api": True},
    {"name": "links", "script": SCRIPTS / "enrich_links.py", "requires_api": True},
]

# Rate limit: pause between enrichment scripts (seconds)
ENRICHMENT_PAUSE = 5


class PipelineLogger:
    """Simple logger that writes to both stdout and a log file."""

    def __init__(self, log_path: Path | None = None):
        self.log_path = log_path
        self.buffer = StringIO()
        self.start_time = datetime.now()

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] [{level}] {message}"
        print(line)
        self.buffer.write(line + "\n")

    def error(self, message: str):
        self.log(message, level="ERROR")

    def warn(self, message: str):
        self.log(message, level="WARN")

    def section(self, title: str):
        separator = "=" * 60
        self.log("")
        self.log(separator)
        self.log(f"  {title}")
        self.log(separator)

    def save(self):
        """Save log buffer to file."""
        if self.log_path:
            self.log_path.parent.mkdir(parents=True, exist_ok=True)
            elapsed = datetime.now() - self.start_time
            self.buffer.write(f"\n--- Pipeline completed in {elapsed} ---\n")
            self.log_path.write_text(self.buffer.getvalue())
            print(f"\nLog saved to {self.log_path}")


class PipelineResult:
    """Track results of each pipeline step."""

    def __init__(self):
        self.steps: list[dict] = []
        self.new_tweet_ids: list[str] = []
        self.fetch_succeeded = False
        self.enrichment_succeeded = False
        self.analysis_succeeded = False
        self.briefing_succeeded = False

    def add_step(self, name: str, success: bool, message: str = "", duration: float = 0):
        self.steps.append({
            "name": name,
            "success": success,
            "message": message,
            "duration_seconds": round(duration, 1),
        })

    def summary(self) -> dict:
        succeeded = sum(1 for s in self.steps if s["success"])
        failed = sum(1 for s in self.steps if not s["success"])
        return {
            "total_steps": len(self.steps),
            "succeeded": succeeded,
            "failed": failed,
            "steps": self.steps,
            "new_tweets_found": len(self.new_tweet_ids),
        }


def get_last_run_date() -> str | None:
    """Get the date of the last successful pipeline run from STATUS.json."""
    try:
        status = json.loads(STATUS_PATH.read_text())
        return status.get("key_dates", {}).get("last_bookmark_fetch")
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        return None


def get_tweet_count(db_path: Path) -> int:
    """Get current tweet count from database."""
    try:
        conn = sqlite3.connect(db_path)
        count = conn.execute("SELECT COUNT(*) FROM tweets").fetchone()[0]
        conn.close()
        return count
    except Exception:
        return 0


def step_fetch_bookmarks(logger: PipelineLogger, result: PipelineResult, dry_run: bool = False) -> bool:
    """Step 1: Fetch new bookmarks from Twitter/X.

    This step requires Chrome with active Twitter auth. If auth is unavailable,
    it fails gracefully and the pipeline continues with analysis of existing data.

    NOTE: This step shells out to Claude Code with --chrome flag, which requires
    the claude CLI to be available and Chrome to be running with Twitter auth.
    For fully autonomous operation, this would be invoked via cron calling:
        claude --chrome -p "Run /fetch-bookmarks"

    For the Python-only pipeline, we skip this and rely on manual fetch or
    pre-existing data in the database.
    """
    logger.section("Step 1: Fetch Bookmarks")

    if dry_run:
        logger.log("DRY RUN: Would attempt to fetch new bookmarks via Chrome auth")
        logger.log("  Requires: claude --chrome CLI, active Twitter session")
        result.add_step("fetch_bookmarks", True, "dry run — skipped")
        return True

    # Check if there are recent JSON files from manual fetch
    data_dir = ROOT / "data"
    today = datetime.now().strftime("%Y-%m-%d")
    recent_files = list(data_dir.glob(f"new_bookmarks_{today}*.json"))

    if recent_files:
        logger.log(f"Found {len(recent_files)} bookmark file(s) from today:")
        for f in recent_files:
            logger.log(f"  {f.name}")
        result.fetch_succeeded = True
        result.add_step("fetch_bookmarks", True, f"using {len(recent_files)} existing file(s)")
        return True

    # Attempt Chrome-based fetch via subprocess
    # This is the main fetch path — requires `claude` CLI with --chrome
    logger.log("No bookmark files from today found.")
    logger.log("Attempting Chrome-based fetch...")

    try:
        # Check if claude CLI is available
        check = subprocess.run(
            ["which", "claude"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if check.returncode != 0:
            logger.warn("claude CLI not found in PATH — skipping fetch")
            logger.log("Fallback: pipeline will analyze existing data")
            result.add_step("fetch_bookmarks", False, "claude CLI not available")
            return False

        logger.log("claude CLI found — but automated Chrome fetch requires interactive session")
        logger.log("Fallback: run manually with `claude --chrome` then `/fetch-bookmarks`")
        result.add_step("fetch_bookmarks", False, "requires interactive Chrome session")
        return False

    except subprocess.TimeoutExpired:
        logger.warn("Timed out checking for claude CLI")
        result.add_step("fetch_bookmarks", False, "timeout")
        return False
    except Exception as e:
        logger.error(f"Fetch failed: {e}")
        result.add_step("fetch_bookmarks", False, str(e))
        return False


def step_enrichment(
    logger: PipelineLogger,
    result: PipelineResult,
    dry_run: bool = False,
    skip: bool = False,
) -> bool:
    """Step 2: Run enrichment pipeline (keywords, summaries, links).

    Calls existing enrichment scripts as subprocesses. Each script:
    - Skips already-enriched items (idempotent)
    - Has its own --dry-run flag
    - Requires GOOGLE_API_KEY for Gemini calls
    """
    logger.section("Step 2: Enrichment Pipeline")

    if skip:
        logger.log("Enrichment skipped (--skip-enrichment flag)")
        result.add_step("enrichment", True, "skipped by user")
        return True

    if dry_run:
        logger.log("DRY RUN: Would run enrichment scripts:")
        for s in ENRICHMENT_SCRIPTS:
            logger.log(f"  {s['name']}: {s['script'].name}")
        result.add_step("enrichment", True, "dry run — skipped")
        return True

    # Check for API key
    if not os.environ.get("GOOGLE_API_KEY"):
        logger.warn("GOOGLE_API_KEY not set — skipping enrichment")
        logger.log("Set GOOGLE_API_KEY in .env or environment to enable enrichment")
        result.add_step("enrichment", False, "GOOGLE_API_KEY not set")
        result.enrichment_succeeded = False
        return False

    all_succeeded = True

    for script_info in ENRICHMENT_SCRIPTS:
        name = script_info["name"]
        script = script_info["script"]

        if not script.exists():
            logger.warn(f"Script not found: {script} — skipping {name}")
            result.add_step(f"enrich_{name}", False, "script not found")
            continue

        logger.log(f"Running {name} enrichment...")
        start = time.time()

        try:
            proc = subprocess.run(
                [sys.executable, str(script)],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout per script
                cwd=str(ROOT),
            )

            duration = time.time() - start

            if proc.returncode == 0:
                # Extract summary from output
                output_lines = proc.stdout.strip().split("\n")
                summary_line = output_lines[-1] if output_lines else "completed"
                logger.log(f"  {name}: {summary_line}")
                result.add_step(f"enrich_{name}", True, summary_line, duration)
            else:
                logger.warn(f"  {name} failed (exit {proc.returncode})")
                if proc.stderr:
                    for line in proc.stderr.strip().split("\n")[:5]:
                        logger.log(f"    stderr: {line}")
                result.add_step(f"enrich_{name}", False, f"exit {proc.returncode}", duration)
                all_succeeded = False

        except subprocess.TimeoutExpired:
            logger.error(f"  {name} timed out after 5 minutes")
            result.add_step(f"enrich_{name}", False, "timeout", 300)
            all_succeeded = False
        except Exception as e:
            logger.error(f"  {name} error: {e}")
            result.add_step(f"enrich_{name}", False, str(e))
            all_succeeded = False

        # Pause between scripts to respect rate limits
        if script_info != ENRICHMENT_SCRIPTS[-1]:
            logger.log(f"  Pausing {ENRICHMENT_PAUSE}s for rate limits...")
            time.sleep(ENRICHMENT_PAUSE)

    result.enrichment_succeeded = all_succeeded
    return all_succeeded


def step_analysis(
    logger: PipelineLogger,
    result: PipelineResult,
    since: str | None = None,
    dry_run: bool = False,
) -> Path | None:
    """Step 3: Analyze new tips against knowledge base.

    Runs analyze_new_tips.py and saves output as JSON.
    Returns path to analysis JSON file, or None on failure.
    """
    logger.section("Step 3: Analysis")

    # Determine the "since" date
    if not since:
        since = get_last_run_date()
        if not since:
            # Default to yesterday
            since = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    logger.log(f"Analyzing tips since: {since}")

    analysis_script = SCRIPTS / "analyze_new_tips.py"
    if not analysis_script.exists():
        logger.error(f"Analysis script not found: {analysis_script}")
        result.add_step("analysis", False, "script not found")
        return None

    date_str = datetime.now().strftime("%Y-%m-%d")
    output_path = ANALYSIS_DIR / f"{date_str}-analysis.json"

    if dry_run:
        logger.log(f"DRY RUN: Would run analysis, output to {output_path}")
        result.add_step("analysis", True, "dry run — skipped")
        return None

    start = time.time()

    try:
        cmd = [
            sys.executable, str(analysis_script),
            "--since", since,
            "--output", str(output_path),
        ]

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(ROOT),
        )

        duration = time.time() - start

        if proc.returncode == 0:
            # Parse stderr for summary
            stderr_lines = proc.stderr.strip().split("\n") if proc.stderr else []
            summary_line = stderr_lines[-1] if stderr_lines else "completed"
            logger.log(f"  Analysis: {summary_line}")
            result.add_step("analysis", True, summary_line, duration)
            result.analysis_succeeded = True
            return output_path
        else:
            logger.error(f"Analysis failed (exit {proc.returncode})")
            if proc.stderr:
                for line in proc.stderr.strip().split("\n")[:5]:
                    logger.log(f"  stderr: {line}")
            result.add_step("analysis", False, f"exit {proc.returncode}", duration)
            return None

    except subprocess.TimeoutExpired:
        logger.error("Analysis timed out after 2 minutes")
        result.add_step("analysis", False, "timeout", 120)
        return None
    except Exception as e:
        logger.error(f"Analysis error: {e}")
        result.add_step("analysis", False, str(e))
        return None


def step_briefing(
    logger: PipelineLogger,
    result: PipelineResult,
    analysis_path: Path | None,
    dry_run: bool = False,
) -> Path | None:
    """Step 4: Generate morning briefing from analysis.

    Runs generate_briefing.py with the analysis JSON.
    Returns path to briefing markdown file, or None on failure.
    """
    logger.section("Step 4: Generate Briefing")

    if analysis_path is None:
        logger.warn("No analysis data available — generating empty briefing")
        # Generate a minimal briefing noting that analysis was not available
        date_str = datetime.now().strftime("%Y-%m-%d")
        briefing_path = ANALYSIS_DIR / f"{date_str}-briefing.md"
        if not dry_run:
            briefing_path.parent.mkdir(parents=True, exist_ok=True)
            briefing_path.write_text(
                f"# Morning Briefing: {date_str}\n\n"
                f"*Generated {datetime.now().strftime('%Y-%m-%d at %H:%M')}*\n\n"
                "## Summary\n\n"
                "No new tips to analyze. Analysis step was skipped or failed.\n\n"
                "Check the pipeline log for details.\n"
            )
            logger.log(f"Minimal briefing written to {briefing_path}")
        else:
            logger.log("DRY RUN: Would write minimal briefing")
        result.add_step("briefing", True, "minimal briefing (no analysis)")
        return briefing_path if not dry_run else None

    briefing_script = SCRIPTS / "generate_briefing.py"
    if not briefing_script.exists():
        logger.error(f"Briefing script not found: {briefing_script}")
        result.add_step("briefing", False, "script not found")
        return None

    if dry_run:
        logger.log(f"DRY RUN: Would generate briefing from {analysis_path}")
        result.add_step("briefing", True, "dry run — skipped")
        return None

    start = time.time()

    try:
        cmd = [
            sys.executable, str(briefing_script),
            "--analysis", str(analysis_path),
            "--output", str(ANALYSIS_DIR),
        ]

        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
            cwd=str(ROOT),
        )

        duration = time.time() - start

        if proc.returncode == 0:
            # Determine output path
            date_str = datetime.now().strftime("%Y-%m-%d")
            briefing_path = ANALYSIS_DIR / f"{date_str}-briefing.md"
            logger.log(f"  Briefing written to {briefing_path}")
            result.add_step("briefing", True, str(briefing_path), duration)
            result.briefing_succeeded = True
            return briefing_path
        else:
            logger.error(f"Briefing generation failed (exit {proc.returncode})")
            if proc.stderr:
                for line in proc.stderr.strip().split("\n")[:5]:
                    logger.log(f"  stderr: {line}")
            result.add_step("briefing", False, f"exit {proc.returncode}", duration)
            return None

    except subprocess.TimeoutExpired:
        logger.error("Briefing generation timed out")
        result.add_step("briefing", False, "timeout", 60)
        return None
    except Exception as e:
        logger.error(f"Briefing error: {e}")
        result.add_step("briefing", False, str(e))
        return None


def step_update_status(
    logger: PipelineLogger,
    result: PipelineResult,
    briefing_path: Path | None,
    dry_run: bool = False,
) -> bool:
    """Step 5: Update STATUS.json with pipeline run results."""
    logger.section("Step 5: Update STATUS.json")

    if dry_run:
        logger.log("DRY RUN: Would update STATUS.json")
        result.add_step("update_status", True, "dry run — skipped")
        return True

    try:
        # Read current STATUS.json
        if STATUS_PATH.exists():
            status = json.loads(STATUS_PATH.read_text())
        else:
            status = {}

        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")

        # Update timestamps
        status["updated_at"] = now.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        status["updated_by"] = "daily-monitor"

        # Update key dates
        if "key_dates" not in status:
            status["key_dates"] = {}
        status["key_dates"]["last_monitor_run"] = date_str

        if result.fetch_succeeded:
            status["key_dates"]["last_bookmark_fetch"] = date_str

        # Update stats from database
        tweet_count = get_tweet_count(DB_PATH)
        if tweet_count > 0 and "stats" in status:
            status["stats"]["tweets"] = tweet_count

        # Add pipeline result to recent_changes
        pipeline_summary = result.summary()
        change_msg = (
            f"Daily monitor: {pipeline_summary['succeeded']}/{pipeline_summary['total_steps']} steps succeeded"
        )
        if pipeline_summary["new_tweets_found"] > 0:
            change_msg += f", {pipeline_summary['new_tweets_found']} new tweets"

        if "recent_changes" not in status:
            status["recent_changes"] = []
        status["recent_changes"].insert(0, change_msg)
        status["recent_changes"] = status["recent_changes"][:10]  # Keep last 10

        # Write
        STATUS_PATH.write_text(json.dumps(status, indent=2) + "\n")
        logger.log(f"STATUS.json updated: {change_msg}")
        result.add_step("update_status", True, change_msg)
        return True

    except Exception as e:
        logger.error(f"Failed to update STATUS.json: {e}")
        result.add_step("update_status", False, str(e))
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Autonomous Daily Bookmark Monitor — runs the full pipeline"
    )
    parser.add_argument(
        "--skip-fetch",
        action="store_true",
        help="Skip bookmark fetching (analyze existing data only)",
    )
    parser.add_argument(
        "--skip-enrichment",
        action="store_true",
        help="Skip enrichment pipeline (analyze data as-is)",
    )
    parser.add_argument(
        "--since",
        type=str,
        help="Override 'since' date for analysis (YYYY-MM-DD)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would run without executing",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DB_PATH,
        help="Path to tips database",
    )

    args = parser.parse_args()

    # Setup logging
    date_str = datetime.now().strftime("%Y-%m-%d")
    time_str = datetime.now().strftime("%H%M")
    log_path = ANALYSIS_DIR / f"{date_str}-pipeline-{time_str}.log"
    logger = PipelineLogger(log_path=None if args.dry_run else log_path)
    result = PipelineResult()

    logger.section("Daily Bookmark Monitor Pipeline")
    logger.log(f"Date: {date_str}")
    logger.log(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    logger.log(f"Database: {args.db}")

    if not args.db.exists():
        logger.error(f"Database not found: {args.db}")
        return 1

    # Pre-run stats
    pre_count = get_tweet_count(args.db)
    logger.log(f"Current tweet count: {pre_count}")

    # Step 1: Fetch
    if args.skip_fetch:
        logger.section("Step 1: Fetch Bookmarks (SKIPPED)")
        logger.log("Skipped by --skip-fetch flag")
        result.add_step("fetch_bookmarks", True, "skipped by user")
    else:
        step_fetch_bookmarks(logger, result, dry_run=args.dry_run)

    # Check for new tweets after fetch
    post_count = get_tweet_count(args.db)
    new_count = post_count - pre_count
    if new_count > 0:
        logger.log(f"New tweets detected: {new_count} (was {pre_count}, now {post_count})")

    # Step 2: Enrichment
    step_enrichment(logger, result, dry_run=args.dry_run, skip=args.skip_enrichment)

    # Step 3: Analysis
    analysis_path = step_analysis(logger, result, since=args.since, dry_run=args.dry_run)

    # Step 4: Briefing
    briefing_path = step_briefing(logger, result, analysis_path, dry_run=args.dry_run)

    # Step 5: Update STATUS.json
    step_update_status(logger, result, briefing_path, dry_run=args.dry_run)

    # Final summary
    logger.section("Pipeline Complete")
    summary = result.summary()
    logger.log(f"Steps: {summary['succeeded']}/{summary['total_steps']} succeeded")
    for step in summary["steps"]:
        status_icon = "[OK]" if step["success"] else "[FAIL]"
        duration = f" ({step['duration_seconds']}s)" if step["duration_seconds"] > 0 else ""
        logger.log(f"  {status_icon} {step['name']}: {step['message']}{duration}")

    if briefing_path and briefing_path.exists():
        logger.log(f"\nBriefing: {briefing_path}")
    else:
        logger.log("\nNo briefing generated.")

    # Save log
    logger.save()

    # Exit code: 0 if at least analysis or briefing succeeded
    if result.analysis_succeeded or result.briefing_succeeded:
        return 0
    elif args.dry_run:
        return 0
    else:
        return 1


if __name__ == "__main__":
    sys.exit(main())
