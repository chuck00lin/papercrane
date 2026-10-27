"""Shared fixture: a scratch copy of the workspace with every demo artifact reset."""
import shutil, subprocess
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
EXP = "EXP-000-example"


def reset_demo_state(ws: Path):
    shutil.rmtree(ws / "experiments" / EXP / "runs", ignore_errors=True)
    shutil.rmtree(ws / "reality" / "facts" / EXP, ignore_errors=True)
    shutil.rmtree(ws / "examples" / "toy-pipeline" / "runs", ignore_errors=True)
    shutil.rmtree(ws / "bus" / "queue", ignore_errors=True); (ws / "bus" / "queue").mkdir(parents=True)
    (ws / "bus" / "events.ndjson").write_text("")
    (ws / "reality" / "index.csv").write_text("fact_file,sha256,experiment,run,frozen_at,frozen_by\n")
    for f in ("manuscript/facts.tex", "experiments/INDEX.md", "decisions/ADR-0001-carry-r02-vs-r01.md", "manuscript/main.pdf"):
        (ws / f).unlink(missing_ok=True)
    ey = ws / "experiments" / EXP / "experiment.yaml"
    ey.write_text(ey.read_text().replace("status: running", "status: designed"))


@pytest.fixture
def ws(tmp_path):
    dst = tmp_path / "ws"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__", ".pytest_cache", "frames", "*.gif"))
    reset_demo_state(dst)
    subprocess.run(["git", "init", "-q"], cwd=dst, check=True)
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "add", "-A"], cwd=dst, check=True)
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "-m", "init"], cwd=dst, check=True)
    return dst
