"""Step 4: Fix w0 'other' reuse refs (footer icons + hero-bg that wc() missed) on all remaining pages.
w0 = no =w\d+ param in URL. These are logo(16383->hero_beach), hero-bg(->hero_beach),
footer socials(->icons by anchor-href brand). NO screenshots needed.
Uses anchor-href brand context match (Ref 1: tokens differ per page, but dest URLs stable)."""
import re, os, json
B=r'V:/__Purecomp';SUB=f'{B}/pages';CI=f'{B}/Content_images';ICO=f'{B}/icons'
FIX='''<style id="purecomp-clone-fix">
/* Google Sites runtime CSS absent from saved static HTML; restores normal flow. */
.Ap4VC.yMxQg.aP9Z7e{display:none !important;}
.zfr3Q.duRjpb.CDt4Ke{position:static !important;overflow:visible !important;height:auto !important;width:auto !important;margin:0 !important;padding:0 !important;}
h1.zfr3Q,h2.zfr3Q,h3.zfr3Q{display:block !important;}
.C9DxTc{display:inline !important;position:static !important;}
.jXK9ad,.jXK9ad-SmKAyb,.tyJCtd,.baZpAe,.mGzaTb,.Depvyb,.lkHyyc{position:static !important;height:auto !important;overflow:visible !important;}
.CjVfdc{position:static !important;}
</style>'''
ICO_FILES=sorted(os.listdir(ICO)) if os.path.isdir(ICO) else []
ICON_BY_BRAND={}
for c in ICO_FILES:
    for b in ('facebook','instagram','youtube','linkedin','tiktok','link'):
        if b in c.lower() and b not in ICON_BY_BRAND:ICON_BY_BRAND[b]=f'icons/{c}'
HERO='Content_images/hero_beach.png' if os.path.exists(f'{B}/Content_images/hero_beach.png') else None
print(f"Hero={HERO} | icons={len(ICO_FILES)} | brands={list(ICON_BY_BRAND)}")
pages=sorted(f for f in os.listdir(SUB) if f.endswith('.html'))
print(f"\nProcessing {len(pages)} pages\n")
for fn in pages:
    fp=f'{SUB}/{fn}';h=open(fp,encoding='utf-8').read();bl=len(h)
    if 'purecomp-clone-fix' not in h:h=h.replace('</head>',FIX+'\n</head>',1)
    for u in set(re.findall(r'https://lh3\.googleusercontent\.com/[^"\s<>]+',h)):
        idx=h.find(u);ctx=h[max(0,idx-600):idx+300].lower()
        # Reuse mapping for w0/w32/w40/w56 tokens (logo, hero-bg, footer socials):
        loc=None
        if ('facebook' in ctx or 'instagram' in ctx or 'youtube' in ctx or
            'linkedin' in ctx or 'tiktok' in ctx or 'twitter' in ctx or 'link' in ctx):
            # footer social icon -> icons by brand
            for br in ('facebook','instagram','youtube','linkedin','tiktok','link'):
                if br in ctx and br in ICON_BY_BRAND:loc=ICON_BY_BRAND[br];break
        elif 'w16383' in u and HERO:loc=HERO
        elif 'w56' in u and os.path.exists(f'{B}/icons/icon_logo_56.png'):loc='icons/icon_logo_56.png'
        elif u not in ctx.split('=')[0:1] and ('logo' in ctx or 'header' in ctx or 'banner' in ctx) and HERO:
            loc=HERO  # hero-bg/logo
        if loc and os.path.exists(f'{B}/{loc}'):h=h.replace(u,loc,1)
    if len(h)!=bl:open(fp,'w',encoding='utf-8').write(h)
    rem=len(re.findall(r'lh3\.googleusercontent',h))
    print(f"  {fn}: {'OK' if rem==0 else f'NEED_SCRAPE({rem})'}")
