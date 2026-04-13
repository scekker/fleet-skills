# openalex-search

Search OpenAlex for scholarly works including preprints across all major servers and repositories.
No API key required (uses polite pool with atlas@uviive.com email). 450M+ works indexed.

## When to use

- Cross-disciplinary sweeps (finds drug design in chemistry *and* biology preprints)
- When you want one query to cover arXiv + bioRxiv + medRxiv + Zenodo + institutional repos
- Semantic search: finds conceptually related work even without exact keywords
- Fetching a specific paper by DOI across any platform
- Finding open-access versions of papers

## Script

`scripts/openalex_search.py`

## Usage

```bash
# Preprints only, last 30 days
python3 ~/.openclaw/workspace/skills/openalex-search/scripts/openalex_search.py "cystic fibrosis CFTR" --preprints --days 30

# Summary stats
python3 ~/.openclaw/workspace/skills/openalex-search/scripts/openalex_search.py "cystic fibrosis CFTR" --preprints --days 60 --summary

# All work types, last 14 days
python3 ~/.openclaw/workspace/skills/openalex-search/scripts/openalex_search.py "VEGF-A peptide UV skin" --days 14 --max 20

# Open access papers on a topic
python3 ~/.openclaw/workspace/skills/openalex-search/scripts/openalex_search.py "zebrafish CRISPR mitochondria" --open-access --max 10

# Fetch by DOI
python3 ~/.openclaw/workspace/skills/openalex-search/scripts/openalex_search.py --doi 10.1101/2024.01.23.576694

# List work types
python3 ~/.openclaw/workspace/skills/openalex-search/scripts/openalex_search.py --list-types
```

## Arguments

| Argument | Description | Default |
|---|---|---|
| `keywords` | Search terms (semantic + keyword) | — |
| `--days` | Search last N days | none |
| `--from` | Start date `YYYY-MM-DD` | — |
| `--to` | End date `YYYY-MM-DD` | — |
| `--max` | Max results | 25 |
| `--sort` | Sort field:direction | `publication_date:desc` |
| `--preprints` | Preprints only (`type:preprint`) | off |
| `--type` | Work type filter | all |
| `--open-access` | Open access only | off |
| `--doi` | Fetch by DOI | — |
| `--summary` | Print counts only | off |
| `--list-types` | List work type options | — |

## Output

JSON with `total_in_openalex` (full count), `returned` (actual), `by_type`, and `results` with:
`title`, `authors`, `date`, `type`, `source`, `doi`, `url`, `abstract` (reconstructed from inverted index), `cited_by`, `open_access`, `concepts` (top 5 topics).

## Notes

- API: `https://api.openalex.org` — free, no key required
- Uses **polite pool** (atlas@uviive.com in User-Agent) — higher rate limits
- Semantic search means results may be conceptually related but not exact matches — review carefully
- Abstract is reconstructed from OpenAlex's inverted index (word positions) — may have minor artifacts
- Source field may be empty for some preprints — use DOI/URL to trace back
- No pip dependencies — uses `urllib` only

## Coverage

OpenAlex indexes: bioRxiv, medRxiv, arXiv, Zenodo, institutional repositories, all major journals (Elsevier, Springer, Nature, Cell, PLOS, etc.), patents (partial), datasets.

## Installed on

- Atlas ✅ (no pip deps needed)
- SCP: `scp atlas@100.90.91.58:~/.openclaw/workspace/skills/openalex-search/scripts/openalex_search.py <dest>`
