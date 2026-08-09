"""Crop+rewire about-us (dpr=1 FIX) AND services (dpr=1) + rewire both in DOM order.
about-us screenshot: browser_screenshot_07a6cb4abbe144ba8148708de04ec9c9.png = 1255x3121 (dpr=1)
services screenshot: browser_screenshot_0f31090ae6a446a4982caa1d98ba759d.png = 1255x1614 (dpr=1)
Reuse: w16383 logo/hero-bg -> hero_beach.png. Crop w1280 content photos at dpr=1."""
import os, re, glob
from PIL import Image
B=r'V:\__Purecomp';CI=f'{B}/Content_images'
def crop_from(ss_path, x, y, w, h, dpr, name, css_w):
    im=Image.open(ss_path)
    # compute dpr from screenshot if not provided
    if dpr is None:
        dpr=round(im.size[0]/css_w)
    c=im.crop((int(x*dpr),int(y*dpr),int((x+w)*dpr),int((y+h)*dpr)))
    c.save(f'{CI}/{name}')
    print(f"  {name}: {c.size} (CSS box {w}x{h}, dpr={dpr}, expect {w*dpr}x{h*dpr})")
# --- about-us (dpr=1) ---
ss_a=r'P:\hermes\home\cache\screenshots\browser_screenshot_07a6cb4abbe144ba8148708de04ec9c9.png'
crop_from(ss_a, 132, 244, 991, 363, 1, 'about-hero-photo.png', 1264)
crop_from(ss_a, 32, 2163, 387, 362, 1, 'about-pc-tower-1.png', 1264)
crop_from(ss_a, 32, 2679, 387, 362, 1, 'about-pc-tower-2.png', 1264)
crop_from(ss_a, 32, 3472, 387, 362, 1, 'about-pc-tower-3.png', 1264)  # 3rd PC tower photo
# --- services (dpr=1) ---
ss_s=r'P:\hermes\home\cache\screenshots\browser_screenshot_0f31090ae6a446a4982caa1d98ba759d.png'
crop_from(ss_s, 32, 275, 588, 252, 1, 'services-1.png', 1264)  # tech doctor image
print("\n--- rewire ---")
def rewire(fn, photo_names, hero='Content_images/hero_beach.png'):
    fp=f'{B}/pages/{fn}';h=open(fp,encoding='utf-8').read()
    urls=re.findall(r'https://lh3\.googleusercontent\.com/[^"\s<>]+',h)
    print(f"{fn}: {len(urls)} remaining lh3:")
    pi=0
    for u in urls:
        if 'w16383' in u:loc=hero
        else:
            loc=f'Content_images/{photo_names[pi]}' if pi<len(photo_names) else 'icons/facebook_white_28dp.png'
            pi+=1
        if not os.path.exists(f'{B}/{loc}'):loc='icons/facebook_white_28dp.png'
        h=h.replace(u, loc, 1)
        print(f"  {u[:60]} -> {loc}")
    open(fp,'w',encoding='utf-8').write(h)
    rem=len(re.findall(r'lh3\.googleusercontent',h))
    print(f"{fn} lh3 remaining: {rem}")
rewire('about-us.html', ['about-hero-photo.png','about-pc-tower-1.png','about-pc-tower-2.png','about-pc-tower-3.png'])
rewire('services.html', ['services-1.png'])
print("\ndone")
