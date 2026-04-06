# europepmc-search

Search Europe PMC for preprints and published papers across 30+ sources in one API call.
No API key required. Covers bioRxiv, medRxiv, Research Square, Preprints.org, PubMed, PMC, and more.

## When to use

- Finding preprints across ALL servers (not just bioRxiv/medRxiv) in one query
- Cross-server preprint monitoring for a topic (CF, rare disease, CRISPR, etc.)
- Full-text search including abstracts (stronger than bioRxiv API)
- Finding open-access papers on a topic
- Searching PubMed alongside preprints in one pass

## Script

`scripts/europepmc_search.py`

## Usage

```bash
# Preprints only, last 30 days
python3 ~/.openclaw/workspace/skills/europepmc-search/scripts/europepmc_search.py "cystic fibrosis CFTR" --preprints-only --days 30

# Summary stats only
python3 ~/.openclaw/workspace/skills/europepmc-search/scripts/europepmc_search.py "cystic fibrosis" --preprints-only --days 60 --summary

# All sources (published + preprints), last 14 days
python3 ~/.openclaw/workspace/skills/europepmc-search/scripts/europepmc_search.py "VEGF-A peptide" --days 14 --max 20

# Open access only
python3 ~/.openclaw/workspace/skills/europepmc-search/scripts/europepmc_search.py "zebrafish CRISPR" --open-access --max 10

# Specific source (PPR = preprints, MED = PubMed, PMC = full text)
python3 ~/.openclaw/workspace/skills/europepmc-search/scripts/europepmc_search.py "CHCHD2 mitochondria" --source MED --max 10

# List available source codes
python3 ~/.openclaw/workspace/skills/europepmc-search/scripts/europepmc_search.py --list-sources
```

## Arguments

| Argument | Description | Default |
|---|---|---|
| `keywords` | Search terms (Europe PMC query language) | — |
| `--days` | Search last N days | none (all time) |
| `--from` | Start date `YYYY-MM-DD` | — |
| `--to` | End date `YYYY-MM-DD` | — |
| `--max` | Max results (default: 25) | 25 |
| `--source` | Source code: `MED`, `PMC`, `PPR` | all |
| `--preprints-only` | Filter to preprints only (SRC:PPR) | off |
| `--open-access` | Open access papers only | off |
| `--pmid` | Fetch specific paper by PubMed ID | — |
| `--summary` | Print counts only, no full records | off |
| `--list-sources` | List source codes | — |

## Output

JSON with `total_hits_in_epmc` (full database count), `returned` (actual results), `by_source` (breakdown), and `results` array with: `title`, `authors`, `date`, `source`, `journal`, `doi`, `pmid`, `url`, `abstract` (500 char), `open_access`, `cited_by`.

## Source Codes

- `PPR` — Preprints (bioRxiv, medRxiv, Research Square, Preprints.org, etc.)
- `MED` — PubMed/MEDLINE (published, indexed)
- `PMC` — PubMed Central (full-text open access)
- `PAT` — Patents
- `CTX` — ClinicalTrials.gov

## Notes

- API: `https://www.ebi.ac.uk/europepmc/webservices/rest/search`
- Free, no key required; uses cursor-based pagination
- `sort` parameter not compatible with cursor pagination — results ordered by relevance
- No pip dependencies — uses `urllib` only
- Europe PMC query language supports field tags: `AUTH:`, `TITLE:`, `ABSTRACT:`, `JOURNAL:`, `OPEN_ACCESS:Y`

## Installed on

- Atlas ✅ (no pip deps needed)
- SCP: `scp atlas@100.90.91.58:~/.openclaw/workspace/skills/europepmc-search/scripts/europepmc_search.py <dest>`
