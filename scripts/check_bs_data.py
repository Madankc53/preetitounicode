#!/usr/bin/env python3
"""Fail if any embedded BS month-length table differs from scripts/bs_data.CANONICAL,
or if the canonical table stops matching the anchor dates."""
import re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import bs_data
from sync_bs_data import TARGETS, ROOT

errors = []
for y, m, d, expected in bs_data.ANCHORS:
    got = str(bs_data.bs_to_ad(y, m, d))
    if got != expected:
        errors.append(f"anchor {y}-{m:02d}-{d:02d} BS: expected {expected}, canonical table gives {got}")

for rel, pat, _ in TARGETS:
    s = (ROOT / rel).read_text(encoding="utf-8")
    m = re.search(pat, s, flags=re.S)
    if not m:
        errors.append(f"{rel}: table block not found")
        continue
    rows = {int(y): list(map(int, v.split(","))) for y, v in re.findall(r"(\d{4}):\s*\[([\d,\s]+)\]", m.group(2))}
    bad = [y for y in bs_data.CANONICAL if rows.get(y) != bs_data.CANONICAL[y]]
    if bad or set(rows) != set(bs_data.CANONICAL):
        errors.append(f"{rel}: differs from canonical table in years {bad[:10]}{'...' if len(bad) > 10 else ''}")

if errors:
    print("BS data check FAILED:")
    print("\n".join(" - " + e for e in errors))
    print("Fix scripts/bs_data.py, then run: python3 scripts/sync_bs_data.py")
    sys.exit(1)
print(f"BS data check passed: {len(bs_data.ANCHORS)} anchors, {len(TARGETS)} embedded tables match.")
