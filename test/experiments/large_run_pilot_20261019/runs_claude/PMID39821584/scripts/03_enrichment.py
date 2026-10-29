"""Gate 10: enrichment for the four planned contrasts (GSEA Hallmark + Enrichr ORA up/down)."""
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
planned = ["grp_r25_vs_sed", "grp_r50_vs_sed", "grp_r75_vs_sed", "grp_rU_vs_sed"]

raw = pd.read_csv("data/GSE275818/GSE275818_Casperson_gene_count.txt.gz", sep="\t", usecols=["gene_id", "gene_name"])
MAP = cdir / "aligned" / "entrez_to_symbol.csv"
raw.set_index("gene_id").to_csv(MAP)
map_ev = case.add_output(MAP, "id_mapping")

summary = {}
for name in planned:
    deg = cdir / "results" / "joint_deseq2" / f"DEG_results_{name}.csv"
    idrep = native.feature_id_report(deg)
    col = native.collapse_to_genes(deg, cdir / "results" / "enrichment" / name / f"DEG_results_{name}_symbols.csv",
                                   mapping_csv=MAP, mapping_column="gene_name", rule="max_mean")
    sym = col["output"]
    entry = {"feature_id_report": {k: idrep.get(k) for k in ("id_type", "gene_set_ready", "note") if k in idrep},
             "collapse": {k: col[k] for k in ("n_features", "n_unmapped", "n_genes", "n_features_collapsed")}}
    # GSEA
    gout = cdir / "results" / "enrichment" / name / "gsea"
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=sym, organism="Mouse",
                               ranking_metric="stat", output_dir=str(gout))
        files = native.find_outputs(gout, "*GSEA*.csv")
        g = pd.read_csv(files[0]) if files else None
        top = None
        if g is not None:
            fdr_col = next((c for c in g.columns if "FDR" in c), None)
            g = g.sort_values(fdr_col) if fdr_col else g
            top = g.head(8)[[c for c in g.columns if c in ("Term", "NES", fdr_col)]].to_dict(orient="records")
        rec = {"status": "completed", "outputs": files, "top": top}
        case.decide("enrichment",
                    final={"method": "GSEA preranked (gseapy.prerank)", "subset": name,
                           "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm", "organism": "Mouse",
                           "feature_id_type": "Entrez gene ID -> gene symbol", "ranking_metric": "stat",
                           "id_mapping": col["mapping_record"], "outputs": files, "top_terms": top},
                    evidence=[case.add_output(sym, f"symbols_{name}"), map_ev],
                    reasoning="Paper reports pathway findings (KEGG); Hallmark GSEA on the full ranking as a declared-library deviation.",
                    confidence="medium", execution_status="completed")
    except native.NativeToolError as error:
        rec = {"status": "failed", "error": str(error)[:400]}
        case.decide("enrichment",
                    final={"method": "GSEA preranked (gseapy.prerank)", "subset": name,
                           "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm", "organism": "Mouse",
                           "feature_id_type": "Entrez gene ID -> gene symbol", "id_mapping": col["mapping_record"],
                           "execution_error": str(error)},
                    evidence=[map_ev], reasoning="GSEA failed", confidence="medium", execution_status="failed")
    entry["gsea"] = rec
    # ORA up / down. Tool filters on padj only (cannot express raw p <= 0.05) -> audit list FDR < 0.05, no LFC cutoff.
    for direction in ("up", "down"):
        oout = cdir / "results" / "enrichment" / name / f"ora_{direction}"
        base = {"method": f"ORA Enrichr ({direction}-regulated)", "subset": f"{name}:{direction}",
                "gene_sets": "Enrichr GO_Biological_Process_2023/MF/CC + KEGG_2019_Mouse", "organism": "Mouse",
                "feature_id_type": "Entrez gene ID -> gene symbol", "id_mapping": col["mapping_record"],
                "input_threshold": {"metric": "padj", "cutoff": 0.05, "inclusive": False, "effect_cutoff": 0},
                "input_threshold_source": "audit",
                "deviation_note": ("paper list = raw p <= 0.05 & mean raw count >= 25 (S2.3.p1); run_enrichment_analysis "
                                   "filters on padj only (tools/enrichment_tools.py:218), so an FDR<0.05 list is used")}
        try:
            native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=sym, organism="Mouse",
                             padj_cutoff=0.05, log2fc_cutoff=0.0, direction=direction, output_dir=str(oout))
            files = native.find_outputs(oout, "*.csv")
            kegg = [f for f in files if "KEGG" in f]
            top = None
            if kegg:
                k = pd.read_csv(kegg[0])
                pcol = next((c for c in k.columns if c.lower().startswith("adjusted")), None)
                k = k.sort_values(pcol) if pcol else k
                top = k.head(8)[[c for c in k.columns if c in ("Term", pcol, "Overlap")]].to_dict(orient="records")
            case.decide("enrichment", final={**base, "outputs": files, "top_kegg": top},
                        evidence=[map_ev], reasoning="ORA on audit FDR list (tool cannot filter on raw p).",
                        confidence="medium", execution_status="completed")
            entry[f"ora_{direction}"] = {"status": "completed", "top_kegg": top}
        except native.NativeToolError as error:
            case.decide("enrichment", final={**base, "execution_error": str(error)},
                        evidence=[map_ev], reasoning="ORA failed", confidence="medium", execution_status="failed")
            entry[f"ora_{direction}"] = {"status": "failed", "error": str(error)[:400]}
    summary[name] = entry
case.write_json("enrichment_summary.json", summary, role="enrichment_summary")
print(json.dumps(summary, indent=1, default=str)[:8000])
