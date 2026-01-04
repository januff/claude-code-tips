#!/usr/bin/env python3
"""
Enrich media (videos and screenshots) with Gemini Vision analysis.

Extracts workflow details, commands shown, and key actions from media.

Usage:
    python scripts/enrich_media.py --limit 10  # Sample run
    python scripts/enrich_media.py             # Full run

Environment:
    GOOGLE_API_KEY - Gemini API key required
"""

import argparse
import base64
import json
import os
import sqlite3
import subprocess
import tempfile
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / ".env")


VIDEO_PROMPT = """This is a screen recording from a Claude Code tutorial tweet.
Describe the WORKFLOW being demonstrated:
- What buttons/UI elements are clicked?
- What commands are typed?
- What is the end result?

Be specific about command names, flags, and UI elements.
Return JSON only (no markdown):
{
  "workflow_summary": "one paragraph description",
  "commands_shown": ["--teleport session_id", "claude --resume"],
  "ui_elements": ["Open in CLI button", "Cursor terminal"],
  "key_action": "the main thing being demonstrated"
}"""


IMAGE_PROMPT = """This is a screenshot from a Claude Code tip tweet.
Extract:
- Any visible command text or code
- Settings or configuration shown
- Key information displayed

Return JSON only (no markdown):
{
  "extracted_text": "literal text visible",
  "content_type": "code|settings|terminal|ui|other",
  "summary": "what this screenshot shows",
  "commands_shown": ["any commands visible"],
  "key_action": "the main thing being shown"
}"""


def extract_frames(video_path: Path, num_frames: int = 4) -> list[bytes]:
    """Extract frames from video and return as bytes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_pattern = Path(tmpdir) / "frame_%03d.jpg"

        # Get video duration
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=noprint_wrappers=1:nokey=1", str(video_path)],
            capture_output=True, text=True
        )
        try:
            duration = float(result.stdout.strip())
            fps = num_frames / duration if duration > 0 else 1
        except ValueError:
            fps = 1  # Fallback

        subprocess.run(
            ["ffmpeg", "-y", "-i", str(video_path), "-vf", f"fps={fps}",
             "-frames:v", str(num_frames), str(output_pattern)],
            capture_output=True, check=True
        )

        frames = []
        for frame_file in sorted(Path(tmpdir).glob("frame_*.jpg")):
            with open(frame_file, "rb") as f:
                frames.append(f.read())

        return frames


def analyze_media(client, media_path: Path, is_video: bool) -> dict | None:
    """Analyze media with Gemini Vision."""
    try:
        if is_video:
            frames = extract_frames(media_path, num_frames=4)
            if not frames:
                print(f"  No frames extracted from {media_path}")
                return None

            content_parts = []
            for frame in frames:
                content_parts.append(types.Part.from_bytes(data=frame, mime_type="image/jpeg"))
            content_parts.append({"text": VIDEO_PROMPT})
        else:
            # Image - read directly
            with open(media_path, "rb") as f:
                image_data = f.read()

            # Determine mime type
            suffix = media_path.suffix.lower()
            mime_type = {
                ".jpg": "image/jpeg",
                ".jpeg": "image/jpeg",
                ".png": "image/png",
                ".gif": "image/gif",
                ".webp": "image/webp"
            }.get(suffix, "image/jpeg")

            content_parts = [
                types.Part.from_bytes(data=image_data, mime_type=mime_type),
                {"text": IMAGE_PROMPT}
            ]

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=content_parts
        )

        text = response.text.strip()

        # Clean up response - sometimes wrapped in markdown
        if text.startswith('```'):
            text = text.split('\n', 1)[1]
            text = text.rsplit('```', 1)[0]

        parsed = json.loads(text)

        # Handle if the response is wrapped in a list
        if isinstance(parsed, list) and len(parsed) > 0:
            parsed = parsed[0]

        return parsed

    except json.JSONDecodeError as e:
        print(f"  JSON parse error: {e}")
        return None
    except Exception as e:
        print(f"  Analysis error: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(
        description="Enrich media with Gemini Vision analysis"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit number of media items to process"
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).parent.parent / "data" / "claude_code_tips_v2.db",
        help="Path to tips database"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-process media even if already enriched"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without making API calls"
    )

    args = parser.parse_args()

    api_key = os.environ.get('GOOGLE_API_KEY')
    if not api_key and not args.dry_run:
        print("Error: GOOGLE_API_KEY environment variable required")
        return 1

    if not args.db.exists():
        print(f"Error: Database not found at {args.db}")
        return 1

    # Configure Gemini
    if not args.dry_run:
        client = genai.Client(api_key=api_key)
    else:
        client = None

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Find media without workflow enrichment
    if args.force:
        query = """
            SELECT m.id, m.tweet_id, m.media_type, m.local_path
            FROM media m
            JOIN tweets t ON m.tweet_id = t.id
            WHERE m.local_path IS NOT NULL
            ORDER BY t.likes DESC
        """
    else:
        query = """
            SELECT m.id, m.tweet_id, m.media_type, m.local_path
            FROM media m
            JOIN tweets t ON m.tweet_id = t.id
            WHERE m.local_path IS NOT NULL AND m.workflow_summary IS NULL
            ORDER BY t.likes DESC
        """
    if args.limit:
        query += f" LIMIT {args.limit}"

    cursor.execute(query)
    media_items = cursor.fetchall()

    print(f"Found {len(media_items)} media items to enrich")

    if args.dry_run:
        for item in media_items:
            print(f"  Would process: {item['media_type']} - {item['local_path']}")
        return 0

    processed = 0
    failed = 0

    for item in media_items:
        media_path = Path(item['local_path'])
        is_video = item['media_type'] == 'video'

        print(f"Processing {item['id']}: {item['media_type']} - {media_path.name}...")

        if not media_path.exists():
            print(f"  File not found: {media_path}")
            failed += 1
            continue

        result = analyze_media(client, media_path, is_video)

        if result:
            workflow_summary = result.get('workflow_summary') or result.get('summary', '')
            commands_shown = result.get('commands_shown', [])
            key_action = result.get('key_action', '')

            cursor.execute("""
                UPDATE media SET
                    workflow_summary = ?,
                    commands_shown = ?,
                    key_action = ?
                WHERE id = ?
            """, (
                workflow_summary,
                json.dumps(commands_shown) if commands_shown else None,
                key_action,
                item['id']
            ))
            conn.commit()
            print(f"  -> {key_action[:60]}..." if len(key_action) > 60 else f"  -> {key_action}")
            processed += 1
        else:
            failed += 1

        # Rate limiting
        time.sleep(0.5)

    conn.close()

    print(f"\nComplete: {processed} enriched, {failed} failed")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    exit(main())
