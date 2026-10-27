"""The simulated three-role session runs end to end in a scratch copy (bus transport, ADR, freeze)."""
import json, subprocess, sys


def test_session_runs(ws):
    r = subprocess.run([sys.executable, "examples/session/run_session.py"], cwd=ws, capture_output=True, text=True)
    assert r.returncode == 0, r.stdout + r.stderr
    T = json.loads((ws / "docs/assets/session/transcript.json").read_text())
    assert sum(1 for e in T if "beat" in e) == 8
    assert not [e for e in T if e.get("kind") == "fail"]
    assert (ws / "decisions/ADR-0001-carry-r02-vs-r01.md").exists()
    assert (ws / "reality/facts/EXP-000-example/r02.facts.json").exists()
    events = (ws / "bus/events.ndjson").read_text().splitlines()
    assert sum(1 for l in events if '"type": "ack"' in l) == 3     # two code-space acks + one experiment ack
    chk = subprocess.run([sys.executable, "tools/check.py"], cwd=ws, capture_output=True, text=True)
    assert "0 failure(s)" in chk.stdout
