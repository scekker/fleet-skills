#!/usr/bin/env python3
"""
assess_input.py — Document ingestion pre-flight checker
Atlas 🏛️ | UViiVe + Ekker Lab
Built: 2026-04-10

Usage:
    python3 assess_input.py <file_path> [--json]

Outputs a processing plan before any large document is loaded into AI context.
Prevents context spiral crashes from oversized inputs.

Categories:
    DIRECT      < 50 KB   — load directly into context
    EXTRACT     50–500 KB — extract text first, load in sections
    CHUNK       500KB–2MB — subagent with targeted reads only
    DANGER      > 2 MB    — never load into context; grep/search only
"""

import sys
import os
import json
import argparse

# ── optional deps (graceful fallback if missing) ──────────────────────────────
try:
    import docx as _docx
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

try:
    import PyPDF2 as _pdf
    HAS_PDF = True
except ImportError:
    HAS_PDF = False

# ── constants ─────────────────────────────────────────────────────────────────
CHARS_PER_TOKEN   = 4          # rough estimate
CONTEXT_WINDOW    = 200_000    # tokens (Claude Sonnet 4.x)
SAFE_CONTEXT_PCT  = 0.25       # don't use >25% of window on one doc

THRESHOLDS = {
    "DIRECT":  50_000,          # bytes
    "EXTRACT": 500_000,
    "CHUNK":   2_000_000,
    # > 2MB → DANGER
}

RECOMMENDATIONS = {
    "DIRECT": (
        "✅ DIRECT LOAD\n"
        "   Safe to load directly into context.\n"
        "   Action: read file, pass contents to model."
    ),
    "EXTRACT": (
        "⚠️  EXTRACT FIRST\n"
        "   Too large to load raw. Extract plain text before ingestion.\n"
        "   Action: strip to .txt → read in sections (max ~40KB each).\n"
        "   Tools: python-docx (docx), PyPDF2/pdfminer (pdf), cat (txt/csv)."
    ),
    "CHUNK": (
        "🔶 CHUNK + SUBAGENT\n"
        "   Too large for single context. Use targeted reads only.\n"
        "   Action: spawn subagent with specific extraction task.\n"
        "   Never load full file. Grep/search for relevant sections first.\n"
        "   Max safe chunk size: 40,000 chars (~10K tokens, 5% context).\n"
        "   Hardware: requires Atlas (Mac Studio M3) or Buster (Linux). Not safe on Pip."
    ),
    "DANGER": (
        "🔴 DANGER — HARD STOP\n"
        "   DO NOT attempt to read, chunk, or process this file in the current session.\n"
        "   Loading this file WILL crash the agent via context spiral.\n"
        "   \n"
        "   Required action:\n"
        "     1. Extract plain text ONLY (already done above if extraction succeeded)\n"
        "     2. Save extracted text to /tmp/<filename>.txt\n"
        "     3. STOP. Do not read the extracted text in this session.\n"
        "     4. Route to Atlas or Buster for heavy processing.\n"
        "   \n"
        "   This script exits with code 2 to prevent automated pipelines from proceeding.\n"
        "   Override with --force-dangerous (human authorization required)."
    ),
}

# Exit codes
EXIT_OK      = 0   # DIRECT or EXTRACT — safe to proceed
EXIT_CAUTION = 1   # CHUNK — proceed with care, subagent recommended
EXIT_DANGER  = 2   # DANGER — hard stop, do not proceed


# ── helpers ───────────────────────────────────────────────────────────────────

def file_size(path):
    return os.path.getsize(path)


def estimate_tokens(char_count):
    return char_count // CHARS_PER_TOKEN


def context_pct(tokens):
    return (tokens / CONTEXT_WINDOW) * 100


def classify(size_bytes):
    if size_bytes < THRESHOLDS["DIRECT"]:
        return "DIRECT"
    elif size_bytes < THRESHOLDS["EXTRACT"]:
        return "EXTRACT"
    elif size_bytes < THRESHOLDS["CHUNK"]:
        return "CHUNK"
    else:
        return "DANGER"


def extract_text(path, ext):
    """Best-effort plain text extraction. Returns (text, method, error)."""
    text, method, error = "", "none", None

    if ext == ".txt" or ext == ".md" or ext == ".csv":
        try:
            with open(path, "r", errors="replace") as f:
                text = f.read()
            method = "direct-read"
        except Exception as e:
            error = str(e)

    elif ext == ".docx":
        if HAS_DOCX:
            try:
                doc = _docx.Document(path)
                text = "\n".join(p.text for p in doc.paragraphs)
                method = "python-docx"
            except Exception as e:
                error = str(e)
        else:
            error = "python-docx not installed (pip3 install python-docx)"

    elif ext == ".pdf":
        if HAS_PDF:
            try:
                reader = _pdf.PdfReader(path)
                pages = []
                for page in reader.pages:
                    pages.append(page.extract_text() or "")
                text = "\n".join(pages)
                method = "PyPDF2"
            except Exception as e:
                error = str(e)
        else:
            error = "PyPDF2 not installed (pip3 install PyPDF2)"

    return text, method, error


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024:
            return f"{n:.1f} {unit}"
        n /= 1024
    return f"{n:.1f} TB"


# ── main ──────────────────────────────────────────────────────────────────────

def assess(path, as_json=False, force_dangerous=False):
    if not os.path.exists(path):
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    size  = file_size(path)
    ext   = os.path.splitext(path)[1].lower()
    fname = os.path.basename(path)
    cat   = classify(size)

    # extract text for richer token estimate
    text, extract_method, extract_error = extract_text(path, ext)
    actual_chars  = len(text) if text else None
    actual_tokens = estimate_tokens(actual_chars) if actual_chars else estimate_tokens(size // 2)
    ctx_pct       = context_pct(actual_tokens)

    # Determine safe chunk size for downstream reading
    if cat == "DIRECT":
        safe_chunk_chars = actual_chars or size
    elif cat == "EXTRACT":
        safe_chunk_chars = 40_000
    elif cat == "CHUNK":
        safe_chunk_chars = 40_000
    else:  # DANGER
        safe_chunk_chars = 0  # do not chunk in current session

    result = {
        "file":              fname,
        "path":              path,
        "size_bytes":        size,
        "size_human":        human_size(size),
        "extension":         ext,
        "category":          cat,
        "estimated_tokens":  actual_tokens,
        "context_window_pct": round(ctx_pct, 1),
        "extract_method":    extract_method,
        "extract_error":     extract_error,
        "safe_to_load":      cat == "DIRECT",
        "safe_chunk_chars":  safe_chunk_chars,
        "recommendation":    RECOMMENDATIONS[cat],
        "char_count":        actual_chars,
        "exit_code":         EXIT_DANGER if cat == "DANGER" else (EXIT_CAUTION if cat == "CHUNK" else EXIT_OK),
    }

    if as_json:
        print(json.dumps(result, indent=2))
        # Still exit with danger code even in JSON mode
        if cat == "DANGER" and not force_dangerous:
            sys.exit(EXIT_DANGER)
        elif cat == "CHUNK":
            sys.exit(EXIT_CAUTION)
        return result

    # ── human-readable report ──────────────────────────────────────────────
    bar_width = 40
    bar_fill  = int(min(ctx_pct / 100, 1.0) * bar_width)
    bar       = "█" * bar_fill + "░" * (bar_width - bar_fill)

    print(f"\n{'─'*55}")
    print(f"  📄  assess_input — {fname}")
    print(f"{'─'*55}")
    print(f"  Size:       {human_size(size)}  ({size:,} bytes)")
    print(f"  Type:       {ext or '(no extension)'}")
    if actual_chars:
        print(f"  Characters: {actual_chars:,}  (extracted via {extract_method})")
    print(f"  Est. tokens:{actual_tokens:,}")
    print(f"  Context %:  [{bar}] {ctx_pct:.1f}%")
    if ctx_pct > SAFE_CONTEXT_PCT * 100:
        print(f"  ⚠️  Exceeds safe context budget ({SAFE_CONTEXT_PCT*100:.0f}%)")
    print()
    print(f"  Category:   {cat}")
    if safe_chunk_chars > 0:
        print(f"  Safe chunk: {safe_chunk_chars:,} chars max per read")
    print()
    for line in RECOMMENDATIONS[cat].splitlines():
        print(f"  {line}")
    if extract_error:
        print(f"\n  ⚠️  Extraction warning: {extract_error}")
    if cat == "DANGER" and not force_dangerous:
        print(f"\n  🛑  Exiting with code 2. Use --force-dangerous to override (human auth required).")
    print(f"{'─'*55}\n")

    # Enforce exit codes — this is what prevents agents from proceeding
    if cat == "DANGER" and not force_dangerous:
        sys.exit(EXIT_DANGER)
    elif cat == "CHUNK":
        sys.exit(EXIT_CAUTION)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Pre-flight document size/type assessment before AI ingestion."
    )
    parser.add_argument("file", help="Path to document to assess")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    parser.add_argument("--force-dangerous", action="store_true",
                        help="Override DANGER hard stop (requires human authorization)")
    args = parser.parse_args()
    assess(args.file, as_json=args.json, force_dangerous=args.force_dangerous)


if __name__ == "__main__":
    main()
