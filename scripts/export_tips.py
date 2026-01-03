#!/usr/bin/env python3
"""
Export Claude Code Tips database to Obsidian vault.

Usage:
    python scripts/export_tips.py              # Full export
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
        default=Path(__file__).parent.parent / "vault",
        help="Output directory for vault (default: ./vault)"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db",
        help="Path to tips database"
    )

    args = parser.parse_args()

    if not args.db.exists():
        print(f"Error: Database not found at {args.db}")
        sys.exit(1)

    exporter = TipsExporter(
        db_path=args.db,
        output_dir=args.output,
        limit=args.limit,
    )

    exporter.export()


if __name__ == "__main__":
    main()
