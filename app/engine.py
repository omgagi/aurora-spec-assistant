"""Cited-answer engine: BM25 over page-level chunks of the three Aurora Water manuals.
Extractive only: every answer is verbatim text from a manual with manual/section/page citation.
Standard library only."""
import json, math, os, re, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
DEMO = os.path.dirname(HERE)
CHUNK_LINES = int(os.environ.get("CHUNK_LINES", "45"))
PROX_W = float(os.environ.get("PROX_W", "0.6"))
INBOX = "waterengineering@auroragov.org"  # Addendum 1, A35
STOP = set("a an the of to in on for and or is are be by with what which how many much does do shall must from at as that this it its can there any per than when where who whom s often far how type kind required requirement minimum maximum".split())
KEEP = {"minimum", "maximum"}  # kept for sentence scoring only
HEAD = re.compile(r"^\s{0,16}(?:SECTION|Section|CHAPTER|Chapter)?\s*((?:\d{1,2}\.\d{1,2}(?:\.\d{1,2}){0,2})|\d{1,2}\.00|\d{1,2})\s{1,8}([A-Z][A-Za-z0-9 ,&/()'\-]{2,70})\s*$")

def stem(w):
    if w.endswith("eed"):
        return w
    for suf in ("ings", "ing", "ies", "es", "ed", "s"):
        if suf == "es" and not re.search(r"(s|x|z|ch|sh)es$", w):
            continue
        if len(w) > len(suf) + 2 and w.endswith(suf):
            return w[: -len(suf)] + ("y" if suf == "ies" else "")
    return w

def toks(s, keep_minmax=False):
    out = []
    for w in re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", s.lower()):
        if w in STOP and not (keep_minmax and w in KEEP):
            continue
        out.append(stem(w))
    return out

def load_manuals():
    return json.load(open(os.path.join(HERE, "manuals.json")))

def pages_of(m):
    txt = os.path.join(DEMO, "text", m["file"].replace(".pdf", ".txt"))
    if not os.path.exists(txt):
        os.makedirs(os.path.dirname(txt), exist_ok=True)
        subprocess.run(["pdftotext", "-layout", os.path.join(DEMO, "manuals", m["file"]), txt], check=True)
    return open(txt, encoding="utf-8", errors="ignore").read().split("\f")

def build_index():
    chunks = []
    for m in load_manuals():
        section = "front matter"
        for pno, page in enumerate(pages_of(m), start=1):
            lines = page.split("\n")
            if sum(1 for l in lines if re.search(r"\.{6,}", l)) >= 5 or sum(1 for l in lines if re.search(r"\s\d{1,2}-\d{1,2}\s*$", l) and not re.search(r"(?i)january|february|march|april|may|june|july|august|september|october|november|december|20\d\d", l)) >= 6:
                continue  # table-of-contents page: not an answer source
            is_detail = bool(re.search(r"(?i)\b(standard detail|detail no|dwg\.? no|drawing no)\b", page)) or \
                        (len(page) > 0 and sum(len(l) > 150 for l in lines) > 8)
            buf, start_sec = [], section
            def flush():
                body = "\n".join(buf).strip()
                if len(re.findall(r"[A-Za-z]{3,}", body)) >= 8:
                    chunks.append({"manual": m["id"], "page": pno, "section": start_sec, "text": body, "detail": is_detail})
            for l in lines:
                h = HEAD.match(l)
                if h and not re.search(r"\.{4,}|\s\d+-\d+\s*$", l):
                    num, title = h.group(1), h.group(2).strip()
                    if not re.match(r"^(Figure|Table|of|and|to)\b", title):
                        if buf:
                            flush(); buf = []
                        section = f"{num} {title}"; start_sec = section
                buf.append(l)
                if len(buf) >= CHUNK_LINES and not l.strip():
                    flush(); buf = []; start_sec = section
            if buf:
                flush()
    return chunks

class Engine:
    def __init__(self):
        self.manuals = {m["id"]: m for m in load_manuals()}
        self.syn = json.load(open(os.path.join(HERE, "reference_library.json")))["synonyms"]
        self.chunks = build_index()
        self.docs = [toks(c["text"] + " " + c["section"]) for c in self.chunks]
        self.N = len(self.docs); self.avg = sum(map(len, self.docs)) / self.N
        self.df = {}
        for d in self.docs:
            for t in set(d):
                self.df[t] = self.df.get(t, 0) + 1
        self.tf = [{} for _ in self.docs]
        for i, d in enumerate(self.docs):
            for t in d:
                self.tf[i][t] = self.tf[i].get(t, 0) + 1

    def idf(self, t):
        n = self.df.get(t, 0)
        return math.log(1 + (self.N - n + 0.5) / (n + 0.5))

    def expand(self, q):
        base = toks(q); extra = []
        for w in re.findall(r"[a-z0-9\-]+", q.lower()):
            for s in self.syn.get(w, []):
                extra += toks(s)
        return base, [t for t in extra if t not in base]

    def score(self, i, terms, weights):
        s, L = 0.0, len(self.docs[i])
        for t, w in zip(terms, weights):
            f = self.tf[i].get(t, 0)
            if f:
                s += w * self.idf(t) * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * L / self.avg))
        return s

    def answer(self, question, history=None, k=3):
        q = question
        follow = bool(history) and (len(toks(question)) <= 4 or re.search(r"(?i)\b(it|that|those|this|they|them|what about|and for)\b", question))
        if follow:
            q = history[-1] + " " + question
        base, extra = self.expand(q)
        terms = base + extra; weights = [1.0] * len(base) + [0.8] * len(extra)
        if not base:
            return self.not_found(question, "no searchable terms")
        pre = sorted(((self.score(i, terms, weights), i) for i in range(self.N)), reverse=True)[:40]
        # rerank: BM25 + proximity bonus (query terms co-occurring inside one sentence of the passage)
        tw = dict(zip(terms, weights))
        def prox(i):
            best = 0.0
            for sent in re.split(r"(?<=[.;])\s+|\n\s*\n", self.chunks[i]["text"]):
                st = set(toks(sent))
                best = max(best, sum(self.idf(t) * w for t, w in tw.items() if t in st))
            sec = set(toks(self.chunks[i]["section"]))
            best += 0.4 * sum(self.idf(t) * w for t, w in tw.items() if t in sec)
            return best
        scored = sorted(((s + PROX_W * prox(i), i) for s, i in pre), reverse=True)[:k]
        top_s, top_i = scored[0]
        # grounding check on the top passage: idf-weighted share of query concepts present (a synonym counts),
        # and the most specific (rarest) query concept must be present.
        have = set(self.docs[top_i])
        syn_of = {}
        for w in re.findall(r"[a-z0-9\-]+", q.lower()):
            for s in self.syn.get(w, []):
                syn_of.setdefault(stem(w), set()).update(toks(s))
        concepts = list(dict.fromkeys(base))
        present = {t: (t in have or bool(syn_of.get(t, set()) & have)) for t in concepts}
        tot = sum(self.idf(t) for t in concepts)
        coverage = sum(self.idf(t) for t in concepts if present[t]) / max(tot, 1e-9)
        rarest = max(concepts, key=self.idf)
        trace = {"query_terms": base, "expanded_terms": extra, "follow_up_context": history[-1] if follow else None,
                 "top": [{"score": round(s, 2), **self.cite(i)} for s, i in scored], "coverage": round(coverage, 2),
                 "rarest_term": rarest, "rarest_present": present[rarest]}
        if top_s < 8.0 or coverage < 0.6:
            r = self.not_found(question, f"low support (score {top_s:.1f}, weighted term coverage {coverage:.0%}, most specific term '{rarest}' {'found' if present[rarest] else 'missing'})"); r["trace"] = trace; return r
        cits = []
        for s, i in scored:
            if s >= 0.6 * top_s:
                c = self.cite(i); c["excerpt"] = self.best_sentences(i, base + extra); cits.append(c)
        return {"found": True, "question": question, "answer": cits[0]["excerpt"], "citations": cits, "trace": trace}

    def best_sentences(self, i, terms):
        text = re.sub(r"[ \t]+", " ", self.chunks[i]["text"])
        sents = [s.strip() for s in re.split(r"(?<=[.;:])\s+(?=[A-Z0-9(•])|\n\s*\n|\n(?=\s*(?:\d{1,2}\.\s|•|[a-z]\)\s|[A-Z]{1,2}\.\s))", text) if len(s.strip()) > 20]
        ts = set(terms)
        ranked = sorted(sents, key=lambda s: -(sum(self.idf(t) for t in set(toks(s, True)) & ts) + (1.5 if re.search(r"\d", s) else 0)))
        best = ranked[:2] if ranked else [text[:400]]
        out = [s for s in sents if s in best]
        return re.sub(r"\s+", " ", " … ".join(out))[:700]

    def cite(self, i):
        c = self.chunks[i]; m = self.manuals[c["manual"]]
        return {"manual_id": m["id"], "manual": m["title"], "edition": m["edition"], "section": c["section"], "page": c["page"],
                "detail_sheet": c["detail"], "official_link": f'{m["url"]}#page={c["page"]}', "local_link": f'/manuals/{m["file"]}#page={c["page"]}'}

    def not_found(self, question, why):
        return {"found": False, "question": question, "reason": why,
                "answer": f"I could not find support for this in the three Aurora Water manuals. Please contact the Aurora Water Engineering inbox: {INBOX}.",
                "citations": []}

def build_id():
    import hashlib
    h = hashlib.sha256()
    for f in ("engine.py", "manuals.json", "reference_library.json"):
        h.update(open(os.path.join(HERE, f), "rb").read())
    h.update(open(os.path.join(DEMO, "manuals", "SHA256SUMS"), "rb").read())
    return h.hexdigest()[:12]
