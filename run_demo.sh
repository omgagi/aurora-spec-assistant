#!/usr/bin/env bash
# One command: fetch manuals (if missing), verify hashes, run eval, start the local UI.
set -euo pipefail
cd "$(dirname "$0")"
./fetch_manuals.sh
python3 eval/run_eval.py | head -1
EVAL_SET=heldout python3 eval/run_eval.py | head -1
exec python3 app/server.py "${PORT:-8765}"
