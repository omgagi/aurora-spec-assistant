# Eval results: heldout set

Bounded test on the public Aurora Water manuals, run 2026-10-14. Ground-truth pages were located by text search of the manuals before scoring. Top-1 citation correct: **{s1}/{n}** · correct citation in top 3: **{s3}/{n}**

| ID | Question | Expected | Got (top-1 manual · section · PDF page) | Top-1 | Top-3 | Key value in excerpt |
|---|---|---|---|---|---|---|
| H01 | What is the maximum inside drop from inlet to outlet in a sanitary manhole? | WSSD p.46 | WSSD · 31.06 Pipe Selection Chart · p.192 | ❌ | ✅ | ✅ |
| H02 | How long must a poured concrete thrust block cure? | WSSD p.83 | WSSD · 11.10 Thrust Blocks · p.83 | ✅ | ✅ | ✅ |
| H03 | What criteria apply to safety grates on culverts? | SDDTC p.197 | SDDTC · 9.4.6 Safety Grates · p.197 | ✅ | ✅ | ✅ |
| H04 | What extra controls are required for stockpiles near a public storm sewer? | SWRULES p.37 | not found (low support (score 19.7, weighted term coverage 54%, most specific term 'extra' missing)) | ❌ | ❌ | ❌ |
| H05 | What minimum slope is required for underdrains in the right-of-way? | WSSD p.152 | WSSD · 24.05 Alignment · p.152 | ✅ | ✅ | ✅ |
| H06 | How soon must graded areas be temporarily stabilized with rough cut street controls? | SWRULES p.36 | SWRULES · 2.2 Design of System of Construction Stormwater BMPs and · p.36 | ✅ | ✅ | ✅ |
| H07 | What is the minimum diameter of private storm pipe? | WSSD p.156 | WSSD · 25.03 Pipe Size · p.7 | ❌ | ✅ | ✅ |
| H08 | What are the hours of the Aurora Municipal Center? | not found → inbox | WSSD · 3.01.1 The Aurora Water Department requires a Public Extension Agreement be · p.32 | ❌ | ❌ | — |
