"""Write discrepancy / plan / summary artifacts, finish the run."""
import json
from common import *  # noqa
from tools import native

native.enable_native_mode()
run = native.RunRecorder.open(RUN_DIR)

DISC = [
    {"item": "direct post-vs-pre test", "paper": "not performed; exercise effect = Δlog2FC vs controls (S2.2.p2)",
     "data": "9 complete pre/post pairs", "class": "requires_explicit_deviation", "case": "case_01"},
    {"item": "normalization", "paper": "edgeR (TMM default presumed; not stated)",
     "data": "inmoose edgeR and preprocess_counts use library size only; median-of-ratios size factor / library "
             "size averages 0.88 (ctrl) vs 1.07 (pre) and 1.10 (post) -> composition shift ~0.27 log2 between "
             "controls and DM1 that TMM would remove; inflates BH counts in pre/post-vs-ctrl, cancels in Δlog2FC",
     "class": "requires_explicit_deviation", "case": "case_02, case_03"},
    {"item": "gene filter", "paper": "'Genes with less than 10 counts in each samples were filtered out' (S4.4.p1)",
     "data": "literal reading (>=10 in >=1 sample) keeps 20,852 (pre+ctrl) / 21,619 (post+ctrl); authors' sheets "
             "list 18,762 / 18,804 genes; no tested rule reproduces those counts",
     "class": "executable_without_change", "case": "all"},
    {"item": "authors' DEG count, grouped pre vs ctrl", "paper": "deposited edgeR sheet: 176 genes pass |logFC|>2 & P<0.05",
     "data": "this run: 475; logFC Pearson r=0.926 over 17,136 shared genes", "class": "executable_without_change",
     "case": "case_02"},
    {"item": "individual analyses", "paper": "18 edgeR fits, 1 sample vs 6 controls (S2.2.p2)",
     "data": "two-arm executors need >=2 per arm (tools/analysis_policy.py:16); run as one limma model "
             "~0+C(unit) on log2(CPM+1)", "class": "requires_explicit_deviation", "case": "case_03"},
    {"item": "age covariate", "paper": "controls mean 32 y vs DM1 48 y (S2.5.p2)", "data": "age not in GEO metadata",
     "class": "executable_without_change (affects only disease-vs-control contrasts)", "case": "case_02, case_03"},
    {"item": "deposited supplementary edgeR_output.xlsx", "paper": "4 sheets (grouped pre, grouped post, "
     "individual pre, individual post)", "data": "download_supplementary_files converted only sheet 1 and deleted the "
     "xlsx (tools/geo_tools.py:85 pd.read_excel(file_path) default sheet; :89 os.remove)",
     "class": "executable_without_change (re-downloaded for concordance)", "case": "case_02, case_03"},
]

summaries = {
    "case_01": {"route": "declared_deviation", "method": "DESeq2 ~ subject + grp, post vs pre (18 DM1 samples)",
                "threshold": "paper rule on deviation route: raw P<0.05 & |log2FC|>2",
                "result": "20 DEGs (18 up, 2 down) by paper rule; audit BH padj<0.05: 166 (134 up, 32 down) of 16,275",
                "top_genes": "PXDN, FSCN1, COL4A1, COL4A2, COL5A3, NID2 up (ECM/basement membrane) - consistent "
                             "with S2.3.p1 (6 ECM genes up after training)",
                "enrichment": "Hallmark GSEA: EMT, IFN-gamma/alpha, allograft rejection, inflammatory response, "
                              "complement, angiogenesis up; MYC targets, OXPHOS, UPR, protein secretion down. ORA "
                              "(audit list): ECM organization, basement membrane, ECM-receptor interaction"},
    "case_02": {"route": "declared_deviation", "method": "edgeR QL (inmoose, no TMM), ~ grp, separate fits",
                "threshold": "paper rule: raw P<0.05 & |log2FC|>2",
                "result": "pre vs ctrl 475 (223 up/252 down); post vs ctrl 512 (377 up/135 down); grouped Δlog2FC: "
                          "of 448 pre-vs-ctrl DEGs, 274 rescued / 72 misrescued / 0 overrescued; dysregulation "
                          "score 2.83 -> 2.38",
                "concordance": "pre vs ctrl logFC vs authors' sheet r=0.926"},
    "case_03": {"route": "exploratory", "method": "limma multilevel ~0+C(unit) on log2(CPM+1)",
                "threshold": "paper rule on deviation route",
                "result": "per-individual mean % rescue: 523 76.9 (highest), 2005 6.2 (lowest), 907/2005/1242 "
                          "smallest dysregulation-score drops; paper: 523 73%, 2005 -7%, 907 and 2005 minor changes",
                "concordance": "individual logFC vs authors' sheets r=0.49-0.75"},
}
for cid, s in summaries.items():
    case = run.case(cid)
    (case.dir / "paper_data_discrepancies.json").write_text(json.dumps(
        [d for d in DISC if d["case"] == "all" or cid in d["case"]], indent=2), encoding="utf-8")
    (case.dir / "reproduction_plan.json").write_text(json.dumps(
        {"paper_route": STUDY_MAP["paper_method"], "this_case": s["method"], "route": s["route"],
         "threshold": s["threshold"]}, indent=2), encoding="utf-8")
    (case.dir / "reproduction_summary.json").write_text(json.dumps(s, indent=2), encoding="utf-8")
print(json.dumps(run.finish(), indent=1, default=str)[:3000])
