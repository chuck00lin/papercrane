# Session contract (8 lines)

Every substantive session opens with this block. It is the agent's declaration of scope and
the human's one-glance check that the agent is about to do the right kind of work.

```text
Stage:                 [idea | design | build | run | analyze | interpret | write | review | submit]
Experiment:            <experiment id, or none>
Target:                <one deliverable, verifiable>
Authoritative inputs:  <explicit file list>
Excluded inputs:       <explicit file list; tmp/ and chat backups by default>
Identity touch:        [story-spine | claim-map | method-trace | venue-calibration | terminology | style-words | none]
Skill invoked:         <skills/<name>.md, or none for draft/render>
Closing condition:     <an externally checkable sentence, usually "tools/check.py passes and X exists">
```

## Field notes

- **Stage** names one of the nine lifecycle stages (`docs/design.md` §2). The skill, not the
  stage, says what the agent will do; the stage says who leads.
- **Human-led stages** (`idea`, `design`, `interpret`): the closing condition must name the
  ADR that will record the human's decision, for example "ADR-0012 written after the human
  chooses between the two framings proposed". Nothing in `identity/` or `decisions/` changes
  before that decision is made in conversation.
- **Experiment** is required for `design`, `build`, `run`, `analyze`, `interpret`, and for any
  session that reads or writes `experiments/` or `reality/`.
- **Identity touch = none** means `identity/` is byte-identical at session end.
- **Closing condition** must be something a second agent could verify without reading the
  conversation.

## Why a contract and not a prompt

The contract is the only artifact that survives the conversation. The first-generation
framework found that undeclared sessions drifted in two ways: reading material that should
have been excluded, and making decisions that were never persisted. Both are visible in the
contract before any file is touched.
