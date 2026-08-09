"""Step 5: Crop + rewire services-optimize-everything (dpr=1). [FINAL content-photo page]
Screenshot: browser_screenshot_3c6ecbc542e64602872bc5bfffe1ea85.png (just captured)
Co:ords (read-only console, dpr=1, pw=1264, ph=1934):
  [0] logo w16383 (y0,x0 w56 h56) -> reuse hero_beach
  [1] hero-bg w16383 -> reuse hero_beach
  [2] content photo 1 (x32,y589,w588,h451) -> optimize-everything-1.png
  [3] content photo 2 (x32,y1054,w588,h514) -> optimize-everything-2.png
  [4] footer w40 (x982,y1878) -> icons/facebook_white_28dp (reuse)
  [5] footer w40 (x1038,y1878) -> icons/facebook_white_28dp (reuse)
Only 2 content photos need cropping. Logo/hero-bg/footer reuse hero_beach/icons."""
import os, re, glob
from PIL import Image
B=r'V:\__Purecomp';CI=f'{B}/Content_images';SUB=f'{B}/pages'
# Find the services-optimize-everything screenshot (newest)
ss=max(glob.glob(r'P:\hermes\home\cache\screenshots\browser_screenshot_*.png'),key=os.path.getmtime)
im=Image.open(ss);PW=im.size[0];CSS_W=1264
dpr=round(PW/CSS_W)
print(f"services-optimize-everything screenshot: {im.size} | CSS_W={CSS_W} | dpr={dpr}")
# Crop content photos at dpr=1
def crop(x,y,w,h,name):
    c=im.crop((int(x*dpr),int(y*dpr),int((x+w)*dpr),int((y+h)*dpr)))
    c.save(f'{CI}/{name}')
    print(f"  {name}: {c.size} (expect {w*dpr}x{h*dpr})")
crop(32,589,588,451,'optimize-everything-1.png')   # woman at desk with RGB
crop(32,1054,588,514,'optimize-everything-2.png') # woman with pink hair/headset
print("cropped")
# Rewire in DOM order: logo(16383)->hero_beach, hero-bg(16383)->hero_beach,
# photo1(1280)->optimize-everything-1, photo2(1280)->optimize-everything-2,
# footer(40)->facebook_white, footer(40)->facebook_white
h=open(f'{SUB}/services-optimize-everything.html',encoding='utf-8').read()
urls=re.findall(r'https://lh3\.googleusercontent\.com/[^"\s<>]+',h)
print(f"\nservices-optimize-everything remaining lh3 ({len(urls)}, DOM order):")
order=['Content_images/hero_beach.png','Content_images/hero_beach.png',
       'Content_images/optimize-everything-1.png','Content_images/optimize-everything-2.png',
       'icons/facebook_white_28dp.png','icons/facebook_white_28dp.png']
for i,u in enumerate(urls):
    loc=order[i] if i<len(order) else 'icons/facebook_white_28dp.png'
    if not os.path.exists(f'{B}/{loc}'):loc='icons/facebook_white_28dp.png'
    h=h.replace(u, loc, 1)
    print(f"  [{i}] -> {loc}")
open(f'{SUB}/services-optimize-everything.html','w',encoding='utf-8').write(h)
rem=len(re.findall(r'lh3\.googleusercontent',h))
print(f"services-optimize-everything lh3 remaining: {rem}")
