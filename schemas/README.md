# schemas/

JSON Schema (draft 2020-12) for every machine-read file in the workspace.

| Schema | Validates |
|--------|-----------|
| `experiment.schema.json` | `experiments/<id>/experiment.yaml` (design contract) |
| `run.schema.json` | `experiments/<id>/runs/<run>/run.yaml` |
| `facts.schema.json` | `reality/facts/<exp>/<run>.facts.json` and the `facts.json` a code space emits |
| `codespace.schema.json` | `codespaces/<name>.yaml` |

Board CSV columns and limits are declared in `boards/README.md` and enforced by `tools/check.py`.
