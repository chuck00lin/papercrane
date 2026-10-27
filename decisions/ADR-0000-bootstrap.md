---
id: ADR-0000
date: 2026-10-27
status: accepted
supersedes: none
experiment: none
facts: []
touches: [whole repository]
---

**Decision.** Start a second-generation research workspace, `papercrane`, as a clean
repository rather than refactoring the first-generation paper repo in place.

**Alternatives rejected.** Refactor the live paper repo (risks the submission in flight).
Publish the first generation as-is with a lessons page (ships the known defects).

**Why.** The audit in `docs/lessons-learned.md` shows the defects are structural
(hand-copied numbers, design outside the loop, prose facts); fixing them means new layers
and a checker, which is a new template, not a patch.
