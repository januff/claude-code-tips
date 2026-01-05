"""
Utility functions for Obsidian export.
"""

import re
import unicodedata
from datetime import datetime
from typing import Optional


def slugify(text: str, max_length: int = 50) -> str:
    """
    Convert text to a URL/filename-safe slug.

    - Remove non-ASCII characters
    - Replace spaces with hyphens
    - Strip special characters
    - Lowercase
    - Max 50 characters
    """
    if not text:
        return ""

    # Normalize unicode and convert to ASCII
    text = unicodedata.normalize('NFKD', text)
    text = text.encode('ascii', 'ignore').decode('ascii')

    # Lowercase
    text = text.lower()

    # Replace spaces and underscores with hyphens
    text = re.sub(r'[\s_]+', '-', text)

    # Remove everything except alphanumeric and hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)

    # Collapse multiple hyphens
    text = re.sub(r'-+', '-', text)

    # Strip leading/trailing hyphens
    text = text.strip('-')

    # Truncate to max length (at word boundary if possible)
    if len(text) > max_length:
        text = text[:max_length]
        # Try to break at last hyphen
        last_hyphen = text.rfind('-')
        if last_hyphen > max_length // 2:
            text = text[:last_hyphen]

    return text


def date_from_tweet_id(tweet_id: str) -> Optional[str]:
    """
    Extract date from Twitter snowflake ID.
    Twitter IDs encode timestamp as: (id >> 22) + 1288834974657 = ms since epoch
    """
    try:
        id_int = int(tweet_id)
        timestamp_ms = (id_int >> 22) + 1288834974657
        dt = datetime.fromtimestamp(timestamp_ms / 1000)
        return dt.strftime("%Y-%m-%d")
    except (ValueError, OSError):
        return None


def format_date(date_str: Optional[str], fallback: str = "unknown") -> str:
    """
    Parse various date formats and return YYYY-MM-DD.

    Handles:
    - ISO format: 2024-01-15T12:00:00Z
    - SQLite datetime: 2024-01-15 12:00:00
    - Date only: 2024-01-15
    """
    if not date_str:
        return fallback

    formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ",  # ISO with microseconds
        "%Y-%m-%dT%H:%M:%SZ",     # ISO
        "%Y-%m-%dT%H:%M:%S",      # ISO without Z
        "%Y-%m-%d %H:%M:%S",      # SQLite datetime
        "%Y-%m-%d",               # Date only
    ]

    for fmt in formats:
        try:
            dt = datetime.strptime(date_str.strip(), fmt)
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            continue

    # If all parsing fails, try to extract YYYY-MM-DD pattern
    match = re.search(r'(\d{4}-\d{2}-\d{2})', date_str)
    if match:
        return match.group(1)

    return fallback


def format_datetime_display(date_str: Optional[str]) -> str:
    """Format date for display in notes (e.g., 'Jan 15, 2024')."""
    if not date_str:
        return "Unknown date"

    date_only = format_date(date_str)
    if date_only == "unknown":
        return "Unknown date"

    try:
        dt = datetime.strptime(date_only, "%Y-%m-%d")
        return dt.strftime("%b %d, %Y")
    except ValueError:
        return date_only


def format_number(n: Optional[int]) -> str:
    """Format number with comma separators for display."""
    if n is None:
        return "0"
    return f"{n:,}"


def generate_filename(
    date_str: str,
    text: str,
    id_fallback: str,
    primary_keyword: Optional[str] = None
) -> str:
    """
    Generate note filename: {date}-{slug}.md

    Uses primary_keyword if available, otherwise falls back to text slug.
    Falls back to {date}-{id}.md if slug is invalid.
    If date_str is missing, extracts date from tweet ID (snowflake format).
    """
    date = format_date(date_str, fallback=None)
    # Fallback to extracting date from tweet ID
    if not date:
        date = date_from_tweet_id(id_fallback) or "unknown"

    # Prefer primary_keyword from LLM enrichment
    if primary_keyword:
        slug = slugify(primary_keyword)
        if slug and len(slug) >= 3:
            return f"{date}-{slug}.md"

    # Fall back to text-based slug
    slug = slugify(text)
    if slug and len(slug) >= 3:
        return f"{date}-{slug}.md"

    return f"{date}-{id_fallback}.md"


def escape_yaml(value: str) -> str:
    """Escape string for YAML frontmatter."""
    if not value:
        return '""'

    # If contains special chars, quote it
    if any(c in value for c in [':', '#', '[', ']', '{', '}', ',', '&', '*', '!', '|', '>', "'", '"', '%', '@', '`']):
        # Escape quotes and wrap in quotes
        value = value.replace('"', '\\"')
        return f'"{value}"'

    return value


def sanitize_text(text: str) -> str:
    """Sanitize text for markdown body (not YAML)."""
    if not text:
        return ""

    # Replace null bytes
    text = text.replace('\x00', '')

    # Normalize line endings
    text = text.replace('\r\n', '\n').replace('\r', '\n')

    return text


def extract_hashtags(text: str) -> list[str]:
    """Extract hashtags from text."""
    if not text:
        return []

    hashtags = re.findall(r'#(\w+)', text)
    return [h.lower() for h in hashtags]


def extract_mentions(text: str) -> list[str]:
    """Extract @mentions from text."""
    if not text:
        return []

    mentions = re.findall(r'@(\w+)', text)
    return mentions
