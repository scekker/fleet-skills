#!/usr/bin/env python3
"""
fleet-sync: push a file from Uvy workspace to all reachable fleet nodes.
Usage: python3 fleet_sync.py <relative_path_in_workspace> [--dry-run]

Nodes and paths are defined in the FLEET dict below.
Unreachable nodes are logged, not fatal.
"""

import subprocess
import sys
import os
from datetime import datetime

WORKSPACE = "/Users/dyrmalabs/.openclaw/workspace"

# node_name: (ssh_target, remote_workspace_path)
FLEET = {
    "Pip":    ("dr.ekker@100.110.31.60",   "/Users/dr.ekker/.openclaw/workspace"),
    "Atlas":  ("atlas@100.90.91.58",        "/Users/atlas/.openclaw/workspace"),
    "Zevo":   ("zevo@100.108.211.25",       "/Users/zevo/.openclaw/workspace"),
    "Buster": ("uvy@100.93.179.107",        "/home/uvy/.openclaw/workspace"),
    "SARAH":  ("sarah@100.120.104.61",      "/Users/sarah/.openclaw/workspace"),
    "Mendel": ("ankit@100.87.33.71",        "/Users/ankit/.openclaw/workspace"),  # SSH often blocked
    "Jimmy":  ("dr.ekker@100.121.106.105",  "/Users/dr.ekker/.openclaw/workspace"),  # No Uvy key yet
}

def sync_file(rel_path: str, dry_run: bool = False):
    src = os.path.join(WORKSPACE, rel_path)
    if not os.path.exists(src):
        print(f"❌ Source not found: {src}")
        sys.exit(1)

    results = {"ok": [], "fail": [], "skip": []}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M CDT")

    for node, (target, remote_ws) in FLEET.items():
        remote_path = os.path.join(remote_ws, rel_path)
        remote_dir  = os.path.dirname(remote_path)

        if dry_run:
            print(f"[DRY RUN] {node}: {target}:{remote_path}")
            continue

        # Ensure remote directory exists
        mkdir_result = subprocess.run(
            ["ssh", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes",
             target, f"mkdir -p {remote_dir}"],
            capture_output=True, timeout=10
        )
        if mkdir_result.returncode != 0:
            print(f"⚠️  {node}: cannot create remote dir — skipping ({mkdir_result.stderr.decode().strip()})")
            results["fail"].append(node)
            continue

        # Copy file
        scp_result = subprocess.run(
            ["scp", "-o", "ConnectTimeout=5", "-o", "BatchMode=yes",
             src, f"{target}:{remote_path}"],
            capture_output=True, timeout=15
        )
        if scp_result.returncode == 0:
            print(f"✅ {node}")
            results["ok"].append(node)
        else:
            err = scp_result.stderr.decode().strip()
            print(f"❌ {node}: {err}")
            results["fail"].append(node)

    print(f"\n📊 {timestamp}")
    print(f"   ✅ Success: {', '.join(results['ok']) or 'none'}")
    print(f"   ❌ Failed:  {', '.join(results['fail']) or 'none'}")
    return results

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 fleet_sync.py <relative_path> [--dry-run]")
        sys.exit(1)
    rel = sys.argv[1]
    dry = "--dry-run" in sys.argv
    sync_file(rel, dry_run=dry)
