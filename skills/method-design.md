---
name: method-design
version: 0.1
ported_from: "Paper3 skills/method-design.md v1.1"
---

# method-design

Add, change, or remove a method bullet, a parameter, or a method figure without decoration,
overfit, or silent drift between what the code does and what the paper says. Stage:
**Build** (the pipeline changes) and **Write** (deciding what the Methods section says).
Owned by head under contract; the human decides when the pipeline backbone or a claim
changes.

## 1. When to invoke

- Any add / change / remove of a row in `identity/method-trace.md` §4 (method-bullet
  trace) or §5 (parameter register), or of a stage in §1 (pipeline backbone).
- A code space changed what a stage does, or how, during Build.
- A shadow or cold review finding asks for more (or less) method detail.
- A method figure is planned, re-rendered, or re-captioned.
- Any judgement of the form "does this detail belong in the paper?"

Not this skill: result sentences and tiers (`claim-audit`), narrative (`story-design`),
wording (`polish`), the first design of an experiment (`design-review`). Session contract:
`Stage: build`, `Identity touch: method-trace`.

## 2. Inputs to read

Authoritative:
- `identity/method-trace.md`, all sections.
- `identity/claim-map.md` §1 to §3: which claim each bullet serves; what may not be claimed.
- `identity/README.md` tier table.
- The `codespaces/<name>.yaml` and `experiments/<id>/experiment.yaml` of the stage in
  question: what the pipeline actually runs and which facts it `emits`.
- `reality/index.csv` and the frozen facts a parameter value will reference.
- The active venue section of the calibration notes from `skills/venue-calibration.md`,
  if it exists. It is the only source for question 5 below.
- `manuscript/labels.yaml` and `manuscript/figures.yaml`
  when a method figure is in scope.

Task-scoped, optional: `identity/story-spine.md` §3 (positioning relative to prior work)
and §5 (which result section carries which node).

## 3. Excluded inputs

- `manuscript/sections/*.tex` Methods prose. Existing wording frames the decision; the
  trace is upstream of it.
- Code-space research notes, raw run outputs, and `experiments/<id>/notes.md` of any
  experiment whose facts are not frozen. These are where overfit comes from.
- `tmp/`, chat backups, and any file the human has not named.

## 4. Protocol steps

1. **Trigger note.** One line: why now, who asked, which claim or result is involved. It
   becomes the `Target` line of the session contract.

2. **Five-question filter.** Run every candidate bullet through all five before touching
   the trace. Question 5 is the venue override channel; it relaxes only the defaults of
   questions 1 and 3.
   - **Q1 Consumed?** Does a result section consume this (method-trace §4 "result
     consumed" column, §3 results narrative)? No: default silent.
   - **Q2 Already covered?** Does a prior paper of the group, or a cited external method,
     already describe it? Yes: cite at first mention and stay silent, unless this paper
     modifies it, in which case only the modification is described.
   - **Q3 Reproducible without it?** If the bullet were removed, could a reader reproduce
     the consumed result? Yes: decoration, removable. No: it must be written, specifically
     enough to reproduce; Q5 cannot touch this answer.
   - **Q4 Overfit?** Is it a fix for an observation from a single run or experiment whose
     facts are not frozen, or whose claim is not in claim-map? Yes: it stays in
     `experiments/<id>/notes.md` until `new-evidence-integration` has placed the finding.
     Nothing overrides Q4.
   - **Q5 Venue norm?** Does the active venue's calibration list this detail as expected
     by that venue's readers (an entry id)? Yes: write it even when Q1 is no or Q3 is yes,
     and put the entry id in the row's justification. No entry: treat as no.

   | Q1 | Q2 | Q3 | Q4 | Q5 | outcome |
   |----|----|----|----|----|---------|
   | yes | any | any | no | any | mention |
   | no | any | any | no | yes | mention; justification cites the calibration entry |
   | no | any | any | no | no | silent |
   | any | yes | any | no | no | cite and stay silent, unless this paper's modification |
   | any | yes | any | no | yes | mention the modification only; cite the base |
   | any | any | no | no | any | mention, regardless of the other answers |
   | any | any | any | yes | any | not in the trace; overfit; no override |

   Q5 never crosses: claim-map §2 disallowed claims; the qualifier on derived or relative
   descriptors; a tier above what `boards/evidence.csv` supports; a frozen fact; Q4.

3. **Anchor the bullet.** A §4 row needs all five columns: bullet; `mention` or `silent`;
   claim served (`C<n>`, or `none` only with a Q5 justification); result consumed (a
   results subsection id, or `none`); fact ids. A row that cannot fill them does not enter
   the trace.

4. **Prior-work alignment.** For every changed stage ask: is the difference from the prior
   paper's same-named step stated accurately? Is an established component being
   re-described as a contribution? If the code changed during Build, do facts produced by
   the old version still anchor claims? Then either the experiment re-runs under the new
   version (new run id, new facts, errata line) or the results are partitioned by version
   and an ADR says so. A silent algorithm change under unchanged text is the failure this
   step exists to catch.

5. **Parameter register.** Every value in §5 is a fact id (`EXP-001.r03.name`). If the
   value is a config constant no run has emitted, add it to the experiment's `emits` and
   have the code space emit it; do not type it. The `anchors` check fails on a literal.

6. **Method figures.** When a figure is in scope, apply the grammar in §4.1, write the
   figure's entry in `manuscript/figures.yaml`, put every label in `manuscript/labels.yaml`,
   and let `manuscript/figures.yaml` record the facts hash at render.

7. **Write back.** Edit §1, §2, §4, §5 of method-trace as needed; update `last_updated`.
   In `boards/draft.csv`, every section whose `depends_on` includes an affected claim goes
   back to `state: drafted`, `polish_passed: no`. If the change alters what a claim can
   say, do not edit the tier: write a `boards/findings.csv` row (source `method-design`,
   target the claim id, status `open`) for a claim-audit session. A backbone stage added,
   removed, or re-ordered, or a partition by version, is a human decision: ADR first.

8. **Check.** `python3 tools/check.py`: anchors, cross-ref, terminology (labels included),
   figures.

### 4.1 Method figure grammar

Derived from exemplar method figures inspected in the first generation's venue corpus.
Re-derive for a new venue through `skills/venue-calibration.md`, recording which papers
and which pages were inspected.

- **Operational, not promotional.** Every block is a data object, a process, or an output,
  and the reader can trace raw observation to analyzable record. The pattern is
  `input -> preprocessing -> extraction -> records -> analysis-ready output`, never
  `contribution -> capability label -> validation rhetoric -> impact`.
- **Declare the grammar or make it obvious.** Boxes are data objects or outputs; arrows
  are data flow only; processes sit on arrows or in small labeled blocks; dashed outlines
  mark scope notes; color groups stages and never ranks contributions.
- **Bands are fine if the eye scans acquisition to output.** Band headings are stage
  names. Author-internal logic ("credibility engine", "contribution axis") never appears.
- **Captions carry the boundaries.** Short labels in the figure; in the caption: what is
  not automated, which descriptors are relative, that any selection step used no
  reference labels, and that validation is reported in Results. Each boundary once, at
  its natural home.
- **Validation is not a method node.** At most a dashed handoff "validated in Results §x".
- **One overview figure; the rest are scoped mechanisms.** One main flow direction per
  figure; one noun phrase plus an optional short process note per node.
- **Acquisition context is a compact, muted figure** and the first to compress when space
  is short.
- **Vector first, legible at print size** (about 7.5 to 8 pt minimum). A clean flowchart
  beats a rich collage that leaves the data flow ambiguous.
- **Labels are data.** Every label comes from `manuscript/labels.yaml`, where the
  terminology check reads it. Words that overstate automation, absoluteness, or cadence
  belong in `identity/terminology.csv` as forbidden variants so the check, not an eye,
  catches them before the figure is wired into the manuscript.

### 4.2 Citing in the Methods

A cited method is cited at its first mention in the backbone and not re-described. This
paper's modification is described; the base is a citation. How much of a cited method the
venue expects restated comes from the calibration corpus, never from an impression of the
venue. A Q2 "cite and stay silent" row still names the citation key in its bullet text so
the trace, not the prose, is where the reference is anchored.

## 5. Anti-patterns

- **Overfit on one run.** "While processing experiment E we hit case X; the fix is Y; add
  Y to the method." If the earlier experiments did not need Y, Y is not the method yet. It
  waits in notes until the finding is integrated.
- **Decoration writing.** A paragraph that makes the section look complete and that no
  result consumes. Reviewers ask why it is there, and every sentence is attack surface.
- **Contribution stealing.** Re-describing a component the group's prior paper
  established as if it were new. Cite it; describe only the delta.
- **Vague bullets.** "We apply quality control." "A robust algorithm is used." Vague and
  important is a reviewer red flag. Specific enough to reproduce, or deleted.
- **Over-writing.** Every small step a paragraph. Each bullet maps to a consumed result or
  a calibration entry; the rest is cut.
- **Silent algorithm update.** The code changed and the text did not; or the text changed
  and the old facts still anchor the claims. Re-run or partition, with an ADR.
- **Typing a parameter.** "It is only a config value." It is a literal in §5 and a check
  failure. Have the code space emit it.
- **The figure as a pitch.** Contribution words, capability labels, or validation numbers
  inside the schematic.
- **Labels typed in a plot script.** They escape the terminology check and drift from the
  prose.
- **Calibration as a license.** Using a venue entry to argue for a detail that crosses a
  claim boundary or Q4. Calibration widens the option space only.

## 6. Closing condition

Every touched row of `identity/method-trace.md` §4 has all five columns filled; §5
contains no literal; `python3 tools/check.py` passes (anchors, cross-ref, terminology,
figures); `boards/draft.csv` rows depending on affected claims are reset; any tier
consequence is an open `boards/findings.csv` row, not a claim-map edit; any backbone
change or version partition has an ADR dated this session; any method figure in scope has
its labels in `manuscript/labels.yaml` and a matching hash in `manuscript/figures.yaml`.
