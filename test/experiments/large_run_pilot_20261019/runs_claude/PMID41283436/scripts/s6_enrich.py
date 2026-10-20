import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
run = native.RunRecorder.open("test/experiments/large_run_pilot_20261019/runs_claude/PMID41283436")
for cid in ["fatigued_pbmt_vs_ctrl", "sedentary_pbmt_vs_ctrl"]:
    case = run.case(cid)
    deg = sorted((case.dir / "results").glob("DEG_results_*_vs_*.csv"))[0]; print(cid, "DEG table", deg.name)
    audit = native.apply_threshold(deg, metric="pvalue", cutoff=0.05, effect_cutoff=None)
    case.write_json("audit_threshold_counts.json", audit | {"label": "audit: raw p<0.05 (diagnostic only, not the paper rule)"})
    print(cid, "AUDIT raw p<0.05", {k: audit[k] for k in ("n_significant", "n_up", "n_down")})
    fid = native.feature_id_report(deg); print(cid, {k: fid.get(k) for k in list(fid)[:6]})
    idtype = fid["dominant_type"]; print(cid, "dominant", idtype, fid["dominant_fraction"], fid["gene_set_ready"])
    d = case.evidence_item(next(k for k in case._source_ids if "DEG_results" in k)) if False else case.add_output(deg, "deg_table_enrich_input")
    for kind in ("gsea", "ora"):
        out = case.dir / "results" / kind
        try:
            if kind == "gsea":
                msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(deg), organism="Mouse", ranking_metric="stat", output_dir=str(out))
                fin = {"method": "GSEA preranked (gseapy)", "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm", "ranking": "DESeq2 Wald stat, all tested genes",
                       "note": "paper used clusterProfiler GO/KEGG ORA; Hallmark GSEA is an added workflow analysis"}
            else:
                msg = native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=str(deg), organism="Mouse", padj_cutoff=0.05, log2fc_cutoff=0.0, direction="up", output_dir=str(out))
                fin = {"method": "ORA (Enrichr via gseapy) on up-regulated genes", "gene_sets": "GO BP/MF/CC 2023 + KEGG 2019 Mouse",
                       "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None, "direction": "up"}, "input_threshold_source": "applied",
                       "note": "paper: clusterProfiler ORA of upregulated genes (FIG1C, FIG4C); Enrichr backend differs"}
            print(cid, kind, str(msg)[-500:])
            ok = True
        except native.NativeToolError as e:
            ok = False
            print(cid, kind, "FAILED", str(e)[:600]); err = str(e)[:2000]
        fin |= {"organism": "Mouse", "feature_id_type": idtype, "id_mapping": "Ensembl gene -> symbol via MyGene.info inside enrichment_tools"}
        if ok:
            files = [str(p) for p in out.rglob("*.csv")]
            fin["outputs"] = files
            case.decide("enrichment", final=fin, evidence=[d] + [case.add_output(f, f"{kind}_output") for f in files[:6]],
                        confidence="medium", execution_status="completed", reasoning=f"{kind} after completed DESeq2 execution.")
        else:
            fin["execution_error"] = err
            case.decide("enrichment", final=fin, evidence=[d], confidence="medium", execution_status="failed", reasoning=f"{kind} failed; DE result unaffected.")
