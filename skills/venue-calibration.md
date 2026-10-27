---
name: venue-calibration
version: 0.1
ported_from: "Paper3 skills/venue-calibration.md v1.2"
---

# venue-calibration

Calibrate how much to write, what to leave silent, and how to package highlights for a venue
from a corpus of its published exemplars, not from the model's impression of the venue. Runs
before Write for any new or changed venue; its output is read at run time by method-design,
story-design, shadow-reviewer, and polish.

Why it exists. Three rule layers govern the prose: the invariants (claim ≤ evidence, immutable
facts, never-weakened disallowed claims and limitations, the qualifier rule); the paper's own
identity (the three identity files); and the venue norm: what this readership expects expanded,
what it accepts as silent, how it packages a contribution, how long a Methods section runs. The
first two have skills and a checker. The third used to live in the agent's training prior,
which runs conservative ("no Results consumer, do not write it") and ages. This skill replaces
the prior with evidence. Calibration widens the option space and never relaxes a principle
boundary: an exemplar expands a detail, we may; an exemplar is silent, we need not force it; an
exemplar overclaims, we do not follow. Learn packaging syntax, never claim strength.

## 1. When to invoke
- Before drafting the first section for a venue (ordinarily Methods) when
  `identity/venue-calibration.md` has no fresh section for it.
- When method-design's silent-vs-mention filter produces a result that feels too conservative;
  the suspicion is that the venue expects a detail the filter dropped.
- When the target venue changes. The venue choice is a human decision, recorded as an ADR.
- When `next_stale_check` in the venue section has passed, or Submit is approaching on a
  calibration older than six months.

Do not invoke for claim-boundary or evidence questions (claim-audit, integrity-check) or for
language only (polish). A fresh calibration plus a drafting skill is the normal path.

## 2. Inputs to read
- `identity/venue-calibration.md`: existing venue sections, if any.
- `reviews/venue/<venue>/corpus.md`: the exemplar registry (candidates, query used, similarity
  scores, acquisition status).
- `reviews/venue/<venue>/<paper_id>.md`: existing dissections.
- `identity/claim-map.md`: the boundary calibration may not cross.
- `identity/method-trace.md` §4: the method bullets whose silent-vs-mention decisions the
  calibration informs.
- The venue's guide for authors: hard limits (abstract length, highlights, reference style).
- Optional: exemplar PDFs when a dissection is ambiguous; the paper's reference list, to mark
  exemplars it already cites.

## 3. Excluded inputs
- `manuscript/`: our prose must not shape what we observe as the venue norm.
- `experiments/*/notes.md`, `tmp/`, chat backups.
- Exemplar supplementary material, unless a dissection field explicitly needs it.

## 4. Protocol steps

### 4.1 Scope line
One sentence: the venue, the section the calibration serves first, and the trigger (first
draft, filter too strict, venue change, stale).

### 4.2 Corpus collection
Quota per venue, minimum 6–8 papers:

| class | count | use |
|---|---|---|
| modern peer (< 4 years, similar topic, similar method scale) | 4–6 | primary calibration source |
| highly cited reference in the venue | 1–2 | top-level expectations |
| revision-tracked (preprint vs published; optional) | 0–2 | what reviewers actually asked for |

Recency decay: papers older than 5 years may be read but do not enter the main corpus. Same
venue, different problem class is not a modern peer. Diversity: at least 3 institutions or
groups, never one author group. Similarity scoring, manual, 1–5 per axis: subject or material
class; sensor, instrument, or data modality; method family; temporal scope (single time point,
longitudinal, dynamics). Total ≥ 12/20 enters the main corpus; below 12 is read-only.

Procedure: search the venue's last four years with the available literature index and record
the query in `corpus.md`; score candidates; obtain PDFs (open access: download; otherwise a
`boards/human-owed.csv` row); register each paper in `corpus.md` with acquisition status.

### 4.3 Per-exemplar dissection
One file per main-corpus paper at `reviews/venue/<venue>/<paper_id>.md`, this schema. The agent
drafts; the human reviews before the file counts (anti-pattern 8). Every quoted sentence
carries a page or section reference; a quote without one is SUSPECTED and blocks aggregation.

```text
---
paper_id: <year-firstauthor-shorttitle>     venue: <name>     year: <YYYY>     doi: <DOI>
citations: <count and index, at dissection time>
title: <full title>
similarity_score: <total /20>
similarity_breakdown: {subject: 1-5, modality: 1-5, method_family: 1-5, temporal: 1-5}
status: dissected | in-progress | corpus-rejected
dissected_by: <agent or human>     dissected_on: <YYYY-MM-DD>     human_reviewed: yes | no
---
## Method section anatomy                               (feeds: method-design)
- Methods word count; sub-section count; sub-section tree with per-node word count and
  detail density (high / med / low); one-line density assessment per sub-section.
## Self-positioning anatomy                             (feeds: story-design)
- Scope-defining sentence (object + scope; location); boundary sentence (what it does not do;
  location); venue-fit sentence (why this readership should care; location); where the three
  fall (abstract / intro first / intro last); immediately clear to the venue reader? (yes /
  partial / no); implication for our abstract and intro opening.
## Result-support mapping                               (feeds: method-design)
| method bullet (paraphrased) | result section / figure | direct Results coverage? |
  ("no" rows annotated: context-establishing, or unsupported)
## What is silent                                       (feeds: method-design)
- Details the exemplar omits that we would worry about writing (threshold values, reference
  protocol); per item: does omitting it cost our reproducibility?
## What is expanded                                     (feeds: method-design)
- Details written more fully than expected (environment, calibration); per item: applicable
  to our paper?
## Highlight packaging                                  (feeds: story-design, polish)
- Highlight sentences quoted with location; packaging-verb inventory (propose / develop /
  extend / introduce / address); novelty strength (hedged / moderate / strong); how the prior
  work closest to ours is handled (cite and extend / cite and differentiate / silent).
## Risk-tolerance signals                               (feeds: claim-audit, shadow-reviewer)
- Claim ≤ evidence strictness (rigorous / moderate / loose), one example; treatment of derived
  or relative quantities (relative / mixed / absolute), one example; limitation disclosure
  density (thorough / standard / minimal).
## Weakness-handling tactics                            (feeds: shadow-reviewer, story-design)
- Observed tactics with location: disclose / reframe as future work / isolate to a limitation
  paragraph / hedge-blunting / silent on a known weakness. Observation only.
- For each of our own known weaknesses: the exemplar's tactic; the tactic we should use.
- Invariant flags: tactics observed but forbidden to imitate (silent on a known weakness,
  absolute claim on a relative quantity), with the invariant each breaks.
## Quotable scaffolds                                   (feeds: polish, story-design)
- Methods opening template; sub-section transition; Methods-to-Results bridge; limitation
  disclosure sentence. Syntax only, never content.
## Reader-engagement moves (after Larry McEnerney)      (feeds: story-design, polish)
- Density of instability / gap / problem / change triggers in the intro opening, with
  examples; venue-coded vocabulary that signals "this is your conversation"; reader-cost and
  value-promise sentences; how the paper signals it addresses this readership rather than a
  neighbouring field; engagement strength (high / moderate / low); templates we may borrow.
## Notes for our paper
- Three things to borrow; one or two not to learn (with invariant flags); where our
  silent-vs-mention filter can loosen; cross-section feedback to the section being calibrated.
```

Round-1 reading discipline. The first round for a venue reads every block through one primary
lens, the section about to be drafted (ordinarily Methods): fill all eleven blocks, but filter
each observation by "what does this imply for that section, including cross-section feedback"
(a scope sentence in the exemplar abstract tells us which scope elements Methods must define; a
weakness isolated to a limitation paragraph tells us which method bullet must lay its
definition; an engagement trigger in a Methods opening tells us whether to adopt the move).
Round 1 propagates only to that section's consuming rules. Later rounds for other skills
re-read the filled dissections, never the PDFs.

Hard-rule reminders while dissecting: self-positioning never adopts an exemplar framing that a
disallowed claim forbids; weakness tactics are observed, never imitated to hide; reader
engagement borrows syntax, not claim strength; an expectation-violating opening needs frozen
facts behind it or drops to hedged wording.

### 4.4 Aggregation
Write or update the venue's section in `identity/venue-calibration.md`. A rule needs support
from at least two papers; a one-paper observation is written as "to be confirmed".

```text
## Venue: <name>
metadata: active_target: yes|no  corpus_size: <N>  last_calibrated: <date>  next_stale_check: <date + 6 months>
          english_variant: US|UK  hard_limits: {abstract_words, highlights_count, highlight_chars, ...}
### Permission space (may loosen)
- P1: <pattern> | supported by: <paper_id, paper_id> | implication for method-design silent-vs-mention: ...
### Constraint space (must include)
- C1: <pattern> | supported by: <...> | implication for method-trace §4: ...
### Highlight playbook
- H1: <template> | example quote + paper_id | tier it is honest at: hedged | moderate | strong
### Forbidden moves (seen in exemplars; red flags under modern review)
- F1: <pattern> | rationale (which invariant) | paper_id (negative example)
### Length, structure, density observations
- Methods word count median and range; sub-section count median and range; result-support
  ratio; reference density per section; sentence-length norm; negation-density norm
### Source corpus
- list of dissection files
### Change log
```

### 4.5 Propagation
In v2 propagation is a data update, not a skill edit. method-design, story-design,
shadow-reviewer, and polish read the active venue's section at run time (silent-vs-mention
override; intro and discussion packaging; venue-specific reviewer expectations; hedge dialect,
highlight verbs, and length targets, respectively). If a downstream skill needs a value the
section lacks, add the field to the section; do not write an exception into the skill. Record
the propagation in the section's change log. claim-audit, integrity-check, and
new-evidence-integration do not consume calibration at all.

### 4.6 Stale tracking
Set `next_stale_check` to `last_calibrated` plus six months. A calibration past that date is
stale: a Write session for that venue re-runs 4.2 as a recency sweep (new modern peers only)
before drafting, and Submit does not proceed on a stale calibration. If the venue was chosen or
changed in this session, the ADR names the venue and the calibration section.

### 4.7 Hard rules
Never overridden, whatever the corpus does: disallowed claims and limitations (claim-map §2,
§3); the qualifier rule for derived or relative descriptors; wording tier ≤ evidence status;
immutability of `reality/`; any tier change that waits on a human decision recorded in an ADR.
May be influenced: which method bullets are mentioned without a direct Results consumer;
reproducibility detail level; detail density, word counts, structure allocation; highlight
verbs and syntax; limitation disclosure density; hedge dialect; reference density; section
balance.

## 5. Anti-patterns
- **Mimicry without principle.** Copying an exemplar's claim strength instead of its packaging.
  Every P or H row names the method-design or polish rule it affects, never a claim-map row.
- **Single-paper anchoring.** One exemplar did X, so X becomes a rule. Two papers or "to be
  confirmed".
- **Old-paper laundering.** A paper older than five years in the main corpus. Review
  expectations have moved; apply recency decay.
- **Highlights beyond what the evidence honours.** "We propose a novel..." learned from the
  corpus for a contribution that is not novel. Packaging verbs follow tier: strong → demonstrate,
  establish; moderate → develop, extend; hedged → explore, investigate.
- **Calibration overriding an invariant.** "The exemplar reports the absolute quantity, so we
  can." It goes into Forbidden moves with a do-not-learn note in the dissection.
- **Nameplate mimicry.** Copying a section's architecture and swapping the subject noun.
  Extract abstract patterns (allocation ratios, verbs, detail level), never concrete content.
- **Calibration as a substitute for judgement.** Every writing decision "per calibration". The
  venue section is a permissive override; story-spine and claim-map still decide.
- **Dissection hallucination.** The draft invents a highlight pattern or exaggerates risk
  tolerance. Human review is mandatory; no location reference, no aggregation.

## 6. Closing condition
Every in-scope corpus paper has a dissection at `reviews/venue/<venue>/<paper_id>.md` with
`status: dissected` and `human_reviewed: yes`; `identity/venue-calibration.md` has the venue's
section with complete metadata and at least two supporting papers for every P, C, H, and F row;
a self-audit line in that section states that no row crosses a hard rule in 4.7;
`python3 tools/check.py` passes (cross-ref: every dissection the section lists exists); an ADR
exists if the venue was chosen or changed this session; the contract's closing condition is met.
