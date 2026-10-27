#!/usr/bin/env python3
"""Simulate one session of the loop on the toy pipeline, as three roles in three panes.

Every `$` command below really runs; its output is captured as-is. The `you ›` and `head ›`
lines are scripted, standing in for the conversation a human has with the paper agent.
Writes docs/assets/session/transcript.json for tools/dev/render_session.py. `make session-clean` resets.
"""
import json, os, re, shutil, subprocess, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "docs" / "assets" / "session"
EXP = "EXP-000-example"
T = []          # transcript events


def beat(title):
    T.append({"beat": title})


def say(pane, who, text):
    for i, line in enumerate(text.splitlines()):
        T.append({"pane": pane, "kind": who if i == 0 else who + "-cont", "text": line})


def cmd(pane, command, cwd=None, max_lines=14, ok=True):
    T.append({"pane": pane, "kind": "cmd", "text": command})
    r = subprocess.run(command, shell=True, cwd=str(cwd or ROOT), capture_output=True, text=True)
    out = (r.stdout + r.stderr).replace(str(ROOT) + "/", "").rstrip().splitlines()
    if len(out) > max_lines:
        out = out[:max_lines - 1] + [f"… ({len(out) - max_lines + 1} more lines)"]
    for line in out:
        T.append({"pane": pane, "kind": "fail" if line.startswith("[FAIL]") else "out", "text": line})
    if ok and r.returncode != 0:
        print("\n".join(out), file=sys.stderr)
        raise SystemExit(f"[session] command failed: {command}")
    return r.stdout


def msg_id(poll_out):
    m = re.search(r'"id": "([0-9a-f]{12})"', poll_out)
    return m.group(1) if m else ""


def main():
    os.chdir(ROOT)
    # ---- beat 1: design, pre-registration (human-led)
    beat("Design: the contract is pre-registered before anything runs")
    say("head", "you", "/design-review EXP-000-example")
    say("head", "head", "Stage: design · Experiment: EXP-000-example · Skill: skills/design-review.md\n"
                        "Authoritative: identity/claim-map.md, experiments/EXP-000-example/experiment.yaml\n"
                        "Excluded: tmp/, chat backups · Identity touch: none\n"
                        "Closing: tools/check.py --design passes and your decision is an ADR")
    cmd("head", f"python3 tools/check.py --design {EXP}")
    say("head", "head", "C1 is targeted and allowed. The contrast has a control: the baseline controller on\n"
                        "the same twelve seeds. The reference protocol names the lane centre and says the\n"
                        "logger is blind to the controller. Dispatch baseline and tuned?")
    say("head", "you", "yes, baseline then tuned")
    # ---- beat 2: head hands the runs to the experiment agent over the bus
    beat("Run: head hands the work to the experiment agent over the file-queue bus")
    out = cmd("head", f"python3 tools/bus.py send --to experiment --task {EXP}-runs --from head "
                      "--payload '{\"runs\": [[\"r01\",\"baseline\"],[\"r02\",\"tuned\"]], \"codespace\": \"example-pipeline-bus\"}'")
    head_task = out.strip()
    cmd("experiment", "python3 tools/bus.py poll --agent experiment", max_lines=3)
    # ---- beat 3/4: dispatch into the code space, which runs and acks
    for run, cfg, base in (("r01", "baseline", ""), ("r02", "tuned", " --baseline r01 --change \"lateral gain retuned on T1\"")):
        beat(f"Run {run}: dispatch → code space runs `make run` → ack → freeze")
        cmd("experiment", f"python3 tools/dispatch.py --experiment {EXP} --run {run} --config {cfg} --variant {cfg}{base} --codespace example-pipeline-bus")
        poll = cmd("codespace", "python3 tools/bus.py poll --agent example-pipeline-bus", max_lines=3)
        mid = msg_id(poll)
        cmd("codespace", f"make run EXP={EXP} RUN={run} CFG={cfg}", cwd=ROOT / "examples" / "toy-pipeline")
        cmd("codespace", f"python3 tools/bus.py ack --agent example-pipeline-bus --id {mid} --result '{{\"facts\": \"runs/{run}/facts.json\"}}'")
        cmd("experiment", f"python3 tools/bus.py wait --to experiment --task {EXP}-{run} --timeout 10", max_lines=2)
        cmd("experiment", f"python3 tools/freeze.py examples/toy-pipeline/runs/{run}/facts.json --run experiments/{EXP}/runs/{run}/run.yaml")
    # ---- beat 5: analyze, report back as questions
    beat("Analyze: leaderboard, then the report goes back to head as questions")
    cmd("experiment", f"python3 tools/compare.py --experiment {EXP} --facts lane_rmse_cm,collisions")
    cmd("experiment", f"python3 tools/bus.py ack --agent experiment --id {head_task} --result '{{\"frozen\": [\"r01\", \"r02\"]}}'")
    cmd("head", f"python3 tools/bus.py wait --to head --task {EXP}-runs --timeout 10", max_lines=2)
    say("head", "head", "Both runs are frozen. Tuned: 13.8 cm mean lateral RMSE, 0 collisions. Baseline:\n"
                        "22.2 cm, 2 collisions, same seeds. Two questions for you, not conclusions:\n"
                        "does the paper carry r02 against r01, and is a drop of this size what you\n"
                        "expected on track T1?")
    # ---- beat 6: interpret (human-led) → ADR
    beat("Interpret: the human decides; the decision becomes an ADR")
    say("head", "you", "yes on both. carry r02 vs r01. next run is a second track, same seeds.")
    say("head", "head", "Drafting ADR-0001: decision, alternatives rejected, why. Writing it on your ok.")
    say("head", "you", "ok")
    adr = ROOT / "decisions" / "ADR-0001-carry-r02-vs-r01.md"
    adr.write_text(f"""---
id: ADR-0001
date: {date.today().isoformat()}
status: accepted
supersedes: none
experiment: {EXP}
facts: [{EXP}.r02.lane_rmse_cm, {EXP}.r01.lane_rmse_cm, {EXP}.r02.collisions, {EXP}.r01.collisions]
touches: [claim-map C1, manuscript/sections/03-results.tex]
---

**Decision.** The paper carries the tuned controller (r02) against the baseline (r01) on track T1.

**Alternatives rejected.** Report tuned alone (no contrast, the claim needs one). Wait for a second track before reporting (the second track is the next experiment, EXP-001).

**Why.** Same seeds, blind logger, a control for the contrast; lateral RMSE and collisions both moved in the same direction. Transfer to other tracks is the next design question, pre-registered as EXP-001.
""")
    cmd("head", "sed -n '10,14p' decisions/ADR-0001-carry-r02-vs-r01.md")
    # ---- beat 7: write → render → check → pdf
    beat("Write: render the facts, check, build")
    cmd("head", "python3 tools/render-facts.py")
    cmd("head", "python3 tools/check.py")
    if shutil.which("pdflatex"):
        cmd("head", "make pdf", max_lines=2)
        cmd("head", "pdftotext manuscript/main.pdf - | sed -n '5,8p'", max_lines=4)
    else:
        say("head", "head", "(pdflatex is not installed here; make pdf skipped)")
    say("head", "head", "Stage closed: ADR-0001 exists, the checker is green, the Results sentence reads its\n"
                        "five numbers from facts.tex. Next: /design-review EXP-001 for the second track.")
    beat("Done")
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "transcript.json").write_text(json.dumps(T, indent=0, ensure_ascii=False))
    print(f"[session] {len(T)} events, {sum(1 for e in T if 'beat' in e)} beats -> {OUT.relative_to(ROOT)}/transcript.json")


if __name__ == "__main__":
    main()
