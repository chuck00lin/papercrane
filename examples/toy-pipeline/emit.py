#!/usr/bin/env python3
"""Toy facts exporter: lane-keeping metrics for one controller on the simulated test track.
Replace the body with your analysis; keep the shape of the output."""
import csv, hashlib, json, subprocess, sys
from datetime import datetime
from pathlib import Path

exp, run, controller = sys.argv[1:4]            # CFG selects the controller to summarise
here = Path(__file__).resolve().parent
src = here / "data" / exp / "episodes.csv"
rows = [r for r in csv.DictReader(open(src)) if r["controller"] == controller]
if not rows:
    sys.exit(f"[toy-pipeline] no episodes for controller {controller!r}")
n = len(rows)
rmse = [float(r["lateral_rmse_cm"]) for r in rows]
lane_rmse = sum(rmse) / n
lane_max = max(float(r["lateral_max_cm"]) for r in rows)
collisions = sum(int(r["collision"]) for r in rows)
completion = sum(int(r["completed"]) for r in rows) / n
commit = subprocess.run(["git", "-C", str(here), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip() or "unknown"
fid = lambda name: f"{exp}.{run}.{name}"
doc = {"experiment": exp, "run": run,
       "provenance": {"codespace": "example-pipeline", "code_commit": commit, "command": " ".join(sys.argv),
                      "inputs": [{"path": str(src.relative_to(here)), "sha256": hashlib.sha256(src.read_bytes()).hexdigest()}],
                      "produced_at": datetime.now().astimezone().isoformat(timespec="seconds"), "controller": controller},
       "facts": [
           {"id": fid("episodes"), "name": "episodes", "kind": "count", "value": n, "unit": None, "definition": "simulated episodes (one lap of track T1 per seed) for this controller"},
           {"id": fid("lane_rmse_cm"), "name": "lane_rmse_cm", "kind": "metric", "value": round(lane_rmse, 3), "unit": "cm", "n": n, "definition": "mean over episodes of the per-episode RMSE of lateral error against the lane centre"},
           {"id": fid("lane_max_cm"), "name": "lane_max_cm", "kind": "metric", "value": round(lane_max, 2), "unit": "cm", "n": n, "definition": "largest lateral error observed in any episode"},
           {"id": fid("collisions"), "name": "collisions", "kind": "count", "value": collisions, "unit": None, "definition": "episodes that ended in a collision"},
           {"id": fid("completion_rate"), "name": "completion_rate", "kind": "metric", "value": round(completion, 4), "unit": None, "n": n, "definition": "fraction of episodes that completed the lap"}]}
out = here / "runs" / run / "facts.json"; out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(doc, indent=1)); print(f"[toy-pipeline] wrote {out.relative_to(here)}  controller={controller} episodes={n}")
