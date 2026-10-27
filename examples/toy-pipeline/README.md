# toy-pipeline

A fake code space for the quickstart: a lane-keeping evaluation on a simulated test track.
`data/<experiment>/episodes.csv` holds per-episode logs for two controllers on the same
track and the same seeds; `make run EXP=… RUN=… CFG=<controller>` summarises one controller
into `runs/<run>/facts.json` with provenance. Swap the body of `emit.py` for your own
analysis, in any domain, and keep the shape of the output.
