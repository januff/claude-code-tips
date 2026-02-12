#!/usr/bin/env python3
"""
Enhance an exported Obsidian vault with:
1. Topic cluster subdirectories (based on llm_category)
2. Bidirectional wiki-links between related tips
3. Adoption status tags from PROGRESS.md

Run AFTER export_tips.py. This is a separate pass that enriches the
already-exported vault without modifying the core export logic.

Usage:
    python scripts/obsidian_export/enhance_vault.py
    python scripts/obsidian_export/enhance_vault.py --vault "Claude Code Tips"
    python scripts/obsidian_export/enhance_vault.py --dry-run
    python scripts/obsidian_export/enhance_vault.py --skip-clusters  # links + tags only
    python scripts/obsidian_export/enhance_vault.py --skip-links     # clusters + tags only
"""

import argparse
import json
import os
import re
import shutil
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Optional


# ── Category → subdirectory mapping ──────────────────────────────────────
# Maps llm_category values to clean subdirectory names.
# Categories with few items get merged into a parent cluster.
CATEGORY_DIRS = {
    "tooling": "tooling",
    "prompting": "prompting",
    "meta": "meta-commentary",
    "context-management": "context-management",
    "skills": "skills-and-commands",
    "commands": "skills-and-commands",
    "automation": "automation",
    "subagents": "subagents",
    "workflow": "workflow",
    "planning": "planning",
    "security": "security",
    "hooks": "hooks",
    "mcp": "mcp",
}

# Minimum notes to justify a subdirectory; smaller categories stay at root
MIN_CLUSTER_SIZE = 3


# ── Adoption status parsing ──────────────────────────────────────────────
# These keywords from PROGRESS.md map to vault tags
ADOPTION_STATUSES = {
    "ADOPTED": "status/adopted",
    "IN_PROGRESS": "status/in-progress",
    "PENDING": "status/pending",
    "SKIPPED": "status/skipped",
    "UNTESTED": "status/untested",
}

# Technique keywords from PROGRESS.md that map to tweet content
# Each entry: (keyword_pattern, adoption_status)
# Built dynamically from PROGRESS.md parsing
TECHNIQUE_PATTERNS: list[tuple[str, str]] = []


def parse_progress_file(progress_path: Path) -> list[tuple[str, str]]:
    """
    Parse PROGRESS.md to extract technique → adoption status mappings.

    Looks for table rows like:
        | The Handoff technique | ADOPTED | ... |
        | Subagents for parallel work | PENDING | ... |

    Returns list of (lowercased_keyword, status_tag) tuples.
    """
    if not progress_path.exists():
        print(f"  Warning: PROGRESS.md not found at {progress_path}")
        return []

    content = progress_path.read_text()
    patterns = []

    # Match table rows with status indicators
    # Pattern: | text | STATUS_EMOJI STATUS | ... |
    row_re = re.compile(
        r'\|\s*(?:\*\*)?(.+?)(?:\*\*)?\s*\|\s*'
        r'(?:[\U0001F300-\U0001F9FF\u2705\U0001F504\U0001F4CB\u23ED\uFE0F\u2753\U0001F525]*\s*)?'
        r'(ADOPTED|IN_PROGRESS|PENDING|SKIPPED|UNTESTED)',
        re.UNICODE
    )

    for match in row_re.finditer(content):
        technique_text = match.group(1).strip()
        status = match.group(2).strip()

        # Clean leading/trailing pipes and whitespace from regex capture
        technique_text = technique_text.strip('|').strip()
        # Clean up markdown bold markers
        technique_text = technique_text.strip('*').strip()

        lower_text = technique_text.lower()

        # Skip table headers and separator rows
        if lower_text in ('tip', 'pattern', 'technique', 'step', 'skill name',
                          'environment', 'status', 'meaning'):
            continue
        # Skip separator rows (----)
        if re.match(r'^[-|:\s]+$', technique_text):
            continue
        # Skip rows that look like status definitions leaking from the legend
        if any(phrase in lower_text for phrase in [
            'part of my regular workflow',
            'currently experimenting',
            'want to try',
            'evaluated, not applicable',
            'high engagement growth',
        ]):
            continue

        # Extract meaningful keywords from technique name
        clean = lower_text
        # Remove common prefixes and articles
        clean = re.sub(r'^(the |a |an )', '', clean)
        # Remove markdown links
        clean = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', clean)
        # Remove backticks
        clean = clean.replace('`', '')
        clean = clean.strip()

        if len(clean) >= 3:
            tag = ADOPTION_STATUSES.get(status)
            if tag:
                patterns.append((clean, tag))

    return patterns


def match_adoption_tags(
    tweet_text: str,
    primary_keyword: Optional[str],
    keywords: list[str],
    llm_category: Optional[str],
    patterns: list[tuple[str, str]],
) -> list[str]:
    """
    Check if a tweet matches any adoption patterns from PROGRESS.md.
    Returns list of matching adoption tags.
    """
    tags = set()
    search_text = (tweet_text or "").lower()
    kw_lower = (primary_keyword or "").lower()
    keywords_lower = [k.lower() for k in keywords]
    cat_lower = (llm_category or "").lower()

    for pattern_text, tag in patterns:
        # Direct keyword match
        if pattern_text in search_text:
            tags.add(tag)
            continue

        # Match against primary_keyword
        if kw_lower and pattern_text in kw_lower:
            tags.add(tag)
            continue

        # Match against keywords list
        for kw in keywords_lower:
            if pattern_text in kw or kw in pattern_text:
                tags.add(tag)
                break

        # Match specific well-known technique names to categories
        technique_category_map = {
            "handoff": "context-management",
            "handover": "context-management",
            "compact": "context-management",
            "subagent": "subagents",
            "hook": "hooks",
            "skill": "skills",
            "slash command": "commands",
            "plan mode": "planning",
            "mcp": "mcp",
            "obsidian": "tooling",
            "playwriter": "tooling",
        }
        for tech_name, tech_cat in technique_category_map.items():
            if tech_name in pattern_text and cat_lower == tech_cat:
                tags.add(tag)

    return sorted(tags)


class VaultEnhancer:
    """Enhance an exported Obsidian vault with clusters, links, and adoption tags."""

    def __init__(
        self,
        vault_dir: Path,
        db_path: Path,
        progress_path: Path,
        dry_run: bool = False,
        skip_clusters: bool = False,
        skip_links: bool = False,
        skip_tags: bool = False,
    ):
        self.vault_dir = vault_dir
        self.db_path = db_path
        self.progress_path = progress_path
        self.dry_run = dry_run
        self.skip_clusters = skip_clusters
        self.skip_links = skip_links
        self.skip_tags = skip_tags

        # State
        self.notes: dict[str, dict] = {}  # filename -> metadata
        self.tweet_id_to_file: dict[str, str] = {}  # tweet_id -> filename
        self.author_to_files: dict[str, list[str]] = defaultdict(list)
        self.category_to_files: dict[str, list[str]] = defaultdict(list)
        self.keyword_to_files: dict[str, list[str]] = defaultdict(list)

        # Stats
        self.clusters_created = 0
        self.files_moved = 0
        self.links_added = 0
        self.tags_added = 0

    def load_vault_notes(self):
        """Scan vault for .md files and parse their frontmatter."""
        print("Scanning vault notes...")
        for md_file in sorted(self.vault_dir.glob("*.md")):
            metadata = self._parse_frontmatter(md_file)
            if metadata and metadata.get("tweet_id"):
                fname = md_file.name
                self.notes[fname] = metadata
                self.notes[fname]["_path"] = md_file

                tid = metadata["tweet_id"]
                self.tweet_id_to_file[tid] = fname

                author = metadata.get("author", "")
                if author:
                    self.author_to_files[author].append(fname)

        print(f"  Found {len(self.notes)} vault notes")

    def load_db_metadata(self):
        """Load category and keyword data from SQLite to supplement frontmatter."""
        if not self.db_path.exists():
            print(f"  Warning: DB not found at {self.db_path}, skipping DB enrichment")
            return

        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT t.id, ti.llm_category, ti.keywords_json, ti.primary_keyword,
                   t.text, t.handle
            FROM tweets t
            LEFT JOIN tips ti ON t.id = ti.tweet_id
        """)

        for row in cursor.fetchall():
            tid = row["id"]
            fname = self.tweet_id_to_file.get(tid)
            if not fname:
                continue

            # Store category
            cat = row["llm_category"]
            if cat:
                self.notes[fname]["llm_category"] = cat
                dir_name = CATEGORY_DIRS.get(cat, cat)
                self.category_to_files[dir_name].append(fname)

            # Store keywords for linking
            keywords_json = row["keywords_json"]
            keywords = []
            if keywords_json:
                try:
                    keywords = json.loads(keywords_json)
                    if not isinstance(keywords, list):
                        keywords = []
                except (json.JSONDecodeError, TypeError):
                    keywords = []

            self.notes[fname]["keywords"] = keywords
            self.notes[fname]["primary_keyword"] = row["primary_keyword"]
            self.notes[fname]["text"] = row["text"] or ""

            for kw in keywords:
                kw_lower = kw.lower().strip()
                if len(kw_lower) >= 3:
                    self.keyword_to_files[kw_lower].append(fname)

        conn.close()
        print(f"  Loaded DB metadata for {len(self.notes)} notes")
        print(f"  Categories: {len(self.category_to_files)}")
        print(f"  Keywords: {len(self.keyword_to_files)}")

    def _parse_frontmatter(self, md_file: Path) -> Optional[dict]:
        """Extract YAML frontmatter fields from a note."""
        try:
            content = md_file.read_text()
        except Exception:
            return None

        if not content.startswith("---"):
            return None

        # Find end of frontmatter
        end_idx = content.find("---", 3)
        if end_idx == -1:
            return None

        fm_text = content[3:end_idx]
        metadata = {"_raw_content": content}

        # Simple YAML parsing (avoid dependency on pyyaml)
        for line in fm_text.split("\n"):
            line = line.strip()
            if ":" in line and not line.startswith("-"):
                key, _, val = line.partition(":")
                key = key.strip()
                val = val.strip().strip('"').strip("'")
                metadata[key] = val

        # Extract tweet_id from the ID line at end of file
        id_match = re.search(r'\*\*ID:\*\*\s*\[(\d+)\]', content)
        if id_match:
            metadata["tweet_id"] = id_match.group(1)

        # Extract existing tags
        tags = []
        tag_match = re.findall(r'^\s+-\s+(.+)$', fm_text, re.MULTILINE)
        if tag_match:
            tags = [t.strip() for t in tag_match]
        metadata["existing_tags"] = tags

        return metadata

    # ── Task 1: Topic Clusters ───────────────────────────────────────────

    def create_topic_clusters(self):
        """Move notes into subdirectories based on llm_category."""
        if self.skip_clusters:
            print("\nSkipping topic clusters (--skip-clusters)")
            return

        print("\nCreating topic clusters...")

        # Filter out small clusters
        viable_clusters = {
            cat: files
            for cat, files in self.category_to_files.items()
            if len(files) >= MIN_CLUSTER_SIZE
        }

        print(f"  Viable clusters (>= {MIN_CLUSTER_SIZE} notes): {len(viable_clusters)}")
        for cat, files in sorted(viable_clusters.items(), key=lambda x: -len(x[1])):
            print(f"    {cat}: {len(files)} notes")

        if self.dry_run:
            print("  (dry run — no files moved)")
            return

        for cat_dir, files in viable_clusters.items():
            target_dir = self.vault_dir / cat_dir
            target_dir.mkdir(exist_ok=True)
            self.clusters_created += 1

            for fname in files:
                src = self.vault_dir / fname
                dst = target_dir / fname
                if src.exists():
                    shutil.move(str(src), str(dst))
                    # Update internal references
                    self.notes[fname]["_path"] = dst
                    self.notes[fname]["_subdir"] = cat_dir
                    self.files_moved += 1

        print(f"  Created {self.clusters_created} cluster directories")
        print(f"  Moved {self.files_moved} files")

    # ── Task 2: Bidirectional Links ──────────────────────────────────────

    def add_bidirectional_links(self):
        """Add wiki-links between related notes."""
        if self.skip_links:
            print("\nSkipping bidirectional links (--skip-links)")
            return

        print("\nAdding bidirectional links...")

        # Build a relationship map: filename -> set of related filenames
        relationships: dict[str, set[str]] = defaultdict(set)

        # 2a. Same author links (authors with 2+ tips)
        author_links = 0
        for author, files in self.author_to_files.items():
            if len(files) < 2:
                continue
            for i, f1 in enumerate(files):
                for f2 in files[i + 1:]:
                    relationships[f1].add(f2)
                    relationships[f2].add(f1)
                    author_links += 1
        print(f"  Author relationships: {author_links}")

        # 2b. Same keyword links (keywords shared by 2+ tips, max 10 tips per keyword)
        keyword_links = 0
        for kw, files in self.keyword_to_files.items():
            if len(files) < 2 or len(files) > 10:
                # Skip very common keywords (too noisy) and singletons
                continue
            for i, f1 in enumerate(files):
                for f2 in files[i + 1:]:
                    relationships[f1].add(f2)
                    relationships[f2].add(f1)
                    keyword_links += 1
        print(f"  Keyword relationships: {keyword_links}")

        # 2c. Same category links — only link within small categories (< 15)
        #     to avoid linking everything in "tooling" to everything else
        category_links = 0
        for cat, files in self.category_to_files.items():
            if len(files) < 2 or len(files) > 15:
                continue
            for i, f1 in enumerate(files):
                for f2 in files[i + 1:]:
                    relationships[f1].add(f2)
                    relationships[f2].add(f1)
                    category_links += 1
        print(f"  Category relationships: {category_links}")

        # Now inject "Related Tips" sections into each note
        total_links = sum(len(v) for v in relationships.values())
        print(f"  Total unique link pairs to inject: {total_links // 2}")

        if self.dry_run:
            print("  (dry run — no files modified)")
            return

        for fname, related_set in relationships.items():
            if not related_set:
                continue
            self._inject_related_section(fname, related_set)

        print(f"  Links injected into {self.links_added} notes")

    def _inject_related_section(self, fname: str, related_files: set[str]):
        """Add a '## Related Tips' section to a note with wiki-links."""
        note = self.notes.get(fname)
        if not note:
            return

        file_path = note.get("_path")
        if not file_path or not file_path.exists():
            return

        content = file_path.read_text()

        # Remove any existing Related Tips section (idempotent)
        content = re.sub(
            r'\n## Related Tips\n.*?(?=\n## |\n> \[!metrics\]|\Z)',
            '',
            content,
            flags=re.DOTALL,
        )

        # Build the related tips section
        # Limit to 8 most relevant links to keep notes clean
        sorted_related = sorted(related_files)[:8]
        links_md = []
        for rel_fname in sorted_related:
            # Wiki-link uses filename without .md extension
            link_name = rel_fname.replace('.md', '')
            rel_note = self.notes.get(rel_fname, {})
            author = rel_note.get("author", "")
            # Include subdirectory path if note was moved to a cluster
            subdir = rel_note.get("_subdir", "")
            if subdir:
                link_target = f"{subdir}/{link_name}"
            else:
                link_target = link_name
            if author:
                links_md.append(f"- [[{link_target}]] ({author})")
            else:
                links_md.append(f"- [[{link_target}]]")

        related_section = "\n## Related Tips\n\n" + "\n".join(links_md) + "\n"

        # Insert before the metrics callout at the end
        metrics_marker = "\n> [!metrics]"
        if metrics_marker in content:
            content = content.replace(
                metrics_marker,
                related_section + metrics_marker,
            )
        else:
            # Append at end
            content = content.rstrip() + "\n" + related_section

        file_path.write_text(content)
        self.links_added += 1

    # ── Task 3: Adoption Tags ────────────────────────────────────────────

    def add_adoption_tags(self):
        """Add adoption status tags from PROGRESS.md."""
        if self.skip_tags:
            print("\nSkipping adoption tags (--skip-tags)")
            return

        print("\nAdding adoption status tags...")

        patterns = parse_progress_file(self.progress_path)
        print(f"  Loaded {len(patterns)} technique patterns from PROGRESS.md")

        if not patterns:
            print("  No patterns found, skipping")
            return

        if self.dry_run:
            # Show what would be tagged
            tagged_count = 0
            for fname, note in self.notes.items():
                tags = match_adoption_tags(
                    note.get("text", ""),
                    note.get("primary_keyword"),
                    note.get("keywords", []),
                    note.get("llm_category"),
                    patterns,
                )
                if tags:
                    tagged_count += 1
                    print(f"    {fname}: {', '.join(tags)}")
            print(f"  (dry run — would tag {tagged_count} notes)")
            return

        for fname, note in self.notes.items():
            tags = match_adoption_tags(
                note.get("text", ""),
                note.get("primary_keyword"),
                note.get("keywords", []),
                note.get("llm_category"),
                patterns,
            )
            if tags:
                self._inject_adoption_tags(fname, tags)

        print(f"  Tagged {self.tags_added} notes with adoption status")

    def _inject_adoption_tags(self, fname: str, new_tags: list[str]):
        """Add adoption status tags to a note's frontmatter."""
        note = self.notes.get(fname)
        if not note:
            return

        file_path = note.get("_path")
        if not file_path or not file_path.exists():
            return

        content = file_path.read_text()

        # Find the tags section in frontmatter
        # Look for the pattern:
        # tags:
        #   - existing/tag
        #   - ...
        # And add new tags

        # First, check if these tags already exist (idempotent)
        existing_tags = note.get("existing_tags", [])
        tags_to_add = [t for t in new_tags if t not in existing_tags]

        if not tags_to_add:
            return

        # Find insertion point: after the last tag line in frontmatter
        tag_section_re = re.compile(
            r'(tags:\n(?:\s+-\s+.+\n)*)',
            re.MULTILINE,
        )
        match = tag_section_re.search(content)
        if match:
            old_section = match.group(1)
            new_lines = "".join(f"  - {tag}\n" for tag in tags_to_add)
            new_section = old_section + new_lines
            content = content.replace(old_section, new_section, 1)
        else:
            # No tags section found — add before the closing ---
            # Find the second ---
            first_end = content.find("---", 3)
            if first_end > 0:
                insert_point = first_end
                tag_block = "tags:\n" + "".join(f"  - {tag}\n" for tag in tags_to_add)
                content = content[:insert_point] + tag_block + content[insert_point:]

        file_path.write_text(content)
        self.tags_added += 1

    # ── Orchestration ────────────────────────────────────────────────────

    def enhance(self):
        """Run all enhancement passes."""
        print(f"Vault Enhancement")
        print(f"=" * 40)
        print(f"Vault: {self.vault_dir}")
        print(f"DB: {self.db_path}")
        print(f"Progress: {self.progress_path}")
        if self.dry_run:
            print("MODE: DRY RUN (no changes)")
        print()

        # Load data
        self.load_vault_notes()
        self.load_db_metadata()

        # Run enhancements in order:
        # 1. Adoption tags first (before moving files)
        self.add_adoption_tags()

        # 2. Bidirectional links (before moving, so paths are correct)
        #    Note: links use wiki-link syntax which Obsidian resolves regardless of path
        self.add_bidirectional_links()

        # 3. Topic clusters last (moves files)
        self.create_topic_clusters()

        # Summary
        print(f"\nEnhancement complete:")
        print(f"  Clusters created: {self.clusters_created}")
        print(f"  Files moved: {self.files_moved}")
        print(f"  Notes with links: {self.links_added}")
        print(f"  Notes with adoption tags: {self.tags_added}")


def main():
    parser = argparse.ArgumentParser(
        description="Enhance exported Obsidian vault with clusters, links, and adoption tags"
    )
    parser.add_argument(
        "--vault", "-v",
        type=Path,
        default=Path(__file__).parent.parent.parent / "Claude Code Tips",
        help="Path to vault directory (default: ./Claude Code Tips)",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=Path(__file__).parent.parent.parent / "data" / "claude_code_tips_v2.db",
        help="Path to tips database",
    )
    parser.add_argument(
        "--progress",
        type=Path,
        default=Path(__file__).parent.parent.parent / "plans" / "PROGRESS.md",
        help="Path to PROGRESS.md for adoption status",
    )
    parser.add_argument(
        "--dry-run", "-n",
        action="store_true",
        help="Show what would be done without modifying files",
    )
    parser.add_argument(
        "--skip-clusters",
        action="store_true",
        help="Skip topic cluster creation (links + tags only)",
    )
    parser.add_argument(
        "--skip-links",
        action="store_true",
        help="Skip bidirectional link injection (clusters + tags only)",
    )
    parser.add_argument(
        "--skip-tags",
        action="store_true",
        help="Skip adoption tag injection (clusters + links only)",
    )

    args = parser.parse_args()

    if not args.vault.exists():
        print(f"Error: Vault directory not found at {args.vault}")
        return 1

    enhancer = VaultEnhancer(
        vault_dir=args.vault,
        db_path=args.db,
        progress_path=args.progress,
        dry_run=args.dry_run,
        skip_clusters=args.skip_clusters,
        skip_links=args.skip_links,
        skip_tags=args.skip_tags,
    )

    enhancer.enhance()
    return 0


if __name__ == "__main__":
    exit(main())
