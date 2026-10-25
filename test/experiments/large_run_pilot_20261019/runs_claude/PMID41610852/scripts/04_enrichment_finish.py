"""Enrichment (GSEA Hallmark on primary per-arm results), study record, run finish."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41610852"
run = native.RunRecorder.open(RUN)
case = run.case("GSE312780")
D = case.dir
P = D / "results/primary_16subjects"
paper_md = case.evidence_item("paper:PMC13237580.paper.md")
summ = json.load(open(D / "results/execution_summary.json"))

# id -> symbol from the deposited matrix's own gene_name column
raw = pd.read_csv("data/GSE312780/GSE312780_salmon.merged.gene_counts.tsv.gz", sep="\t", usecols=["gene_id", "gene_name"])
map_csv = D / "results/gene_id_to_symbol.csv"
raw.set_index("gene_id").to_csv(map_csv)
map_item = case.add_output(map_csv, "id_mapping")
gsea = {}
for name in ["time_post_vs_pre_arm-BFRT", "time_post_vs_pre_arm-CREST"]:
    deg = P / f"DEG_results_{name}.csv"
    fid = native.feature_id_report(deg)
    col = native.collapse_to_genes(deg, D / "results/enrichment" / name / f"DEG_symbols_{name}.csv",
                                   mapping_csv=map_csv, mapping_column="gene_name", rule="max_mean")
    sym_item = case.add_output(col["output"], f"deg_symbols_{name}")
    out_dir = D / "results/enrichment" / name
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=col["output"], organism="Human",
                               ranking_metric="stat", output_dir=str(out_dir))
        outs = [p for p in native.find_outputs(out_dir, "*GSEA*.csv")]
        items = [case.add_output(p, f"gsea_{name}") for p in outs]
        top = {}
        if outs:
            t = pd.read_csv(outs[0])
            fdr_col = next((c for c in t.columns if c.lower() in ("fdr q-val", "fdr", "padj")), None)
            nes_col = next((c for c in t.columns if c.upper() == "NES"), None)
            if fdr_col and nes_col:
                t = t.sort_values(fdr_col)
                top = t[[t.columns[1] if "Term" not in t.columns else "Term", nes_col, fdr_col]].head(12).to_dict("records")
        gsea[name] = {"outputs": outs, "top": top}
        case.decide("enrichment",
                    final={"method": "GSEA preranked (gseapy) on DESeq2 Wald stat", "subset": name,
                           "gene_sets": "MSigDB Hallmark (h.all, Human)", "organism": "Human",
                           "feature_id_type": fid["dominant_type"], "ranking_metric": "stat",
                           "id_mapping": {**col["mapping_record"], "n_unmapped": col["n_unmapped"],
                                          "n_features_collapsed": col["n_features_collapsed"]},
                           "paper_route": {"method": "clusterProfiler gseKEGG (organism 'mmu' as written)", "status": "blocked",
                                           "reason": "repository GSEA executor provides MSigDB Hallmark only, no KEGG"},
                           "outputs": outs},
                    evidence=[case.add_output(P / f"DEG_results_{name}.csv", f"deg_{name}"), sym_item, map_item] + items,
                    paper={"locator": "S8.3.15.p1; S2.4.p2"}, reasoning="Paper ran GSEA per arm; Hallmark run as declared deviation.",
                    confidence="medium", execution_status="completed")
    except native.NativeToolError as e:
        gsea[name] = {"error": str(e)}
        case.decide("enrichment",
                    final={"method": "GSEA preranked (gseapy) on DESeq2 Wald stat", "subset": name,
                           "gene_sets": "MSigDB Hallmark (h.all, Human)", "organism": "Human",
                           "feature_id_type": fid["dominant_type"], "execution_error": str(e),
                           "id_mapping": col["mapping_record"]},
                    evidence=[sym_item, map_item], reasoning="GSEA failed", confidence="medium",
                    execution_status="failed")
json.dump(gsea, open(D / "results/enrichment/gsea_summary.json", "w"), indent=1, default=str)
print(json.dumps(gsea, indent=1, default=str)[:4000])

prim = summ["primary_16subjects"]["counts"]
paper_n = {"time_post_vs_pre_arm-BFRT": 110, "time_post_vs_pre_arm-CREST": 18, "arm_time_BFRT_post_vs_CREST_pre": None}
comparison = {k: {"ours_applied": v["applied"]["n_significant"], "up": v["applied"]["n_up"], "down": v["applied"]["n_down"],
                  "paper": paper_n[k]} for k, v in prim.items()}
plan = {"paper_route": "DESeq2 ~ cohort + cohort:person_within_cohort + cohort:timepoint on tximport lengthScaledTPM counts, "
                       "apeglm LFC, padj<0.05 & |log2FC|>=0.585, 16 subjects",
        "executed_route": "DESeq2 (pydeseq2) ~ subject + tcell (same column space) on rounded unscaled salmon gene counts, "
                          "MLE LFC, same threshold, 16 subjects (Resist18 excluded as the inferred PCA outlier)",
        "deviations": ["matrix: unscaled salmon counts instead of lengthScaledTPM", "no apeglm shrinkage",
                       "excluded participant inferred, not named in the paper", "GSEA Hallmark instead of KEGG"],
        "exploratory": ["17-subject sensitivity", "between-arm cross-sectional contrasts", "male-only", "female CREST only (n=3, df=2)"]}
case.write_json("reproduction_plan.json", plan)
case.write_json("reproduction_summary.json", {"deg_comparison": comparison, "all_units": summ, "gsea": gsea,
                                              "note": "MLE LFC without apeglm shrinkage keeps more low-count genes above "
                                                      "|log2FC| 0.585, plausibly explaining higher counts than the paper; "
                                                      "direction of finding (BFRT >> CREST) reproduced."})
case.decide("study",
            final={"route": "declared_deviation",
                   "exploratory_units": {"exploratory_female_CREST": "fewer than 3 residual df (3 subjects, df 2)",
                                         "others": "outside the paper's planned set"},
                   "deg_comparison": comparison},
            evidence=[paper_md], reasoning="Paper design, model and threshold reproduced; matrix, LFC shrinkage, "
                                           "excluded-sample identity and KEGG GSEA are declared deviations.",
            confidence="medium", execution_status="completed")
b = prim["time_post_vs_pre_arm-BFRT"]["applied"]
print(case.finish(n_deg=b["n_significant"], deg_sanity=b["deg_sanity"]))
print(run.finish())
