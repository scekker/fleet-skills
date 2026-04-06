---
name: bird-x
description: Read-only access to X (Twitter) for AI agents using the bird CLI. Use when searching tweets, reading timelines, fetching threads, checking trends, or monitoring accounts on X/Twitter — without an API key. Triggers on phrases like "search Twitter", "look up tweets", "what's trending", "read this tweet", "monitor X for", "find tweets about". Read-only — do NOT use for posting, liking, or any write actions.
---

# bird-x

Read-only X/Twitter access via the `bird` CLI (`@steipete/bird`). Uses browser cookie auth — no Twitter developer account required.

## Install (per node)

```bash
npm install -g @steipete/bird
```

Then set auth token (one-time per node):
```bash
export TWITTER_AUTH_TOKEN=your_auth_token_here
# Add to ~/.bashrc or ~/.zshrc to persist
```

To get auth token: log into x.com in browser → DevTools → Application → Cookies → copy `auth_token` value.

See `references/node-setup.md` for per-node status and auth token instructions.

## Core Commands

```bash
# Search tweets
bird search "VEGF-A skin redness" --limit 20

# Read a tweet/thread
bird read https://x.com/user/status/123456789

# User timeline
bird timeline @username --limit 30

# Trending topics
bird trending

# User profile
bird user @username

# Advanced search operators
bird search "from:@username since:2026-01-01 CAST protein design"

# JSON output (for piping)
bird search "zebrafish CRISPR" --json
```

## Fleet Usage Pattern

```bash
# SciPulse biotech signal scan
bird search "protein design AI" --limit 50 --json | jq '.[] | {text, author, likes, date}'

# Monitor a list of accounts
for handle in AlphaFold_AI RoseTTAFold baker_lab; do
  bird timeline @$handle --limit 5 --json
done
```

## ⚠️ Rules

- **Read-only only.** No `bird tweet`, `bird reply`, `bird like` — account suspension risk.
- Use secondary/bot accounts if testing write features is ever needed.
- Cookie-based auth is unofficial — may break if Twitter changes internals.
- If `bird` returns auth errors, re-extract `auth_token` from browser.

## Fleet Status

See `references/node-setup.md` for install status per node.
