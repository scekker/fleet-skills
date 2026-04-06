---
name: discord-dm-recover
description: >
  Recover lost session context by fetching and summarizing a Discord DM conversation.
  Use when an agent crashes mid-session, a DM context is cleared, or you need to
  reconstruct what was discussed before a reset. Triggers on phrases like
  "recover context", "what were we doing", "grab our DM from this morning",
  "patch context after crash", "reconstruct session", "what did we discuss".
  Also use proactively on session boot when TODAY.md indicates a recent crash or context wipe.
---

# Discord DM Recover

Fetches recent DM history from a Discord channel and produces a structured context summary the agent can act on immediately.

## When to Use

- After a crash, reset, or context wipe — pull the conversation to reconstruct what was in-flight
- On session boot when `TODAY.md` or `HEARTBEAT.md` mention a recent crash
- When a human says "you crashed" or "Sarah cleared the DM" or "we need to patch things"

## Core Workflow

### Step 1: Identify the channel

For Steve's DM: channel ID `1468002684048113837`  
For other people: check `memory/discord-channels.md` under the DMs section.  
If unknown: ask the human which channel or person.

### Step 2: Fetch messages

Use the `message` tool:

```
action: read
channel: discord
target: <channel_id>
limit: 50   # increase to 100 if crash was >30 min ago
```

**Default: today's messages only.** 50 messages covers a full morning of active conversation. Only go higher if the crash happened across a long session (>1 hour of dense back-and-forth). Do not pull the full channel history — today's context is what matters.

### Step 3: Produce a context summary

From the fetched messages, extract and write out:

1. **What we were working on** — active tasks/projects at time of crash
2. **What was completed** — anything finished before crash
3. **What was in-flight** — mid-task items that need resuming
4. **Decisions made** — any explicit yes/no, approvals, or direction changes
5. **Open questions** — things asked but not yet answered
6. **Errors/lessons** — any mistakes called out by the human (important to not repeat)

Format as a brief numbered list under each heading. Omit empty sections.

### Step 4: Write to recovery file (optional but recommended)

If the crash was significant or the session will be long:

```
memory/crash-recovery-YYYY-MM-DD-HHMM.md
```

Content: the structured summary from Step 3 + raw timestamp of fetch.

### Step 5: Resume

State clearly: "I've recovered context. Here's where we left off: [top 2-3 items]" and ask which to tackle first, or proceed directly if obvious.

## Notes

- Images attached to Discord messages will appear as attachment URLs in the raw data — note them but don't try to re-fetch unless the human asks
- The `message(action=read)` tool returns newest-first — mentally reverse when summarizing chronology
- If messages go back further than `limit` allows, use the `before` parameter with the oldest message ID to paginate
- This skill works on any Discord channel, not just DMs — use the same workflow for #gene-pool or project channels if needed
