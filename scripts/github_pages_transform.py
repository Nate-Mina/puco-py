import re, os

B = r'V:\__Purecomp'
PG = os.path.join(B, 'pages')

# slug (href="/X") -> flat filename (segments joined with -)
SLUGS = [
 '/pc-home', '/about-us', '/get-help-now', '/get-help-now/computer-help',
 '/get-help-now/it-support', '/services', '/services/a-i-tools',
 '/services/simulation-with-optimization', '/services/optimize-everything',
 '/services/fast-tech-support', '/services/gaming', '/services/pc-performance',
 '/form', '/more/microsoft-challenge', '/more/game', '/referral-program',
 '/privacyterms/privacy-policy', '/privacyterms/yum-cookies', '/privacyterms/disclaimers',
]

def flat(slug):
    return slug.replace('/', '-') + '.html'

def fix_assets_subpage(h):
    # assets: prefix ../ (idempotent via negative lookbehind for ../)
    c = {}
    h, m = re.subn(r'(?<![\w/.])Content_images/', '../Content_images/', h)
    if m: c['Content_images/'] = m
    h, m = re.subn(r'(?<![\w/])icons/', '../icons/', h)
    if m: c['icons/'] = m
    h, m = re.subn(r'(?<![\w/.])favicon\.ico', '../favicon.ico', h)
    if m: c['favicon.ico'] = m
    h, m = re.subn(r'(?<![\w/.])images/', '../Content_images/', h)
    if m: c['images/->Content_images/'] = m
    return h, c

def fix_nav_subpage(h):
    c = {}
    # href="/" -> href="../index.html"  (homepage at repo root)
    if 'href="/" in h':
        n = h.count('href="/"')
        h = h.replace('href="/"', 'href="../index.html"')
        c['/'] = n
    # href="/slug" -> href="flat.html" (sibling in pages/), longest first
    for s in sorted(SLUGS, key=len, reverse=True):
        pat = 'href="' + s + '"'
        if pat in h:
            dst = 'href="' + flat(s) + '"'
            if dst not in h:
                n = h.count(pat)
                h = h.replace(pat, dst)
                c[s] = n
    return h, c

def fix_homepage(h):
    c = {}
    # images/ (empty orphan) -> Content_images/  (root level)
    h, m = re.subn(r'(?<![\w/.])images/', 'Content_images/', h)
    if m: c['images/->Content_images/'] = m
    # href="/" -> href="index.html"
    if 'href="/" in h':
        n = h.count('href="/"')
        h = h.replace('href="/"', 'href="index.html"')
        c['/'] = n
    # href="/slug" -> href="pages/flat.html"
    for s in sorted(SLUGS, key=len, reverse=True):
        pat = 'href="' + s + '"'
        if pat in h:
            dst = 'href="pages/' + flat(s) + '"'
            if dst not in h:
                n = h.count(pat)
                h = h.replace(pat, dst)
                c[s] = n
    return h, c

# --- Sub-pages ---
print('=== pages/*.html GitHub Pages transform ===')
rep = {}
for fn in sorted(os.listdir(PG)):
    if not fn.endswith('.html'):
        continue
    p = os.path.join(PG, fn)
    h = open(p, encoding='utf-8').read()
    orig = h
    h, ac = fix_assets_subpage(h)
    h, nc = fix_nav_subpage(h)
    if h != orig:
        open(p, 'w', encoding='utf-8').write(h)
        rep[fn] = {'assets': ac, 'nav': nc}
        print('  {}: {}'.format(fn, rep[fn]))
print('Fixed {} sub-pages'.format(len(rep)))

# --- Homepage ---
hp = os.path.join(B, 'index.html')
h = open(hp, encoding='utf-8').read()
oh = h
h, hc = fix_homepage(h)
if h != oh:
    open(hp, 'w', encoding='utf-8').write(h)
    print('Homepage transform: {}'.format(hc))
else:
    print('Homepage: unchanged')

# --- .nojekyll + .gitignore ---
open(os.path.join(B, '.nojekyll'), 'w').write('Static GitHub Pages site. Bypass Jekyll build.\n')
open(os.path.join(B, '.gitignore'), 'w').write('_venv/\n__pycache__/\n*.pyc\nscripts/__pycache__/\n')
print('\nWrote .nojekyll + .gitignore')
print('DONE')
