---
name: design-review
version: 0.1
---

# design-review

Pre-register an experiment against the paper's claim boundary before anything runs.

## 1. When to invoke
A new `experiments/<id>/experiment.yaml` is drafted, or an existing one is redesigned, or
a code space is about to be dispatched for an experiment whose status is still `designed`.

## 2. Inputs to read
`identity/claim-map.md` (all sections), `identity/story-spine.md` §6 and §8, the
experiment's `experiment.yaml`, the target code space's YAML.

## 3. Excluded inputs
`manuscript/`, `tmp/`, other experiments' notes.

## 4. Protocol steps
1. **Target check.** For each `targets[].claim`: does the id exist in claim-map §1? Is it in
   §2 disallowed? A disallowed target stops the review; the human rewrites the question.
2. **Evidence sufficiency.** For each target, name the `emits[]` entry that would support it.
   A target with no emitted fact is a gap: add the fact or drop the target.
3. **Contrast check.** If any target is comparative (A vs B, treatment vs control, better
   than), `design.controls` must contain a control for that contrast and `design.n` must
   be per cell. An incomplete factorial or a row-confounded contrast is recorded as a
   candidate disallowed claim now, not after acquisition.
4. **Reference independence.** `reference_protocol` must say who measures, how, and that
   they do not see pipeline output first. If it cannot, record the limitation now.
5. **Acquisition log completeness.** Walk `acquisition_log`. Ask: if this item is missing in
   six months, which manuscript sentence cannot be written? Add anything the human names.
6. **Write back.** Propose, in conversation, any new disallowed claim or limitation. On the
   human's yes, add it to claim-map §2 or §3 and write an ADR. Set `status: designed` and
   record the review date in `notes.md`.

## 5. Anti-patterns
- Reviewing the design after the data exist and calling it pre-registration.
- Accepting "we will see what the data show" as a target.
- Letting a comparative question through without a control because the comparison "is
  only descriptive". Descriptive comparisons become claims under reviewer pressure.
- Treating the acquisition log as optional metadata. It is the list of facts that cannot be
  recovered later.

## 6. Closing condition
`tools/check.py --design <exp>` passes; every new disallowed claim or limitation has an ADR;
the human has said yes to the design in this conversation.
