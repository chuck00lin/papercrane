---
name: experiment-loop
version: 0.1
---

# experiment-loop

Run, freeze, plot, and hand the human the Interpret stage. Owned by the experiment agent.

## 1. When to invoke
An experiment with `status: designed` or `running` needs a run, or a code space reports a
finished run, or the human asks to see results.

## 2. Inputs to read
The experiment's `experiment.yaml`, its `runs/`, the code space YAML, `reality/index.csv`,
`manuscript/labels.yaml` (for figure labels only).

## 3. Excluded inputs
`identity/` beyond claim ids, `manuscript/` prose, `tmp/`.

## 4. Protocol steps
1. **Dispatch.** Create `runs/<run_id>/run.yaml` with `started`, the exact command, the code
   commit (query the code space), and input hashes. If an agent lives in the code space, the
   dispatch message ends with the literal reply command. Use only pre-approved command
   patterns for long runs.
2. **Collect.** Completion is an event addressed to `experiment` in the bus log, or the
   command's exit. Fill `ended`, `exit_status`. Non-zero exit: record, do not freeze, report.
3. **Freeze.** Validate `facts.json`. Reject on missing provenance or an id collision with
   `reality/index.csv`. Copy, hash, index. If any fact has `supersedes`, append the errata
   line in the same step.
4. **Figures.** If the code space emitted figures for the run, copy them under
   `runs/<run>/figures/` and list them in the report. Labels come from `labels.yaml`,
   read by the code space's plotting code; no label is typed in a script.
5. **Report for Interpret.** One message to the human: experiment id, run id, the facts
   (name, value, n), the plots, and anything that surprised the agent, worded as a
   question. Never as a conclusion.
6. **Record the verdict.** The human's response becomes an ADR (draft it, get a yes, write
   it). If the verdict is "run again with X", loop to step 1 with a new run id. If the
   targeted claims now have frozen facts, set `status: frozen` and open a claim-audit
   session.

## 5. Anti-patterns
- Freezing output that the code space produced without provenance "because the number is
  right".
- Editing a frozen facts file to fix a typo. Run again.
- Keeping a figure whose numbers differ from the frozen facts of the same run.
- Writing an interpretation into the Interpret report. Surprises are questions.
- Letting the run record's `code_commit` be "latest".

## 6. Closing condition
Every run in `runs/` has a complete record; every frozen file is in `reality/index.csv`
with a matching hash; the human's verdict for the latest run exists as an ADR or the run is
marked for re-run.
