# Monitor Auth Strategy — Chrome Token Management

> Reference document for the autonomous bookmark monitor pipeline.
> Documents how authentication works, failure modes, and recovery.

---

## Architecture Decision: Graceful Degradation (Option C)

The monitor uses **option (c)** from the planning phase: skip fetch on auth failure, still run analysis on existing data.

**Rationale:**
- The monitor is useful even without daily fetch (analyzes recently imported data)
- Chrome auth tokens expire unpredictably (hours to days)
- Fully automated token refresh requires keeping Chrome open + logged in
- Manual refresh is quick (visit x.com in Chrome) and needed infrequently

---

## Auth Flow

```
┌─────────────────────────────────────────────────────────────┐
│                     Daily Pipeline                           │
│                                                              │
│  ┌──────────────┐     ┌─────────────┐     ┌──────────────┐ │
│  │  Step 1:      │     │  Step 2:     │     │  Step 3+:    │ │
│  │  Fetch        │────>│  Enrichment  │────>│  Analysis    │ │
│  │  (needs auth) │     │  (needs API) │     │  (local)     │ │
│  └──────────────┘     └─────────────┘     └──────────────┘ │
│        │                                                      │
│        │ auth failed?                                         │
│        │                                                      │
│        ▼                                                      │
│   Skip fetch, log warning, continue with enrichment+analysis │
└─────────────────────────────────────────────────────────────┘
```

---

## Token Types

| Token | Source | Lifetime | Used For |
|-------|--------|----------|----------|
| Bearer token | Twitter OAuth | ~24hrs | GraphQL API calls |
| CSRF token | Twitter cookies | ~24hrs | Request headers |
| Session cookies | Chrome | Days-weeks | Maintaining auth |

Tokens are captured by intercepting network requests when Chrome navigates to x.com.

---

## Failure Modes

### 1. Auth tokens expired (most common)
- **Symptom:** Fetch returns 401/403
- **Recovery:** Open Chrome, navigate to x.com, tokens auto-refresh
- **Pipeline behavior:** Skips fetch, continues with analysis

### 2. Chrome not running
- **Symptom:** Cannot connect to Chrome debug port
- **Recovery:** Launch Chrome
- **Pipeline behavior:** Skips fetch, continues with analysis

### 3. Twitter account issues (rate limited, suspended)
- **Symptom:** Fetch returns 429 or other error
- **Recovery:** Wait for rate limit to clear (usually 15 min)
- **Pipeline behavior:** Skips fetch, continues with analysis

### 4. GOOGLE_API_KEY expired or missing
- **Symptom:** Enrichment scripts fail
- **Recovery:** Refresh API key at console.cloud.google.com
- **Pipeline behavior:** Skips enrichment, still runs analysis on existing data

---

## Token Refresh Workflow

### Automated (when Chrome is running):
1. Pipeline starts at 7:00 AM via cron
2. Attempts to capture auth from Chrome
3. If successful, fetches new bookmarks
4. If failed, logs warning and continues

### Manual (recommended after auth expiry):
1. Morning briefing notes "fetch failed — auth expired"
2. User opens Chrome, visits x.com
3. User runs: `python scripts/daily_monitor.py` (or waits for next cron)
4. Fresh tokens captured automatically

### Token Cache:
Auth tokens are cached in `.claude/auth_cache.json`:
```json
{
  "twitter": {
    "csrf_token": "...",
    "bearer_token": "...",
    "captured_at": "2026-02-10T12:00:00Z",
    "expires_at": "2026-02-11T12:00:00Z"
  }
}
```

The fetch step checks cache validity before attempting Chrome capture.

---

## Pipeline Without Fetch

Even when fetch is skipped, the pipeline provides value:

1. **Enrichment** — Processes any unenriched tweets already in the database
2. **Analysis** — Cross-references all recent tips against LEARNINGS.md and PROGRESS.md
3. **Briefing** — Generates morning report with whatever data is available
4. **Status** — Updates STATUS.json with pipeline run results

The `--skip-fetch` flag makes this explicit:
```bash
python scripts/daily_monitor.py --skip-fetch
```

---

## Future Improvements

When/if we want fully autonomous fetch:
- **Option A:** Use `pmset` to wake Mac, schedule Chrome launch before pipeline
- **Option B:** Explore headless Chrome with saved cookies (fragile with Twitter)
- **Option D:** Twitter API v2 with proper OAuth app tokens (requires developer account)

For now, option (c) with manual refresh is the pragmatic choice.

---

*Part of the autonomous bookmark monitor (Phase 7). See `plans/active/HANDOFF_autonomous-monitor.md`.*
