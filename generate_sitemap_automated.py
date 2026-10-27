"""Generate sitemap.xml for converter.thenepal.io.

Rules (match how Cloudflare serves this repo):
  * dir/index.html  -> https://converter.thenepal.io/dir/
  * page.html       -> https://converter.thenepal.io/page   (no .html, no trailing slash)
  * header.html / footer.html / 404.html are partials, never listed
  * pages with <meta name="robots" content="noindex"> are never listed
  * pages whose canonical points to a different host are never listed
  * lastmod is the date of the last git commit that touched the file

Warnings are printed when a page's canonical tag differs from the URL it serves
at, so the problem is visible in the workflow log instead of silently hurting SEO.
Run:  python3 generate_sitemap_automated.py
"""
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from urllib.parse import urlparse
from xml.sax.saxutils import escape

BASE_URL = "https://converter.thenepal.io"
HOST = urlparse(BASE_URL).netloc
REPO_PATH = os.path.dirname(os.path.abspath(__file__))
SITEMAP_PATH = os.path.join(REPO_PATH, "sitemap.xml")
EXCLUDE_DIRS = {".git", ".github", "github", "node_modules", "functions", "assets", "fonts"}
EXCLUDE_FILES = {"404.html", "header.html", "footer.html", "google_verify.html"}

CANONICAL_RE = re.compile(
    r'<link\b[^>]*\brel=["\']canonical["\'][^>]*\bhref=["\']([^"\']+)["\']'
    r'|<link\b[^>]*\bhref=["\']([^"\']+)["\'][^>]*\brel=["\']canonical["\']',
    re.I,
)
NOINDEX_RE = re.compile(
    r'<meta\b[^>]*\bname=["\']robots["\'][^>]*\bcontent=["\'][^"\']*noindex', re.I
)


def served_path(rel):
    """URL path (with the right trailing-slash form) that Cloudflare serves rel at."""
    rel = rel.replace(os.sep, "/")
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel[: -len(".html")]


def last_modified(rel):
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel],
            cwd=REPO_PATH, capture_output=True, text=True, check=True,
        ).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    ts = os.path.getmtime(os.path.join(REPO_PATH, rel))
    return datetime.fromtimestamp(ts, timezone.utc).strftime("%Y-%m-%d")


def collect():
    entries, warnings = [], []
    for dirpath, dirs, files in os.walk(REPO_PATH):
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS)
        for name in sorted(files):
            if not name.endswith(".html") or name in EXCLUDE_FILES:
                continue
            rel = os.path.relpath(os.path.join(dirpath, name), REPO_PATH)
            with open(os.path.join(dirpath, name), encoding="utf-8", errors="ignore") as fh:
                html = fh.read()
            if NOINDEX_RE.search(html):
                continue
            path = served_path(rel)
            m = CANONICAL_RE.search(html)
            canonical = (m.group(1) or m.group(2)) if m else None
            if canonical is None:
                warnings.append(f"no canonical tag: {rel}")
            else:
                c = urlparse(canonical)
                if c.netloc and c.netloc != HOST:
                    warnings.append(f"skipped (canonical is on {c.netloc}): {rel}")
                    continue
                if c.path != path:
                    warnings.append(f"canonical {c.path!r} != served {path!r}: {rel}")
            entries.append((path, last_modified(rel)))
    entries.sort(key=lambda e: (e[0] != "/", e[0]))
    return entries, warnings


def write(entries):
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for path, lastmod in entries:
        lines += ["  <url>",
                  f"    <loc>{escape(BASE_URL + path)}</loc>",
                  f"    <lastmod>{lastmod}</lastmod>",
                  "  </url>"]
    lines.append("</urlset>")
    with open(SITEMAP_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    entries, warnings = collect()
    write(entries)
    print(f"Sitemap written with {len(entries)} URLs.")
    for w in warnings:
        print("WARNING:", w, file=sys.stderr)
