"""Friday demo safety check — verifies the LIVE path the demo might use works end-to-end,
without re-running the full keyword cohort.

ORDER MATTERS: the Europe PMC fetch (direct pmcid) runs BEFORE the S2 search, because once a
search is cached the direct-pmcid anti-hallucination guard in fetch_paper_text rejects it.

Exercises: API keys -> Europe PMC fetch (seeded paper) -> SEA-CDM extraction (real LLM) ->
provenance verifier -> Rscript+limma (analysis backend) -> Semantic Scholar search -> demo
artifacts intact. Prints a PASS/FAIL table. Cost ~ $0.02-0.05 (the one extraction call).

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/demo_safety_check.py
"""

import os
import sys
import glob
import json
import subprocess

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from dotenv import load_dotenv
load_dotenv()

SEED_PMCID = "PMC12248044"
SEED_GSE = "GSE279359"
SEED_TEXT = "data/papers/2267864b41e9b481bd2c3bbf6967fca3f0db8c34.txt"

rows = []
def rec(stage, ok, detail):
    rows.append((stage, "PASS" if ok else "FAIL", detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {stage}: {detail}")

# --- 0. API keys present (never print the values) -----------------------------------------
rec("API keys (.env)", bool(os.getenv("CLAUDE_API_KEY")),
    f"CLAUDE_API_KEY={'set' if os.getenv('CLAUDE_API_KEY') else 'MISSING'}, "
    f"S2_API_KEY={'set' if os.getenv('S2_API_KEY') else 'absent (anon pool)'}")

from tools.paper_tools import fetch_paper_text, search_papers
from tools.seacdm_tools import extract_tables_from_text
from tools.limma_voom_tools import _find_rscript

# --- 1. Europe PMC fetch (seeded paper, direct pmcid, BEFORE any search) -------------------
try:
    msg = fetch_paper_text.invoke({"pmcid": SEED_PMCID})
    head = (msg.splitlines()[0] if msg else "")
    ok = ("GSE" in msg) or ("saved" in msg.lower()) or ("character" in msg.lower())
    rec("Europe PMC fetch (seeded)", ok, head[:120])
except Exception as e:
    rec("Europe PMC fetch (seeded)", False, f"{type(e).__name__}: {e}")

# --- 2. Seeded paper full text available --------------------------------------------------
text, src = "", "NOT FOUND"
for p in (SEED_TEXT, f"data/papers/{SEED_PMCID}.txt"):
    if os.path.exists(p):
        text = open(p, encoding="utf-8", errors="replace").read()
        src = p
        break
rec("Seeded paper text", bool(text), f"{len(text)} chars ({src})")

# --- 3. SEA-CDM extraction (REAL LLM) + provenance verifier --------------------------------
if text:
    try:
        prov = {}
        tables = extract_tables_from_text(SEED_GSE, text, "Mouse", report=prov)
        nrows = {k: len(v) for k, v in tables.items() if v}
        rec("SEA-CDM extraction (LLM)", bool(nrows.get("study")),
            " ".join(f"{k}={v}" for k, v in nrows.items()))
        rec("Provenance verifier", prov.get("n_total", 0) > 0,
            f"{prov.get('n_verified', 0)}/{prov.get('n_total', 0)} verbatim, "
            f"{prov.get('n_unverified', 0)} flagged [UNVERIFIED]")
        os.makedirs(f"output/{SEED_GSE}", exist_ok=True)
        json.dump(prov, open(f"output/{SEED_GSE}/seacdm_provenance_freshcheck.json", "w"),
                  indent=2, default=str)
    except Exception as e:
        rec("SEA-CDM extraction (LLM)", False, f"{type(e).__name__}: {e}")
else:
    rec("SEA-CDM extraction (LLM)", False, "skipped — no seed text")

# --- 4. Rscript + limma (analysis backend health) -----------------------------------------
try:
    rscript = _find_rscript()
    if rscript:
        out = subprocess.run([rscript, "-e", "cat(as.character(packageVersion('limma')))"],
                             capture_output=True, text=True, encoding="utf-8",
                             errors="replace", timeout=90)
        ver = (out.stdout or "").strip()
        rec("Rscript + limma", bool(ver and "." in ver), f"limma {ver} @ {rscript}")
    else:
        rec("Rscript + limma", False, "Rscript not found on PATH or standard R dir")
except Exception as e:
    rec("Rscript + limma", False, f"{type(e).__name__}: {e}")

# --- 5. Semantic Scholar search (LAST — would poison the direct-pmcid guard above) ---------
try:
    sr = search_papers.invoke({"keyword": "exercise skeletal muscle transcriptome", "max_results": 3})
    head = (sr.splitlines()[0] if sr else "")
    ok = ("[#1]" in sr) or ("PMC" in sr) or ("hit" in sr.lower())
    rec("Semantic Scholar search", ok, head[:120])
except Exception as e:
    rec("Semantic Scholar search", False, f"{type(e).__name__}: {e}")

# --- 6. Demo artifacts intact (don't clean.py before Friday!) ------------------------------
ncsv = len(glob.glob("output/agentA_cohort_demo/csv/*.csv"))
deliv = os.path.isdir("output/deliverables")
rec("Demo artifacts intact", ncsv >= 13 and deliv,
    f"{ncsv} CSVs in demo + deliverables/ {'present' if deliv else 'MISSING'}")

# --- summary ------------------------------------------------------------------------------
print("\n" + "=" * 72)
npass = sum(1 for _, s, _ in rows if s == "PASS")
print(f"DEMO SAFETY CHECK: {npass}/{len(rows)} PASS")
for st, s, d in rows:
    print(f"  [{s}] {st}")
print("=" * 72)
