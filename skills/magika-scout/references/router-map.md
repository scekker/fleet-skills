# Router Map — Magika Content Types → Parsers

Full reference for `scout.py` routing decisions. Extend `ROUTER` dict in `scout.py` to add custom mappings.

## Document Types

| Magika type | MIME | Recommended parser | Notes |
|-------------|------|--------------------|-------|
| `pdf` | application/pdf | `pdfplumber` / `pymupdf` | Validate size >10KB — small PDFs may be HTML stubs (PMC gotcha) |
| `html` | text/html | `readability` / `beautifulsoup4` | Common false positive when PDF fetch fails silently |
| `xml` | text/xml | `lxml` / `xml.etree` | Includes XBRL (SEC filings) |
| `docx` | application/vnd.openxmlformats... | `python-docx` | |
| `xls` | application/vnd.ms-excel | `pandas.read_excel` | |
| `xlsx` | application/vnd.openxmlformats... | `pandas.read_excel` | |
| `txt` | text/plain | `open().read()` | Low-confidence detections common |
| `markdown` | text/markdown | `open().read()` / `mistune` | |
| `rst` | text/x-rst | `docutils` | |

## Data Types

| Magika type | MIME | Recommended parser | Notes |
|-------------|------|--------------------|-------|
| `json` | application/json | `json.loads` | |
| `csv` | text/csv | `pandas.read_csv` | |
| `tsv` | text/tab-separated-values | `pandas.read_csv(sep='\t')` | |

## Code Types

| Magika type | MIME | Recommended parser | Notes |
|-------------|------|--------------------|-------|
| `python` | text/x-python | `ast.parse` / exec | Review before exec |
| `javascript` | text/javascript | Review before exec | |
| `shell` | text/x-shellscript | `subprocess` | **Review carefully** |
| `batch` | text/x-msdos-batch | `subprocess` | **Review carefully** |

## Archive Types

| Magika type | MIME | Recommended parser | Notes |
|-------------|------|--------------------|-------|
| `zip` | application/zip | `zipfile` | Scout contents after extraction |
| `tar` | application/x-tar | `tarfile` | Scout contents after extraction |
| `gzip` | application/gzip | `gzip` | |

## Dangerous / Executable Types (🚨 exit code 1)

| Magika type | Description | Action |
|-------------|-------------|--------|
| `elf` | Linux/Unix executable | Do not parse — flag for review |
| `pe` | Windows executable (.exe/.dll) | Do not parse — flag for review |
| `macho` | macOS executable | Do not parse — flag for review |
| `shell` | Shell script | Review before any execution |
| `batch` | Windows batch script | Review before any execution |

## Common False Positives

| Situation | What Magika sees | What it actually is | Fix |
|-----------|-----------------|---------------------|-----|
| PMC PDF stub | `html` (~1,800 bytes) | Failed PDF fetch | Use PMC FTP path, validate size >10KB |
| Empty/corrupted download | `unknown` low confidence | Network error | Re-fetch, check response code |
| Python venv binary | `macho` or `elf` | Normal interpreter binary | Exclude `.venv/` dirs from scans |
| XBRL filing | `xml` | SEC financial data | Parse with `lxml` + XBRL namespace |

## Fleet-Specific Notes

- **Buster pipeline**: Magika installed at `~/timesfm-env` — use `source ~/timesfm-env/bin/activate` or install separately
- **PMC batch downloads**: Always scout before parsing — silent HTML stubs are the #1 failure mode
- **SEC EDGAR**: Mix of HTML, XBRL, PDF — scout each file in a filing package before routing
- **Endpoint Arena / trial docs**: Expect PDF and HTML — flag anything else
