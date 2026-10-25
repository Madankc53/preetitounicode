"""Site health check, run on every pull request (see .github/workflows/check.yml).

Fails (exit 1) when it finds the kinds of problems that were silently hurting
the site: internal links that go nowhere, canonical tags that do not match the
URL a page is really served at, duplicate canonicals, and invalid JSON-LD.

Run locally from the repo root:  python3 scripts/check_site.py
"""
import json
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOST = "converter.thenepal.io"
SKIP_DIRS = {".git", ".github", "github", "node_modules", "functions", "scripts"}
PARTIALS = {"header.html", "footer.html"}
NO_CANONICAL_NEEDED = {"404.html", "offline.html"}

errors = []


def err(msg):
    errors.append(msg)


def html_files():
    for dp, dn, fn in os.walk(ROOT):
        dn[:] = sorted(d for d in dn if d not in SKIP_DIRS)
        for f in sorted(fn):
            if f.endswith(".html"):
                yield os.path.relpath(os.path.join(dp, f), ROOT).replace(os.sep, "/")


def served(rel):
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[:-len("index.html")]
    return "/" + rel[:-len(".html")]


redirects = set()
rp = os.path.join(ROOT, "_redirects")
if os.path.exists(rp):
    for line in open(rp, encoding="utf-8"):
        parts = line.split("#")[0].split()
        if len(parts) >= 2:
            redirects.add(parts[0].rstrip("/") or "/")


def exists(rel):
    return os.path.isfile(os.path.join(ROOT, rel))


def resolves(path):
    p = path.rstrip("/") or "/"
    if p in redirects:
        return True
    if p == "/":
        return exists("index.html")
    rel = p.lstrip("/")
    return exists(rel) or exists(rel + ".html") or exists(rel + "/index.html")


HREF = re.compile(r'(?:href|src)\s*=\s*["\']([^"\']+)["\']', re.I)
CANON = re.compile(r'<link\b[^>]*\brel=["\']canonical["\'][^>]*>', re.I)
LDJSON = re.compile(r'<script type="application/ld\+json">(.*?)</script>', re.S)

for rel in html_files():
    text = open(os.path.join(ROOT, rel), encoding="utf-8", errors="ignore").read()
    if rel in PARTIALS:
        continue

    # 1. internal links
    for m in HREF.finditer(text):
        h = m.group(1).strip()
        if h.startswith(("#", "mailto:", "tel:", "javascript:", "data:", "{", "$")):
            continue
        u = urlparse(h)
        if u.scheme in ("http", "https"):
            if u.netloc != HOST:
                continue
            path = u.path or "/"
        elif u.scheme:
            continue
        else:
            if not u.path:
                continue
            path = u.path if u.path.startswith("/") else os.path.normpath("/" + os.path.dirname(rel) + "/" + u.path)
        if not resolves(path):
            err(f"{rel}: link to {path} does not resolve")

    # 2. canonical must exist, be unique, and match where the page is served
    if rel not in NO_CANONICAL_NEEDED:
        tags = CANON.findall(text)
        if len(tags) != 1:
            err(f"{rel}: expected exactly 1 canonical tag, found {len(tags)}")
        else:
            href = re.search(r'href=["\']([^"\']+)', tags[0])
            c = urlparse(href.group(1)) if href else None
            if not c or c.netloc != HOST:
                err(f"{rel}: canonical is not on {HOST}: {href.group(1) if href else None}")
            elif c.path != served(rel):
                err(f"{rel}: canonical {c.path} != served URL {served(rel)}")

    # 3. structured data must be valid JSON
    for m in LDJSON.finditer(text):
        try:
            json.loads(m.group(1))
        except ValueError as e:
            err(f"{rel}: invalid JSON-LD ({e})")

if errors:
    print(f"{len(errors)} problem(s) found:\n")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("Site check passed: links, canonicals and structured data are all consistent.")
