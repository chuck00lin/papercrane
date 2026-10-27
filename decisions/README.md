# decisions/

Human decisions, written so the agent can cite them. ADR = architecture decision record,
borrowed from software practice. Three lines minimum, ten maximum.

```
decisions/
├── ADR-0001-<slug>.md
├── scenarios/            temporary governance with an expiry trigger (see docs/design.md §10)
└── TEMPLATE.md
```

Rules: append-only (a reversed decision is a new ADR with `supersedes:`); every ADR names the
experiment and fact ids it rests on when there are any; the agent drafts, the human approves
in conversation before the file is written.

Chat transcripts are not decisions. If a decision was made in conversation and no ADR
exists at session end, the decision does not exist (invariant I6).
