# Claude Code Tips

A curated collection of 100+ tips from the Claude Code community, with analysis and commentary from Claude Opus 4.5.

**Source:** [Twitter/X thread by @alexalbert__](https://x.com/alexalbert__/status/2004575443484319954) (Anthropic's Claude Relations lead)
**Posted:** December 26, 2025
**Engagement:** 98.3K views, 667 likes, 941 bookmarks, 182 replies

## What's Here

| File | Description |
|------|-------------|
| [`CLAUDE.md`](CLAUDE.md) | Project instructions for Claude Code instances |
| [`tips/claude-tips-numbered.md`](tips/claude-tips-numbered.md) | Complete numbered list of 100+ tips |
| [`tips/claude-tips-grouped.md`](tips/claude-tips-grouped.md) | Tips organized by theme |
| [`analysis/claude-tips-analysis.md`](analysis/claude-tips-analysis.md) | Opus 4.5 commentary and recommendations |

## Top 5 Tips by Engagement

1. **The Handoff Technique** (160 likes) — Generate self-contained prompts for handing work to another AI instance
2. **"Take a step back and think holistically"** (77 likes) — Escape loops with this phrase
3. **"Threaten to use Codex"** (53 likes) — Emotional prompting (works, but see analysis for caveats)
4. **Architect in Claude Desktop first** (52 likes) — Separate planning from execution
5. **DevSQL for prompt analysis** (43 likes) — Analyze your own prompt history

## Key Themes

- **Context Management** — Clear sessions proactively, use `/compact`, leverage subagents for isolation
- **Planning vs Execution** — Never plan and implement in the same session
- **Documentation** — CLAUDE.md is foundational; treat memory files like code files
- **Extended Thinking** — `think` < `think hard` < `think harder` < `ultrathink`

## Using This Repo

### For Humans
Browse the tips, read the analysis, steal what works for you.

### For Claude Instances
The `CLAUDE.md` file contains project-specific instructions. New Claude Code sessions in this directory will automatically read it.

### Multi-Instance Workflows
This repo is designed to support handoffs between Claude instances (see Tip #1). The `/plans` directory contains documents formatted for inter-instance review and critique.

## Roadmap

- [ ] Starter CLAUDE.md template (`configs/starter-claude-md.md`)
- [ ] Example hooks configuration (`configs/example-hooks.json`)
- [ ] Context management skill (`skills/context-management/SKILL.md`)
- [ ] 4-week learning curriculum (`lessons/learning-plan.md`)
- [ ] Self-updating tip collector agent

## Contributing

Found a great Claude Code tip? Open an issue or PR with:
- The tip itself
- Source/attribution
- Your experience using it

## License

MIT — use freely, attribution appreciated.

---

*This repository was created as a handoff from Claude Opus 4.5 (claude.ai) to Claude Code, December 26, 2025*
