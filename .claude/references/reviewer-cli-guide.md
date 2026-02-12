# Reviewer CLI Guide

Reference for the `/review` and `/review-plan` commands. These commands shell out to
a second AI model for independent review.

## Supported CLIs

| CLI | Model | Install | Invocation |
|-----|-------|---------|------------|
| `codex` | OpenAI Codex / GPT | `npm install -g @openai/codex` | `codex -q "<prompt>"` |
| `gemini` | Google Gemini | `npm install -g @anthropic-ai/gemini-cli` or via Google | `gemini -q "<prompt>"` |
| `opencode` | Various (configurable) | See [opencode repo](https://github.com/nicholasgriffintn/opencode) | `opencode -q "<prompt>"` |

## Detection Order

The review commands check for available CLIs in this order:

1. **User-specified** — second argument to the command overrides default
2. `codex` — default reviewer
3. `gemini` — first fallback
4. `opencode` — second fallback

If none are found, the review is skipped with a clear message (no error, no failure).

## CLI Invocation Pattern

All supported CLIs follow the same pattern:

```bash
<cli> -q "<prompt with content>"
```

The `-q` flag (quiet/query) sends a one-shot prompt and returns the response to stdout.
No interactive session is opened.

## Adding a New Reviewer CLI

To add support for another CLI:

1. Add it to the detection order in `/review` and `/review-plan`
2. Verify it supports a `-q` or equivalent one-shot flag
3. Add an entry to this table
4. Test with: `<new-cli> -q "Say hello"`

## Troubleshooting

**"REVIEW SKIPPED — No reviewer CLI found"**
- Install one of the CLIs listed above
- Ensure it's on your `$PATH`: `which codex`
- Some CLIs require API keys in environment variables (e.g., `OPENAI_API_KEY`)

**Reviewer returns an error**
- Check API key is set and valid
- Check network connectivity
- The review commands will display the error output — read it for details

**Review is too long / too short**
- The review prompt asks for specificity — reviewers may vary in verbosity
- Edit the prompt in the command file to adjust (e.g., add "limit to 500 words")
