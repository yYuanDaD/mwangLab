"""Gate 10 (enrichment): GSEA Hallmark (mouse) on the planned contrasts."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, glob
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42277794"
run = native.RunRecorder.open(RUN)
case = run.case("PMID42277794")
cdir = case.dir
jd = cdir / "results" / "joint_deseq2"
targets = {"A_ExTctrl_vs_SEDctrl": "ex_EXT_vs_SED_exo-ctrl", "B_ExTexo_vs_SEDexo": "ex_EXT_vs_SED_exo-exo",
           "C_SEDexo_vs_SEDctrl": "exo_exo_vs_ctrl_ex-SED", "exploratory_EXTexo_vs_EXTctrl": "exo_exo_vs_ctrl_ex-EXT"}
focus = ["HALLMARK_TNFA_SIGNALING_VIA_NFKB", "HALLMARK_INFLAMMATORY_RESPONSE", "HALLMARK_BILE_ACID_METABOLISM",
         "HALLMARK_XENOBIOTIC_METABOLISM", "HALLMARK_FATTY_ACID_METABOLISM", "HALLMARK_CHOLESTEROL_HOMEOSTASIS",
         "HALLMARK_INTERFERON_GAMMA_RESPONSE", "HALLMARK_IL6_JAK_STAT3_SIGNALING"]
idrep = native.feature_id_report(str(jd / "DEG_results_ex_EXT_vs_SED_exo-ctrl.csv"))
for lab, name in targets.items():
    deg = str(jd / f"DEG_results_{name}.csv")
    od = cdir / "results" / "gsea" / lab
    base = {"method": "GSEA preranked (gseapy.prerank)", "gene_sets": "MSigDB mouse Hallmark mh.all v2024.1.Mm",
            "organism": "Mouse", "feature_id_type": idrep["dominant_type"], "ranking_metric": "stat (DESeq2 Wald)",
            "subset": lab,
            "paper_route": {"method": "GSEA Java v4.3.2, human h.all v2023.2 via mouse->human ortholog chip, 1000 phenotype/gene-set permutations",
                            "status": "blocked", "reason": "no Java GSEA executor; repository runs gseapy prerank on native mouse Hallmark"}}
    try:
        native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Mouse",
                         ranking_metric="stat", output_dir=str(od))
        files = sorted(glob.glob(str(od / "*GSEA*.csv")))
        items = [case.add_output(f, "gsea_table") for f in files]
        t = pd.read_csv(files[0])
        tcol = next(c for c in ("Term", "term", "Name") if c in t.columns)
        t = t.set_index(tcol)
        fdr = next(c for c in t.columns if "FDR" in c)
        keep = t.reindex([f for f in focus if f in t.index] )[["NES", fdr]]
        top = t.sort_values(fdr).head(10)[["NES", fdr]]
        print(lab, "\n", keep.round(3), "\n top:\n", top.round(3))
        case.decide("enrichment",
                    final={**base, "outputs": [i["path"] for i in items],
                           "focus_sets": keep.round(4).to_dict("index"),
                           "top10_by_fdr": top.round(4).to_dict("index")},
                    evidence=[case.add_output(deg, "deg_table")] + items, paper={"locator": "S2.15.p2"},
                    reasoning="Paper ran Hallmark GSEA (S2.15.p2, S3.4.p1); full ranking, no gene-list threshold.",
                    confidence="medium", execution_status="completed")
    except native.NativeToolError as e:
        case.decide("enrichment", final={**base, "execution_error": str(e)},
                    evidence=[case.add_output(deg, "deg_table")], paper={"locator": "S2.15.p2"},
                    reasoning="GSEA failed to run.", confidence="medium", execution_status="failed")
        print(lab, "FAILED", e)
