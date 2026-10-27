---
name: shadow-reviewer
version: 0.2
note: "rewritten from concepts; no adapted text"
---

# shadow-reviewer

An adversarial read of drafted text by the head agent acting as a reviewer. The skill
produces findings; it never edits prose. Stage: Review (also the last step of Write for one
section). cold-review is the external counterpart and runs later, on the whole render.

The lens questions, trap catalog, and calibration questions it applies are project data in
`reviews/review-lenses.md`, filled in by the human; the skill says when to apply them.

Credit: the observation behind 4.9 (a reviewer agent that keeps conceding to an author agent
of the same model) comes from the devil's-advocate role in Academic Research Skills (ARS) by
Cheng-I Wu; the idea is used, no text is. See ATTRIBUTION.md.

## 1. When to invoke
- A section has been drafted or rewritten end to end; `boards/draft.csv` marks it `drafted`
  or `polished`.
- A Results or Discussion section changed after new-evidence-integration.
- The full render, once before cold-review and again before Submit.
- The human asks how a reviewer would read a passage.
- Re-review: an author-side rebuttal of earlier findings has arrived (4.9).

Not for a half-written section, for word choice (polish), for doubt about whether a fact is
real (integrity-check), or as a stand-in for the cold read. Contract
(`docs/session-contract.md`): `Stage: review`, `Identity touch: none`,
`Skill invoked: skills/shadow-reviewer.md`.

## 2. Inputs to read
- The text in scope, as rendered, with the scope fixed in the contract. The reviewer reads
  what a reviewer would receive.
- `identity/claim-map.md`: allowed claims and tiers, disallowed claims, limitations,
  boundary statements.
- `identity/method-trace.md`: what the method is, so "the method" in prose can be checked.
- `identity/story-spine.md`: reader, promise, anti-pivot guardrails.
- `identity/venue-calibration.md`: the active venue's reviewer expectations, risk-tolerance
  signals, weakness-handling tactics. If it keeps a per-concern catalog (one entry per
  question on the venue's reviewer form: concern, the paper's stance, the claim and fact
  ids behind it, the section that answers it), pass 2 walks it.
- `reviews/review-lenses.md`: lens questions, trap catalog, calibration questions. If it
  still holds only its illustrative entries, say so in the review header and propose
  project entries in conversation; the human owns the file.
- `boards/evidence.csv`: which fact ids are `frozen`, `partial`, `pending`.
- `boards/findings.csv`: open findings, to avoid duplicates and to scope a re-review.

## 3. Excluded inputs
- `experiments/*/notes.md`, `tmp/`, chat backups. The reviewer never sees the sandbox.
- Text outside the declared scope; a passage is not defended with pages the reviewer lacks.
- `reviews/reserve.md`: a fact held back under disclosure economy cannot excuse a gap on the page.
- On re-review: the earlier session's reasoning; only the review file and the rebuttal are read.

## 4. Protocol steps

### 4.1 Declare scope and roles
Open the review file with three lines: the section ids in scope; one sentence stating what
the text asks the reader to accept; the role for this pass. Three roles, one per pass:

| Role | What it defends |
|------|-----------------|
| handling editor | fit to the venue; length; novelty against the nearest prior work; abstract and conclusion saying what Results says |
| methods reviewer | design, sample, reference measurement, provenance of every number, every equation |
| practitioner reviewer | usefulness in the reader's own work; whether the setting resembles one they know |

A review is complete when all three roles have run 4.2 to 4.5 over the same text.

### 4.2 Pre-pass: the claim and what carries it
Before criticising anything, answer two questions in writing: what is the one claim the text
rests on, and which fact ids and figures carry it. Then take each carrier away in turn and
ask whether the claim still stands. A claim that falls when one fact is removed is a
linchpin claim; name it and the fact id. Apply the lens questions from
`reviews/review-lenses.md` here, one lens at a time, one written answer per question.

### 4.3 Pass 1: surface
Mark, with the sentence quoted:
- method adjectives that carry no information;
- a settled tone over a `pending` or `partial` anchor, or wording above the tier the row allows;
- a derived or relative descriptor missing the qualifier claim-map gives it;
- a disallowed claim entering through an adjective, a title word, or a caption;
- the group's earlier publication re-described as if new, or without its citation.

### 4.4 Pass 2: argument
- Does each step from facts to conclusion appear on the page, or does the reader supply it?
- Does every method mention in Results have a method-trace bullet, and the reverse?
- Is the claim carried by Results, or only asserted in Discussion?
- Are limitations where a reviewer will look for them, and are they quantified?
- Is the delta from prior work, the group's own included, stated in one sentence?
- Does each catalog entry in venue-calibration have its answer in the right section?

### 4.5 Pass 3: reader value
In the practitioner's voice: after reading this, what can I do that I could not do before,
and in which task? Do the method details map onto a setting I recognise (cost, cadence,
skill required)? Does the text give me grounds to judge whether it transfers to my own
conditions? A text that is correct but fails here belongs at a different venue.

### 4.6 Frame lock
After the passes, ask one more question: is the text still arguing from a framing adopted
before the evidence arrived, which the evidence should have changed? Typical shapes: an
introduction motivating a capability the experiments never test; a granularity chosen for
the method's sake rather than the reader's; a comparison promised up front that the design
cannot support. Record the answer either way ("frame lock: none found" counts). A positive
answer goes to the human in conversation: an Interpret question; story-spine is human-owned.

### 4.7 Severity
Grade before writing the comment. The board enum is BLOCKER, MAJOR, MINOR, NOTE.

| Severity | Test | Where it goes |
|----------|------|---------------|
| BLOCKER | a competent reviewer would reject on this alone, and no rewording fixes it: it takes a run, a redesign, or withdrawal of the claim | `boards/findings.csv`; blocks Submit |
| MAJOR | the claim or the method description must change before submission | `boards/findings.csv` |
| MINOR | should change; may ride the last polish pass | `boards/findings.csv` |
| NOTE | not a defect: a strength, an alternative reading, a linchpin, a frame-lock result | end of the review file |

Grounds that qualify for BLOCKER (anything else is at most MAJOR): the paper's own frozen
facts contradict the conclusion drawn from them; an assumption the method depends on is
falsified by the paper's own measurements; a step from facts to conclusion is missing and no frozen
fact could supply it; a rival explanation fits the facts at least as well with fewer
assumptions. Wording-only findings go to polish and are not filed.

### 4.8 Deliver and record
- One finding list. Each entry: quoted sentence and location, role, pass, severity, a
  one-line fix direction, and the owning skill (claim-audit, method-design, story-design,
  polish, integrity-check, experiment-loop, new-evidence-integration).
- The single most important finding is restated in one line at the top of the file; then
  the frame-lock result, the linchpin claims, the NOTEs, and written answers to the
  calibration questions in `reviews/review-lenses.md`.
- File: `reviews/<date>-shadow-review.md`. Every BLOCKER and MAJOR becomes a row in
  `boards/findings.csv` (`source` `shadow-reviewer`, status `open`, summary within the cell
  limit, detail by finding id in the file). A row leaves `open` only on the human's
  decision; a declined BLOCKER or MAJOR carries the ADR id in `adr`.
- Routing: a missing fact to the experiment agent; a claim-strength question to claim-audit;
  doubt about a fact's reality to integrity-check; a frame lock to the human.
- `manuscript/` is not touched.

### 4.9 Re-review: scoring a rebuttal (anti-sycophancy rules)
The author side (the head in a later session, or the human) may rebut a finding. When author
and reviewer are the same model the reviewer agrees too easily; these rules make it cost.

1. Check that the rebuttal answers the finding as written. If it answers a different point,
   say which point it answered and restate the finding; do not follow the new topic.
2. Score the rebuttal before writing any response:

   | Score | The rebuttal | Action |
   |-------|--------------|--------|
   | 5 | brings new evidence or logic that removes the problem | withdraw |
   | 4 | removes most of the problem | lower severity one step |
   | 3 | answers part of it; the core stands | maintain, noting the part answered |
   | 2 | answers something else | restate the finding; name what is missing |
   | 1 | asserts without evidence | maintain; add the dimension the rebuttal ignored |

3. Log next to the finding: `[REBUTTAL <finding_id> | score n | action | one-line reason]`.

Hard rules:
- Severity moves down only on a 4 or a 5. Pushback below that changes nothing.
- No two concessions in a row. After a withdraw or a downgrade, the next finding is conceded
  only on a 5; a 4 maintains.
- Repetition does not raise a score. The third statement of a point scores what the first did.
- Track the concession rate: withdrawn plus downgraded, over the original finding count. At
  one half or more, write a self-flag in the file ("I have conceded half or more of my
  findings; a human should judge whether the text improved or I accommodated"), file it as
  a NOTE row in `boards/findings.csv`, and add an item to `boards/human-owed.csv`.

## 5. Anti-patterns
How a shadow reviewer fools itself:
- **Defending what it wrote.** The review explains why a passage is fine. Find the attack
  first; a strength is a NOTE, not the review.
- **Volume as rigour.** Twenty small comments and the one fatal gap missed. The top line
  names the worst problem before anything else.
- **Grading from tone.** Gentle comment, harsh severity, or the reverse. Severity first.
- **Swayed by confidence.** An author's certainty is not evidence. Score the argument.
- **Role blending.** "I feel" in place of "the authors state X; the evidence shows Y".
- **Editing instead of diagnosing.** The fix is another skill's session.
- **Skipping pass 3.** A correct paper nobody at the venue can use is a finding.
- **Reviewing with the reserve in hand.** What is not on the page does not count.

## 6. Closing condition
- `reviews/<date>-shadow-review.md` exists with: scope and claim sentence; three roles run;
  a written answer to every lens and calibration question in `reviews/review-lenses.md`;
  linchpin claims; the frame-lock result; a finding list with quote, role, pass, severity,
  fix direction, owning skill; the top-line finding.
- Every BLOCKER names which of the 4.7 grounds it meets.
- Every BLOCKER and MAJOR has a `boards/findings.csv` row with `source` `shadow-reviewer`.
- `python3 tools/check.py` passes, and `git diff --stat manuscript/` is empty.
- On re-review: every rebuttal has a logged score and action; the concession rate is
  written; at one half or above, the NOTE row and the human-owed item exist.
- The contract's closing line is satisfied as written.
