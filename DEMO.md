# Demo one-pager: Aurora R-2528 Technical Specification Assistant

**Need it answers.** The RFP (sections 1.1.1–1.1.3 and Addendum 1 A21) asks for a browser chatbot that answers from Aurora Water's three manuals with section and page citations, falls back when it can't, discloses AI use, and takes feedback. A21 says a prototype built on those manuals satisfies the video demonstration requirement.

**What it shows.** A local web page that retrieves passages with BM25 from the three public manuals, quotes them, and cites manual, section and PDF page (with a link to that page on auroragov.org). When support is low it says so and names waterengineering@auroragov.org. Thumbs up/down with a written reason on thumbs-down. Sample questions, AI-in-use notice, City disclaimer slot. Extractive only: no generative model, so no invented numbers.

**Run / view.** `./run_demo.sh` → http://127.0.0.1:8765/. Walkthrough video: `screenshots/demo-walkthrough.mp4`. Screenshots: `screenshots/01-start.png` through `05-feedback.png`.

**Prototype boundary.** Banner on every screen: "OMEGACORTEX prototype · public Aurora Water manuals only · not a production system · not reviewed or endorsed by the City of Aurora". Public data only. Bounded synthetic tests (the 20-question and 8-question evals); the City's 95% accuracy bar is not met. No Okta, admin portal, version cutover or analytics.



**Build.** `1efc21d85575` (see `EVIDENCE_REPRODUCIBILITY.md`).
