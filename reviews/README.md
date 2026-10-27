# reviews/

Review artifacts. Nothing here is cited by `identity/` or `manuscript/`; findings that
matter are mirrored as rows in `boards/findings.csv` with a severity and an owner.

```
reviews/
├── <date>-shadow-review.md      in-house adversarial review synthesis (skills/shadow-reviewer.md)
├── <date>-cold-review.md        different model, PDF only, no workspace context (skills/cold-review.md)
├── <date>-integrity-check.md    seven-failure-mode sweep (skills/integrity-check.md)
├── review-lenses.md             human-owned: reviewer lenses, trap catalog, calibration questions (fill to taste)
├── reserve.md                   reviewer reserve: facts that support no claim, held for reactive disclosure
└── venue/<venue>/
    ├── corpus.md                exemplar registry: candidates, similarity scores, read status
    └── <exemplar>.md            per-exemplar dissections feeding identity/venue-calibration.md
```

`reserve.md` is the disclosure-economy mechanism: a true fact the paper does not need is not
volunteered; it is parked here with the question it would answer, so a reviewer's request can
be met in a day.
