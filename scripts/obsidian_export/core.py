"""
Core export logic for Obsidian vaults.
"""

import sqlite3
import shutil
from pathlib import Path
from typing import Optional
from abc import ABC, abstractmethod

from jinja2 import Environment, FileSystemLoader, select_autoescape

from .models import Tweet, Video, Media, Reply, Link, Resource, Compilation, parse_json_field
from .utils import (
    generate_filename, generate_video_filename, format_date, format_datetime_display,
    format_number, slugify, sanitize_text
)


TEMPLATES_DIR = Path(__file__).parent / "templates"


class VaultExporter(ABC):
    """Base class for vault exporters."""

    def __init__(self, db_path: Path, output_dir: Path, limit: Optional[int] = None):
        self.db_path = db_path
        self.output_dir = output_dir
        self.limit = limit

        # Stats
        self.exported = 0
        self.skipped = 0
        self.errors = []

        # Setup Jinja2
        self.env = Environment(
            loader=FileSystemLoader(TEMPLATES_DIR),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Add custom filters
        self.env.filters['basename'] = lambda p: Path(p).name if p else ''
        self.env.filters['tojson'] = lambda v: self._to_json(v)
        self.env.filters['format_number'] = format_number

    def _to_json(self, value) -> str:
        """Convert value to JSON-safe string for YAML."""
        import json
        if value is None:
            return 'null'
        if isinstance(value, bool):
            return 'true' if value else 'false'
        if isinstance(value, (int, float)):
            return str(value)
        if isinstance(value, str):
            # Escape for YAML
            if any(c in value for c in ['"', "'", '\n', ':', '#']):
                escaped = value.replace('\\', '\\\\').replace('"', '\\"')
                return f'"{escaped}"'
            return f'"{value}"'
        return json.dumps(value, ensure_ascii=False)

    def setup_vault(self):
        """Create vault directory structure."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        (self.output_dir / "_dashboards").mkdir(exist_ok=True)
        (self.output_dir / "attachments").mkdir(exist_ok=True)
        (self.output_dir / "attachments" / "thumbnails").mkdir(exist_ok=True)
        (self.output_dir / "attachments" / "screenshots").mkdir(exist_ok=True)
        (self.output_dir / "attachments" / "videos").mkdir(exist_ok=True)

    def export_dashboards(self):
        """Export dashboard templates."""
        dashboards = [
            ("dashboard_engagement.md.j2", "top-by-engagement.md"),
            ("dashboard_creator.md.j2", "by-creator.md"),
            ("dashboard_recent.md.j2", "recent-additions.md"),
            ("dashboard_tags.md.j2", "tag-index.md"),
        ]

        for template_name, output_name in dashboards:
            try:
                template = self.env.get_template(template_name)
                content = template.render()
                output_path = self.output_dir / "_dashboards" / output_name
                output_path.write_text(content)
            except Exception as e:
                self.errors.append(f"Dashboard {output_name}: {e}")

    def write_note(self, filename: str, content: str, subdir: Optional[str] = None):
        """Write a note to the vault."""
        if subdir:
            output_path = self.output_dir / subdir / filename
            output_path.parent.mkdir(exist_ok=True)
        else:
            output_path = self.output_dir / filename

        output_path.write_text(content)

    def print_summary(self):
        """Print export summary."""
        print(f"\nExport complete:")
        print(f"  - {self.exported} notes exported")
        print(f"  - {self.skipped} skipped")
        if self.errors:
            print(f"  - {len(self.errors)} errors")
            for err in self.errors[:5]:
                print(f"    - {err}")

    @abstractmethod
    def export(self):
        """Run the export."""
        pass


class TipsExporter(VaultExporter):
    """Exporter for Claude Code Tips vault."""

    def __init__(self, db_path: Path, output_dir: Path, limit: Optional[int] = None,
                 quality_filter: bool = True):
        super().__init__(db_path, output_dir, limit)
        self.quality_filter = quality_filter
        (self.output_dir / "_resources").mkdir(parents=True, exist_ok=True)

    def setup_vault(self):
        super().setup_vault()
        (self.output_dir / "_resources").mkdir(exist_ok=True)

    def load_tweets(self) -> list[Tweet]:
        """Load tweets from database with all related data."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # Pre-load all links into a lookup dict by short_url
        cursor.execute("""
            SELECT short_url, expanded_url, content_type, title, description, llm_summary
            FROM links WHERE expanded_url IS NOT NULL
        """)
        links_by_short_url = {}
        for l_row in cursor.fetchall():
            links_by_short_url[l_row['short_url']] = Link(
                short_url=l_row['short_url'],
                expanded_url=l_row['expanded_url'],
                content_type=l_row['content_type'],
                title=l_row['title'],
                description=l_row['description'],
                llm_summary=l_row['llm_summary'],
            )

        # Main query with tips join
        query = """
            SELECT
                t.*,
                ti.category,
                ti.summary,
                ti.quality_rating,
                ti.is_curated,
                ti.tools_mentioned,
                ti.commands_mentioned,
                ti.code_snippets,
                ti.primary_keyword,
                ti.keywords_json,
                ti.llm_category,
                ti.llm_tools,
                ti.holistic_summary,
                ti.one_liner
            FROM tweets t
            LEFT JOIN tips ti ON t.id = ti.tweet_id
        """
        # Quality filter: only export tweets with engagement OR enrichment
        # Exclude @unknown handles (duplicate thread replies already in parent notes)
        if self.quality_filter:
            query += """ WHERE (t.likes > 0 OR ti.holistic_summary IS NOT NULL)
                AND t.handle != '@unknown'"""
        query += " ORDER BY t.likes DESC"
        if self.limit:
            query += f" LIMIT {self.limit}"

        cursor.execute(query)
        rows = cursor.fetchall()

        tweets = []
        for row in rows:
            tweet = Tweet(
                id=row['id'],
                handle=row['handle'],
                display_name=row['display_name'],
                text=row['text'] or '',
                url=row['url'],
                posted_at=row['posted_at'],
                replies=row['replies'] or 0,
                reposts=row['reposts'] or 0,
                likes=row['likes'] or 0,
                bookmarks=row['bookmarks'] or 0,
                views=row['views'] or 0,
                quotes=row['quotes'] or 0,
                engagement_score=row['engagement_score'] or 0,
                conversation_id=row['conversation_id'],
                is_reply=bool(row['is_reply']),
                in_reply_to_id=row['in_reply_to_id'],
                in_reply_to_user=row['in_reply_to_user'],
                reply_depth=row['reply_depth'] or 0,
                card_url=row['card_url'],
                card_title=row['card_title'],
                card_description=row['card_description'],
                category=row['category'],
                summary=row['summary'],
                quality_rating=row['quality_rating'],
                is_curated=bool(row['is_curated']),
                tools_mentioned=parse_json_field(row['tools_mentioned']),
                commands_mentioned=parse_json_field(row['commands_mentioned']),
                code_snippets=parse_json_field(row['code_snippets']),
                primary_keyword=row['primary_keyword'],
                keywords=parse_json_field(row['keywords_json']),
                llm_category=row['llm_category'],
                llm_tools=parse_json_field(row['llm_tools']),
                holistic_summary=row['holistic_summary'],
                one_liner=row['one_liner'],
            )

            # Load media
            cursor.execute("""
                SELECT id, tweet_id, media_type, url, expanded_url, alt_text,
                       video_url, local_path, ocr_text, vision_description,
                       is_settings_screenshot, is_code_screenshot, extracted_commands,
                       workflow_summary, commands_shown, key_action,
                       focus_text, full_ocr, ui_context
                FROM media WHERE tweet_id = ?
            """, (tweet.id,))
            for m_row in cursor.fetchall():
                tweet.media.append(Media(
                    id=m_row['id'],
                    tweet_id=m_row['tweet_id'],
                    media_type=m_row['media_type'],
                    url=m_row['url'],
                    expanded_url=m_row['expanded_url'],
                    alt_text=m_row['alt_text'],
                    video_url=m_row['video_url'],
                    local_path=m_row['local_path'],
                    ocr_text=m_row['ocr_text'],
                    vision_description=m_row['vision_description'],
                    is_settings_screenshot=bool(m_row['is_settings_screenshot']),
                    is_code_screenshot=bool(m_row['is_code_screenshot']),
                    extracted_commands=m_row['extracted_commands'],
                    workflow_summary=m_row['workflow_summary'],
                    commands_shown=parse_json_field(m_row['commands_shown']),
                    key_action=m_row['key_action'],
                    focus_text=m_row['focus_text'],
                    full_ocr=m_row['full_ocr'],
                    ui_context=m_row['ui_context'],
                ))

            # Load replies
            cursor.execute(
                "SELECT * FROM thread_replies WHERE parent_tweet_id = ? ORDER BY reply_likes DESC",
                (tweet.id,)
            )
            for r_row in cursor.fetchall():
                # Match extracted URLs to links
                reply_links = []
                extracted_urls = r_row['extracted_urls']
                if extracted_urls:
                    try:
                        import json
                        urls = json.loads(extracted_urls)
                        for url in urls:
                            if url in links_by_short_url:
                                reply_links.append(links_by_short_url[url])
                    except (json.JSONDecodeError, TypeError):
                        pass

                tweet.replies_list.append(Reply(
                    id=r_row['id'],
                    parent_tweet_id=r_row['parent_tweet_id'],
                    reply_tweet_id=r_row['reply_tweet_id'],
                    reply_text=r_row['reply_text'] or '',
                    reply_author_handle=r_row['reply_author_handle'],
                    reply_author_name=r_row['reply_author_name'],
                    reply_posted_at=r_row['reply_posted_at'],
                    reply_likes=r_row['reply_likes'] or 0,
                    reply_depth=r_row['reply_depth'] or 1,
                    is_author_reply=bool(r_row['is_author_reply']),
                    is_thread_continuation=bool(r_row['is_thread_continuation']),
                    is_author_response=bool(r_row['is_author_response']),
                    response_to_reply_id=r_row['response_to_reply_id'],
                    is_educational=bool(r_row['is_educational']),
                    quality_score=r_row['quality_score'],
                    has_media=bool(r_row['has_media']),
                    media_urls=r_row['media_urls'],
                    links=reply_links,
                ))

            tweets.append(tweet)

        conn.close()
        return tweets

    def export_tweet(self, tweet: Tweet) -> bool:
        """Export a single tweet to a note."""
        try:
            template = self.env.get_template("tweet.md.j2")

            filename = generate_filename(
                tweet.posted_at,
                tweet.text[:100],
                tweet.id,
                primary_keyword=tweet.primary_keyword,
                handle=tweet.handle
            )

            content = template.render(
                tweet=tweet,
                date=format_date(tweet.posted_at),
                date_display=format_datetime_display(tweet.posted_at),
                display_name=tweet.display_name or tweet.handle,
                likes_fmt=format_number(tweet.likes),
                tags=tweet.get_tags(),
            )

            self.write_note(filename, content)
            return True

        except Exception as e:
            self.errors.append(f"Tweet {tweet.id}: {e}")
            return False

    def export(self):
        """Run the full export."""
        print(f"Tips Vault Export")
        print(f"=" * 40)
        print(f"Database: {self.db_path}")
        print(f"Output: {self.output_dir}")
        print(f"Quality filter: {'ON (likes > 0 OR has summary)' if self.quality_filter else 'OFF (all tweets)'}")
        if self.limit:
            print(f"Limit: {self.limit}")

        self.setup_vault()

        tweets = self.load_tweets()
        print(f"\nLoaded {len(tweets)} tweets")

        print("Exporting tweets...")
        for tweet in tweets:
            if self.export_tweet(tweet):
                self.exported += 1
            else:
                self.skipped += 1

        print("Exporting dashboards...")
        self.export_dashboards()

        self.print_summary()


class HoFExporter(VaultExporter):
    """Exporter for Hall of Fake vault."""

    def __init__(self, db_path: Path, output_dir: Path,
                 videos_dir: Optional[Path] = None,
                 thumbnails_dir: Optional[Path] = None,
                 limit: Optional[int] = None):
        super().__init__(db_path, output_dir, limit)
        self.videos_dir = videos_dir
        self.thumbnails_dir = thumbnails_dir

    def setup_vault(self):
        super().setup_vault()
        (self.output_dir / "_compilations").mkdir(exist_ok=True)

    def load_videos(self) -> list[Video]:
        """Load videos from database with all related data."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        query = """
            SELECT
                v.*,
                va.primary_subject,
                va.role_or_character,
                va.subject_category,
                va.format_reference,
                va.ip_reference,
                va.action_summary,
                va.setting,
                va.era_aesthetic,
                va.characters,
                va.notable_objects,
                va.searchable_elements,
                va.style_tags,
                va.thematic_tags,
                tr.text as transcription
            FROM videos v
            LEFT JOIN visual_analysis va ON v.video_id = va.video_id
            LEFT JOIN transcriptions tr ON v.video_id = tr.video_id
            ORDER BY v.likes DESC
        """
        if self.limit:
            query += f" LIMIT {self.limit}"

        cursor.execute(query)
        rows = cursor.fetchall()

        videos = []
        for row in rows:
            video = Video(
                video_id=row['video_id'],
                creator=row['creator'],
                prompt=row['prompt'],
                caption=row['caption'],
                discovery_phrase=row['discovery_phrase'],
                likes=row['likes'] or 0,
                views=row['views'] or 0,
                remixes=row['remixes'] or 0,
                comments_count=row['comments_count'] or 0,
                duration=row['duration'],
                width=row['width'],
                height=row['height'],
                orientation=row['orientation'],
                posted_at=row['posted_at'],
                fetched_at=row['fetched_at'],
                has_speech=bool(row['has_speech']),
                is_remix=bool(row['is_remix']),
                parent_post_id=row['parent_post_id'],
                root_post_id=row['root_post_id'],
                local_filename=row['local_filename'],
                thumbnail_path=row['thumbnail_path'],
                transcription=row['transcription'],
                primary_subject=row['primary_subject'],
                role_or_character=row['role_or_character'],
                subject_category=row['subject_category'],
                format_reference=row['format_reference'],
                ip_reference=row['ip_reference'],
                action_summary=row['action_summary'],
                setting=row['setting'],
                era_aesthetic=row['era_aesthetic'],
                characters=parse_json_field(row['characters']),
                notable_objects=parse_json_field(row['notable_objects']),
                searchable_elements=parse_json_field(row['searchable_elements']),
                style_tags=parse_json_field(row['style_tags']),
                thematic_tags=parse_json_field(row['thematic_tags']),
            )

            # Load compilation appearances
            cursor.execute(
                "SELECT * FROM used_in WHERE video_id = ?",
                (video.video_id,)
            )
            for u_row in cursor.fetchall():
                video.featured_in.append({
                    'compilation_id': u_row['compilation_id'],
                    'headline': u_row['headline'],
                    'timestamp': u_row['timestamp'],
                    'url': u_row['url'],
                    'platform': u_row['platform'],
                })

            videos.append(video)

        # Load remix relationships
        video_map = {v.video_id: v for v in videos}
        for video in videos:
            if video.is_remix and video.parent_post_id:
                parent = video_map.get(video.parent_post_id)
                if parent:
                    parent.remix_children.append(video.video_id)

        conn.close()
        return videos

    def copy_media(self, video: Video):
        """Copy video and thumbnail to vault attachments."""
        if self.thumbnails_dir and video.thumbnail_path:
            src = self.thumbnails_dir / video.thumbnail_path
            dst = self.output_dir / "attachments" / "thumbnails" / video.thumbnail_path
            if src.exists() and not dst.exists():
                shutil.copy2(src, dst)

        # Note: Videos are typically too large to copy; we just reference them

    def export_video(self, video: Video) -> bool:
        """Export a single video to a note."""
        try:
            template = self.env.get_template("video.md.j2")

            filename = generate_video_filename(
                video.posted_at,
                video.video_id,
                primary_subject=video.primary_subject,
                action_summary=video.action_summary,
                thematic_tags=video.thematic_tags,
                characters=video.characters,
                prompt=video.prompt,
            )

            content = template.render(
                video=video,
                date=format_date(video.posted_at),
                date_display=format_datetime_display(video.posted_at),
                likes_fmt=format_number(video.likes),
                views_fmt=format_number(video.views),
                tags=video.get_tags(),
            )

            self.write_note(filename, content)

            # Copy media files
            self.copy_media(video)

            return True

        except Exception as e:
            self.errors.append(f"Video {video.video_id}: {e}")
            return False

    def export_compilations(self, videos: list[Video]):
        """Export compilation notes."""
        # Gather unique compilations
        compilations = {}
        for video in videos:
            for feat in video.featured_in:
                comp_id = feat.get('compilation_id')
                if comp_id:
                    if comp_id not in compilations:
                        compilations[comp_id] = Compilation(
                            compilation_id=comp_id,
                            url=feat.get('url'),
                            headline=feat.get('headline'),
                            platform=feat.get('platform', 'youtube'),
                        )
                    compilations[comp_id].video_appearances.append({
                        'video_id': video.video_id,
                        'timestamp': feat.get('timestamp'),
                    })

        # Export each compilation
        for comp in compilations.values():
            filename = f"{slugify(comp.headline or comp.compilation_id)}.md"
            content = f"""---
compilation_id: "{comp.compilation_id}"
platform: "{comp.platform}"
url: "{comp.url or ''}"
headline: {self._to_json(comp.headline)}
---

# {comp.headline or 'Compilation'}

**URL:** [{comp.url}]({comp.url})

## Featured Videos

| Video | Timestamp |
|-------|-----------|
"""
            for app in comp.video_appearances:
                content += f"| [[{app['video_id']}]] | {app.get('timestamp', '')} |\n"

            self.write_note(filename, content, subdir="_compilations")

    def export(self):
        """Run the full export."""
        print(f"Hall of Fake Vault Export")
        print(f"=" * 40)
        print(f"Database: {self.db_path}")
        print(f"Output: {self.output_dir}")
        if self.limit:
            print(f"Limit: {self.limit}")

        self.setup_vault()

        videos = self.load_videos()
        print(f"\nLoaded {len(videos)} videos")

        print("Exporting videos...")
        for video in videos:
            if self.export_video(video):
                self.exported += 1
            else:
                self.skipped += 1

        print("Exporting compilations...")
        self.export_compilations(videos)

        print("Exporting dashboards...")
        self.export_dashboards()

        self.print_summary()
