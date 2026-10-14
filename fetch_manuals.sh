#!/usr/bin/env bash
# Downloads the three public Aurora Water manuals (A19) from auroragov.org and verifies SHA-256.
set -euo pipefail
cd "$(dirname "$0")/manuals"
python3 - <<'P'
import json, os, subprocess
for m in json.load(open("../app/manuals.json")):
    if not os.path.exists(m["file"]):
        print("downloading", m["file"]); subprocess.run(["curl", "-sfL", "-A", "Mozilla/5.0", m["url"], "-o", m["file"]], check=True)
P
cd ..
mkdir -p text
for f in manuals/*.pdf; do b=$(basename "$f" .pdf); [ -f "text/$b.txt" ] || pdftotext -layout "$f" "text/$b.txt"; done
cd manuals
sha256sum -c SHA256SUMS || { echo "HASH MISMATCH: the City may have published a new edition. Re-run eval before using."; exit 1; }
