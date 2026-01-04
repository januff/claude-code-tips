# HANDOFF: ContentUnit Architecture — Unified Enrichment Pipeline

**Created:** 2026-01-04
**Purpose:** Refactor enrichment as a composable pipeline that treats tweets and high-quality replies equally
**Priority:** HIGH — architectural foundation for scaling

---

## Problem Statement

Current architecture treats replies as second-class content:
- Tweets get: media download → vision analysis → OCR → link fetch → keyword extraction → holistic summary
- Replies get: text storage with maybe a quality score

But high-quality replies often contain:
- Screenshots and videos (same as tweets)
- External links to blogs/docs/tools (same as tweets)
- Rich context needing summarization (same as tweets)

**Solution:** Abstract the analysis pipeline into a `ContentUnit` pattern that applies uniformly to any content worth analyzing.

---

## Architecture: ContentUnit Abstraction

### Core Data Model

```python
@dataclass
class ContentUnit:
    """Base class for any content worth analyzing."""
    
    # Identity
    id: str
    source_type: str  # 'tweet' | 'reply' | 'quote'
    
    # Core content
    text: str
    author_handle: str
    author_name: Optional[str]
    posted_at: Optional[str]
    url: Optional[str]
    
    # Media attachments
    media: list[MediaItem] = field(default_factory=list)
    
    # Extracted URLs from text
    extracted_urls: list[str] = field(default_factory=list)
    
    # Enrichment results
    keywords: list[str] = field(default_factory=list)
    primary_keyword: Optional[str] = None
    category: Optional[str] = None
    holistic_summary: Optional[str] = None
    one_liner: Optional[str] = None
    
    # Processing metadata
    enriched_at: Optional[str] = None
    enrichment_cost: float = 0.0


@dataclass
class MediaItem:
    """Media attached to a content unit."""
    id: int
    media_type: str  # 'photo' | 'video' | 'gif'
    url: str
    local_path: Optional[str] = None
    
    # Vision analysis results
    summary: Optional[str] = None
    focus_text: Optional[str] = None
    full_ocr: Optional[str] = None
    workflow_summary: Optional[str] = None
    commands_shown: list[str] = field(default_factory=list)
    key_action: Optional[str] = None
    
    # Processing metadata
    analyzed_at: Optional[str] = None


@dataclass 
class LinkItem:
    """URL extracted from content."""
    url: str
    title: Optional[str] = None
    content_type: Optional[str] = None  # 'blog' | 'github' | 'docs' | 'tool'
    summary: Optional[str] = None
    key_points: list[str] = field(default_factory=list)
    fetched_at: Optional[str] = None


@dataclass
class Tweet(ContentUnit):
    """Tweet with metrics and threading."""
    
    # Metrics
    likes: int = 0
    views: int = 0
    replies_count: int = 0
    reposts: int = 0
    engagement_score: int = 0
    
    # Threading
    conversation_id: Optional[str] = None
    is_reply: bool = False
    
    # Child content
    thread_continuations: list['Reply'] = field(default_factory=list)  # Author self-replies
    replies: list['Reply'] = field(default_factory=list)  # Other replies
    
    # Card preview (if tweet links somewhere)
    card_url: Optional[str] = None
    card_title: Optional[str] = None


@dataclass
class Reply(ContentUnit):
    """Reply to a tweet."""
    
    # Threading
    parent_tweet_id: str
    reply_depth: int = 1
    is_author_reply: bool = False
    
    # Metrics (subset)
    likes: int = 0
    
    # Quality assessment
    quality_score: Optional[int] = None
    is_educational: bool = False
```

---

## Unified Enrichment Pipeline

### Core Pipeline Function

```python
# scripts/enrichment/pipeline.py

import re
from typing import Optional
from datetime import datetime, timezone

from .media import download_media, analyze_media
from .links import fetch_url, summarize_link
from .keywords import extract_keywords
from .summaries import generate_holistic_summary


URL_PATTERN = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')


def extract_urls(text: str) -> list[str]:
    """Extract URLs from text content."""
    return URL_PATTERN.findall(text)


def enrich_content_unit(
    unit: ContentUnit,
    analyze_media: bool = True,
    fetch_links: bool = True,
    extract_kw: bool = True,
    generate_summary: bool = True,
    force: bool = False
) -> ContentUnit:
    """
    Apply full enrichment pipeline to any ContentUnit.
    
    Pipeline stages:
    1. Extract URLs from text
    2. Download media files
    3. Analyze media (vision + OCR)
    4. Fetch and summarize linked URLs
    5. Extract keywords
    6. Generate holistic summary
    
    Each stage is idempotent — skips if already done unless force=True.
    """
    
    # Stage 0: Extract URLs from text
    if not unit.extracted_urls:
        unit.extracted_urls = extract_urls(unit.text)
    
    # Stage 1: Download media
    for media in unit.media:
        if not media.local_path or force:
            download_media(media)
    
    # Stage 2: Analyze media
    if analyze_media:
        for media in unit.media:
            if not media.analyzed_at or force:
                analyze_media_item(media)
    
    # Stage 3: Fetch and summarize links
    if fetch_links:
        for url in unit.extracted_urls:
            link = get_or_create_link(url)
            if not link.fetched_at or force:
                content = fetch_url(url)
                summarize_link(link, content)
    
    # Stage 4: Extract keywords
    if extract_kw:
        if not unit.primary_keyword or force:
            extract_keywords(unit)
    
    # Stage 5: Generate holistic summary
    if generate_summary:
        if not unit.holistic_summary or force:
            generate_holistic_summary(unit)
    
    unit.enriched_at = datetime.now(timezone.utc).isoformat()
    
    return unit


def should_enrich_reply(reply: Reply) -> bool:
    """Determine if a reply warrants full enrichment."""
    
    # Always enrich author self-replies (they're thread continuations)
    if reply.is_author_reply:
        return True
    
    # Enrich high-quality replies
    if reply.quality_score and reply.quality_score >= 7:
        return True
    
    # Enrich replies marked as educational
    if reply.is_educational:
        return True
    
    # Enrich replies with significant engagement
    if reply.likes >= 20:
        return True
    
    # Enrich replies that have media
    if reply.media:
        return True
    
    # Enrich replies with external links
    if extract_urls(reply.text):
        return True
    
    return False
```

### Batch Processing

```python
# scripts/enrichment/batch.py

def enrich_tweet_with_replies(
    tweet: Tweet,
    max_replies: int = 10,
    force: bool = False
) -> Tweet:
    """
    Enrich a tweet and its worthy replies.
    """
    
    # Enrich main tweet
    print(f"Enriching tweet {tweet.id}...")
    enrich_content_unit(tweet, force=force)
    
    # Separate author self-replies (always enrich)
    for reply in tweet.thread_continuations:
        print(f"  Enriching thread continuation from {reply.author_handle}...")
        enrich_content_unit(reply, force=force)
    
    # Enrich worthy replies
    enriched_count = 0
    for reply in tweet.replies:
        if enriched_count >= max_replies:
            break
        
        if should_enrich_reply(reply):
            print(f"  Enriching reply from {reply.author_handle}...")
            enrich_content_unit(reply, force=force)
            enriched_count += 1
    
    return tweet


def enrich_all_tweets(
    limit: Optional[int] = None,
    force: bool = False
):
    """
    Run enrichment pipeline on all tweets.
    """
    tweets = load_tweets(limit=limit)
    
    for i, tweet in enumerate(tweets):
        print(f"\n[{i+1}/{len(tweets)}] Processing {tweet.id}...")
        enrich_tweet_with_replies(tweet, force=force)
        save_tweet(tweet)
        
        # Checkpoint
        if (i + 1) % 10 == 0:
            print(f"  Checkpoint: {i+1} tweets processed")
```

---

## Schema Updates

### New Tables

```sql
-- Unified content units (optional — could also extend existing tables)
CREATE TABLE IF NOT EXISTS content_units (
    id TEXT PRIMARY KEY,
    source_type TEXT NOT NULL,  -- 'tweet' | 'reply'
    source_id TEXT NOT NULL,    -- tweet.id or reply.id
    
    -- Enrichment results
    keywords_json TEXT,
    primary_keyword TEXT,
    category TEXT,
    holistic_summary TEXT,
    one_liner TEXT,
    
    -- Processing metadata
    enriched_at TEXT,
    enrichment_cost REAL DEFAULT 0,
    
    UNIQUE(source_type, source_id)
);

-- Reply media (mirrors media table structure)
CREATE TABLE IF NOT EXISTS reply_media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reply_id INTEGER NOT NULL REFERENCES thread_replies(id),
    media_type TEXT NOT NULL,
    url TEXT NOT NULL,
    local_path TEXT,
    
    -- Vision analysis
    summary TEXT,
    focus_text TEXT,
    full_ocr TEXT,
    workflow_summary TEXT,
    commands_shown TEXT,  -- JSON array
    key_action TEXT,
    
    analyzed_at TEXT
);

-- Reply links (URLs extracted from reply text)
CREATE TABLE IF NOT EXISTS reply_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    reply_id INTEGER NOT NULL REFERENCES thread_replies(id),
    url TEXT NOT NULL,
    title TEXT,
    content_type TEXT,
    summary TEXT,
    key_points_json TEXT,
    fetched_at TEXT
);
```

### Extend thread_replies

```sql
ALTER TABLE thread_replies ADD COLUMN media_json TEXT;  -- Raw media from scrape
ALTER TABLE thread_replies ADD COLUMN extracted_urls TEXT;  -- JSON array
ALTER TABLE thread_replies ADD COLUMN keywords_json TEXT;
ALTER TABLE thread_replies ADD COLUMN primary_keyword TEXT;
ALTER TABLE thread_replies ADD COLUMN holistic_summary TEXT;
ALTER TABLE thread_replies ADD COLUMN enriched_at TEXT;
```

---

## Directory Structure

```
scripts/
├── enrichment/
│   ├── __init__.py
│   ├── models.py          # ContentUnit, MediaItem, LinkItem, Tweet, Reply
│   ├── pipeline.py        # enrich_content_unit(), should_enrich_reply()
│   ├── batch.py           # enrich_tweet_with_replies(), enrich_all_tweets()
│   ├── media.py           # download_media(), analyze_media_item()
│   ├── links.py           # fetch_url(), summarize_link()
│   ├── keywords.py        # extract_keywords()
│   ├── summaries.py       # generate_holistic_summary()
│   └── db.py              # load_tweets(), save_tweet(), etc.
├── enrich_all.py          # CLI entry point
└── obsidian_export/       # Existing export code
```

---

## CLI Interface

```bash
# Enrich everything (tweets + worthy replies)
python scripts/enrich_all.py

# Limit for testing
python scripts/enrich_all.py --limit 10

# Force re-enrichment
python scripts/enrich_all.py --force

# Skip specific stages
python scripts/enrich_all.py --skip-media --skip-links

# Only enrich replies (tweets already done)
python scripts/enrich_all.py --replies-only
```

---

## Export Template Updates

### Tweet with Thread Continuations

```jinja
> [!tweet] {{ tweet.handle }} · {{ date_display }}
> {{ tweet.text | replace('\n', '\n> ') }}
{% for cont in tweet.thread_continuations %}
>
> ---
> *{{ cont.author_handle }} · {{ cont.posted_at | format_date }}:*
> {{ cont.text | replace('\n', '\n> ') }}
{% if cont.media %}
> {% for m in cont.media %}
> ![[attachments/{{ m.local_path | basename }}]]
> {% endfor %}
{% endif %}
{% endfor %}
>
> Likes: {{ tweet.likes | format_number }} · Replies: {{ tweet.replies_count | format_number }}
```

### Enriched Replies

```jinja
## Replies

{% for reply in tweet.replies if not reply.is_author_reply %}
> [!reply] {{ reply.author_handle }}{% if reply.posted_at %} · {{ reply.posted_at | format_date }}{% endif %}
> {{ reply.text | replace('\n', '\n> ') }}
{% if reply.likes > 0 %}
> *{{ reply.likes }} likes*
{% endif %}

{% if reply.media %}
### Media from {{ reply.author_handle }}
{% for m in reply.media %}
![[attachments/{{ m.local_path | basename }}]]
{% if m.workflow_summary %}
**Workflow:** {{ m.workflow_summary }}
{% endif %}
{% endfor %}
{% endif %}

{% if reply.extracted_urls %}
**Links:** {% for url in reply.extracted_urls %}[{{ url | truncate(40) }}]({{ url }}){% if not loop.last %}, {% endif %}{% endfor %}
{% endif %}

{% endfor %}
```

---

## Recursion Limits

| Depth | Content Type | Treatment |
|-------|--------------|-----------|
| 0 | Main tweet | Full enrichment always |
| 1 | Direct reply | Full enrichment if `should_enrich_reply()` |
| 1 | Author self-reply | Full enrichment always (thread continuation) |
| 2 | Reply to reply | Text capture only |
| 3+ | Deep thread | Ignore |

This keeps analysis focused on high-value content without infinite recursion.

---

## Migration Path

### Phase 1: Create Infrastructure
1. Create `scripts/enrichment/` directory and modules
2. Add new schema tables/columns
3. Implement `ContentUnit` models

### Phase 2: Migrate Existing Scripts
1. Refactor `enrich_media.py` → `enrichment/media.py`
2. Refactor `enrich_keywords.py` → `enrichment/keywords.py`
3. Refactor `enrich_links.py` → `enrichment/links.py`
4. Create unified `enrichment/pipeline.py`

### Phase 3: Re-scrape with Full Reply Data
1. Run thread extractor on top tweets
2. Import with full reply media/URLs
3. Run unified enrichment pipeline

### Phase 4: Update Export
1. Update templates to handle enriched replies
2. Include thread continuations in tweet card
3. Show reply media and links

---

## Test Checklist

- [ ] ContentUnit model works for both tweets and replies
- [ ] `should_enrich_reply()` correctly identifies worthy replies
- [ ] Author self-replies always enriched
- [ ] Reply media downloaded and analyzed
- [ ] Reply URLs extracted and summarized
- [ ] Export shows thread continuations in main card
- [ ] Export shows enriched reply content
- [ ] Eric Buess thread renders with full self-reply chain
- [ ] Geoffrey Huntley reply shows ghuntley.com link summary

---

*Handoff created: 2026-01-04*
