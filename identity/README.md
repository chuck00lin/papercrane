# identity/

What the paper *is*. Three files plus a terminology table. Read all of them at the start of
every substantive session; each should take under five minutes.

| File | Axis | Owner |
|------|------|-------|
| `story-spine.md` | narrative: reader, gap, positioning, promise, arc, RQs, discussion arc, anti-pivot guardrails | **human** |
| `claim-map.md` | claims: allowed (with fact anchors and strength tier), disallowed, limitations, boundary statements | human for boundary; head agent for rows under contract |
| `method-trace.md` | method: pipeline backbone, section narrative, method-bullet trace, parameter register (fact refs only) | head agent under contract |
| `terminology.csv` | canonical term, forbidden variants, scope | human + agent |
| `venue-calibration.md` | venue norms from an exemplar corpus: permission space, constraint space, highlight playbook, forbidden moves | agent (venue-calibration skill); stale after six months |

## Consistency (checked by `tools/check.py`, not by ceremony)

- Every claim the story-spine makes has a row in claim-map.
- Every claim-map row has a method anchor and either frozen fact ids or an explicit `pending` tier.
- Every parameter in method-trace is a fact id, not a literal.
- Disallowed claims and limitations only grow. A deletion is a check failure unless an ADR
  with `touches: [claim-map disallowed]` exists for it.

## Strength tiers

| Tier | Evidence state | Maximum wording |
|------|----------------|-----------------|
| hedged | targeted facts pending | suggests, is consistent with, appears |
| moderate | some facts frozen | shows, indicates, the data show |
| strong | all targeted facts frozen and checked | demonstrates, establishes |

Derived or relative descriptors keep their qualifier at every tier.
