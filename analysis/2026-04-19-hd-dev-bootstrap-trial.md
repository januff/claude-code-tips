# HD-Dev Bootstrap Trial — 2026-04-19

Single-day real-world application of the Project Bootstrap Playbook (v0.2) against Will Kreth's Human & Digital startup. Notes for the playbook's next revision.

## What we built

- `PROJECT_BOOTSTRAP_PLAYBOOK.md` v0.2 (major revision from v0.1)
- `HD-Dev/wiki/` full structure: 8 concept articles, 6 person profiles, 5 event articles, GLOSSARY, WHO, TIMELINE, DECISIONS, _index, _SUMMARY_FOR_WILL
- 4 compilation passes in a single day, no Will involvement required
- PR #1 opened to `humandigital-tech/HD-Dev` via fork pattern

## What worked

- **Research-first before writing.** Deep-reading 6 HD source documents via a research subagent produced a structured findings report that made the compilation work fast and high-fidelity.
- **Concept articles with Sources + Related + Open questions sections.** Template held up across 8 different topics. The "Open questions" section is where genuine unresolved-ness lives, which makes the wiki honest about its gaps.
- **Exhaust-the-docs before asking the human.** 5 of 6 original open questions resolved from source material alone, without bothering Will. Only 4 genuinely-unresolved items remain in DECISIONS.md.
- **Terminology-collision detection.** The wiki caught a Type 01/02/03 naming conflict between public and internal docs — the kind of thing a human wouldn't notice reading them separately.
- **People/events pass as the fast legibility test.** Short articles, high-density information, immediate spot-checkability. Perfect for the first review artifact.
- **Summary doc as handhold + preview.** The `_SUMMARY_FOR_WILL.md` serves double duty — it's the entry point for a GitHub reviewer AND it's what gets emailed ahead of the PR so the receiver has context.

## What didn't work / surprised us

- **Obsidian `[[wiki-link]]` syntax is a liability for non-Obsidian readers.** Required a conversion-and-fixup pipeline (`convert_wiki_links.py` + `fix_broken_links.py` + `fix_stub_paths.py`) — ~4 passes of script-then-validate to get all 294 links right. For future projects, **author in Markdown-link syntax from the start**. Don't use wiki-links if GitHub-web viewing is a first-class requirement.
- **The conversion script had a real bug.** `./path.md` relative paths only work from repo root; from subdirectories the paths needed `../` adjustment. The second-pass fix was necessary, not polish. A better design: resolve the target file first, *then* compute the relative path, don't emit a blind `./` default.
- **Private repos often have forking disabled.** Standard GitHub security hygiene. Meant that even the "outside contributor" pattern required one admin toggle from the repo owner before anything could move.
- **Read-only collaborator status is common.** We assumed Joey could push to Will's repo because he'd cloned it. Not so — read-only by default. The fork + PR pattern became mandatory, not optional.
- **`gh` auth is keyed to a single account.** If you're collaborating on multiple orgs with different accounts, there's no easy multi-account workflow. Worth noting in the playbook.
- **Auto-mode / permission setup needs explicit onboarding.** Will's summary doc now has a dedicated Step 3b because otherwise every git operation would prompt for approval. The Shift+Tab cycle isn't discoverable.

## Decisions that should inform the playbook v0.3

1. **Recommend Markdown-link syntax as the canonical format from day 1.** Obsidian handles both; GitHub/TextMate/everything else only handles the standard form. Save everyone the conversion.

2. **Lead the team-enrollment docs with "enable forking on private repos."** Add to Phase 4 as an explicit step. For private org repos, forking needs to be enabled before outside contribution works.

3. **Formalize the paste-this-prompt pattern.** Every ask to a team member should be structured as an executable prompt for their Claude Code session, not a natural-language request. This works dramatically better for technical onboarding friction.

4. **Auto mode is now table stakes.** The Shift+Tab → Auto Mode setup should be a named step in team enrollment, not a footnote.

5. **The summary doc is a first-class artifact of the bootstrap.** v0.1 implied it as an output; v0.3 should name it explicitly and provide a template.

6. **The fork-and-PR-from-fork pattern is the default.** Even if you could grant write access, the fork pattern gives you a cleaner iteration boundary. Name it as the primary contribution path.

## Scripts preserved

In `scripts/playbook/`:

- `convert_wiki_links.py`
- `fix_broken_links.py`
- `fix_stub_paths.py`

See `scripts/playbook/README.md` for usage notes and known limitations.

## Numbers

- **Source documents processed:** 9 (1 email, 1 tool README, 1 top-level README, 3 HTML files, 3 PDFs)
- **Wiki artifacts produced:** 30 files
- **Total internal links generated:** 294
- **Broken-stub links (intentional):** 21
- **Pass-count:** 4 on the documents alone (no chat archive yet)
- **Compilation time:** ~6 hours end-to-end
- **Questions asked of Will:** 0

That last number is the one that matters most.
