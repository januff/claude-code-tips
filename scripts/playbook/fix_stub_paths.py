#!/usr/bin/env python3
"""Second fixup pass: remap './subtree/X.md' paths to the correct relative form
for links that target files that don't exist yet (stub articles).

The bug: the original conversion script used './path.md' for any link_target,
which is correct only when source is at wiki/ root. From inside wiki/concepts/,
wiki/people/, or wiki/events/, the path needs adjustment.
"""

import re
from pathlib import Path

REPO_ROOT = Path('/Users/joeyanuff-m2/Development/HD-Dev')
WIKI_ROOT = REPO_ROOT / 'wiki'
SUBTREES = ('concepts', 'people', 'events')

LINK_PATTERN = re.compile(r'\[([^\]]*)\]\(([^)]+)\)')


def fix_link(match, source_file: Path) -> str:
    text = match.group(1)
    raw_path = match.group(2)

    if raw_path.startswith(('http://', 'https://', 'mailto:', '#')):
        return match.group(0)

    # Separate path and anchor
    if '#' in raw_path:
        path_part, anchor_tail = raw_path.split('#', 1)
        anchor = '#' + anchor_tail
    else:
        path_part = raw_path
        anchor = ''

    if not path_part:
        return match.group(0)

    # Only concerned with paths that start with './'
    if not path_part.startswith('./'):
        return match.group(0)

    rel_inner = path_part[2:]  # strip './'

    # Determine source's position relative to wiki/
    try:
        source_in_wiki = source_file.relative_to(WIKI_ROOT)
    except ValueError:
        return match.group(0)
    source_parts = source_in_wiki.parts
    source_subtree = source_parts[0] if len(source_parts) > 1 else ''

    # Check if the link target starts with a subtree prefix
    for subtree in SUBTREES:
        prefix = subtree + '/'
        if rel_inner.startswith(prefix):
            if source_subtree == subtree:
                # Same subtree: strip the redundant prefix
                new_path = './' + rel_inner[len(prefix):]
            elif source_subtree in SUBTREES:
                # Different subtree: need to go up one then into target subtree
                new_path = '../' + rel_inner
            else:
                # Source is at wiki/ root: original is correct
                return match.group(0)

            # Verify: does the new path resolve? (could be a stub that doesn't exist,
            # but the PATH structure should now be sensible)
            return f'[{text}]({new_path}{anchor})'

    # No subtree prefix — check if the target is a bare stem for a stub in the same subtree
    # e.g., from wiki/events/foo.md, './provenance-schema.md' would only be valid if source is
    # in wiki/concepts/. Since source is wiki/events/, and the file doesn't exist, we can't
    # be sure what subtree it belongs in. Leave alone.
    return match.group(0)


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
for f in sorted(WIKI_ROOT.rglob('*.md')):
    if process_file(f, dry_run=dry_run):
        print(f'{"[DRY]" if dry_run else "[FIX]"} {f.relative_to(REPO_ROOT)}')
        fixed += 1
print(f'\n{fixed} files {"would be" if dry_run else "were"} remapped.')
