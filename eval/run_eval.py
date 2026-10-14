"""Scores the engine against eval/questions.json. Ground-truth pages were found by text search of the manuals (grep) before scoring."""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(D), "app"))
import engine
E = engine.Engine(); SET = os.environ.get("EVAL_SET", "questions"); Q = json.load(open(os.path.join(D, SET + ".json"))); rows = []
for q in Q:
    r = E.answer(q["q"]); cits = r["citations"]
    if q["manual"] is None:
        ok1 = ok3 = not r["found"]; key = None
    else:
        hit = lambda c: c["manual_id"] == q["manual"] and c["page"] in q["pages"]
        ok1 = r["found"] and hit(cits[0]); ok3 = r["found"] and any(hit(c) for c in cits)
        key = r["found"] and any(q["key"].lower() in c["excerpt"].lower() for c in cits if hit(c))
    rows.append({**q, "found": r["found"], "top1_correct": ok1, "top3_correct": ok3, "key_in_excerpt": key,
                 "got": [(c["manual_id"], c["section"], c["page"]) for c in cits], "answer": r["answer"], "reason": r.get("reason")})
n = len(rows); s1 = sum(r["top1_correct"] for r in rows); s3 = sum(r["top3_correct"] for r in rows)
summary = {"n": n, "top1_citation_correct": s1, "top3_citation_correct": s3, "build": engine.build_id() if hasattr(engine, "build_id") else None}
json.dump({"summary": summary, "rows": rows}, open(os.path.join(D, f"results_{SET}.json"), "w"), indent=1, ensure_ascii=False)
with open(os.path.join(D, f"RESULTS_{SET}.md"), "w") as f:
    f.write("# Eval results: " + SET + " set\n\nBounded test on the public Aurora Water manuals, run 2026-10-14. Ground-truth pages were located by text search of the manuals before scoring. Top-1 citation correct: **{s1}/{n}** · correct citation in top 3: **{s3}/{n}**\n\n")
    f.write("| ID | Question | Expected | Got (top-1 manual · section · PDF page) | Top-1 | Top-3 | Key value in excerpt |\n|---|---|---|---|---|---|---|\n")
    for r in rows:
        exp = f'{r["manual"]} p.{"/".join(map(str, r["pages"]))}' if r["manual"] else "not found → inbox"
        got = f'{r["got"][0][0]} · {r["got"][0][1]} · p.{r["got"][0][2]}' if r["got"] else f'not found ({r["reason"]})'
        yn = lambda v: "—" if v is None else ("✅" if v else "❌")
        f.write(f'| {r["id"]} | {r["q"]} | {exp} | {got} | {yn(r["top1_correct"])} | {yn(r["top3_correct"])} | {yn(r["key_in_excerpt"])} |\n')
print(json.dumps(summary)); [print(r["id"], r["top1_correct"], r["top3_correct"], r["key_in_excerpt"], r["got"][:2], r["reason"] or "") for r in rows]
