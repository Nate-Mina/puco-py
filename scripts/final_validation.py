"""Final validation: crop dims (dpr=1) + urllib HTTP server + 0 lh3 + 0 missing assets.
Reference 1, Step 4: assert per page 0 lh3 remaining + every local src/href resolves."""
import os, re, threading, time, urllib.request
from http.server import HTTPServer, SimpleHTTPRequestHandler
from PIL import Image
B=r'V:\__Purecomp';CI=f'{B}/Content_images'
# 1. Verify crop dimensions are dpr=1 (not oversized x2)
print("=== Crop dimension check (dpr=1) ===")
checks={'about-hero-photo.png':(991,363),'about-pc-tower-1.png':(387,362),
        'about-pc-tower-2.png':(387,362),'about-pc-tower-3.png':(387,362),
        'pc-home-1.png':(287,192),'pc-home-2.png':(287,197),'pc-home-3.png':(387,376),
        'pc-home-4.png':(387,610),'pc-home-5.png':(387,610),'services-1.png':(588,252),
        'services-gaming-1.png':(491,390),'optimize-everything-1.png':(588,451),
        'optimize-everything-2.png':(588,514)}
allcrop_ok=True
for name,exp in checks.items():
    p=f'{CI}/{name}'
    if os.path.exists(p):
        im=Image.open(p);ok=im.size==exp
        if not ok:allcrop_ok=False
        print(f"  {name}: {im.size} (expect {exp}) {'OK' if ok else 'WRONG!'}")
    else:print(f"  {name}: MISSING");allcrop_ok=False
# 2. HTTP server + urllib integrity
os.chdir(B)
srv=HTTPServer(('127.0.0.1',8201),SimpleHTTPRequestHandler)
t=threading.Thread(target=srv.serve_forever,daemon=True);t.start();time.sleep(0.5)
pages=sorted(f for f in os.listdir(f'{B}/pages') if f.endswith('.html'))
pts=['index.html']+[f'pages/{p}' for p in pages]
total_lh3=0;total_assets=0;total_bad=0;http_errors=0;served=0
print(f"\n=== urllib integrity ({len(pts)} pages) ===")
for rel in pts:
    try:
        r=urllib.request.urlopen(f'http://127.0.0.1:8201/{rel}');html=r.read().decode('utf-8','replace')
        if r.status!=200:http_errors+=1;print(f"  BAD: {rel} -> HTTP {r.status}");continue
        served+=1
    except Exception as e:http_errors+=1;print(f"  ERROR: {rel} -> {e}");continue
    lh3=len(re.findall(r'lh3\.googleusercontent',html));total_lh3+=lh3
    for m in re.finditer(r'(?:src|href)="((?:Content_images|icons)/[^"]+)"',html):
        total_assets+=1
        if not os.path.exists(f'{B}/{m.group(1)}'):print(f"  MISSING: {rel} -> {m.group(1)}");total_bad+=1
    print(f"  [{'OK' if lh3==0 else 'NEED('+str(lh3)+')'}] {rel} (lh3={lh3})")
srv.shutdown()
print(f"\n=== SUMMARY ===")
print(f"  Served HTTP 200: {served}/{len(pts)} | errors: {http_errors}")
print(f"  lh3 remaining: {total_lh3} | asset refs: {total_assets} | missing: {total_bad}")
print(f"  Crops dpr=1: {allcrop_ok}")
r='ALL CLEAR' if total_lh3==0 and total_bad==0 and http_errors==0 and allcrop_ok else 'HAS ISSUES'
print(f"  RESULT: {r}")
