#!/usr/bin/env python3
"""Freeze a code space's facts.json into reality/ (invariant I2).

Usage:
  python3 tools/freeze.py <facts.json> [--run experiments/<exp>/runs/<run>/run.yaml] [--errata "reason"]

Steps: validate against schemas/facts.schema.json; refuse id collisions with already-frozen
facts; copy to reality/facts/<exp>/<run>.facts.json; record sha256 in reality/index.csv;
if a run record is given, write facts_file + facts_sha256 into it; if any fact declares
`supersedes`, require --errata and append one line per superseded id to reality/errata.md.
"""
import csv, hashlib, json, shutil, sys
from datetime import date
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent


def die(msg):
    print(f"[freeze] {msg}", file=sys.stderr)
    sys.exit(1)


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def frozen_ids():
    ids = set()
    for p in (ROOT / "reality" / "facts").rglob("*.facts.json"):
        ids |= {f["id"] for f in json.load(open(p)).get("facts", [])}
    return ids


def main(argv):
    if not argv:
        die(__doc__)
    src = Path(argv[0])
    run_rec = Path(argv[argv.index("--run") + 1]) if "--run" in argv else None
    errata = argv[argv.index("--errata") + 1] if "--errata" in argv else None
    if not src.exists():
        die(f"{src} not found")
    data = json.load(open(src))
    v = Draft202012Validator(json.load(open(ROOT / "schemas" / "facts.schema.json")))
    errs = list(v.iter_errors(data))
    if errs:
        for e in errs:
            print(f"[freeze] schema: {'/'.join(map(str, e.path)) or '<root>'}: {e.message}", file=sys.stderr)
        sys.exit(1)
    exp, run = data["experiment"], data["run"]
    if not (ROOT / "experiments" / exp / "experiment.yaml").exists():
        die(f"experiments/{exp}/experiment.yaml does not exist; design before run")
    already = frozen_ids()
    ids = [f["id"] for f in data["facts"]]
    bad = [i for i in ids if not i.startswith(f"{exp}.{run}.")]
    if bad:
        die(f"fact ids must start with {exp}.{run}.: {bad}")
    if len(set(ids)) != len(ids):
        die("duplicate fact ids inside the file")
    clash = sorted(set(ids) & already)
    if clash:
        die(f"fact ids already frozen (use a new run id): {clash}")
    sup = [(f["id"], f["supersedes"]) for f in data["facts"] if f.get("supersedes")]
    if sup and not errata:
        die(f"{len(sup)} fact(s) declare supersedes; pass --errata \"reason\"")
    for new, old in sup:
        if old not in already:
            die(f"{new} supersedes {old}, which is not a frozen fact")
    dst = ROOT / "reality" / "facts" / exp / f"{run}.facts.json"
    if dst.exists():
        die(f"{dst.relative_to(ROOT)} already exists; frozen files are never overwritten")
    dst.parent.mkdir(parents=True, exist_ok=True)
    # table facts: copy the referenced file next to the facts file and point the value at it
    extra = []
    for f in data["facts"]:
        if f.get("kind") == "table":
            tsrc = src.parent / str(f["value"])
            if not tsrc.exists():
                die(f"table fact {f['id']} references missing file {tsrc}")
            tdst = dst.parent / f"{run}.{f['name']}{tsrc.suffix}"
            shutil.copyfile(tsrc, tdst)
            f["value"] = tdst.name
            extra.append(tdst)
    dst.write_text(json.dumps(data, indent=1))
    digest = sha256(dst)
    idx = ROOT / "reality" / "index.csv"
    new_file = not idx.exists() or idx.stat().st_size == 0
    with open(idx, "a", newline="") as f:
        w = csv.writer(f)
        if new_file:
            w.writerow(["fact_file", "sha256", "experiment", "run", "frozen_at", "frozen_by"])
        w.writerow([str(dst.relative_to(ROOT / "reality")), digest, exp, run, date.today().isoformat(), "experiment"])
        for tdst in extra:
            w.writerow([str(tdst.relative_to(ROOT / "reality")), sha256(tdst), exp, run, date.today().isoformat(), "experiment"])
    if sup:
        with open(ROOT / "reality" / "errata.md", "a") as f:
            for new, old in sup:
                f.write(f"- {date.today().isoformat()}  {new} supersedes {old} — {errata}\n")
    if run_rec:
        rec = yaml.safe_load(open(run_rec)) or {}
        rec["facts_file"] = str(dst.relative_to(ROOT))
        rec["facts_sha256"] = digest
        if rec.get("status") == "dispatched":          # bus transport: facts arriving closes the run
            from datetime import datetime, timezone
            rec["status"], rec["exit_status"] = "done", 0
            rec["ended"] = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
        with open(run_rec, "w") as f:
            yaml.safe_dump(rec, f, sort_keys=False)
    print(f"[freeze] {dst.relative_to(ROOT)}  sha256={digest[:12]}…  {len(ids)} fact(s)")


if __name__ == "__main__":
    main(sys.argv[1:])
