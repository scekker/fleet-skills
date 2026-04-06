#!/bin/bash
# deploy.sh — Deploy FLEET-MEM-001 MoE shards to a fleet node
# Usage: bash deploy.sh <ssh-target> <remote-workspace-path>
# Example: bash deploy.sh zevo@100.108.211.25 ~/.openclaw/workspace

set -e

SSH_TARGET="$1"
REMOTE_WS="$2"
LOCAL_WS="/Users/dyrmalabs/.openclaw/workspace"

if [[ -z "$SSH_TARGET" || -z "$REMOTE_WS" ]]; then
  echo "Usage: bash deploy.sh <ssh-target> <remote-workspace-path>"
  exit 1
fi

echo "🚀 Deploying FLEET-MEM-001 to $SSH_TARGET..."

# Ensure remote memory dir exists
ssh "$SSH_TARGET" "mkdir -p $REMOTE_WS/memory"

# Sync topic shards
echo "📦 Syncing topic shards..."
scp \
  "$LOCAL_WS/memory/science.md" \
  "$LOCAL_WS/memory/contacts.md" \
  "$LOCAL_WS/memory/infrastructure.md" \
  "$LOCAL_WS/memory/projects.md" \
  "$LOCAL_WS/memory/company.md" \
  "$LOCAL_WS/memory/lessons.md" \
  "$LOCAL_WS/memory/cron-jobs.md" \
  "$LOCAL_WS/memory/arc-agi.md" \
  "$LOCAL_WS/memory/reasoning-journal.md" \
  "$LOCAL_WS/memory/ROUTER.md" \
  "$SSH_TARGET:$REMOTE_WS/memory/"

# Sync core files
echo "📄 Syncing core files..."
scp \
  "$LOCAL_WS/AGENTS.md" \
  "$LOCAL_WS/GROUND.md" \
  "$LOCAL_WS/TODAY.md" \
  "$LOCAL_WS/MEMORY.md" \
  "$SSH_TARGET:$REMOTE_WS/"

# Verify
echo "✅ Verifying deployment..."
SHARD_COUNT=$(ssh "$SSH_TARGET" "ls $REMOTE_WS/memory/*.md 2>/dev/null | wc -l | tr -d ' '")
MOE_CHECK=$(ssh "$SSH_TARGET" "grep -c 'Layer 0' $REMOTE_WS/AGENTS.md 2>/dev/null || echo 0")

echo "   Shards found: $SHARD_COUNT (expect ≥10)"
echo "   MoE bootstrap in AGENTS.md: $MOE_CHECK (expect ≥1)"

if [[ "$SHARD_COUNT" -ge 10 && "$MOE_CHECK" -ge 1 ]]; then
  echo "✅ FLEET-MEM-001 deployed successfully to $SSH_TARGET"
else
  echo "⚠️  Deployment may be incomplete — check manually"
  exit 1
fi
