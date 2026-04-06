#!/usr/bin/env python3
"""install_latex.py — Self-install TinyTeX for fleet agents."""
import argparse, json, os, shutil, subprocess, sys, urllib.request
from pathlib import Path

TINYTEX_INSTALLER_URL = "https://yihui.org/tinytex/install-unx.sh"
REQUIRED_PACKAGES = [
    "natbib","booktabs","lineno","setspace","geometry","hyperref",
    "preprint","microtype","titlesec","caption","lmodern",
    "collection-fontsrecommended",
]
TINYTEX_BIN_PATHS = {
    "darwin": [
        Path.home()/"Library/TinyTeX/bin/universal-darwin",
        Path.home()/"Library/TinyTeX/bin/aarch64-darwin",
        Path.home()/"Library/TinyTeX/bin/x86_64-darwin",
    ],
    "linux": [
        Path.home()/".TinyTeX/bin/x86_64-linux",
        Path.home()/".TinyTeX/bin/aarch64-linux",
    ],
}

def find_tinytex_bin():
    import platform
    plat = "darwin" if platform.system() == "Darwin" else "linux"
    for path in TINYTEX_BIN_PATHS.get(plat, []):
        if path.exists() and (path/"pdflatex").exists():
            return path
    return None

def find_pdflatex():
    tin = find_tinytex_bin()
    if tin: return str(tin/"pdflatex")
    return shutil.which("pdflatex")

def find_tlmgr():
    tin = find_tinytex_bin()
    if tin: return str(tin/"tlmgr")
    return shutil.which("tlmgr")

def check_status():
    pdflatex = find_pdflatex(); tlmgr = find_tlmgr(); tinytex_bin = find_tinytex_bin()
    return {"tinytex_installed": bool(tinytex_bin), "tinytex_bin": str(tinytex_bin) if tinytex_bin else None,
            "pdflatex": pdflatex or "not found", "tlmgr": tlmgr or "not found",
            "system_pdflatex": shutil.which("pdflatex")}

def install_tinytex():
    installer = Path("/tmp/install-tinytex.sh")
    print("Downloading TinyTeX installer...", flush=True)
    urllib.request.urlretrieve(TINYTEX_INSTALLER_URL, installer)
    print("Running installer (~2-3 min)...", flush=True)
    subprocess.run(["sh", str(installer)])
    installer.unlink(missing_ok=True)
    bin_dir = find_tinytex_bin()
    if not bin_dir: return False, "TinyTeX installed but binary not found"
    return True, str(bin_dir)

def install_packages(tlmgr_path):
    results = {}
    for pkg in REQUIRED_PACKAGES:
        r = subprocess.run([tlmgr_path,"install",pkg], capture_output=True, text=True)
        results[pkg] = "ok" if ("already present" in r.stdout or r.returncode==0) else "failed"
    return results

def verify_compile():
    pdflatex = find_pdflatex()
    if not pdflatex: return False, "pdflatex not found"
    test_dir = Path("/tmp/tinytex-verify"); test_dir.mkdir(exist_ok=True)
    test_tex = test_dir/"test.tex"
    test_tex.write_text(r"""\documentclass{article}
\usepackage{natbib,booktabs,lineno,setspace,geometry,hyperref}
\begin{document}Hello fleet!\end{document}""")
    r = subprocess.run([pdflatex,"-interaction=nonstopmode","-output-directory",str(test_dir),str(test_tex)], capture_output=True, text=True)
    pdf = test_dir/"test.pdf"; success = pdf.exists()
    for f in test_dir.iterdir(): f.unlink()
    test_dir.rmdir()
    return success, "compile test passed" if success else r.stdout[-300:]

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--packages-only", action="store_true")
    args = parser.parse_args()
    status = check_status()
    if args.check:
        ok, msg = verify_compile() if status["tinytex_installed"] else (False,"not installed")
        print(json.dumps({**status,"compile_test":ok,"compile_msg":msg},indent=2)); return
    if args.packages_only:
        tlmgr = find_tlmgr()
        if not tlmgr: print(json.dumps({"error":"tlmgr not found"})); sys.exit(1)
        print(json.dumps({"packages":install_packages(tlmgr)},indent=2)); return
    if status["tinytex_installed"]:
        print(json.dumps({"status":"already_installed",**status}))
        tlmgr = find_tlmgr()
        if tlmgr:
            print("Ensuring packages...", flush=True)
            ok, msg = verify_compile()
            print(json.dumps({"packages":install_packages(tlmgr),"compile_test":ok,"compile_msg":msg},indent=2))
        return
    print(json.dumps({"status":"installing","note":"No sudo required"}))
    success, msg = install_tinytex()
    if not success: print(json.dumps({"status":"install_failed","error":msg})); sys.exit(1)
    tlmgr = find_tlmgr()
    ok, cmsg = verify_compile()
    print(json.dumps({"status":"success","tinytex_bin":str(find_tinytex_bin()),
        "pdflatex":find_pdflatex(),"packages":install_packages(tlmgr),
        "compile_test":ok,"compile_msg":cmsg},indent=2))

if __name__ == "__main__": main()
