import re, os

B = r'V:\__Purecomp'
PG = os.path.join(B, 'pages')

# all nav slugs: href="/X" -> flat basename (segments joined with -, + .html)
SLUGS = [
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

# --- Sub-page nav fix ---(pages/*.html: href="/X" -> href="<flat>.html" sibling)
print('=== Sub-page nav transform ===')
rep = {}
for fn in sorted(os.listdir(PG)):
    if not fn.endswith('.html'):
        continue
    p = os.path.join(PG, fn)
    h = open(p, encoding='utf-8').read()
    orig = h
    c = {}
    # nav: href="/" -> href="../index.html"  (homepage at repo root)
    if 'href="/" in h':
        n = h.count('href="/"')
        h = h.replace('href="/"', 'href="../index.html"')
        c['/'] = n
    # nav: href="/slug" -> href="flat.html" (sibling in pages/), longest first
    for s in sorted(SLUGS, key=len, reverse=True):
        pat = 'href="' + s + '"'
        if pat in h:
            dst = 'href="' + flat(s) + '"'
            if dst not in h:
                n = h.count(pat)
                h = h.replace(pat, dst)
                c[s] = n
    if h != orig:
        open(p, 'w', encoding='utf-8').write(h)
        rep[fn] = c
        print('  {}: {}'.format(fn, c))
print('Fixed {} sub-pages'.format(len(rep)))

# --- Homepage nav fix ---
hp = os.path.join(B, 'index.html')
h = open(hp, encoding='utf-8').read()
oh = h
c = {}
# images/ orphan -> Content_images/  (homepage at root)
m = re.findall(r'(?<![\w/.])images/', h)
if m:
    h = re.sub(r'(?<![\w/.])images/', 'Content_images/', h)
    c['images/'] = len(m)
# nav: href="/" -> href="index.html"
if 'href="/" in h':
    n = h.count('href="/"')
    h = h.replace('href="/"', 'href="index.html"')
    c['/'] = n
# nav: href="/slug" -> href="pages/<flat>.html"
for s in sorted(SLUGS, key=len, reverse=True):
    pat = 'href="' + s + '"'
    if pat in h:
        dst = 'href="pages/' + flat(s) + '"'
        if dst not in h:
            n = h.count(pat)
            h = h.replace(pat, dst)
            c[s] = n
if h != oh:
    open(hp, 'w', encoding='utf-8').write(h)
    print('index.html: {}'.format(c))
else:
    print('index.html: unchanged')

# --- .nojekyll + .gitignore ---
open(os.path.join(B, '.nojekyll'), 'w').write('Bypass Jekyll build; raw static site.\n')
open(os.path.join(B, '.gitignore'), 'w').write('_venv/\n__pycache__/\n*.pyc\nscripts/__pycache__/\n')
print('Wrote .nojekyll + .gitignore')
print('DONE')
