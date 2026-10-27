---
name: cold-review
version: 0.1
ported_from: "Paper3 review practice 2026-06/07"
---

# cold-review

External review of the rendered manuscript by a reviewer that has never seen the workspace:
a different model, or at minimum a fresh agent with an empty context, given only the PDF and
the venue's reviewer guidelines. Several personas review independently; the head and the
human synthesise a go/no-go. Stage: Review, immediately before Submit.

The first-generation project found that its in-house shadow review, run by the model that
wrote the text, missed gaps (reference-definition alignment, repeated-measures inflation,
missing runtime diagnostics) that a different model and a cold human read found at once. The
reviewer that was the writer cannot un-know the intent behind a sentence. This skill makes
the cold read a lifecycle step rather than an improvisation.

## 1. When to invoke

- The submission build renders, `tools/check.py` is green, shadow review has closed with no
  open BLOCKER, and the human intends to submit.
- After a revision round that changed claims, structure or front matter: run again with new
  personas on the new PDF. Never re-run the same reviewer instance on a revised PDF.
- Optionally once at the end of Write on the whole render, to find structural problems while
  they are cheap. Not for a single section; not a replacement for shadow review.

## 2. Inputs to read

Two lists. The separation between them is the skill.

**The head reads**, to prepare the package and to synthesise:
- `manuscript/` submission build: the PDF with `%!` notes stripped and every figure wired.
- `identity/venue-calibration.md`: the venue's reviewer guidelines, or the pointer to the
  venue's public reviewer form, plus the venue risk catalog (for persona briefs only).
- `boards/findings.csv`, to allocate ids and to see what shadow review already found. Read
  it after the persona reports are in, not before writing the briefs.
- `identity/claim-map.md` and `decisions/ADR-*.md`, during adjudication only.

**The cold reviewer receives, and nothing else:**
- the rendered PDF (the same bytes for every persona; record its `sha256`);
- the venue's reviewer guidelines (the public document the venue gives its reviewers);
- a one-paragraph persona brief (4.3) stating the hat and the output format.

## 3. Excluded inputs

For the cold reviewer, everything in the workspace: `identity/`, `reality/`, `boards/`,
`decisions/`, `experiments/`, the LaTeX source, prior review files, the cover letter, the
conversation, and any rebuttal. A reviewer given the claim-map "for context" is no longer
cold; it will review the paper the authors meant to write.

For the head: `tmp/`, chat backups, and the reviewer reserve until adjudication.

## 4. Protocol steps

### 4.1 Preconditions and version pin

Check: `python3 tools/check.py` passes; no open BLOCKER in `boards/findings.csv`; the PDF
has no placeholder figure boxes, no empty title or author field, no visible working note.
Record in the synthesis header: date, git commit of `manuscript/`, `sha256` of the PDF,
reviewer model and version, persona list. A review that cannot be tied to a version cannot
be acted on later.

### 4.2 Choose the reviewer

Preferred: a model from a different family than the one that drafted the prose. Acceptable:
the same family in a fresh agent with an empty context and no workspace access. Never: the
head, or any agent that has read `identity/`. Write the choice and the reason in the header.

### 4.3 Personas (minimum four; default five plus the logic lens)

Each persona is one independent run: same PDF, same guidelines, its own brief, no shared
context, no reading of other personas' output.

| Persona | Attacks |
|---------|---------|
| Domain practitioner | value to the venue's reader; realism of the setting; fit to practice |
| Methodologist / statistician | design, sample, independence of reference measurements, pseudo-replication, model choice, every equation |
| Adjacent-field reader | novelty against the neighbouring literature; a repackaged method from next door; missing citations |
| Editor-in-chief | 60-second desk screen of title, keywords, abstract; then whole-paper consistency, length, figure budget, data and code availability |
| Devil's advocate | the strongest counter-narrative; linchpin evidence; unstated premises; what the authors are quietly not saying |
| Logic coherence (4.4) | structure index, argument chain, abstract and conclusion against results |

The brief says: the hat; what the venue's guidelines ask reviewers to judge; that disclosed
limitations typical of the field are rated against venue norms, not against an ideal; the
output format of 4.5; and that the reviewer must quote the passage it attacks. The brief
never says what the authors think is weak, what was already fixed, or which claims are
locked. That anchors the reviewer and wastes the cold read.

### 4.4 Logic-coherence lens

A persona that checks the text against itself, not against the world. Three sweeps:

1. **Structure index.** List every figure, table, equation, appendix and supplementary item
   and every reference to one. Flag: references to items that do not exist; items never
   referenced; numbering gaps; a later item cited before an earlier one. Not errors: "we do
   not show", "in future work", supplementary naming variants, repeated references.
2. **Argument chain.** Extract research questions (introduction, objectives), claims
   (abstract, results, discussion, conclusion, each with strength and scope) and evidence
   (results and captions; caption-only evidence counts, mark it). Walk each chain: question,
   method, evidence, interpretation, claim. Issue types: missing link, overgeneralization,
   causal leap, internal contradiction, method mismatch, question never answered.
3. **Conclusion match.** Map every abstract and conclusion claim to a results finding or
   mark it unsupported. Check numbers agree within rounding; hedging matches (a result that
   "suggests" cannot be concluded as "demonstrates"); scope qualifiers (dataset, task,
   condition) survive into the abstract. Tolerances: rounding and synonymous quantities pass;
   an interval in results against a point in the abstract is MINOR; a hedged conclusion on a
   trend is "needs clarification", not over-claim.

Hard threshold: BLOCKER or MAJOR only when the claim is located, the evidence is located or
its absence is explicit, and the gap type is named. Otherwise MINOR with a human-judgment
flag. When argument plausibility and numeric consistency disagree, numbers win. In this
workspace a numeric mismatch inside the PDF usually means two facts mapped to one quantity
or a precision setting in `manuscript/facts-map.yaml`; it is still a finding.

### 4.5 Per-persona output

Each persona returns one report: a verdict as a reviewer would file it (accept, minor
revision, major revision, reject); findings, each with the quoted passage and its page or
section as seen in the PDF, severity (BLOCKER, MAJOR, MINOR, NOTE), the question a reader
would ask, a fix direction, and confidence (high, medium, low); then "what is strong", at
least one item. The head stores every report verbatim in the appendix of the synthesis file.
No report is edited, summarised in place, or answered.

### 4.6 Synthesis (head drafts, human adjudicates in the same conversation)

1. **Deduplicate.** Same location, same issue across personas: one finding; keep the version
   with the better evidence span; record which personas converged. Convergence of two or
   more raises confidence, not severity. Severity follows shadow-reviewer 4.7.
2. **Verdict table.** One row per persona: verdict, counts of BLOCKER / MAJOR / MINOR / NOTE,
   one head note.
3. **Go/no-go.** `NO-GO` if any BLOCKER stands after adjudication; `GO-AFTER-FIXES` if only
   MAJOR and MINOR remain and none needs a new run; `GO` otherwise. It is the first line of
   the file; the single most important issue is the second.
4. **Adjudicate every BLOCKER and MAJOR with the human**, one at a time: `verified` (real;
   enters the fix queue), `misread` (the reviewer misunderstood; the misreading is itself
   evidence of unclear text and is kept, usually as MINOR or NOTE with a clarity fix), or
   `declined` (the human decides not to act; reason recorded, ADR id when the reason is a
   prior decision). The head never adjudicates alone and never argues with the report.
5. **Sections of the file**: BLOCKERS; MAJORS; MINORS (one polish pass); "What is strong, do
   not break" (items confirmed by two or more personas, so the fix pass protects them);
   "Ownership and sequence" (human: title, authors, framing and claim-boundary calls; head:
   mechanical and prose fixes with no claim change; experiment agent: anything that needs a
   run); appendix of verbatim reports.
6. **Boards.** Every verified or declined BLOCKER and MAJOR becomes a row in
   `boards/findings.csv` with `source` `cold-review`, status `open` or `declined`, and the
   ADR id for declined ones. Human-owned items go to `boards/human-owed.csv`. The
   160-character cell limit holds; detail lives in the review file under the finding id.

### 4.7 No rebuttal channel

The cold reviewer never sees the rebuttal, the adjudication, or the revised PDF. If the
human wants a second opinion after the fixes, that is a new cold review: new personas, new
PDF hash, new file. A reviewer that can be argued down is a shadow reviewer; the
anti-sycophancy protocol lives there, and this skill avoids the problem by construction.

## 5. Anti-patterns

- Giving the reviewer the source, the claim-map, or a prior review "so it understands the
  context". Context is the contamination; the point is the reader who has none.
- Running the cold review inside the conversation that drafted the text and calling it
  cold. That is shadow review, and it is already a skill.
- Replying to a persona report. There is no channel; adjudication is head plus human.
- The head marking findings `declined` on its own, or softening a BLOCKER because "we
  decided this in an ADR". The ADR explains the decision; it does not mean the page
  communicates it. Ask the human whether the manuscript should say what the ADR says.
- Discarding a misread as reviewer error. A fresh expert misread it; a real reviewer will.
- Reviewing a build with placeholders, an empty author block, or visible working notes. The
  review spends itself on mechanics and the content gets a shallow read.
- One persona. A single hat has a single blind spot; convergence is the signal.
- Omitting "what is strong". The fix pass then breaks what worked.
- A synthesis that is a long list with no first line. State the verdict and the one issue
  that matters most before anything else.
- Rating a disclosed, field-typical limitation as fatal because an ideal study would not
  have it; or the reverse, excusing an undisclosed one because the field tolerates it.
- Letting the review float free of a version: no commit, no PDF hash, no model recorded.

## 6. Closing condition

- `reviews/<date>-cold-review.md` exists with: header (date, commit, PDF `sha256`, reviewer
  model, persona list, reason for the reviewer choice); verdict in line one; per-persona
  table; BLOCKERS, MAJORS, MINORS; "What is strong, do not break"; "Ownership and
  sequence"; an adjudication entry (`verified` / `misread` / `declined`, with the human's
  decision) for every BLOCKER and MAJOR; appendix of verbatim persona reports.
- Every verified or declined BLOCKER and MAJOR has a row in `boards/findings.csv` with
  `source` `cold-review`; declined rows carry an ADR id.
- Human-owned items appear in `boards/human-owed.csv`.
- `python3 tools/check.py` passes.
- `manuscript/` is byte-identical to the reviewed commit at session end; fixes are later
  sessions under their own skills.
- Submit stays gated: no `open` BLOCKER from this file.
