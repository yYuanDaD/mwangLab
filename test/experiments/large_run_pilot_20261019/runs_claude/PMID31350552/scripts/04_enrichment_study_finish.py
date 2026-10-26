import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import numpy as np
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID31350552"
run = native.RunRecorder.open(RUN); case = run.case("GSE129962")
paper = case.evidence_item("paper:PMC7177479.paper.md")
adir = case.dir / "aligned"
counts = json.load(open(case.dir / "results" / "deg_counts.json"))

# ---------- enrichment: GSEA Hallmark on the two planned edgeR exercise contrasts
# edgeR 'stat' is the unsigned QL F statistic, so rank by signed sqrt(F) (= signed |t| for a 1-df test).
enr = {}
for name, fn in [("cond_EX6_vs_RA6_geno-WT", "DEG_results_WT_EX6_vs_WT_RA6.csv"), ("cond_EX6_vs_RA6_geno-DH", "DEG_results_DH_EX6_vs_DH_RA6.csv")]:
    od = case.dir / "results" / "gsea" / name
    od.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(case.dir / "results" / "edger" / name / fn, index_col=0)
    d["signed_sqrtF"] = np.sign(d["log2FoldChange"]) * np.sqrt(d["stat"])
    d.to_csv(od / "ranked_ensembl.csv")
    col = native.collapse_to_genes(od / "ranked_ensembl.csv", od / "ranked_symbol.csv", mapping_csv=adir / "gene_annotation.csv",
                                   mapping_column="GeneSymbol", rule="max_abs_score", score_column="signed_sqrtF")
    fid = native.feature_id_report(od / "ranked_symbol.csv")
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(od / "ranked_symbol.csv"), organism="Mouse",
                               ranking_metric="signed_sqrtF", output_dir=str(od))
        outs = [case.add_output(p, f"gsea_{name}") for p in native.find_outputs(od, "*GSEA*.csv")]
        g = pd.read_csv(outs[0]["path"]) if outs else pd.DataFrame()
        top = {}
        if len(g):
            qcol = next((c for c in g.columns if c.lower() in ("fdr q-val", "fdr_q-val", "fdr")), None)
            ncol = next((c for c in g.columns if c.upper() == "NES"), None)
            tcol = next((c for c in g.columns if c.lower() in ("term", "name")), g.columns[0])
            if qcol and ncol:
                sig = g[pd.to_numeric(g[qcol], errors="coerce") < 0.05]
                top = {"n_q<0.05": int(len(sig)), "up": sig[sig[ncol] > 0][tcol].tolist(), "down": sig[sig[ncol] < 0][tcol].tolist()}
        enr[name] = top
        case.decide("enrichment", final={"method": "GSEA preranked (gseapy)", "subset": name, "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm",
            "organism": "Mouse", "feature_id_type": "Ensembl gene -> deposited GeneSymbol", "ranking_metric": "sign(log2FC)*sqrt(QL F) from edgeR",
            "id_mapping": col.get("mapping_record", col), "feature_id_report": fid, "outputs": outs, "summary": top,
            "paper_comparison": "paper used GSEA 2.2.3 with MSigDB 3.0 hallmark + canonical pathways (S5.8.p1)"},
            evidence=outs + [paper], paper={"locator": "S5.8.p1"}, confidence="medium", execution_status="completed",
            reasoning="Paper reports Hallmark GSEA for the exercise contrasts (S6.4.p4/p5, FIG2F). Full ranking, no gene-list threshold.")
    except native.NativeToolError as err:
        enr[name] = {"error": str(err)}
        case.decide("enrichment", final={"method": "GSEA preranked (gseapy)", "subset": name, "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm",
            "organism": "Mouse", "feature_id_type": "gene symbol", "id_mapping": col.get("mapping_record", col), "execution_error": str(err)},
            evidence=[paper], confidence="medium", execution_status="failed", reasoning="GSEA failed")
    print(name, json.dumps(enr[name])[:1500])

# ---------- study
paper_counts = {"cond_EX6_vs_RA6_geno-WT": 2529, "cond_EX6_vs_RA6_geno-DH": 2391, "geno_cond_DH_EX6_vs_WT_RA6": 65,
                "geno_DH_vs_WT_cond-RA3": 56, "geno_DH_vs_WT_cond-RA6": 781, "cond_RA3_vs_RA6_geno-WT (6M vs 3M)": 310, "cond_RA3_vs_RA6_geno-DH (6M vs 3M)": 1643}
case.write_json("reproduction_plan.json", {
    "paper_aligned": ["edgeR QL two-arm: WT EX6 vs RA6; DH EX6 vs RA6; padj<0.05, no FC cutoff"],
    "declared_deviation": ["genotype-by-exercise interaction via DESeq2 joint cell-means model (edgeR executor has no interaction)",
                           "edgeR gene filter CPM>=1 in >=5 compared samples (paper rule not reported)"],
    "exploratory": ["all other suitability comparisons from the joint DESeq2 model", "per-sex joint DESeq2 contrasts",
                    "age contrasts without RUVr"]})
case.write_json("reproduction_summary.json", {"status": "finished", "deg_counts": counts, "paper_counts": paper_counts, "gsea": enr,
    "notes": ["Exercise contrasts reproduce in size order of magnitude but fewer DEGs (WT 1724 vs 2529; DH 1409 vs 2391); DH direction differs (781 up/628 down vs paper 867 up/1524 down).",
              "Genotype effect at 6 months reproduces poorly (64 joint DESeq2 vs 781); Dsp transcript is not clearly lower in DH than WT at RA6.",
              "EX6 and RA6 samples come from different featureCounts runs (ERCC-ID pattern); exercise simple contrasts are aliased with that run; interaction unaffected.",
              "DH_EX6 GSM3728660 (female) has a heart-failure signature (Nppa, Nppb, Myh7 high): the mouse that stopped exercising (S6.4.p6); kept as in the paper."]})
case.decide("study", final={"route": "paper_aligned",
    "components": {"paper_aligned": ["cond_EX6_vs_RA6_geno-WT (edgeR)", "cond_EX6_vs_RA6_geno-DH (edgeR)"],
                   "declared_deviation": ["geno_cond_DH_EX6_vs_WT_RA6 (DESeq2 joint)"],
                   "exploratory": ["other joint DESeq2 comparisons", "per-sex comparisons"]},
    "deg_counts_applied_threshold": {k: v.get("n_significant") for k, v in counts.items()}, "paper_counts": paper_counts,
    "exploratory_reason": "per-sex male cells have n=3 (female exercise cells n=1-2 not analyzable); non-exercise comparisons are context only"},
    evidence=[paper], paper={"locator": "S6.4.p4"}, confidence="medium",
    reasoning="Exercise contrasts run with the paper's method and threshold; the interaction as a declared deviation.")
main = counts["cond_EX6_vs_RA6_geno-DH"]
print(case.finish(n_deg=main["n_significant"], deg_sanity=main["deg_sanity"]))
print(run.finish())
