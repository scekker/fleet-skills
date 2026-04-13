#!/usr/bin/env python3
"""latex_paper.py — Build LaTeX papers for academic publication."""
import argparse, json, os, shutil, subprocess, sys
from datetime import datetime
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
TEMPLATES_DIR = SKILL_DIR / "templates"
LATEX_PATHS = [
    str(Path.home()/"Library/TinyTeX/bin/universal-darwin"),
    str(Path.home()/"Library/TinyTeX/bin/aarch64-darwin"),
    str(Path.home()/"Library/TinyTeX/bin/x86_64-darwin"),
    str(Path.home()/".TinyTeX/bin/x86_64-linux"),
    str(Path.home()/".TinyTeX/bin/aarch64-linux"),
    "/Library/TeX/texbin", "/usr/local/bin", "/usr/bin",
]

def find_latex_bin(binary="pdflatex"):
    found = shutil.which(binary)
    if found: return found
    for p in LATEX_PATHS:
        candidate = Path(p)/binary
        if candidate.exists(): return str(candidate)
    return None

def check_deps():
    results = {}
    for b in ["pdflatex","xelatex","bibtex","biber"]:
        path = find_latex_bin(b)
        results[b] = {"found": bool(path), "path": path or "not found"}
    results["pdflatex_preferred"] = results["pdflatex"]["found"]
    return results

def list_templates():
    templates = []
    if TEMPLATES_DIR.exists():
        for f in sorted(TEMPLATES_DIR.glob("*.tex")):
            desc = ""
            try:
                with open(f) as fh:
                    for line in fh:
                        if line.startswith("% DESCRIPTION:"):
                            desc = line.replace("% DESCRIPTION:","").strip(); break
            except: pass
            templates.append({"name":f.stem,"file":str(f),"description":desc})
    return templates

def scaffold_paper(title, output_dir, template="generic", authors=None, abstract="", affiliations=None):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    template_file = TEMPLATES_DIR/f"{template}.tex"
    if not template_file.exists(): template_file = TEMPLATES_DIR/"generic.tex"
    if not template_file.exists(): print(json.dumps({"error":f"Template not found: {template}"})); sys.exit(1)
    with open(template_file) as f: tex = f.read()
    date_str = datetime.now().strftime("%B %d, %Y")
    author_str = (", ".join(authors[:-1])+" and "+authors[-1]) if authors and len(authors)>1 else (authors[0] if authors else "Author Name")
    affil_str = affiliations[0] if affiliations else "Institution Name"
    tex = tex.replace("{{TITLE}}",title).replace("{{AUTHORS}}",author_str).replace("{{AFFILIATIONS}}",affil_str).replace("{{ABSTRACT}}",abstract or "Abstract goes here.").replace("{{DATE}}",date_str)
    with open(out/"main.tex","w") as f: f.write(tex)
    with open(out/"paper_metadata.json","w") as f:
        json.dump({"title":title,"authors":authors or ["Author Name"],"affiliations":affiliations or ["Institution"],"abstract":abstract,"template":template,"created":datetime.now().isoformat()},f,indent=2)
    with open(out/"references.bib","w") as f: f.write("% BibTeX references\n\n")
    with open(out/".gitignore","w") as f: f.write("*.aux\n*.log\n*.out\n*.bbl\n*.blg\n*.fls\n*.fdb_latexmk\n*.synctex.gz\n")
    print(json.dumps({"status":"created","output_dir":str(out),"main_tex":str(out/"main.tex"),"files":[p.name for p in out.iterdir()]},indent=2))

def compile_paper(tex_file, engine="pdflatex", bibtex=True, clean=False):
    tex_path = Path(tex_file).resolve()
    if not tex_path.exists(): print(json.dumps({"error":f"Not found: {tex_file}"})); sys.exit(1)
    work_dir = tex_path.parent
    latex_bin = find_latex_bin(engine)
    if not latex_bin: print(json.dumps({"error":f"{engine} not found","deps":check_deps()})); sys.exit(1)
    steps = []
    latex_cmd = [latex_bin,"-interaction=nonstopmode","-output-directory",str(work_dir),str(tex_path)]
    def run(cmd, label):
        r = subprocess.run(cmd, cwd=work_dir, capture_output=True, text=True)
        steps.append({"step":label,"returncode":r.returncode,"stdout_tail":r.stdout[-500:],"stderr_tail":r.stderr[-200:]})
        return r.returncode == 0
    run(latex_cmd, f"{engine} pass 1")
    if bibtex:
        bib_bin = find_latex_bin("bibtex")
        if bib_bin: run([bib_bin, str(work_dir/tex_path.with_suffix(".aux").name)], "bibtex")
    run(latex_cmd, f"{engine} pass 2")
    run(latex_cmd, f"{engine} pass 3")
    pdf_path = work_dir/tex_path.with_suffix(".pdf").name
    success = pdf_path.exists()
    if clean and success:
        for ext in [".aux",".log",".out",".bbl",".blg",".fls",".fdb_latexmk"]:
            a = work_dir/tex_path.with_suffix(ext).name
            if a.exists(): a.unlink()
    print(json.dumps({"status":"success" if success else "failed","pdf":str(pdf_path) if success else None,"engine":engine,"steps":steps},indent=2))

def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command")
    p_new = sub.add_parser("new")
    p_new.add_argument("title"); p_new.add_argument("--output","-o",required=True)
    p_new.add_argument("--template","-t",default="generic"); p_new.add_argument("--authors","-a",nargs="+")
    p_new.add_argument("--affiliations",nargs="+"); p_new.add_argument("--abstract")
    p_c = sub.add_parser("compile")
    p_c.add_argument("tex_file"); p_c.add_argument("--engine",default="pdflatex",choices=["pdflatex","xelatex","lualatex"])
    p_c.add_argument("--no-bibtex",action="store_true"); p_c.add_argument("--clean",action="store_true")
    sub.add_parser("list-templates"); sub.add_parser("check-deps")
    args = parser.parse_args()
    if args.command == "new":
        scaffold_paper(args.title,args.output,args.template,args.authors,args.abstract or "",args.affiliations)
    elif args.command == "compile":
        compile_paper(args.tex_file,args.engine,not args.no_bibtex,args.clean)
    elif args.command == "list-templates":
        print(json.dumps({"templates":list_templates()},indent=2))
    elif args.command == "check-deps":
        print(json.dumps(check_deps(),indent=2))
    else: parser.print_help()

if __name__ == "__main__": main()
