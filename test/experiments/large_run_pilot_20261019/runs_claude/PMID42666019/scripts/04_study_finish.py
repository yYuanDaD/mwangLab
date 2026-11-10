"""Gate 11 (study), reproduction plan/summary, case and run finish."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42666019"
CASE = "PMID42666019"
run = native.RunRecorder.open(RUN)
case = run.case(CASE)
counts = json.loads((case.dir / "results" / "threshold_counts.json").read_text(encoding="utf-8"))
genes = json.loads((case.dir / "results" / "paper_gene_check.json").read_text(encoding="utf-8"))
recs = json.loads((case.dir / "decisions.json").read_text(encoding="utf-8"))
audit = {r["final"]["subset"]: r["final"]["threshold_counts"] for r in recs
         if r["stage"] == "execution" and str(r["final"].get("subset", "")).startswith("audit_")}

plan = {"route": "DESeq2 on deposited raw counts, |log2FC| > 1 and padj < 0.05 (paper S2.16.p1)",
        "model": "joint DESeq2 ~ grp on all 9 samples (SED/CE/EE x 3); Wald contrasts CE vs SED, EE vs CE (planned), EE vs SED (exploratory)",
        "declared_deviation": "joint model instead of the per-pair fits the paper's vendor pipeline most likely used; per-pair refits run as audit",
        "enrichment": "Enrichr ORA (GO BP/MF/CC 2023, KEGG 2019 Mouse) on the applied-threshold DEG lists; paper used GO + KEGG (tool not named)"}
pl_ev = case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
summ = {"threshold": "padj < 0.05 and |log2FC| > 1 (paper)",
        "deg_counts": {k: {"n": v["paper_threshold"]["n_significant"], "up": v["paper_threshold"]["n_up"],
                           "down": v["paper_threshold"]["n_down"], "paper": "not_reported (volcano only)"}
                       for k, v in counts.items()},
        "audit_pairwise_refit": {k: {"n": v["n_significant"], "up": v["n_up"], "down": v["n_down"]} for k, v in audit.items()},
        "paper_gene_check": genes,
        "comparison_to_paper": [
            "Prkag3, Cox7a1, Cox6a2, Cox8b are up in CE vs SED (log2FC 1.25-2.73, padj <= 0.0011), consistent with S3.8.p1",
            "the same genes are NOT significantly higher in EE than CE (log2FC 0.02-0.66, padj >= 0.29), so the paper's 'sequential increase SED < CE < EE' is supported for SED -> CE and EE vs SED, not for CE -> EE",
            "Myog is up in EE vs CE (log2FC 1.28, padj < 1e-4) and EE vs SED (2.03), consistent with FIG8f; Myod1 is unchanged (paper reports higher Myod by qPCR/WB)",
            "ORA top terms: CE vs SED = xenobiotic/glutathione metabolism, complement; EE vs CE = muscle contraction / myofibril; the paper's fatty-acid-metabolism enrichment (FIG8a, pooled over groups) is not among the top terms of either planned contrast"]}
sm_ev = case.write_json("reproduction_summary.json", summ, role="reproduction_summary")
case.decide("study",
            final={"route": "paper_aligned",
                   "note": "paper method, input and threshold; one joint DESeq2 model across the three groups (per-pair refits as audit give 766 / 54 DEGs vs 834 / 47 joint)",
                   "exploratory": ["grp_EE_vs_SED (not shown in the paper)"],
                   "planned_results": {k: counts[k]["paper_threshold"]["n_significant"] for k in ("grp_CE_vs_SED", "grp_EE_vs_CE")}},
            evidence=[pl_ev, sm_ev], confidence="high", execution_status="completed",
            reasoning="All gates valid; planned contrasts executed with the paper's method and threshold.")
p = counts["grp_CE_vs_SED"]["paper_threshold"]
print(case.finish(n_deg=p["n_significant"], deg_sanity=p["deg_sanity"]))
print(run.finish())
