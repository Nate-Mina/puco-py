#!/usr/bin/env bash
cd /v/__Purecomp
F=wb_full.html
echo "=== UtePc (main content wrapper) styling ==="
grep -o -E "\.UtePc[^{]*\{[^}]*\}" "$F" | head -5
echo
echo "=== atari/header background (BbxBP / header) ==="
grep -o -E "\.BbxBP[^{]*\{[^}]*\}" "$F" | head -5
echo
echo "=== look for a site-level background on body or html ==="
grep -o -E "(body|html|#yDmH0d)[^{]*\{[^}]*background[^}]*\}" "$F" | head -5
echo
echo "=== any 'background-image' with gradient on big wrappers ==="
grep -o -E "background-image: *linear-gradient\([^)]*\)" "$F" | sort | uniq -c | sort -rn | head -10
echo
echo "=== font-family on body/scaffold ==="
grep -o -E "\.(BbxBP|UtePc|TxnWlb|Gi8Rwc)[^{]*\{[^}]*\}" "$F" | head -8
echo
echo "=== search raw 'background-color' close to class='UtePc' in HTML ==="
grep -o -E "class=\"UtePc[^\"]*\"[^>]*style=\"[^\"]*\"" "$F" | head -3
