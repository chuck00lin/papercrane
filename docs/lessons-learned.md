# Lessons learned from the first generation

This page is the honest part of the project. The framework is the third iteration of a way
of working the author refined across three papers; the first generation described here
governed the third paper end to end.

The first generation of this method governed one journal manuscript from February to October
2026: a control index, three identity files, an append-only facts folder, three status CSVs,
eight protocol files, a 7-line session contract, and a tmux bus connecting agents in four
repositories. It reached a polished, fully drafted manuscript. This page records what it got
right and what it got wrong, because the second generation is designed against this list.

## What it got right (kept)

- **Claim / reality / status separation** with hard, never-weakened disallowed claims and
  limitations. It held through a complete swap of the primary dataset without touching the
  story.
- **Skills as protocols**: a fixed six-section structure (when, inputs, excluded inputs,
  steps, anti-patterns, closing condition). Anti-patterns and checkable closing conditions
  were the parts that actually changed agent behavior.
- **Excluded inputs** as a first-class field. Saying what will not be read prevented more
  drift than listing what would be read.
- **Shadow review with concession tracking.** A reviewer agent that counts its own
  withdrawals and flags itself when it has conceded half of its findings.
- **Integrity check** adapted from the seven failure modes of AI-assisted research
  (implementation bug passing self-review, hallucinated citation, hallucinated result,
  shortcut reliance, bug reframed as insight, methodology fabrication, frame lock), with a
  mandatory "surprise language" sweep.
- **Decision records with a supersedes chain**, and **errata blocks instead of overwrites**.
  History was never lost.
- **Disclosure economy**: facts that support no claim are held in a reviewer reserve, not
  volunteered; each boundary is stated once at its natural home, never as a repeated
  disclaimer.
- **Venue calibration** from an exemplar corpus rather than from the model's impression of
  the journal.
- **Experiment campaign records in the compute repository**: numbered records from a fixed
  template, a variant tag per run, a benchmark table with a declared schema, a leaderboard,
  an index, and campaign retrospectives. This was the best-run part of the project and the
  model for v2's experiment registry. Its one gap was that nothing linked a new run to the
  manuscript sentences that depended on the old one.
- **Working notes inside the LaTeX source** behind a comment marker, stripped by the
  submission build. Notes and prose co-locate but never co-render.

## What it got wrong (fixed in v2)

### 1. Numbers travelled by hand through four copies

Pipeline CSV, hand-typed into a facts markdown, hand-typed into the claim map and status
board, hand-typed into LaTeX. A reconciliation audit in month eight found exactly the
failures this produces: a prose threshold the data did not meet, a ratio no script could
reproduce, a cluster count presented as a plant count, a caption describing interval ends
where the code computed midpoints, and an inconsistent rounding. Figures were already
script-rendered; numbers were not.

**v2:** facts are emitted by runs as schema-checked JSON with provenance, frozen by hash, and
compiled into LaTeX macros. A bare numeral in prose fails the build.

### 2. Experiment design sat outside the loop

The writing side learned the second dataset's design weeks after acquisition had started
and extracted the basic facts from the PI in four rounds of Q&A. One treatment arm turned
out to be an incomplete factorial with no control cell and became a prohibited claim: zero
usable content. Plant spacing, the reference-measurement start date, and whether reference
heights were measured vertically were all recovered months later.

**v2:** a design contract is written with the human before any run, pre-registered against
the disallowed-claim list, and lists the metadata that must be logged at acquisition time.

### 3. Reality was prose, not data

The facts file grew to four hundred lines with sixteen errata blocks that superseded each
other. Append-only was a social rule. The hash-pinned data package with a reconciliation
directory that finally made numbers auditable was built in month eight as a rescue.

**v2:** `reality/` holds frozen files and one errata log. Immutability is enforced by the
freeze step and the checker, not by discipline.

### 4. Ceremony was heavy and got gamed

One identity edit required five writes. CSV cells became five-hundred-character essays. The
live tracker grew past two hundred kilobytes. The human eventually had to write a rule
telling the agent to stop adding checks just to turn every row green.

**v2:** boards have schemas and cell-length limits. Cross-file consistency is a checker, not
a ritual. A rule the checker cannot express is a candidate for deletion.

### 5. The exploration layer was designed but never used

The sandbox folder stayed empty. Ideation happened in chat and landed in backups the agent
was forbidden to read. Decision rationale columns were frequently empty.

**v2:** human decisions are recorded as three-line ADRs the agent can cite. Chat transcripts
stay excluded.

### 6. Governance documents drifted from each other

The workflow document still spoke the language of layers retired five months earlier. A
strategy document never received the decision that made it obsolete. A placeholder facts
file sat with an "obsolete" banner. Two agent-instruction files disagreed about the default
literature tool.

**v2:** fewer documents, one authority per concern, and a checker that fails on dangling
references between them.

### 7. Speculative governance was over-built

A five-path taxonomy, a dedicated integration skill, and a decision gate were built for a
scenario ("second batch as add-on") that a single PI decision replaced with "substitution".

**v2:** build the minimal invariants; scenario documents are short, carry an explicit expiry
trigger, and are archived when it fires.

### 8. The reviewer was the writer

External reviews by a different model and a cold human read found real gaps (reference
definition alignment, repeated-measures inflation, missing runtime diagnostics) that the
in-house shadow review, run by the same model that wrote the text, had not.

**v2:** a cold external review stage with a different model and no workspace context is a
named lifecycle step, not an improvisation.

### 9. Authority split across repositories

The pipeline repo kept its own claims framing; the plotting repo had no agent instructions;
the bus worked as a transport but agents printed results in their own pane instead of
pushing them, and permission prompts stalled them silently.

**v2:** one claim authority. External repos are attached as code spaces with a small
contract: run a named experiment, emit facts, reply through the bus with a literal command.

### 10. Terminology and labels were policed by eye

A trait name flipped twice. A cadence word needed a formal decision to suppress. A display
remap of row labels lived in a prose section.

**v2:** terminology rules and label maps are data files consumed by the checker and by every
plot script.

### 11. Human-owed inputs were not tracked

Pre-submission blockers were author front matter and hand-assembled figures. A PI briefing
carried a list of five facts only the human could supply.

**v2:** `boards/human-owed.csv` is a first-class queue with due dates, and Submit is gated on
it being empty.
