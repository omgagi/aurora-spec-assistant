# Evidence and reproducibility: Aurora R-2528 prototype

Recorded 2026-10-14, ~07:30 PT.

## Command

```
cd aurora-spec-assistant
./run_demo.sh
```

`./run_demo.sh` runs `fetch_manuals.sh` (download if missing, then `sha256sum -c manuals/SHA256SUMS`), then `python3 eval/run_eval.py` for both question sets, then `python3 app/server.py`.

## Build

`build_id()` in `app/engine.py` is the first 12 hex chars of SHA-256 over `app/engine.py`, `app/manuals.json`, `app/reference_library.json` and `manuals/SHA256SUMS`. The running page footer shows it. At the time of the screenshots it was `1efc21d85575`. Re-run `python3 -c "import sys;sys.path.insert(0,'app');import engine;print(engine.build_id())"` from `` to confirm.

## Manuals (public, auroragov.org, fetched 2026-10-14)

| Manual | Edition | Pages | SHA-256 |
|---|---|---|---|
| Water, Sanitary Sewer & Storm Drainage Infrastructure Standards & Specifications | 2026, Final, January 15, 2026 | 332 | `2954f393148298ad82f5aa22dc7b6e509c6ee51595cab972a0443f2db6ebbf3f` |
| Rules and Regulations Regarding Stormwater Discharges Associated with Construction Activities | file linked on auroragov.org; PDF metadata says created 2010-11-16, modified 2014-04-04 | 317 | `d1468eb82a8cf206511757222db1f5af5c92b75592974bb0aa051805d84816e5` |
| Storm Drainage Design and Technical Criteria Manual | 2026, FINAL, January 2026 | 257 | `86b64f6de46fac7134d9b445dff468d8fa0c80007cb62240576462b0b16760ce` |

URLs are in `app/manuals.json`. Text was extracted with `pdftotext -layout`. The PDFs are not committed (see `.gitignore`); the hashes are.

## Tests

`eval/run_eval.py` scores citation correctness against page numbers found by text search of the manuals before the engine was scored. Results at this build:

- Primary set (20 questions, 7 taken from RFP section 1.1.8, 11 derived from the same use cases, 2 out of scope): **top-1 citation correct 13/20, correct citation somewhere in the top 3 16/20**.
- Held-out set (8 questions written after the engine was frozen): **top-1 4/8, top-3 6/8**.

Full tables: `eval/RESULTS_questions.md`, `eval/RESULTS_heldout.md`. The City's 95% accuracy bar (Addendum 1, A35) is **not met** by this prototype. That is stated in the proposal as a gap, not a claim.

## Re-recording the video

```
PORT=8765 ./run_demo.sh &
python record.py   # with playwright installed
```

The recording environment used Playwright's Chromium and ffmpeg; both are tools on the build machine, not part of the prototype.
