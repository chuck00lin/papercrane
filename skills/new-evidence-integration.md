---
name: new-evidence-integration
version: 0.1
ported_from: "Paper3 skills/batch2-integration.md v1.0"
---

# new-evidence-integration

Frozen facts from a new experiment have arrived for a claim that already has a row. Decide,
one finding at a time, how they enter the paper. Sits between **Analyze** and **Write**;
the human's **Interpret** decision, recorded as an ADR, gates every path that changes what
a claim says. Owned by head; the experiment agent hands over at freeze.

## 1. When to invoke

- An experiment reaches `status: frozen` and one or more of its targeted claims already
  has a row in `identity/claim-map.md` §1.
- A frozen fact appears to disagree with an existing claim, or with an earlier
  experiment's facts for the same claim.
- The human asks "does finding X go in the paper?"
- Before any sentence of the form "because the new experiment shows ..., we will ...".

Not this skill: the first claim row from a first experiment (`claim-audit`, after
`design-review` and `experiment-loop`); a method detail the new run suggested
(`method-design`, after this skill has placed the finding); the narrative consequences
(`story-design`, after a path C or D decision).

Hard rule: no file in `identity/` changes on the strength of a fact that is not in
`reality/facts/` with a line in `reality/index.csv`. Session contract: `Stage:
interpret`, `Experiment: <id>`, `Identity touch:` by path (A to D touch claim-map or
more; E touches nothing).

## 2. Inputs to read

Authoritative:
- `reality/facts/<exp>/*.facts.json` for the new experiment, `reality/index.csv`,
  `reality/errata.md`.
- `experiments/<id>/experiment.yaml`: what the experiment was pre-registered to target.
- `identity/claim-map.md` §1 (rows, tiers, fact anchors, sensitivity column), §2, §3.
- `identity/story-spine.md` §5 (arc) and §8 (guardrails); `identity/method-trace.md` §3
  (results narrative).
- `boards/evidence.csv`.
- `decisions/ADR-*.md` naming this experiment: the Interpret ADR written after the
  `experiment-loop` report, and the role ADR (what this experiment is for the paper; step 2)
  if it exists.

Task-scoped, optional: `experiments/<id>/notes.md`, at step 1 only, to locate what the
experiment agent flagged as surprising. Never as evidence.

## 3. Excluded inputs

- `manuscript/sections/*.tex`. Existing prose bends the path choice toward "where does
  this paragraph go"; integration is upstream of prose.
- Code-space outputs, CSVs, and any figure whose numbers differ from the frozen facts.
- Other experiments' notes; `tmp/`; chat backups.

## 4. Protocol steps

1. **Locate the finding.** One sentence: the fact ids; the existing claim row(s) they bear
   on; what the pre-registered target said. If any fact is not frozen, stop and hand back
   to `experiment-loop`. If the finding concerns a claim the experiment did not target,
   mark it `unplanned`: an unplanned finding may take paths A, C, or E, never B. A
   stronger claim needs a pre-registered confirmatory experiment (`design-review`).

2. **Check for the role ADR.** Does an ADR state what this experiment is for this paper:
   replication, extension, substitution of the primary evidence, or a pivot? If none
   exists, this is the Interpret stage: lay out the alternatives with the facts beside
   them, in conversation, and stop. The human decides; the agent drafts the ADR
   (`experiment: <id>`, `facts:` the ids); the human says yes; the file is written. Paths
   A and E may proceed without a role ADR because they do not change what any claim says.
   Paths B, C, and D wait for it.

3. **Choose exactly one close path.**

   ```
   Does the finding agree with the existing evidence for the claim?
   ├─ yes → does it support the same statement, or a stronger one?
   │        ├─ same     → A (add evidence)
   │        └─ stronger → B (strengthen), if the role ADR allows and pre-conditions hold
   └─ no  → does the claim hold under some conditions and not others?
            ├─ yes → C (narrow): the statement gains a boundary condition
            └─ no  → is the finding in this paper's scope (story-spine §8)?
                     ├─ yes → does it change only how an existing result is shown? → D
                     │        otherwise → C or E, decided by the human
                     └─ no  → E (justified decline)
   ```

4. **The five close paths.**

   | path | trigger | action | pre-conditions | downstream |
   |------|---------|--------|----------------|------------|
   | A add evidence | the new facts replicate or confirm the existing statement | fact ids appended to the claim row's anchors; wording unchanged; `boards/evidence.csv` row gains the ids | facts frozen | `polish`, only if prose states an evidence count |
   | B strengthen | the new facts support a higher tier (`hedged` to `moderate` to `strong`) | tier changes per the table in `identity/README.md`; manuscript wording follows | role ADR exists and permits it; sensitivity column is not single-experiment; every targeted fact frozen; `integrity-check` run on any surprising fact | `claim-audit`, then `polish` |
   | C narrow | the claim fails under a condition the new facts expose | statement gains a boundary condition; a limitation may be added to §3 (never removed); existing anchors stay | an ADR, because the statement changes; existing evidence still stands alone | `claim-audit` |
   | D restructure presentation | an existing figure, table, or subsection should expand to show both experiments | panels, table rows, or an existing subsection expand; method-trace §3 and the figure registry updated | no section moves; results order and arc nodes unchanged; a role ADR | `method-design` or `story-design` |
   | E justified decline | out of scope, a follow-up paper, or not mature | nothing in `identity/` changes; `boards/findings.csv` row with status `declined` naming the ADR | an ADR with the reason, because scope is the human's | none |

5. **Anti-drift cross-check before executing.** Four questions; all must pass.
   - *Standalone.* If this experiment's facts were deleted, is the paper still
     submittable? An action that makes the answer no is invalid.
   - *No assumed outcome.* Does the action depend on a run that is not frozen yet, or on
     a property of the experiment that no fact states? Then wait.
   - *Upgrade, do not rebuild.* Does it move a section, reorder results, change an arc
     node, or change the order in which trust is built across results? Then it is not
     path D; it is a `story-design` or `method-design` session with its own ADR.
   - *Decision gate.* For B, and for any D beyond a panel or a row: the role ADR exists.

6. **Execute one path per finding.** Several findings from one run are several rows, each
   with its own path, in this session or across sessions. Never blend.

7. **Update boards.** `boards/evidence.csv`: fact ids, status, `checked_by`,
   `last_updated` for every touched claim. `boards/findings.csv`: one row per finding,
   source `new-evidence-integration`, summary naming the path, `adr` filled for B, C, D,
   E. `boards/draft.csv`: sections whose `depends_on` includes a changed claim go back to
   `state: drafted`, `polish_passed: no`.

8. **Name the downstream sessions** in conversation (table above). Anything only the human
   can supply goes to `boards/human-owed.csv`.

9. **Check.** `python3 tools/check.py`: freeze, anchors, boards, cross-ref.

Worked example, generic. A second experiment, role ADR "replication on a second cohort",
freezes run r01. Finding 1: its agreement metric for C1 matches the first experiment's;
path A, two fact ids appended, tier unchanged. Finding 2: its error for C2 doubles in the
late part of the observation window; path C, C2 gains "within the first part of the
window", a new limitation row, an ADR, and a claim-audit session named. Finding 3: a
contrast between two groups that nobody pre-registered looks large, and the design had no
control cell for it; path E, findings row `declined`, ADR "follow-up paper". Three rows,
three paths, one session.

## 5. Anti-patterns

- **Skipping the freeze.** Integrating from a code-space CSV, a notebook, or a plot
  because "the number is right." `reality/` is the only source; the rest is observation.
- **Several paths for one finding.** Strengthen and restructure and add evidence at once.
  Each path has its own pre-conditions; the blend cannot be audited. Split the finding.
- **Implicit restructure.** Swapping two results subsections "because it flows better
  now." That is a rebuild, needs an ADR, and is not this skill.
- **Tier upgrade without the role ADR.** The facts look strong, so the tier goes up. Until
  the human has said what the experiment is for, the ceiling is path A.
- **Rewriting the earlier evidence.** The new facts disagree, so the old wording or the
  old numbers are quietly adjusted. Frozen facts do not move; a disagreement is a finding
  (C or E), and a discovered bug is a new run plus an errata line.
- **Forgetting E.** Every finding forced into the paper dilutes it and widens the attack
  surface. Decline is legitimate and common.
- **Assuming the outcome.** Prose, story, or figure layouts prepared for the experiment
  before its facts froze; existing framing weakened "to make room."
- **Existing evidence no longer standing alone.** After the action, removing the new
  experiment would leave a claim without anchors.
- **Treating an unplanned finding as pre-registered.** It can narrow or be declined; it
  cannot strengthen.
- **Choosing the path from the manuscript.** "Where would this paragraph go" is a Write
  question. The path is chosen from facts and claims.

## 6. Closing condition

Every finding named in the session contract has a `boards/findings.csv` row with source
`new-evidence-integration` whose summary names its path and whose `adr` column is filled
for paths B, C, D, and E; `boards/evidence.csv` is updated for every touched claim; no
tier in `identity/claim-map.md` changed without an ADR dated this session that names the
experiment; no manuscript section moved; `python3 tools/check.py` passes; downstream
sessions are named in conversation and human-supplied inputs are rows in
`boards/human-owed.csv`.
