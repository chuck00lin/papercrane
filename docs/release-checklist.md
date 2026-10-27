# Release checklist

What stands between this repository and a public release. Status as of 2026-10-27 (evening).
`decision` means the owner has to choose; `todo` is work; `done` is verified.

## Gate (all closed 2026-10-27)

| # | Item | Status |
|---|------|--------|
| 1 | Skills carry concepts only; zero shared 8-grams against every credited source (`tools/dev/overlap_check.py`) | done 2026-10-27: 0 shared 8-grams over skills, docs, identity, reviews, README |
| 2 | No content from the author's own papers in the tree: terminology rows, toy values, cohort counts, repo names | done 2026-10-27 |
| 3 | **Publish from a fresh history.** The working history (pre-rewrite skill text, pre-scrub examples) is archived as a git bundle beside the repo; the repo itself now starts at a single commit tagged v0.1.0. | done |
| 4 | `LICENSE`: MIT | done |
| 5 | `ATTRIBUTION.md` current; ARS credited for ideas only | done |
| 6 | Timing: no text from the author's papers is in the tree, so the release does not wait for a submission decision | done |
| 7 | Name: papercrane (PyPI free; no notable GitHub repo of that name) | done |

## Before first users (v0.1.0)

| # | Item | Status |
|---|------|--------|
| 8 | `examples/toy-pipeline/`, `make demo`, `make pdf` (article-class shell compiles with the rendered sentence) | done |
| 9 | `tests/test_loop.py` (7 tests over the toy loop) and `.github/workflows/check.yml` | done |
| 10 | `docs/quickstart.md`: toy loop, attach your code, write the identity and first contract, mount skills | done |
| 11 | Skills reading order in README and `skills/README.md` | done |
| 12 | `tools/mount-skills.py` and `docs/agent-runtimes.md` | done |
| 13 | Plot specs cut; figures are code-space outputs registered in `manuscript/figures.yaml` with run, fact ids and sha256 | done |
| 14 | `CITATION.cff`, `CONTRIBUTING.md`, `CHANGELOG.md`, tag `v0.1.0` | done |
| 15 | `README.zh-TW.md` synced with the rebuilt English README | done |

## Next iteration (v0.2)

| # | Item |
|---|------|
| 16 | Bus transport with a resident code-space agent on real work |
| 17 | `cold-review` and `claim-audit` run end to end once; promote frozen facts to a claim row |
| 18 | Claims as YAML with the markdown generated, so the checker stops parsing tables |
| 19 | A written retrospective: what the third paper's framework got wrong and how v2 answers it |
| 20 | Read-only web view over the same files (render preview with provenance; experiment registry) |

## The claim the release must not make

That the framework works from day one. It was derived after the fact from one paper in one
lab. The honest statement is the one in the README: a hypothesis the next paper will test.

## Left for the owner

- `git remote add origin git@github.com:chuck00lin/papercrane.git && git push -u origin main --tags` (or create the repository on GitHub first; `gh` is not installed here).
- Open `README.zh-TW.md` in a browser once to confirm the CJK labels in the diagrams render.
- Edit the copyright holder in `LICENSE` and the author in `CITATION.cff` if a real name is preferred over the handle.
