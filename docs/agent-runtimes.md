# Agent runtimes

The workspace is files plus a checker. Any agent that can read Markdown and run Python can
work in it; what differs between runtimes is how the skills get invoked.

| Runtime | Invariants | Skills | Notes |
|---------|------------|--------|-------|
| Claude Code | `CLAUDE.md` is read automatically | `python3 tools/mount-skills.py` generates `.claude/skills/<name>/SKILL.md` wrappers, so `/design-review` and friends appear as slash commands; each wrapper tells the agent to read and follow `skills/<name>.md` | re-run after adding a skill |
| Codex CLI and others that read `AGENTS.md` | `AGENTS.md` (same content as `CLAUDE.md`) | the agent reads `skills/README.md` and opens the file named in the session contract | no generated wrappers needed |
| A plain chat model | paste `CLAUDE.md` and the skill at the start of the session | manual | the checker still enforces the invariants on the files |

A code space with a resident agent of any runtime takes part through the file-queue bus
(`docs/design.md` §8): it polls `bus/queue/<its name>/`, runs the command in the message, and
acknowledges with `python3 tools/bus.py ack`.
