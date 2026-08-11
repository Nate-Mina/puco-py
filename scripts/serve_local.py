import re, os, shutil

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = os.path.join(BASE, "_site")

# Pages to render: index.html at root + everything in pages/
def collect():
    out = [("index.html", os.path.join(BASE, "index.html"), "")]
    pages_dir = os.path.join(BASE, "pages")
    for fn in sorted(os.listdir(pages_dir)):
        if fn.endswith(".html"):
            out.append((os.path.join("pages", fn), os.path.join(pages_dir, fn), "pages"))
    return out

def strip_fm(html):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", html, re.S)
    if not m:
        return {}, html
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2)

def render_layout(layout, title, content):
    html = layout
    # active-tab conditionals: {% if page.title == 'X' %}active{% endif %}
    def cond(m):
        expr = m.group(1)
        # match: page.title == 'Some Title'
        mm = re.match(r"page\.title == '([^']*)'", expr.strip())
        if mm and title == mm.group(1):
            return "active"
        return ""
    html = re.sub(r"{%\s*if\s+(.*?)\s*%}(.*?){%\s*endif\s*%}", cond, html, flags=re.S)
    html = html.replace("{{ content }}", content)
    html = html.replace("{{ page.title }}", title)
    # baseurl empty for local root serving
    html = html.replace("{{ site.baseurl }}", "")
    return html

def build():
    os.makedirs(SITE, exist_ok=True)
    layout = open(os.path.join(BASE, "_layouts", "default.html"), encoding="utf-8").read()
    for rel, src, _ in collect():
        raw = open(src, encoding="utf-8").read()
        fm, content = strip_fm(raw)
        title = fm.get("title", "")
        rendered = render_layout(layout, title, content.strip())
        dst = os.path.join(SITE, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        open(dst, "w", encoding="utf-8").write(rendered)
    # copy assets
    for asset in ["Content_images", "icons", "favicon.ico"]:
        src = os.path.join(BASE, asset)
        if os.path.isdir(src):
            shutil.copytree(src, os.path.join(SITE, asset), dirs_exist_ok=True)
        elif os.path.isfile(src):
            shutil.copy2(src, os.path.join(SITE, asset))
    # copy also to pages/ so /pages/X.html absolute asset refs resolve from root
    print("Built", len(collect()), "pages into _site/")

if __name__ == "__main__":
    build()
