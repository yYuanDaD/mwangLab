"""Resume after 02_execution.py stopped at the TME enrichment record (feature_id_type "gene symbol" rejected; contract wants "gene_symbol"). Gates 9-11 (execution, enrichment, study) + run.finish for PMID42155766. Continues the run with RunRecorder.open."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native
from common import RUN, PAPER_THRESHOLD, CASES, COMPARISON

native.enable_native_mode()
run = native.RunRecorder.open(RUN)
TH = dict(metric="padj", cutoff=PAPER_THRESHOLD["cutoff"], effect_cutoff=None)
report = {}

for case_id, cfg in CASES.items():
    case = run.case(case_id)
    am = case.dir / "aligned" / "aligned_matrix.csv"
    dm = case.dir / "aligned" / "design_metadata.csv"
    res_dir = case.dir / "results" / "deseq2_grp"
    res_dir.mkdir(parents=True, exist_ok=True)
    plan_ev = case.write_json("reproduction_plan.json",
                              {"route": "paper_aligned", "method": "DESeq2 ~ grp (exercise vs sedentary) within fraction",
                               "contrast": COMPARISON, "threshold": PAPER_THRESHOLD,
                               "audits": ["padj<0.05"], "paper_reported": cfg["reported"]}, role="reproduction_plan")
    exec_err, deg, summary = None, None, {}
    done = {r["stage"] for r in case.records}  # 02_execution.py already recorded TME execution
    try:
        if "execution" not in done:
            msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(am), metadata_csv=str(dm),
                                   design_column="grp", control_group="sed", treatment_group="ex", output_dir=str(res_dir))
        deg = native.deg_outputs(res_dir)[0]
    except native.NativeToolError as e:
        exec_err = str(e)
    if exec_err is None:
        deg_ev = case.add_output(deg, f"deg_{COMPARISON}")
        paper_rule = native.apply_threshold(deg, **TH)
        audit = native.apply_threshold(deg, metric="padj", cutoff=0.05)
        t = pd.read_csv(deg, index_col=0)
        summary = {"contrast": COMPARISON, "paper_rule": paper_rule, "audit_padj_0.05": audit,
                   "n_genes_tested": int(t["padj"].notna().sum()), "n_genes_in_table": int(len(t)),
                   "paper_reported": cfg["reported"]}
        # marker genes the paper names (Fig 4C cancer-cell targets; IFN genes in TME)
        genes = ["Mki67", "Top2a", "Cenpf", "Tpx2", "Hmmr", "Anln", "Etfb", "Thrsp", "Fasn", "Tgm2",
                 "Aif1", "Stat1", "Irf7", "Isg15", "Hmgb2", "Ctf1"]
        summary["named_genes"] = {g: {k: (None if pd.isna(v) else float(v)) for k, v in t.loc[g, ["log2FoldChange", "padj"]].items()}
                                  for g in genes if g in t.index}
        if "execution" not in done:
          case.decide("execution",
                    final={"method": "DESeq2 (pydeseq2) ~ grp", "formula": "~ grp", "outputs": [deg],
                           "counts": {COMPARISON: paper_rule}, "audit_padj_0.05": audit},
                    evidence=[deg_ev], execution_status="completed", paper={"locator": "S2.4.p1"}, confidence="high",
                    reasoning=f"DESeq2 exercise vs sedentary on {cfg['celltype']}; paper threshold applied with apply_threshold.")
    else:
        case.decide("execution", final={"method": "DESeq2 (pydeseq2) ~ grp", "execution_error": exec_err},
                    evidence=[plan_ev], execution_status="failed", paper={"locator": "S2.4.p1"}, confidence="high",
                    reasoning="Executor failed.")
    case.write_json("reproduction_summary.json", summary, role="reproduction_summary")

    # ------------------------------------------------------------ enrichment
    if cfg["frac"] == "tme":
        efinal = {"method": "GSEA preranked (gseapy) on log2FoldChange", "gene_sets": "MSigDB Hallmark mouse (mh.all)",
                  "organism": "Mouse", "feature_id_type": "gene_symbol", "ranking_metric": "log2FoldChange",
                  "paper_route": "genekitr GSEA Hallmark on log2FC ranking, BH p_adj < 0.05 (S2.4.p1, FIG2B)"}
        if exec_err is None:
            gdir = case.dir / "results" / "gsea_hallmark"
            try:
                gmsg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Mouse",
                                        ranking_metric="log2FoldChange", output_dir=str(gdir))
                outs = [str(p) for p in native.find_outputs(gdir, "*GSEA*.csv")]
                g_ev = [case.add_output(p, "gsea_hallmark") for p in outs]
                top = []
                if outs:
                    g = pd.read_csv(outs[0])
                    qcol = next((c for c in g.columns if c.lower() in ("fdr q-val", "fdr", "padj", "fdr_q_val")), None)
                    if qcol:
                        g = g.sort_values(qcol)
                        top = g.head(12)[[c for c in g.columns if c in ("Term", "NES", qcol)]].to_dict("records")
                summary["gsea_top"] = top
                case.decide("enrichment", final={**efinal, "outputs": outs, "top_terms": top},
                            evidence=g_ev or [deg_ev], execution_status="completed", paper={"locator": "S2.4.p1"},
                            confidence="medium", reasoning="Hallmark GSEA on the full log2FC ranking, as the paper did for TME (Fig 2B).")
            except native.NativeToolError as e:
                case.decide("enrichment", final={**efinal, "execution_error": str(e)}, evidence=[deg_ev],
                            execution_status="failed", paper={"locator": "S2.4.p1"}, confidence="medium",
                            reasoning="GSEA executor failed (network or MSigDB).")
        else:
            case.decide("enrichment", final={**efinal, "reason_not_run": "no completed DE table"}, evidence=[plan_ev],
                        execution_status="not_run", paper={"locator": "S2.4.p1"}, confidence="medium", reasoning="No DE table.")
    else:
        case.decide("enrichment",
                    final={"method": "Reactome ORA on up- and down-regulated DEGs (paper)", "gene_sets": "Reactome",
                           "organism": "Mouse", "feature_id_type": "gene_symbol",
                           "input_threshold": PAPER_THRESHOLD, "input_threshold_source": "applied",
                           "reason_not_run": ("repository ORA executor (run_enrichment_analysis) offers GO BP/MF/CC + KEGG only, "
                                              "no Reactome library; IPA is proprietary")},
                    evidence=[deg_ev] if exec_err is None else [plan_ev], execution_status="not_run",
                    paper={"locator": "S3.p4"}, confidence="medium", reasoning="Paper enrichment route has no executor here.")
    case.write_json("reproduction_summary.json", summary, role="reproduction_summary")

    case.decide("study", final={"route": "paper_aligned",
                                "note": "DESeq2 exercise vs sedentary per sorted fraction, paper threshold p_adj < 0.1"},
                evidence=[deg_ev] if exec_err is None else [plan_ev], paper={"locator": "S2.4.p1"}, confidence="high",
                reasoning="Paper route reproduced." if exec_err is None else "Execution failed.")
    if exec_err is None:
        case.finish(n_deg=summary["paper_rule"]["n_significant"], deg_sanity=summary["paper_rule"]["deg_sanity"])
    else:
        case.finish()
    report[case_id] = {"exec_err": exec_err, **{k: summary.get(k) for k in ("paper_rule", "audit_padj_0.05", "n_genes_tested", "named_genes", "gsea_top")}}
print(json.dumps(report, indent=1, default=str))
print(run.finish())
