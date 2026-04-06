---
name: fleet-sync
description: Push any file from Uvy's workspace to all fleet nodes in one command. Use when: (1) a new memory shard, config file, or script needs to be deployed fleet-wide, (2) a file was updated on Uvy and needs to propagate to Pip, Atlas, Zevo, Buster, SARAH, Mendel, Jimmy, (3) Steve says "give this to the entire fleet" or "deploy this fleet-wide". Handles per-node path differences (macOS /Users vs Linux /home), creates remote directories automatically, reports per-node success/failure. Unreachable nodes are logged, not fatal.
---

# Fleet Sync

Push a workspace file to all fleet nodes.

## Usage

```bash
python3 skills/fleet-sync/scripts/fleet_sync.py <relative_path> [--dry-run]
```

`relative_path` is relative to `/Users/dyrmalabs/.openclaw/workspace/`.

**Examples:**
```bash
# Push a memory shard fleet-wide
python3 skills/fleet-sync/scripts/fleet_sync.py memory/discord-channels.md

# Dry run first to preview targets
python3 skills/fleet-sync/scripts/fleet_sync.py memory/ROUTER.md --dry-run
```

## Fleet Node Registry

Defined in `scripts/fleet_sync.py` → `FLEET` dict. Current nodes:

| Node | SSH Target | Notes |
|------|-----------|-------|
| Pip | dr.ekker@100.110.31.60 | macOS, canary |
| Atlas | atlas@100.90.91.58 | macOS |
| Zevo | zevo@100.108.211.25 | macOS |
| Buster | uvy@100.93.179.107 | Ubuntu/Linux |
| SARAH | sarah@100.120.104.61 | Ubuntu/Linux |
| Mendel | ankit@100.87.33.71 | SSH often blocked — needs Ankit auth |
| Jimmy | dr.ekker@100.121.106.105 | No Uvy SSH key yet |

## After Syncing

After pushing a memory shard, also update each node's ROUTER.md and AGENTS.md if the shard needs to be router-discoverable. Do this manually or via ssh for now — future versions of this skill will handle it.

## Updating the Fleet Registry

When a new node joins the fleet, add it to the `FLEET` dict in `scripts/fleet_sync.py`:
```python
"NodeName": ("user@tailscale-ip", "/Users/or/home/user/.openclaw/workspace"),
```
