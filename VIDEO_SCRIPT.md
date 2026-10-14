# Walkthrough video (Addendum 1, A21)

Recorded 2026-10-14, 07:26 PT, with Playwright driving Chromium and ffmpeg encoding. File: `screenshots/demo-walkthrough.mp4` (about 23 s, 1280x800). Under the RFP's 5-minute limit.

1. Open the page. Banner states prototype, public manuals, not a production system, not City-endorsed. AI-in-use notice and the City disclaimer slot are visible, with links to all three manuals on auroragov.org.
2. Ask "What is the minimum horizontal distance between a water line and a sewer line?" Answer is a verbatim quote with manual, section 5.04, PDF page 48, and links to that page locally and on auroragov.org.
3. Ask "What is the speed limit on residential streets in Aurora?" Answer says it is not in the manuals and gives waterengineering@auroragov.org.
4. Ask "What is the minimum culvert pipe diameter within the public right-of-way?" Answer quotes 24 inches, section 9.4.1, page 196. Open the retrieval-path view to show the ranked passages and term coverage.
5. Click thumbs-down and type what was wrong. The note is recorded locally.

To re-record: start `./run_demo.sh`, then run `python record.py` (needs playwright + chromium + ffmpeg).
