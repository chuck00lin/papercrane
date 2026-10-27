#!/usr/bin/env python3
"""Apply the string rows of identity/style-words.csv to any text files (README, docs, prose).
  python3 tools/dev/style_scan.py README.md docs/*.md
Prints file:line, the pattern, its kind, and the suggested replacement. Exit 1 on hits so it
can gate a doc edit; `kind=structure` rows whose pattern has no literal form are skipped."""
import csv, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
rows = [r for r in csv.DictReader(open(ROOT / "identity" / "style-words.csv")) if r["pattern"].strip()]
hits = 0
for f in sys.argv[1:]:
    p = Path(f)
    in_code = False
    for i, line in enumerate(p.read_text().splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code; continue
        if in_code or line.lstrip().startswith(("|", "<", "![", "├", "└", "│")):
            continue
        low = line.lower()
        for r in rows:
            pat = r["pattern"].lower()
            if " " in pat.strip() or len(pat.strip()) > 3:
                if pat in low:
                    hits += 1
                    print(f"{f}:{i}: [{r['kind']}] '{r['pattern'].strip()}' -> {r['replace_with'] or 'reconsider'}\n    {line.strip()[:110]}")
print(f"\n{hits} hit(s)")
sys.exit(1 if hits else 0)
