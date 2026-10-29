"""Reproduction artifacts, study record, finish."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID35025912"
run = native.RunRecorder.open(RUN)
case = run.case("PMID35025912")
cdir = case.dir
deg = json.loads((cdir / "results" / "deg_counts.json").read_text(encoding="utf-8"))
tmm = json.loads((cdir / "results" / "audit_tmm" / "audit_tmm_counts.json").read_text(encoding="utf-8"))
gsea = json.loads((cdir / "results" / "gsea" / "gsea_summary.json").read_text(encoding="utf-8"))["summaries"]
cnt = {k: {x: v["paper_rule"][x] for x in ("n_significant", "n_up", "n_down")} for k, v in deg["counts"].items()}
pct_down = {k: round(100 * v["n_down"] / v["n_significant"], 1) if v["n_significant"] else None for k, v in cnt.items()}
plan = {"paper_route": "limma-voom with RIN covariate, 14,789 genes, FDR<0.05 & logFC>1 (S3.5.p1)",
        "executed_route": "limma (inmoose) on log2(CPM+1), ~ 0 + cell + rin on 48 samples, median-CPM>=0.5 filter (14,789 genes, identical), same contrasts and threshold",
        "deviation": "no voom precision weights, no TMM (library-size CPM), inmoose instead of R limma",
        "contrasts": {"paper_planned": ["PLN_HIinLRT", "PLN_HIinHRT", "PLN_DELTA", "SOL_HIinLRT", "SOL_HIinHRT", "SOL_DELTA"],
                      "exploratory": [k for k in cnt if k.startswith("line_")],
                      "not_run": "tissue comparisons (within-animal, no animal key)"},
        "enrichment": "Hallmark GSEA on moderated t instead of GO BP GSEA"}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
summary = {
    "deg_counts_paper_rule": cnt, "pct_down": pct_down,
    "paper_counts": {"PLN_HIinLRT": "744 (58.5% down)", "PLN_HIinHRT": "251 (66.5% down)",
                     "SOL_HIinLRT": "294 (57.1% down)", "SOL_HIinHRT": "326 (57.1% down)", "common_all_four": 40},
    "common_all_four_ours": deg["common_all_four_HI_contrasts"],
    "audits": {"no_rin": deg["audit_paper_rule"]["no_rin"], "per_muscle_models": deg["audit_paper_rule"]["per_muscle"],
               "tmm_logcpm": tmm["counts"],
               "fdr_0.001_rule_S2.2.p2": {k: v["audit_padj0.001"]["n_significant"] for k, v in deg["counts"].items()}},
    "genes_of_interest": {"ours": deg["genes_of_interest"], "paper": deg["paper_genes_of_interest"]},
    "agreement": ("Gene filter reproduced exactly (14,789). Atrogene log2FCs match S3.7.p1 within 0.06 (e.g. PLN LRT Trim63 "
                  "2.56 vs 2.55, Fbxo32 2.74 vs 2.74). DEG counts are 50-70% of the paper's, with the same ordering in "
                  "plantaris (LRT >> HRT) and soleus (HRT ~ LRT). Plain CPM gives an up-majority; the TMM audit restores "
                  "the paper's down-majority (57-65% down), so the direction split is a normalisation effect. The DELTA "
                  "interaction has 0-2 DEGs, consistent with the paper reporting no DELTA DEG count and using GSEA."),
    "gsea": gsea,
    "gsea_vs_paper": ("PLN DELTA: unfolded protein response, MYC targets (ribosome/RNA metabolism) and TNFa/NFkB higher in "
                      "LRT, OXPHOS lower: consistent in direction with the paper's stronger RNA-metabolism/ribosome-biogenesis "
                      "up-regulation and nucleotide-metabolism down-regulation in LRT plantaris (S4.p5, S4.p7). Different "
                      "library; not a term-level reproduction."),
}
s_ev = case.write_json("reproduction_summary.json", summary, role="reproduction_summary")
print(json.dumps(summary, indent=1, default=str)[:4000])
case.decide("study",
            final={"route": "declared_deviation",
                   "summary": "paper contrasts, gene filter and threshold on limma log-CPM with RIN (joint 48-sample model) instead of voom",
                   "deg_counts_paper_rule": cnt, "paper_counts": summary["paper_counts"],
                   "exploratory": plan["contrasts"]["exploratory"],
                   "estimand_note": "no trained-vs-sedentary samples; 'exercise' enters only as the endurance-trainability line (associational)"},
            evidence=[s_ev], paper={"locator": "S3.5.p1"}, confidence="medium",
            reasoning="All gates valid; the paper's voom route is blocked by executor limits, so the run is a declared deviation.",
            execution_status="completed", decision_status="valid")
print(case.finish(n_deg=cnt["PLN_HIinLRT"]["n_significant"], deg_sanity="ok"))
print(run.finish())
