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
    primary_keyword: Optional[str] = None,
    handle: Optional[str] = None
) -> str:
    """
    Generate note filename: {date}-{slug}.md

    Priority:
    1. primary_keyword from LLM enrichment
    2. Auto-extracted keyword from text (hashtags, Claude terms, etc.)
    3. Falls back to {date}-{id}.md if all else fails

    If date_str is missing, extracts date from tweet ID (snowflake format).
    """
    date = format_date(date_str, fallback=None)
    # Fallback to extracting date from tweet ID
    if not date:
        date = date_from_tweet_id(id_fallback) or "unknown"

    # 1. Prefer primary_keyword from LLM enrichment
    if primary_keyword:
        slug = slugify(primary_keyword)
        if slug and len(slug) >= 3:
            return f"{date}-{slug}.md"

    # 2. Try auto-extracted fallback keyword
    fallback_kw = generate_fallback_keyword(text, handle)
    if fallback_kw:
        slug = slugify(fallback_kw, max_length=40)
        if slug and len(slug) >= 3:
            return f"{date}-{slug}.md"

    # 3. Last resort: use ID
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


# Common Claude Code terms for keyword extraction
CLAUDE_CODE_TERMS = [
    'claude code', 'claude-code', 'claudecode',
    'claude.md', 'claudemd', 'claude md',
    'mcp', 'mcp server', 'mcp servers',
    'subagent', 'subagents', 'sub-agent', 'sub-agents',
    'hooks', 'hook', 'pretooluse', 'posttooluse',
    'slash command', 'slash commands', '/compact', '/clear', '/help',
    'agent sdk', 'agent-sdk',
    'skills', 'skill',
    'obsidian', 'cursor', 'vscode', 'vs code',
    'opus', 'sonnet', 'haiku',
    'ultrathink', 'think hard', 'think harder',
    'sandbox', 'sandboxing',
    'context window', 'context management',
    'plan mode', 'planning',
    'handoff', 'hand-off',
]

# Stopwords to filter from extracted keywords
STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
    'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your',
    'his', 'her', 'its', 'our', 'their', 'what', 'which', 'who', 'whom',
    'when', 'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few',
    'more', 'most', 'other', 'some', 'such', 'no', 'not', 'only', 'same',
    'so', 'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there',
    'im', 'ive', 'youre', 'youve', 'hes', 'shes', 'its', 'were', 'theyre',
    'dont', 'doesnt', 'didnt', 'wont', 'wouldnt', 'cant', 'couldnt',
    'using', 'use', 'used', 'get', 'got', 'getting', 'make', 'made',
    'making', 'like', 'really', 'actually', 'basically', 'literally',
}

# Generic subjects that shouldn't be included in filename
GENERIC_SUBJECTS = {
    'person', 'man', 'woman', 'people', 'group', 'crowd',
    'news anchor', 'reporter', 'host', 'presenter', 'announcer',
    'character', 'figure', 'individual', 'someone',
    'actor', 'actress', 'model', 'unknown',
    'monroe',  # Generic reporter name, not Marilyn
}

# Known celebrities/figures - use last name or moniker
CELEBRITY_SHORT_NAMES = {
    'bob barker': 'barker',
    'gene wilder': 'wilder',
    'don knotts': 'knotts',
    'andy griffith': 'griffith',
    'ronald reagan': 'reagan',
    'george h.w. bush': 'bush-sr',
    'george hw bush': 'bush-sr',
    'george h. w. bush': 'bush-sr',
    'george bush': 'bush',
    'wilford brimley': 'brimley',
    'maury povich': 'povich',
    'rod serling': 'serling',
    'audrey hepburn': 'hepburn',
    'marilyn monroe': 'marilyn',
    'john lennon': 'lennon',
    'alfred hitchcock': 'hitchcock',
    'richard pryor': 'pryor',
    'philip seymour hoffman': 'hoffman',
    'ted kaczynski': 'kaczynski',
    'joe biden': 'biden',
    'jfk': 'jfk',
    'john f. kennedy': 'jfk',
    'james brown': 'brown',
}


def get_subject_slug(primary_subject: Optional[str]) -> Optional[str]:
    """
    Get a short slug for the subject, or None if generic.
    """
    if not primary_subject:
        return None

    subject_lower = primary_subject.lower().strip()

    # Skip None/null values that leaked through as strings
    if subject_lower in ('none', 'null', 'n/a', 'unknown', ''):
        return None

    # Check if it's a generic subject
    if subject_lower in GENERIC_SUBJECTS:
        return None

    # Check for known celebrity short names
    for full_name, short_name in CELEBRITY_SHORT_NAMES.items():
        if full_name in subject_lower or subject_lower in full_name:
            return short_name

    # For unknown subjects, use last word (usually last name)
    # But skip if it looks generic
    words = subject_lower.split()
    if words:
        last_word = slugify(words[-1], max_length=15)
        if last_word and last_word not in GENERIC_SUBJECTS and len(last_word) >= 3:
            return last_word

    return None


def find_distinctive_element(
    searchable_elements: Optional[list[str]],
    thematic_tags: Optional[list[str]],
    action_summary: Optional[str],
    prompt: Optional[str],
) -> Optional[str]:
    """
    Find the most distinctive/memorable element for the filename.
    """
    # Skip terms
    skip_terms = {'sora', 'ai video', 'ai generated', 'viral', 'deepfake', 'parody'}

    # Highly memorable words to prioritize
    memorable_keywords = {
        'tank', 'abrams', 'whale', 'orca', 'tricycle', 'bike', 'submarine',
        'chase', 'crash', 'explosion', 'dance', 'dancing', 'ski', 'skiing',
        'shit', 'pants', 'fail', 'fight', 'riot', 'bust', 'arrest',
        'mega-ramp', 'ramp', 'jump', 'flip', 'drifting', 'surfing',
        'snowman', 'unicycle', 'hoverboard', 'broomstick',
        'father', 'not-the-father', 'you-are-not',
        'imagination', 'pure-imagination',
        'collaborate', 'listen',
        'saxophone', 'flute', 'guitar', 'bass',
        'lion', 'tiger', 'bear', 'cat', 'otter',
        'mona-lisa', 'scream', 'pearl-earring',
    }

    # 1. Check searchable_elements for memorable phrases
    if searchable_elements:
        best_score = 0
        best_element = None

        for elem in searchable_elements:
            elem_lower = elem.lower().strip()

            # Skip generic terms
            if any(skip in elem_lower for skip in skip_terms):
                continue

            slug = slugify(elem, max_length=30)
            if not slug or len(slug) < 3:
                continue

            # Score by memorable keywords
            score = sum(1 for kw in memorable_keywords if kw in elem_lower)

            # Bonus for multi-word phrases (more specific)
            word_count = len(elem_lower.split())
            if 2 <= word_count <= 4:
                score += 1

            # Bonus for action words
            action_words = {'chase', 'crash', 'dance', 'fight', 'jump', 'escape', 'bust'}
            if any(aw in elem_lower for aw in action_words):
                score += 2

            if score > best_score:
                best_score = score
                best_element = slug

        if best_element:
            return best_element

        # Fallback: first non-generic element
        for elem in searchable_elements:
            elem_lower = elem.lower().strip()
            if any(skip in elem_lower for skip in skip_terms):
                continue
            slug = slugify(elem, max_length=25)
            if slug and len(slug) >= 5:
                return slug

    # 2. Try thematic_tags
    if thematic_tags:
        for tag in thematic_tags:
            tag_lower = tag.lower()
            if tag_lower not in skip_terms and tag_lower not in ('humor', 'comedy', 'parody'):
                slug = slugify(tag, max_length=20)
                if slug and len(slug) >= 4:
                    return slug

    # 3. Try action_summary
    if action_summary:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', action_summary)
        significant = [w.lower() for w in words if w.lower() not in STOPWORDS][:3]
        if len(significant) >= 2:
            return '-'.join(significant[:2])

    # 4. Try prompt
    if prompt:
        words = re.findall(r'\b[a-zA-Z]{4,}\b', prompt)
        significant = [w.lower() for w in words if w.lower() not in STOPWORDS][:2]
        if significant:
            return '-'.join(significant)

    return None


def generate_video_filename(
    date_str: str,
    video_id: str,
    primary_subject: Optional[str] = None,
    action_summary: Optional[str] = None,
    thematic_tags: Optional[list[str]] = None,
    characters: Optional[list] = None,
    prompt: Optional[str] = None,
    searchable_elements: Optional[list[str]] = None,
) -> str:
    """
    Generate semantic filename: subject + distinctive element

    - Recognizable subjects get short name prefix (barker, reagan, povich)
    - Generic subjects are skipped
    - Always include a distinctive element for context
    """
    date = format_date(date_str, fallback="unknown")

    # Get subject slug (None if generic)
    subject_slug = get_subject_slug(primary_subject)

    # Find distinctive element
    distinctive = find_distinctive_element(searchable_elements, thematic_tags, action_summary, prompt)

    # Combine subject + distinctive
    if subject_slug and distinctive:
        # Avoid redundancy - don't repeat subject in distinctive
        if subject_slug not in distinctive:
            return f"{date}-{subject_slug}-{distinctive}.md"
        else:
            return f"{date}-{distinctive}.md"
    elif distinctive:
        return f"{date}-{distinctive}.md"
    elif subject_slug:
        # Subject alone as last resort (shouldn't happen often)
        return f"{date}-{subject_slug}.md"
    else:
        return f"{date}-{video_id}.md"


def generate_fallback_keyword(text: str, handle: Optional[str] = None) -> str:
    """
    Generate a short keyword from tweet text when primary_keyword is missing.

    Priority:
    1. First hashtag (without #)
    2. Common Claude Code terms found in text
    3. First quoted phrase
    4. Handle + first 2-3 significant words
    """
    if not text:
        return ""

    text_lower = text.lower()

    # 1. Check for hashtags — use first hashtag
    hashtags = re.findall(r'#(\w+)', text)
    if hashtags:
        return hashtags[0].lower()

    # 2. Check for common Claude Code terms (prefer multi-word matches first)
    found_terms = []
    for term in sorted(CLAUDE_CODE_TERMS, key=len, reverse=True):
        if term in text_lower:
            # Normalize the term for filename
            normalized = term.replace('.', '').replace('/', '').replace(' ', '-')
            found_terms.append(normalized)
            if len(found_terms) >= 2:
                break

    if found_terms:
        # Dedupe similar terms and combine up to 2
        unique_terms = []
        for term in found_terms:
            # Skip if this term is a substring of an existing term or vice versa
            if not any(term in t or t in term for t in unique_terms):
                unique_terms.append(term)
        keyword = '-'.join(unique_terms[:2])

        # For very common terms, prefix with handle to avoid collisions
        common_terms = {'claude-code', 'obsidian', 'skills', 'skill', 'hooks', 'mcp', 'opus', 'sonnet'}
        if keyword in common_terms and handle:
            clean_handle = handle.lstrip('@').lower()
            if clean_handle and clean_handle not in ('unknown', 'undefined'):
                return f"{clean_handle}-{keyword}"
        return keyword

    # 3. Check for quoted phrases
    quoted = re.findall(r'["\']([^"\']{3,30})["\']', text)
    if quoted:
        # Use first short quoted phrase
        phrase = quoted[0].strip()
        if len(phrase) <= 25:
            return slugify(phrase, max_length=25)

    # 4. Fall back to handle + significant words
    # Clean handle
    clean_handle = ""
    if handle:
        clean_handle = handle.lstrip('@').lower()
        # Skip generic handles
        if clean_handle in ('unknown', 'undefined', ''):
            clean_handle = ""

    # Extract significant words from text
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text)
    significant = [w.lower() for w in words if w.lower() not in STOPWORDS][:4]

    if clean_handle and significant:
        # Handle + first 2 words
        return f"{clean_handle}-{'-'.join(significant[:2])}"
    elif significant:
        # Just first 3 significant words
        return '-'.join(significant[:3])
    elif clean_handle:
        return clean_handle

    return ""
