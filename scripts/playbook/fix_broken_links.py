#!/usr/bin/env python3
"""Fix broken relative paths in markdown links across wiki/."""

import re
import os
from pathlib import Path

REPO_ROOT = Path('/Users/joeyanuff-m2/Development/HD-Dev')
WIKI_ROOT = REPO_ROOT / 'wiki'

# Build index of all files by stem, basename, and directory-README
file_by_key = {}  # key -> list of paths

for f in REPO_ROOT.rglob('*'):
    if not f.is_file() or '.git' in f.parts or '.obsidian' in f.parts:
        continue
    file_by_key.setdefault(f.stem, []).append(f)
    file_by_key.setdefault(f.name, []).append(f)

# Also index README.md by parent directory name
for f in REPO_ROOT.rglob('README.md'):
    if '.git' in f.parts:
        continue
    file_by_key.setdefault(f.parent.name, []).append(f)


LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')


def fix_link(match, source_file: Path) -> str:
    text = match.group(1)
    raw_path = match.group(2)

    # Skip external URLs and bare anchors
    if raw_path.startswith(('http://', 'https://', 'mailto:', '#')):
        return match.group(0)

    # Split path and anchor
    path_part = raw_path
    anchor = ''
    if '#' in path_part:
        path_part, anchor_tail = path_part.split('#', 1)
        anchor = '#' + anchor_tail

    source_dir = source_file.parent

    # If path part is empty, it's an anchor-only link — leave it
    if not path_part:
        return match.group(0)

    # Test whether the resolved path exists
    try:
        target = (source_dir / path_part).resolve()
        if target.exists() and target.is_file():
            return match.group(0)  # already correct
    except Exception:
        pass

    # Path is broken — try to find the actual file
    name = Path(path_part).name
    stem = Path(path_part).stem

    candidates = []
    for key in (name, stem):
        for c in file_by_key.get(key, []):
            if c not in candidates:
                candidates.append(c)

    if not candidates:
        # Can't find — leave it (flag for manual review)
        return match.group(0)

    # Prefer candidates inside wiki/ if source is inside wiki/
    if 'wiki' in source_file.parts and len(candidates) > 1:
        in_wiki = [c for c in candidates if 'wiki' in c.parts]
        if in_wiki:
            candidates = in_wiki

    target = candidates[0]
    rel = os.path.relpath(target, source_dir)
    if not rel.startswith(('.', '/')):
        rel = './' + rel

    return f'[{text}]({rel}{anchor})'


def process_file(path: Path, dry_run: bool = False):
    content = path.read_text()
    new_content = LINK_PATTERN.sub(lambda m: fix_link(m, path), content)
    if new_content != content:
        if not dry_run:
            path.write_text(new_content)
        return True
    return False


import sys
dry_run = '--dry-run' in sys.argv

fixed = 0
targets = list(WIKI_ROOT.rglob('*.md')) + [REPO_ROOT / 'CLAUDE.md']
for f in sorted(targets):
    if not f.exists():
        continue
    if process_file(f, dry_run=dry_run):
        print(f'{"[DRY]" if dry_run else "[FIX]"} {f.relative_to(REPO_ROOT)}')
        fixed += 1

print(f'\n{fixed} files {"would be" if dry_run else "were"} fixed.')
