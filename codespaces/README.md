# codespaces/

Adapters to the researcher's external repositories, pipelines, plotting scripts, or compute
hosts. One YAML per code space (schema: `schemas/codespace.schema.json`). This folder
replaces the first generation's prose "external repos index" and tmux manifest.

A code space must be able to: run a named experiment from a command, emit `facts.json` with
provenance, and (if an agent lives there) reply through the bus with the literal command it
was given. See `docs/design.md` §5.

Claims never live in a code space. If your pipeline repo keeps research notes, they are
notes; the paper's claims are only in `identity/claim-map.md`.
