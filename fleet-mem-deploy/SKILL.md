---
name: fleet-mem-deploy
description: Deploy the FLEET-MEM-001 Memory Mixture-of-Experts (MoE) architecture to one or more fleet nodes. Use when onboarding a new node to the MoE memory system, syncing updated shards to existing nodes, or recovering a node after a reset. Triggers on phrases like "deploy memory shards", "sync MoE to [node]", "onboard [node] to fleet memory", "update shards on [node]", "deploy FLEET-MEM-001".
---

# fleet-mem-deploy

Deploy the FLEET-MEM-001 Memory MoE architecture to a fleet node. This syncs all topic shards, core files, and the MoE bootstrap block in AGENTS.md.

## What Gets Deployed

**Core files** (workspace root):
- `AGENTS.md` — MoE bootstrap instructions (Layer 0/1/2 routing)
- `GROUND.md` — behavioral priors
- `TODAY.md` — live priorities
- `MEMORY.md` — pointer index

**Topic shards** (workspace/memory/):
- `science.md`, `contacts.md`, `infrastructure.md`, `projects.md`
- `company.md`, `lessons.md`, `cron-jobs.md`, `arc-agi.md`
- `reasoning-journal.md`, `ROUTER.md`, `discord-channels.md`

## Deploy to a Node

```bash
bash scripts/deploy.sh <ssh-target> <workspace-path>
```

Examples:
```bash
bash scripts/deploy.sh zevo@100.108.211.25 ~/.openclaw/workspace
bash scripts/deploy.sh uvy@100.93.179.107 ~/.openclaw/workspace   # Buster
bash scripts/deploy.sh sarah@100.120.104.61 ~/.openclaw/workspace  # SARAH
bash scripts/deploy.sh dr.ekker@100.110.31.60 ~/.openclaw/workspace # Pip
```

The script syncs all files, then verifies shards landed correctly.

## Node-Specific Gotchas

Read `references/node-gotchas.md` before deploying to: Jimmy, Atlas, SARAH, Buster.

Each node has quirks (PATH issues, user account confusion, gateway bind config) that can cause silent failures.

## After Deployment

1. Verify node can read shards: `ssh <target> 'ls ~/.openclaw/workspace/memory/*.md'`
2. Check AGENTS.md has MoE bootstrap: `ssh <target> 'grep -c "Layer 0" ~/.openclaw/workspace/AGENTS.md'` (expect ≥ 1)
3. If node has a cron, restart gateway: `ssh <target> 'openclaw gateway restart'`
4. Update `memory/2026-MM-DD.md` with deployment record

## Adding a New Node

When deploying to a node not yet in the fleet:
1. Check `references/node-gotchas.md` for known issues
2. Verify SSH access before running deploy script
3. Ensure node is on OpenClaw v2026.3.31+ (run upgrade first if needed)
4. Get "yes to [node]" from Steve before any action
5. After deploy, add node entry to `memory/infrastructure.md`
