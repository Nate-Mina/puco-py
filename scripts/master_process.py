"""Master processor — inject heading fix + rewrite lh3 refs for all 19 sub-pages.
Reuse: logo w16383 -> hero_beach.png (SAME beach image everywhere).
Footer socials w32/w40 -> icons/ white glyphs matched by surrounding anchor href brand.
Content photos (w=1280/16383-hero-bg) flagged in missing_assets.json for screenshot+crop."""
import re, os, json
BASE=r'V:/__Purecomp';SUB=f'{BASE}/pages';CI=f'{BASE}/Content_images';ICO=f'{BASE}/icons'
FIX='''<style id="purecomp-clone-fix">
/* Google Sites runtime CSS absent from saved static HTML; restores normal flow. */
.Ap4VC.yMxPgf.aP9Z7e{display:none !important;}
.zfr3Q.duRjpb.CDt4Ke{position:static !important;overflow:visible !important;height:auto !important;width:auto !important;margin:0 !important;padding:0 !important;}
h1.zfr3Q,h2.zfr3Q,h3.zfr3Q{display:block !important;}
.C9DxTc{display:inline !important;position:static !important;}
.jXK9ad,.jXK9ad-SmKAyb,.tyJCtd,.baZpAe,.mGzaTb,.Depvyb,.lkHyyc{position:static !important;height:auto !important;overflow:visible !important;}
.CjVfdc{position:static !important;}
</style>'''
def tok(u):
    m=re.search(r'/([A-Za-z0-9_-]{22,})',u);return m.group(1)[:22] if m else None
def wc(u):
    m=re.search(r'=w(\d+)',u);return m.group(1) if m else None
ICO_FILES=sorted(os.listdir(ICO)) if os.path.isdir(ICO) else[]
# icon files by brand
ICON_BY_BRAND={}
for c in ICO_FILES:
    for b in ('facebook','instagram','youtube','linkedin','tiktok'):
        if b in c.lower() and b not in ICON_BY_BRAND:ICON_BY_BRAND[b]=f'icons/{c}'
HERO='Content_images/hero_beach.png' if os.path.exists(f'{BASE}/Content_images/hero_beach.png') else None
LOGO='icons/icon_logo_56.png' if os.path.exists(f'{BASE}/icons/icon_logo_56.png') else None
print(f"Hero={HERO} LOGO={LOGO}")
print(f"ICON_BY_BRAND={ICON_BY_BRAND}")
pages=sorted(f for f in os.listdir(SUB) if f.endswith('.html'))
print(f"Sub-pages: {len(pages)}\n")
rw=0;miss=[]
for fn in pages:
    fp=f'{SUB}/{fn}';h=open(fp,encoding='utf-8').read();bl=len(h)
    if 'purecomp-clone-fix' not in h:h=h.replace('</head>',FIX+'\n</head>',1)
    for u in set(re.findall(r'https://lh3\.googleusercontent\.com/[^"\s<>]+',h)):
        t=tok(u);w=wc(u);loc=None
        idx=h.find(u);ctx=h[max(0,idx-400):idx+200].lower()
        if w=='16383' and HERO:loc=HERO
        elif w=='56' and LOGO:loc=LOGO
        elif w in('32','40'):
            for br in ('facebook','instagram','youtube','linkedin','tiktok','link'):
                if br in ctx and br in ICON_BY_BRAND:loc=ICON_BY_BRAND[br];break
            if not loc:loc=ICON_BY_BRAND.get('facebook')
        if loc and os.path.exists(f'{BASE}/{loc}'):h=h.replace(u,loc)
        else:miss.append({'page':fn,'t':t,'w':w,'u':u[:100]})
    if len(h)!=bl:open(fp,'w',encoding='utf-8').write(h);rw+=1
    rem=len(re.findall(r'lh3\.googleusercontent',h))
    print(f"  {fn}: {'OK' if rem==0 else f'NEED_CROP({rem})'}")
json.dump(miss,open(f'{BASE}/scripts/missing_assets.json','w'),indent=1)
tot=sum(len(re.findall(r'lh3',open(f'{SUB}/{f}',encoding='utf-8').read())) for f in pages)
ok=sum(1 for f in pages if len(re.findall(r'lh3',open(f'{SUB}/{f}',encoding='utf-8').read()))==0)
print(f"\nRewritten: {rw}/{len(pages)} | fully OK: {ok} | need crop: {len(miss)} | total lh3 remaining: {tot}")
