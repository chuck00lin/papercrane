#!/usr/bin/env bash
# Open the three roles of a papercrane session as three tmux panes.
#   tools/dev/tmux-session.sh [agent command] [code space path]
# Pane 0 (left): head — you talk to the paper agent here, in the workspace.
# Pane 1 (top right): experiment — the experiment agent, in the workspace.
# Pane 2 (bottom right): the code-space agent, inside your repository.
# The agent command defaults to `claude`; pass e.g. `codex` or `bash` to use another runtime.
set -euo pipefail
AGENT="${1:-claude}"
CS="${2:-$(pwd)/examples/toy-pipeline}"
WS="$(cd "$(dirname "$0")/../.." && pwd)"
S=papercrane
tmux has-session -t "$S" 2>/dev/null && { echo "session '$S' exists: tmux attach -t $S"; exit 0; }
tmux new-session -d -s "$S" -n loop -c "$WS" -x 220 -y 50
tmux select-pane -t "$S:loop.0" -T "head"
tmux split-window -h -t "$S:loop" -c "$WS"
tmux select-pane -t "$S:loop.1" -T "experiment"
tmux split-window -v -t "$S:loop.1" -c "$CS"
tmux select-pane -t "$S:loop.2" -T "codespace"
tmux set -t "$S" pane-border-status top
tmux send-keys -t "$S:loop.0" "echo 'head: open with the 8-line session contract (docs/session-contract.md)'; $AGENT" C-m
tmux send-keys -t "$S:loop.1" "echo 'experiment: poll with  python3 tools/bus.py poll --agent experiment'; $AGENT" C-m
tmux send-keys -t "$S:loop.2" "echo 'codespace: poll with  python3 $WS/tools/bus.py poll --agent <codespace name>'; $AGENT" C-m
tmux select-pane -t "$S:loop.0"
echo "tmux attach -t $S"
