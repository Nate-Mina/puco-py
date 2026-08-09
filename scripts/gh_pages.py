import re, os

B = r'V:\__Purecomp'
PG = os.path.join(B, 'pages')

# slug -> basename (segments joined with -, plus .html)
SLUGS = [
 '/pc-home','/about-us','/get-help-now','/get-help-now/computer-help',
 '/get-help-now/it-support','/services','/services/a-i-tools',
 '/services/simulation-with-optimization','/services/optimize-everything',
 '/services/fast-tech-support','/services/gaming','/services/pc-performance',
 '/form','/more/microsoft-challenge','/more/game','/referral-program',
 '/privacyterms/privacy-policy','/privacyterms/yum-cookies','/privacyterms/disclaimers',
]

def flat(s):
    return s.replace('/', '-') + '.html'

def transform_subpage(h):
    changed = {}
    # nav: href="/" -> href="../index.html"
    if 'href="/" in h':
        n = h.count('href="/"')
        h = h.replace('href="/"', 'href="../index.html"')
        changed['/'] = n
    # nav: href="/slug" -> href="flat.html" (sibling in pages/)
    for s in sorted(SLUGS, key=len, reverse=True):
        pat = 'href="' + s + '"'
        if pat in h:
            dst = 'href="' + flat(s) + '"'
            if dst not in h:
                n = h.count(pat)
                h = h.replace(pat, dst)
                changed[s] = n
    return h, changed

def transform_homepage(h):
    changed = {}
    # nav: href="/" -> href="index.html"
    if 'href="/" in h:
        n = h.count('href="/"')
        h = h.replace('href="/"', 'href="index.html"')
        changed['/'] = n
    # nav: href="/slug" -> href="pages/flat.html"
    for s in sorted(SLUGS, key=len, reverse=True):
        pat = 'href="' + s + '"'
        if pat in h:
            dst = 'href="pages/' + flat(s) + '"'
            if dst not in h:
                n = h.count(pat)
                h = h.replace(pat, dst)
                changed[s] = n
    return h, changed

# --- Sub-pages ---
print('=== pages/*.html GitHub Pages transform ===')
rep = {}
for fn in sorted(os.listdir(PG)):
    if not fn.endswith('.html'):
        continue
    p = os.path.join(PG, fn)
    h = open(p, encoding='utf-8').read()
    orig = h
    h, c = transform_subpage(h)
    if h != orig:
        open(p, 'w', encoding='utf-8').write(h)
        rep[fn] = c
        print('  {}: {}'.format(fn, c))
print('Fixed {} sub-pages'.format(len(rep)))

# --- Homepage ---
hp = os.path.join(B, 'index.html')
h = open(hp, encoding='utf-8').read()
oh = h
h, hc = transform_homepage(h)
if h != oh:
    open(hp, 'w', encoding='utf-8').write(h)
    print('index.html: {}'.format(hc))
else:
    print('index.html: unchanged')

# --- .nojell + .gitignore ---
open(os.path.join(B, '.nojekyll'), 'w').write('Bypass Jekyll build; static site.\n')
open(os.path.join(B, '.gitignore'), 'w').write('_venv/\n__pycache__/\n*.pyc\nscripts/__pycache__/\n')
print('Wrote .nojekyll + .gitignore')
print('DONE')
