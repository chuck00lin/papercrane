# Quickstart

Thirty minutes from clone to a compiled PDF whose numbers came from a run.

## 1. The toy loop (five minutes)

```bash
git clone https://github.com/chuck00lin/papercrane my-paper && cd my-paper
python3 tools/check.py      # 0 failure(s): the empty workspace validates
make demo                   # two runs on the toy pipeline: dispatch, freeze, render, compare, check
make pdf                    # manuscript/main.pdf; every number in it is a \fact{} macro
make demo-clean             # back to the empty workspace
```

Open `manuscript/main.pdf`. The sentence in it compares two controllers on a simulated track;
its numbers come from `manuscript/facts.tex`, which `tools/render-facts.py` generated from the
two frozen files under `reality/facts/EXP-000-example/`.
Change a value in that frozen file and run `python3 tools/check.py`: the hash check fails.

## 2. Attach your own code (ten minutes)

1. Copy `codespaces/example-pipeline.yaml` to `codespaces/<name>.yaml`; set `path` to your
   repository and `entry.command` to the command that runs one named experiment.
2. In that repository, write an exporter that reads your outputs and writes
   `runs/<run>/facts.json` in the shape of `examples/toy-pipeline/emit.py` (facts with a
   definition, provenance with the commit and the hashes of what it read).
3. `python3 tools/dispatch.py --experiment <id> --run r01 --config default`, then
   `python3 tools/freeze.py <your repo>/runs/r01/facts.json --run experiments/<id>/runs/r01/run.yaml`.

A real attachment is walked through in `worked-example-pipeline.md`.

## 3. Write the identity and the first design contract (fifteen minutes)

1. Idea (human): fill `identity/story-spine.md`. Short. One decision record in `decisions/`
   per directional choice.
2. Design (human, with the agent): copy `experiments/EXP-000-example/experiment.yaml`, name
   the claims it targets, the controls, the reference protocol, and what must be logged on
   acquisition day. The agent runs `skills/design-review.md`; `python3 tools/check.py
   --design <id>` must pass before anything runs.
3. Read three skills: `design-review`, `experiment-loop`, `claim-audit`. The rest wait
   until you need them (`skills/README.md`).

## 4. Mount the skills in your agent runtime

```bash
python3 tools/mount-skills.py     # writes .claude/skills/<name>/SKILL.md wrappers for Claude Code
```

Other runtimes read `AGENTS.md` and `skills/*.md` directly; see `agent-runtimes.md`.
