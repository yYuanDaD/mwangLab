"""Robustness sweep: run the Agent A cohort on SEVERAL DIFFERENT keywords (not the same one
repeated) to check whether the current validations hold across diverse studies / code paths.

Each keyword -> search -> top paper -> own-GSE (if any) -> full pipeline. We then read each run's
manifest (papers.csv) + batch summary (cohort_analysis/summary.csv) + failures.log and tabulate
what actually happened + WHICH validations were exercised:
  * matrix-type classification (raw_counts / fpkm_or_tpm / log_transformed)
  * contrast auto-detection + (gated) LLM contrast validation
  * GSEA gene-ID handling incl. the new integer->symbol sidecar
  * enrichment->groups FK resolution (the '__method' fix)
  * #5 findings / #6 agreement / #7+#7b chain
  * fail-soft group extraction, metadata-structural derivation

All runs land under output/_kw_robustness/ (grouped, not cluttering the top level).

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/robustness_keywords_0622.py
"""
import os
import re
import sys
import glob

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from tools.cohort_tools import run_agent_a_cohort

OUT_BASE = "./output/_kw_robustness"

# diverse exercise keywords -> different organisms / tissues / study designs / matrix types
KEYWORDS = [
    ("resistance exercise human skeletal muscle RNA-seq", "Human"),
    ("treadmill exercise mouse skeletal muscle RNA sequencing", "Mouse"),
    ("aerobic exercise training mouse heart RNA-seq", "Mouse"),
]
TK = ["exercise", "training", "trained", "post", "run", "HIIT", "endurance", "resistance", "aerobic"]
CK = ["sedentary", "control", "pre", "rest", "sham", "untrained", "baseline"]


def _slug(s):
    return re.sub(r"_+", "_", re.sub(r"[^a-z0-9]+", "_", s.lower())).strip("_")[:48]


def _read1(path):
    return pd.read_csv(path) if os.path.isfile(path) else pd.DataFrame()


def _csv_rows(csv_dir, name):
    p = os.path.join(csv_dir, f"{name}.csv")
    return len(pd.read_csv(p)) if os.path.isfile(p) else 0


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
    csv_dir = os.path.join(cohort, "csv")

    if not man.empty:
        m0 = man.iloc[0]
        rec.update({
            "pmcid": m0.get("pmcid"), "gse": m0.get("chosen_gse"),
            "ownership": m0.get("ownership"), "analyzed": m0.get("analyzed"),
            "status": m0.get("status"), "da_method": m0.get("da_method"),
            "n_findings": m0.get("n_findings"), "metadata_struct": m0.get("metadata_structural"),
            "extract": m0.get("extract_group_errors"),
            "enrich_edges": m0.get("enrichment_edges"), "pathway_nodes": m0.get("pathway_nodes"),
            "chain_gsea": m0.get("chain_gsea_pathways"), "chain_gene": m0.get("chain_gene_links"),
            "agree_det": m0.get("agree_not_detected"), "agree_conf": m0.get("agree_confirmed"),
        })
    if not summ.empty:
        s0 = summ.iloc[0]
        rec.update({
            "matrix_type": s0.get("matrix_type"), "n_contrasts": s0.get("n_contrasts"),
            "n_deg": s0.get("n_deg"), "n_gsea_sig": s0.get("n_gsea_sig"),
            "llm_validated": s0.get("llm_validated"),
        })
    rec["chain_view"] = _csv_rows(csv_dir, "chain_view")
    # failures (analysis-substep failures don't abort the paper, but we want to see them)
    fl = os.path.join(cohort, "cohort_analysis", "failures.log")
    rec["failures"] = (open(fl, encoding="utf-8").read().strip()[:160] if os.path.isfile(fl)
                       and os.path.getsize(fl) > 0 else "")
    rows.append(rec)

# ---------------- robustness table ----------------
df = pd.DataFrame(rows)
print("\n" + "=" * 100)
print("ROBUSTNESS SWEEP RESULTS")
print("=" * 100)
show = ["keyword", "gse", "ownership", "analyzed", "matrix_type", "da_method", "n_contrasts",
        "n_deg", "n_gsea_sig", "enrich_edges", "chain_view", "n_findings", "status"]
show = [c for c in show if c in df.columns]
with pd.option_context("display.max_colwidth", 26, "display.width", 240):
    print(df[show].to_string(index=False))

print("\n--- which validations were EXERCISED per keyword ---")
for _, r in df.iterrows():
    fired = []
    if str(r.get("metadata_struct")) == "True": fired.append("metadata-structural")
    if pd.notna(r.get("matrix_type")): fired.append(f"classify={r.get('matrix_type')}")
    if pd.notna(r.get("n_contrasts")): fired.append(f"contrasts={r.get('n_contrasts')}")
    if pd.notna(r.get("llm_validated")): fired.append(f"contrastLLM={r.get('llm_validated')}")
    if pd.notna(r.get("n_gsea_sig")): fired.append(f"GSEA_sig={r.get('n_gsea_sig')}")
    if r.get("enrich_edges") not in (None, 0): fired.append(f"#7b_edges={r.get('enrich_edges')}")
    print(f"  [{r.get('gse')}] {r['keyword'][:40]:40s} -> {', '.join(fired) or 'text-only (no own-GSE analysis)'}")
    if r.get("failures"):
        print(f"       FAILURES: {r['failures']}")

print("\n--- verdict ---")
crashed = df[df.get("run", "").astype(str).str.startswith("EXC")] if "run" in df else pd.DataFrame()
print(f"  runs completed without crashing: {len(df) - len(crashed)}/{len(df)}")
analyzed = df[df.get("analyzed") == True] if "analyzed" in df else pd.DataFrame()
print(f"  reached the DA/GSEA path (own-GSE): {len(analyzed)}/{len(df)}")
print(f"  text-only (no own-GSE, exercised search+extract+#5): {len(df) - len(analyzed)}/{len(df)}")
print("=" * 100)
df.to_csv(os.path.join(OUT_BASE, "robustness_summary.csv"), index=False)
print(f"saved: {os.path.join(OUT_BASE, 'robustness_summary.csv')}")
