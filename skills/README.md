# skills/

Collaboration protocols. Each skill is one working mode: when to start it, what to read,
what not to read, the steps, the known failure patterns, and when the session is done.
Skills are stable; they change rarely and carry a change log.

## Structure (every skill)

```
1. When to invoke
2. Inputs to read
3. Excluded inputs
4. Protocol steps
5. Anti-patterns
6. Closing condition   (externally checkable; usually names a tools/check.py result, a board row, or an ADR)
```

## Reading order

| Read first | Then | When you need them |
|------------|------|--------------------|
| `design-review` · `experiment-loop` · `claim-audit` | `story-design` · `method-design` · `polish` | `shadow-reviewer` · `integrity-check` · `cold-review` · `venue-calibration` · `new-evidence-integration` |

Three skills carry the loop; the rest are reached from a stage or a finding.

## Router (by lifecycle stage)

| Stage | Lead | Skill | What it governs |
|-------|------|-------|-----------------|
| ● Idea | human | `story-design.md` | Socratic story work; alternatives; promotion to story-spine after the human decides |
| ● Design | human | `design-review.md` | pre-registration of a design contract against the claim map |
| Build | agent | `method-design.md` | method bullets, silent-vs-mention, method figures, parameter trace |
| Run, Analyze | agent | `experiment-loop.md` | dispatch, run records, freeze, plots, the Interpret report |
| ● Interpret | human | `new-evidence-integration.md` | what to do when frozen facts land on an existing claim: add, strengthen, narrow, restructure, decline |
| Write | agent | `claim-audit.md` | every claim sentence traced to fact ids and a tier |
| Write | agent | `venue-calibration.md` | venue norms from an exemplar corpus, before drafting for a new venue |
| Write | agent | `polish.md` | stance, strength, terminology, style; runs last |
| Review | agent | `shadow-reviewer.md` | in-house adversarial review with anti-sycophancy rules |
| Review | agent | `integrity-check.md` | seven failure modes of AI-assisted research; also before Submit |
| Review | agent + cold model | `cold-review.md` | different model, PDF only, no workspace context; synthesis and go/no-go |

Drafting and rendering inside Write have no skill; they are governed by the session contract
and `tools/check.py`. Submit is a checklist in `docs/design.md` §2.

## Meta anti-patterns

- Replacing a skill reference with conversational instruction. It will need repeating.
- Writing working notes into a skill.
- Invoking several skills in one session and blending them. One primary skill per session.
- Running a human-led stage's skill to completion without a human decision in the
  conversation. The skill ends at a proposal; the ADR ends the stage.
