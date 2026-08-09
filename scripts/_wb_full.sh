#!/usr/bin/env bash
cd /v/__Purecomp
SNAP="https://web.archive.org/web/20250321025801/https://www.purecomp.net/"
curl -s -L "$SNAP" -o wb_full.html
echo "bytes: $(wc -c < wb_full.html)"
echo "=== background style values (top 20) ==="
grep -o -E "background[-a-z]*: *(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))" wb_full.html | sort | uniq -c | sort -rn | head -20
echo "=== google fonts ==="
grep -o -E "fonts.googleapis.com/css2\?[^ \"'\"]+" wb_full.html | head -2
echo "=== page bg wrapper classes near 'sites-canvas' or 'atIdView' ==="
grep -o -E "(sites-canvas|sites-body|page-wrapper)[^\"']{0,80}" wb_full.html | head -5
echo "=== body tag (first 300) ==="
grep -o -E "<body[^>]*>" wb_full.html | head -1 | cut -c1-300
