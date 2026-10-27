#!/usr/bin/env python3
"""Render a terminal transcript to an SVG card.  python3 tools/dev/term_card.py --title T --out file.svg < transcript.txt"""
import argparse, sys

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

ap = argparse.ArgumentParser(); ap.add_argument("--title", default=""); ap.add_argument("--out", required=True); ap.add_argument("--max-cols", type=int, default=112)
a = ap.parse_args()
lines = [(l.rstrip("\n")[:a.max_cols - 1] + "…") if len(l.rstrip("\n")) > a.max_cols else l.rstrip("\n") for l in sys.stdin]
cols = max(len(l) for l in lines) if lines else 40
W = int(8.45 * cols + 52); H = 20 * len(lines) + 66
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="ui-monospace, SFMono-Regular, Menlo, Consolas, DejaVu Sans Mono, Liberation Mono, monospace" font-size="14">',
     f'<rect width="{W}" height="{H}" rx="12" fill="#0B1220"/>', f'<rect x="0" y="0" width="{W}" height="36" rx="12" fill="#111A2E"/>', f'<rect x="0" y="24" width="{W}" height="12" fill="#111A2E"/>',
     '<circle cx="20" cy="18" r="6" fill="#FF5F57"/><circle cx="40" cy="18" r="6" fill="#FEBC2E"/><circle cx="60" cy="18" r="6" fill="#28C840"/>',
     f'<text x="{W/2}" y="23" text-anchor="middle" fill="#8B9BB4" font-size="13">{esc(a.title)}</text>']
for i, l in enumerate(lines):
    y = 58 + 20 * i
    if l.startswith("$ "):
        s.append(f'<text x="22" y="{y}" fill="#64748B">$</text><text x="{22 + 2 * 8.45:.1f}" y="{y}" fill="#7DD3FC" xml:space="preserve">{esc(l[2:])}</text>')
    elif l.startswith("[FAIL]"):
        s.append(f'<text x="22" y="{y}" fill="#FCA5A5" xml:space="preserve">{esc(l)}</text>')
    elif l.startswith("[WARN]"):
        s.append(f'<text x="22" y="{y}" fill="#FDE68A" xml:space="preserve">{esc(l)}</text>')
    elif l.startswith(("[dispatch]", "[freeze]", "[render-facts]", "[impact]", "[status]", "[compare]")):
        s.append(f'<text x="22" y="{y}" fill="#A7F3D0" xml:space="preserve">{esc(l)}</text>')
    elif l.startswith("#"):
        s.append(f'<text x="22" y="{y}" fill="#F1F5F9" font-weight="600" xml:space="preserve">{esc(l)}</text>')
    else:
        s.append(f'<text x="22" y="{y}" fill="#E2E8F0" xml:space="preserve">{esc(l)}</text>')
s.append("</svg>")
open(a.out, "w").write("\n".join(s) + "\n"); print("wrote", a.out)
