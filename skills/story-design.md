---
name: story-design
version: 0.1
ported_from: "Paper3 skills/story-design.md v1.0"
---

# story-design

Design or revise what the paper says to its reader: the gap, the positioning, the promise,
the narrative arc, the discussion arc. Stage: **Idea** (human-led). Run by head; decided by
the human. The agent proposes alternatives in conversation, the human chooses, and the
choice is an ADR before `identity/story-spine.md` changes.

## 1. When to invoke

- Any edit to a section of `identity/story-spine.md` (reader, gap, positioning, promise,
  arc, research questions, discussion arc, anti-pivot guardrails).
- An introduction paragraph or a discussion topic is being planned or re-aimed.
- The paper's relation to the group's prior papers or to the closest external works is
  being re-argued.
- Title or highlights are being chosen. They are story and carry the same boundary.
- A new experiment's facts have been integrated (`skills/new-evidence-integration.md`,
  path C or D) and the question is whether the story should move.
- Any conversation of the form "I think the story would read better if ...".

Not this skill: adding a method bullet (`method-design`), changing a result sentence or a
tier (`claim-audit`), wording (`polish`). Session contract: `Stage: idea`,
`Identity touch: story-spine`.

## 2. Inputs to read

Authoritative:
- `identity/story-spine.md`, all sections.
- `identity/claim-map.md` §0 to §3: boundary statements, allowed claims with tiers,
  disallowed claims, limitations. The story may not promise past them.
- `boards/evidence.csv`: which claims are `frozen`, `partial`, `pending`. The story leans
  on frozen claims; pending ones appear only as questions.
- `decisions/ADR-*.md` whose `touches` includes `story-spine`. The supersedes chain is the
  record of where the story has already been pulled and pulled back.
- The venue's reviewer guidelines and the active venue section of the calibration notes
  produced by `skills/venue-calibration.md`, when they exist.

Task-scoped, optional:
- `experiments/<id>/notes.md` for the experiment whose outcome triggered the discussion,
  to understand the question that was asked. Facts come only from `reality/`.
- The workspace's literature notes for positioning, if it keeps any.

## 3. Excluded inputs

- `manuscript/sections/*.tex`. Existing prose frames the thinking; the story is upstream
  of it and is rewritten into prose later, never read back out of it.
- `identity/method-trace.md` beyond §1 (pipeline backbone). Method detail does not belong
  in a story session.
- Code-space outputs, run folders, and plots not rendered from frozen facts. Claims live
  only in `identity/`.
- `tmp/`, chat backups, and any file the human has not named.

## 4. Protocol steps

1. **Map the current story (under five minutes).** Read story-spine. Answer in one line
   each, in conversation: who the reader is, what the gap is, how the paper is positioned,
   what it promises, what the arc nodes are. Name the one section that feels unstable and
   say why. This is the baseline the alternatives are measured against.

2. **Diagnose before proposing.** Quote the sentence from the human that triggered the
   session. Classify the defect as one of: gap not sharp; positioning unclear or taking
   credit for prior work; promise too weak or too strong; arc node with no result section
   to carry it; discussion topic that restates a result; a §8 guardrail about to be
   crossed. Then ask whether frozen evidence can fix it. If the fix needs facts that do not
   exist, stop: that is a Design-stage question (`skills/design-review.md`) or an
   integration question (`skills/new-evidence-integration.md`), and this session ends by
   naming it.

3. **Generate at least two alternatives, in conversation only.** Nothing is written to
   story-spine yet. For each alternative give: the hook sentence; the claim ids that carry
   it; what the reader can do afterwards; which guardrail it stresses. Score each on four
   questions:
   - Does it speak to the venue's reader, in their problem, before it speaks of the method?
   - Is every claim it needs inside claim-map §1 and absent from §2?
   - Is each of those claims `frozen` in `boards/evidence.csv`, or explicitly `pending`
     and phrased as a question?
   - Does it name what the group's prior papers already established, so the contribution
     is the delta?

4. **Pressure-test without the full shadow review.** For each alternative: the first
   question a reviewer in the field asks on reading the hook; the weakest sentence;
   whether the contribution has quietly become "method X reaches accuracy Y" rather than a
   capability the reader lacked. Report the weakest alternative as weak. An agent that
   makes every alternative look good has not done this step.

5. **The human decides.** Present the alternatives with their scores and stop. When the
   human chooses, draft the ADR from `decisions/TEMPLATE.md`: decision, alternatives
   rejected, why, `touches: [story-spine §n]`, `facts:` the anchors the chosen story rests
   on. The human says yes; the file is written. No story-spine edit precedes the ADR
   (invariant I6).

6. **Write one section.** Edit the one story-spine section the ADR names. Update
   `last_updated`. If the new story needs a claim that claim-map does not have, do not add
   the claim here: write a `boards/findings.csv` row (source `story-design`, severity
   `MAJOR`, target `identity/claim-map.md §1`, status `open`) and name a claim-audit
   session. If the new story drops a claim, its row stays in claim-map until claim-audit
   removes it.

7. **Check.** `python3 tools/check.py`: cross-ref (every claim id the spine names exists)
   and terminology (spine wording obeys `identity/terminology.csv`). In
   `boards/draft.csv`, every section whose `depends_on` includes a moved claim goes back
   to `state: drafted`, `polish_passed: no`.

Worked example, generic. Trigger: "the introduction reads like a software paper."
Diagnosis: the hook leads with the method. Alternative A leads with the measurement that
practitioners cannot currently make; alternative B leads with the gap in the literature on
repeated measurement of the same subjects. Pressure test: A's weakest sentence is the
promise, which implies decision support that C3 (`hedged`) cannot carry; B's hook needs a
generality claim that sits in §2. Decision: A, with the promise cut back to what C1 and C2
(`moderate`) support. ADR written; story-spine §4 rewritten; the introduction row in
`boards/draft.csv` reset.

## 5. Anti-patterns

- **Methods-venue drift.** The hook reads "we propose X and reach Y." The venue's reader
  wants the problem they have, the capability they lack, and what this work lets them do.
  The method is the means and appears third.
- **Novelty over-pivot.** Selling as this paper's contribution something the group's
  prior paper already established. Fix: the positioning section contains an explicit
  "prior paper did A; this paper adds B" sentence, and the arc is built on B.
- **Promise inflation.** The promise uses wording above the tier of the claims it rests on
  (tier table in `identity/README.md`). Fix: the promise is written after the claim ids
  are listed, never before.
- **Reserving room for an unfrozen experiment.** Shaping the story so a running or planned
  experiment "fits later." The story assumes that experiment does not exist. When its
  facts freeze, `new-evidence-integration` decides whether the story moves.
- **Discussion arc as results restatement.** Each discussion topic must answer: what does
  this tell the reader that the results section did not? Implication, boundary, or
  future; never a repeat.
- **Drafting into story-spine "to see how it reads."** Alternatives live in conversation.
  The spine receives only the decided one, after the ADR.
- **Deciding in chat.** A chosen direction with no ADR at session end does not exist, and
  the next session will re-argue it.
- **Title as a loophole.** A title or highlight carrying a claim the claim-map does not
  have. Titles are story and obey the same boundary.
- **Reading the manuscript to find the story.** The prose is a render of the spine.
  Reading it back in freezes the current wording as the story.

## 6. Closing condition

Every modified section of `identity/story-spine.md` has an ADR dated this session with
`touches: [story-spine ...]`; `python3 tools/check.py` passes; any claim the new story
needs but claim-map lacks is an open `boards/findings.csv` row with source `story-design`;
if step 2 found an evidence gap, the next session (`design-review` or
`new-evidence-integration`) is named in conversation and any human-supplied input is a row
in `boards/human-owed.csv`. If `Identity touch` was declared `none`, story-spine is
byte-identical at session end.
