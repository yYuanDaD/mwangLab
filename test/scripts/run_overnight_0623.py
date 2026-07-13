"""Overnight cohort on the ESTABLISHED keyword with an EXPANDED max_papers, so multiple own-GSE
studies get analyzed (more GSEA + chains) and the new reporting fixes (gap 2 agreement notes /
gap 3 DA reasons) are exercised across several studies. Per-paper failures are caught and do not
abort the cohort; max_chars kept small to respect the 30k tok/min cap over a long unattended run.

Run: PYTHONIOENCODING=utf-8 .venv/Scripts/python.exe test/scripts/run_overnight_0623.py
"""
import os
import sys
import glob
import time

_HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(os.path.dirname(os.path.dirname(_HERE)))
sys.path.insert(0, os.path.dirname(os.path.dirname(_HERE)))

from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from tools.cohort_tools import run_agent_a_cohort

LABEL = "overnight_0623"
COHORT = os.path.join("output", "_kw_robustness", f"agentA_cohort_{LABEL}")

print("=" * 80)
print("OVERNIGHT COHORT  keyword='voluntary wheel running mouse skeletal muscle RNA sequencing'")
print("max_papers=25  search_pool=50  raw_da_method='all'  extract_findings=True")
print("=" * 80)


def _run():
    return run_agent_a_cohort(
        keyword="voluntary wheel running mouse skeletal muscle RNA sequencing",
        max_papers=25, organism="Mouse", with_analysis=True,
        treatment_keywords=["exercise", "training", "trained", "post", "run", "running", "acute",
                            "endurance", "exercised", "active", "wheel"],
        control_keywords=["sedentary", "control", "pre", "rest", "sham", "baseline", "untrained",
                          "inactive"],
        raw_da_method="all", require_pdf=True, search_pool=50,
        run_label=LABEL, output_base="./output/_kw_robustness",
        max_chars=24000, extract_findings=True,
    )


# Semantic Scholar's /paper/search 500s and rate-limits transiently. Retry the WHOLE cohort only
# while it dies at SEARCH (no papers / search failed) — once papers are in, per-paper failures are
# already caught inside the cohort, so we stop retrying and keep that result. Backoff caps at 10min;
# ~24 attempts spans the night.
MAX_ATTEMPTS = 24
report = ""
for attempt in range(1, MAX_ATTEMPTS + 1):
    report = _run()
    low = (report or "").lower()
    search_failed = ("paper search failed" in low or "no papers to process" in low)
    if not search_failed:
        print(f"[attempt {attempt}] search succeeded — proceeding with this run.")
        break
    wait = min(600, 45 * attempt)
    print(f"[attempt {attempt}/{MAX_ATTEMPTS}] Semantic Scholar search failed (transient); "
          f"retrying in {wait}s ...\n   {report.splitlines()[-1][:160] if report else ''}")
    time.sleep(wait)

print("\n===== REPORT =====")
print(report)

# ---- per-paper manifest summary ----
man = os.path.join(COHORT, "papers.csv")
if os.path.isfile(man):
    m = pd.read_csv(man)
    print(f"\n===== papers.csv ({len(m)} papers) =====")
    cols = [c for c in ["pmcid", "chosen_gse", "ownership", "analyzed", "status", "da_method",
                        "n_findings", "enrichment_edges", "chain_gsea_pathways",
                        "agree_confirmed", "agree_not_detected"] if c in m.columns]
    with pd.option_context("display.max_colwidth", 22, "display.width", 240):
        print(m[cols].to_string(index=False))
    print(f"\nanalyzed: {int((m.get('analyzed') == True).sum())}/{len(m)} | "
          f"text_ok: {int(m['status'].astype(str).str.startswith('text_ok').sum())}/{len(m)}")

# ---- batch summary (matrix types, contrasts, DEG, GSEA, deg_sanity per analyzed study) ----
summ = os.path.join(COHORT, "cohort_analysis", "summary.csv")
if os.path.isfile(summ):
    s = pd.read_csv(summ)
    print(f"\n===== cohort_analysis/summary.csv ({len(s)} analyzed studies) =====")
    cols = [c for c in ["accession", "matrix_type", "da_method", "n_contrasts", "n_deg",
                        "n_gsea_sig", "deg_sanity", "status"] if c in s.columns]
    with pd.option_context("display.max_colwidth", 26, "display.width", 240):
        print(s[cols].to_string(index=False))

# ---- chain_view richness ----
cv = os.path.join(COHORT, "csv", "chain_view.csv")
if os.path.isfile(cv):
    d = pd.read_csv(cv)
    print(f"\n===== chain_view.csv: {len(d)} chains across "
          f"{d['study_id'].nunique() if 'study_id' in d else '?'} studies =====")
    if len(d):
        top = d.reindex(d["nes"].abs().sort_values(ascending=False).index)
        print(top[["study_id", "pathway_name", "direction", "nes", "fdr"]].head(12).to_string(index=False))

print("\nDONE.")
