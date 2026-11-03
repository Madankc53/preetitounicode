#!/usr/bin/env python3
"""Rewrite every embedded BS month-length table from scripts/bs_data.CANONICAL.

Usage: python3 scripts/sync_bs_data.py   (then run scripts/check_bs_data.py)
"""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import bs_data

ROOT = pathlib.Path(__file__).resolve().parent.parent
NOTE = ("2000-2084 BS match two independent open-source calendar datasets and 48 anchor dates "
        "(see scripts/bs_data.py); 2085-2090 are projections until NPNS publishes them.")

# (file, regex capturing 1=prefix, 2=body, 3=suffix, rows per line)
TARGETS = [
    ("date-converter/data/bs-calendar-data.js", r"(const BS_DATA = \{\n)(.*?)(\n\};)", 1),
    ("date-converter/index.html", r"(const bsData=\{\n)(.*?)(\n\};)", 1),
    ("bs-to-ad/index.html", r"(const BS=\{\n)(.*?)(\n\};)", 2),
    ("ad-to-bs/index.html", r"(const BS=\{\n)(.*?)(\n\};)", 2),
    ("today-nepali-date/index.html", r"(const BS = \{\n)(.*?)(\n\};)", 1),
    ("calculator/age-calculator.html", r"(const BS_TABLE = \{\n)(.*?)(\n    \};)", 1),
]

def main():
    for rel, pat, per in TARGETS:
        p = ROOT / rel
        s = p.read_text(encoding="utf-8")
        body = bs_data.js_rows("  " if "age-calc" not in rel else "      ", per)
        new, n = re.subn(pat, lambda m: m.group(1) + body + m.group(3), s, count=1, flags=re.S)
        if n != 1:
            sys.exit(f"{rel}: table block not found")
        if new != s:
            p.write_text(new, encoding="utf-8")
            print("updated", rel)
        else:
            print("ok     ", rel)

if __name__ == "__main__":
    main()
