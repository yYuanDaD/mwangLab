"""Round 2 of the keyword robustness sweep — NEW keywords chosen to land on DIFFERENT studies
than round 1 (which kept hitting GSE279359 / GSE208615). Vary tissue + organism deliberately:
human blood, mouse liver, mouse brain. Also reads the new `deg_sanity` column to see whether the
post-DA implausibility guard fires on any freshly-hit study (e.g. a small-n cohort).

All runs land under output/_kw_robustness/. Run:
  PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/robustness_keywords2_0623.py
"""
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from tools.cohort_tools import run_agent_a_cohort

OUT_BASE = "./output/_kw_robustness"

# NEW keywords — different tissue/organism to surface studies not seen in round 1
KEYWORDS = [
    ("exercise human blood PBMC RNA-seq transcriptome", "Human"),
    ("swimming exercise mouse liver RNA sequencing", "Mouse"),
    ("exercise hippocampus brain mouse RNA-seq", "Mouse"),
]
TK = ["exercise", "training", "trained", "post", "run", "swim", "swimming", "endurance",
      "aerobic", "resistance", "active"]
CK = ["sedentary", "control", "pre", "rest", "sham", "untrained", "baseline", "inactive"]


def _slug(s):
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", s.lower())).strip("_")[:48]


def _read1(p):
    return pd.read_csv(p) if os.path.isfile(p) else pd.DataFrame()


rows = []
for kw, org in KEYWORDS:
    label = _slug(kw)
    print("=" * 80)
    print(f"KEYWORD: {kw}  (organism={org})  label={label}")
    print("=" * 80)
    rec = {"keyword": kw, "organism": org}
    try:
        report = run_agent_a_cohort(
            keyword=kw, max_papers=1, organism=org, with_analysis=True,
            treatment_keywords=TK, control_keywords=CK,
            raw_da_method="all", require_pdf=True, search_pool=25,
            run_label=label, output_base=OUT_BASE, max_chars=24000, extract_findings=True,
        )
        print((report or "").splitlines()[0] if report else "(no report)")
        rec["run"] = "ok"
    except Exception as e:
        print(f"!! run raised: {type(e).__name__}: {e}")
        rec["run"] = f"EXC:{type(e).__name__}"

    cohort = os.path.join(OUT_BASE, f"agentA_cohort_{label}")
    man = _read1(os.path.join(cohort, "papers.csv"))
    summ = _read1(os.path.join(cohort, "cohort_analysis", "summary.csv"))
    if not man.empty:
        m0 = man.iloc[0]
        rec.update({"pmcid": m0.get("pmcid"), "gse": m0.get("chosen_gse"),
                    "ownership": m0.get("ownership"), "analyzed": m0.get("analyzed"),
                    "status": m0.get("status"), "da_method": m0.get("da_method"),
                    "n_findings": m0.get("n_findings"),
                    "enrich_edges": m0.get("enrichment_edges"), "chain": m0.get("chain_gsea_pathways")})
    if not summ.empty:
        s0 = summ.iloc[0]
        rec.update({"matrix_type": s0.get("matrix_type"), "n_contrasts": s0.get("n_contrasts"),
                    "n_deg": s0.get("n_deg"), "n_gsea_sig": s0.get("n_gsea_sig"),
                    "llm_validated": s0.get("llm_validated"),
                    "deg_sanity": s0.get("deg_sanity")})
    rows.append(rec)

df = pd.DataFrame(rows)
print("\n" + "=" * 100)
print("ROUND-2 KEYWORD SWEEP RESULTS")
print("=" * 100)
show = [c for c in ["keyword", "gse", "ownership", "analyzed", "matrix_type", "da_method",
                    "n_contrasts", "n_deg", "n_gsea_sig", "deg_sanity", "n_findings", "status"]
        if c in df.columns]
with pd.option_context("display.max_colwidth", 24, "display.width", 240):
    print(df[show].to_string(index=False))

print("\n--- new studies hit (vs round 1's GSE279359/GSE208615) ---")
seen_before = {"GSE279359", "GSE208615"}
for _, r in df.iterrows():
    g = r.get("gse")
    tag = "NEW" if (pd.notna(g) and g not in seen_before) else ("text-only" if pd.isna(g) else "repeat")
    print(f"  {r['keyword'][:42]:42s} -> {g if pd.notna(g) else '(no own-GSE)'}  [{tag}]")

print("\n--- did the DEG-sanity guard fire on any new study? ---")
if "deg_sanity" in df.columns:
    flagged = df[df["deg_sanity"].astype(str).str.contains("implausible|tiny", na=False)]
    if len(flagged):
        for _, r in flagged.iterrows():
            print(f"  {r.get('gse')}: {r.get('deg_sanity')}")
    else:
        print("  none flagged (all analyzed studies passed the implausibility guard)")

print("\n--- verdict ---")
crashed = df[df.get("run", "").astype(str).str.startswith("EXC")] if "run" in df else pd.DataFrame()
print(f"  runs completed without crashing: {len(df) - len(crashed)}/{len(df)}")
df.to_csv(os.path.join(OUT_BASE, "robustness_keywords2_summary.csv"), index=False)
print("=" * 100)
print("saved:", os.path.join(OUT_BASE, "robustness_keywords2_summary.csv"))
