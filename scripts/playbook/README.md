# Playbook Tooling

Scripts extracted from the 2026-04-19 HD-Dev bootstrap trial that proved useful enough to generalize.

## `convert_wiki_links.py`

Converts Obsidian `[[wiki-link]]` syntax to GitHub-compatible Markdown links (`[text](./path.md)`).

Use when:
- Shipping an Obsidian-authored wiki to GitHub for team review
- Getting a knowledge base to work in both Obsidian AND GitHub web view without forcing tool installs

Handles:
- Bare-name, path-form, and alias-form wiki-links (`[[foo]]`, `[[path/foo]]`, `[[foo|display text]]`)
- Section references (`[[foo#section]]` → `[text](./foo.md#anchor)`)
- Same-file anchors (`[[#section]]`)
- File resolution across `.md`, `.pdf`, `.txt`, `.html`
- Prefix-match stems (e.g., `[[HD_PreSeed_Deck]]` → `HD_PreSeed_Deck_v11.7.pdf`)

Known limitation: emits `./path.md` for link targets without leading dot, which is wrong when the source file is in a subdirectory. Follow with `fix_broken_links.py` + `fix_stub_paths.py` to repair.

## `fix_broken_links.py`

Post-conversion cleanup: for every Markdown link in every file, tests whether the path resolves and, if not, searches the repo for the intended target by filename/stem and rewrites the path correctly.

Handles:
- Indirect directory references (e.g., `./hd-candidate-search-tool.md` when only `hd-candidate-search-tool/README.md` exists)
- Subtree-relative paths broken by the conversion bug above

## `fix_stub_paths.py`

Second pass: for broken links pointing to *non-existent* stub articles (planned-but-not-drafted), remaps paths to be syntactically correct relative to the source file's subtree. These will auto-resolve when the target files are eventually created.

## Usage pattern

```bash
# From the repo root of the wiki you're converting
python3 /path/to/convert_wiki_links.py
python3 /path/to/fix_broken_links.py
python3 /path/to/fix_stub_paths.py

# Validate
# (write your own quick grep for remaining [[ or broken paths)
```

All three scripts hard-code `/Users/joeyanuff-m2/Development/HD-Dev` — edit the `REPO_ROOT` constant before using elsewhere. A future iteration should take the path as a CLI argument.
