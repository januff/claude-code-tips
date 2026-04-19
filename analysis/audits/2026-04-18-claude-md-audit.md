# CLAUDE.md + Setup Audit — 2026-04-18

> Experiment 2 from the Karpathy/community-best-practices investigation.
> Method: @itsolelehmann's "audit your setup" prompt (1,695 likes, 2026-03-23).
> Status: **Assessment only. No changes applied yet.**

## Source prompt

From @itsolelehmann (2026-03-23), applied literally. The five audit questions per rule:

1. Is this something Claude already does by default?
2. Does this contradict or conflict with another rule?
3. Does this repeat something already covered elsewhere?
4. Does this read like a one-off fix for one bad output rather than a general improvement?
5. Is this so vague that it would be interpreted differently every time?

## Before-state inventory

| Artifact | Size | Notes |
|----------|-----:|-------|
| `CLAUDE.md` | 239 lines, 8,542 bytes (~2,135 tokens) | Close to Boris's 2.5k budget but heavily sectioned |
| `.claude/commands/` | 10 files | 4 Anthropic-supplied, 6 project-specific |
| `.claude/references/` | 8 files | Specs and context docs |
| `.claude/hooks/` | 2 active hooks | pre-compact, session-end |
| `MEMORY.md` (auto-memory) | Separate file at `~/.claude/projects/.../memory/MEMORY.md` | Not audited in this pass |

CLAUDE.md has 18 distinct sections. Breaking each down:

---

## Section-by-section audit

### 1. 🎯 First: Check STATUS.json
**Verdict: KEEP but deduplicate.** The same instruction appears again in "Your Task" (section 13). Consolidate.

### 2. Project Purpose
**Verdict: KEEP but destatify.** Numbers are stale (says 468 tips / 457 notes; real numbers are 562 / 552). Either update or remove specific counts and let STATUS.json own them.

### 3. Current Date Awareness — "should be February 2026"
**Verdict: CUT.** This is the single most obvious one-off fix in the document. Three strikes:
- Claude already gets current date in the system prompt (today's system reminder says `2026-04-18`)
- The value is stale (says Feb 2026, we're in April)
- It's the exact "I got one bad output so I added a rule" anti-pattern itsolelehmann describes

### 4. 🔄 Working Model: Code Tab as Orchestrator
**Verdict: KEEP, TRIM.** Core insight is valuable (why this project uses one-tab orchestration). But the capability bullet list mixes project-specific (pre-compact hook) with general Claude Code features (Plan mode, subagents via Task tool). Trim to project-specific.

### 5. Historical note about chat-tab/code-tab delegation
**Verdict: CUT.** This explains what NOT to do. The Decision 13 reference is enough — anyone who needs the history can follow the pointer. CLAUDE.md shouldn't carry legacy notes in perpetuity.

### 6. 🏆 Boris Cherny's Tips (12-row table)
**Verdict: CUT from CLAUDE.md, migrate to LEARNINGS.md if not there.** This is the loudest violation in the file. It's:
- 12 rows of general Claude Code community advice
- Not project-specific
- Not operational guidance (Claude reading CLAUDE.md isn't going to toggle Plan Mode because the table says to)
- Reference material wearing the clothing of instructions
- Exactly the "table of rules piled up" pattern itsolelehmann warns against

### 7. 🔍 Research-First Heuristic
**Verdict: KEEP.** Arguably the strongest section. Project-grounded ("VectCutAPI lesson"), specific, actionable. This is what *every* section should look like.

### 8. 🌐 Browser Automation: Claude-in-Chrome
**Verdict: KEEP, TRIM.** The contention note (only one instance can hold the connection) is critical operational context. The list of 5 MCP tool names is bloat — Claude can see the MCP tool list directly and doesn't need reminding which ones exist.

### 9. 📊 Quality-Filtered Export Pattern
**Verdict: KEEP.** Project-specific design decision with a literal SQL snippet. Gold-standard section.

### 10. Project Structure (ASCII tree)
**Verdict: BORDERLINE, likely CUT.** A new instance can run `ls` or `tree`. The tree becomes stale as directories move. But it helps cold-start orientation. Possible compromise: keep a 3-line pointer ("primary data: data/, vault: Claude Code Tips/, plans: plans/active/") instead of the full tree.

### 11. Key Files table
**Verdict: MERGE with section 10.** Duplicates purpose of the tree.

### 12. Data State — one line
**Verdict: KEEP.** Cheap pointer, no staleness risk.

### 13. Your Task (4 decision-tree conditions)
**Verdict: MERGE with section 1.** "Read STATUS.json first; if it has an active_task, read its handoff doc and execute" could be one sentence, not two separate sections.

### 14. Extended Thinking
**Verdict: CUT.** Generic Claude info ("think" < "think hard" < "ultrathink"). Default knowledge. Not project-specific.

### 15. Useful Commands
**Verdict: CUT 3 of 4.** `/cost`, `/compact`, `Shift+Tab` are general Claude Code UX. Only `python scripts/whats_new.py --days 7` is project-specific. Keep that one, drop the rest.

### 16. Related Projects table
**Verdict: KEEP.** Useful cross-project context ("if you see hall-of-fake references, that's the sibling project").

### 17. 🚀 Cold-Start Prompt
**Verdict: CUT.** This is a template for the *user*, not an instruction for Claude. Move to README if it's useful to onboard new contributors.

### 18. Verification — "include 'context-first' in your first response"
**Verdict: CUT.** Classic one-off fix. Attestation-as-instruction — the assumption is "Claude wouldn't read CLAUDE.md unless forced to." That's addressing a symptom with a rule. If Claude isn't reading CLAUDE.md reliably, the fix is structural (hooks, tooling, harness config), not a magic word. Also: this rule conflicts with Karpathy's "Simplicity First" principle — it adds ceremony without improving outputs.

---

## Skills / commands audit

Less detailed pass across `.claude/commands/`:

| Command | Lines | Verdict |
|---------|------:|---------|
| `create-skill.md` | 42 | Duplicates `anthropic-skills:skill-creator` (now available as built-in skill). **CANDIDATE CUT.** |
| `daily-summary.md` | 71 | Project-specific. Unknown last use — has it fired in the last month? |
| `fetch-bookmarks.md` | 287 | **Largest single skill.** Essential but likely has accumulated edge cases. Worth a dedicated audit pass later. |
| `goals-audit.md` | 83 | Project-specific. Unknown last use. |
| `review-plan.md` | 104 | Duplicates anthropic-skills built-in `review-plan`. **CANDIDATE CUT.** |
| `review.md` | 90 | Duplicates anthropic-skills built-in `review`. **CANDIDATE CUT.** |
| `start-session.md` | 63 | Overlaps with `wrap-up.md`? Are both needed? |
| `task-plan.md` | 45 | Duplicates anthropic-skills built-in `task-plan`. **CANDIDATE CUT.** |
| `weekly-review.md` | 85 | Aspirational — has this ever been run? |
| `wrap-up.md` | 51 | Session close ritual. Likely worth keeping. |

**Pattern observed:** 4 of 10 commands duplicate built-in Anthropic skills. These were written before the skills existed or before we became aware of them. Classic accumulation: the custom version stuck around after the canonical version shipped.

---

## Summary of findings

### If we applied all "CUT" verdicts:

- CLAUDE.md would drop from **239 lines / 8,542 bytes** to roughly **90 lines / 3,500 bytes** — about 60% reduction
- Still over Boris's 2.5k-token guideline but much closer, and with less redundant content
- `.claude/commands/` would drop from **10 to 6** files

### Biggest violations ranked:

1. **Boris Cherny's Tips table** (section 6) — 12 rows of non-project-specific reference material
2. **Verification magic word** (section 18) — classic attestation-as-instruction
3. **Current Date Awareness** (section 3) — stale one-off fix, now actively wrong
4. **Extended Thinking + Useful Commands** (sections 14-15) — general Claude Code knowledge in a project-specific file
5. **Duplicate commands** — 4 of 10 skills shadow built-in Anthropic skills

### What the audit validates:

- Section 7 (Research-First) and Section 9 (Quality-Filtered Export) are the gold-standard examples of what a project CLAUDE.md section should look like: project-specific, action-grounded, has a concrete anecdote or snippet.
- The hook setup and STATUS.json architecture are working and shouldn't be touched.

### What the audit does NOT address:

- **Does Claude actually follow the rules that are in CLAUDE.md?** This is a separate empirical question. The audit only checks whether rules *deserve* to be there.
- **Is MEMORY.md redundant with any of this?** Not audited. The auto-memory file is separately maintained and should get its own pass.
- **Are the references/ files all being read?** Would need a usage analysis (which reference files are actually pulled in which sessions).
- **Does this match community best practices?** Comparison to `andrej-karpathy-skills` CLAUDE.md (2,357 bytes, 4 principles) is deferred to Experiment 1 when that plugin is installed.

---

## Recommended next steps

1. **Do NOT apply cuts yet.** The itsolelehmann prompt explicitly recommends a 3-task A/B test before deleting anything. Pick 3 common tasks that exercise CLAUDE.md (e.g., starting a session, running a fetch, running an analysis) and note current behavior.
2. **Then apply cuts in a branch.** Test the same 3 tasks. If outputs stay the same or improve, merge. If something breaks, add back only the specific rule that fixed it.
3. **Schedule a follow-up audit in ~30 days.** itsolelehmann's principle: "your AI setup should be getting simpler over time." If it's growing, we're drifting.

---

## Notes for the playbook

When this experiment completes, the playbook's Phase 5 (Iteration) should gain:

- **Audit-your-setup ritual** — run itsolelehmann's prompt quarterly
- **The 5-question filter** as a criterion for adding any new CLAUDE.md rule
- **The gold-standard pattern**: project-specific, action-grounded, with a concrete anecdote or snippet
- **The anti-pattern list**: one-off fix rules, attestation magic words, reference material disguised as instructions, general Claude info

---

*Audit performed by Claude Opus 4.6 in the claude-code-tips repo, 2026-04-18.*
*Source: itsolelehmann — https://x.com/itsolelehmann/status/2036065138147471665*
