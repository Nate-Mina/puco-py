"""Master processor: inject heading fix + rewrite lh3->local for ALL sub-pages.
Reuse homepage assets + icons. Flag content-photo pages for screenshot+crop.
Run crop_new.py after capturing screenshots."""
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
hj=open(f'{BASE}/index.html',encoding='utf-8').read()
HM={}
for u in re.findall(r'https://lh3\.googleusercontent\.com/[^"\s<>]+',hj):
    t=tok(u)
    if t and t not in HM:
        idx=hj.find(u);seg=hj[max(0,idx-120):idx+120]
        ref=re.findall(r'(?:src|href)="((?:Content_images|icons)/[^"]+)"',seg)
        HM[t]=ref[0] if ref else None
IOC=sorted(os.listdir(ICO)) if os.path.isdir(ICO) else []
def icon40():
    for c in IOC:
        if 'facebook' in c.lower():return f'icons/{c}'
    return f'icons/{IOC[0]}' if IOC else None
pages=sorted(f for f in os.listdir(SUB) if f.endswith('.html'))
print(f"Sub-pages: {len(pages)}")
rewritten=0;missing=[]
for fname in pages:
    fp=f'{SUB}/{fname}';html=open(fp,encoding='utf-8').read();before=len(html)
    if 'purecomp-clone-fix' not in html:html=html.replace('</head>',FIX+'\n</head>',1)
    for u in set(re.findall(r'https://lh3\.googleusercontent\.com/[^"\s<>]+',html)):
        t=tok(u);w=wc(u);local=None
        if t in HM and HM[t] and os.path.exists(f'{BASE}/{HM[t]}'):local=HM[t]
        elif w=='56':local='icons/icon_logo_56.png' if os.path.exists(f'{BASE}/icons/icon_logo_56.png') else None
        elif w in('32','40'):local=icon40()
        if local and os.path.exists(f'{BASE}/{local}'):html=html.replace(u,local)
        else:missing.append({'page':fname,'url':u[:100],'t':t,'w':w})
    if len(html)!=before:open(fp,'w',encoding='utf-8').write(html);rewritten+=1
    rem=len(re.findall(r'lh3\.googleusercontent',html))
    print(f"  {fname}: {'OK' if rem==0 else f'NEED_CROP({rem})'}")
json.dump(missing,open(f'{BASE}/scripts/missing_assets.json','w'),indent=1)
total=sum(len(re.findall(r'lh3',open(f'{SUB}/{f}',encoding='utf-8').read())) for f in pages)
print(f"\nRewritten: {rewritten} pages | need scrape: {len(missing)} | total lh3 remaining: {total}")
