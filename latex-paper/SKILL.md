---
name: latex-paper
version: 0.1.0
author: atlas
requires:
  - python>=3.9
tested-on:
  - macos-arm64
  - ubuntu-22.04
description: >
  Build and compile LaTeX papers for academic publication. Use when: (1) drafting a new paper from scratch (scaffolds directory with template + bibliography), (2) compiling an existing .tex file to PDF, (3) need journal-specific formatting (generic, bioRxiv preprint, Nature-style, PLOS). Self-installs LaTeX via TinyTeX — no sudo required, works on any fleet machine. Run scripts/install_latex.py once per machine, then use latex_paper.py to build papers.
---

# latex-paper

Scaffold and compile academic papers using LaTeX. Four journal templates included.
**Self-installing** — no sudo, no system access needed.

## First-time setup (run once per machine)

```bash
python3 ~/.openclaw/workspace/skills/latex-paper/scripts/install_latex.py
```

Installs TinyTeX to `~/Library/TinyTeX` (macOS) or `~/.TinyTeX` (Linux) — ~300MB, no sudo required. Takes ~3 minutes.

```bash
python3 ~/.openclaw/workspace/skills/latex-paper/scripts/install_latex.py --check
```

## Build a paper

```bash
python3 ~/.openclaw/workspace/skills/latex-paper/scripts/latex_paper.py new \
  "My Paper Title" --template biorxiv \
  --output ~/papers/my-paper/ \
  --authors "Author Name" --affiliations "Institution"

python3 ~/.openclaw/workspace/skills/latex-paper/scripts/latex_paper.py compile \
  ~/papers/my-paper/main.tex --clean
```

## Templates

- `generic` — Clean 12pt article, journal-agnostic
- `biorxiv` — bioRxiv/medRxiv, double-spaced, line numbers
- `nature-style` — Two-column, tight, superscript citations
- `plos` — PLOS ONE/Biology, structured abstract, ethics statement

## Commands

### install_latex.py
```
--check          Verify status + compile test
--packages-only  Add packages to existing install
```

### latex_paper.py new
```
--template    generic|biorxiv|nature-style|plos
--authors     Author name(s)
--affiliations  Affiliation(s)
--abstract    Abstract text
```

### latex_paper.py compile
```
--engine    pdflatex|xelatex|lualatex
--no-bibtex  Skip bibliography pass
--clean      Remove build artifacts
```

### latex_paper.py list-templates
### latex_paper.py check-deps
