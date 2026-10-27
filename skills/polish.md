---
name: polish
version: 0.2
note: "rewritten from concepts; no adapted text"
---

# polish

The last pass over a section's wording, taken once its claims and evidence have stopped
moving. Polish changes how sentences read; it never changes what they assert, which number
they show, or how strongly they say it. Head runs it at the end of Write, and the section
then goes to Review. Every list of words, openers, or shapes this skill sweeps for lives in a
data file the writer owns, not in this text.

## 1. When to invoke

- The section's row in `boards/draft.csv` is `drafted`, every claim in its `depends_on` has
  `frozen` evidence or an explicit `pending` tier in `identity/claim-map.md`, and no run is
  scheduled that would move those rows.
- Before shadow review, cold review, or Submit.
- After a review round, to close wording-only MINOR and NOTE rows in `boards/findings.csv`.

Not this skill: content that may still move (wait); a sentence that says more than its facts
(claim-audit); a method description that differs from what ran (method-design); a section that
still needs drafting (a draft session, which has no skill). Contract: `Stage: write`, `Identity
touch: none`, naming `identity/terminology.csv` or `identity/style-words.csv` if rows may be added.

## 2. Inputs to read

- `manuscript/sections/<id>.tex` and the PDF of the same build, so that every `\fact{}` is
  read as the value the reader will see.
- `identity/claim-map.md`: §0 boundary statements, §1 tiers, §2, §3.
- `boards/evidence.csv` rows for the claims in `depends_on`; the section's `boards/draft.csv` row.
- `identity/terminology.csv` and `identity/style-words.csv`.
- `identity/venue-calibration.md`, the active venue's section: stance values, hedge dialect,
  length and density targets, English variant, hard limits.
- Optional: `identity/story-spine.md` §1 for the reader and the arc nodes; the section's
  figure captions; `reviews/reserve.md`, to know what is deliberately unsaid.

## 3. Excluded inputs

- `experiments/*/notes.md`, `tmp/`, chat backups. Working-note phrasing must not reach prose.
- Sections outside the contract, except abstract, highlights, and conclusion in step 7.
- `reviews/venue/**`: polish reads the calibrated summary, not the exemplars.
- `reality/facts/` directly. A displayed value that looks wrong is a finding against the
  `manuscript/facts-map.yaml` entry, never an edit.

## 4. Protocol steps

### 4.0 What polish does not do

- Meaning. No sentence gains or loses a claim, a scope, a cause, or a condition.
- Numbers. Every numeral is a `\fact{}` or an `allow_literals` entry; polish types no digit.
- Strength. A verb moves down to meet its tier, never up. Tiers belong to claim-audit.
- Anchors and methods. No fact id, no parameter, no description of what ran.
- Additions. No new citation, abbreviation, experiment, result, or limitation.
- Structure, except merging or reordering paragraphs so that a boundary is stated once (4.6).

Permitted: spelling, grammar, punctuation, splitting or joining sentences, a synonym of the
same strength, a pronoun resolved from words already on the page, one English variant. One
rewrite per sentence. Anything on the list above becomes a `boards/findings.csv` row instead.

Pass order: stance, strength, terminology, words and shapes, rhythm and the reader's path,
qualifier and economy, cross-check, record. Stance first: commas do not fix a defensive paragraph.

### 4.1 Step 1: prose stance (first, always)

Published empirical writing names the object, the measurement, the method, the number, and
the reading, then moves on. It does not advertise the contribution, defend the boundary, or
answer reviewers paragraph by paragraph. Drafts produced with an agent fail here far more
often than at grammar, so posture is corrected before any word is touched. Per paragraph:

1. Subjects. Mark each grammatical subject. When most are abstractions about the work (the
   framework, the approach, its reliability), rewrite around the things measured.
2. One job. A paragraph motivates, describes data, describes a method step, reports a result,
   interprets, or states a limitation. A paragraph doing several is split.
3. Positive first. Say what was done; then the scope boundary, once, if it belongs here.
4. Quality adjectives. An adjective that praises the work survives only with a metric in the
   same sentence; otherwise it becomes an observable condition or is cut.
5. Defensive negations. Count them; the active venue section sets the ceiling.
6. Length. Sentence and paragraph targets come from the venue section, never from here.

### 4.2 Step 2: strength and hedge alignment

List every claim sentence; find its claim id and its `boards/evidence.csv` row. The tier table
in `identity/README.md` sets the ceiling: `pending` evidence takes hedged wording, `partial`
takes moderate wording, `frozen` and checked takes strong wording. Wording above the ceiling
is lowered now; wording below it is left alone, because raising a tier is claim-audit's job
after integrity-check. One claim keeps one strength wherever it appears: abstract,
highlights, results, discussion, conclusion. The abstract never exceeds the body. The venue
section says which hedging verbs its exemplars use.

### 4.3 Step 3: terminology (data, enforced)

`identity/terminology.csv` holds `canonical, forbidden_variants, scope, note`; variants are
`;`-separated. `tools/check.py` matches every variant as a whole token in
`manuscript/sections/*.tex` and in `manuscript/labels.yaml` and prints the file, the line, the
variant, and the canonical term. Polish maintains the table: when the pass finds two spellings
of one concept, add a row; put first-mention expansion rules in `note`; renaming a canonical
term is a human decision and gets an ADR. On a failure, change the prose. When the hit is a
legitimate use of the word in another sense, narrow the row (the variant or the scope); never
delete a row to pass, never split a word or hide one behind a macro.

### 4.4 Step 4: words and shapes (data: `identity/style-words.csv`)

Columns `pattern, kind, replace_with, note`. The kinds:

| kind | what it marks |
|------|---------------|
| vague | a word that points at a quality or quantity without stating it |
| cliche | a worn figure of speech that signals register rather than meaning |
| throat-clearing | an opener that delays the subject of the sentence |
| overwrought | a dressed-up word where the plain one is more exact |
| meta-commentary | a sentence that announces what the text will do instead of doing it |
| structure | a shape, not a string: a list length, paragraph size, or paragraph architecture that repeats; found by reading |

A hit is a question, not a ban: is this the most exact word here, or the default one? A word
the paper's field uses as a technical term is exempt, and `note` records the exemption.
Punctuation habits (dashes, semicolons, list openers) are rows of kind `structure` or values
in the venue section; none are fixed here. The file ships with a few illustrative rows; grow
it from your own drafts and the habits of your first language. The template's welcome applies
here most of all: adapt this to your own habits. The idea of sweeping prose by word families
comes from Academic Research Skills (ARS) by Cheng-I Wu; the rows are yours (see ATTRIBUTION.md).

### 4.5 Step 5: rhythm, the reader's path, so-what

Rhythm. Read the paragraph aloud. A run of sentences of nearly equal length is a flag: split
one, or join two short ones. Per-section variation targets are venue-section values, not rules here.

The reader's path, per paragraph: which claim id, or which arc node of
`identity/story-spine.md`, does this paragraph serve (none means a candidate for
`reviews/reserve.md` or the cut)? Does its opening sentence state what it will establish, so
that a reader skimming first sentences still gets the argument? Does its closing sentence
hand off to the next paragraph rather than summarise this one?

So-what, per section, asked once: what would a reader lose if this section were missing? If
the answer names nothing a claim depends on, the section is too long; if it names a claim,
the section's first paragraph should already say so.

### 4.6 Step 6: qualifier rule, boundary economy, disclosure economy

Qualifier rule, permanent. A quantity that `identity/claim-map.md` defines as a derived or
relative descriptor keeps its qualifier at every tier, in the sentence that defines it and in
its claim row. No mention anywhere uses absolute or true-value wording for it; after the
definition it goes by its name. A violation is fixed before any other edit.

Boundary economy. Each boundary is stated once, at its natural home: a definitional boundary
in the Methods paragraph that defines the quantity; a result-type boundary where the number
first appears in Results; a scope boundary as one sentence in Limitations. `claim-map` §0
lists them. Captions describe what is in the figure and carry no boundary text; in-figure
annotations are removed in the code space's plotting code and the figure re-exported. Discussion does not restate a
boundary already given in Results; if it must come up, it is phrased as the next design step.
Sentences of the form "we do not claim", "is not interpreted as", or "serves only as" become
an affirmative statement of what the quantity is and what it is used for. The fix is
de-duplication, never deletion: dropping a boundary's only statement is a claim change.

Disclosure economy. A fact that supports no claim and contradicts none is not volunteered; it
goes to `reviews/reserve.md` with the reviewer question it would answer and a pointer to the
detail. A sentence that closes an attack path earns its place. The test for each sentence:
does it hand the reviewer material, or take material away?

### 4.7 Step 7: cross-check and venue hard limits

When the section is Results or Discussion, read the abstract, highlights, and conclusion
against it for strength and terminology; a mismatch outside the contract becomes a
`boards/findings.csv` row (severity MINOR, source polish) for the next polish session. Hard
limits (abstract length, highlight count, abbreviations defined at first use, locatable
cross-references, citations matching the reference list, required disclosure statements) come
from the venue section; a miss is a BLOCKER finding, and a missing limit is added there.

### 4.8 Record

Set the section's `boards/draft.csv` row to `state: polished`, `polish_passed: yes`, fresh
`last_updated`. Mark the wording findings worked off `resolved` in `boards/findings.csv`;
open a row for anything deferred. Run `python3 tools/check.py`.

## 5. Anti-patterns

- **Polish becomes rewrite.** A strength verb moves up, a sentence is added. Stop; open claim-audit.
- **Harmonising across tiers.** Sections at different tiers forced to one wording. Strength follows the board.
- **Hedge deleted for sounding weak.** A tier up needs evidence up; polish has no such authority.
- **Qualifier cut as clutter.** The descriptor becomes the plain physical quantity. No exception.
- **Boundary on every mention.** Repetition adds no safety and tells a reviewer where to look.
- **Volunteering an unclaimed fact.** A limitation nobody asked for, supporting no claim. Reserve it.
- **Commas before posture.** Grammar fixed in a paragraph still defending itself.
- **Typing a number.** A rendered value looks off and the `.tex` is edited. File a finding.
- **The word file as a ban list.** Every hit replaced mechanically, technical terms included.
- **Skipping the cross-check.** Abstract and conclusion never read against the body.
- **Gaming the terminology check.** A split word or a macro to pass. Fix the prose or the data file.

## 6. Closing condition

- The section's `boards/draft.csv` row reads `state: polished`, `polish_passed: yes`, fresh `last_updated`.
- Wording findings worked off are `resolved` in `boards/findings.csv`; deferrals are open rows.
- `identity/` is byte-identical, except rows added to `identity/terminology.csv` or
  `identity/style-words.csv` under a contract that named them.
- `python3 tools/check.py` passes, terminology and numerals included.
- A diff of the section shows no changed `\fact{}` key, no new numeral, no claim sentence
  whose verb strength rose, and no boundary statement removed.
