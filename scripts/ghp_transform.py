import re, os

B = r'V:\__Purecomp'
PG = os.path.join(B, 'pages')
D = chr(34)

SLUGS = [
 '/pc-home', '/about-us', '/get-help-now', '/get-help-now/computer-help',
 '/get-help-now/it-support', '/services', '/services/a-i-tools',
 '/services/simulation-with-optimization', '/services/optimize-everything',
 '/services/fast-tech-support', '/services/gaming', '/services/pc-performance',
 '/form', '/more/microsoft-challenge', '/more/game', '/referral-program',
 '/privacyterms/privacy-policy', '/privacyterms/yum-cookies', '/privacyterms/disclaimers',
]

def flat(s):
    return s.replace('/', '-') + '.html'

def transform_subpage(h):
    c = {}
    for old, new in [('Content_images/', '../Content_images/'), ('icons/', '../icons/'), ('images/', '../Content_images/'), ('favicon.ico', '../favicon.ico')]:
        if old in h:
            n = h.count(old); h = h.replace(old, new); c[old] = n
    root = 'href=' + D + '/' + D
    if root in h:
        n = h.count(root); h = h.replace(root, 'href=' + D + '../index.html' + D); c['/'] = n
    for s in sorted(SLUGS, key=len, reverse=True):
        pat = 'href=' + D + s + D
        if pat in h:
            dst = 'href=' + D + flat(s) + D
            if dst not in h:
                n = h.count(pat); h = h.replace(pat, dst); c[s] = n
    return h, c

def transform_homepage(h):
    c = {}
    if 'images/' in h:
        n = h.count('images/'); h = h.replace('images/', 'Content_images/'); c['images/'] = n
    root = 'href=' + D + '/' + D
    if root in h:
        n = h.count(root); h = h.replace(root, 'href=' + D + 'index.html' + D); c['/'] = n
    for s in sorted(SLUGS, key=len, reverse=True):
        pat = 'href=' + D + s + D
        if pat in h:
            dst = 'href=' + D + 'pages/' + flat(s) + D
            if dst not in h:
                n = h.count(pat); h = h.replace(pat, dst); c[s] = n
    return h, c

print('=== Sub-page transform ===')
rep = {}
for fn in sorted(os.listdir(PG)):
    if not fn.endswith('.html'): continue
    p = os.path.join(PG, fn)
    h = open(p, encoding='utf-8').read()
    orig = h
    h, c = transform_subpage(h)
    if h != orig:
        open(p, 'w', encoding='utf-8').write(h)
        rep[fn] = c
        print('  ' + fn + ': ' + str(c))
print('Fixed ' + str(len(rep)) + ' sub-pages')

print('=== Homepage transform ===')
hp = os.path.join(B, 'index.html')
h = open(hp, encoding='utf-8').read(); oh = h
h, hc = transform_homepage(h)
if h != oh:
    open(hp, 'w', encoding='utf-8').write(h)
    print('  ' + str(hc))
else:
    print('  unchanged')
print('DONE')
