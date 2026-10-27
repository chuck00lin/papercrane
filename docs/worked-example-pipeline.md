# Worked example: attaching a real pipeline as the first code space

The first-generation project's pipeline repository was attached to a trial workspace to test
the adapter contract on real data. This page records what it took and what the contract
lacked. No result values are reproduced here; the trial workspace is private.

## What the code space had to add

Two files and one Makefile target, about 120 lines in total, no change to any pipeline stage:

```
<pipeline repo>/
├── Makefile                 make run EXP=<experiment> RUN=<run> CFG=<config> [ARGS=...]
└── craft/
    ├── README.md            the contract, stated from the code space's side
    └── export_facts.py      reads outputs already on disk, writes craft/runs/<run>/facts.json
```

The exporter reuses the repo's own scanning helper for per-plant summary files, so the
analysis logic is not duplicated. It records the repo's git commit and a sha256 for each of
the input files it read, then emits seven facts: three counts describing the cohort it saw,
three counts and one metric for the quantity under study, and one `table` fact pointing at a
per-plant-day CSV written next to `facts.json`.

## The adapter in the workspace

```yaml
name: my-pipeline
path: /home/<user>/github/my-pipeline
kind: pipeline
entry:
  command: "make run EXP={experiment} RUN={run_id} CFG={config} ARGS=\"--start <first day> --end <last day>\""
  cwd: .
  env: system python3 (pyyaml)
emits:
  facts: "craft/runs/{run_id}/facts.json"
agent:
  transport: none          # no resident agent; dispatch runs it synchronously
provenance:
  code_commit: "git rev-parse HEAD"
  inputs: []               # the exporter hashes its own inputs; dispatch does not re-walk the data disk
preapproved_commands: ["make run *"]
```

`{config}` selects which output branch the exporter reads, so one design contract and one
code space serve several variants.

## What the loop looked like

```
tools/dispatch.py --experiment EXP-001-... --run r01 --config <branch A> --variant a
tools/freeze.py   <repo>/craft/runs/r01/facts.json --run experiments/EXP-001-.../runs/r01/run.yaml
tools/dispatch.py ... --run r02 --config <branch B> --variant b --baseline r01 --change "..."
tools/freeze.py   ...
tools/status.py --write          # registry: 1 experiment, 2 runs, 2 frozen
tools/compare.py --experiment EXP-001-...   # leaderboard: one row per variant
tools/render-facts.py            # three \fact{} macros for one Results sentence
tools/check.py                   # 0 failures
```

Dispatch to freeze took seconds per variant because the exporter reads summaries, not point
clouds. The exported quantity matched the value the first-generation project had reached by
hand after a month of reconciliation, for both branches, which is the point: the number now
has a run record, a commit, and a hash for every input file behind it instead of a chat
transcript.

## What the contract lacked (fixed in the same session)

1. **Code-space names starting with a digit were rejected** by the schema pattern. Real repos
   are named like that (the pipeline attached here is one). Pattern widened.
2. **Table facts had no freeze path.** A `kind: table` fact pointed at a CSV beside
   `facts.json`; freeze copied only the JSON. Freeze now copies and indexes the referenced
   file and rewrites the fact's value to the frozen name; the checker verifies both.
3. **`impact.py` conflated variants.** It treated every earlier run with the same fact name
   as replaced by the new run, so a run of variant B was reported as replacing variant A's
   numbers in the manuscript. Rule now: a run replaces earlier runs of the same experiment
   *and the same variant*; a different variant is a comparison and shows up only on the
   leaderboard.
4. **Input hashing at dispatch does not scale to a data disk.** The adapter's
   `provenance.inputs` globs are fine for a few config files; for hundreds of per-plant
   outputs the exporter must hash what it actually read and put it in the facts provenance.
   The contract now says so.

## What was not tested

A code space with a resident agent (bus transport) on real work; a figure registered against
a frozen table fact; a claim-map row promoted from these facts through claim-audit.
