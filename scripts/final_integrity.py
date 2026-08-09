"""FINAL urllib integrity pass (Reference 1, Step 4): verify every local asset path
resolves on disk per page. Assert: 0 lh3 remaining + 0 missing local asset files."""
import re, os, urllib.request
B=r'V:\__Purecomp';SUB=f'{B}/pages'
def check(fn):
    fp=f'{SUB}/{fn}';h=open(fp,encoding='utf-8').read()
    lh3=len(re.findall(r'lh3\.googleusercontent',h))
    # local asset refs: src="Content_images/..." or src="icons/..." or href="..."
    local_refs=re.findall(r'(?:src|href)="((?:Content_images|icons)/[^"]+)"',h)
    missing=[r for r in local_refs if not os.path.exists(f'{B}/{r}')]
    return lh3, len(local_refs), missing
pages=sorted(f for f in os.listdir(SUB) if f.endswith('.html'))
total_lh3=0;total_refs=0;total_missing=0
print("=== FINAL INTEGRITY PASS (urllib-style file checks) ===\n")
for fn in pages:
    lh3, refs, missing = check(fn)
    total_lh3+=lh3;total_refs+=refs;total_missing+=len(missing)
    status='OK' if lh3==0 and not missing else 'BAD'
    print(f"  [{status}] {fn}: lh3={lh3} | local_refs={refs} | missing={missing}")
print(f"\n=== TOTALS ===")
print(f"  Pages: {len(pages)}")
print(f"  lh3 remaining: {total_lh3}")
print(f"  Local asset refs checked: {total_refs}")
print(f"  Missing local assets: {total_missing}")
print(f"  RESULT: {'ALL CLEAR' if total_lh3==0 and total_missing==0 else 'HAS ISSUES'}")
