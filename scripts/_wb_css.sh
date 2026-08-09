#!/usr/bin/env bash
cd /v/__Purecomp
F=wb_full.html
echo "=== stylesheet links ==="
grep -o -E "<link[^>]*stylesheet[^>]*>" "$F" | head -10
echo
echo "=== css file urls ==="
grep -o -E "https://[^\"']+\.css" "$F" | sort -u | head -10
echo
echo "=== inline <style> blocks count ==="
grep -c "<style" "$F"
echo
echo "=== search for 'background-color' within <style> near 'sites' or 'page' ==="
grep -o -E "<style[^>]*>.*?</style>" "$F" | head -1 | grep -o -E "(background|color):[^;]{0,40}" | sort | uniq -c | sort -rn | head -15
echo
echo "=== does the HTML set a background on a big wrapper div inline? ==="
grep -o -E "<div class=\"[^\"]*\"[^>]*style=\"[^\"]*background[^\"]*\"" "$F" | head -5
