# Skills Best Practices Reference

> Synthesized from [anthropics/skills](https://github.com/anthropics/skills) skill-creator
> and [Claude Code Skills docs](https://code.claude.com/docs/en/skills).
> Last fetched: 2026-02-11

---

## Core Principles

### 1. Concise is Key

The context window is a public good. Only add context Claude doesn't already have. Challenge each piece of information: "Does Claude really need this?" and "Does this justify its token cost?"

Prefer concise examples over verbose explanations.

### 2. Set Appropriate Degrees of Freedom

- **High freedom** (text-based instructions): Multiple approaches valid, context-dependent
- **Medium freedom** (pseudocode/scripts with params): Preferred pattern exists, some variation OK
- **Low freedom** (specific scripts, few params): Fragile operations, consistency critical

Narrow bridge = guardrails (low freedom). Open field = many routes (high freedom).

### 3. Progressive Disclosure (Three Levels)

1. **Metadata** (name + description) — Always in context (~100 words)
2. **SKILL.md body** — Loaded when skill triggers (<5k words, <500 lines)
3. **Bundled resources** — Loaded as needed (scripts, references, assets)

---

## Skill Anatomy

```
skill-name/
├── SKILL.md              # Required: frontmatter + instructions
├── scripts/              # Executable code (deterministic, reusable)
├── references/           # Docs loaded into context as needed
└── assets/               # Files used in output (templates, etc.)
```

### YAML Frontmatter (Required)

```yaml
---
name: skill-name
description: >
  What the skill does AND when to use it. This is the primary
  triggering mechanism — include all "when to use" info here,
  not in the body.
---
```

### Additional Frontmatter Fields (Claude Code)

| Field | Purpose |
|-------|---------|
| `argument-hint` | Hint shown during autocomplete |
| `disable-model-invocation` | `true` = user-only invocation (deploy, commit) |
| `user-invocable` | `false` = Claude-only (background knowledge) |
| `allowed-tools` | Tools Claude can use without permission |
| `model` | Model to use when skill is active |
| `context` | `fork` for subagent execution |
| `agent` | Subagent type when `context: fork` |
| `hooks` | Hooks scoped to skill lifecycle |

### String Substitutions

- `$ARGUMENTS` — Full argument string
- `$ARGUMENTS[N]` — Nth argument (0-indexed)
- `$N` — Shorthand for `$ARGUMENTS[N]`
- `${CLAUDE_SESSION_ID}` — Current session ID

### Dynamic Context Injection

`` !`command` `` syntax runs shell commands before skill content is sent to Claude.

---

## Where Skills Live (Priority Order)

1. **Enterprise** (managed settings) — all users in org
2. **Personal** (`~/.claude/skills/<name>/SKILL.md`) — all your projects
3. **Project** (`.claude/skills/<name>/SKILL.md`) — this project only
4. **Plugin** (`<plugin>/skills/<name>/SKILL.md`) — where plugin is enabled

Legacy location: `.claude/commands/<name>.md` still works.

---

## Progressive Disclosure Patterns

### Pattern 1: High-Level Guide + References

```markdown
# PDF Processing
## Quick start
[core example]
## Advanced features
- **Forms**: See references/forms.md
- **API ref**: See references/api.md
```

### Pattern 2: Domain-Specific Organization

```
bigquery-skill/
├── SKILL.md (overview + navigation)
└── references/
    ├── finance.md
    ├── sales.md
    └── product.md
```

### Pattern 3: Conditional Details

```markdown
# DOCX Processing
## Creating documents
Use docx-js. See references/docx-js.md.
## Editing documents
For simple edits, modify XML directly.
**For tracked changes**: See references/redlining.md
```

---

## What NOT to Include

- README.md, INSTALLATION_GUIDE.md, CHANGELOG.md
- Setup/testing procedures
- User-facing documentation
- Auxiliary context about the creation process

Only include what an AI agent needs to do the job.

---

## Workflow Patterns

### Sequential Workflows

Break operations into numbered phases with clear handoffs:

```markdown
## Workflow
1. **Analyze** — Examine the input, identify requirements
2. **Plan** — Create mappings/strategy
3. **Validate** — Verify plan before execution
4. **Execute** — Perform the operation
5. **Verify** — Check output matches expectations
```

### Conditional Workflows

Guide through decision points with branching:

```markdown
## Determine task type
- If creating new content → See "Creation Workflow"
- If editing existing content → See "Editing Workflow"
```

---

## Output Patterns

### Template Pattern

For strict requirements:
```markdown
ALWAYS use this exact structure:
# [Title]
## Executive summary
## Key findings
## Recommendations
```

For flexible guidance:
```markdown
Sensible default format — adapt as needed:
# [Title]
## Summary
## Findings (adapt sections to context)
## Recommendations
```

### Examples Pattern

Provide input/output pairs so Claude understands desired style:

```markdown
Input: Added user auth with JWT
Output: feat(auth): implement JWT-based authentication
```

---

## Key Takeaways for This Project

1. **Frontmatter description is the trigger** — put "when to use" there, not in the body
2. **Keep SKILL.md under 500 lines** — split to references/ when approaching
3. **References are loaded on demand** — they don't cost tokens until needed
4. **Scripts are most token-efficient** — executed without loading into context
5. **One level of reference depth** — all references link directly from SKILL.md
6. **Large references (>10k words)** — include grep patterns in SKILL.md

---

*Sources:*
- *[skill-creator/SKILL.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)*
- *[Claude Code Skills docs](https://code.claude.com/docs/en/skills)*
- *[skill-creator/references/workflows.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/references/workflows.md)*
- *[skill-creator/references/output-patterns.md](https://github.com/anthropics/skills/blob/main/skills/skill-creator/references/output-patterns.md)*
