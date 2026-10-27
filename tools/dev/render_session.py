#!/usr/bin/env python3
"""Render docs/assets/session/transcript.json as a simulated three-pane tmux window:
one SVG frame per pane switch, PNG frames via ImageMagick, docs/assets/session.gif, plus
docs/assets/session-final.svg and docs/assets/session/transcript.md.
  python3 tools/dev/render_session.py [--no-gif]"""
import json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
A = ROOT / "docs" / "assets"
SRC = A / "session" / "transcript.json"
W, H = 1200, 740
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, DejaVu Sans Mono, Liberation Mono, monospace"
PANES = {  # name: (x, y, w, h, title)
    "head": (10, 44, 640, 656, "0 · head — you ↔ the paper agent (workspace)"),
    "experiment": (658, 44, 532, 326, "1 · experiment — the experiment agent (workspace)"),
    "codespace": (658, 378, 532, 322, "2 · example-pipeline — the code-space agent (your repo)"),
}
COL = {"you": "#7DD3FC", "head": "#F1F5F9", "cmd": "#7DD3FC", "out": "#CBD5E1", "fail": "#FCA5A5", "prefix": "#64748B", "agent": "#A7F3D0"}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pane_lines(events, name):
    out = []
    for e in events:
        if e.get("pane") != name:
            continue
        k, t = e["kind"], e["text"]
        if k == "you": out.append(("you › ", t, "prefix", "you"))
        elif k == "head": out.append(("head › ", t, "agent", "head"))
        elif k.endswith("-cont"): out.append(("       ", t, "prefix", "you" if k.startswith("you") else "head"))
        elif k == "cmd": out.append(("$ ", t, "prefix", "cmd"))
        else: out.append(("", t, "out", k))
    return out


def frame_svg(events, active, status):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}" font-size="13">',
         f'<rect width="{W}" height="{H}" rx="12" fill="#0B1220"/>', f'<rect x="0" y="0" width="{W}" height="36" rx="12" fill="#111A2E"/>', f'<rect x="0" y="24" width="{W}" height="12" fill="#111A2E"/>',
         '<circle cx="20" cy="18" r="6" fill="#FF5F57"/><circle cx="40" cy="18" r="6" fill="#FEBC2E"/><circle cx="60" cy="18" r="6" fill="#28C840"/>',
         f'<text x="{W/2}" y="23" text-anchor="middle" fill="#8B9BB4" font-size="13" font-family="Inter, Helvetica, Arial, sans-serif">tmux — papercrane: one session, three roles</text>']
    for name, (x, y, w, h, title) in PANES.items():
        border = "#4ADE80" if name == active else "#243049"
        s.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="#0F172A" stroke="{border}" stroke-width="{2 if name == active else 1}"/>')
        s.append(f'<rect x="{x+1}" y="{y+1}" width="{w-2}" height="22" rx="5" fill="#172036"/>')
        s.append(f'<text x="{x+10}" y="{y+16}" fill="{"#BBF7D0" if name == active else "#8B9BB4"}" font-size="12" font-family="Inter, Helvetica, Arial, sans-serif">{esc(title)}</text>')
        cols = int((w - 24) / 7.85); rows = int((h - 34) / 18)
        lines = pane_lines(events, name)[-rows:]
        for i, (pre, text, pc, tc) in enumerate(lines):
            yy = y + 40 + 18 * i
            body = text if len(pre) + len(text) <= cols else text[:max(0, cols - len(pre) - 1)] + "…"
            if pre:
                s.append(f'<text x="{x+12}" y="{yy}" fill="{COL[pc]}" xml:space="preserve">{esc(pre)}</text>')
            s.append(f'<text x="{x+12+7.85*len(pre):.1f}" y="{yy}" fill="{COL[tc]}" xml:space="preserve">{esc(body)}</text>')
    s.append(f'<rect x="0" y="{H-32}" width="{W}" height="32" fill="#14532D"/>')
    s.append(f'<text x="14" y="{H-11}" fill="#BBF7D0" font-size="13">[papercrane]  0:head{"*" if active=="head" else ""}  1:experiment{"*" if active=="experiment" else ""}  2:example-pipeline{"*" if active=="codespace" else ""}</text>')
    s.append(f'<text x="{W-14}" y="{H-11}" text-anchor="end" fill="#BBF7D0" font-size="13" font-family="Inter, Helvetica, Arial, sans-serif">{esc(status)}</text>')
    s.append("</svg>")
    return "\n".join(s) + "\n"


def main():
    T = json.loads(SRC.read_text())
    beats = [e["beat"] for e in T if "beat" in e]
    nb = len([b for b in beats if b != "Done"])
    frames, events, active, bi = [], [], "head", 0
    seen = []
    for e in T:
        if "beat" in e:
            if events and seen:
                frames.append((list(seen), active, f"{bi}/{nb} · {beats[bi-1]}" if bi else ""))
            if e["beat"] != "Done":
                bi += 1
            continue
        if e.get("pane") != active and seen:
            frames.append((list(seen), active, f"{bi}/{nb} · {beats[bi-1]}"))
        active = e.get("pane", active)
        seen.append(e); events = seen
    frames.append((list(seen), active, f"{nb}/{nb} · {beats[nb-1]} — done"))
    fdir = A / "session" / "frames"; shutil.rmtree(fdir, ignore_errors=True); fdir.mkdir(parents=True)
    for i, (ev, act, st) in enumerate(frames):
        (fdir / f"frame-{i:02d}.svg").write_text(frame_svg(ev, act, st), encoding="utf-8")
    (A / "session-final.svg").write_text(frame_svg(*frames[-1]), encoding="utf-8")
    # transcript.md
    md = ["# Session transcript\n", "Generated by `examples/session/run_session.py`; every `$` line ran, every output is real.",
          "`you ›` and `head ›` lines are scripted.\n"]
    for e in T:
        if "beat" in e:
            if e["beat"] != "Done": md.append(f"\n## {e['beat']}\n")
            continue
        k, t = e["kind"], e["text"]
        tag = "" if k.endswith("-cont") else f"**[{e['pane']}]** "
        if k == "cmd": md.append(f"{tag}`$ {t}`  ")
        elif k in ("you", "head"): md.append(f"{tag}{k} › {t}  ")
        elif k.endswith("-cont"): md.append(f"&nbsp;&nbsp;&nbsp;&nbsp;{t}  ")
        else: md.append(f"&nbsp;&nbsp;&nbsp;&nbsp;`{t}`  ")
    (A / "session" / "transcript.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"[render-session] {len(frames)} frames -> {fdir.relative_to(ROOT)}, session-final.svg, transcript.md")
    if "--no-gif" in sys.argv or not shutil.which("convert"):
        print("[render-session] GIF skipped (no ImageMagick or --no-gif)"); return
    pngs = []
    for p in sorted(fdir.glob("frame-*.svg")):
        png = p.with_suffix(".png")
        subprocess.run(["convert", "-density", "96", "-font", "DejaVu-Sans-Mono", str(p), str(png)], check=True)
        pngs.append(str(png))
    args = ["convert", "-loop", "0"]
    for i, png in enumerate(pngs):
        args += ["-delay", "550" if i == len(pngs) - 1 else "260", png]
    args += ["-layers", "Optimize", "-colors", "64", str(A / "session.gif")]
    subprocess.run(args, check=True)
    for png in pngs: Path(png).unlink()
    print(f"[render-session] wrote docs/assets/session.gif ({(A / 'session.gif').stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
