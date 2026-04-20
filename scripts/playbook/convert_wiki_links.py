#!/usr/bin/env python3
"""Convert Obsidian [[wiki-links]] to Markdown [text](./path.md) format.

Handles:
- [[bare-name]] → resolves against all files in repo
- [[path/to/file]] → resolves with or without .md extension
- [[path/to/file|display text]] → custom display text
- [[path#section]] → GitHub anchor format
- [[#section-only]] → in-page anchor
- Non-.md targets (.pdf, .txt, .html) for source documents
"""

import re
import os
import sys
from pathlib import Path

REPO_ROOT = Path('/Users/joeyanuff-m2/Development/HD-Dev')
WIKI_ROOT = REPO_ROOT / 'wiki'

# Build index of all files in the repo by multiple keys
file_index = {}  # key -> absolute Path

for f in REPO_ROOT.rglob('*'):
    if not f.is_file():
        continue
    parts = f.parts
    if '.git' in parts or '.obsidian' in parts:
        continue
    rel = f.relative_to(REPO_ROOT)
    file_index.setdefault(str(rel), f)  # full rel path with ext
    file_index.setdefault(str(rel.with_suffix('')), f)  # full rel path without ext
    file_index.setdefault(f.name, f)  # basename with ext
    file_index.setdefault(f.stem, f)  # basename without ext


def resolve_target(link_target: str):
    """Find the actual file for a link target. Returns Path or None."""
    # Exact and extension-padded lookups
    candidates = [
        link_target,
        link_target + '.md',
        link_target + '.txt',
        link_target + '.pdf',
        link_target + '.html',
    ]
    for c in candidates:
        if c in file_index:
            return file_index[c]

    # Prefix match on stem — e.g., "HD_PreSeed_Deck" → "HD_PreSeed_Deck_v11.7.pdf"
    stem = link_target.split('/')[-1]
    for key, path in file_index.items():
        if path.is_file() and path.stem.startswith(stem) and path.stem != stem:
            return path

    return None


def github_anchor(section: str) -> str:
    """Convert a heading text to GitHub's anchor format."""
    # GitHub lowercases, strips most punctuation, replaces spaces with hyphens
    s = section.lower()
    # Remove characters that GitHub strips (punctuation other than hyphens/underscores)
    s = re.sub(r'[^\w\s-]', '', s)
    # Collapse whitespace to single hyphen
    s = re.sub(r'\s+', '-', s)
    # Collapse multiple hyphens (but GitHub keeps them — actually depends, let's keep as-is)
    return s


def human_text(link_target: str) -> str:
    """Derive display text from a path-style target."""
    stem = link_target.split('/')[-1]
    for ext in ('.md', '.html', '.txt', '.pdf'):
        if stem.endswith(ext):
            stem = stem[:-len(ext)]
            break
    # Replace dashes and underscores with spaces
    return stem.replace('_', ' ').replace('-', ' ')


def make_relative(target: Path, source: Path) -> str:
    """Build a relative Markdown path from source file to target."""
    source_dir = source.parent
    rel = os.path.relpath(target, source_dir)
    # Ensure leading ./ or ../
    if not rel.startswith(('.', '/')):
        rel = './' + rel
    return rel


LINK_PATTERN = re.compile(r'\[\[([^\]|]+?)(?:\|([^\]]+))?\]\]')


def convert_link(match, source_file: Path) -> str:
    link_target = match.group(1).strip()
    display_text = match.group(2).strip() if match.group(2) else None

    # Section anchor
    raw_section = None
    if '#' in link_target:
        link_target, raw_section = link_target.split('#', 1)

    # Same-file anchor: [[#Open questions]]
    if not link_target and raw_section:
        anchor = github_anchor(raw_section)
        text = display_text or raw_section
        return f'[{text}](#{anchor})'

    # Resolve target
    target_file = resolve_target(link_target)

    if target_file is None:
        # Unresolvable — best-effort. Assume .md in the same logical subtree.
        # If link_target starts with a known subdir (concepts/, people/, events/, documents/), use it.
        # Otherwise, guess as if it's a sibling.
        assumed_path = link_target + '.md' if not link_target.endswith(('.md', '.pdf', '.txt', '.html')) else link_target
        # If the link target has no slash, it's likely a sibling of the source in wiki/
        if '/' not in assumed_path:
            # Might be CLAUDE.md at repo root, or a wiki root file, or a stub
            rel = './' + assumed_path
        else:
            rel = './' + assumed_path
    else:
        rel = make_relative(target_file, source_file)

    if raw_section:
        # Use the section as given if it already looks like an anchor (contains dashes, no spaces)
        if re.match(r'^[a-z0-9\-_]+$', raw_section):
            anchor = raw_section
        else:
            anchor = github_anchor(raw_section)
        rel += '#' + anchor

    if not display_text:
        display_text = human_text(link_target)

    return f'[{display_text}]({rel})'


def process_file(path: Path, dry_run: bool = False):
    content = path.read_text()
    matches_before = len(LINK_PATTERN.findall(content))
    new_content = LINK_PATTERN.sub(lambda m: convert_link(m, path), content)
    changed = new_content != content
    if changed and not dry_run:
        path.write_text(new_content)
    return changed, matches_before


def main():
    dry_run = '--dry-run' in sys.argv
    total_files = 0
    total_links = 0
    # Process all .md files under wiki/ AND the top-level CLAUDE.md
    targets = list(WIKI_ROOT.rglob('*.md'))
    targets += [REPO_ROOT / 'CLAUDE.md']
    for f in sorted(targets):
        if not f.exists():
            continue
        changed, count = process_file(f, dry_run=dry_run)
        if changed or count > 0:
            rel = f.relative_to(REPO_ROOT)
            marker = '[DRY]' if dry_run else '[OK]'
            print(f'{marker} {rel} — {count} links')
            if changed:
                total_files += 1
                total_links += count
    print(f'\nTotal: {total_files} files {"would be" if dry_run else "were"} updated, {total_links} links converted.')


if __name__ == '__main__':
    main()
