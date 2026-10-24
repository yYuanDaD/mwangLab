"""Reproduction artifacts, study records, finish."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40577041"
run = native.RunRecorder.open(RUN)
AGREE = {
    "PMID40577041_SM": ("FDR<0.05: 32 (27 up, 5 down) vs paper 34 (30 up, 4 down); Cox7a1 up at FDR<0.05 (log2FC 0.58, padj 0.018) as in "
                        "S3.3.p2; fast-fibre genes (Myh4, Myl1, Mylpf, Tnni2) down at p<0.05 as in S3.3.p2/FIG S2C-F. FDR<0.2: 415 vs "
                        "487. Hallmark GSEA: OXPHOS and fatty-acid metabolism up in ExT, consistent with the paper's Reactome TCA / "
                        "fatty-acid / aerobic-respiration terms."),
    "PMID40577041_MT": ("FDR<0.05: 0 vs paper 0. p<0.05: 371 vs paper 365 (TMM routes 306-371). Library-size-only voom gives a "
                        "degenerate p-value distribution here (0 genes at p<0.05)."),
    "PMID40577041_LV": ("FDR<0.05: 0 vs paper 0. p<0.05: 694 vs 738; p<0.01: 130 vs 121. Hallmark GSEA: OXPHOS up in ExT, "
                        "consistent with the paper's mitochondrial Reactome terms; n = 7 per group."),
}
for cid in AGREE:
    case = run.case(cid)
    cdir = case.dir
    t = cid.split("_")[-1]
    deg = json.loads((cdir / "results" / "deg_counts.json").read_text(encoding="utf-8"))
    gsea_p = cdir / "results" / "gsea" / "gsea_summary.json"
    gsea = json.loads(gsea_p.read_text(encoding="utf-8")) if gsea_p.exists() else None
    applied = {k: deg["applied_FDR<0.05"][k] for k in ("n_significant", "n_up", "n_down")}
    plan = {"paper_route": "voom/limma in Degust v4.1.5 (TMM), ExT vs Sed, paper CPM filter, FDR<0.05 (S2.10.p1)",
            "executed_route": f"limma (inmoose) on log2(TMM-CPM+1), ~ grp, filter {deg['filter']}, BH FDR<0.05",
            "deviation": "no voom precision weights (repository voom executor has no TMM; tools/limma_voom.R)",
            "audits": ["R limma-voom lib.size only", "edgeR QL TMM", "DESeq2"],
            "enrichment": "Hallmark GSEA instead of Reactome GSEA" if gsea else "not run (paper reports none for this fraction)"}
    case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
    summ = {"contrast": f"{t}_ExT_vs_Sed", "n_genes_tested": deg["n_genes_tested"], "applied_FDR<0.05": applied,
            "other_rules": {k: v for k, v in deg["primary_limma_tmm"].items() if k != "FDR<0.05"},
            "paper": deg["paper"], "audits": deg["audits"], "genes_of_interest": deg["genes_of_interest"],
            "agreement": AGREE[cid],
            "gsea": ({k: gsea.get(k) for k in ("n_fdr_lt_0.05", "up_in_ExT", "down_in_ExT", "paper_terms")} if gsea else None)}
    s_ev = case.write_json("reproduction_summary.json", summ, role="reproduction_summary")
    case.decide("study",
                final={"route": "declared_deviation",
                       "summary": "paper contrast, filter and threshold on limma with TMM log-CPM instead of Degust voom",
                       "deg_counts_applied": applied, "paper_counts": deg["paper"], "agreement": AGREE[cid]},
                evidence=[s_ev], paper={"locator": "S2.10.p1"}, confidence="medium",
                reasoning="All gates valid; the paper's voom+TMM route is blocked by the executor, so the run is a declared deviation.",
                execution_status="completed", decision_status="valid")
    print(cid, case.finish(n_deg=applied["n_significant"], deg_sanity="ok"))
print(run.finish())
