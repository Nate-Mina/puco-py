#!/usr/bin/env bash
cd /v/__Purecomp
F=wb_full.html
echo "=== full header inner HTML (structure only, first 2500 chars) ==="
sed -n 's/.*\(<header id="atIdViewHeader">\)/\1/p' "$F" | head -c 2500
echo
echo "=== IFuOkc full block (neon section bg) ==="
grep -o -E ".{80}IFuOkc.{400}" "$F" | head -1 | tr -d '\n' | cut -c1-600
