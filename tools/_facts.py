"""Shared helpers for status / compare / impact."""
import csv, json, re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent


def load_yaml(p):
    with open(p) as f:
        return yaml.safe_load(f) or {}


def experiments():
    out = {}
    for d in sorted((ROOT / "experiments").iterdir()):
        if d.is_dir() and (d / "experiment.yaml").exists():
            out[d.name] = load_yaml(d / "experiment.yaml")
    return out


def runs(exp_id):
    out = {}
    for ry in sorted((ROOT / "experiments" / exp_id).glob("runs/*/run.yaml")):
        out[ry.parent.name] = load_yaml(ry)
    return out


def frozen_facts():
    """fact id -> fact dict (+ _file). Also returns the set of superseded ids."""
    facts, superseded = {}, set()
    for p in sorted((ROOT / "reality" / "facts").rglob("*.facts.json")):
        d = json.load(open(p))
        for f in d.get("facts", []):
            f = dict(f); f["_file"] = str(p.relative_to(ROOT)); f["_experiment"] = d["experiment"]; f["_run"] = d["run"]
            facts[f["id"]] = f
            if f.get("supersedes"):
                superseded.add(f["supersedes"])
    return facts, superseded


def split_id(fid):
    exp, run, name = fid.rsplit(".", 2)
    return exp, run, name


def adrs():
    out = []
    for p in sorted((ROOT / "decisions").glob("ADR-*.md")):
        t = p.read_text()
        m = re.search(r"^---\n(.*?)\n---", t, re.S)
        fm = yaml.safe_load(m.group(1)) if m else {}
        fm = fm or {}
        fm["_file"] = p.name
        out.append(fm)
    return out


def evidence_rows():
    p = ROOT / "boards" / "evidence.csv"
    return list(csv.DictReader(open(p))) if p.exists() else []
