#!/usr/bin/env python3
"""
pymol-render: Headless PyMOL structure renderer
Usage: python3 render_structure.py <PDB_ID_or_file> [output.png] [style] [width] [height]

Styles: cartoon (default), surface, sticks, spheres, ribbon, publication
"""

import sys
import os
import subprocess
import tempfile

try:
    import requests
except ImportError:
    import urllib.request as requests_fallback
    requests = None

def fetch_pdb(pdb_id, out_path):
    """Download PDB file from RCSB."""
    url = f"https://files.rcsb.org/download/{pdb_id.upper()}.pdb"
    if requests:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        with open(out_path, 'w') as f:
            f.write(r.text)
    else:
        import urllib.request
        urllib.request.urlretrieve(url, out_path)
    return out_path

def render(pdb_input, output_png="structure.png", style="cartoon", width=1200, height=900):
    """Render structure using PyMOL headless."""

    pdb_file = pdb_input
    tmp_pdb = None

    if not os.path.exists(pdb_input):
        tmp_pdb = tempfile.mktemp(suffix=".pdb")
        print(f"Fetching {pdb_input.upper()} from RCSB...")
        fetch_pdb(pdb_input, tmp_pdb)
        pdb_file = tmp_pdb

    pymol_script = f"""
load {pdb_file}, structure
hide everything
bg_color black
set ray_shadows, 0
set antialias, 2
set ray_trace_fog, 0
set depth_cue, 0
set ray_opaque_background, 1
"""

    if style == "cartoon":
        pymol_script += """
show cartoon, structure
spectrum count, rainbow, structure
"""
    elif style == "surface":
        pymol_script += """
show surface, structure
color orange, structure
set transparency, 0.15
"""
    elif style == "sticks":
        pymol_script += """
show sticks, structure
util.cbao structure
"""
    elif style == "spheres":
        pymol_script += """
show spheres, structure
color orange, structure
"""
    elif style == "ribbon":
        pymol_script += """
show ribbon, structure
spectrum count, rainbow, structure
"""
    elif style == "publication":
        pymol_script += """
show cartoon, structure
set cartoon_fancy_helices, 1
set cartoon_highlight_color, grey70
color orange, structure and ss h
color tv_yellow, structure and ss s
color white, structure and ss l+''
set ray_shadows, 1
set ambient, 0.3
"""

    pymol_script += f"""
orient structure
zoom structure, 5
ray {width}, {height}
png {output_png}, dpi=300
quit
"""

    script_file = tempfile.mktemp(suffix=".pml")
    with open(script_file, 'w') as f:
        f.write(pymol_script)

    print(f"Rendering {pdb_input} → {output_png} (style={style}, {width}x{height})...")
    result = subprocess.run(
        ["pymol", "-c", script_file],
        capture_output=True, text=True, timeout=180
    )

    os.unlink(script_file)
    if tmp_pdb and os.path.exists(tmp_pdb):
        os.unlink(tmp_pdb)

    if result.returncode != 0:
        print(f"PyMOL stderr:\n{result.stderr[-1000:]}")
        raise RuntimeError(f"PyMOL exited with code {result.returncode}")

    if os.path.exists(output_png):
        size = os.path.getsize(output_png)
        print(f"✅ Rendered: {output_png} ({size/1024:.0f} KB)")
        return output_png
    else:
        print(f"PyMOL stdout: {result.stdout[-500:]}")
        raise FileNotFoundError(f"PyMOL did not produce {output_png}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nExample: python3 render_structure.py 1ATP output.png cartoon 1200 900")
        sys.exit(1)

    pdb_input = sys.argv[1]
    output    = sys.argv[2] if len(sys.argv) > 2 else f"{os.path.splitext(os.path.basename(pdb_input))[0]}.png"
    style     = sys.argv[3] if len(sys.argv) > 3 else "cartoon"
    width     = int(sys.argv[4]) if len(sys.argv) > 4 else 1200
    height    = int(sys.argv[5]) if len(sys.argv) > 5 else 900

    render(pdb_input, output, style, width, height)
