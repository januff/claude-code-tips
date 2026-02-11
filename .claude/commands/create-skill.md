---
name: create-skill
description: >
  Create a new skill (slash command) following Anthropic's best practices. Use when
  the user wants to create a new skill, command, or update an existing one. Reads the
  best practices guide first to ensure quality.
argument-hint: <skill-name> <description of what it should do>
---

# Create a Skill

Before creating or modifying any skill, read the best practices guide:

**Read `.claude/references/skills-best-practices.md` first.**

## Process

1. **Understand** what the skill should do — ask for concrete usage examples if unclear
2. **Plan** what resources it needs (scripts, references, assets)
3. **Check** if similar functionality already exists in `.claude/commands/`
4. **Create** the skill following these principles:
   - YAML frontmatter with `name` and comprehensive `description` (this is the trigger)
   - Body under 500 lines — split to `references/` if approaching limit
   - Move large inline content (scripts, API docs, schemas) to `.claude/references/`
   - Use imperative form in instructions
   - Only include what Claude doesn't already know
5. **Verify** the skill works by mentally walking through a usage scenario

## Checklist

- [ ] Frontmatter `description` includes "when to use" triggers
- [ ] Body is concise — no redundant explanations
- [ ] Large content moved to reference files with clear pointers
- [ ] `disable-model-invocation: true` if the skill should only be user-triggered (deploy, commit, destructive actions)
- [ ] No extraneous files (README, CHANGELOG, etc.)

## Where to Place Skills

- Project-specific: `.claude/commands/<name>.md` (legacy) or `.claude/skills/<name>/SKILL.md`
- Personal: `~/.claude/skills/<name>/SKILL.md`

For this project, use `.claude/commands/<name>.md` for consistency with existing commands.
