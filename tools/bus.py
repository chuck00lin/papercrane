#!/usr/bin/env python3
"""File-queue bus (docs/design.md §8). Importable and a CLI.

  python3 tools/bus.py send --to plot --task T-001 --from head [--kind run] [--payload '{"k":"v"}' | --payload-file f.json]
  python3 tools/bus.py poll --agent plot
  python3 tools/bus.py ack  --agent plot --id <msg-id> [--result '{"ok":true}']
  python3 tools/bus.py tail [-n 20]
  python3 tools/bus.py wait --to head --task T-001-reply [--timeout 3600]
"""
import argparse, json, os, shutil, sys, time, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUS = ROOT / "bus"
LOG = BUS / "events.ndjson"


def _now():
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def _event(**ev):
    ev = {"ts": _now(), **ev}
    with open(LOG, "a") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")
    return ev


def send(to, task, payload=None, frm="head", kind="run", reply_to=None):
    msg = {"id": uuid.uuid4().hex[:12], "ts": _now(), "from": frm, "to": to, "task": task,
           "kind": kind, "payload": payload or {}, "reply_to": reply_to}
    q = BUS / "queue" / to
    q.mkdir(parents=True, exist_ok=True)
    (q / f"{msg['id']}.json").write_text(json.dumps(msg, indent=2, ensure_ascii=False))
    _event(type="send", id=msg["id"], **{"from": frm, "to": to, "task": task, "kind": kind})
    return msg["id"]


def poll(agent):
    q = BUS / "queue" / agent
    return [json.load(open(p)) for p in sorted(q.glob("*.json"))] if q.exists() else []


def ack(agent, msg_id, result=None):
    q = BUS / "queue" / agent
    src = q / f"{msg_id}.json"
    if not src.exists():
        raise SystemExit(f"[bus] no pending message {msg_id} for {agent}")
    msg = json.load(open(src))
    msg["result"] = result
    msg["acked"] = _now()
    done = q / "done"
    done.mkdir(exist_ok=True)
    (done / src.name).write_text(json.dumps(msg, indent=2, ensure_ascii=False))
    src.unlink()
    _event(type="ack", id=msg_id, **{"from": agent, "to": msg["from"], "task": msg["task"]})
    return msg


def tail(n=20):
    lines = LOG.read_text().splitlines() if LOG.exists() else []
    return [json.loads(l) for l in lines[-n:] if l.strip()]


def wait(to, task, timeout=3600, poll_s=5):
    """Block until an event addressed to `to` with this task appears (ack or send)."""
    deadline = time.time() + timeout
    seen = 0
    while time.time() < deadline:
        lines = LOG.read_text().splitlines() if LOG.exists() else []
        for l in lines[seen:]:
            ev = json.loads(l)
            if ev.get("to") == to and ev.get("task") == task:
                return ev
        seen = len(lines)
        time.sleep(poll_s)
    return None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("send"); s.add_argument("--to", required=True); s.add_argument("--task", required=True)
    s.add_argument("--from", dest="frm", default="head"); s.add_argument("--kind", default="run")
    s.add_argument("--payload"); s.add_argument("--payload-file"); s.add_argument("--reply-to")
    p = sub.add_parser("poll"); p.add_argument("--agent", required=True)
    a = sub.add_parser("ack"); a.add_argument("--agent", required=True); a.add_argument("--id", required=True); a.add_argument("--result")
    t = sub.add_parser("tail"); t.add_argument("-n", type=int, default=20)
    w = sub.add_parser("wait"); w.add_argument("--to", required=True); w.add_argument("--task", required=True); w.add_argument("--timeout", type=int, default=3600)
    args = ap.parse_args()
    if args.cmd == "send":
        payload = json.loads(args.payload) if args.payload else (json.load(open(args.payload_file)) if args.payload_file else {})
        print(send(args.to, args.task, payload, args.frm, args.kind, args.reply_to))
    elif args.cmd == "poll":
        for m in poll(args.agent):
            print(json.dumps(m, ensure_ascii=False))
    elif args.cmd == "ack":
        ack(args.agent, args.id, json.loads(args.result) if args.result else None); print("acked")
    elif args.cmd == "tail":
        for ev in tail(args.n):
            print(json.dumps(ev, ensure_ascii=False))
    elif args.cmd == "wait":
        ev = wait(args.to, args.task, args.timeout)
        print(json.dumps(ev) if ev else "timeout"); sys.exit(0 if ev else 2)


if __name__ == "__main__":
    main()
