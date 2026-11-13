"""End-to-end test of the loop on the toy pipeline, in a scratch copy of the workspace."""
import json, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXP = "EXP-000-example"


def run(ws, *args, ok=True):
    r = subprocess.run([sys.executable, *args], cwd=ws, capture_output=True, text=True)
    if ok:
        assert r.returncode == 0, r.stdout + r.stderr
    return r


def dispatch(ws, run_id, cfg, variant, baseline=None):
    args = ["tools/dispatch.py", "--experiment", EXP, "--run", run_id, "--config", cfg, "--variant", variant]
    if baseline:
        args += ["--baseline", baseline, "--change", "test"]
    run(ws, *args)
    run(ws, "tools/freeze.py", f"examples/toy-pipeline/runs/{run_id}/facts.json", "--run", f"experiments/{EXP}/runs/{run_id}/run.yaml")


def test_empty_workspace_validates(ws):
    assert "0 failure(s)" in run(ws, "tools/check.py").stdout


def test_dispatch_freeze_render_check(ws):
    dispatch(ws, "r01", "baseline", "baseline")
    frozen = ws / "reality" / "facts" / EXP / "r01.facts.json"
    assert frozen.exists()
    assert len((ws / "reality" / "index.csv").read_text().splitlines()) == 2
    dispatch(ws, "r02", "tuned", "tuned", baseline="r01")
    run(ws, "tools/render-facts.py")
    tex = (ws / "manuscript" / "facts.tex").read_text()
    assert "fact@lane_rmse_tuned" in tex and "fact@collisions_baseline" in tex
    assert "0 failure(s)" in run(ws, "tools/check.py").stdout


def test_duplicate_freeze_refused(ws):
    dispatch(ws, "r01", "baseline", "baseline")
    r = run(ws, "tools/freeze.py", "examples/toy-pipeline/runs/r01/facts.json", ok=False)
    assert r.returncode == 1 and "already frozen" in r.stderr


def test_tampered_frozen_file_fails_check(ws):
    dispatch(ws, "r01", "baseline", "baseline")
    f = ws / "reality" / "facts" / EXP / "r01.facts.json"
    d = json.loads(f.read_text()); d["facts"][0]["value"] = 0.5; f.write_text(json.dumps(d))
    r = run(ws, "tools/check.py", ok=False)
    assert "hash differs" in r.stdout


def test_bare_numeral_fails_check(ws):
    dispatch(ws, "r01", "baseline", "baseline")
    dispatch(ws, "r02", "tuned", "tuned", baseline="r01")
    run(ws, "tools/render-facts.py")
    sec = ws / "manuscript" / "sections" / "03-results.tex"
    sec.write_text(sec.read_text() + "\nAn earlier study reported 0.95 here.\n")
    r = run(ws, "tools/check.py", ok=False)
    assert "bare numeral '0.95'" in r.stdout


def test_frozen_facts_match_design_contract(ws):
    """The example contract declares exactly what the toy pipeline freezes."""
    dispatch(ws, "r01", "baseline", "baseline")
    import yaml
    declared = {e["name"] for e in yaml.safe_load((ws / "experiments" / EXP / "experiment.yaml").read_text())["emits"]}
    frozen = {f["name"] for f in json.loads((ws / "reality" / "facts" / EXP / "r01.facts.json").read_text())["facts"]}
    assert declared == frozen
    out = run(ws, "tools/check.py").stdout
    assert "0 failure(s), 0 warning(s)" in out


def test_undeclared_or_missing_emit_fails_check(ws):
    dispatch(ws, "r01", "baseline", "baseline")
    ey = ws / "experiments" / EXP / "experiment.yaml"
    import yaml
    contract = yaml.safe_load(ey.read_text())           # dispatch re-dumps the file, so edit it as data

    def rewrite(target, **changes):
        d = json.loads(json.dumps(contract))
        next(e for e in d["emits"] if e["name"] == target).update(changes)
        ey.write_text(yaml.safe_dump(d, sort_keys=False))

    rewrite("collisions", name="near_misses")
    r = run(ws, "tools/check.py", ok=False)
    assert r.returncode == 1 and "froze fact 'collisions', which emits[] does not declare" in r.stdout
    assert "[WARN] design" in r.stdout and "declares 'near_misses'" in r.stdout
    rewrite("lane_max_cm", unit="m")
    r = run(ws, "tools/check.py", ok=False)
    assert r.returncode == 1 and "froze 'lane_max_cm' with unit 'cm'; emits[] declares 'm'" in r.stdout


def test_impact_respects_variant_and_remaps(ws):
    dispatch(ws, "r01", "baseline", "baseline")
    dispatch(ws, "r02", "tuned", "tuned", baseline="r01")          # other variant: no impact
    out = run(ws, "tools/impact.py", "--run", f"{EXP}.r02").stdout
    assert "0 earlier value(s)" in out
    dispatch(ws, "r03", "baseline", "baseline", baseline="r01")   # same variant: replaces r01
    out = run(ws, "tools/impact.py", "--run", f"{EXP}.r03").stdout
    assert "lane_rmse_baseline" in out and "lane_rmse_tuned" not in out and "03-results.tex" in out
    run(ws, "tools/impact.py", "--run", f"{EXP}.r03", "--apply")
    run(ws, "tools/render-facts.py")
    tex = (ws / "manuscript" / "facts.tex").read_text()
    assert f"{EXP}.r03.lane_rmse_cm" in tex and f"{EXP}.r02.lane_rmse_cm" in tex
    assert "0 failure(s)" in run(ws, "tools/check.py").stdout


def test_status_and_compare(ws):
    dispatch(ws, "r01", "baseline", "baseline")
    dispatch(ws, "r02", "tuned", "tuned", baseline="r01")
    assert "r02 (tuned)" in run(ws, "tools/status.py", "--write").stdout
    assert (ws / "experiments" / "INDEX.md").exists()
    table = run(ws, "tools/compare.py", "--experiment", EXP).stdout
    assert "| r01 | baseline" in table and "| r02 | tuned" in table
