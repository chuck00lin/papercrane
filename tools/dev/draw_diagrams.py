#!/usr/bin/env python3
"""Generate the README diagrams: the lifecycle loop and the workspace architecture, EN + zh-TW.
Both languages share one geometry. Run: python3 tools/dev/draw_diagrams.py"""
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "assets"
FONT = "Inter, -apple-system, Segoe UI, Helvetica, Arial, Noto Sans CJK TC, PingFang TC, sans-serif"
INK, SLATE, EDGE, LABEL = "#1E293B", "#475569", "#94A3B8", "#64748B"
H_FILL, H_STROKE = "#FFF1EC", "#E4573D"
A_FILL, A_STROKE = "#F4F7FA", "#CBD5E1"

T = {
 "en": dict(idea="Idea / story", design="Design", build="Build", run="Run", analyze="Analyze", interpret="Interpret",
            write="Write", review="Review", submit="Submit", human="human-led", agent="agent-led, turns fast",
            next_run="next run", new_idea="new idea", imagery="story imagery", data="the data", refine="refine",
            method="method + code", dispatch="dispatch", freeze="freeze", render="render \\fact{}", preregister="pre-register",
            claims="claims + prose", status="status", human_owned="human-owned", immutable="immutable", your_repos="your repos",
            protocols="one protocol per working mode", check="tools/check.py · schema · freeze hash · fact anchors · bare numerals · terminology · boards · cross-refs"),
 "zh-TW": dict(idea="想法 / 故事", design="設計", build="方法開發", run="實驗", analyze="分析", interpret="詮釋",
            write="寫作", review="審稿", submit="投稿", human="人主導", agent="agent 主導，要轉得快",
            next_run="下一次 run", new_idea="新想法", imagery="故事的意象", data="資料", refine="修訂",
            method="方法與程式", dispatch="派送", freeze="凍結", render="render \\fact{}", preregister="預先登錄",
            claims="claim 與 prose", status="狀態", human_owned="人擁有", immutable="不可變", your_repos="你的 repo",
            protocols="每種工作模式一份 protocol", check="tools/check.py · schema · 凍結 hash · fact 錨點 · 裸數字 · 術語 · boards · 交叉引用"),
}


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def border(cx, cy, hw, hh, a):
    c, s = math.cos(a), math.sin(a)
    t = min(hw / abs(c) if abs(c) > 1e-9 else 1e9, hh / abs(s) if abs(s) > 1e-9 else 1e9)
    return cx + t * c, cy + t * s


def arrow(x1, y1, x2, y2, hw, hh, label="", curve=None, dash=False, dy=0, dx=0, lang="en"):
    a = math.atan2(y2 - y1, x2 - x1)
    sx, sy = border(x1, y1, hw, hh, a); ex, ey = border(x2, y2, hw, hh, a + math.pi)
    if curve:
        cx, cy = curve; d = f"M{sx:.1f},{sy:.1f} Q{cx},{cy} {ex:.1f},{ey:.1f}"
        lx, ly = (sx + 2 * cx + ex) / 4, (sy + 2 * cy + ey) / 4; tx, ty = ex - cx, ey - cy
    else:
        d = f"M{sx:.1f},{sy:.1f} L{ex:.1f},{ey:.1f}"; lx, ly = (sx + ex) / 2, (sy + ey) / 2; tx, ty = ex - sx, ey - sy
    dash_attr = ' stroke-dasharray="6 5"' if dash else ""
    s = f'<path d="{d}" fill="none" stroke="{EDGE}" stroke-width="1.8" stroke-linecap="round"{dash_attr}/>'
    ta = math.atan2(ty, tx); bx, by = ex - 11 * math.cos(ta), ey - 11 * math.sin(ta); px, py = -math.sin(ta) * 5, math.cos(ta) * 5
    s += f'<polygon points="{ex:.1f},{ey:.1f} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{EDGE}"/>'
    if label:
        w = (7.6 * len(label) if lang == "en" else 14.5 * len(label)) + 16
        lx += dx; ly += dy
        s += (f'<rect x="{lx-w/2:.1f}" y="{ly-11:.1f}" width="{w:.1f}" height="22" rx="11" fill="#FFFFFF" stroke="#E2E8F0"/>'
              f'<text x="{lx:.1f}" y="{ly+4.5:.1f}" text-anchor="middle" font-size="13" fill="{LABEL}">{esc(label)}</text>')
    return s


def ortho(pts, label="", at=None, lang="en"):
    d = "M" + " L".join(f"{x},{y}" for x, y in pts)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    ta = math.atan2(y2 - y1, x2 - x1); bx, by = x2 - 11 * math.cos(ta), y2 - 11 * math.sin(ta); px, py = -math.sin(ta) * 5, math.cos(ta) * 5
    s = (f'<path d="{d}" fill="none" stroke="{EDGE}" stroke-width="1.8" stroke-linejoin="round"/>'
         f'<polygon points="{x2},{y2} {bx+px:.1f},{by+py:.1f} {bx-px:.1f},{by-py:.1f}" fill="{EDGE}"/>')
    if label and at:
        lx, ly = at; w = (7.6 * len(label) if lang == "en" else 14.5 * len(label)) + 16
        s += (f'<rect x="{lx-w/2:.1f}" y="{ly-11}" width="{w:.1f}" height="22" rx="11" fill="#FFFFFF" stroke="#E2E8F0"/>'
              f'<text x="{lx}" y="{ly+4.5}" text-anchor="middle" font-size="13" fill="{LABEL}">{esc(label)}</text>')
    return s


def node(x, y, w, h, label, human, lang):
    fill, stroke, sw = (H_FILL, H_STROKE, 2.2) if human else (A_FILL, A_STROKE, 1.5)
    return (f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>'
            f'<text x="{x}" y="{y+6}" text-anchor="middle" font-size="18" font-weight="{650 if human else 500}" fill="{INK if human else SLATE}">{esc(label)}</text>')


def loop(lang):
    t = T[lang]; W, H = 168, 56; hw, hh = W / 2, H / 2
    P = {"idea": (240, 60), "design": (570, 60), "build": (900, 60), "interpret": (240, 240), "analyze": (570, 240),
         "run": (900, 240), "write": (240, 420), "review": (570, 420), "submit": (900, 420)}
    human = {"idea", "design", "interpret"}
    A = lambda p, q, **k: arrow(*P[p], *P[q], hw, hh, lang=lang, **k)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1070 530" width="1070" height="530" font-family="{FONT}">',
             '<rect width="1070" height="530" fill="#FFFFFF"/>',
             A("idea", "design"), A("design", "build", label=t["method"]), A("build", "run"),
             A("design", "run", curve=(800, 150), dash=True), A("run", "analyze"), A("analyze", "interpret"),
             A("interpret", "design", label=t["next_run"], curve=(460, 160), dy=-6),
             A("interpret", "idea", label=t["new_idea"], dx=52), A("interpret", "write", label=t["data"], dx=40),
             A("idea", "write", label=t["imagery"], curve=(10, 240), dx=-30),
             A("write", "review"), A("review", "write", label=t["refine"], curve=(405, 505), dy=6), A("review", "submit")]
    parts += [node(*P[k], W, H, t[k], k in human, lang) for k in P]
    parts += [f'<rect x="700" y="492" width="22" height="14" rx="5" fill="{H_FILL}" stroke="{H_STROKE}" stroke-width="2"/>',
              f'<text x="730" y="504" font-size="13" fill="{SLATE}">{esc(t["human"])}</text>',
              f'<rect x="830" y="492" width="22" height="14" rx="5" fill="{A_FILL}" stroke="{A_STROKE}" stroke-width="1.5"/>',
              f'<text x="860" y="504" font-size="13" fill="{SLATE}">{esc(t["agent"])}</text>', "</svg>"]
    return "\n".join(parts) + "\n"


def box(x, y, w, h, title, tag, lines, human, lang):
    hf, hs = (H_FILL, H_STROKE) if human else (A_FILL, A_STROKE)
    s = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#FFFFFF" stroke="{hs}" stroke-width="{2 if human else 1.4}"/>',
         f'<path d="M{x+12},{y} h{w-24} a12,12 0 0 1 12,12 v18 h-{w} v-18 a12,12 0 0 1 12,-12 z" fill="{hf}"/>',
         f'<text x="{x+14}" y="{y+21}" font-size="14" font-weight="650" fill="{INK}">{esc(title)}</text>',
         f'<text x="{x+w-14}" y="{y+21}" text-anchor="end" font-size="12" fill="{H_STROKE if human else LABEL}">{esc(tag)}</text>']
    for i, l in enumerate(lines):
        s.append(f'<text x="{x+14}" y="{y+50+i*18}" font-size="13" fill="{SLATE}" font-family="SFMono-Regular, Menlo, Consolas, monospace">{esc(l)}</text>')
    return "\n".join(s)


def architecture(lang):
    t = T[lang]
    B = {  # name: (x, y, w, h)
        "identity": (60, 36, 330, 128), "decisions": (420, 36, 210, 128), "skills": (660, 36, 280, 128),
        "codespaces": (60, 222, 210, 108), "experiments": (360, 222, 250, 108), "reality": (690, 222, 250, 108),
        "boards": (360, 384, 250, 92), "manuscript": (690, 384, 250, 92)}
    C = {k: (x + w / 2, y + h / 2, w / 2, h / 2) for k, (x, y, w, h) in B.items()}
    def A(p, q, **k):
        (x1, y1, hw1, hh1), (x2, y2, hw2, hh2) = C[p], C[q]
        a = math.atan2(y2 - y1, x2 - x1)
        sx, sy = border(x1, y1, hw1, hh1, a); ex, ey = border(x2, y2, hw2, hh2, a + math.pi)
        return arrow(sx, sy, ex, ey, 0.01, 0.01, lang=lang, **k)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 560" width="1000" height="560" font-family="{FONT}">',
             '<rect width="1000" height="560" fill="#FFFFFF"/>',
             A("identity", "experiments", label=t["preregister"], dx=-70),
             A("codespaces", "experiments", label=t["dispatch"], dy=-20),
             A("experiments", "reality", label=t["freeze"], dy=-20),
             A("reality", "manuscript", label=t["render"], dx=74),
             ortho([(600, 164), (650, 164), (650, 357), (815, 357), (815, 384)], label=t["claims"], at=(732, 357), lang=lang),
             A("experiments", "boards", label=t["status"], dx=52)]
    parts.append(box(*B["identity"], "identity/", t["human_owned"], ["story-spine.md   claim-map.md", "method-trace.md  terminology.csv", "venue-calibration.md"], True, lang))
    parts.append(box(*B["decisions"], "decisions/", t["human_owned"], ["ADR-0001-*.md", "scenarios/"], True, lang))
    parts.append(box(*B["skills"], "skills/", t["protocols"], ["design-review  experiment-loop", "claim-audit  integrity-check", "shadow-reviewer  cold-review  polish"], False, lang))
    parts.append(box(*B["codespaces"], "codespaces/", t["your_repos"], ["my-pipeline.yaml", "  entry: make run EXP= RUN=", "  emits: runs/{run}/facts.json"], False, lang))
    parts.append(box(*B["experiments"], "experiments/", "", ["EXP-001/experiment.yaml", "EXP-001/runs/r03/run.yaml", "EXP-001/runs/r03/figures/"], False, lang))
    parts.append(box(*B["reality"], "reality/", t["immutable"], ["facts/EXP-001/r03.facts.json", "index.csv  (sha256 per file)", "errata.md  (append-only)"], False, lang))
    parts.append(box(*B["boards"], "boards/", "", ["evidence.csv  findings.csv", "draft.csv  human-owed.csv"], False, lang))
    parts.append(box(*B["manuscript"], "manuscript/", "", ["facts.tex  (generated \\fact{})", "sections/*.tex  figures.yaml"], False, lang))
    parts += [f'<rect x="60" y="506" width="880" height="34" rx="10" fill="#0F172A"/>',
              f'<text x="500" y="528" text-anchor="middle" font-size="13" fill="#E2E8F0" font-family="SFMono-Regular, Menlo, Consolas, monospace">{esc(t["check"])}</text>', "</svg>"]
    return "\n".join(parts) + "\n"


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, suf in (("en", ""), ("zh-TW", ".zh-TW")):
        (OUT / f"loop{suf}.svg").write_text(loop(lang), encoding="utf-8")
        (OUT / f"architecture{suf}.svg").write_text(architecture(lang), encoding="utf-8")
    print("wrote loop + architecture (en, zh-TW)")
