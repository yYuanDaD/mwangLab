"""Corrected GSEA term summary, reproduction artifacts, study record, finish."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json, glob
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID33486778"
run = native.RunRecorder.open(RUN)
case = run.case("PMID33486778")
cdir = case.dir

# 03_enrichment.py read the gseapy 'Name' column ('prerank') instead of 'Term' for the term lists;
# rebuild the per-contrast lists from the saved tables (NES/FDR counts in the record were correct).
gsea = {}
for n in ("FOinLRT", "FOinHRT", "DELTA"):
    t = pd.read_csv(glob.glob(str(cdir / "results" / "gsea" / n / "*GSEA_Hallmark*.csv"))[0])
    s = t[t["FDR q-val"] < 0.05].sort_values("NES", ascending=False)
    gsea[n] = {"n_fdr_lt_0.05": int(len(s)),
               "up": [f"{r.Term} (NES {r.NES:.2f})" for r in s.itertuples() if r.NES > 0],
               "down": [f"{r.Term} (NES {r.NES:.2f})" for r in s.itertuples() if r.NES < 0]}
gs = case.write_json("results/gsea/gsea_summary_corrected.json", gsea, role="gsea_summary_corrected")

deg = json.loads((cdir / "results" / "deg_counts.json").read_text(encoding="utf-8"))
cnt = {k: {x: v["paper_rule"][x] for x in ("n_significant", "n_up", "n_down")} for k, v in deg["counts"].items()}
plan = {"paper_route": "edgeR TMM + limma-voom, ~ group + RIN, median CPM >= 0.5 filter, FDR<0.001 & FC>2",
        "executed_route": "limma (inmoose) on log2(CPM+1), ~ 0 + grp + rin, same filter (14,956 genes), same contrasts, same threshold",
        "deviation": "no voom precision weights, no TMM (library-size CPM), inmoose instead of R limma",
        "contrasts": {"paper_planned": ["FOinLRT", "FOinHRT", "DELTA"], "exploratory": ["LRTvsHRT_CTRL", "LRTvsHRT_FO"]},
        "enrichment": "Hallmark GSEA on moderated t instead of GO BP GSEA"}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
summary = {
    "deg_counts_paper_rule": cnt,
    "paper_counts": {"FOinLRT": "1866 (92.4% up)", "FOinHRT": "2460 (79.6% up)", "common": 1612, "DELTA": "not reported"},
    "ours": {"FOinLRT": f"{cnt['FOinLRT']['n_significant']} ({cnt['FOinLRT']['n_up'] / cnt['FOinLRT']['n_significant']:.1%} up)",
             "FOinHRT": f"{cnt['FOinHRT']['n_significant']} ({cnt['FOinHRT']['n_up'] / cnt['FOinHRT']['n_significant']:.1%} up)",
             "common": deg["common_FO_DEGs"]},
    "audit_without_rin": deg["audit_without_rin_paper_rule"],
    "gene_filter": "14,956 genes, identical to the paper (S3.4.p1)",
    "agreement": ("FO response larger in HRT than LRT, as in the paper; counts 86-95% of the paper's; fewer down-regulated "
                  "genes than the paper (likely TMM: FO up-regulates thousands of genes, which TMM offsets and plain CPM does not)."),
    "gsea": gsea,
    "gsea_vs_paper": ("DELTA: protein secretion and unfolded protein response lower in LRT than HRT, consistent in direction with "
                      "the paper's ER-stress (GO:0034976) and Golgi vesicle transport (GO:0048193) findings (FIG5, FIG6); "
                      "different library, so not a term-level reproduction."),
}
case.write_json("reproduction_summary.json", summary, role="reproduction_summary")
print(json.dumps(summary, indent=1))

case.decide("study",
            final={"route": "declared_deviation",
                   "summary": "paper contrasts and threshold on limma log-CPM with RIN instead of voom/TMM",
                   "deg_counts_paper_rule": cnt, "paper_counts": summary["paper_counts"],
                   "gsea_corrected_summary": str(cdir / "results" / "gsea" / "gsea_summary_corrected.json"),
                   "enrichment_record_note": "enrichment record lists 'prerank' in place of term names (script bug); corrected lists in gsea_summary_corrected.json",
                   "exploratory": ["LRTvsHRT_CTRL", "LRTvsHRT_FO"]},
            evidence=[gs, case.add_output(cdir / "reproduction_summary.json", "reproduction_summary_json")],
            paper={"locator": "S3.5.p1"}, confidence="medium",
            reasoning="All gates valid; the paper's voom route is blocked by executor limits, so the run is a declared deviation.",
            execution_status="completed", decision_status="valid")
print(case.finish(n_deg=cnt["FOinHRT"]["n_significant"], deg_sanity="ok"))
print(run.finish())
