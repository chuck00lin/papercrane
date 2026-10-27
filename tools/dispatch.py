#!/usr/bin/env python3
"""Dispatch a run into a code space (Run stage; invariant I4).

  python3 tools/dispatch.py --experiment EXP-001-slug --run r03 [--codespace name] [--config default]
                            [--variant ct06_ss] [--baseline r01] [--change "..."] [--dry-run]

Creates experiments/<exp>/runs/<run>/run.yaml, hashes the declared inputs, then either runs
the code space's entry command synchronously (adapter `agent.transport` absent or `none`)
or enqueues a task on the bus for the resident agent and leaves the run `dispatched`.
Refuses if the experiment is not `designed`/`running` or targets a disallowed claim
(delegates that to tools/check.py --design).
"""
import argparse, glob, hashlib, os, shlex, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import bus  # noqa: E402


def now():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def die(m):
    print(f"[dispatch] {m}", file=sys.stderr); sys.exit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--experiment", required=True); ap.add_argument("--run", required=True)
    ap.add_argument("--codespace"); ap.add_argument("--config", default="default")
    ap.add_argument("--variant", default="default"); ap.add_argument("--baseline"); ap.add_argument("--change")
    ap.add_argument("--dispatched-by", default="experiment"); ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    exp_dir = ROOT / "experiments" / a.experiment
    ey = exp_dir / "experiment.yaml"
    if not ey.exists():
        die(f"{ey.relative_to(ROOT)} not found; Design before Run")
    exp = yaml.safe_load(open(ey))
    if exp.get("status") not in ("designed", "running"):
        die(f"experiment status is {exp.get('status')!r}; only designed/running can be dispatched")
    rc = subprocess.run([sys.executable, str(ROOT / "tools/check.py"), "--design", a.experiment], capture_output=True, text=True)
    if rc.returncode != 0:
        die("design check failed:\n" + rc.stdout)
    cs_name = a.codespace or exp.get("codespace")
    if not cs_name:
        die("no code space: pass --codespace or set codespace: in experiment.yaml")
    cs_path = ROOT / "codespaces" / f"{cs_name}.yaml"
    if not cs_path.exists():
        die(f"{cs_path.relative_to(ROOT)} not found")
    cs = yaml.safe_load(open(cs_path))
    run_dir = exp_dir / "runs" / a.run
    if run_dir.exists():
        die(f"{run_dir.relative_to(ROOT)} already exists; run ids are never reused")
    cs_root = Path(os.path.expanduser(cs["path"]))
    if not cs_root.is_absolute():
        cs_root = ROOT / cs_root
    # provenance: code commit + input hashes (globs are relative to the code space path)
    commit = "unknown"
    if cs_root.exists():
        r = subprocess.run(["git", "-C", str(cs_root), "rev-parse", "HEAD"], capture_output=True, text=True)
        if r.returncode == 0:
            commit = r.stdout.strip()
    inputs = []
    for pat in cs.get("provenance", {}).get("inputs", []):
        pat = pat.format(experiment=a.experiment, run_id=a.run, config=a.config)
        for f in sorted(glob.glob(str(cs_root / pat), recursive=True))[:500]:
            if Path(f).is_file():
                inputs.append({"path": os.path.relpath(f, cs_root), "sha256": sha256(f)})
    cmd = cs["entry"]["command"].format(experiment=a.experiment, run_id=a.run, config=a.config, variant=a.variant)
    rec = {"run_id": a.run, "experiment": a.experiment, "codespace": cs_name, "command": cmd, "config": a.config,
           "variant": a.variant, "code_commit": commit, "env": cs["entry"].get("env", ""), "started": now(),
           "status": "dispatched", "inputs": inputs, "dispatched_by": a.dispatched_by}
    if a.baseline: rec["baseline_run"] = a.baseline
    if a.change: rec["change_vs_baseline"] = a.change
    if commit == "unknown":
        print("[dispatch] WARNING: code space is not a git checkout; code_commit=unknown will fail the schema until set", file=sys.stderr)
    if a.dry_run:
        print(yaml.safe_dump(rec, sort_keys=False)); return
    run_dir.mkdir(parents=True)
    transport = (cs.get("agent") or {}).get("transport", "none")
    if transport == "bus":
        reply = (cs.get("agent") or {}).get("reply", "").format(task_id=f"{a.experiment}-{a.run}")
        task = f"{a.experiment}-{a.run}"
        payload = {"experiment": a.experiment, "run_id": a.run, "command": cmd, "cwd": cs["entry"].get("cwd", "."),
                   "emit_facts_to": cs["emits"]["facts"].format(run_id=a.run),
                   "closing_condition": f"facts.json written and acked on the bus. Reply via: {reply}"}
        rec["task_id"] = bus.send(cs_name, task, payload, frm=a.dispatched_by, kind="run")
        print(f"[dispatch] enqueued task {task} for agent {cs_name} (msg {rec['task_id']}); run stays `dispatched` until collected")
    else:
        cwd = cs_root / cs["entry"].get("cwd", ".")
        print(f"[dispatch] running in {cwd}: {cmd}")
        r = subprocess.run(cmd, shell=True, cwd=str(cwd) if cwd.exists() else None)
        rec["ended"] = now(); rec["exit_status"] = r.returncode
        rec["status"] = "done" if r.returncode == 0 else "failed"
        print(f"[dispatch] exit {r.returncode} -> {rec['status']}")
    with open(run_dir / "run.yaml", "w") as f:
        yaml.safe_dump(rec, f, sort_keys=False)
    if exp.get("status") == "designed":
        exp["status"] = "running"
        with open(ey, "w") as f:
            yaml.safe_dump(exp, f, sort_keys=False, allow_unicode=True, width=100)
    print(f"[dispatch] wrote {run_dir.relative_to(ROOT)}/run.yaml")


if __name__ == "__main__":
    main()
