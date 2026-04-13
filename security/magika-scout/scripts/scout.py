#!/usr/bin/env python3
"""
scout.py — Magika-powered file type detection and routing utility.
Usage:
    python3 scout.py <file_or_url> [file_or_url ...]
    python3 scout.py --dir <directory> [--recursive]
    python3 scout.py --json   # machine-readable output

Exit codes:
    0 — all files matched expected type (or no expectation set)
    1 — one or more files failed type check or were unexpected
    2 — install error
"""

import sys, os, json, argparse, tempfile, urllib.request
from pathlib import Path

# ── Install magika if needed ───────────────────────────────────────────────────
try:
    from magika import Magika
    from magika.types import MagikaResult
except ImportError:
    import subprocess
    print("Installing magika...", file=sys.stderr)
    subprocess.check_call([sys.executable, "-m", "pip", "install", "magika", "-q"])
    from magika import Magika
    from magika.types import MagikaResult

# ── Router map: magika content type → recommended parser ─────────────────────
ROUTER = {
    "pdf":          "pdfplumber / pymupdf",
    "html":         "readability / beautifulsoup4",
    "xml":          "lxml / xml.etree",
    "json":         "json.loads",
    "csv":          "pandas.read_csv",
    "xls":          "pandas.read_excel",
    "xlsx":         "pandas.read_excel",
    "docx":         "python-docx",
    "txt":          "open().read()",
    "python":       "ast.parse / exec",
    "shell":        "subprocess (review first)",
    "zip":          "zipfile",
    "tar":          "tarfile",
    "elf":          "⚠️  EXECUTABLE — do not auto-parse",
    "pe":           "⚠️  EXECUTABLE — do not auto-parse",
    "unknown":      "⚠️  UNKNOWN — manual review required",
}

SAFE_TYPES = {
    "pdf", "html", "xml", "json", "csv", "xls", "xlsx",
    "docx", "txt", "python", "markdown", "rst",
}

DANGEROUS_TYPES = {"elf", "pe", "macho", "shell", "batch"}


def fetch_url(url: str) -> Path:
    """Download URL to a temp file, preserving extension hint."""
    suffix = Path(url.split("?")[0]).suffix or ".bin"
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    urllib.request.urlretrieve(url, tmp.name)
    return Path(tmp.name)


def scan(paths: list[str], recursive: bool = False) -> list[dict]:
    m = Magika()
    results = []

    all_files = []
    for p in paths:
        if p.startswith("http://") or p.startswith("https://"):
            tmp = fetch_url(p)
            all_files.append((tmp, p))  # (local_path, display_name)
        else:
            path = Path(p)
            if path.is_dir() and recursive:
                for f in path.rglob("*"):
                    if f.is_file():
                        all_files.append((f, str(f)))
            else:
                all_files.append((path, str(path)))

    for local, display in all_files:
        try:
            result: MagikaResult = m.identify_path(local)
            ct = result.output.label
            score = result.score
            mime = result.output.mime_type
            parser = ROUTER.get(ct, f"check docs for '{ct}'")
            safe = ct in SAFE_TYPES
            dangerous = ct in DANGEROUS_TYPES

            results.append({
                "path": display,
                "type": ct,
                "mime": mime,
                "confidence": round(score, 3),
                "parser": parser,
                "safe": safe,
                "dangerous": dangerous,
            })
        except Exception as e:
            results.append({
                "path": display,
                "type": "error",
                "mime": None,
                "confidence": 0,
                "parser": "N/A",
                "safe": False,
                "dangerous": False,
                "error": str(e),
            })

    return results


def print_human(results: list[dict]) -> int:
    exit_code = 0
    for r in results:
        flag = "✅" if r["safe"] else ("🚨" if r["dangerous"] else "⚠️ ")
        conf = f"{r['confidence']*100:.0f}%"
        print(f"{flag} {r['path']}")
        print(f"   type={r['type']}  mime={r['mime']}  confidence={conf}")
        print(f"   parser → {r['parser']}")
        if r.get("error"):
            print(f"   error: {r['error']}")
        if r["dangerous"]:
            exit_code = 1
        if r["type"] in ("error", "unknown"):
            exit_code = 1
    return exit_code


def main():
    parser = argparse.ArgumentParser(description="Magika scout — file type detection + routing")
    parser.add_argument("paths", nargs="*", help="Files or URLs to scan")
    parser.add_argument("--dir", help="Directory to scan")
    parser.add_argument("--recursive", "-r", action="store_true")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    targets = list(args.paths)
    if args.dir:
        targets.append(args.dir)
    if not targets:
        parser.print_help()
        sys.exit(0)

    results = scan(targets, recursive=args.recursive)

    if args.json:
        print(json.dumps(results, indent=2))
        sys.exit(0)

    exit_code = print_human(results)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
