# bus/

File-queue transport between agents (`docs/design.md` §8). `events.ndjson` is the append-only
log; `queue/<agent>/*.json` are pending messages; `queue/<agent>/done/` holds acknowledged
ones. Use `python3 tools/bus.py` (send / poll / ack / tail / wait). Message files and the
log are workspace state and are committed; a code space with a resident agent polls its own
queue directory.
