"""GitHub Pages path transform (Ref 1+2: models converge). Content done (0 lh3).
Fixes subdir serving: pages/*.html at /repo/pages/X.html.
- assets already have ../Content_images/ prefix; remap empty images/ -> ../Content_images/
- nav: href="/slug" -> href="flat.html" (sibling); href="/" -> href="../index.html"
Homepage (root):
- nav: href="/slug" -> href="pages/flat.html"; href="/" -> href="index.html"
Preserve: externals https:// mailto: tel: + injected <style id=purecomp-clone-fix>.
"""
import re, os

B = r'V:\__Purecomp'
PG = os.path.join(B, 'pages')

# all nav slugs (href value after leading /) -> flat filename
S = [
 '/pc-home', '/about-us', '/get-help-now', '/get-help-now/computer-help',
 '/get-help-now/it-support', '/services', '/services/a-i-tools',
 '/services/simulation-with-optimization', '/services/optimize-everything',
 '/services/fast-tech-support', '/services/gaming', '/services/pc-performance',
 '/form', '/more/microsoft-challenge', '/more/game', '/referral-program',
 '/privacyterms/privacy-policy', '/privacyterms/yum-cookies',
 '/privacyterms/disclaimers',
]
def flat(s):
    return s.replace('/', '-') + '.html'

def fix_assets(h, is_home):
    """Prefix asset dirs with ../ for subpages. images/ -> Content_images/ (orphan remap)."""
    c = {}
    prefix = '' if is_home else '../'
    # negative lookbehind: only match if NOT already prefixed with ../
    for d, real in [('Content_images', 'Content_images'), ('icons', 'icons'), ('favicon.ico', 'favicon.ico')]:
        pat = re.compile(r'(?<![\w/.])' + re.escape(d))
        m = pat.findall(h)
        if m:
            h = pat.sub(prefix + d, h)
            c[d] = len(m)
    # images/ (empty orphan) -> Content_images/ (real files)
    pat = re.compile(r'(?<![\w/.])images/')
    m = pat.findall(h)
    if m:
        h = pat.sub(prefix + 'Content_images/', h)
        c['images/'] = len(m)
    return h, c

def fix_nav_subpage(h):
    """href='/X' -> href='<flat>.html' ; href='/' -> href='../index.html'."""
    c = {}
    if 'href=\"/\"' in h:
        n = h.count('href=\"/\"')
        h = h.replace('href=\"/\"', 'href=\"../index.html\"')
        c['/'] = n
    for s in sorted(S, key=len, reverse=True):
        pat = 'href=\"' + s + '\"'
        if pat in h:
            dst = 'href=\"' + flat(s) + '\"'
            if dst not in h:
                n = h.count(pat)
                h = h.replace(pat, dst)
                c[s] = n
    return h, c

def fix_nav_homepage(h):
    """href='/X' -> href='pages/<flat>.html' ; href='/' -> href='index.html'."""
    c = {}
    if 'href=\"/\"' in h:
        n = h.count('href=\"/\"')
        h = h.replace('href=\"/\"', 'href=\"index.html\"')
        c['/'] = n
    for s in sorted(S, key=len, reverse=True):
        pat = 'href=\"' + s + '\"'
        if pat in h:
            dst = 'href=\"pages/' + flat(s) + '\"'
            if dst not in h:
                n = h.count(pat)
                h = h.replace(pat, dst)
                c[s] = n
    return h, c

# --- Sub-pages ---
print('=== Sub-page transform ===')
rep = {}
for fn in sorted(os.listdir(PG)):
    if not fn.endswith('.html'):
        continue
    p = os.path.join(PG, fn)
    h = open(p, encoding='utf-8').read()
    orig = h
    h, ac = fix_assets(h, False)
    h, nc = fix_nav_subpage(h)
    if h != orig:
        open(p, 'w', encoding='utf-8').write(h)
        rep[fn] = {'assets': ac, 'nav': nc}
        print('  {}: {} | {}'.format(fn, ac, nc))
print('Fixed {} sub-pages'.format(len(rep)))

# --- Homepage ---
hp = os.path.join(B, 'index.html')
h = open(hp, encoding='utf-8').read()
oh = h
h, ac = fix_assets(h, True)
h, nc = fix_nav_homepage(h)
if h != oh:
    open(hp, 'w', encoding='utf-8').write(h)
    print('index.html: assets={} nav={}'.format(ac, nc))
else:
    print('index.html: unchanged')

# --- .nojekyll + .gitignore ---
open(os.path.join(B, '.nojekyll'), 'w').write('Static GitHub Pages site. Bypass Jekyll build.\n')
open(os.path.join(B, '.gitignore'), 'w').write('_venv/\n__pycache__/\n*.pyc\nscripts/__pycache__/\n')
print('Wrote .nojekyll + .gitignore')
print('DONE')
