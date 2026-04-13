---
name: openclaw-test-flight
description: Run a structured post-update validation test flight after any OpenClaw version update. Use when OpenClaw has just been updated on a node and you need to verify the new version is functioning correctly before fleet rollout. Covers gateway health, memory, Google Workspace (gog), web tools, exec, Discord, and session hygiene. Reports pass/fail to Steve's DM. Designed for Pip (canary node) but usable on any fleet node.
---

# OpenClaw Test Flight

Run immediately after any `openclaw update` or `npm install -g openclaw@*` completes. No manual trigger needed — this is automatic post-update validation.

## Checklist

Work through each section in order. Note pass ✅ or fail ❌ for each item.

### 1. Core Health
- `openclaw --version` — confirm correct version installed
- `openclaw status` — gateway running, no critical errors
- `openclaw doctor` — note all flags; run `--fix` if fixable issues present, then re-run to confirm clean
- Pre-existing/cosmetic flags (NVM warning, empty allowlist) → note but do not block

### 2. Memory
- Write a test memory entry (e.g. "test flight vXXXX.X.XX ran successfully")
- Retrieve it in the next turn — confirms mem0 end-to-end working

### 3. Google Workspace (gog)
- `gog drive ls` — Drive accessible
- Create a test doc, write one line, read it back — confirms Docs write/read working
- Use the configured gog account for this node

### 4. Tools
- Web search — run a simple query (e.g. "openclaw latest version"), confirm results returned
- Web fetch — fetch `https://example.com`, confirm content returned
- Exec — run `echo "test-flight-ok"`, confirm output

### 5. Discord
- Confirm bot is responsive (the report message itself proves DM routing works)

### 6. Session Health
- Check session count: `ls ~/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null | wc -l`
- Flag if > 40
- Check for stale locks: `ls ~/.openclaw/agents/main/sessions/*.lock 2>/dev/null` — should be empty

## Report

Post to Steve's DM channel (`1468002684048113837`) immediately after completing all checks:

```
🐣 Pip Test Flight — OpenClaw vXXXX.X.XX

| Check            | Result | Notes                        |
|------------------|--------|------------------------------|
| Version          | ✅/❌  | vXXXX.X.XX confirmed         |
| Gateway/Doctor   | ✅/❌  | N flags: [list if any]       |
| Memory           | ✅/❌  |                              |
| Google Drive     | ✅/❌  |                              |
| Google Docs      | ✅/❌  |                              |
| Web search       | ✅/❌  |                              |
| Web fetch        | ✅/❌  |                              |
| Exec             | ✅/❌  |                              |
| Discord          | ✅/❌  |                              |
| Sessions         | ✅/❌  | N sessions                   |

🟢 GREEN LIGHT — safe to roll to fleet
OR
🔴 HOLD — [describe issue] — do not update fleet until resolved
```

## Pass Criteria
- All checks pass → 🟢 GREEN LIGHT
- Any functional check fails → 🔴 HOLD, notify Steve, do not proceed with fleet update
- Doctor cosmetic flags → note in report, do not block

## Fleet Context
- Steve waits for overnight soak (cold restart, crons, memory recall) before authorizing fleet rollout
- Fleet update order: Pip (canary) → Zevo → SARAH → Atlas → Buster
- Run `openclaw doctor --fix` on every node after update
