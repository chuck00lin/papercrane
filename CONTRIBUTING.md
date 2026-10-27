# Contributing

Thank you. Three rules keep this repository what it is.

1. **Concepts only.** A skill, a doc, or an example carries ideas in original wording. Nothing
   is adapted from another source, and nothing from anyone's unpublished paper goes in.
   `python3 tools/dev/overlap_check.py <corpus>` must report zero shared 8-grams against
   any source you credit in `ATTRIBUTION.md`.
2. **Checks over ceremony.** A new rule arrives with the check that enforces it, or with a
   sentence explaining why it cannot be checked. `python3 tools/check.py` and
   `python3 -m pytest -q` stay green.
3. **Adapt, do not prescribe.** Taste lives in data files (`identity/terminology.csv`,
   `identity/style-words.csv`, `reviews/review-lenses.md`, `identity/venue-calibration.md`).
   A pull request that hard-codes one lab's taste into a skill will be asked to move it.

## Running things

```bash
python3 tools/check.py        # the workspace validates
python3 -m pytest -q          # the loop end to end on the toy pipeline
make demo && make pdf         # two runs, a render, a compiled PDF; make demo-clean resets
python3 tools/dev/draw_diagrams.py   # regenerate the README diagrams after editing geometry
```

## Skills

Every skill has the six sections (when to invoke, inputs, excluded inputs, steps,
anti-patterns, closing condition) and a closing condition a second agent could verify.
Describe the protocol; put lists and examples in the data files.
