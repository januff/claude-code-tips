"""
Data models for Obsidian export.
"""

from dataclasses import dataclass, field
from typing import Optional
import json


@dataclass
class Tweet:
    """Represents a tweet from the tips database."""
    id: str
    handle: str
    display_name: Optional[str]
    text: str
    url: str
    posted_at: Optional[str]

    # Metrics
    replies: int = 0
    reposts: int = 0
    likes: int = 0
    bookmarks: int = 0
    views: int = 0
    quotes: int = 0
    engagement_score: int = 0

    # Threading
    conversation_id: Optional[str] = None
    is_reply: bool = False
    in_reply_to_id: Optional[str] = None
    in_reply_to_user: Optional[str] = None
    reply_depth: int = 0

    # Card/link preview
    card_url: Optional[str] = None
    card_title: Optional[str] = None
    card_description: Optional[str] = None

    # Curation data (from tips table)
    category: Optional[str] = None
    summary: Optional[str] = None
    quality_rating: Optional[int] = None
    is_curated: bool = False
    tools_mentioned: list[str] = field(default_factory=list)
    commands_mentioned: list[str] = field(default_factory=list)
    code_snippets: list[str] = field(default_factory=list)

    # LLM enrichment data
    primary_keyword: Optional[str] = None
    keywords: list[str] = field(default_factory=list)
    llm_category: Optional[str] = None
    llm_tools: list[str] = field(default_factory=list)
    # Enrichment v3 holistic summaries
    holistic_summary: Optional[str] = None
    one_liner: Optional[str] = None

    # Related data
    media: list['Media'] = field(default_factory=list)
    replies_list: list['Reply'] = field(default_factory=list)

    @property
    def has_code(self) -> bool:
        return len(self.code_snippets) > 0 or any(m.is_code_screenshot for m in self.media)

    @property
    def has_screenshot(self) -> bool:
        return any(m.media_type == 'photo' for m in self.media)

    @property
    def has_external_link(self) -> bool:
        return self.card_url is not None

    def get_tags(self) -> list[str]:
        """Generate tags based on content."""
        tags = []

        # Category tag
        if self.category and self.category != 'other':
            tags.append(f"category/{self.category}")

        # Content type tags
        if self.has_code:
            tags.append("type/code-snippet")
        if self.has_screenshot:
            tags.append("type/screenshot")
        if self.is_reply:
            tags.append("type/reply")
        if len(self.replies_list) > 0:
            tags.append("type/thread")

        # Tool tags
        for tool in self.tools_mentioned[:5]:  # Limit to 5
            clean_tool = tool.lower().replace(' ', '-')
            tags.append(f"tool/{clean_tool}")

        return tags


@dataclass
class Media:
    """Represents media attached to a tweet."""
    id: int
    tweet_id: str
    media_type: str
    url: str
    expanded_url: Optional[str] = None
    alt_text: Optional[str] = None
    video_url: Optional[str] = None
    local_path: Optional[str] = None
    ocr_text: Optional[str] = None
    vision_description: Optional[str] = None
    is_settings_screenshot: bool = False
    is_code_screenshot: bool = False
    extracted_commands: Optional[str] = None
    # Enrichment v2 fields
    workflow_summary: Optional[str] = None
    commands_shown: list[str] = field(default_factory=list)
    key_action: Optional[str] = None
    # Enrichment v3 fields
    focus_text: Optional[str] = None
    full_ocr: Optional[str] = None
    ui_context: Optional[str] = None


@dataclass
class Reply:
    """Represents a reply in a thread."""
    id: int
    parent_tweet_id: str
    reply_tweet_id: str
    reply_text: str
    reply_author_handle: Optional[str] = None
    reply_author_name: Optional[str] = None
    reply_posted_at: Optional[str] = None
    reply_likes: int = 0
    reply_depth: int = 1
    is_author_reply: bool = False
    is_thread_continuation: bool = False
    is_author_response: bool = False
    response_to_reply_id: Optional[str] = None
    is_educational: bool = False
    quality_score: Optional[int] = None
    has_media: bool = False
    media_urls: Optional[str] = None

    @property
    def quality_level(self) -> str:
        """Return quality level for callout styling."""
        if self.is_educational or (self.quality_score and self.quality_score > 7):
            return "high"
        elif self.quality_score and self.quality_score >= 4:
            return "medium"
        else:
            return "low"


@dataclass
class Resource:
    """Represents a linked resource (URL)."""
    url: str
    content_type: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    fetched_at: Optional[str] = None
    referenced_by: list[str] = field(default_factory=list)  # List of tweet IDs


@dataclass
class Video:
    """Represents a video from the Hall of Fake database."""
    video_id: str
    creator: str
    prompt: Optional[str] = None
    caption: Optional[str] = None
    discovery_phrase: Optional[str] = None

    # Metrics
    likes: int = 0
    views: int = 0
    remixes: int = 0
    comments_count: int = 0

    # Technical
    duration: Optional[int] = None
    width: Optional[int] = None
    height: Optional[int] = None
    orientation: Optional[str] = None

    # Dates
    posted_at: Optional[str] = None
    fetched_at: Optional[str] = None

    # Content flags
    has_speech: bool = False
    is_remix: bool = False
    parent_post_id: Optional[str] = None
    root_post_id: Optional[str] = None

    # Local files
    local_filename: Optional[str] = None
    thumbnail_path: Optional[str] = None

    # Transcription
    transcription: Optional[str] = None

    # Visual analysis (flattened)
    primary_subject: Optional[str] = None
    role_or_character: Optional[str] = None
    subject_category: Optional[str] = None
    format_reference: Optional[str] = None
    ip_reference: Optional[str] = None
    action_summary: Optional[str] = None
    setting: Optional[str] = None
    era_aesthetic: Optional[str] = None
    characters: list[dict] = field(default_factory=list)
    notable_objects: list[dict] = field(default_factory=list)
    searchable_elements: list[str] = field(default_factory=list)
    style_tags: list[str] = field(default_factory=list)
    thematic_tags: list[str] = field(default_factory=list)

    # Compilation appearances
    featured_in: list[dict] = field(default_factory=list)

    # Child remixes
    remix_children: list[str] = field(default_factory=list)

    @property
    def has_local_video(self) -> bool:
        return self.local_filename is not None

    @property
    def has_thumbnail(self) -> bool:
        return self.thumbnail_path is not None

    def get_tags(self) -> list[str]:
        """Generate tags based on content."""
        tags = []

        # Subject category
        if self.subject_category:
            tags.append(f"subject/{self.subject_category.lower()}")

        # Style tags
        for style in self.style_tags[:5]:
            clean = style.lower().replace(' ', '-')
            tags.append(f"style/{clean}")

        # Thematic tags
        for theme in self.thematic_tags[:3]:
            clean = theme.lower().replace(' ', '-')
            tags.append(f"theme/{clean}")

        # Format reference
        if self.format_reference:
            clean = self.format_reference.lower().replace(' ', '-')
            tags.append(f"format/{clean}")

        # Special flags
        if self.is_remix:
            tags.append("type/remix")
        if self.has_speech:
            tags.append("has/speech")
        if len(self.featured_in) > 0:
            tags.append("featured/compilation")

        return tags


@dataclass
class Compilation:
    """Represents a YouTube compilation that features videos."""
    compilation_id: str
    platform: str = "youtube"
    url: Optional[str] = None
    headline: Optional[str] = None
    published_at: Optional[str] = None
    video_appearances: list[dict] = field(default_factory=list)  # [{video_id, timestamp}]


def parse_json_field(value: Optional[str]) -> list:
    """Safely parse a JSON field, returning empty list on failure."""
    if not value:
        return []
    try:
        result = json.loads(value)
        return result if isinstance(result, list) else []
    except (json.JSONDecodeError, TypeError):
        return []
