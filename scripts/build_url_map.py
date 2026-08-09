"""Classify all sub-page images: reuse homepage / reuse icons / needs-scrape."""
import re, os
BASE = r'V:/__Purecomp'
SUB = f'{BASE}/pages/sub'

def token(u):
    m = re.search(r'/([A-Za-z0-9_-]{22,})', u)
    return m.group(1)[:22] if m else None
def wclass(u):
    m = re.search(r'=w(\d+)', u)
    return m.group(1) if m else '?'

HOME_TOK_LOCAL = {}
HOME_HTML = open(f'{BASE}/index.html', encoding='utf-8').read()
for u in re.findall(r'https://lh3\.googleusercontent\.com/[^\"\' )]+', HOME_HTML):
    t = token(u)
    if t and t not in HOME_TOK_LOCAL:
        idx = HOME_HTML.find(u)
        seg = HOME_HTML[idx-80:idx+90]
        refs = re.findall(r'(?:src|href)="((?:Content_images|icons)/[^"]+)"', seg)
        HOME_TOK_LOCAL[t] = refs[0] if refs else None

all_new = {}
for f in sorted(os.listdir(SUB)):
    if not f.endswith('.html'): continue
    h = open(f'{SUB}/{f}', encoding='utf-8').read()
    for u in sorted(set(re.findall(r'https://lh3\.googleusercontent\.com/[^\"\' )]+', h))):
        t = token(u)
        if t not in all_new:
            all_new[t] = {'url': u, 'w': wclass(u), 'pages': []}
        all_new[t]['pages'].append(f)

reuse=[]; new_icons=[]; new_content=[]
for t, info in sorted(all_new.items(), key=lambda kv: kv[1]['w']):
    if t in HOME_TOK_LOCAL: reuse.append((t,info))
    elif info['w'] in ('32','40','56'): new_icons.append((t,info))
    else: new_content.append((t,info))

print(f"REUSE (homepage): {len(reuse)}")
print(f"NEW icons (32/40/56): {len(new_icons)}")
print(f"NEW content photos: {len(new_content)}\n")
print("=== NEW content photos (need scrape) ===")
for t,info in new_content:
    print(f"  w={info['w']} t={t} pages={info['pages']}")
    print(f"    {info['url'][:115]}")
print("\n=== NEW icons ===")
for t,info in new_icons:
    print(f"  w={info['w']} t={t} pages={info['pages']}")
print("\n=== REUSE ===")
for t,info in reuse:
    print(f"  w={info['w']} t={t} -> {HOME_TOK_LOCAL.get(t)}  pages={info['pages']}")
