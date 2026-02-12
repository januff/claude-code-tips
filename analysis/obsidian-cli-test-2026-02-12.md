# Obsidian CLI Test Results — 2026-02-12

> Tester: Claude Code (Opus 4.6)

## Summary

**Obsidian CLI is NOT available.** The installed version (1.11.7) predates the CLI feature (requires 1.12+).

## Findings

| Check | Result |
|-------|--------|
| Installed version | **1.11.7** (runtime via self-update; bundled installer 1.10.6) |
| CLI in PATH? | No — `which obsidian` returns nothing |
| CLI wrapper? | None found in `/usr/local/bin/` or `/opt/homebrew/bin/` |
| `--version` flag? | Not recognized — launches full Electron app |
| `--help` flag? | Not recognized — launches full Electron app |
| URI scheme? | **Yes** — `obsidian://` is registered in `Info.plist` |

## Available Interface: URI Scheme

The `obsidian://` URI scheme works via `open` on macOS:

```bash
# Open a vault
open "obsidian://open?vault=Claude%20Code%20Tips"

# Open a specific note
open "obsidian://open?vault=Claude%20Code%20Tips&file=2025-12-28-claude-code-20"

# Search
open "obsidian://search?vault=Claude%20Code%20Tips&query=agent%20teams"
```

## Recommendations

1. **Update Obsidian to 1.12+** to get CLI support
2. In the meantime, use `obsidian://` URI scheme for basic automation (open vault/note after export)
3. Direct file manipulation of vault `.md` files remains the primary integration method

## Pipeline Integration Assessment

| Use Case | Feasible Now? | Notes |
|----------|---------------|-------|
| Post-export: auto-open vault | Yes (URI scheme) | `open "obsidian://open?vault=..."` |
| Post-export: open specific note | Yes (URI scheme) | `open "obsidian://open?vault=...&file=..."` |
| Trigger vault reindex | No | Requires CLI (1.12+) |
| Programmatic vault health checks | No | Requires CLI (1.12+) |
| Run Obsidian commands | No | Requires CLI (1.12+) |

## Action Items

- [ ] Update Obsidian to 1.12+ when convenient
- [ ] Re-test after update (re-run this assessment)
- [ ] Consider adding `--open` flag to `export_tips.py` using URI scheme (works now)
