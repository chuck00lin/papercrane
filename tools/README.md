# tools/

| Script | Role | Status |
|--------|------|--------|
| `check.py` | the checker; see `docs/design.md` §7 for the catalog | v0: schema, design, freeze, anchors, boards, numerals, terminology, cross-ref |
| `render-facts.py` | compile `manuscript/facts-map.yaml` + `reality/facts/` into `manuscript/facts.tex` | v0 working |
| `freeze.py` | validate, hash, copy, index a code space's `facts.json`; errata on `supersedes`; updates the run record | v0 working |
| `dispatch.py` | create a run record, hash inputs, run the code space synchronously or enqueue a task on the bus | v0 working |
| `bus.py` | file-queue bus: send / poll / ack / tail / wait | v0 working |
| `status.py` | experiment registry table; `--write` regenerates `experiments/INDEX.md` | v0 working |
| `compare.py` | leaderboard of fact values across runs (`--experiment`) or across experiments (`--fact`) | v0 working |
| `mount-skills.py` | Claude Code wrappers under `.claude/skills/` for every protocol in `skills/` | v0 working |
| `impact.py` | what a newly frozen run changes in the paper: facts-map keys, manuscript lines, figures, claims; `--apply` remaps facts-map | v0 working |

`check.py` depends on `pyyaml` and `jsonschema`. Exit status 1 on any failure.

`make check`, `make render`, `make freeze FACTS=... [RUN=...] [ERRATA=...]` wrap the three.

`tools/dev/overlap_check.py <corpus>` reports word n-grams shared with another corpus; the release
gate is zero against any source the skills credit.
