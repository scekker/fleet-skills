---
name: arxiv-search
description: >
  Search arXiv for academic papers using the official arXiv API. Use when: (1) looking up recent preprints or papers by topic, (2) fetching paper metadata (title, authors, abstract, PDF URL, DOI) for any domain, (3) scoping searches to specific arXiv categories (e.g. cs.AI, q-bio.GN, q-bio.BM, physics.bio-ph), (4) seeding literature reviews or SciPulse scouting runs. No API key required. Works on any fleet machine with Python 3 and the arxiv package installed.
---

# arXiv Search

Query the arXiv API for academic papers. Free, no key required.

## Quick Start

```bash
python3 skills/arxiv-search/scripts/arxiv_search.py "VEGF-A peptide inhibitor" --max 10
```

Returns JSON array with: `arxiv_id`, `title`, `authors` (up to 6), `abstract` (500 chars), `published`, `updated`, `pdf_url`, `categories`, `journal_ref`, `doi`.

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--max N` | 10 | Results (max 50) |
| `--sort` | `relevance` | `relevance` / `date` / `updated` |
| `--category` | none | arXiv category filter (e.g. `cs.AI`, `q-bio.GN`) |

## Category Reference

See `references/arxiv-categories.md` for full list. Key categories for fleet use:

- `cs.AI` — AI/ML general
- `cs.LG` — Machine learning
- `cs.CL` — NLP/language models
- `q-bio.GN` — Genomics
- `q-bio.BM` — Biomolecules
- `q-bio.QM` — Quantitative methods in biology
- `physics.bio-ph` — Biological physics

## Installation (per machine)

```bash
pip3 install arxiv --break-system-packages
```

Verify: `python3 -c "import arxiv; print('OK')"`

**Fleet status:** See `references/fleet-install-status.md`

## Usage in Agent Context

Call the script via `exec` tool and parse the JSON output:

```python
# Example: search + summarize top 5 results
python3 skills/arxiv-search/scripts/arxiv_search.py \
  "zebrafish CHCHD2 mitochondria" --max 5 --sort date
```

For programmatic use within Python agents, import directly:

```python
import sys
sys.path.insert(0, 'skills/arxiv-search/scripts')
from arxiv_search import search
results = search("sparse attention transformer", max_results=10, category="cs.LG")
```
