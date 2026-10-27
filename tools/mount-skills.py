#!/usr/bin/env python3
"""Generate Claude Code skill wrappers: .claude/skills/<name>/SKILL.md -> skills/<name>.md.
The wrapper carries the frontmatter Claude Code needs and tells the agent to follow the
protocol file; the protocol itself stays in skills/."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / ".claude" / "skills"
n = 0
for p in sorted((ROOT / "skills").glob("*.md")):
    if p.name == "README.md":
        continue
    text = p.read_text()
    m = re.search(r"^# .+?\n\n(.+?)\n", text, re.M | re.S)
    desc = (m.group(1).strip().replace("\n", " ") if m else p.stem)[:200]
    d = OUT / p.stem; d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(f"---\nname: {p.stem}\ndescription: {desc}\n---\n\nRead `skills/{p.name}` in this workspace and follow it exactly: open with the 8-line session\ncontract (docs/session-contract.md), read only its listed inputs, and stop at its closing\ncondition. Do not paraphrase the protocol from memory.\n")
    n += 1
print(f"[mount-skills] wrote {n} wrapper(s) under .claude/skills/")
