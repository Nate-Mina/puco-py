import re, os, shutil

BASE = r'V:\__Purecomp'
PAGES = os.path.join(BASE, 'pages')

# Map internal page links to the flattened, Jekyll-friendly URLs we use in the nav.
# (keeps existing href values that already point at the right file; only rewrites root-absolute slugs)
SLUG_MAP = {
    '/pc-home': '/',
    '/about-us': '/pages/about-us.html',
    '/get-help-now': '/pages/get-help-now.html',
    '/get-help-now/computer-help': '/pages/get-help-now-computer-help.html',
    '/get-help-now/it-support': '/pages/get-help-now-it-support.html',
    '/services': '/pages/services.html',
    '/services/simulation-with-optimization': '/pages/services-simulation-with-optimization.html',
    '/services/a-i-tools': '/pages/services-a-i-tools.html',
    '/services/optimize-everything': '/pages/services-optimize-everything.html',
    '/services/fast-tech-support': '/pages/services-fast-tech-support.html',
    '/services/pc-performance': '/pages/services-pc-performance.html',
    '/services/gaming': '/pages/services-gaming.html',
    '/form': '/pages/form.html',
    '/more/microsoft-challenge': '/pages/more-microsoft-challenge.html',
    '/more/game': '/pages/more-game.html',
    '/referral-program': '/pages/referral-program.html',
    '/privacyterms/privacy-policy': '/pages/privacyterms-privacy-policy.html',
    '/privacyterms/yum-cookies': '/pages/privacyterms-yum-cookies.html',
    '/privacyterms/disclaimers': '/pages/privacyterms-disclaimers.html',
}

def strip_shell(html):
    """Return just the <body> inner content, with Google runtime junk removed."""
    # Grab body inner HTML
    m = re.search(r'<body[^>]*>(.*)</body>', html, re.S | re.I)
    body = m.group(1) if m else html
    # Remove all <script>...</script>
    body = re.sub(r'<script[\s\S]*?</script>', '', body, flags=re.I)
    # Remove all <style>...</style> (we supply our own CSS)
    body = re.sub(r'<style[\s\S]*?</style>', '', body, flags=re.I)
    # Remove google nonce attrs / data-js* attrs are fine to keep but trim jsaction/jscontroller for cleanliness
    # Drop empty structural divs that have no text/img
    return body

def clean_body(body):
    # Cut everything from the start of body up to the first <section (the real content).
    # Google Sites puts the header nav + search chrome before the <section>s; we render our own nav.
    sec = re.search(r'<section', body)
    if sec:
        body = body[sec.start():]
    # Remove the floating "site actions" button block (Google Sites chrome)
    body = re.sub(r'<div jscontroller="j1RDQb"[\s\S]*?</div>\s*</div>\s*</div>', '', body)
    body = re.sub(r'<div class="Xpil1b xgQ6eb"></div>', '', body)
    # Remove the "Skip to main content"/"Search this site" chrome and header search widget
    body = re.sub(r'<div role="button"[^>]*aria-label="Back to site"[\s\S]*?</div>\s*</div>', '', body, count=1)
    # Remove copy-link anchor buttons inside headings (keep the heading text span)
    body = re.sub(r'<div jscontroller="Ae65rd"[\s\S]*?(?=<span class="C9DxTc )', '', body)
    # Strip all jscontroller/jsaction/jsmodel/jsname attributes (harmless but noisy)
    body = re.sub(r'\sjscontroller="[^"]*"', '', body)
    body = re.sub(r'\sjsaction="[^"]*"', '', body)
    body = re.sub(r'\sjsmodel="[^"]*"', '', body)
    body = re.sub(r'\sjsname="[^"]*"', '', body)
    body = re.sub(r'\sjsshadow', '', body)
    # Remove empty structural divs (no text, no img, no section)
    body = re.sub(r'<div[^>]*>\s*</div>', '', body)
    return body

def rewrite_assets_and_links(body, is_home=False):
    # Assets: any Content_images/ or icons/ -> prefix with {{ site.baseurl }}/
    body = re.sub(r'(?<![\w/.])Content_images/', '{{ site.baseurl }}/Content_images/', body)
    body = re.sub(r'(?<![\w/])icons/', '{{ site.baseurl }}/icons/', body)
    body = re.sub(r'(?<![\w/.])images/', '{{ site.baseurl }}/Content_images/', body)
    body = re.sub(r'(?<![\w/.])favicon\.ico', '{{ site.baseurl }}/favicon.ico', body)
    # Links: root-absolute slug -> mapped url
    for slug, dst in sorted(SLUG_MAP.items(), key=lambda kv: len(kv[0]), reverse=True):
        body = re.sub(r'href="' + re.escape(slug) + r'"', 'href="' + dst + '"', body)
    # any leftover /pages/X.html at root is already correct relative from root
    return body

def extract_title(html, fallback):
    m = re.search(r'<title>(.*?)</title>', html, re.S | re.I)
    if m:
        t = m.group(1).strip()
        t = re.sub(r'\s*—\s*Pure Computers$', '', t)
        return t
    return fallback

def build_page(path, out_path, fallback_title):
    raw = open(path, encoding='utf-8').read()
    body = strip_shell(raw)
    body = clean_body(body)
    body = rewrite_assets_and_links(body, is_home=False)
    title = extract_title(raw, fallback_title)
    out = '---\ntitle: ' + title + '\nlayout: default\n---\n\n' + body.strip() + '\n'
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, 'w', encoding='utf-8').write(out)
    return title

# Ensure Jekyll output dirs: pages/ go to pages/, index stays at root
os.makedirs(os.path.join(BASE, 'pages'), exist_ok=True)

results = []
for fn in sorted(os.listdir(PAGES)):
    if not fn.endswith('.html'):
        continue
    src = os.path.join(PAGES, fn)
    dst = os.path.join(PAGES, fn)  # keep flat file in pages/
    title = build_page(src, dst, fn.replace('.html', '').replace('-', ' ').title())
    results.append((fn, title))

# Rebuild index.html at root from the LIVE homepage DOM (fresh pull) if present,
# otherwise fall back to the bundled pc-home.html.
home_src = os.path.join(BASE, 'live_content.html')
if os.path.exists(home_src):
    raw = open(home_src, encoding='utf-8').read()
    title = 'Pure Computers'
else:
    home_src = os.path.join(PAGES, 'pc-home.html')
    raw = open(home_src, encoding='utf-8').read()
    title = extract_title(raw, 'Pure Computers')
body = strip_shell(raw)
body = clean_body(body)
body = rewrite_assets_and_links(body, is_home=True)
out = '---\ntitle: Pure Computers\nlayout: default\n---\n\n' + body.strip() + '\n'
open(os.path.join(BASE, 'index.html'), 'w', encoding='utf-8').write(out)
results.insert(0, ('index.html (from live home)', title))

print('Built', len(results), 'pages:')
for fn, t in results:
    print('  ', fn, '->', t)
