import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))  # repository root
import pandas as pd
from tools import native
native.enable_native_mode()
REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41314005"
run = native.RunRecorder.open(REL)
case = run.case("GSE308674")
plan = json.loads((case.dir / "reproduction_plan.json").read_text(encoding="utf-8"))
res = json.loads((case.dir / "execution_results.json").read_text(encoding="utf-8"))
PT = plan["threshold"]
paper = case.evidence_item("paper:PMC12702345.paper.json")
summary = {"gsea": {}, "ora": {}}
for name in ["H_vs_C", "HM_vs_C", "L_vs_C", "M_vs_C"]:
    deg = res[name]["deg_csv"]
    idr = native.feature_id_report(deg)
    out = case.dir / "enrichment" / name
    item = case.evidence_item(f"tool_output:{pathlib.Path(deg).name}")
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Mouse",
                               ranking_metric="stat", output_dir=str(out))
        files = native.find_outputs(out, "*GSEA*.csv")
        tab = pd.read_csv(files[0]) if files else None
        top = []
        if tab is not None:
            fdr_col = next((c for c in tab.columns if c.lower() in ("fdr q-val", "fdr", "fdr_q-val")), None)
            term_col = "Term" if "Term" in tab.columns else tab.columns[0]
            sig = tab[pd.to_numeric(tab[fdr_col], errors="coerce") <= 0.25] if fdr_col else tab
            top = [f"{r[term_col]} NES={float(r['NES']):.2f}" for _, r in sig.sort_values("NES").iterrows()]
        summary["gsea"][name] = {"files": files, "fdr_le_0.25": top}
        outs = [case.add_output(f, f"gsea_{name}") for f in files]
        case.decide("enrichment", final={"method": "GSEA preranked (gseapy prerank)", "subset": name,
                    "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm", "organism": "Mouse",
                    "feature_id_type": idr["dominant_type"], "ranking_metric": "stat (DESeq2 Wald)",
                    "outputs": files, "paper_route": "fgsea, 10,000 permutations, padj <= 0.25 (S2.7.1.p1)",
                    "n_sets_fdr_le_0.25": len(top)},
                    evidence=[item, paper] + outs, paper={"locator": "S2.7.1.p1; S3.3.p3"}, confidence="medium",
                    execution_status="completed", reasoning=f"Paper reports Hallmark GSEA; ranked the full {name} table by Wald stat. Engine differs from fgsea (declared).")
    except native.NativeToolError as error:
        summary["gsea"][name] = {"error": str(error)}
        case.decide("enrichment", final={"method": "GSEA preranked (gseapy prerank)", "subset": name,
                    "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm", "organism": "Mouse",
                    "feature_id_type": idr["dominant_type"], "execution_error": str(error)},
                    evidence=[item, paper], paper={"locator": "S2.7.1.p1"}, confidence="medium",
                    execution_status="failed", reasoning="GSEA failed")

# ORA on the primary exercise contrast, with the applied threshold
name = "H_vs_C"; deg = res[name]["deg_csv"]; out = case.dir / "enrichment" / f"{name}_ORA"
item = case.evidence_item(f"tool_output:{pathlib.Path(deg).name}")
for direction in ("up", "down"):
    try:
        msg = native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=deg, organism="Mouse",
                               padj_cutoff=PT["cutoff"], log2fc_cutoff=PT["effect_cutoff"], direction=direction,
                               output_dir=str(out / direction))
        files = native.find_outputs(out / direction, "*.csv")
        summary["ora"][f"{name}_{direction}"] = {"files": files, "message": str(msg)[-1500:]}
        outs = [case.add_output(f, f"ora_{name}_{direction}_{i}") for i, f in enumerate(files)]
        case.decide("enrichment", final={"method": "ORA (Enrichr)", "subset": f"{name} {direction}",
                    "gene_sets": "GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG_2019_Mouse (Enrichr)",
                    "organism": "Mouse", "feature_id_type": "gene_symbol", "input_threshold": PT,
                    "input_threshold_source": "applied", "outputs": files,
                    "paper_route": "clusterProfiler GO BP + KEGG (S2.7.1.p1)"},
                    evidence=[item, paper] + outs, paper={"locator": "S2.7.1.p1; S3.3.p2"}, confidence="medium",
                    execution_status="completed", reasoning="Paper reports GO/KEGG enrichment of up- and down-regulated DEGs; gene lists use the applied paper threshold.")
    except native.NativeToolError as error:
        summary["ora"][f"{name}_{direction}"] = {"error": str(error)}
        case.decide("enrichment", final={"method": "ORA (Enrichr)", "subset": f"{name} {direction}",
                    "gene_sets": "GO 2023 + KEGG_2019_Mouse (Enrichr)", "organism": "Mouse", "feature_id_type": "gene_symbol",
                    "input_threshold": PT, "input_threshold_source": "applied", "execution_error": str(error)},
                    evidence=[item, paper], paper={"locator": "S2.7.1.p1"}, confidence="medium",
                    execution_status="failed", reasoning="ORA failed")
(case.dir / "enrichment_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")

comparison = {n: {"ours": {k: res[n]["threshold"][k] for k in ("n_significant", "n_up", "n_down", "n_tested")},
                  "paper": next(c["paper_n_deg"] for c in plan["contrasts"] if c["name"] == n),
                  "formula": res[n]["formula"]} for n in res}
case.write_json("reproduction_summary.json", {"route": "declared_deviation", "threshold": PT,
                "threshold_source": "paper_on_deviation_route", "deg_comparison": comparison,
                "gsea_fdr_le_0.25": {k: v.get("fdr_le_0.25", v.get("error")) for k, v in summary["gsea"].items()},
                "paper_gsea_claims": {"H_vs_C": "inflammatory, hypoxia, mTORC1, complement, oxidative phosphorylation enriched (S3.3.p3)",
                                      "L_vs_C": "angiogenesis, secretory, EMT, hormone-responsive enriched; MYC, p53, DNA repair negative (S3.3.p3)"}},
                role="reproduction_summary")
h = res["H_vs_C"]["threshold"]
case.decide("study", final={"route": "declared_deviation", "primary_contrast": "H_vs_C",
            "deviations": ["two-group DESeq2 fits instead of one 5-group model", "no edgeR filterByExpr pre-filter",
                           "gseapy prerank instead of fgsea", "6 split rows of the deposited CSV repaired"],
            "deg_comparison": comparison},
            evidence=[paper, case.evidence_item("tool_output:reproduction_summary.json")], paper={"locator": "S3.3.p1"},
            confidence="medium", reasoning="All four planned contrasts executed with the paper threshold on a declared-deviation DESeq2 route.")
case.finish(n_deg=h["n_significant"], deg_sanity=h["deg_sanity"])
print(run.finish())
print(json.dumps({k: v.get("fdr_le_0.25", v.get("error")) for k, v in summary["gsea"].items()}, indent=1))
print(json.dumps({k: (v.get("error") or v["message"][-600:]) for k, v in summary["ora"].items()}, indent=1))
