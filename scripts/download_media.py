#!/usr/bin/env python3
"""
Download media files for Claude Code Tips.

Downloads images and video thumbnails from Twitter to local storage,
updating the database with local paths.

Usage:
    python scripts/download_media.py
    python scripts/download_media.py --limit 5
"""

import argparse
import sqlite3
import requests
from pathlib import Path
from datetime import datetime
import shutil
import mimetypes


def get_extension_from_url(url: str) -> str:
    """Extract file extension from URL."""
    path = url.split('?')[0]
    if '.' in path.split('/')[-1]:
        return '.' + path.split('.')[-1]
    return '.jpg'


def download_file(url: str, dest_path: Path) -> bool:
    """Download a file from URL to destination path."""
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with open(dest_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"  Error downloading {url}: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download media files for Claude Code Tips"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of files to download (for testing)"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db",
        help="Path to tips database"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "media",
        help="Output directory for downloaded media"
    )
    parser.add_argument(
        "--vault",
        type=Path,
        default=Path(__file__).parent.parent / "vault" / "attachments" / "screenshots",
        help="Vault attachments directory to copy files to"
    )

    args = parser.parse_args()

    if not args.db.exists():
        print(f"Error: Database not found at {args.db}")
        return 1

    # Create output directories
    args.output.mkdir(parents=True, exist_ok=True)
    args.vault.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find media without local_path
    query = """
        SELECT id, tweet_id, media_type, url, video_url
        FROM media
        WHERE local_path IS NULL AND url IS NOT NULL
    """
    if args.limit:
        query += f" LIMIT {args.limit}"

    cursor.execute(query)
    media_items = cursor.fetchall()

    print(f"Found {len(media_items)} media items to download")

    downloaded = 0
    failed = 0

    for item in media_items:
        media_id = item['id']
        tweet_id = item['tweet_id']
        media_type = item['media_type']
        url = item['url']

        # For videos, use the video_url if available, otherwise thumbnail
        if media_type == 'video' and item['video_url']:
            download_url = item['video_url']
        else:
            download_url = url

        ext = get_extension_from_url(download_url)
        filename = f"tweet_{tweet_id}_{media_id}{ext}"
        local_path = args.output / filename

        print(f"Downloading {media_type}: {filename}")

        if download_file(download_url, local_path):
            # Update database with local path
            cursor.execute(
                "UPDATE media SET local_path = ?, downloaded_at = ? WHERE id = ?",
                (str(local_path), datetime.now().isoformat(), media_id)
            )
            conn.commit()

            # Copy to vault attachments
            vault_dest = args.vault / filename
            if not vault_dest.exists():
                shutil.copy(local_path, vault_dest)
                print(f"  Copied to vault: {vault_dest.name}")

            downloaded += 1
        else:
            failed += 1

    conn.close()

    print(f"\nComplete: {downloaded} downloaded, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
