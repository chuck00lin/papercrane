#!/usr/bin/env python3
"""What must change in the paper now that a run is frozen.
  python3 tools/impact.py --run EXP-001-slug.r03 [--apply]
Lists, for each fact in the run that has an earlier frozen value with the same name:
facts-map keys that still point at the old run, the manuscript lines that use them, figures
that depend on those facts or that run, claim-map rows and evidence rows that cite the old ids.
--apply rewrites manuscript/facts-map.yaml to the new run (then: make render && make check)."""
import argparse, re, sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _facts import ROOT, frozen_facts, split_id, evidence_rows, load_yaml, runs  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True, help="<experiment>.<run>")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    exp, run = a.run.rsplit(".", 1)
    facts, superseded = frozen_facts()
    new = {f["name"]: f for f in facts.values() if f["_experiment"] == exp and f["_run"] == run}
    if not new:
        sys.exit(f"[impact] no frozen facts for {a.run}; freeze first")
    # A run replaces earlier runs of the SAME experiment and the SAME variant. A different
    # variant is a comparison, not a replacement (the leaderboard shows those side by side).
    rs = runs(exp)
    variant = (rs.get(run) or {}).get("variant")
    same_variant = {r for r, rec in rs.items() if rec.get("variant") == variant} if variant else set(rs)
    old_ids = {}  # old id -> new id
    for name, f in new.items():
        for g in facts.values():
            if (g["_experiment"] == exp and g["name"] == name and g["_run"] != run
                    and g["_run"] < run and g["_run"] in same_variant):
                old_ids[g["id"]] = f["id"]
    print(f"# Impact of {a.run}  (variant: {variant or 'unspecified'})\n")
    print(f"{len(new)} fact(s) in the run; {len(old_ids)} earlier value(s) with the same name and variant.\n")
    if not old_ids:
        print("Nothing in the paper can depend on an earlier value of these facts. New facts only."); return
    # facts-map keys
    fm_path = ROOT / "manuscript" / "facts-map.yaml"
    fm = load_yaml(fm_path) if fm_path.exists() else {}
    keys = {k: s for k, s in (fm.get("facts") or {}).items() if s.get("id") in old_ids}
    print("## facts-map keys pointing at the old run")
    for k, s in keys.items():
        print(f"- `{k}`: {s['id']}  ->  {old_ids[s['id']]}")
    if not keys: print("- none")
    # manuscript lines
    print("\n## manuscript lines using those keys")
    hits = 0
    for p in sorted((ROOT / "manuscript" / "sections").glob("*.tex")) if (ROOT / "manuscript" / "sections").exists() else []:
        for i, line in enumerate(p.read_text().splitlines(), 1):
            used = [k for k in keys if re.search(r"\\fact\{" + re.escape(k) + r"\}", line)]
            if used:
                hits += 1; print(f"- {p.relative_to(ROOT)}:{i}  [{', '.join(used)}]  {line.strip()[:90]}")
    if not hits: print("- none")
    # figures
    print("\n## figures depending on these facts")
    figs = (load_yaml(ROOT / "manuscript" / "figures.yaml").get("figures") or {}) if (ROOT / "manuscript" / "figures.yaml").exists() else {}
    fh = 0
    for fid, spec in figs.items():
        dep = set(spec.get("facts") or [])
        same_run = spec.get("experiment") == exp and spec.get("run") in {split_id(o)[1] for o in old_ids}
        if dep & set(old_ids) or same_run:
            fh += 1; print(f"- {fid}: file `{spec.get('file')}` from run {spec.get('run')}; re-export from the new run and update sha256")
    if not fh: print("- none")
    # claim rows + evidence rows + method-trace parameters
    print("\n## identity and boards citing the old ids")
    ch = 0
    for name in ("claim-map.md", "method-trace.md"):
        p = ROOT / "identity" / name
        if p.exists():
            for i, line in enumerate(p.read_text().splitlines(), 1):
                cited = [o for o in old_ids if o in line]
                if cited: ch += 1; print(f"- identity/{name}:{i}  {cited}")
    for r in evidence_rows():
        cited = [o for o in old_ids if o in (r.get("fact_ids") or "")]
        if cited: ch += 1; print(f"- boards/evidence.csv claim {r.get('claim_id')}: {cited}")
    if not ch: print("- none")
    if a.apply and keys:
        for k in keys:
            fm["facts"][k]["id"] = old_ids[fm["facts"][k]["id"]]
        with open(fm_path, "w") as f:
            yaml.safe_dump(fm, f, sort_keys=False)
        print(f"\n[impact] facts-map remapped for {len(keys)} key(s). Next: make render && make check; "
              "update identity/boards rows listed above by hand (they are claims, not renders).")
    elif keys:
        print("\nRun with --apply to remap facts-map.yaml, then make render && make check.")


if __name__ == "__main__":
    main()
