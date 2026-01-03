#!/usr/bin/env python3
"""
Export Hall of Fake database to Obsidian vault.

Usage:
    python scripts/export_hof.py              # Full export
    python scripts/export_hof.py --limit 10   # Sample export
    python scripts/export_hof.py --output ~/custom/path
"""

import argparse
from pathlib import Path
import sys

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from obsidian_export import HoFExporter

# Default paths for Hall of Fake
HOF_DIR = Path.home() / "Development" / "Hall of Fake"
DEFAULT_DB = HOF_DIR / "hall_of_fake.db"
DEFAULT_OUTPUT = HOF_DIR / "vault"
DEFAULT_VIDEOS = HOF_DIR / "videos"
DEFAULT_THUMBNAILS = HOF_DIR / "thumbnails"


def main():
    parser = argparse.ArgumentParser(
        description="Export Hall of Fake to Obsidian vault"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of videos to export (for testing)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output directory for vault (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DEFAULT_DB,
        help=f"Path to Hall of Fake database (default: {DEFAULT_DB})"
    )
    parser.add_argument(
        "--videos",
        type=Path,
        default=DEFAULT_VIDEOS,
        help="Path to videos directory"
    )
    parser.add_argument(
        "--thumbnails",
        type=Path,
        default=DEFAULT_THUMBNAILS,
        help="Path to thumbnails directory"
    )

    args = parser.parse_args()

    if not args.db.exists():
        print(f"Error: Database not found at {args.db}")
        sys.exit(1)

    exporter = HoFExporter(
        db_path=args.db,
        output_dir=args.output,
        videos_dir=args.videos if args.videos.exists() else None,
        thumbnails_dir=args.thumbnails if args.thumbnails.exists() else None,
        limit=args.limit,
    )

    exporter.export()


if __name__ == "__main__":
    main()
