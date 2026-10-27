# reality/

What was observed. Frozen, hash-pinned, never edited.

```
reality/
├── index.csv          one line per frozen facts file: fact_file, sha256, experiment, run, frozen_at, frozen_by
├── errata.md          append-only: which fact id supersedes which, and why
└── facts/
    └── EXP-001-slug/
        └── r01.facts.json
```

## Freeze step (experiment agent)

1. Validate the code space's `facts.json` against `schemas/facts.schema.json`. Reject if any
   fact lacks provenance.
2. Compute sha256, copy to `facts/<exp>/<run>.facts.json`, append to `index.csv`.
3. Record `facts_file` and `facts_sha256` in the run record.

## Correction

Never edit a frozen file. Run again (new run id), freeze the new facts with `supersedes:` set
on each corrected fact, and append to `errata.md`:

```
- 2026-10-27  EXP-001.r03.height_r2 supersedes EXP-001.r01.height_r2 — reference sample
  re-extracted after the min-points threshold was restored to the pipeline default.
```

The checker fails if a facts file's hash differs from `index.csv`, or if a fact declares
`supersedes` without a matching errata line.

## What is not a fact

Interpretation ("the pipeline is reliable"), comparison claims, and evaluation of a protocol
are not facts. They belong in `identity/claim-map.md` once anchored to facts.
