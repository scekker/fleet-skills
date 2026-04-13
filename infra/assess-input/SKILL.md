---
name: assess-input
description: >
  Pre-flight document size and type assessment before AI ingestion. Prevents context spiral
  crashes caused by oversized files. Use BEFORE loading ANY document not created in the
  current session — uploads, Drive files, Discord attachments, any file > a few KB.
  Triggers on: user shares a file, fetching a doc from Drive/Discord, any ingestion task
  where file size is unknown.
---

# assess-input

**Assess document size and type before AI ingestion. Prevents context spiral crashes.**

Born from: Atlas crashing on Jon Mochel's 7MB CEIRR `.docx` (2026-04-10).

---

## When to use

Run `assess_input.py` BEFORE loading ANY document that wasn't just created in the current session:
- User-uploaded files (docx, pdf, txt, csv)
- Files fetched from Google Drive or Discord attachments
- Any file > a few KB you haven't personally just written

**Do not skip this.** The cost is one shell call. The cost of skipping is a context spiral crash.

---

## Categories

| Category | Threshold | Action |
|----------|-----------|--------|
| ✅ DIRECT  | < 50 KB   | Load directly into context |
| ⚠️ EXTRACT | 50–500 KB | Extract plain text first; read in sections |
| 🔶 CHUNK   | 500KB–2MB | Subagent + targeted reads only |
| 🔴 DANGER  | > 2 MB    | Never load raw. Extract → chunk → grep only |

---

## Usage

```bash
python3 ~/scripts/assess_input.py <file_path>
python3 ~/scripts/assess_input.py <file_path> --json
```

### Example output

```
───────────────────────────────────────────────────────
  📄  assess_input — VaaS-preprint.pdf
───────────────────────────────────────────────────────
  Size:       1.6 MB  (1,729,814 bytes)
  Type:       .pdf
  Characters: 96,847  (extracted via PyPDF2)
  Est. tokens:24,211
  Context %:  [████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 12.1%

  Category:   CHUNK

  🔶 CHUNK + SUBAGENT
     Too large for single context. Use targeted reads only.
     Action: spawn subagent with specific extraction task.
     Never load full file. Grep/search for relevant sections first.
───────────────────────────────────────────────────────
```

---

## Self-Install (any fleet agent)

Run this once on a new node to install the script and dependencies:

```bash
# 1. Create scripts dir if needed
mkdir -p ~/scripts

# 2. Copy script from workspace (if fleet-synced) or fetch from Drive
#    If workspace is available:
cp ~/.openclaw/workspace/skills/assess-input/scripts/assess_input.py ~/scripts/
chmod +x ~/scripts/assess_input.py

# 3. Install Python dependencies
pip3 install PyPDF2 python-docx --break-system-packages --quiet

# 4. Verify
python3 ~/scripts/assess_input.py --help
```

**Dependencies:**
- `python-docx` — `.docx` extraction
- `PyPDF2` — `.pdf` extraction
- Both gracefully degrade: if missing, falls back to size-based estimation

---

## What it checks

1. **File size** — raw bytes
2. **File type** — docx, pdf, txt, md, csv
3. **Actual character/token count** — extracts text where possible (real estimate, not size guess)
4. **Context window %** — assumes 200K token window (Claude Sonnet 4.x)
5. **Processing recommendation** — concrete next action

---

## Script location

- **Canonical source:** `skills/assess-input/scripts/assess_input.py` (this skill)
- **Runtime location:** `~/scripts/assess_input.py` (deployed on each node)

---

## Exit Codes (v1.1+)

The script enforces hard stops via exit codes — automated pipelines cannot proceed without explicit override:

| Exit code | Meaning |
|-----------|---------|
| 0 | DIRECT or EXTRACT — safe to proceed |
| 1 | CHUNK — proceed with caution; subagent recommended |
| 2 | DANGER — hard stop; do not proceed |

Override DANGER with `--force-dangerous` flag (requires human authorization).

---

## Hardware Routing

| Category | Pip (2017 Intel) | Atlas (M3 Ultra) | Buster (Linux) |
|----------|-----------------|-----------------|----------------|
| DIRECT   | ✅ | ✅ | ✅ |
| EXTRACT  | ✅ | ✅ | ✅ |
| CHUNK    | ❌ will crash | ✅ | ✅ |
| DANGER   | ❌ will crash | ✅ | ✅ |

**CHUNK and DANGER docs must be routed to Atlas or Buster.** Pip should extract only and hand off.

---

## Root cause this prevents

The **"7MB docx crash"** pattern:
1. Large file attachment arrives
2. Agent tries to load it raw → context fills
3. Agent tries workarounds → more context fills
4. Context spiral → session crash

`assess_input` catches this at step 1 and routes to the right strategy before any loading attempt.

---

## Test validation

### v1.0 — Atlas (2026-04-10)
| File | Size | Category | Notes |
|------|------|----------|-------|
| synthetic_small.txt | 6 KB | ✅ DIRECT | |
| synthetic_medium.pdf | 162 KB | ⚠️ EXTRACT | |
| synthetic_large.docx | 852 KB | 🔶 CHUNK | 164% context |
| synthetic_danger.docx | 5.5 MB | 🔴 DANGER | 1130% context |
| VaaS preprint (real Drive PDF) | 1.6 MB | 🔶 CHUNK | 12.1% context — PyPDF2 clean |

### v1.1 — Pip test flight (2026-04-10)
| File | Size | Category | Result |
|------|------|----------|--------|
| Jon Mochel CEIRR .docx | 7.1 MB | 🔴 DANGER | Correctly flagged + extracted. Agent crashed on downstream chunk read — expected on 2017 Intel hardware. Confirmed: DANGER docs must route to Atlas/Buster. |

---

## Changelog

| Date | Entry |
|------|-------|
| 2026-04-10 | v1.0 — Initial build + test. 4 synthetic docs + 1 real Drive PDF. All categories verified. Built by Atlas 🏛️ per Steve Ekker directive. Formalized as fleet skill. |
| 2026-04-10 | v1.1 — Added exit codes (0/1/2), `--force-dangerous` override, `safe_chunk_chars` output, hardware routing table (Pip/Atlas/Buster), DANGER hard stop enforcement. Triggered by Pip crash on 7MB CEIRR doc. |
