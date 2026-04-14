# SKILL.md — patent-search

## Purpose
Search US (USPTO) and European (EPO OPS) patent databases programmatically. Use for IP landscape sweeps, prior art searches, and provisional claim preparation.

---

## Credentials

### EPO OPS (European Patent Office)
- **Working app:** Unicorn | Owner: stephen.ekker@gmail.com
- **Consumer Key:** `E3iArveOSxaBKXbzDuVBBe6smENQinoMyGp3mCxzJ3oRqQfw`
- **Consumer Secret:** `ZiggWUAn0XWfn765ATQH2ryzUVgt1mlK0XPmTKfwkix6AeDYMRNKGfNBXxQp49im`
- Stored in: `config/api-keys.env` as `EPO_UNICORN_KEY` / `EPO_UNICORN_SECRET`
- **Confirmed working:** 2026-04-07 ✅

### USPTO ODP (US Patent and Trademark Office)
- **API Key:** `mbbruxqjbnzcbotyqpmitqmrclxqzc`
- **Header:** `X-Api-Key`
- **Base URL:** `https://api.uspto.gov/api/v1/patent/applications/search`
- Stored in: `config/api-keys.env` as `USPTO_ODP_KEY`
- **Confirmed working:** 2026-03-31 ✅

---

## EPO OPS — Step by Step

### Step 1 — Get access token (valid 20 min)
```bash
TOKEN=$(curl -s -X POST "https://ops.epo.org/3.2/auth/accesstoken" \
  -u "E3iArveOSxaBKXbzDuVBBe6smENQinoMyGp3mCxzJ3oRqQfw:ZiggWUAn0XWfn765ATQH2ryzUVgt1mlK0XPmTKfwkix6AeDYMRNKGfNBXxQp49im" \
  -d "grant_type=client_credentials" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
echo "Token: $TOKEN"
```

### Step 2 — Search by title/abstract keyword
```bash
# URL-encode spaces as %20, use 'ta=' for title+abstract
curl -s "https://ops.epo.org/3.2/rest-services/published-data/search/biblio?q=ta%3D%22VEGF%22+and+ta%3D%22peptide%22&Range=1-10" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

### Step 3 — Search by applicant name
```bash
curl -s "https://ops.epo.org/3.2/rest-services/published-data/search/biblio?q=pa%3D%22C3+AI%22&Range=1-10" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

### Step 4 — Fetch full biblio for a specific patent
```bash
# Format: CC.DOCNUMBER.KIND (e.g. US.20240370709.A1)
curl -s "https://ops.epo.org/3.2/rest-services/published-data/publication/docdb/US.20240370709.A1/biblio" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/json"
```

### Query syntax reference
| Prefix | Meaning |
|--------|---------|
| `ta=` | Title + Abstract |
| `pa=` | Applicant/Assignee |
| `in=` | Inventor |
| `pn=` | Publication number |
| `ic=` | IPC classification |
| `cl=` | CPC classification |
| `pd=` | Publication date (YYYYMMDD) |

Combine with `and`, `or`, `not`. Use quotes for phrases.

---

## USPTO ODP — Step by Step

### Step 1 — Full-text search
```bash
curl -s -X POST "https://api.uspto.gov/api/v1/patent/applications/search" \
  -H "X-Api-Key: mbbruxqjbnzcbotyqpmitqmrclxqzc" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "\"VEGF\" AND \"peptide\" AND \"hallucination\"",
    "dateRangeData": {"field": "patentApplicationFilingDate", "startDate": "2020-01-01", "endDate": "2026-04-07"},
    "start": 0,
    "rows": 10,
    "largeTextSearchFlag": "N"
  }'
```

### Step 2 — Search by assignee
```bash
curl -s -X POST "https://api.uspto.gov/api/v1/patent/applications/search" \
  -H "X-Api-Key: mbbruxqjbnzcbotyqpmitqmrclxqzc" \
  -H "Content-Type: application/json" \
  -d '{
    "q": "assigneeEntityName:\"C3 AI\"",
    "start": 0,
    "rows": 10
  }'
```

### Step 3 — Parse results
Key fields in response:
- `patentApplicationNumber` — application number
- `inventionTitle` — title
- `assigneeEntityName` — assignee
- `patentApplicationFilingDate` — filing date
- `applicationStatusDescriptionText` — status (Patented, Pending, etc.)
- `abstractText` — abstract

---

## Full Sweep Pattern (both databases)

For any IP landscape analysis:
1. Get EPO token (Step 1 above)
2. Run EPO search on key terms → note total count + top 5 results
3. Run USPTO search on same terms → note total count + top 5 results
4. Search by known competitor names (both databases)
5. Check specific patent numbers of interest (full biblio fetch)
6. Summarize: total prior art found, closest hits, white space

---

## Gotchas

- **EPO token expires in 20 min** — re-request if you get 401 mid-session
- **EPO "Unicorn" app is the working one** — UViiVE 1/2/3 apps all return 401 (unknown EPO backend issue as of Apr 7 2026)
- **USPTO pagination:** use `start` + `rows` (max 100/page)
- **EPO pagination:** use `Range` header (e.g. `1-25`, `26-50`)
- **EPO rate limit:** 30 requests/min on free tier — add `sleep 2` in loops
- **USPTO full text:** set `largeTextSearchFlag: "Y"` for claims/description search (slower)

---

*Skill authored by Uvy 🦾 | 2026-04-07*
*EPO OPS confirmed working: 490 results on VEGF+peptide test*
*USPTO ODP confirmed working: 2026-03-31*
