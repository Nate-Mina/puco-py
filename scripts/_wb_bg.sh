#!/usr/bin/env bash
cd /v/__Purecomp
F=wb_full.html
echo "=== context around IFuOkc (page background) ==="
grep -o -E ".{200}IFuOkc.{200}" "$F" | head -1 | tr -d '\n' | cut -c1-500
echo
echo "=== the background image URL ==="
grep -o -E "lh5.googleusercontent.com/[^\"') ]+" "$F" | sort -u | head -5
echo
echo "=== does a translucent overlay/card exist? search 'rgba(0,0,0' high alpha or 'backdrop' ==="
grep -o -E "background-color: rgba\(0,0,0,[0-9.]\)" "$F" | sort | uniq -c
echo
echo "=== search for the content card wrapper class with a background (e.g. rgba with alpha) ==="
grep -o -E "\.[A-Za-z]{4,8}\{background-color: rgba\([0-9]+,[0-9]+,[0-9]+,[0-9.]\)" "$F" | head -20
