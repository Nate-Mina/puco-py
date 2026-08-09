# Pure Computers — Local Archive

Self-contained offline clone of the Google Sites pages at `purecomp.net`, saved under this directory.

---

## 📖 Contents

- `index.html` — PC-Home (the homepage). Full HTML with all image refs rewritten to local assets.
- `pages/` — the 18 sub-pages (about-us, services, get-help-now, privacy-terms, more, referral-program, etc.). `form.html` is kept as a dead 404 link (the original Google Form was removed).
- `Content_images/` — cropped content photos (hero beach bg, section photos, PC-tower shots, gaming images).
- `icons/` — white social glyphs used for footer/header social links (facebook, instagram, youtube, linkedin, tiktok) + the PURE logo glyph.
- `scripts/` — record of the build pipeline (`master_process.py` rewrites refs; crop scripts).

## 🖼️ Image strategy (what's local vs. live)

- **All Google CDN images localized.** Every `lh3.googleusercontent.com` reference has been replaced with a local file in `Content_images/` or `icons/`. This includes hero beacons, content photos, the logo, and social icons.
- **External links preserved as-is.** The 29 profile/social links (Facebook, Instagram, YouTube, TikTok, LinkedIn, P-C.live, the phone number, etc.) still point to the live web — clicking them leaves the archive. Only *images* are localized, not links.
- **Footer social icons** are matched by the surrounding `<a href="...facebook.com">` brand anchor and mapped to the corresponding `icons/*_white_28dp.png` glyph (tokens differ per page, but the destination URLs are stable).
- **Hero background / logo** (`w=16383`) on sub-pages = the same beach image used on the homepage → mapped to `Content_images/hero_beach.png`.

## ▶️ How to view / serve locally

From this directory, run a static server (Python is preinstalled):

```bash
cd V:\__Purecomp
python -m http.server 8099 --bind 127.0.0.1
```

Then open in your browser:

```
http://127.0.0.1:8099/index.html
```

Browse sub-pages at:

```
http://127.0.0.1:8099/pages/about-us.html
```

A directory listing is also available at `http://127.0.0.1:8099/pages/`.

> **Note:** Each HTML file is self-contained. You can also open `index.html`
> directly via `file://` — just be aware your browser may block `fetch`/XHR
> requests from `file://` origins. Serving via the static server above is the
> recommended path.

## 🛠️ Developer notes

- Image captures were taken via an authorized browser session screenshot + crop
  (page coordinates, 1:1 with page geometry — Google Sites `lh3` content images
  return HTTP 403 for all direct/server-side fetches including browser fetches
  with a Referer, because they are cookie/referrer-protected in the live runtime).
- The static HTML produced by Google Sites omits the runtime-injected CSS that
  hides duplicate SEO anchor `<h1>`s. A scoped `<style id="purecomp-clone-fix">`
  block is injected before `</head>` on every page to restore normal text flow
  (this is cosmetic — the original text content is intact).
- Build record (do not re-run unless regenerating):
  - `master_process.py` — inject fix + rewrite logo/footer-icon refs by reuse
  - `step3_crop_rewire_batch.py` — crop about-us at dpr=1 + rewire
  - `step5_final_crop.py` — crop + rewire services-optimize-everything
  - `fix_w0_reuse.py` — map leftover logo/hero-bg/footer icons by anchor-href brand
  - `final_integrity.py` — integrity pass (0 lh3, 0 missing local assets per page)

## Validation

- **20/20 pages**: 0 external `lh3` image refs remaining (index.html + 19 sub-pages)
- 98 local asset refs (src/href into `Content_images/` or `icons/`), 0 missing
- External profile/social links preserved (point to live URLs)
- Verified via `os.path.exists` on every local ref per page (not via browser — the browser guard blocks `127.0.0.1`/`file://`)
