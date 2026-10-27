# boards/

Small-cell status tables. Machine-read by `tools/check.py`, partly regenerated. A board is a
mirror of state that lives elsewhere; it is never the source of truth.

Hard limit: **no cell longer than 160 characters**. Long explanations belong in an ADR, a
finding file, or `experiments/<id>/notes.md`, referenced by id.

| File | Columns | Enums |
|------|---------|-------|
| `evidence.csv` | claim_id, fact_ids (`;`-separated), status, checked_by, last_updated | status: pending, partial, frozen |
| `findings.csv` | finding_id, source (skill), severity, target (file:line or section), summary, status, adr | severity: BLOCKER, MAJOR, MINOR, NOTE; status: open, resolved, declined |
| `draft.csv` | section_id, state, canonical_file, depends_on (claim ids), polish_passed, last_updated | state: empty, outline, drafted, polished; polish_passed: yes, no |
| `human-owed.csv` | item_id, description, needed_by (stage or date), owner, status | status: open, done |

Decisions are not a board; they are files in `decisions/` and are indexed by `tools/check.py`.

## Conventions the skills rely on

- `evidence.csv.checked_by`: `integrity-check <YYYY-MM-DD>` after a CLEAR verdict; empty while
  unchecked or after INSUFFICIENT / FAIL; `n/a` when the scope rule applies (no manuscript
  sentence or claim tier depends on the row).
- `findings.csv`: a `declined` BLOCKER or MAJOR must carry an ADR id in `adr`. Each
  integrity-check session leaves one NOTE row even when its surprise-language sweep found
  nothing, so the sweep is externally checkable. Skills other than reviews may file rows with
  `source = <skill>` for items they hand to another skill.
- A board row is never the place for the reasoning; it points at the ADR, the finding file in
  `reviews/`, or the experiment notes that hold it.
