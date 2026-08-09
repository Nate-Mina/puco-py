"""Step 1: Re-crop about-us content photos at dpr=1 (FIX oversized ×2 crops).
Screenshot: browser_screenshot_07a6cb4abbe144ba8148708de04ec9c9.png = 1255x3121.
CSS W=1264 -> 1255/1264=0.99 -> dpr=1 (NOT 2). about-hero-photo was 1982x726 (WRONG).
about-us content photos (CSS coords, dpr=1):
  hero-photo:  (132,244, 991,363) -> expect 991x363
  pc-tower-1:  (32,2163, 387,362) -> expect 387x362
  pc-tower-2:  (32,2679, 387,362) -> expect 387x362
  pc-tower-3:  (32,3472, 387,362) -> expect 387x362"""
import os
from PIL import Image
B = r'V:\__Purecomp'
CI = B + r'\Content_images'
ss = r'P:\hermes\home\cache\screenshots\browser_screenshot_07a6cb4abbe144ba8148708de04ec9c9.png'
im = Image.open(ss)
PW = im.size[0]
CSS_W = 1264
dpr = round(PW / CSS_W)
print(f"about-us: screenshot {im.size} | CSS_W={CSS_W} | dpr={dpr} (was incorrectly 2 before)")
def crop(x, y, w, h, name):
    c = im.crop((int(x * dpr), int(y * dpr), int((x + w) * dpr), int((y + h) * dpr)))
    c.save(CI + r'\\' + name)
    print(f"  {name}: {c.size} (expect {w*dpr}x{h*dpr})")
crop(132, 244, 991, 363, 'about-hero-photo.png')
crop(32, 2163, 387, 362, 'about-pc-tower-1.png')
crop(32, 2679, 387, 362, 'about-pc-tower-2.png')
crop(32, 3472, 387, 362, 'about-pc-tower-3.png')
print("done — about-us re-cropped at dpr=1")
