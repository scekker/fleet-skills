# Context Window Skill — SKILL.md

## When to use this skill
When user says anything like:
- "turn on 1M context" / "enable 1M" / "use extended context"
- "switch to large context" / "turn off extended context" / "back to normal"
- "context status" / "what context mode are we in"
- "use 1M for this" / "need more context"

## How it works
OpenClaw has native support for `context1m: true` on model configs.
When enabled, it adds the `context-1m-2025-08-07` beta header to Bedrock requests.
Supported models: Claude Opus 4.6, Sonnet 4.6 (both via Bedrock).
NOTE: Does NOT work with OAuth auth — Bedrock AWS SDK auth only (which is what we use ✅).

## Modes

| Mode   | contextWindow | maxTokens | reserveFloor | context1m | Use for |
|--------|--------------|-----------|--------------|-----------|---------|
| normal | 200,000      | 16,384    | 5,000        | false     | Everyday tasks |
| large  | 200,000      | 32,000    | 2,000        | false     | Long docs, big outputs |
| 1m     | 1,000,000    | 32,000    | 2,000        | true      | Massive context needs |

## Toggle script
`/Users/dyrmalabs/.openclaw/workspace/tools/ctx-toggle.sh [normal|large|1m|status]`

## Confirmation flow (REQUIRED before enabling 1m or large)

When user asks to enable 1m or large, ALWAYS reply first:

> ⚠️ **Context Mode: [MODE]**
> - Window: [X] tokens
> - Cost: [impact]
> - Gateway restart required (~2 seconds)
>
> Confirm? (yes / no)

Wait for explicit "yes" before running the script.

## On confirm — run:
exec: `/Users/dyrmalabs/.openclaw/workspace/tools/ctx-toggle.sh [mode]`

## Natural language → mode mapping
- "1M" / "one million" / "extended" / "maximum" → 1m
- "large" / "big" / "more tokens" / "more output" → large  
- "normal" / "standard" / "default" / "turn off" / "back to normal" → normal
- "status" / "current mode" / "what mode" → status (no confirmation needed)
