#!/usr/bin/env python3
"""papercrane checker. Consistency is a program, not a ritual (invariant I8).

Usage:
  python3 tools/check.py            run every check
  python3 tools/check.py --design EXP-001-slug   design checks for one experiment only
Exit status 1 if any check fails.
"""
import csv, hashlib, json, re, sys
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent.parent
FAILS, WARNS = [], []
FACT_ID = re.compile(r"^EXP-[0-9]{3}[a-z0-9-]*\.r[0-9]{2,}\.[a-z][a-z0-9_]*$")


def fail(check, where, msg):
    FAILS.append(f"[FAIL] {check}: {where}: {msg}")


def warn(check, where, msg):
    WARNS.append(f"[WARN] {check}: {where}: {msg}")


def load_yaml(p):
    with open(p) as f:
        return yaml.safe_load(f)


def schema(name):
    with open(ROOT / "schemas" / f"{name}.schema.json") as f:
        return Draft202012Validator(json.load(f))


def validate(name, data, where):
    for err in sorted(schema(name).iter_errors(data), key=lambda e: list(e.path)):
        path = "/".join(str(x) for x in err.path) or "<root>"
        fail("schema", f"{where}:{path}", err.message)


def coerce_run(r):
    """YAML parses all-digit hashes and commits as integers; the schema wants strings."""
    for k in ("code_commit", "facts_sha256", "run_id"):
        if k in r and not isinstance(r[k], str):
            r[k] = str(r[k])
    for inp in r.get("inputs", []) or []:
        if isinstance(inp, dict) and "sha256" in inp and not isinstance(inp["sha256"], str):
            inp["sha256"] = str(inp["sha256"]).zfill(64)
    return r


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ---------- claim-map parsing (markdown tables) ----------
def md_table_ids(text, heading_prefix, col=0):
    """Return first-column ids from the markdown table under the heading."""
    ids = []
    in_section, in_table = False, False
    for line in text.splitlines():
        if line.startswith("## "):
            in_section = line.startswith(heading_prefix)
            in_table = False
            continue
        if not in_section:
            continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if set("".join(cells)) <= set("-: "):
                in_table = True
                continue
            if in_table and cells and cells[col]:
                ids.append(cells[col])
    return ids


def claim_map():
    p = ROOT / "identity" / "claim-map.md"
    text = p.read_text() if p.exists() else ""
    allowed = {i for i in md_table_ids(text, "## 1.") if re.match(r"^C\d+", i)}
    disallowed = {i for i in md_table_ids(text, "## 2.") if re.match(r"^D\d+", i)}
    return allowed, disallowed


# ---------- checks ----------
def check_codespaces():
    names = set()
    for p in sorted((ROOT / "codespaces").glob("*.yaml")):
        d = load_yaml(p) or {}
        validate("codespace", d, p.relative_to(ROOT))
        names.add(d.get("name"))
    return names


def check_experiments(only=None, codespaces=()):
    allowed, disallowed = claim_map()
    for exp_dir in sorted((ROOT / "experiments").iterdir()):
        if not exp_dir.is_dir() or (only and exp_dir.name != only):
            continue
        ey = exp_dir / "experiment.yaml"
        if not ey.exists():
            fail("schema", exp_dir.relative_to(ROOT), "missing experiment.yaml")
            continue
        d = load_yaml(ey) or {}
        where = ey.relative_to(ROOT)
        validate("experiment", d, where)
        if d.get("id") != exp_dir.name:
            fail("schema", where, f"id {d.get('id')!r} != folder name {exp_dir.name!r}")
        # design checks
        emitted = {e.get("name") for e in d.get("emits", [])}
        for t in d.get("targets", []):
            cid = t.get("claim")
            if cid in disallowed:
                fail("design", where, f"targets disallowed claim {cid}")
            elif cid not in allowed:
                fail("design", where, f"targets claim {cid} not present in identity/claim-map.md §1")
        if not emitted:
            fail("design", where, "emits nothing; no target can be supported")
        if d.get("codespace") and d["codespace"] not in codespaces:
            fail("cross-ref", where, f"codespace {d['codespace']!r} has no codespaces/*.yaml")
        comparative = any(re.search(r"\b(vs|versus|than|compar|treatment|effect)\b", t.get("needs", ""), re.I)
                          for t in d.get("targets", []))
        if comparative and not d.get("design", {}).get("controls"):
            fail("design", where, "a target is comparative but design.controls is empty")
        check_emits_contract(d, where)
        # runs
        for ry in sorted(exp_dir.glob("runs/*/run.yaml")):
            r = coerce_run(load_yaml(ry) or {})
            validate("run", r, ry.relative_to(ROOT))
            if r.get("status") == "dispatched":
                warn("runs", ry.relative_to(ROOT), "in flight (dispatched, not collected)")
            if r.get("code_commit") == "unknown":
                fail("schema", ry.relative_to(ROOT), "code_commit is unknown; the code space must be a git checkout")
            if r.get("experiment") != d.get("id"):
                fail("cross-ref", ry.relative_to(ROOT), "run.experiment != experiment.id")


def check_emits_contract(d, where):
    """The design contract's emits[] against what the experiment's runs actually froze."""
    declared = {e.get("name"): e for e in d.get("emits", []) if isinstance(e, dict)}
    seen = set()
    for p in sorted((ROOT / "reality" / "facts" / str(d.get("id"))).glob("*.facts.json")):
        try:
            doc = json.load(open(p))
        except Exception:
            continue                                   # check_reality reports unreadable files
        for f in doc.get("facts", []):
            name = f.get("name") or str(f.get("id", "")).rsplit(".", 1)[-1]
            seen.add(name)
            rel = p.relative_to(ROOT)
            if name not in declared:
                fail("design", where, f"{rel} froze fact {name!r}, which emits[] does not declare")
                continue
            for key in ("kind", "unit"):
                if f.get(key) != declared[name].get(key):
                    fail("design", where, f"{rel} froze {name!r} with {key} {f.get(key)!r}; emits[] declares {declared[name].get(key)!r}")
    if seen:
        for name in sorted(set(declared) - seen):
            msg = f"emits[] declares {name!r}, which no frozen run has produced"
            (fail if d.get("status") == "frozen" else warn)("design", where, msg)


_FROZEN = None


def frozen_fact_ids():
    global _FROZEN
    if _FROZEN is None:
        _FROZEN = set()
        for p in (ROOT / "reality" / "facts").rglob("*.facts.json"):
            try:
                for f in json.load(open(p)).get("facts", []):
                    _FROZEN.add(f.get("id"))
            except Exception:
                pass
    return _FROZEN


def check_reality():
    idx = ROOT / "reality" / "index.csv"
    indexed = {}
    if idx.exists():
        for row in csv.DictReader(open(idx)):
            indexed[row["fact_file"]] = row["sha256"]
            p = ROOT / "reality" / row["fact_file"]
            if not p.exists():
                fail("freeze", f"reality/index.csv", f"{row['fact_file']} listed but missing")
            elif sha256(p) != row["sha256"]:
                fail("freeze", row["fact_file"], "hash differs from reality/index.csv (frozen file edited?)")
    errata = (ROOT / "reality" / "errata.md").read_text() if (ROOT / "reality" / "errata.md").exists() else ""
    seen = set()
    for p in sorted((ROOT / "reality" / "facts").rglob("*.facts.json")):
        rel = str(p.relative_to(ROOT / "reality"))
        if rel not in indexed:
            fail("freeze", rel, "frozen file not in reality/index.csv")
        try:
            d = json.load(open(p))
        except Exception as e:
            fail("schema", rel, f"not valid JSON: {e}")
            continue
        validate("facts", d, rel)
        for f in d.get("facts", []):
            fid = f.get("id", "")
            if fid in seen:
                fail("freeze", rel, f"duplicate fact id {fid}")
            seen.add(fid)
            if not fid.startswith(f"{d.get('experiment')}.{d.get('run')}."):
                fail("schema", rel, f"fact id {fid} does not match experiment.run prefix")
            if f.get("supersedes") and fid not in errata:
                fail("freeze", rel, f"{fid} supersedes {f['supersedes']} but has no line in reality/errata.md")
            if f.get("kind") == "table":
                tpath = p.parent / str(f.get("value"))
                trel = str(tpath.relative_to(ROOT / "reality")) if tpath.exists() else None
                if not tpath.exists():
                    fail("freeze", rel, f"table fact {fid} references missing file {f.get('value')}")
                elif trel not in indexed:
                    fail("freeze", rel, f"table file {trel} not in reality/index.csv")


BOARDS = {
    "evidence.csv": {"status": {"pending", "partial", "frozen"}},
    "findings.csv": {"severity": {"BLOCKER", "MAJOR", "MINOR", "NOTE"}, "status": {"open", "resolved", "declined"}},
    "draft.csv": {"state": {"empty", "outline", "drafted", "polished"}, "polish_passed": {"yes", "no"}},
    "human-owed.csv": {"status": {"open", "done"}},
}


def check_boards():
    for name, enums in BOARDS.items():
        p = ROOT / "boards" / name
        if not p.exists():
            fail("boards", f"boards/{name}", "missing")
            continue
        for i, row in enumerate(csv.DictReader(open(p)), start=2):
            for k, v in row.items():
                if v and len(v) > 160:
                    fail("boards", f"boards/{name}:{i}", f"cell {k} is {len(v)} chars (limit 160)")
                if k in enums and v and v not in enums[k]:
                    fail("boards", f"boards/{name}:{i}", f"{k}={v!r} not in {sorted(enums[k])}")
            if name == "evidence.csv":
                for fid in filter(None, (row.get("fact_ids") or "").split(";")):
                    if row.get("status") == "frozen" and fid not in frozen_fact_ids():
                        fail("anchors", f"boards/{name}:{i}", f"status frozen but {fid} is not a frozen fact")


def check_identity():
    mt = ROOT / "identity" / "method-trace.md"
    if mt.exists():
        for fid in md_table_ids(mt.read_text(), "## 5.", col=1):
            if not FACT_ID.match(fid):
                fail("anchors", "identity/method-trace.md §5", f"parameter value {fid!r} is a literal, not a fact id")
    cm = ROOT / "identity" / "claim-map.md"
    if cm.exists():
        text = cm.read_text()
        for row in md_table_ids(text, "## 1.", col=3):
            for fid in re.split(r"[;,\s]+", row):
                if fid and not FACT_ID.match(fid):
                    fail("anchors", "identity/claim-map.md §1", f"fact anchor {fid!r} malformed")
                elif fid and fid not in frozen_fact_ids():
                    warn("anchors", "identity/claim-map.md §1", f"fact anchor {fid} not frozen yet")


MATH_ENVS = ("equation", "equation*", "align", "align*", "gather", "gather*", "eqnarray", "multline")


def strip_tex(line):
    line = re.sub(r"(?<!\\)%.*$", "", line)
    line = re.sub(r"[\^_]\{?\d+\}?", " ", line)                      # R^2, CO_2, x^{10}
    line = re.sub(r"\\(fact|ref|cite\w*|label|eqref|pageref|includegraphics)(\[[^\]]*\])?\{[^}]*\}", " ", line)
    line = re.sub(r"\\(begin|end)\{[^}]*\}", " ", line)
    return line


def check_figures():
    fy = ROOT / "manuscript" / "figures.yaml"
    if not fy.exists():
        return
    for fid, spec in ((load_yaml(fy) or {}).get("figures") or {}).items():
        f = ROOT / "manuscript" / str(spec.get("file", ""))
        if not spec.get("file") or not f.exists():
            fail("figures", f"manuscript/figures.yaml:{fid}", f"file {spec.get('file')!r} missing under manuscript/")
        elif spec.get("sha256") and sha256(f) != spec["sha256"]:
            fail("figures", f"manuscript/figures.yaml:{fid}", "file hash differs from figures.yaml (re-exported figure not re-registered?)")
        for dep in spec.get("facts") or []:
            if dep not in frozen_fact_ids():
                fail("figures", f"manuscript/figures.yaml:{fid}", f"depends on {dep}, which is not a frozen fact")


def check_manuscript():
    fm = ROOT / "manuscript" / "facts-map.yaml"
    allow = []
    if fm.exists():
        allow = [re.compile(a) for a in (load_yaml(fm) or {}).get("allow_literals", [])]
    terms = []
    tcsv = ROOT / "identity" / "terminology.csv"
    if tcsv.exists():
        for row in csv.DictReader(open(tcsv)):
            for v in filter(None, row["forbidden_variants"].split(";")):
                terms.append((v.strip(), row["canonical"], re.compile(r"(?<![\w-])" + re.escape(v.strip()) + r"(?![\w-])")))
    for p in sorted((ROOT / "manuscript" / "sections").glob("*.tex")) if (ROOT / "manuscript" / "sections").exists() else []:
        in_math = False
        for i, raw in enumerate(p.read_text().splitlines(), start=1):
            if re.search(r"\\begin\{(" + "|".join(re.escape(e) for e in MATH_ENVS) + r")\}", raw):
                in_math = True
            if re.search(r"\\end\{(" + "|".join(re.escape(e) for e in MATH_ENVS) + r")\}", raw):
                in_math = False
                continue
            line = strip_tex(raw)
            if in_math:
                continue
            for num in re.findall(r"(?<![\w\\{])\d+(?:\.\d+)?(?![\w}])", line):
                if not any(a.search(num) for a in allow):
                    fail("numerals", f"{p.relative_to(ROOT)}:{i}", f"bare numeral {num!r}; use \\fact{{}} or allow_literals")
            for v, canon, rx in terms:
                if rx.search(line):
                    fail("terminology", f"{p.relative_to(ROOT)}:{i}", f"{v!r} -> use {canon!r}")
    lab = ROOT / "manuscript" / "labels.yaml"
    if lab.exists():
        for k, v in ((load_yaml(lab) or {}).get("labels") or {}).items():
            for var, canon, rx in terms:
                if rx.search(str(v)):
                    fail("terminology", f"manuscript/labels.yaml:{k}", f"{var!r} -> use {canon!r}")


def main(argv):
    only = None
    if "--design" in argv:
        only = argv[argv.index("--design") + 1]
        check_experiments(only=only, codespaces=check_codespaces())
    else:
        cs = check_codespaces()
        check_experiments(codespaces=cs)
        check_reality()
        check_boards()
        check_identity()
        check_figures()
        check_manuscript()
    for w in WARNS:
        print(w)
    for f in FAILS:
        print(f)
    print(f"\n{len(FAILS)} failure(s), {len(WARNS)} warning(s)")
    return 1 if FAILS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
