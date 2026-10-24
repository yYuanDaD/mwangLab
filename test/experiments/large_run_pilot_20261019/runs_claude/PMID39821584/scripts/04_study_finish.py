"""Reproduction artifacts, study record, finish."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID39821584"
run = native.RunRecorder.open(RUN)
case = run.case("PMID39821584")
cdir = case.dir
deg = json.loads((cdir / "deg_counts.json").read_text(encoding="utf-8"))
enr = json.loads((cdir / "enrichment_summary.json").read_text(encoding="utf-8"))
planned = ["grp_r25_vs_sed", "grp_r50_vs_sed", "grp_r75_vs_sed", "grp_rU_vs_sed"]
reported = {"grp_r25_vs_sed": (1347, 25), "grp_r50_vs_sed": (1823, 78), "grp_r75_vs_sed": (1103, 15), "grp_rU_vs_sed": (1107, 16)}

# qPCR-validated genes (S3.p5): direction check in the joint model
qpcr = ["Aldh1l1", "Xdh", "Car4", "Aldh9a1", "Pik3r1", "Fkbp5", "Foxo1", "Klf10", "Fibin", "Sesn1", "Phyhd1", "Lars2"]
genes = {}
for name in planned:
    t = pd.read_csv(cdir / "results" / "enrichment" / name / f"DEG_results_{name}_symbols.csv", index_col=0)
    genes[name] = {g: {"log2FC": round(float(t.loc[g, "log2FoldChange"]), 3), "pvalue": float(t.loc[g, "pvalue"]),
                       "padj": None if pd.isna(t.loc[g, "padj"]) else float(t.loc[g, "padj"])}
                   for g in qpcr if g in t.index}

cnt = {k: deg["joint"][k]["paper_rule_p<=0.05"] for k in deg["joint"]}
table = {k: {"ours_joint_p<=0.05": cnt[k]["n_significant"], "up": cnt[k]["n_up"], "down": cnt[k]["n_down"],
             "ours_pairwise_audit_p<=0.05": deg["audit_pairwise"][k]["p<=0.05"],
             "paper_p<=0.05": reported[k][0],
             "ours_joint_FDR<=0.05&|LFC|>=1": deg["joint"][k]["secondary_FDR<=0.05&|LFC|>=1"]["n_significant"],
             "ours_pairwise_FDR<=0.05&|LFC|>=1": deg["audit_pairwise"][k]["FDR<=0.05&|LFC|>=1"],
             "paper_FDR<=0.05&|LFC|>=1": reported[k][1]} for k in planned}
plan = {"paper_route": "Novogene DESeq2 (R 1.20.0) per exercise group vs HFD-C, raw p <= 0.05",
        "executed_route": "pydeseq2 joint model ~ grp on the 30 HFD samples, Wald contrasts r25/r50/r75/rU vs sed, raw p <= 0.05",
        "audit": "pydeseq2 two-group fit per planned pair (12 samples each), the presumed Novogene structure",
        "exploratory": [k for k in cnt if k not in planned],
        "not_run": ["HFD-C vs pooled exercise (1094 DEGs): pools levels", "DRomics dose-response: no executor",
                    "NFD-C (deposited, not in paper)"],
        "enrichment": "Hallmark GSEA (full ranking) and Enrichr KEGG/GO ORA on an audit FDR<0.05 list; paper used clusterProfiler KEGG on raw p<=0.05 & mean count>=25"}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
summary = {
    "deg_table_planned": table,
    "exploratory_counts_p<=0.05": {k: cnt[k]["n_significant"] for k in cnt if k not in planned},
    "direction_pattern": ("paper: r50 has more up than down; r75 and rU more down. Ours (joint): r50 1273 up/1124 down; "
                          "r75 438/682; rU 484/682 -> same pattern"),
    "ranking": "r50 has the most DEGs under both rules in ours and in the paper",
    "qpcr_genes_lfc": genes,
    "agreement": ("Pairwise audit reproduces the paper's p<=0.05 counts within 3-4% (1308/1783/1061/1070 vs "
                  "1347/1823/1103/1107). The joint 30-sample model (skill route) gives 1482/2397/1120/1166: more power "
                  "from the shared dispersion, mainly for r25 and r50. FDR<=0.05&|LFC|>=1 counts are a little above the paper "
                  "(joint 31/119/19/23, pairwise 30/90/18/26 vs 25/78/15/16) with the same ordering."),
    "enrichment": {k: {"gsea_top": [(t["Term"], round(t["NES"], 2)) for t in (v["gsea"].get("top") or [])[:5]],
                       "ora_up_kegg_top": [t["Term"] for t in (v["ora_up"].get("top_kegg") or [])[:5]],
                       "ora_down_kegg_top": [t["Term"] for t in (v["ora_down"].get("top_kegg") or [])[:5]]}
                   for k, v in enr.items()},
    "enrichment_vs_paper": ("r50 down list includes MAPK signalling (paper: MAPK enriched in r50 down); r75 up list "
                            "enriched for PPAR signalling (paper: PPAR in r75 and r50 up); tryptophan metabolism up in r50 and "
                            "rU (paper: tryptophan in r50 up). Different library/list rule; not a term-level reproduction."),
}
s_ev = case.write_json("reproduction_summary.json", summary, role="reproduction_summary")
print(json.dumps(summary, indent=1, default=str)[:6000])
case.decide("study",
            final={"route": "paper_aligned",
                   "summary": "paper contrasts, DESeq2 on raw featureCounts, paper threshold raw p<=0.05; joint 30-sample model",
                   "deg_counts_paper_rule": table, "exploratory": plan["exploratory"],
                   "exploratory_reason": "exercise-vs-exercise pairs not planned by the paper"},
            evidence=[s_ev], paper={"locator": "FIG2"}, confidence="high",
            reasoning="All gates valid; DESeq2 on raw counts as in the paper, exact paper threshold.",
            execution_status="completed", decision_status="valid")
print(case.finish(n_deg=cnt["grp_r50_vs_sed"]["n_significant"], deg_sanity="ok"))
print(run.finish())
