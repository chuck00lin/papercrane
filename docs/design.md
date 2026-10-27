# Design — papercrane v0

## 0. Why this exists

The pain this workspace addresses: co-developing research with an agent is hard because the
two of you must align on abstract concepts and dive into concrete detail at the same time,
stay rigorous throughout, and still keep both the work and the content flexible. The
position taken here is that a journal paper can be run the way a software project is run:
the identity files are the spec, experiments are builds, frozen facts are artifacts, the
manuscript is a release, and a checker tells you what broke. The practice that proved itself
in the first generation was managing many experiment variants in the compute repository with
numbered records, variant tags, a benchmark table with a schema, and a leaderboard. This
workspace connects that practice to the data and figure analysis record, so that when a new
experiment lands, every sentence, figure, and claim that must change is found by a tool, not
by memory.

A paper is the last render of a research process that starts months earlier with a design
decision and a first run. Most agent-assisted writing tools enter at the end, when the
numbers already exist as loose CSVs and the story already lives in someone's head. This
workspace enters on day one. It is the folder the researcher opens first, and it stays the
single place where experiments, facts, decisions, and the manuscript meet.

## 1. Principles

| # | Principle | Consequence |
|---|-----------|-------------|
| P1 | Human owns the story | `identity/story-spine.md` and `decisions/` are human-authored. The agent proposes alternatives in conversation, never writes a decision it was not given. |
| P2 | Agent owns the process | Bookkeeping, dispatch, freeze, plot, check, review, draft. Governed by `skills/`, not by memory. |
| P3 | Manuscript is a render | Numbers, tables, figures, parameter registers come from `reality/`. Prose is human source compiled by the agent. |
| P4 | External code becomes operable | Every repo that produces evidence is attached as a code space with the adapter contract (§5). |
| P5 | Immutable facts, mutable interpretation | `reality/` never changes after freeze; `identity/` changes under contract. |
| P6 | Checks over ceremony | Consistency is a program, not a ritual. |
| P7 | Minimal speculative governance | Scenario documents carry an expiry trigger and get archived. |

## 2. Lifecycle

Nine stages. Three are **human-led** (●). In a human-led stage the agent may ask, propose
alternatives, and map consequences in conversation, but it writes nothing to `identity/` or
`decisions/` until the human has decided; the decision is recorded as an ADR in the same
session. The other six are agent-led and governed by skills and the checker.

```
 ● Idea ─▶ ● Design ─▶ Build ─▶ Run ─▶ Analyze ─▶ ● Interpret ─▶ Write ─▶ Review ─▶ Submit
    ▲          ▲                                       │  │          ▲  ▲          │
    │          └──────────────── next run ─────────────┘  │          │  └─ refine ─┘
    └───────────────────────── new idea ──────────────────┘          │
    └───────────────────── the story's imagery ──────────────────────┘
```

**● Idea.** The human writes `identity/story-spine.md`: reader, gap, positioning, promise,
narrative arc, research questions, discussion arc, anti-pivot guardrails. The agent is
Socratic here: it asks what the reader must be able to do afterwards, offers two or three
alternative framings, and maps what evidence each would require. Each directional choice
becomes an ADR. Analysis results loop back to this stage when they change what the paper is
about, and that loop is a human decision, never an agent's.

**● Design.** Human and agent write `experiments/<id>/experiment.yaml`: the question, the
claims it targets (by claim id), the variables, controls, sample plan, reference-measurement
protocol, the facts it must emit, and the metadata that must be logged at acquisition time.
The agent runs the design-review skill: does any targeted claim sit in the disallowed list?
Does every targeted claim have a fact that would support it? Is there a control for every
contrast the claim needs? A design that fails is revised before anything runs. The intent is
the human's; the completeness check is the agent's.

**Build.** Agent-led method and code development inside a code space: the method itself, the
analysis script, the facts exporter, the figure export. External development agents live here.
The stage ends when the code space satisfies the adapter contract (§5) and a run can be
dispatched. Method bullets that will appear in the paper are traced in
`identity/method-trace.md` by the method-design skill.

**Run.** The experiment agent dispatches a run to a code space. The run record
(`runs/<run-id>/run.yaml`) captures the code space, the command, the code commit, input
hashes, the environment, start and end time, exit status. Raw outputs stay in the code space;
only facts cross into the workspace.

**Analyze.** The code space emits `facts.json` (schema in `schemas/facts.schema.json`). The
experiment agent validates it, computes its hash, copies it to
`reality/facts/<exp>/<run-id>.facts.json`, and appends a line to `reality/index.csv`. From
this moment the file is immutable; a later correction is a new run plus a line in
`reality/errata.md`. Figures the code space emitted for the run are copied under
`runs/<run>/figures/`. The agent hands the human a report of facts, figures, and anything
that surprised it, phrased as questions, never as conclusions.

**● Interpret.** The human reads the analysis and decides what it means and what comes next:
another run, a redesign, a claim to audit, a narrowed boundary, or a new idea. The verdict
becomes an ADR (decision, alternatives rejected, reason; three to ten lines) that names the
experiment and the fact ids it rests on. When the targeted claims have frozen facts, the
experiment's status becomes `frozen` and a claim-audit session opens.

**Write.** Two inputs: the story's imagery from Idea (what the reader should see) and the
data from Interpret (what the facts say). The claim-audit skill writes or updates rows in
`identity/claim-map.md` with fact ids as anchors and a strength tier derived from evidence
status; `boards/evidence.csv` mirrors it. `tools/render-facts.py` compiles
`manuscript/facts-map.yaml` into `manuscript/facts.tex`; `manuscript/figures.yaml` names, for
each figure, the run it came from, the fact ids it depends on, and the file's hash. Human-authored prose uses `\fact{...}` and `\ref{fig:...}`; a bare
numeral fails `make check`. Polish runs last.

**Review.** Shadow review (in-house, with concession tracking), integrity check (seven
failure modes), and a **cold review** by a different model given only the rendered PDF and
the venue's reviewer guidelines. Findings land in `boards/findings.csv` with severity; the
synthesis lives in `reviews/`. The human adjudicates; accepted findings loop back into
Write as refinements.

**Submit.** Gated on: `tools/check.py` green, no open BLOCKER finding, `boards/human-owed.csv`
empty.

Three loops: Interpret to Design (next run), Interpret or Analyze to Idea (new idea, human
decision), Review to Write (refine).

## 3. Layers

| Folder | Authority | Who writes | Immutable? |
|--------|-----------|-----------|------------|
| `identity/` | highest, for what the paper *is* | human (story, boundary); head agent under contract (method trace, claim rows) | no, versioned |
| `experiments/` | what was tried | experiment agent; human for the design contract and notes | run records yes; contract versioned |
| `codespaces/` | how to reach external code | human + experiment agent | no |
| `reality/` | what was observed | experiment agent (freeze step only) | **yes** |
| `boards/` | current status | agents | no, regenerated |
| `decisions/` | why | human | append-only |
| `reviews/` | what reviewers said | agents (review skills); human for reserve decisions | syntheses append-only |
| `skills/` | how we work | human + agent, rarely | no |
| `manuscript/` | the render | head agent; human prose | generated parts regenerated |
| `schemas/`, `tools/` | the machine | agent | no |

Dependency direction: `manuscript` depends on `identity` and `reality`; `identity` depends
on `reality` and `decisions`; `reality` depends on `experiments` and `codespaces`; nothing
depends on `manuscript`. The checker fails on any reverse edge (for example, a fact file that
cites a manuscript section).

## 4. Identity (three files, human-owned at the top)

Carried over from the first generation with the schemas tightened:

- `story-spine.md`: reader, gap, positioning, promise, narrative arc, research questions,
  discussion arc, anti-pivot guardrails. Short. The human writes it; the agent may only
  propose edits in conversation.
- `claim-map.md`: allowed claims (id, statement, strength tier, fact anchors, method
  anchor, batch sensitivity), disallowed claims, limitations, canonical boundary statements.
  Disallowed and limitations are never weakened.
- `method-trace.md`: pipeline backbone, section narrative, method-bullet trace (silent vs
  mention), parameter register. Every parameter value is a `\fact{}` reference, not a
  literal.
- `terminology.csv`: canonical term, forbidden variants, scope. Consumed by the checker.

Consistency rules (checked, not ceremonial): every story-spine claim appears in claim-map;
every claim-map row has a method anchor and at least one frozen fact or an explicit
`pending` tier; every method-trace parameter resolves to a fact id.

## 5. Code-space adapter contract

A code space is any external repository or compute location that produces evidence. The
adapter is `codespaces/<name>.yaml`:

```yaml
name: sim-pipeline
path: /home/me/github/sim-pipeline            # or ssh://host/path
kind: pipeline | analysis | plotting | compute
entry:                                        # how the experiment agent invokes a run
  command: "make run EXP={experiment} CFG={config}"
  cwd: .
  env: conda:gaussian-pipeline
emits:
  facts: "runs/{run_id}/facts.json"           # must validate against schemas/facts.schema.json
  plots: "runs/{run_id}/plots/"               # optional; otherwise plots render here from facts
agent:                                        # optional: an agent that lives in the code space
  transport: bus | none
  reply: "squad-send --to experiment --task {task_id}-reply"
provenance:
  code_commit: "git rev-parse HEAD"
  inputs: ["data/{experiment}/**"]            # hashed at run time
```

Obligations of a code space:

1. Accept a named experiment and a config, run deterministically enough to record.
2. Emit `facts.json` with provenance, or fail loudly. Facts without provenance are rejected
   at freeze.
3. If an agent lives there, reply through the bus with the literal command given in the
   dispatch. Printing in its own pane does not count.
4. Keep its own research notes out of claim territory. Claims live only in `identity/`.
5. Hash what it actually read. `provenance.inputs` in the adapter is for a few config files;
   an exporter that reads hundreds of files records their hashes in the facts provenance
   itself, and dispatch does not re-walk the data disk.

A worked attachment of a real pipeline is in `docs/worked-example-pipeline.md`.

This contract is the forcing function: a researcher attaching their code must make it
runnable from a command, make it declare its outputs, and make it record its commit. Those
are reproducibility habits, imposed gently by the loop rather than by a policy document.

## 6. Facts and the render chain

A **fact** is one observed or computed value with provenance:

```json
{
  "id": "EXP-001.r03.lane_rmse_cm",
  "experiment": "EXP-001",
  "run": "r03",
  "name": "lane_rmse_cm",
  "kind": "metric",
  "value": 13.825,
  "unit": "cm",
  "n": 12,
  "definition": "mean over episodes of the per-episode RMSE of lateral error against the lane centre",
  "provenance": {"codespace": "sim-pipeline", "code_commit": "4e8c2c0", "command": "...", "inputs": [{"path": "...", "sha256": "..."}]}
}
```

Kinds: `metric`, `count`, `date`, `interval`, `string`, `table` (value is a path to a CSV
inside the same frozen facts folder). A fact id is `experiment.run.name` and is globally
unique forever. Errata never reuse an id.

**Render chain:**

```
reality/facts/**.json ──▶ manuscript/facts-map.yaml ──▶ tools/render-facts.py ──▶ manuscript/facts.tex
                                                                                   │
experiments/*/runs/*/figures/ ──▶ manuscript/figures.yaml (run, fact ids, sha256) ──▶ figures/ ──┤
                                                                                   ▼
                                               human prose (\fact{}, \ref{}) ──▶ pdflatex ──▶ PDF
```

`facts-map.yaml` is the only place a fact becomes a manuscript number. It declares the display
precision and an optional allowlist of literals that are legitimately typed (section numbers,
equation constants, years). Everything else numeric in prose is a check failure.

## 7. Checks (`tools/check.py`)

| Check | Fails when |
|-------|-----------|
| schema | any `experiment.yaml`, `run.yaml`, `facts.json`, `codespaces/*.yaml`, or board CSV does not validate |
| freeze | a file under `reality/facts/` differs from its hash in `reality/index.csv` |
| anchors | a claim row cites a fact id that does not exist or is not frozen; a method-trace parameter has a literal value |
| design | an experiment targets a claim listed as disallowed, or targets a claim with no fact it emits |
| numerals | a numeric literal in manuscript prose is neither a `\fact{}` nor allowlisted |
| figures | a figure in `figures.yaml` names a missing file, a changed hash, or a fact id that is not frozen |
| terminology | a forbidden term appears in manuscript text or in a figure label file |
| boards | a cell exceeds its length limit; a status value is outside its enum |
| cross-ref | a document references a file, section, or id that no longer exists |
| human-owed | (Submit only) the queue is non-empty |

Each check prints the offending file and line. The checker is the contract between human and
agent: when the human wants a new rule, the first question is which check expresses it.

## 8. Agents and the bus

Three roles (`CLAUDE.md`): head, experiment, code-space agents. Transport is a **file queue**
so that any agent runtime (a terminal agent, a cron job, a human with an editor) can take
part without a shared process:

```
bus/
├── events.ndjson              append-only log: every send, ack, done, reply
└── queue/<agent>/
    ├── <msg-id>.json          one pending message per file
    └── done/<msg-id>.json     acknowledged messages, moved here with their result
```

A message is `{id, ts, from, to, task, kind, payload, reply_to}`. `tools/bus.py` provides
`send`, `poll`, `ack`, `tail`, and `wait` (block until an event addressed to a given agent
for a given task appears in the log). Lessons encoded from the first generation:

- Completion is detected by an event in the append-only log, never by scraping a terminal.
- Every dispatch includes the literal reply command in its payload; an agent that prints its
  result instead of acking has not replied.
- Long runs use pre-approved command patterns from the code-space YAML so permission
  prompts cannot stall silently.
- The head never runs experiments; the experiment agent never edits identity or manuscript.
- A code space whose adapter says `transport: none` is run synchronously by
  `tools/dispatch.py` itself; the bus is only for code spaces with a resident agent.

## 9. Human-led versus agent-led

| Stage | Human | Agent |
|-------|-------|-------|
| ● Idea | story-spine; what the paper promises; every directional choice | Socratic questions; alternative framings; evidence each would need |
| ● Design | question, contrast, controls, reference protocol intent | contract completeness; pre-registration against disallowed claims; acquisition-log prompts |
| Build | approve the method's scope | method and analysis code; facts exporter; figure export; method-trace rows |
| Run | pre-approve command patterns | dispatch; run records; provenance |
| Analyze | nothing until the report arrives | freeze; plots; report phrased as questions |
| ● Interpret | what it means; what next; the ADR | draft the ADR; propose claim rows and tiers |
| Write | choose which numbers to report; interpretation prose | claim audit; render; draft mechanics; polish |
| Review | adjudicate findings; reserve decisions | shadow review; integrity check; cold review orchestration |
| Submit | venue; package sign-off | checks; package assembly; human-owed queue |

The rule that makes the table enforceable: in a ● stage, the agent's output is a proposal in
conversation, and the file is written only after the human's explicit decision, which the ADR
records. `tools/check.py` cannot see conversations, so this one rule stays a discipline; the
session contract's closing condition for a ● stage must name the ADR.

## 10. Scenario documents

Anything that governs a temporary situation (a dataset transition, a pending PI decision, a
revision round) is a file in `decisions/scenarios/` with a `expires_when:` line in its
front matter. The checker warns when the trigger is satisfied and the file is still active.
Archive, do not delete.

## 11. Migration from the first generation

Carried over nearly as-is: identity three-file structure, skills six-section structure,
excluded-inputs field, shadow-review concession tracking, integrity-check seven modes,
disclosure economy, venue calibration, `%!` working-note convention, decision supersedes
chain, errata format.

Replaced: prose facts file with frozen JSON facts; control-index plus five governance files
with `docs/design.md` plus the checker; three hand-edited CSV boards with schema-checked,
partly generated boards; speculative batch-integration taxonomy with the generic
new-evidence-integration skill; tmux manifest with code-space adapters.

Added: design contract and design-review skill; experiment registry and experiment agent;
code-space adapter contract; render chain for numbers; cold external review stage; ADR log;
human-owed queue; terminology as data; file-queue bus.

Imported from the first generation's compute repository, where it worked: numbered experiment
records with a fixed template (goal, hypothesis, change versus baseline, command, results,
wall time); config **variant tags** on every run; a benchmark table with a declared schema; a
leaderboard across runs; a generated index. In v2 these are `experiment.yaml` + `run.yaml`
(`variant`, `baseline_run`, `change_vs_baseline`), facts as the benchmark rows,
`tools/compare.py` as the leaderboard, `tools/status.py` as the index, and `tools/impact.py`
as the piece the compute repo never had: the link from a new run to the manuscript.

## 12. Decisions taken for v0

- **Render stops at numbers, tables, figures, parameter register, and data-derived
  limitation sentences.** Results sentences stay human prose with `\fact{}` inside them, so
  each researcher keeps their own voice. Semi-templated sentences are not offered.
- **Bus transport is a file queue** (§8), not tmux. `tools/dispatch.py` and `tools/bus.py`
  implement it.
- **One workspace serves one paper.** A lab keeps several workspaces; code spaces may be
  shared between them.
- **Documentation is English-first** with a language toggle on the README.

## 13. Interface

Terminal first. The workspace is files plus a checker; every interaction is text inside the
agent's terminal session. Nothing in the lifecycle requires a GUI, and the checker is the
primary feedback surface.

Two surfaces are candidates for a future local web view, read-only, over the same files:

1. **Render preview**: the compiled PDF with per-number provenance. Click a number, see the
   fact id, the run, the code commit, the input hashes.
2. **Experiment registry**: experiments by status, runs, plots, the Interpret report, and the
   ADR that followed.

Rule: a web view reads the same files and never becomes a second source of truth. The
first-generation pipeline repositories already carried their own run dashboards; the
workspace should link to those, not duplicate them.
