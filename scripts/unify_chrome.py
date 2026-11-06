"""One-off/idempotent: give every page the shared header/footer and drop duplicate bars.

- every content page gets <div id="header"> ... <div id="footer"> + /components.js
- duplicate site-nav strips (top-nav / nav / topnav) and page-level <footer>s are removed
- guide + currency footers keep their sources/disclaimer text as a small page note
Run from repo root: python3 scripts/unify_chrome.py
"""
import re, glob, sys

SKIP = {'header.html', 'footer.html', '404.html', 'offline.html'}
NOTE_CSS = ('<style>.page-note{max-width:900px;margin:28px auto;padding:0 16px;'
            'font-size:.85rem;line-height:1.6;color:#6b6b6b;text-align:center}'
            '.page-note a{color:inherit;text-decoration:underline}</style>')
KEEP_AS_NOTE = ('guide/', 'currency/index.html')
STRIP_NAV = re.compile(r'[ \t]*<nav class="(?:top-nav|nav|topnav)"[^>]*>.*?</nav>[ \t]*\n?', re.S)
PLAIN_NAV_PAGES = {'download-preeti-font.html', 'preeti-to-unicode-converter/kantipur-to-unicode.html',
                   'preeti-unicode-guide/index.html'}

def process(p, s):
    notes = []
    if 'site-header' in s:            # pages with their own inline include (already shared)
        return s, ['inline-include, left as is']
    body_i = s.find('<body')
    head, body = s[:body_i], s[body_i:]
    n0 = len(body)
    # 1. duplicate site navs
    body, k = STRIP_NAV.subn('', body)
    if k: notes.append('removed %d nav strip(s)' % k)
    if p in PLAIN_NAV_PAGES:
        body, k = re.subn(r'[ \t]*<header class="hdr">.*?</header>[ \t]*\n?', '', body, count=1, flags=re.S) if p == 'download-preeti-font.html' else (body, 0)
        if not k:
            body, k = re.subn(r'[ \t]*<nav>.*?</nav>[ \t]*\n?', '', body, count=1, flags=re.S)
        if k: notes.append('removed own header/nav')
    # 2. own footers
    def foot(m):
        if p.startswith(KEEP_AS_NOTE) and 'id="footer"' not in m.group(0):
            inner = re.sub(r'^<footer[^>]*>|</footer>$', '', m.group(0).strip())
            return '<div class="page-note">' + inner + '</div>'
        return ''
    body, k = re.subn(r'[ \t]*<footer\b.*?</footer>[ \t]*\n?', foot, body, flags=re.S)
    if k: notes.append('handled %d page footer(s)' % k)
    if 'page-note' in body and NOTE_CSS not in head:
        head = head.replace('</head>', NOTE_CSS + '\n</head>', 1)
    # 3. shared header / footer
    if 'id="header"' not in body:
        body = re.sub(r'(<body[^>]*>)', r'\1\n<div id="header" style="min-height:61px"></div>', body, count=1)
        notes.append('added #header')
    elif 'style=' not in re.search(r'<div id="header"[^>]*>', body).group(0):
        body = body.replace('<div id="header">', '<div id="header" style="min-height:61px">', 1)
    def before_last(text, marker, add):
        i = text.rfind(marker)
        return text[:i] + add + text[i:]
    if 'id="footer"' not in body:
        if 'src="/components.js"' in body:
            body = before_last(body, '<script src="/components.js">', '<div id="footer"></div>\n')
        else:
            body = before_last(body, '</body>', '<div id="footer"></div>\n')
        notes.append('added #footer')
    if 'components.js' not in body:
        body = before_last(body, '</body>', '<script src="/components.js"></script>\n'); notes.append('added components.js')
    # JS that wrote into the removed footers/navs must not throw
    body, k = re.subn(r"document\.getElementById\((['\"])(ftr-year|fy)\1\)\.textContent",
                      r"(document.getElementById(\1\2\1)||{}).textContent", body)
    body, k2 = re.subn(r'document\.getElementById\("(installBtn|themeBtn)"\)\.', r'(document.getElementById("\1")||document.createElement("i")).', body)
    if k or k2: notes.append('null-safe js')
    # 4. preload so the include starts immediately
    if 'rel="preload" href="/header.html"' not in head:
        head = head.replace('</head>', '<link rel="preload" href="/header.html" as="fetch" crossorigin>\n'
                            '<link rel="preload" href="/footer.html" as="fetch" crossorigin>\n</head>', 1)
        notes.append('preload')
    return head + body, notes

if __name__ == '__main__':
    for p in sorted(glob.glob('**/*.html', recursive=True)):
        if p in SKIP: continue
        s = open(p, encoding='utf8').read()
        new, notes = process(p, s)
        if new != s:
            open(p, 'w', encoding='utf8').write(new)
        print(p, '|', '; '.join(notes) if notes else 'unchanged')
