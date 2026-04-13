---
name: magika-scout
description: "AI-powered file type detection and parser routing using Google's Magika model. Use when: (1) validating downloaded files before parsing (PDFs, SEC filings, trial docs, data dumps), (2) routing unknown files to the correct parser automatically, (3) pre-flight safety checks on ingested files to catch executables or misidentified formats, (4) scanning directories for unexpected file types. Triggers on: 'check what this file is', 'validate before parsing', 'scout this file', 'what type is this', 'pre-flight file check', 'route to correct parser', 'is this safe to parse'. NOT for: parsing file contents (use the routed parser), virus scanning (use VirusTotal), or large binary analysis."
---

# Magika Scout

Fast (~5ms/file) AI file-type detection via Google's Magika model (99% accuracy, 200+ types). Identifies what a file *actually is* — not what its extension claims.

## Quick Start

```bash
# Single file or URL
python3 scripts/scout.py <file_or_url>

# Directory (recursive)
python3 scripts/scout.py --dir <path> --recursive

# JSON output for pipeline integration
python3 scripts/scout.py --json <file>

# Exit codes: 0=all safe/expected, 1=dangerous or unknown type found
```

Auto-installs `magika` on first run if not present.

## Output

```
✅ report.pdf       type=pdf    mime=application/pdf   confidence=99%   parser → pdfplumber / pymupdf
🚨 payload.pdf      type=elf    mime=application/x-elf confidence=98%   parser → ⚠️ EXECUTABLE — do not auto-parse
⚠️  data.csv        type=unknown mime=None              confidence=12%   parser → ⚠️ UNKNOWN — manual review required
```

- ✅ = known safe type
- 🚨 = executable/dangerous (`elf`, `pe`, `macho`, `shell`, `batch`) — exit code 1
- ⚠️ = unexpected or low-confidence — review manually

## Pipeline Integration

```python
import subprocess, json

def scout(path: str) -> dict:
    result = subprocess.run(
        ["python3", "skills/magika-scout/scripts/scout.py", "--json", path],
        capture_output=True, text=True
    )
    findings = json.loads(result.stdout)
    return findings[0] if findings else {}

f = scout("downloads/filing.pdf")
if f["dangerous"]:
    raise ValueError(f"Unsafe file type: {f['type']}")
if f["type"] != "pdf":
    raise ValueError(f"Expected PDF, got: {f['type']}")
# safe to parse
```

## When to Use in Pipelines

Add a scout call **before**:
- Parsing downloaded PDFs, HTML, or data files
- Processing user-uploaded or externally-fetched documents
- Ingesting SEC filings, trial readout PDFs, patent docs, earnings transcripts
- Any batch download where silent failures are possible

## Router Map

See `references/router-map.md` for the full content-type → parser routing table and notes on each type.

## Installing on a Fleet Node

```bash
pip install magika
# or inside a venv:
source <venv>/bin/activate && pip install magika
```

Magika model (~few MB) downloads on first run and caches locally. No GPU required — runs on CPU in ~5ms/file.
