---
name: claim-audit
version: 0.2
note: "rewritten from concepts; no adapted text"
---

# claim-audit

Check that each claim sentence says no more than its frozen facts allow, and that none of
them steps over the claim boundary. Stage: Write; re-entered from Review when a finding
targets a claim's strength. Run by head. The boundary (claim-map §0, §2, §3) is human-owned;
the rows in §1 are the head's, under contract.

The skill assumes the facts are true; whether they are true is integrity-check's question.
The decomposition in 4.2 follows Toulmin's layout of an argument (1958); the level names in
4.4 are this workspace's own.

## 1. When to invoke
- An experiment reaches `status: frozen` and experiment-loop hands over: its facts become or
  update rows in `identity/claim-map.md` §1.
- A Results or Discussion section under `manuscript/sections/` was edited.
- A claim row's tier is about to move, in either direction.
- A `boards/findings.csv` row from shadow-reviewer or cold-review targets claim strength.
- new-evidence-integration chose a path and a row must be rewritten.
- Before Submit: every §1 row and every Results and Discussion section.

Not this skill: wording with no strength question (polish); adding or removing a method
bullet (method-design); doubting a number (integrity-check). A session that finds a strength
problem under another skill closes and this one opens. Contract (`docs/session-contract.md`):
`Stage: write`, `Identity touch: claim-map` or `none`, `Skill invoked: skills/claim-audit.md`.

## 2. Inputs to read
- `identity/claim-map.md`, all sections. §1 is the object; §0, §2, §3 are the boundary.
- `identity/method-trace.md`, method-bullet trace and parameter register, for method anchors.
- `identity/story-spine.md`, promise and anti-pivot guardrails, for 4.8.
- `identity/README.md`, the strength-tier table (hedged / moderate / strong, maximum wording).
- The frozen facts each row cites: `reality/facts/<exp>/<run>.facts.json`;
  `reality/errata.md` for superseded ids.
- `boards/evidence.csv`.
- When prose is in scope: the sections under `manuscript/sections/`, and
  `manuscript/facts-map.yaml` to resolve each `\fact{}` key to a fact id.
- `decisions/ADR-*.md` whose `touches:` names claim-map or a claim in scope.
- Optional: `experiments/<id>/experiment.yaml` `emits[]` when a fact's meaning is unclear;
  the current `python3 tools/check.py` output as the starting list of broken anchors.

## 3. Excluded inputs
- `experiments/*/notes.md` and any code-space output not yet frozen. Notes explain; they never anchor.
- Sections outside the declared scope.
- `%!` working notes in the LaTeX source.
- `tmp/`, chat backups.

## 4. Protocol steps

### 4.1 Sort the sentences
Read the scope one sentence at a time and label each:

| Label | What the sentence does | Audited? |
|-------|------------------------|----------|
| fact | reports a measured or computed value through `\fact{}` | no; a bare numeral is a checker failure, not an audit matter |
| claim | asserts something the facts are meant to support | yes |
| interpretation | offers a reason or mechanism for a result | yes, and must pass 4.7 |

### 4.2 Take each claim apart
Six parts, after Toulmin. Name each; a part that cannot be named is a defect.

| Part | Ask | Defect when |
|------|-----|-------------|
| the assertion | what exactly is said to be so? | the sentence reads two ways |
| the grounds | which frozen fact ids are offered for it? | none, or a `pending` id |
| the licence | why do those facts entitle the authors to this assertion? | the step from facts to assertion cannot be said in one sentence |
| support for the licence | what makes the licence trustworthy here: a reference measurement, a protocol, prior work? | the method's validity is taken for granted |
| the force | how strongly is it asserted? | absolute verbs on a one-study result |
| the exception | what observation would make it false, and is that acknowledged? | no limitation attached |

A claim with grounds but no stateable licence is a report, not an argument.

Linchpin test: imagine each cited fact id absent in turn. If the claim falls when any single
one is absent, record a NOTE in `boards/findings.csv` ("linchpin: <claim id> rests on
<fact id>"); that fact goes through integrity-check before the row may be `strong`.

### 4.3 The per-claim table
One row per claim sentence. An empty cell is fixed in this session.

| Column | Holds | Defect when |
|--------|-------|-------------|
| claim id | the `C<n>` row in §1 | no row: a new claim (propose a row; the human decides; an ADR records) or a smuggled one (cut) |
| tier | hedged / moderate / strong | the verbs exceed the tier's maximum wording |
| fact anchors | ids of the form `EXP-001.r03.name`, frozen, not superseded | an id missing, pending, superseded, or whose `definition` says something other than the sentence |
| method anchor | a method-trace bullet or parameter | no method step produces this result |
| boundary check | not in §2; no §3 limitation contradicted; descriptor qualifiers intact (4.6) | any hit |

Three fixes exist for an empty cell: lower the tier, cut the sentence, or name the missing
fact (an experiment for design-review, or a `boards/human-owed.csv` item).

### 4.4 Epistemic status
Place each claim on the ladder, then read off the tier ceiling.

| Level | Evidence state | Wording that fits | Tier ceiling |
|-------|----------------|-------------------|--------------|
| conjectured | reasoning or analogy; no frozen fact targets it | "we expect", "may" | hedged |
| disputed | frozen facts, or external work, point in different directions | "in this setting ..., whereas ..." | hedged |
| indicated | one experiment, one setting; facts frozen, `checked_by` empty | "indicates", "the data show" | moderate |
| corroborated | more than one experiment, or an independent reference measurement; facts frozen and checked | "demonstrates" | strong; the ceiling for one paper |
| settled | the wider literature agrees; this paper is one voice among several | plain present tense | strong; background, rarely a contribution |

Default for a one-site, one-period, or small-n study: `indicated`. Settled wording on an
indicated claim is the most common first-draft defect; lower it on sight.

### 4.5 Evidence status check
Two columns of `boards/evidence.csv` bound the tier:

| `status` | `checked_by` | Tier ceiling |
|----------|--------------|--------------|
| pending | any | hedged |
| partial | any | moderate |
| frozen | empty | moderate; open integrity-check to go higher |
| frozen | an integrity-check verdict | strong permitted |

Then open every cited facts file and read `definition`, `n`, `unit`. The anchor must mean
what the sentence means: same quantity, same sample, same window. `tools/check.py` catches
an id that is not frozen; only a reader catches one that is frozen but says something else.

### 4.6 Derived and relative descriptors (permanent rule)
A derived descriptor is a quantity the method computes in place of one it does not measure:
an extent seen from one viewpoint standing for a surface, an orientation fitted to a point
set, an ordinal index, a ratio of two estimates. For each one, at every tier: the qualifier
stays in the sentence ("relative", "approximate", "as a proxy for", "within-unit over
time") and raising the tier never removes it; it is never reported as an absolute value of
the thing it stands for; it is never compared across sites, instruments, or studies as if
calibrated. The project's descriptor list lives in claim-map §0 or §3; if none exists, the
first audit proposes one and the human decides. A violation is fixed in the session.

### 4.7 Discussion: at least one rival explanation
For every interpretation sentence:
1. Write down the authors' explanation and at least two others that could produce the same
   frozen facts. Rivals to try first: measurement noise accumulated across the window; a
   selection or design artefact that removed the hard cases; a confound from acquisition
   timing or order.
2. For each, note how much of the facts it accounts for, how many extra assumptions it
   needs, and what new observation would tell it apart from the others.
3. The Discussion must name the two strongest rivals in the text, even where it ends by
   preferring the original. One explanation, however well argued, is a MAJOR finding.

### 4.8 Cross-claim consistency
- A downstream claim's tier is capped by the tier of every upstream claim it depends on.
- Results is the ceiling: a Discussion sentence carries no claim above its Results tier.
- Abstract, Results, Discussion, and Conclusion state the same claim at the same tier.
- No claim exceeds the story-spine promise or trips an anti-pivot guardrail.
- The `sensitivity` column names the experiments the fact anchors come from.

### 4.9 Write back
- Update §1 rows: tier, fact anchors, method anchor. A tier that follows mechanically from
  4.5 needs no ADR. A new row, a new §2 or §3 entry, or a tier above what 4.5 permits needs
  the human's yes in conversation and an ADR, this session.
- Mirror to `boards/evidence.csv`: `claim_id`, `fact_ids`, `status`, `last_updated`. Never
  write `checked_by`; only integrity-check does.
- Every defect is a `boards/findings.csv` row with `source: claim-audit`. Severity: boundary
  violation BLOCKER (fixed now); overclaim or stale anchor MAJOR; single-explanation
  Discussion MAJOR; cross-section mismatch MINOR; linchpin NOTE.
- A missing fact becomes a `boards/human-owed.csv` item or a named experiment.
- Run `python3 tools/check.py`.

## 5. Anti-patterns
- **Strength creep.** Discussion says "demonstrates" over pending evidence. Fix: "suggests".
- **Smuggled disallowed claim.** A §2 claim returns as an adjective ("complete", "fully
  automatic", "general") instead of a sentence. Fix: cut or rewrite; the §2 row stays.
- **Descriptor as absolute.** The proxy is named as the thing it stands for. Fix: restore
  the qualifier; a boundary violation, not a style choice.
- **Anchor by id without reading the definition.** The `\fact{}` resolves, so the sentence
  passes, but the fact is a different quantity, sample, or window. Fix: 4.5, every time.
- **Silent upgrade.** New facts land and a tier rises in claim-map without a
  new-evidence-integration session. Fix: path first, row second.
- **Preliminary described as established.** Settled wording ("proves", "establishes") on an
  indicated claim. Fix: 4.4; moderate is the default ceiling.
- **Single-explanation Discussion.** One cause offered, none weighed against it. Fix: 4.7.
- **Cross-section mismatch.** Results hedges, Discussion asserts. Fix: Results is the ceiling.
- **Passing the audit by widening the allowlist.** A numeral pattern added to
  `manuscript/facts-map.yaml` so a hand-typed number stops failing. That is invariant I3.

## 6. Closing condition
- Every claim-map §1 row in scope has all five columns filled, and `python3 tools/check.py`
  passes (anchors, boards, cross-ref).
- Every row at tier `strong` has `status: frozen` and a non-empty `checked_by` in
  `boards/evidence.csv`.
- Every tier change this session is visible in `boards/evidence.csv` `last_updated`; every
  boundary change (new row, §2, §3) has an ADR dated this session.
- Every defect found is a `boards/findings.csv` row (`source: claim-audit`); no BLOCKER open.
- Every missing fact is a `boards/human-owed.csv` item or an experiment id named in a finding.
- The contract's `Identity touch` was `claim-map` or `none`; no other identity file changed.
