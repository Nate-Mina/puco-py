#!/usr/bin/env bash
cd /v/__Purecomp
SNAP="https://web.archive.org/web/20250321025801id_/https://www.purecomp.net/"
curl -s "$SNAP" -o wb_snapshot.html
echo "bytes: $(wc -c < wb_snapshot.html)"
echo "=== body/background styles ==="
grep -o -E "(background[-a-z]*|color): *(#[0-9a-fA-F]{3,8}|rgba?\([^)]*\))" wb_snapshot.html | sort | uniq -c | sort -rn | head -25
echo "=== google fonts link ==="
grep -o -E "fonts.googleapis.com/css2\?[^ \"']+" wb_snapshot.html | head -3
echo "=== body tag ==="
grep -o -E "<body[^>]*>" wb_snapshot.html | head -1 | cut -c1-400
