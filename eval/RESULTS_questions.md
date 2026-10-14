# Eval results: questions set

Bounded test on the public Aurora Water manuals, run 2026-10-14. Ground-truth pages were located by text search of the manuals before scoring. Top-1 citation correct: **{s1}/{n}** · correct citation in top 3: **{s3}/{n}**

| ID | Question | Expected | Got (top-1 manual · section · PDF page) | Top-1 | Top-3 | Key value in excerpt |
|---|---|---|---|---|---|---|
| Q01 | What is the minimum bury depth for water lines? | WSSD p.47/80 | WSSD · 22.08 Deep Sewers · p.143 | ❌ | ❌ | ❌ |
| Q02 | What type of pipe is required for sewer lines deeper than 20 feet? | WSSD p.46 | WSSD · 5.04 Alignment, Depth and Easements · p.48 | ❌ | ❌ | ❌ |
| Q03 | What is the minimum horizontal distance between a water line and a sewer line? | WSSD p.47/48 | WSSD · 5.04 Alignment, Depth and Easements · p.48 | ✅ | ✅ | ✅ |
| Q04 | How many residential units can be on a dead-end water main? | WSSD p.44/45 | WSSD · 5.02.2 Main Size · p.44 | ✅ | ✅ | ✅ |
| Q05 | What type of bedding is required for reinforced concrete pipe? | WSSD p.156 | WSSD · 26.07.3 Mortared Joints · p.162 | ❌ | ❌ | ❌ |
| Q06 | What is the maximum ponding depth in a parking lot? | SDDTC p.230/161 | SDDTC · 10.10 DESIGN STANDARDS FOR PARKING LOT DETENTION · p.231 | ❌ | ✅ | ✅ |
| Q07 | What is the minimum clearance for a stormwater and sanitary crossing in ROW with minimum pipe sizes? | WSSD p.82 | WSSD · 11.08.1 Storm Sewer Crossing over Water or Sanitary Sewer · p.82 | ✅ | ✅ | ✅ |
| Q08 | What is the maximum distance between manholes on an 8-inch sanitary sewer? | WSSD p.53 | WSSD · 5.06 Manhole Spacing · p.53 | ✅ | ✅ | ✅ |
| Q09 | What is the required fire hydrant spacing? | WSSD p.109 | WSSD · 16.06 Fire Hydrant Spacing · p.109 | ✅ | ✅ | ✅ |
| Q10 | How far can a fire department connection be from a fire hydrant? | WSSD p.109 | WSSD · 16.06 Fire Hydrant Spacing · p.109 | ✅ | ✅ | ✅ |
| Q11 | What is the maximum flow velocity in a water main? | WSSD p.44 | WSSD · 5.03 Sanitary Sewer System Design Criteria · p.47 | ❌ | ✅ | ✅ |
| Q12 | What is the minimum water main diameter in single family residential areas? | WSSD p.44 | WSSD · 5.02.2 Main Size · p.44 | ✅ | ✅ | ✅ |
| Q13 | What is the minimum diameter of a sanitary sewer service line? | WSSD p.145/151 | WSSD · 5.03 Sanitary Sewer System Design Criteria · p.47 | ❌ | ❌ | ❌ |
| Q14 | What is the minimum diameter for public storm drain mains and laterals? | SDDTC p.162 | SDDTC · 6.4.2 Minimum Sizes · p.162 | ✅ | ✅ | ✅ |
| Q15 | What is the minimum culvert pipe diameter within the public right-of-way? | SDDTC p.196 | SDDTC · 9.4.1 Construction Material and Pipe Size · p.196 | ✅ | ✅ | ✅ |
| Q16 | How often must BMPs be inspected during construction? | SWRULES p.36/52/77 | SWRULES · 5 INSPECTIONS AND MAINTENANCE · p.266 | ❌ | ✅ | ❌ |
| Q17 | After construction is complete, how often must the permittee self-inspect the site until final permit closeout? | SWRULES p.80/52/95 | SWRULES · 3.4 After Construction is Complete · p.80 | ✅ | ✅ | ✅ |
| Q18 | What is required when stockpiles are located within 100 feet of a drainageway? | SWRULES p.37 | SWRULES · 2.2 Design of System of Construction Stormwater BMPs and · p.37 | ✅ | ✅ | ✅ |
| Q19 | What is the speed limit on residential streets in Aurora? | not found → inbox | not found (low support (score 11.9, weighted term coverage 32%, most specific term 'speed' missing)) | ✅ | ✅ | — |
| Q20 | What is the City's remote work policy for engineering staff? | not found → inbox | not found (low support (score 17.1, weighted term coverage 57%, most specific term 'remote' missing)) | ✅ | ✅ | — |

## Failure cases (stated as observed)

- **Q01** "minimum bury depth for water lines": the manual says "minimum cover of four and one-half feet" (WSSD p.47 and p.80). The query word "bury" is not in the manual and the synonym expansion to "cover" was not enough; the engine returned WSSD §22.08 Deep Sewers, p.143, which is about sewer depth. Wrong manual section.
- **Q02** "pipe required for sewer lines deeper than 20 feet": the supporting sentence (WSSD §5.03, p.46) says "pipe stiffness greater than forty-six (46) psi for depths greater than twenty feet", with none of the query's words "type", "required" or "deeper". Returned §5.04, p.48, a different depth rule.
- **Q05** "bedding required for reinforced concrete pipe": WSSD §25.05, p.156 says bedding class for RCP "shall be specified on the project drawings" and does not name a class. The engine returned §26.07.3 Mortared Joints, p.162, and §9.05.1 Class A Bedding, p.69, which defines a bedding class but not as the RCP requirement. Both wrong.
- **Q06** top result is the right section (SDDTC §10.10, p.231) but the page holding the "12 inches" figure is p.230, which ranked second. Citation is right only in the top 3, and the displayed excerpt can omit the number.
- **Q11** "maximum flow velocity in a water main": the water-main velocity rule is the table referenced at WSSD §5.02.2, p.44 ("maximum velocity and head loss requirements based on pipe diameter"). The engine instead cited p.47 (§5.03, sanitary sewer criteria), on the same topic word but for the wrong system. Note: this question's expected page was first set to p.46 by mistake (that sentence is the sanitary sewer limit); it was corrected to p.44 after reading the page, before final scoring.
- **Q13** "minimum diameter of a sanitary sewer service line": the rule is at WSSD §23.04, p.145 ("minimum diameter of service lines is four inches"), which did not rank in the top 3. Returned §5.03, p.47.
- **Q16** "how often must BMPs be inspected during construction": correct passage is in the top 3 (SWRULES p.52, "every 7 calendar days and within 24 hours") but the top hit was p.266 (section label "5 INSPECTIONS AND MAINTENANCE"), and the excerpt did not contain "seven".

Out-of-scope questions Q19 and Q20 correctly returned no answer. Held-out set (`RESULTS_heldout.md`): H08 ("hours of the Aurora Municipal Center") was answered with an unrelated passage instead of "I don't know": a false answer, the most serious failure type for this RFP. H04 went the other way: the right passage exists (SWRULES p.37) but the engine declined to answer. H01 and H07 had the right page only at rank 2; H07's top hit was a table-of-contents page that the TOC filter missed.

## Tuning disclosure

The primary set was used during development: chunk size, the proximity rerank and parts of `reference_library.json` (e.g. bury→cover, deeper→greater) were adjusted while looking at these 20 questions. First full run scored 12/20 top-1, 13/20 top-3. Treat the primary-set score as optimistic; the held-out set, written after the engine was frozen and run once, is the fairer number.
