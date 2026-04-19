#!/usr/bin/env python3
"""Build the enriched infographic HTML with data from the SQLite database."""

import json
import html

def esc(s):
    """Escape for safe HTML embedding."""
    if not s:
        return ''
    return html.escape(str(s)).replace('\n', '<br>')

def esc_js(s):
    """Escape for safe JS string embedding."""
    if not s:
        return ''
    return str(s).replace('\\', '\\\\').replace("'", "\\'").replace('"', '\\"').replace('\n', '\\n').replace('\r', '')

def truncate(s, n=280):
    if not s or len(s) <= n:
        return s or ''
    return s[:n] + '…'

# Load data
with open('data/categories_rich.json') as f:
    categories = json.load(f)
with open('data/voices_rich.json') as f:
    voices_raw = json.load(f)
# Deduplicate: strip @ prefix, merge team+community entries, prefer team
seen = {}
for v in voices_raw:
    h = v['handle'].lstrip('@')
    v['handle'] = h
    if h in seen:
        # Prefer team entry; merge bookmarks if both exist
        if v.get('is_team') and not seen[h].get('is_team'):
            v['bookmarks'] = max(v['bookmarks'], seen[h]['bookmarks'])
            seen[h] = v
        elif not v.get('is_team') and seen[h].get('is_team'):
            seen[h]['bookmarks'] = max(v['bookmarks'], seen[h]['bookmarks'])
        # else skip duplicate
    else:
        seen[h] = v
voices = list(seen.values())
with open('data/principles_rich.json') as f:
    principles = json.load(f)
with open('data/pipeline.json') as f:
    pipeline = json.load(f)
with open('data/vitals.json') as f:
    vitals = json.load(f)

# Category analysis — why they're grouped together
category_analysis = {
    'tooling': 'The largest cluster by far — tooling tips track the expanding surface area of Claude Code itself. From Dispatch and Cowork to git worktrees and the AskUserQuestionTool, this category captures the features that change how developers physically interact with Claude. High engagement here reflects the community\'s hunger for capability updates.',
    'skills': 'Skills (slash commands in .claude/commands/) are Claude Code\'s extensibility layer. This category tracks the ecosystem of community-built and official skills — from Remotion video generation to /simplify and /batch. The skill-creator-that-creates-skills pattern shows the community reaching for meta-level tooling.',
    'meta': 'The "meta" category captures reflection about Claude Code itself: adoption stories, setup guides, usage philosophy. Boris Cherny\'s vanilla-setup thread (45K+ likes) anchors this — it\'s less about specific techniques and more about how to think about the tool. High engagement suggests people need framing, not just features.',
    'context-management': 'Context management is the craft of keeping Claude\'s working memory useful across long sessions. /btw, auto-memory, state.md, compaction strategies — these tips address the fundamental constraint that context windows are finite and attention degrades. This is where the most sophisticated users differentiate themselves.',
    'subagents': 'Subagents represent Claude Code\'s distributed computing model — spinning up child agents for parallel work. From "Chief of Staff" patterns to agent swarms, this category tracks the evolution from single-agent to multi-agent workflows. The agent-teams feature (research preview) formalized what the community was already doing.',
    'prompting': 'Prompting tips focus on the input side: how to structure requests, when to be specific vs. abstract, and patterns like prompt-stashing for reuse. This is the most transferable category — techniques here work across AI tools, not just Claude Code.',
    'automation': 'Automation tips push Claude Code beyond interactive use into scheduled, recurring, and unattended workflows. /loop, Cowork, browser automation via --chrome — these represent the frontier of "set it and forget it" AI assistance. The reliability challenges here are real (our own bookmark fetching is manual for this reason).',
    'security': 'Security tips navigate the tension between power and safety. --dangerously-skip-permissions exists because some workflows need full autonomy, but /sandbox and allow-ask-deny show the community developing more nuanced permission models. This category is small but critical.',
    'workflow': 'Workflow tips describe end-to-end patterns: how to organize a session, when to use Plan Mode, how to structure multi-day projects. The Ralph Wiggum Loop (auto-restore across compaction) is the signature pattern here — it turned a limitation into a feature.',
    'hooks': 'Hooks are Claude Code\'s event system — code that runs before/after tool calls, on compaction, etc. This small category has outsized impact: pre-auto-compact hooks preserve context, PostToolUse hooks catch formatting issues. Boris calls this "the last 10%."',
    'commands': 'Built-in slash commands like /model, /compact, /insights. A small but essential category — these are the native primitives that skills and hooks build on top of.',
    'planning': 'Planning tips focus on the think-before-you-code pattern: Plan Mode (Shift+Tab), planning-with-files, and the co-founder master plan approach. The insight is that AI coding benefits from the same discipline human coding does — architecture before implementation.',
    'mcp': 'Model Context Protocol servers extend Claude Code\'s reach into external tools — databases, APIs, browsers. The "claude mcp add" command is the entry point. This category is small because MCP is infrastructure, not a daily-use feature, but it underpins much of the automation category.',
    'plugins': 'The newest and smallest category — local plugins that sync between desktop and CLI. This represents Claude Code\'s plugin architecture evolving toward a proper extension system.'
}

# Status enrichment
status_details = {
    'Enrichment Pipeline': {
        'color': 'green',
        'summary': 'Working. Keywords, summaries, link resolution, Gemini analysis.',
        'detail': 'Every bookmarked tweet goes through a multi-stage pipeline: keyword extraction, one-line summary, holistic summary (via Gemini), link resolution (t.co → final URL), and content fetch for linked pages. The analyze_new_tips.py script runs LLM classification on batches. ~95% of tweets are fully enriched within one session of the pipeline running.'
    },
    'Obsidian Export': {
        'color': 'green',
        'summary': 'Working. 552 quality-filtered notes with semantic filenames.',
        'detail': 'Quality filter: only tweets with likes > 0 OR holistic_summary present get exported. Filenames use LLM-generated primary_keyword for browsability (e.g., "2026-01-15-git-worktree.md" not "2026-01-15-1881234567890.md"). Attachment-only tweets get vision analysis. The vault includes dataview dashboards for browsing by category, author, and engagement.'
    },
    'Bookmark Fetching': {
        'color': 'yellow',
        'summary': 'Manual ~2×/week. Scheduled tasks tried and disabled.',
        'detail': 'Fetching requires browser automation (Twitter/X blocks headless access). Desktop scheduled tasks were tried March 9–16 but disabled due to: tasks not auto-executing, permission settings reverting between sessions, and Chrome connection reliability issues. Current process: manual terminal session with copy-paste prompt from FETCH_PROMPT.md. Takes ~5 minutes per fetch, yields 5–20 new tweets.'
    },
    'Weekly Digest': {
        'color': 'red',
        'summary': 'Aspirational. Not yet automated.',
        'detail': 'The vision: a weekly summary of new tips, trending topics, and pipeline events, auto-generated and possibly posted. The what\'s_new.py script exists and works for ad-hoc reporting, but there\'s no scheduled trigger or distribution mechanism. Blocked on the same reliability issues as bookmark fetching — needs a stable cron-like execution environment.'
    }
}

# Build voice profiles with analytical context
team_context = {
    'bcherny': 'Boris Cherny created Claude Code. His January 2, 2026 thread (45,567 likes) became the founding document of the community — a simple setup guide that taught people to start vanilla and customize. He ships 10–30 PRs daily without editing code by hand. His philosophy: the tool should be simple enough that you don\'t need a guide, but the community builds one anyway.',
    'trq212': 'Thariq is the most prolific feature announcer on the team, with the highest bookmark count (10). He introduced /btw, Plan Mode, auto-memory, Quick Mode, and AskUserQuestionTool — each one addressing a specific community pain point. His tweets are characteristically concise: feature name, what it does, ship it.',
    'lydiahallie': 'Lydia Hallie focuses on the extensibility layer: agent teams, local plugins, context:fork for skill isolation, and --dangerously-skip-permissions. Her contributions map the boundary between power and safety — how to give Claude more autonomy without losing control.',
    'felixrieseberg': 'Felix Rieseberg shipped Dispatch and Cowork — the features that push Claude Code beyond the terminal into persistent, cross-device workflows. Dispatch alone (17K likes) represents the biggest engagement spike for a single feature announcement in our dataset.',
    'alexalbert__': 'Alex Albert (CEO of Anthropic\'s developer relations) appears less frequently in our bookmarks but his "underrated trick" framing is influential — he highlights features that exist but aren\'t widely known, serving as a signal booster for the team\'s own product.'
}

community_context = {
    'jarrodwatts': 'Prolific community builder. Created Claude HUD, Claude Delegator, and documents his workflows in detail. His tips tend toward complete systems rather than isolated tricks.',
    'nummanali': 'Power user focused on agent orchestration: agent-swarms, cc-mirror, status-line customization. Represents the "run many Claudes at once" school of thought.',
    'kepano': 'Creator of Obsidian. His tips naturally focus on Obsidian integration with Claude Code — a direct bridge between our two primary tools.',
    'mattpocockuk': 'Matt Pocock (TypeScript educator) brings the "keep it simple" philosophy. His docker sandbox tip and KISS prompting approach counterbalance the community\'s tendency toward complexity.',
    'alexhillman': 'Focuses on meta-patterns: AI slop detection, date-time context injection, the Smaug pattern. His tips are about discipline and quality control rather than features.',
    'adocomplete': 'Security-conscious contributor. /sandbox, allow-ask-deny permission models, prompt-stashing — his tips navigate the safety/power tradeoff.',
    'frankdegods': 'High-engagement contributor known for bold automation: automatic subscription cancellation and agent-sdk experiments. Represents the "push the boundary" community.',
    'ericbuess': 'Workflow architect. Frictionless context management, Ralph Wiggum loops, native install methods — he documents the complete session lifecycle.',
}

# Build the HTML
html_parts = []

html_parts.append('''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Claude Code Tips — Community Intelligence</title>
<style>
  :root {
    --bg: #1a1a2e;
    --bg-card: #232340;
    --bg-card-hover: #2a2a50;
    --bg-panel: #1e1e38;
    --terracotta: #e07a5f;
    --cream: #f2cc8f;
    --sage: #81b29a;
    --slate: #3d405b;
    --text: #e8e0d8;
    --text-muted: #9a938b;
    --text-dim: #6b6560;
    --coral: #f4845f;
    --peach: #f0a868;
  }

  * { margin: 0; padding: 0; box-sizing: border-box; }
  html { scroll-behavior: smooth; }

  body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif;
    background: var(--bg);
    color: var(--text);
    line-height: 1.6;
    overflow-x: hidden;
  }

  section {
    min-height: 100vh;
    padding: 80px 24px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transform: translateY(40px);
    transition: opacity 0.8s ease, transform 0.8s ease;
  }
  section.visible { opacity: 1; transform: translateY(0); }

  .section-inner { max-width: 1060px; width: 100%; }

  h2 {
    font-size: clamp(1.6rem, 4vw, 2.4rem);
    font-weight: 700;
    color: var(--cream);
    margin-bottom: 8px;
    letter-spacing: -0.02em;
  }
  .section-subtitle {
    font-size: 1rem;
    color: var(--text-muted);
    margin-bottom: 48px;
  }

  /* NAV */
  nav {
    position: fixed; top: 0; left: 0; right: 0; z-index: 100;
    background: rgba(26, 26, 46, 0.88);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid rgba(242, 204, 143, 0.08);
    padding: 0 24px;
    display: flex; justify-content: center; gap: 28px;
    height: 48px; align-items: center;
    opacity: 0; transition: opacity 0.4s;
  }
  nav.show { opacity: 1; }
  nav a {
    color: var(--text-muted); text-decoration: none;
    font-size: 0.8rem; font-weight: 500;
    letter-spacing: 0.06em; text-transform: uppercase;
    transition: color 0.2s;
  }
  nav a:hover, nav a.active { color: var(--terracotta); }

  /* HERO */
  #hero {
    min-height: 100vh; text-align: center;
    background: radial-gradient(ellipse at 50% 30%, rgba(224,122,95,0.08) 0%, transparent 60%);
  }
  #hero .logo {
    font-size: clamp(2.4rem, 7vw, 4.2rem);
    font-weight: 800; letter-spacing: -0.03em;
    background: linear-gradient(135deg, var(--cream) 0%, var(--terracotta) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
    margin-bottom: 12px;
  }
  #hero .tagline {
    font-size: clamp(1rem, 2.5vw, 1.3rem);
    color: var(--text-muted); max-width: 560px;
    margin: 0 auto 56px;
  }
  .stats-row { display: flex; justify-content: center; gap: 40px; flex-wrap: wrap; }
  .stat-item { text-align: center; }
  .stat-num {
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 800; color: var(--terracotta);
    font-variant-numeric: tabular-nums; line-height: 1.1;
  }
  .stat-label {
    font-size: 0.78rem; color: var(--text-muted);
    text-transform: uppercase; letter-spacing: 0.08em; margin-top: 4px;
  }

  /* PIPELINE */
  .timeline { position: relative; padding-left: 36px; }
  .timeline::before {
    content: ''; position: absolute; left: 14px; top: 0; bottom: 0;
    width: 2px;
    background: linear-gradient(to bottom, var(--terracotta), var(--sage));
  }
  .tl-event { position: relative; margin-bottom: 36px; cursor: pointer; }
  .tl-dot {
    position: absolute; left: -29px; top: 6px;
    width: 12px; height: 12px;
    background: var(--terracotta); border-radius: 50%;
    border: 2px solid var(--bg);
    transition: transform 0.3s, background 0.3s;
  }
  .tl-event:hover .tl-dot { transform: scale(1.4); background: var(--cream); }
  .tl-event h3 { font-size: 1.1rem; font-weight: 600; margin-bottom: 4px; }
  .tl-gap {
    display: inline-block; font-size: 0.75rem; font-weight: 600;
    background: rgba(224,122,95,0.15); color: var(--terracotta);
    padding: 2px 10px; border-radius: 12px; margin-left: 8px;
  }
  .tl-gap.convergence { background: rgba(129,178,154,0.15); color: var(--sage); }
  .tl-signals { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 12px; font-size: 0.85rem; }
  .tl-sig { background: var(--bg-card); border-radius: 8px; padding: 12px 14px; border-left: 3px solid var(--terracotta); }
  .tl-sig.ship { border-left-color: var(--sage); }
  .tl-sig-label { font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--text-muted); margin-bottom: 4px; }
  .tl-detail {
    max-height: 0; overflow: hidden; transition: max-height 0.5s ease;
    font-size: 0.85rem; color: var(--text-muted); margin-top: 8px; line-height: 1.5;
  }
  .tl-event.open .tl-detail { max-height: 200px; }

  /* TREEMAP */
  .treemap { display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 4px; width: 100%; }
  .tm-cell {
    border-radius: 6px; padding: 14px 12px; cursor: pointer;
    transition: transform 0.2s, box-shadow 0.2s;
    position: relative; overflow: hidden;
    display: flex; flex-direction: column; justify-content: space-between;
    min-height: 80px;
  }
  .tm-cell:hover { transform: translateY(-2px); box-shadow: 0 8px 24px rgba(0,0,0,0.3); z-index: 2; }
  .tm-cell.selected { outline: 2px solid var(--cream); outline-offset: -2px; }
  .tm-name { font-size: 0.78rem; font-weight: 600; text-transform: capitalize; color: rgba(255,255,255,0.9); }
  .tm-count { font-size: 1.4rem; font-weight: 800; color: rgba(255,255,255,0.95); }

  /* EXPANDED PANELS (shared) */
  .expand-panel {
    display: none; background: var(--bg-panel);
    border-radius: 12px; padding: 32px;
    margin-top: 20px; border: 1px solid rgba(242,204,143,0.08);
    max-height: 80vh; overflow-y: auto;
  }
  .expand-panel.active { display: block; animation: panelIn 0.3s ease; }
  @keyframes panelIn { from { opacity: 0; transform: translateY(8px); } to { opacity: 1; transform: translateY(0); } }
  .expand-panel h3 { font-size: 1.2rem; color: var(--cream); margin-bottom: 6px; text-transform: capitalize; }
  .expand-panel .panel-meta { font-size: 0.82rem; color: var(--text-muted); margin-bottom: 16px; }
  .panel-close {
    float: right; background: none; border: none; color: var(--text-muted);
    font-size: 1.2rem; cursor: pointer; padding: 4px 8px;
  }
  .panel-close:hover { color: var(--cream); }

  /* ANALYSIS BLOCK */
  .analysis {
    background: rgba(224,122,95,0.06); border-left: 3px solid var(--terracotta);
    border-radius: 0 8px 8px 0; padding: 16px 20px;
    margin-bottom: 20px; font-size: 0.88rem; line-height: 1.6;
    color: var(--text);
  }
  .analysis-label {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.08em;
    color: var(--terracotta); margin-bottom: 6px; font-weight: 600;
  }

  /* QUOTE CARD */
  .quote-card {
    background: var(--bg-card); border-radius: 10px; padding: 18px 20px;
    margin-bottom: 12px; border: 1px solid rgba(255,255,255,0.04);
    transition: border-color 0.2s;
  }
  .quote-card:hover { border-color: rgba(242,204,143,0.12); }
  .quote-header {
    display: flex; justify-content: space-between; align-items: center;
    margin-bottom: 8px;
  }
  .quote-author { font-size: 0.82rem; font-weight: 600; color: var(--cream); }
  .quote-likes { font-size: 0.72rem; color: var(--terracotta); }
  .quote-text { font-size: 0.85rem; color: var(--text); line-height: 1.55; margin-bottom: 8px; }
  .quote-summary { font-size: 0.78rem; color: var(--sage); font-style: italic; }

  /* CONSTELLATION */
  .constellation-wrap { width: 100%; max-width: 700px; margin: 0 auto; }
  .constellation-wrap svg { width: 100%; height: auto; }

  /* VOICE PANEL */
  .voice-panel-header { display: flex; gap: 20px; align-items: flex-start; margin-bottom: 20px; }
  .voice-avatar {
    width: 64px; height: 64px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.6rem; font-weight: 800; flex-shrink: 0;
  }
  .voice-avatar.team { background: var(--terracotta); color: var(--bg); }
  .voice-avatar.community { background: var(--sage); color: var(--bg); }
  .voice-handle { font-size: 1.3rem; font-weight: 700; color: var(--cream); }
  .voice-role { font-size: 0.82rem; color: var(--terracotta); font-weight: 600; margin-bottom: 4px; }
  .voice-stats { font-size: 0.78rem; color: var(--text-muted); }
  .voice-cats { display: flex; gap: 6px; margin-top: 8px; flex-wrap: wrap; }
  .voice-cat {
    font-size: 0.68rem; background: rgba(129,178,154,0.12); color: var(--sage);
    padding: 3px 10px; border-radius: 10px;
  }

  /* PRINCIPLES */
  .principles-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; }
  .principle-card {
    background: var(--bg-card); border-radius: 12px; padding: 28px 24px;
    border-top: 3px solid var(--terracotta);
    transition: transform 0.3s; cursor: pointer;
  }
  .principle-card:nth-child(2) { border-top-color: var(--cream); }
  .principle-card:nth-child(3) { border-top-color: var(--sage); }
  .principle-card:nth-child(4) { border-top-color: var(--coral); }
  .principle-card:hover { transform: translateY(-4px); }
  .principle-card.selected { outline: 2px solid var(--cream); outline-offset: -2px; }
  .principle-icon { font-size: 1.8rem; margin-bottom: 12px; display: block; }
  .principle-card h3 { font-size: 1rem; font-weight: 700; margin-bottom: 8px; }
  .principle-card p { font-size: 0.82rem; color: var(--text-muted); line-height: 1.5; }

  /* STATUS */
  .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 16px; }
  .status-card {
    background: var(--bg-card); border-radius: 10px; padding: 20px;
    cursor: pointer; transition: transform 0.2s;
  }
  .status-card:hover { transform: translateY(-2px); }
  .status-card.selected { outline: 2px solid var(--cream); outline-offset: -2px; }
  .status-header { display: flex; gap: 14px; align-items: flex-start; }
  .status-light {
    width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; margin-top: 4px;
  }
  .status-light.green { background: #81b29a; box-shadow: 0 0 8px rgba(129,178,154,0.4); }
  .status-light.yellow { background: #f2cc8f; box-shadow: 0 0 8px rgba(242,204,143,0.4); }
  .status-light.red { background: #e07a5f; box-shadow: 0 0 8px rgba(224,122,95,0.4); }
  .status-card h4 { font-size: 0.9rem; font-weight: 600; margin-bottom: 4px; }
  .status-card p { font-size: 0.78rem; color: var(--text-muted); line-height: 1.4; }

  /* KEYWORD CHIPS */
  .keyword-chips { display: flex; flex-wrap: wrap; gap: 6px; margin: 12px 0; }
  .keyword-chip {
    font-size: 0.72rem; background: rgba(224,122,95,0.12); color: var(--terracotta);
    padding: 4px 10px; border-radius: 12px; white-space: nowrap;
  }

  /* TOOLTIP */
  .voice-tooltip {
    position: fixed; background: var(--bg-card);
    border: 1px solid rgba(242,204,143,0.15);
    border-radius: 8px; padding: 12px 16px; font-size: 0.82rem;
    pointer-events: none; opacity: 0; transition: opacity 0.2s;
    z-index: 200; max-width: 260px; box-shadow: 0 8px 32px rgba(0,0,0,0.4);
  }
  .voice-tooltip.show { opacity: 1; }
  .vt-name { font-weight: 700; color: var(--cream); margin-bottom: 4px; }
  .vt-stat { color: var(--text-muted); font-size: 0.75rem; }
  .vt-topics { color: var(--terracotta); font-size: 0.72rem; margin-top: 6px; }
  .vt-hint { color: var(--sage); font-size: 0.68rem; margin-top: 4px; font-style: italic; }

  footer {
    text-align: center; padding: 48px 24px;
    font-size: 0.75rem; color: var(--text-dim);
    border-top: 1px solid rgba(255,255,255,0.04);
  }
  footer a { color: var(--terracotta); text-decoration: none; }

  @media (max-width: 640px) {
    section { padding: 60px 16px; }
    .stats-row { gap: 24px; }
    .tl-signals { grid-template-columns: 1fr; }
    nav { gap: 14px; font-size: 0.7rem; }
    .expand-panel { padding: 20px; }
  }
</style>
</head>
<body>

<nav id="nav">
  <a href="#hero">Home</a>
  <a href="#pipeline">Pipeline</a>
  <a href="#categories">Categories</a>
  <a href="#voices">Voices</a>
  <a href="#principles">Principles</a>
  <a href="#status">Status</a>
</nav>

<div class="voice-tooltip" id="tooltip"></div>
''')

# === HERO ===
html_parts.append('''
<section id="hero" class="visible">
  <div class="logo">Claude Code Tips</div>
  <p class="tagline">87 days of community intelligence — tracking how Claude Code users teach each other (and Anthropic) what works.</p>
  <div class="stats-row">
    <div class="stat-item"><div class="stat-num" data-target="206">0</div><div class="stat-label">Curated Tips</div></div>
    <div class="stat-item"><div class="stat-num" data-target="87">0</div><div class="stat-label">Days Tracked</div></div>
    <div class="stat-item"><div class="stat-num" data-target="140">0</div><div class="stat-label">Unique Voices</div></div>
    <div class="stat-item"><div class="stat-num" data-target="14">0</div><div class="stat-label">Categories</div></div>
  </div>
</section>
''')

# === PIPELINE ===
events = pipeline['events']
html_parts.append('''
<section id="pipeline">
  <div class="section-inner">
    <h2>The Tips-to-Tool Pipeline</h2>
    <p class="section-subtitle">Community hacks become native features in ~4–6 weeks. Click any event for the full story.</p>
    <div class="timeline">
''')

for ev in events:
    gap_weeks = ev['gap_weeks']
    is_converge = gap_weeks < 0
    gap_label = 'convergence' if is_converge else f"{gap_weeks} weeks"
    gap_class = 'convergence' if is_converge else ''
    html_parts.append(f'''
      <div class="tl-event" onclick="this.classList.toggle('open')">
        <div class="tl-dot"></div>
        <h3>{esc(ev['name'])} <span class="tl-gap {gap_class}">{gap_label}</span></h3>
        <div class="tl-signals">
          <div class="tl-sig">
            <div class="tl-sig-label">Community Signal — {esc(ev['community_date'])}</div>
            {esc(ev['community_signal'])}
          </div>
          <div class="tl-sig ship">
            <div class="tl-sig-label">Shipped — {esc(ev['ship_date'])}</div>
            {esc(ev['ship_signal'])}
          </div>
        </div>
        <div class="tl-detail"><p>{esc(ev['notes'])}</p></div>
      </div>
    ''')

html_parts.append('</div></div></section>')

# === CATEGORIES ===
colors = ['#e07a5f','#f2cc8f','#81b29a','#f4845f','#f0a868',
          '#b8a9c9','#88b7d5','#d4a574','#a8c686','#e8918f',
          '#c4b5a0','#96c8c8','#d4a0c0','#b0c4a8']

html_parts.append('''
<section id="categories">
  <div class="section-inner">
    <h2>What 206 Tips Actually Cover</h2>
    <p class="section-subtitle">Click a category to see why these tips belong together, with full quotes from the community.</p>
    <div class="treemap">
''')

max_count = max(c['count'] for c in categories)
for i, cat in enumerate(categories):
    name = cat['category']
    span = max(1, round((cat['count'] / max_count) * 3))
    color = colors[i % len(colors)]
    html_parts.append(f'''
      <div class="tm-cell" style="grid-column:span {span}; background:{color}"
           onclick="showCategory('{esc_js(name)}')" id="tm-{name.replace(' ','-')}">
        <div class="tm-name">{esc(name)}</div>
        <div class="tm-count">{cat['count']}</div>
      </div>
    ''')

html_parts.append('</div><div class="expand-panel" id="cat-panel"></div></div></section>')

# === VOICES ===
html_parts.append('''
<section id="voices">
  <div class="section-inner" style="text-align:center">
    <h2>The Voices</h2>
    <p class="section-subtitle">Team members (inner, terracotta) and top community contributors (outer, sage). Size = bookmarks. Click any node for a full profile.</p>
    <div class="constellation-wrap" id="constellation"></div>
    <div class="expand-panel" id="voice-panel" style="text-align:left"></div>
  </div>
</section>
''')

# === PRINCIPLES ===
icons = ['&#9713;', '&#9201;', '&#9878;', '&#8635;']
html_parts.append('''
<section id="principles">
  <div class="section-inner">
    <h2>Four Principles</h2>
    <p class="section-subtitle">How this project decides what to adopt and when. Click a principle to see it in action.</p>
    <div class="principles-grid">
''')

for i, p in enumerate(principles):
    html_parts.append(f'''
      <div class="principle-card" onclick="showPrinciple({i})" id="pc-{i}">
        <span class="principle-icon">{icons[i]}</span>
        <h3>{esc(p['principle'])}</h3>
        <p>{esc(p['description'])}</p>
      </div>
    ''')

html_parts.append('</div><div class="expand-panel" id="principle-panel"></div></div></section>')

# === STATUS ===
html_parts.append('''
<section id="status">
  <div class="section-inner">
    <h2>Project Status</h2>
    <p class="section-subtitle">An honest look at what works, what's manual, and what's aspirational. Click for details.</p>
    <div class="status-grid">
''')

for name, s in status_details.items():
    html_parts.append(f'''
      <div class="status-card" onclick="showStatus('{esc_js(name)}')">
        <div class="status-header">
          <div class="status-light {s['color']}"></div>
          <div><h4>{esc(name)}</h4><p>{esc(s['summary'])}</p></div>
        </div>
      </div>
    ''')

html_parts.append('</div><div class="expand-panel" id="status-panel"></div></div></section>')

# === FOOTER ===
html_parts.append('''
<footer>
  Built by Claude Code — an infographic about Claude, made by Claude.<br>
  <a href="https://github.com/joeyanuff/claude-code-tips">github.com/joeyanuff/claude-code-tips</a>
</footer>
''')

# === JAVASCRIPT ===
html_parts.append('<script>\n')

# Embed data as JS objects
html_parts.append('// === EMBEDDED DATA ===\n')
html_parts.append(f'const categoriesData = {json.dumps({c["category"]: c for c in categories}, ensure_ascii=False)};\n')
html_parts.append(f'const categoryAnalysis = {json.dumps(category_analysis, ensure_ascii=False)};\n')

# Build voice data with context
voice_data = {}
for v in voices:
    handle = v['handle'].lstrip('@')
    ctx = team_context.get(handle, '') or community_context.get(handle, '')
    voice_data[handle] = {
        'handle': handle,
        'display_name': v['display_name'],
        'is_team': v.get('is_team', False),
        'bookmarks': v['bookmarks'],
        'total_likes': v['total_likes'],
        'avg_likes': round(v['avg_likes']),
        'top_categories': v.get('top_categories', []),
        'top_tweets': v.get('top_tweets', [])[:5],
        'context': ctx
    }
html_parts.append(f'const voiceData = {json.dumps(voice_data, ensure_ascii=False)};\n')
html_parts.append(f'const principlesData = {json.dumps(principles, ensure_ascii=False)};\n')
html_parts.append(f'const statusDetails = {json.dumps(status_details, ensure_ascii=False)};\n')

html_parts.append('''
// === COUNTER ANIMATION ===
function animateCounters() {
  document.querySelectorAll('.stat-num[data-target]').forEach(el => {
    const target = +el.dataset.target;
    const duration = 1600;
    const start = performance.now();
    function tick(now) {
      const t = Math.min((now - start) / duration, 1);
      const ease = 1 - Math.pow(1 - t, 3);
      el.textContent = Math.round(ease * target);
      if (t < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  });
}

// === INTERSECTION OBSERVER ===
let heroAnimated = false;
const obs = new IntersectionObserver((entries) => {
  entries.forEach(e => {
    if (e.isIntersecting) {
      e.target.classList.add('visible');
      if (e.target.id === 'hero' && !heroAnimated) { animateCounters(); heroAnimated = true; }
      document.querySelectorAll('nav a').forEach(a => a.classList.remove('active'));
      const link = document.querySelector(`nav a[href="#${e.target.id}"]`);
      if (link) link.classList.add('active');
    }
  });
}, { threshold: 0.2 });
document.querySelectorAll('section').forEach(s => obs.observe(s));

window.addEventListener('scroll', () => {
  document.getElementById('nav').classList.toggle('show', window.scrollY > 300);
}, { passive: true });

// === HELPER: escape HTML ===
function escHTML(s) {
  const d = document.createElement('div');
  d.textContent = s || '';
  return d.innerHTML;
}
function nl2br(s) { return escHTML(s).replace(/\\n/g, '<br>'); }

// === SHOW CATEGORY ===
function showCategory(name) {
  const cat = categoriesData[name];
  const analysis = categoryAnalysis[name] || '';
  const panel = document.getElementById('cat-panel');

  // Highlight selected
  document.querySelectorAll('.tm-cell').forEach(c => c.classList.remove('selected'));
  const cell = document.getElementById('tm-' + name.replace(/ /g, '-'));
  if (cell) cell.classList.add('selected');

  const likes = cat.total_likes >= 1000 ? (cat.total_likes / 1000).toFixed(0) + 'K' : cat.total_likes;

  let html = `<button class="panel-close" onclick="this.parentElement.classList.remove('active')">&times;</button>`;
  html += `<h3>${escHTML(name)}</h3>`;
  html += `<div class="panel-meta">${cat.count} tips &middot; ${likes} total likes</div>`;

  if (analysis) {
    html += `<div class="analysis"><div class="analysis-label">Why these belong together</div>${escHTML(analysis)}</div>`;
  }

  if (cat.top_tweets && cat.top_tweets.length > 0) {
    html += `<h4 style="color:var(--text-muted);font-size:0.82rem;margin:16px 0 12px;text-transform:uppercase;letter-spacing:0.06em">Top tweets in this category</h4>`;
    cat.top_tweets.forEach(t => {
      const tLikes = t.likes >= 1000 ? (t.likes / 1000).toFixed(1) + 'K' : t.likes;
      html += `<div class="quote-card">
        <div class="quote-header">
          <span class="quote-author">@${escHTML(t.handle.replace(/^@+/,''))}</span>
          <span class="quote-likes">${tLikes} likes</span>
        </div>
        <div class="quote-text">${nl2br(t.text.substring(0, 500))}</div>
        ${t.one_liner ? `<div class="quote-summary">${escHTML(t.one_liner)}</div>` : ''}
      </div>`;
    });
  }

  panel.innerHTML = html;
  panel.classList.add('active');
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// === SHOW VOICE ===
function showVoice(handle) {
  const v = voiceData[handle];
  if (!v) return;
  const panel = document.getElementById('voice-panel');

  const role = v.is_team ? 'ANTHROPIC TEAM' : 'COMMUNITY';
  const avatarClass = v.is_team ? 'team' : 'community';
  const initials = (v.display_name || handle).substring(0, 2).toUpperCase();
  const likes = v.total_likes >= 1000 ? (v.total_likes / 1000).toFixed(1) + 'K' : v.total_likes;

  let html = `<button class="panel-close" onclick="this.parentElement.classList.remove('active')">&times;</button>`;
  html += `<div class="voice-panel-header">
    <div class="voice-avatar ${avatarClass}">${initials}</div>
    <div>
      <div class="voice-role">${role}</div>
      <div class="voice-handle">@${escHTML(handle)}</div>
      <div class="voice-stats">${escHTML(v.display_name)} &middot; ${v.bookmarks} bookmarked tips &middot; ${likes} total likes &middot; ${v.avg_likes.toLocaleString()} avg</div>
      <div class="voice-cats">${(v.top_categories || []).map(c => `<span class="voice-cat">${escHTML(c)}</span>`).join('')}</div>
    </div>
  </div>`;

  if (v.context) {
    html += `<div class="analysis"><div class="analysis-label">Our read</div>${escHTML(v.context)}</div>`;
  }

  if (v.top_tweets && v.top_tweets.length > 0) {
    html += `<h4 style="color:var(--text-muted);font-size:0.82rem;margin:16px 0 12px;text-transform:uppercase;letter-spacing:0.06em">Bookmarked tweets</h4>`;
    v.top_tweets.forEach(t => {
      const tLikes = t.likes >= 1000 ? (t.likes / 1000).toFixed(1) + 'K' : t.likes;
      html += `<div class="quote-card">
        <div class="quote-header">
          <span class="quote-author">${t.primary_keyword ? escHTML(t.primary_keyword) : ''}</span>
          <span class="quote-likes">${tLikes} likes</span>
        </div>
        <div class="quote-text">${nl2br(t.text.substring(0, 600))}</div>
        ${t.one_liner ? `<div class="quote-summary">${escHTML(t.one_liner)}</div>` : ''}
      </div>`;
    });
  }

  panel.innerHTML = html;
  panel.classList.add('active');
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// === SHOW PRINCIPLE ===
function showPrinciple(idx) {
  const p = principlesData[idx];
  const panel = document.getElementById('principle-panel');

  document.querySelectorAll('.principle-card').forEach(c => c.classList.remove('selected'));
  document.getElementById('pc-' + idx)?.classList.add('selected');

  let html = `<button class="panel-close" onclick="this.parentElement.classList.remove('active')">&times;</button>`;
  html += `<h3>${escHTML(p.principle)}</h3>`;
  html += `<div class="panel-meta">${escHTML(p.description)}</div>`;

  if (p.exemplar_tweets && p.exemplar_tweets.length > 0) {
    html += `<div class="analysis"><div class="analysis-label">This principle in practice</div>These tweets from our collection exemplify what "${escHTML(p.principle)}" looks like in the wild — community voices demonstrating the pattern before we codified it.</div>`;
    p.exemplar_tweets.forEach(t => {
      const tLikes = t.likes >= 1000 ? (t.likes / 1000).toFixed(1) + 'K' : t.likes;
      html += `<div class="quote-card">
        <div class="quote-header">
          <span class="quote-author">@${escHTML(t.handle.replace(/^@+/,''))}</span>
          <span class="quote-likes">${tLikes} likes</span>
        </div>
        <div class="quote-text">${nl2br(t.text.substring(0, 500))}</div>
        ${t.one_liner ? `<div class="quote-summary">${escHTML(t.one_liner)}</div>` : ''}
      </div>`;
    });
  }

  panel.innerHTML = html;
  panel.classList.add('active');
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// === SHOW STATUS ===
function showStatus(name) {
  const s = statusDetails[name];
  if (!s) return;
  const panel = document.getElementById('status-panel');

  document.querySelectorAll('.status-card').forEach(c => c.classList.remove('selected'));

  let html = `<button class="panel-close" onclick="this.parentElement.classList.remove('active')">&times;</button>`;
  html += `<h3>${escHTML(name)}</h3>`;
  html += `<div class="panel-meta"><span class="status-light ${s.color}" style="display:inline-block;vertical-align:middle;margin-right:8px"></span>${escHTML(s.summary)}</div>`;
  html += `<div class="analysis"><div class="analysis-label">Details</div>${escHTML(s.detail)}</div>`;

  panel.innerHTML = html;
  panel.classList.add('active');
  panel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// === BUILD CONSTELLATION ===
(function() {
  const wrap = document.getElementById('constellation');
  const tooltip = document.getElementById('tooltip');
  const W = 700, H = 700, CX = 350, CY = 350;

  const teamHandles = ['bcherny','trq212','felixrieseberg','lydiahallie','alexalbert__'];
  const communityHandles = Object.keys(voiceData).filter(h => !voiceData[h].is_team);

  let svg = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">`;
  svg += `<circle cx="${CX}" cy="${CY}" r="280" fill="none" stroke="rgba(242,204,143,0.06)" stroke-width="1"/>`;
  svg += `<circle cx="${CX}" cy="${CY}" r="140" fill="none" stroke="rgba(224,122,95,0.1)" stroke-width="1"/>`;

  const allNodes = [];

  teamHandles.forEach((h, i) => {
    const v = voiceData[h]; if (!v) return;
    const angle = (i / teamHandles.length) * Math.PI * 2 - Math.PI / 2;
    const x = CX + Math.cos(angle) * 120;
    const y = CY + Math.sin(angle) * 120;
    const size = 6 + v.bookmarks * 2.5;
    allNodes.push({ ...v, x, y, size });
  });

  communityHandles.forEach((h, i) => {
    const v = voiceData[h]; if (!v) return;
    const angle = (i / communityHandles.length) * Math.PI * 2 - Math.PI / 2;
    const x = CX + Math.cos(angle) * 250;
    const y = CY + Math.sin(angle) * 250;
    const size = 4 + v.bookmarks * 2;
    allNodes.push({ ...v, x, y, size, is_team: false });
  });

  // Lines
  allNodes.filter(n => !n.is_team).forEach(n => {
    let closest = allNodes.filter(t => t.is_team)[0];
    let minD = Infinity;
    allNodes.filter(t => t.is_team).forEach(t => {
      const d = Math.hypot(t.x - n.x, t.y - n.y);
      if (d < minD) { minD = d; closest = t; }
    });
    if (closest) svg += `<line x1="${n.x}" y1="${n.y}" x2="${closest.x}" y2="${closest.y}" stroke="rgba(242,204,143,0.06)" stroke-width="1"/>`;
  });

  // Nodes
  allNodes.forEach((n, idx) => {
    const color = n.is_team ? 'var(--terracotta)' : 'var(--sage)';
    const glow = n.is_team ? 'rgba(224,122,95,0.3)' : 'rgba(129,178,154,0.2)';
    svg += `<circle cx="${n.x}" cy="${n.y}" r="${n.size}" fill="${color}" opacity="0.9"
      data-idx="${idx}" style="cursor:pointer;filter:drop-shadow(0 0 ${n.size/2}px ${glow})"
      onclick="showVoice('${n.handle}')">
      <animate attributeName="opacity" values="0.9;0.65;0.9" dur="${3 + Math.random()*2}s" repeatCount="indefinite"/>
    </circle>`;
    if (n.bookmarks >= 3 || n.is_team) {
      svg += `<text x="${n.x}" y="${n.y + n.size + 14}" text-anchor="middle" fill="var(--text-muted)" font-size="10" font-family="system-ui" style="cursor:pointer" onclick="showVoice('${n.handle}')">@${n.handle}</text>`;
    }
  });

  svg += '</svg>';
  wrap.innerHTML = svg;

  // Tooltip on hover
  wrap.querySelectorAll('circle[data-idx]').forEach(el => {
    el.addEventListener('mouseenter', () => {
      const n = allNodes[+el.dataset.idx];
      const badge = n.is_team ? '<span style="color:var(--terracotta)">TEAM</span>' : '<span style="color:var(--sage)">COMMUNITY</span>';
      tooltip.innerHTML = `
        <div class="vt-name">@${n.handle} ${badge}</div>
        <div class="vt-stat">${n.display_name} &middot; ${n.bookmarks} tips &middot; ${(n.total_likes/1000).toFixed(1)}K likes</div>
        <div class="vt-topics">${(n.top_categories || []).join(' · ')}</div>
        <div class="vt-hint">Click for full profile</div>
      `;
      tooltip.classList.add('show');
    });
    el.addEventListener('mousemove', (e) => {
      tooltip.style.left = e.clientX + 16 + 'px';
      tooltip.style.top = e.clientY - 10 + 'px';
    });
    el.addEventListener('mouseleave', () => tooltip.classList.remove('show'));
  });
})();
''')

html_parts.append('</script></body></html>')

# Write output
output = ''.join(html_parts)
with open('infographic.html', 'w') as f:
    f.write(output)

print(f"Written {len(output):,} bytes to infographic.html")
print(f"Embedded: {len(categories)} categories, {len(voices)} voices, {len(principles)} principles")
