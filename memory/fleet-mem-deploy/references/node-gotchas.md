# Node-Specific Gotchas — FLEET-MEM-001 Deployment
*Lessons from the 2026-04-03 fleet rollout. Read before deploying to any of these nodes.*

---

## Jimmy (100.121.106.105, user: ekker)

- **SSH user:** `ekker` (not `jimmy`)
- **Node path:** `~/.openclaw/workspace` (standard)
- **npm PATH issue:** `npm` and `openclaw` not on default SSH PATH. Use full paths:
  ```bash
  export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
  ```
- **npm install fix:** Add full PATH before npm commands or `spawn sh ENOENT` error occurs
- **openclaw binary:** Not symlinked to PATH — use `node /usr/local/lib/node_modules/openclaw/dist/index.js` for gateway commands
- **Slow machine:** 2012 Intel MBP. npm install takes ~2 minutes. Gateway response ~468ms. Be patient.
- **Ownership:** Zevo owns Jimmy. Do not touch without Zevo's explicit authorization AND Steve "yes to Jimmy".

---

## Atlas (100.90.91.58, user: atlas)

- **SSH key:** Use `-i ~/.ssh/id_ed25519`
- **PATH issue:** Homebrew not on default SSH PATH. Always prefix: `export PATH="/opt/homebrew/bin:$PATH"`
- **Gateway bind deviation (fixed 2026-04-03):** Was bound to tailnet IP instead of loopback. Fix:
  ```python
  import json
  with open("/Users/atlas/.openclaw/openclaw.json") as f: d = json.load(f)
  d.setdefault("gateway", {})["bind"] = "loopback"
  with open("/Users/atlas/.openclaw/openclaw.json", "w") as f: json.dump(d, f, indent=2)
  ```
- **Perplexity config issue:** After upgrade, may hit `tools.web.search: Unrecognized key: "perplexity"` error. Fix: `openclaw doctor --fix`
- **CVE note:** GHSA-9hjh-fr4f-gxc4 patched in v2026.3.31 (loopback bind fix above resolves this)

---

## SARAH (100.120.104.61, user: sarah)

- **CRITICAL:** OpenClaw runs under the `ekker` macOS user account, NOT `sarah`. Always SSH as `sarah` but the process runs as `ekker`.
- **LaunchAgent location:** `/Users/ekker/Library/LaunchAgents/ai.openclaw.gateway.plist` — NOT sarah's LaunchAgents
- **HOME in plist:** `/Users/sarah` — config and workspace live under sarah's home
- **Gateway log:** `/Users/sarah/.openclaw/logs/gateway.log` — but only readable by sarah user
- **After upgrade:** Run `openclaw doctor --fix` to rebuild sqlite3 (mem0 extension)
- **If gateway down:** The LaunchAgent is under `ekker`. To restart, must be physically logged in as `ekker` on that machine. SSH cannot bootstrap the LaunchAgent (`gui/501` domain).
- **Self-update behavior:** SARAH self-updated from v2026.2.26 → v2026.3.24 on 2026-04-03. The update ran correctly but required `openclaw doctor --fix` afterward.
- **DO NOT attempt:** `sudo launchctl bootstrap gui/504` — fails with I/O error. The `sarah` macOS account has never had a GUI session and cannot bootstrap LaunchAgents.

---

## Buster (100.93.179.107, user: uvy)

- **Standard node** — no unusual gotchas
- **systemd (not LaunchAgent):** `openclaw gateway restart` uses systemd, not LaunchAgent
- **GPU jobs:** Gateway restart does NOT affect running GPU processes (separate conda envs)
- **npm PATH:** Source `~/.bashrc` first if running commands via SSH: `source ~/.bashrc && npm ...`

---

## Pip (100.110.31.60, user: dr.ekker)

- **Standard node** — canary, always upgraded first
- **nvm:** Node installed via nvm at `~/.nvm/versions/node/v22.22.0/bin/`
- **Role:** Canary node. Always upgrade Pip first, wait full day, then fleet rollout.

---

## Fleet SSH Quick Reference

| Node | SSH Target | Architecture | Notes |
|------|-----------|-------------|-------|
| Uvy | `dyrmalabs@100.94.110.26` | Apple Silicon | Local (this machine) |
| Pip | `dr.ekker@100.110.31.60` | **Intel Mac** | nvm node, PATH issues |
| Zevo | `zevo@100.108.211.25` | Apple Silicon | M4 Pro Mac Mini |
| Buster | `uvy@100.93.179.107` | **Linux** (Ubuntu) | systemd, `/home/uvy/` |
| Atlas | `atlas@100.90.91.58` | Apple Silicon | Mac Studio, use `-i ~/.ssh/id_ed25519` |
| SARAH | `sarah@100.120.104.61` | Apple Silicon | Runs as ekker — see above |
| Jimmy | `ekker@100.121.106.105` | **Intel Mac** | Zevo's domain — get auth first |

---

## Upgrade SOP (hard lesson 2026-04-02/03)

1. "yes to [node]" = that node only. Never chain.
2. Pip first → full-day canary wait → Steve approves per node
3. "Roll out if ok" ≠ authorization. Each node needs explicit "yes to [node]"
4. Zevo owns Jimmy. Uvy does not touch Jimmy without Zevo + Steve authorization.
5. After every upgrade: run `openclaw doctor --fix` to catch config issues
