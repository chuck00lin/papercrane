#! papercrane helpers
.PHONY: check render freeze status impact demo demo-clean pdf pdf-clean session session-clean

check:
	python3 tools/check.py

render:
	python3 tools/render-facts.py

# usage: make freeze FACTS=/path/to/facts.json [RUN=experiments/EXP-001/runs/r01/run.yaml] [ERRATA="reason"]
freeze:
	python3 tools/freeze.py $(FACTS) $(if $(RUN),--run $(RUN)) $(if $(ERRATA),--errata "$(ERRATA)")

status:
	python3 tools/status.py --write

# usage: make impact RUN=EXP-001-slug.r03 [APPLY=1]
impact:
	python3 tools/impact.py --run $(RUN) $(if $(APPLY),--apply)

# Five-minute demo on the toy pipeline (see README quickstart). `make demo-clean` resets it.
demo:
	python3 tools/dispatch.py --experiment EXP-000-example --run r01 --config baseline --variant baseline
	python3 tools/freeze.py examples/toy-pipeline/runs/r01/facts.json --run experiments/EXP-000-example/runs/r01/run.yaml
	python3 tools/dispatch.py --experiment EXP-000-example --run r02 --config tuned --variant tuned --baseline r01 --change "lateral gain retuned on track T1"
	python3 tools/freeze.py examples/toy-pipeline/runs/r02/facts.json --run experiments/EXP-000-example/runs/r02/run.yaml
	python3 tools/render-facts.py
	python3 tools/status.py --write
	python3 tools/compare.py --experiment EXP-000-example
	python3 tools/check.py

demo-clean:
	rm -rf experiments/EXP-000-example/runs reality/facts/EXP-000-example examples/toy-pipeline/runs manuscript/facts.tex experiments/INDEX.md manuscript/main.pdf manuscript/main.aux manuscript/main.log manuscript/main.out
	git checkout -- reality/index.csv experiments/EXP-000-example/experiment.yaml 2>/dev/null || true

# Render facts, then compile manuscript/main.tex twice (no bibliography in the shell).
pdf:
	python3 tools/render-facts.py
	cd manuscript && pdflatex -interaction=nonstopmode -halt-on-error main.tex >/dev/null && pdflatex -interaction=nonstopmode -halt-on-error main.tex | tail -1

pdf-clean:
	rm -f manuscript/main.aux manuscript/main.log manuscript/main.out manuscript/main.pdf manuscript/sections/*.aux

# Simulate one three-pane session on the toy pipeline and render docs/assets/session.gif.
session:
	python3 examples/session/run_session.py
	python3 tools/dev/render_session.py

session-clean: demo-clean
	rm -f decisions/ADR-0001-carry-r02-vs-r01.md
	rm -rf bus/queue/*
	: > bus/events.ndjson
