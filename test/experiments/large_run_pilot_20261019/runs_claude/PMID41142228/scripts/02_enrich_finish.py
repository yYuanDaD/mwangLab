import sys, pathlib, json; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41142228"
ACC = "GSE308626"
run = native.RunRecorder.open(REL)
case = run.case(ACC)
st = json.load(open(case.dir / "_stage1.json"))
deg = json.load(open(case.dir / "results" / "_deg_path.json"))["deg"]
deg_item = case.add_output(deg, "deg_table")

# ---- paper findings check (genes named in S3.4.p3-p4, S4.p20), Ensembl -> symbol via MyGene
from tools.enrichment_tools import _query_symbols
d = pd.read_csv(deg, index_col=0)
ids = [i.split(".")[0] for i in d.index]
sym = _query_symbols(ids, "mouse")
d["symbol"] = [sym.get(i) for i in ids]
named = {"up": ["Myh7", "Foxp1", "Gata6", "Akap13", "Ccn2", "Bcl2l1", "Hspb6", "Akap1"],
         "down": ["Plin5", "Fabp3", "Gck", "Acsf2", "Col4a2", "Adamts9"]}
rows = []
for exp, genes in named.items():
    for g in genes:
        sub = d[d["symbol"] == g]
        if sub.empty:
            rows.append({"gene": g, "paper_direction": exp, "found": False}); continue
        r = sub.iloc[0]
        rows.append({"gene": g, "paper_direction": exp, "found": True, "log2FC": round(float(r.log2FoldChange), 3),
                     "padj": None if pd.isna(r.padj) else float(r.padj),
                     "sig_fdr0.1": bool(r.padj < 0.1) if not pd.isna(r.padj) else False,
                     "direction_agrees": (r.log2FoldChange > 0) == (exp == "up")})
chk = case.write_json("results/paper_gene_check.json", rows, role="paper_gene_check")
for r in rows: print(r)

# ---- enrichment: GSEA Hallmark (declared deviation from fgsea GO BP)
fid = native.feature_id_report(deg)
gdir = case.dir / "results" / "gsea"
try:
    msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Mouse",
                           ranking_metric="stat", output_dir=str(gdir))
    print(msg[-2500:])
    outs = native.find_outputs(gdir, "*GSEA*.csv")
    items = [case.add_output(p, "gsea_table") for p in outs]
    case.decide("enrichment", final={"method": "GSEA preranked (gseapy.prerank)", "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm",
                "organism": "Mouse", "feature_id_type": "ensembl_gene", "ranking_metric": "stat",
                "id_mapping": "Ensembl gene -> symbol via MyGene.info inside run_gsea_analysis",
                "paper_route": {"method": "fgsea 1.22.0, msigdbr 7.5.1 GO BP, size 15-500, ranked by DESeq2 stat", "status": "blocked",
                                "reason": "repository GSEA executor supports MSigDB Hallmark only; Hallmark used as declared deviation"},
                "outputs": [str(p) for p in outs], "feature_id_report": {k: fid[k] for k in ("dominant_type", "dominant_fraction", "gene_set_ready")}},
                evidence=[deg_item] + items, paper={"locator": "S2.8.p3"}, confidence="medium", execution_status="completed",
                reasoning="Paper ranks genes by the DESeq2 statistic for fgsea; same ranking used with Hallmark sets. Kept separate from the DE result.")
    enr = "completed"
except native.NativeToolError as e:
    case.decide("enrichment", final={"method": "GSEA preranked (gseapy.prerank)", "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm",
                "organism": "Mouse", "feature_id_type": "ensembl_gene", "id_mapping": "Ensembl -> symbol via MyGene.info",
                "execution_error": str(e)}, evidence=[deg_item], confidence="medium", execution_status="failed",
                reasoning="GSEA executor failed; DE result unaffected.")
    enr = f"failed: {e}"

thr = st["thr"]
case.write_json("reproduction_summary.json", {"contrast": "grp_ex_vs_sed", "method": "DESeq2 ~ grp", "threshold": "BH padj < 0.1 (paper)",
    "n_deg": thr["n_significant"], "n_up": thr.get("n_up"), "n_down": thr.get("n_down"), "paper_n_deg": "not_reported",
    "paper_gene_check": rows, "enrichment": enr}, role="reproduction_summary")
case.decide("study", final={"route": "paper_aligned", "contrast": "grp_ex_vs_sed",
            "notes": "DESeq2 on STAR integer counts with the paper's FDR < 0.1; count source (STAR vs RSEM) not stated in the paper. Forced-vs-voluntary comparison (external PRJNA811435) out of scope. GSEA Hallmark is a declared deviation from fgsea GO BP."},
            evidence=[deg_item, chk], paper={"locator": "S2.8.p3"}, confidence="high",
            execution_status="completed" if st["ok"] else "failed",
            reasoning="Planned route reproduces the paper's DE method, contrast and threshold.")
case.finish(n_deg=thr["n_significant"], deg_sanity=thr.get("deg_sanity"))
run.finish()
