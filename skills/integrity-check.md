---
name: integrity-check
version: 0.2
note: "rewritten from concepts; no adapted text"
---

# integrity-check

Tests whether the facts under a claim are real: emitted by a recorded run, recomputable from the
frozen file at the recorded code commit, and described in Methods as they were executed. claim-audit
assumes the facts are true and asks whether a sentence says more than they allow; this skill tests
the assumption. It runs between Analyze and Write, once facts are frozen and before claim rows
harden, and again at Review before Submit. Head runs it; every recomputation is a run dispatched
through the experiment agent and recorded like any other. Modes run on triggers, never as a ritual.

The seven failure modes are those catalogued in
Lu, C. et al. (2026). Towards end-to-end automation of AI research. Nature 651:914-919
The three-verdict shape of the protocol follows Academic Research Skills (ARS) by Cheng-I Wu
(see ATTRIBUTION.md); the text here is written from the ideas alone.

## 1. When to invoke

- A claim row's tier is about to rise. claim-audit needs a verdict on every anchor before `strong`.
- Enthusiastic or unexpected-finding wording appears about a result anywhere: a draft, an
  Interpret report, `experiments/<id>/notes.md`, or the conversation. Hard trigger; mode 5.
- A new experiment's facts have frozen and none of them anchors a claim yet: modes 1 and 3.
- Before the first render of `manuscript/facts.tex` that Results prose will cite, and again
  before Submit: modes 1, 3, 5, and 6 over every entry in `manuscript/facts-map.yaml`.
- method-design is about to mark a method-trace §4 bullet or §5 parameter `mention`: mode 6.

Not this skill: wording (polish); claim versus evidence (claim-audit); whether a step belongs
in Methods (method-design); verifying references (the citation gate; flagged here only).

Hand-offs: claim-audit reads `checked_by` and raises no tier without a verdict from here;
new-evidence-integration takes its add, strengthen, and restructure paths only after a mode 5 CLEAR;
method-design cannot mark an element `mention` over a mode 6 FAIL; experiment-loop performs every
recomputation as a recorded run; shadow-reviewer and cold-review attack the narrative from the
reader's side while this skill checks the evidence from the source side; mode 7 flags go to story-design.

## 2. Inputs to read

- `boards/evidence.csv` rows in scope: `claim_id`, `fact_ids`, `status`, `checked_by`.
- The frozen facts those rows cite, `reality/facts/<exp>/<run>.facts.json`, with `reality/index.csv`
  for the hash and `reality/errata.md` for supersession.
- Each fact's run record, `experiments/<id>/runs/<run>/run.yaml` (`command`, `config`, `code_commit`,
  `inputs`, `exit_status`, `facts_sha256`); `experiment.yaml` for `emits[]`; the Interpret `decisions/ADR-*.md`.
- `codespaces/<name>.yaml`; `identity/method-trace.md` §4 and §5; `identity/claim-map.md` §1 rows in scope.
- `manuscript/facts-map.yaml` and the sections in scope, read for two purposes only: the surprise-language
  sweep and the Methods-versus-run comparison of mode 6. Optional: `experiments/<id>/notes.md`; code-space logs.

## 3. Excluded inputs

- `manuscript/` as a baseline (confirming a fact from the sentence that cites it is circular); `tmp/`; chat backups.
- Unfrozen outputs: a CSV, plot, or notebook that did not pass freeze; `experiments/*/notes.md` as a baseline.

## 4. Protocol steps

### 4.1 Declare scope

One line: what this session verifies and why (a tier rise; a surprise in the latest Interpret report;
the pre-Submit sweep), then the fact ids in scope, from `fact_ids` or the `facts-map.yaml` keys, pruned by 4.7.

### 4.2 The seven failure modes

Each mode names the stage where its defect is born and the questions that detect it; every question
is answered against a frozen file, a run record, or an ADR, never from memory.

**Mode 1: a code defect that survived its author's review** (born in Build, surfaces in Analyze). The
analysis code is wrong in a way that still yields a believable value, and the value reaches the paper
because the headline metric looked fine. Does the run record exist with `exit_status: 0`, a `code_commit`,
input hashes, and a `facts_sha256` equal to the hash in `reality/index.csv` (no record: INSUFFICIENT)?
Across runs (`tools/compare.py`), does the value move when the variant moves? Recompute from the frozen
facts file and the run record in a code space checked out at the recorded `code_commit`; a code space
that cannot be checked out at that commit gives INSUFFICIENT, not CLEAR.

**Mode 2: a citation that does not exist or does not say what it is cited for** (born in Write).
Verified elsewhere: a reference enters the citation map only after its publisher record and full text
were checked. A cited work without that record is a MINOR finding routed to the gate; no sweep here.

**Mode 3: a result that no run produced** (born in Analyze or Write). An aggregate computed differently
from how the sentence describes it, a value from a run that failed, or a number that fits the story.
Does every quantitative sentence resolve through `facts-map.yaml` to a fact id that is frozen and not
superseded, whose `definition`, `n`, and `unit` say what the sentence says? Does every table cell and
figure annotation trace to a fact id, or to a `table` fact in the same frozen folder? Is every aggregate
across runs or units recomputed from the frozen per-run facts, as in mode 1?

**Mode 4: a genuine score reached by the wrong route** (born in Design or Build). The number is real,
but a fitted component arrived at it through a cue other than the one the claim names. Applies only
when something with free parameters was trained, tuned, or fitted; a fixed pretrained component records
`n/a` with that reason. Where it applies: does `experiment.yaml` list a control condition with the
suspected cue absent or decoupled, and does a frozen fact from it exist? If not, the remedy is a new experiment.

**Mode 5: a defect retold as a discovery** (born in Analyze, sealed in Interpret and Write). The
highest-risk mode: mode 1 plus a narrative. The pipeline emits an unexpected pattern, the writing stage
presents it as a finding, and the paper reads better than the correct version would. For every surprise
in scope: was the pattern reported to the human as a question in an Interpret report, and did an ADR
accept it as a finding, before any sentence stated it as one (a prose-only finding is a FAIL)? Does a
second frozen run, new run id at the same `code_commit`, carry the same pattern (until it does, at best
INSUFFICIENT)? Has the stage directly upstream of the pattern passed mode 1 on the same facts?

**Mode 6: Methods that describe what should have run rather than what ran** (born in Write). Methods
text drifts from the run record toward a tidy account of the procedure; only elements already marked
`mention` apply. Is every method-trace §5 parameter a fact id whose value equals the run record's
`config` and the code space's configuration at `code_commit`? Does every operation named in Methods map
to a code path at `code_commit` and execute in the runs whose facts the paper cites? A described operation
that no cited run executed is a FAIL; one every run executed that Methods omits is a silent-versus-mention
question for method-design, flagged only.

**Mode 7: an early frame that later stages cannot revisit** (born in Idea or Design). A question,
method, or parameter direction fixed early, so that the paper answers the wrong question well. Prevented
upstream by design-review and the story-spine's anti-pivot guardrails. Does the ADR chain from Idea and
Design record alternatives rejected for this frame, and did any Interpret ADR reopen it when the facts
pointed elsewhere? A frame with no recorded alternative, or prose that looks back on a choice as a
regret, is a NOTE for a story-design session; the human decides, an ADR records.

### 4.3 Choose the modes

| trigger | modes |
|---------|-------|
| tier rise on a claim row | 1 and 3 on the row's fact ids |
| surprise language | 5 always, plus 1 and 3 on the facts behind the sentence |
| new experiment frozen | 1 and 3 on the new facts |
| first render of facts.tex; pre-Submit | 1, 3, 5, 6 over facts-map; 2 and 7 as flags |
| method element marked `mention` | 6 on that element |

Modes 2, 4, and 7 are flag-or-`n/a` by default; sweeping every fact with them is an anti-pattern.

### 4.4 Verdicts

| verdict | meaning | effect |
|---------|---------|--------|
| CLEAR | a concrete comparison shows the mode does not apply, or the recomputation matched | eligible for `checked_by` |
| INSUFFICIENT | undecidable: no run record, no log, no checkout at the commit, no replication | `checked_by` stays empty; the tier cannot rise; a `boards/human-owed.csv` item names what is missing |
| FAIL | a detection question has a concerning answer, or the recomputation did not match | BLOCKER finding; tier rise, `mention` mark, and new-evidence paths blocked |

One verdict per fact id per mode. INSUFFICIENT is a block, not a pass. A recomputation that nearly
matches is a FAIL with the delta recorded; the tolerance is the display precision in `facts-map.yaml`.
A FAIL in mode 1 or 3 is closed only by a new run whose facts carry `supersedes` and an `errata.md`
line, after which `facts-map.yaml` repoints and the manuscript renders again; a mode 6 FAIL by
correcting the prose to what ran or repeating the run as described; a mode 7 flag by a story-design ADR.

### 4.5 Surprise-language sweep (every session)

Whatever the trigger, search the scope for enthusiastic or unexpected-finding wording: adverbs of
surprise or delight, phrases that set a result against expectation, sentences that present a pattern as
a discovery. Scope: the sections in the contract, `experiments/<id>/notes.md`, the latest Interpret
report, and the conversation. Each hit goes through the mode 5 questions; an unanswered question is a
FAIL for the facts behind that sentence. Record the hit count even when it is zero (4.6).

### 4.6 Write findings and update the boards

Per fact and mode, in the conversation first, five labelled lines: the mode, the fact id
(`EXP-001.r03.name`), the verdict, the basis (one sentence naming the file or record compared), and the
next action (what the human or experiment agent must supply or re-run). Then `boards/findings.csv` with
`source: integrity-check`. Severity follows what the finding blocks: a FAIL on a fact that a manuscript
number or a claim tier depends on is BLOCKER; INSUFFICIENT is MAJOR and also a `boards/human-owed.csv`
item; a flag handed to another skill takes that skill's queue severity (a reference without a
verification record MINOR; a frame question NOTE). One NOTE row per session records the sweep
(`summary: "surprise sweep: <n> hits over <scope>"`, status `resolved` when n is zero). Cells stay under
160 characters; the basis lives in the conversation or an ADR.

`boards/evidence.csv` `checked_by` is written by this skill only: `integrity-check <YYYY-MM-DD>` when
every fact in the row's `fact_ids` is CLEAR for every mode the trigger required; empty on INSUFFICIENT
or FAIL, and until a check has happened; `n/a` under the scope rule (4.7), with the reason in a finding.
Only a passing check or a recorded recomputation writes the cell. Name the downstream sessions in
conversation (§1 hand-offs), then run `python3 tools/check.py`.

### 4.7 Scope rule against over-checking

`checked_by` means something only for a row whose facts a manuscript number or a claim tier depends on.
Mark `n/a`, and schedule no mode, for an illustrative figure no sentence draws a number from, a
descriptor shown in a panel but used in no numeric sentence, and evidence cut from the manuscript. The
test: if this row's value changed, which manuscript sentence would change? No answer means `n/a`. The
count of empty `checked_by` cells is not a quality metric, and an all-green board is not one either;
checking everything costs tokens, dilutes the one FAIL that matters, and volunteers facts the paper does not need.

## 5. Anti-patterns

- **Ceremonial sweep.** All seven modes in every session, "all CLEAR". Triggers only (§1).
- **Modes 4 and 7 everywhere.** Shortcut checks where nothing was fitted; frame checks where ADRs trace the frame.
- **Surprise word waved through.** An adverb of surprise in a draft and no mode 5 that session.
- **INSUFFICIENT read as CLEAR.** An empty `checked_by` treated as consent. The empty cell is the objection.
- **Improvised baseline.** A notes file, a plot, or a code-space CSV standing in for a frozen fact. INSUFFICIENT.
- **Recomputing at the current head.** The latest commit instead of the recorded one proves nothing either way.
- **Self-certification.** `checked_by` written because the number looked right or matched memory.
- **Checking to turn the board green.** A row nobody can tie to a sentence is `n/a`, not pending.

## 6. Closing condition

- Every fact id declared in 4.1 has a verdict line in the conversation and, for INSUFFICIENT or FAIL, a
  `boards/findings.csv` row with `source: integrity-check` and a next action.
- `boards/evidence.csv` `checked_by` is updated for every row in scope: a dated value, empty with a
  finding, or `n/a` with a reason.
- One `boards/findings.csv` NOTE row records the surprise-sweep hit count, even when zero.
- Every FAIL is an open BLOCKER row until a superseding freeze, a correction, or an ADR resolves it;
  every INSUFFICIENT has a `boards/human-owed.csv` item.
- `python3 tools/check.py` passes (freeze, anchors, boards). No claim-map tier rose; this skill verifies, claim-audit raises.
