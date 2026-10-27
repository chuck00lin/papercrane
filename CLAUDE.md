# CLAUDE.md — agent invariants for this workspace

This file is short on purpose. Architecture lives in `docs/design.md`; protocols live in
`skills/`. Read `identity/` (three files) at the start of every substantive session.

## Roles

- **Human**: leads the three human-led stages, Idea, Design, and Interpret. Owns
  `identity/story-spine.md`, the claim boundary in `identity/claim-map.md`, the intent of every
  `experiments/<id>/experiment.yaml`, and every `decisions/ADR-*.md`. In a human-led stage the
  agent proposes in conversation; nothing is written to `identity/` or `decisions/` until the
  human has decided, and the ADR records it.
- **head** (paper agent): leads Write and Review. Edits `identity/` only under a declared
  contract, drafts and renders `manuscript/`, orchestrates review, keeps `boards/` current.
- **experiment** (experiment-manager agent): leads Build, Run, and Analyze. Owns
  `experiments/` and `reality/`. Dispatches runs into code spaces, freezes facts, renders
  plots from frozen facts, reports surprises as questions. Never edits `identity/` or
  `manuscript/`.
- **code-space agents**: live in the researcher's external repos. Receive run requests, emit
  facts, reply through the bus. Never write into this workspace except through the
  freeze step.

## Invariants (a session that breaks one is not finished)

- **I1 Claim ≤ evidence.** Every claim row cites fact ids whose status is `frozen`.
  Wording strength follows the evidence tier. Disallowed claims and limitations are never
  weakened or deleted.
- **I2 Reality is immutable.** Facts enter `reality/facts/` as hash-pinned files produced by a
  recorded run. Corrections are new facts plus an `reality/errata.md` entry. No file in
  `reality/facts/` is edited after freeze.
- **I3 No hand-typed numbers.** Manuscript numerals come from `manuscript/facts.tex`
  (generated) or the allowlist in `manuscript/facts-map.yaml`. `tools/check.py` enforces it.
- **I4 Design before run.** A run is dispatched only for an experiment whose
  `experiment.yaml` validates and whose targeted claims are not in the disallowed list.
- **I5 Promotion is rewrite.** Moving information up a layer (notes to facts, facts to claims,
  claims to prose) rewrites it into the target schema. No paragraph is pasted upward.
- **I6 Decisions leave a trace.** A directional decision made in conversation is recorded as
  an ADR in the same session or it does not exist.
- **I7 Excluded inputs are declared.** The session contract lists what will not be read.
  Chat transcripts and scratch folders are excluded by default.
- **I8 Checks replace ceremony.** Consistency between identity files, boards, and manuscript
  is verified by `tools/check.py`, not by a multi-step manual ritual. If a check cannot
  express a rule, the rule is a candidate for deletion.

## Session contract

Every substantive session opens with the 8-line contract in `docs/session-contract.md`.
Sessions without it do not modify `identity/`, `reality/`, `boards/`, `decisions/`, or
`manuscript/`.

## Never

- Fabricate a number, a citation, or a run that did not happen.
- Mark an evidence row verified without a passing check or a recorded recomputation.
- Add a sentence to the manuscript that supports no claim (disclosure economy).
- Park content in "supplementary" to avoid a main-text-or-cut decision.
- Read `tmp/` or any chat backup unless the human names the file.
- Write a story-spine section, a design contract's intent, or an interpretation on the
  human's behalf. Propose it; wait for the decision.

## Terminology

Project-specific terminology rules live in `identity/terminology.csv` and are enforced by
`tools/check.py` on manuscript text and figure labels.
