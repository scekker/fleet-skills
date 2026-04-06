# biorxiv-search Skill

Search bioRxiv and medRxiv preprints via the official biorxiv.org API.
No API key required. No Python package required beyond `requests` (stdlib-adjacent).

## When to use
- User asks about recent bioRxiv/medRxiv preprints on a topic
- SciPulse-style literature scouting on life sciences topics
- Checking for new structural biology, genomics, or biotech preprints

## Script
`skills/biorxiv-search/scripts/biorxiv_search.py`

## Usage

```bash
# Search bioRxiv for VEGF-A peptide papers in last 30 days
python3 ~/.openclaw/workspace/skills/biorxiv-search/scripts/biorxiv_search.py "VEGF-A peptide" --server biorxiv --days 30 --max 10

# Search medRxiv for clinical trial results
python3 ~/.openclaw/workspace/skills/biorxiv-search/scripts/biorxiv_search.py "rosacea treatment" --server medrxiv --days 60 --max 5

# JSON output for programmatic use
python3 ~/.openclaw/workspace/skills/biorxiv-search/scripts/biorxiv_search.py "zebrafish CRISPR" --json
```

## Parameters
- `query` — space-separated terms; ALL must appear in title or abstract
- `--server` — `biorxiv` (default) or `medrxiv`
- `--days` — how many days back to search (default: 30)
- `--max` — max results to return (default: 10)
- `--json` — output raw JSON

## Output fields
- `doi`, `title`, `authors`, `date`, `category`, `abstract` (truncated to 400 chars), `url`, `server`

## Notes
- Search is client-side filtered: fetches all papers in date range, then filters by query terms
- For very broad date ranges or very common terms, use `--days` to limit fetch size
- Rate limit: ~3 req/sec (built-in 0.4s delay between pages)
- API docs: https://api.biorxiv.org
