#!/usr/bin/env python3
"""Shared word n-gram scan between this repo's text and another corpus.
  python3 tools/dev/overlap_check.py <corpus-dir> [--n 8] [--paths skills docs]
Reports every n-gram of words that appears in both; used as the acceptance test for
"concepts only, no adapted text" before a public release."""
import argparse, re, sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOILER = {"when to invoke", "inputs to read", "excluded inputs", "protocol steps", "anti patterns", "closing condition"}


def grams(text, n):
    w = re.findall(r"[a-z0-9]+", text.lower())
    return {" ".join(w[i:i + n]): i for i in range(len(w) - n + 1)}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("corpus"); ap.add_argument("--n", type=int, default=8)
    ap.add_argument("--paths", nargs="*", default=["skills", "docs", "CLAUDE.md", "README.md"])
    ap.add_argument("--allow", default=r"Lu, C\. et al|Nature 651|Imbad0202|Cheng-I Wu", help="regex; lines matching are skipped (bibliographic citations)")
    a = ap.parse_args()
    allow = re.compile(a.allow) if a.allow else None
    corpus = defaultdict(set)
    for p in Path(a.corpus).rglob("*"):
        if p.suffix.lower() in (".md", ".txt", ".yaml", ".yml", ".json") and p.is_file():
            try:
                for g in grams(p.read_text(errors="ignore"), a.n):
                    corpus[g].add(str(p.relative_to(a.corpus)))
            except Exception:
                pass
    total = 0
    for rel in a.paths:
        for p in sorted((ROOT / rel).rglob("*.md")) if (ROOT / rel).is_dir() else [ROOT / rel]:
            text = "\n".join(l for l in p.read_text().splitlines() if not (allow and allow.search(l)))
            hits = [(g, i) for g, i in grams(text, a.n).items() if g in corpus and not any(b in g for b in BOILER)]
            if hits:
                print(f"\n== {p.relative_to(ROOT)}: {len(hits)} shared {a.n}-gram(s)")
                for g, i in sorted(hits, key=lambda x: x[1])[:12]:
                    print(f"   '{g}'  <- {sorted(corpus[g])[0]}")
                total += len(hits)
    print(f"\n{total} shared {a.n}-gram(s) total")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
