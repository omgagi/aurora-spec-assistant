# Technical Specification Assistant: prototype (City of Aurora R-2528)

OMEGACORTEX prototype · public Aurora Water manuals only · not a production system · not reviewed or endorsed by the City of Aurora.

A small cited-answer assistant over the three Aurora Water manuals named in Addendum 1, item A19. It answers by quoting passages it retrieves (BM25, no generative model) and cites manual, section and PDF page, or says "I don't know" and points to the Aurora Water Engineering inbox when the manuals don't support an answer. This is the prototype video the RFP accepts in place of a polished demo (Addendum 1, A21).

## Run it

```
./run_demo.sh            # downloads manuals if missing, verifies SHA-256, prints eval scores, serves http://127.0.0.1:8765/
PORT=9000 ./run_demo.sh  # choose a port
```

Needs only Python 3.9+ and `pdftotext` (poppler). Everything else is the Python standard library. `fetch_manuals.sh` refuses to start if a manual's SHA-256 no longer matches `manuals/SHA256SUMS`, which is the signal that the City published a new edition.

## What's in here

| Path | What |
|---|---|
| `app/engine.py` | chunking, BM25, citation, "I don't know" threshold |
| `app/server.py` | local web UI, `/api/ask`, feedback log |
| `app/index.html` | the chat page (AI-in-use notice, disclaimer slot, manual links, sample questions, thumbs up/down, retrieval-path view) |
| `app/manuals.json` | the three manuals: edition, URL, file |
| `app/reference_library.json` | synonym list used only to expand queries, never as an answer source (RFP 1.1.5 item 4) |
| `manuals/` | the PDFs + `SHA256SUMS` |
| `eval/` | 20 questions (`questions.json`) and an 8-question held-out set (`heldout.json`), `run_eval.py`, results |
| `screenshots/` | labeled screenshots and the walkthrough video |

Feedback (thumbs up/down plus the written note on thumbs-down) appends to `app/feedback.jsonl`. Nothing is sent anywhere.

## What this does not do

No single sign-on, no admin portal, no version cutover between manual editions, no usage analytics, no learning from past answers, and no generative model. Those are described in the proposal as proposed work, not as things this prototype shows. See the proposal.
