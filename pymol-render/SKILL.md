---
name: pymol-render
description: >
  Render publication-quality protein structure images using headless PyMOL. Use when
  you need to visualize a PDB structure, generate figures for papers or decks, or
  create structure images for any protein design project. Accepts PDB IDs (auto-fetched
  from RCSB) or local .pdb files. Six rendering styles available: cartoon, surface,
  sticks, spheres, ribbon, publication. Outputs 300 DPI PNG. Requires PyMOL installed
  on the target node. Triggers on phrases like "render structure", "visualize PDB",
  "make a figure of", "show me the structure", "PyMOL render", "protein image".
---

# PyMOL Structure Renderer

Renders publication-quality protein structure images headlessly (no GUI required).
Accepts PDB IDs or local files, auto-fetches from RCSB when given a PDB ID.

## Requirements

- PyMOL installed and in PATH (`pymol -c` must work)
- Python 3 + `requests` library (`pip install requests`)
- Works on: Buster ✅ (confirmed), macOS nodes (requires PyMOL install)

**Install PyMOL on macOS:**
```bash
brew install pymol
# or via conda:
conda install -c conda-forge pymol-open-source
```

**Install PyMOL on Ubuntu (Buster):**
```bash
sudo apt-get install pymol
# or via conda env:
conda install -c conda-forge pymol-open-source
```

## Usage

```bash
python3 skills/pymol-render/render_structure.py \
  <PDB_ID_or_file.pdb> \
  [output.png] \
  [style] \
  [width] \
  [height]
```

### Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `PDB_ID_or_file` | required | PDB ID (e.g. `1ATP`) or path to `.pdb` file |
| `output.png` | `<input>.png` | Output image path |
| `style` | `cartoon` | Rendering style (see below) |
| `width` | `1200` | Image width in pixels |
| `height` | `900` | Image height in pixels |

### Rendering Styles

| Style | Best For |
|-------|----------|
| `cartoon` | General protein overview, secondary structure visible, rainbow coloring |
| `surface` | Binding site visualization, surface accessibility |
| `sticks` | Small molecules, active site detail |
| `spheres` | Space-filling representation |
| `ribbon` | Backbone trace, cleaner than cartoon |
| `publication` | High-quality figures — fancy helices, highlight coloring, ray shadows |

### Examples

```bash
# Render VEGF-A structure from RCSB (PDB: 2VPF)
python3 skills/pymol-render/render_structure.py 2VPF vegf_a.png cartoon

# Render local file in publication style, high resolution
python3 skills/pymol-render/render_structure.py /tmp/binder_design.pdb \
  binder_figure.png publication 2400 1800

# Surface view of binding site
python3 skills/pymol-render/render_structure.py 1ATP atp_surface.png surface

# Quick spheres render
python3 skills/pymol-render/render_structure.py 4ZFF peptide.png spheres
```

## Output

- PNG file at specified path
- 300 DPI, suitable for papers and presentations
- Black background (standard for structural biology figures)
- Anti-aliasing enabled

## Notes

- PDB files are auto-fetched from `https://files.rcsb.org/download/<ID>.pdb`
- Temp files are cleaned up automatically
- For very large structures, increase timeout in script if needed (default: 180s)
- The `vegfa_test.png` in this directory is a rendered example (VEGF-A, cartoon style)
- On Buster: use within a conda env that has pymol installed

## Integration with UViiVe Pipeline

Use after protein design runs to generate figures for:
- Deck slides (use `publication` style, 1920×1080)
- Paper figures (use `publication` style, 2400×1800, 300 DPI)
- Quick sanity checks (use `cartoon` style, default size)
- CAST client deliverables (use `surface` or `publication` style)
