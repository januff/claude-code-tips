# Claude-in-Chrome Connection Bug Report

## Title

Claude-in-Chrome `tabs_context_mcp` fails to connect in scheduled/headless sessions — requires repeated Chrome restarts with no reliable fix

## Environment

- **Claude Code:** 2.1.73
- **Chrome:** 146.0.7680.71
- **macOS:** Darwin 23.6.0 (Sonoma)
- **Chrome extension:** Claude in Chrome v1.0.52
- **Context:** Both Claude Desktop app and terminal (`claude` CLI)

## Summary

When Claude Code's scheduled tasks (or new interactive sessions) attempt to connect to Chrome via `tabs_context_mcp`, the connection frequently fails with a "Check your Claude in Chrome account" dialog. The user must manually restart Chrome — often 3-5 times — to re-establish the connection. This is especially disruptive because:

1. Restarting Chrome closes all open tabs, windows, and authenticated sessions
2. On macOS, Chrome is typically the most resource-intensive and state-heavy application
3. The fix is unreliable — sometimes 3+ restarts still don't resolve it
4. Scheduled tasks cannot prompt for user intervention, so they must skip entirely

## Reproduction Steps

1. Run a Claude Code session that uses Claude-in-Chrome (e.g., browser automation to extract data from a website)
2. End the session normally
3. Start a new Claude Code session (or let a scheduled task fire)
4. Call `mcp__Claude_in_Chrome__tabs_context_mcp` with `createIfEmpty: true`
5. **Expected:** Returns tab data, connection established
6. **Actual:** "Claude in Chrome is not connected" error, or the macOS "Check your Claude in Chrome account" dialog appears

### Variant: "Connected but stuck" loop

1. After Chrome restart, `tabs_context_mcp` reports the connection is established
2. But it never returns tab data
3. Subsequent calls enter a "just connected, retry" loop indefinitely
4. Additional Chrome restarts may or may not resolve this

## Frequency

Observed in ~50% of new sessions when a prior session used Chrome. In a 10-day period tracking 3 scheduled tasks per day (30 total runs):

| Date | claude-code-tips | book-queue | hall-of-fake |
|------|-----------------|------------|--------------|
| 2026-03-09 | SKIP (Chrome not connected) | n/a (not scheduled yet) | n/a |
| 2026-03-09 | SUCCESS (after manual Chrome restart by user mid-session) | n/a | n/a |
| 2026-03-10 | SUCCESS | SUCCESS | n/a |
| 2026-03-11 | SKIP (Chrome not connected) | SKIP (Chrome not connected) | SKIP (Chrome not connected) |

The 3/10 successes were during an interactive session where the user was present to manually restart Chrome. The 3/11 failures were all scheduled tasks running without user intervention.

## Key Observations

1. **Stale connection locks:** The extension appears to retain a connection lock from the previous session. Closing all Claude Code terminal windows and the desktop app does not release it.

2. **Not an auth/account issue:** The extension is signed in, permissions are correct, and the account matches. The dialog's suggestion to "check your account" is misleading.

3. **Tab group borders persist:** After a Claude-in-Chrome session ends, the colored tab group borders remain visible in Chrome. These are cosmetic, but they suggest the extension's session state isn't fully cleaned up.

4. **Affects both terminal and desktop app:** The bug occurs regardless of whether Claude Code is run from the terminal CLI or the desktop application.

5. **No programmatic workaround:** There is no API to reset the extension connection, clear the lock, or force a reconnect without restarting Chrome.

## Impact

This bug makes Claude-in-Chrome unusable for automated/scheduled workflows. Any task that depends on browser automation (authenticated web scraping, bookmark extraction, page interaction) cannot run reliably without human intervention.

We have 3 daily scheduled tasks across 3 projects that all depend on Chrome, and they fail silently when this bug occurs.

## Desired Behavior

1. **Connection should auto-recover** between sessions without Chrome restarts
2. **Stale locks should time out** — if a Claude Code session exits, the extension should release the connection within seconds
3. **`tabs_context_mcp` should fail fast** with a clear error rather than entering the retry loop
4. **Ideally:** A programmatic reconnect mechanism (e.g., a `force_reconnect` parameter on `tabs_context_mcp`, or a separate `reconnect` tool)

## Workaround

For scheduled tasks: detect the connection failure, log it, and skip. Do not attempt to restart Chrome programmatically — this causes more disruption than value.

For interactive sessions: manually restart Chrome (may require 1-3 attempts).
