#!/usr/bin/env python3
"""
Export Claude Code Tips database to Obsidian vault.

Usage:
    python scripts/export_tips.py              # Quality tweets only (default)
    python scripts/export_tips.py --all        # Include all tweets
    python scripts/export_tips.py --limit 10   # Sample export
    python scripts/export_tips.py --output ~/custom/path
"""

import argparse
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from obsidian_export import TipsExporter


def main():
    parser = argparse.ArgumentParser(
        description="Export Claude Code Tips to Obsidian vault"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of tweets to export (for testing)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=Path(__file__).parent.parent / "Claude Code Tips",
        help="Output directory for vault (default: ./Claude Code Tips)"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db",
        help="Path to tips database"
    )
    parser.add_argument(
        "--all", "-a",
        action="store_true",
        dest="include_all",
        help="Include all tweets (skip quality filter)"
    )

    args = parser.parse_args()

    if not args.db.exists():
        print(f"Error: Database not found at {args.db}")
        sys.exit(1)

    # Quality filter is ON by default, --all disables it
    quality_filter = not args.include_all

    exporter = TipsExporter(
        db_path=args.db,
        output_dir=args.output,
        limit=args.limit,
        quality_filter=quality_filter,
    )

    exporter.export()


if __name__ == "__main__":
    main()
