"""Audit sensitivity (two-group fits), Hallmark GSEA, summary, study, finish."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40932577"
run = native.RunRecorder.open(REL)
case = run.case("GSE301564")
plan = json.loads((case.dir / "reproduction_plan.json").read_text(encoding="utf-8"))
res = json.loads((case.dir / "execution_results.json").read_text(encoding="utf-8"))
named = json.loads((case.dir / "paper_named_genes_check.json").read_text(encoding="utf-8"))
PT = plan["threshold"]
paper = case.evidence_item("paper:PMC12972430.paper.json")
am = case.evidence_item("tool_output:aligned_matrix.csv")
named_item = case.add_output(case.dir / "paper_named_genes_check.json", "paper_named_genes_check")

# ---------------- audit: separate two-group DESeq2 fits (alternative reading of "each pairwise comparison")
grp = native.derive_columns(plan["metadata_csv"], case.dir / "aligned" / "design_metadata_grp.csv",
                            patterns={"grp": ("title", r"^(\w+ \w+) D\d+$")},
                            recode={"grp": {"robust control": "low_sed", "robust 24h": "low_run",
                                            "frail control": "high_sed", "frail 24h": "high_run"}})
gitem = case.add_output(grp["output"], "design_metadata_grp")
audit = {}
for name, ctrl, trt in [("run_run_vs_sed_frail-high", "high_sed", "high_run"), ("run_run_vs_sed_frail-low", "low_sed", "low_run")]:
    out = case.dir / "results" / "audit_two_group" / name
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=plan["counts_csv"], metadata_csv=grp["output"],
                         design_column="grp", control_group=ctrl, treatment_group=trt, output_dir=str(out))
        deg = native.deg_outputs(out)[0]
        th = native.apply_threshold(deg, metric="padj", cutoff=PT["cutoff"])
        audit[name] = {"deg_csv": deg, "threshold": th}
        item = case.add_output(deg, f"audit_two_group_{name}")
        case.decide("execution",
                    final={"method": "DESeq2 (pydeseq2 Wald), two-group fit", "subset": f"audit: {name} two-group",
                           "role": "audit (sensitivity to dispersion pooling; not the paper-aligned result)",
                           "formula": "~ grp (2 arms only)", "outputs": [deg], "n_tested": th["n_tested"],
                           "n_deg": th["n_significant"], "n_up": th["n_up"], "n_down": th["n_down"], "rule": th["rule"],
                           "deg_sanity": th["deg_sanity"],
                           "note": "executor uses pydeseq2 default independent-filtering alpha 0.05 (no alpha argument)"},
                    evidence=[am, gitem, item], paper={"locator": "S2.10.p2"}, confidence="medium", execution_status="completed",
                    reasoning="S2.10.p2 'for each pairwise comparison' may mean separate fits; run as a labelled sensitivity check only.")
    except native.NativeToolError as error:
        audit[name] = {"error": str(error)}
        case.decide("execution", final={"method": "DESeq2 two-group fit", "subset": f"audit: {name} two-group",
                    "execution_error": str(error)}, evidence=[am, gitem], paper={"locator": "S2.10.p2"},
                    confidence="medium", execution_status="failed", reasoning="audit fit failed")

# ---------------- enrichment: Hallmark GSEA on the planned contrasts
gsea = {}
for name in ["run_run_vs_sed_frail-low", "run_run_vs_sed_frail-high", "frail_run_high_run_vs_low_sed"]:
    deg = res[name]["deg_csv"]
    idr = native.feature_id_report(deg)
    out = case.dir / "enrichment" / name
    item = case.evidence_item(f"tool_output:{pathlib.Path(deg).name}")
    base = {"method": "GSEA preranked (gseapy prerank)", "subset": name, "gene_sets": "MSigDB Hallmark mh.all 2024.1.Mm",
            "organism": "Mouse", "feature_id_type": idr["dominant_type"], "ranking_metric": "stat (DESeq2 Wald)",
            "id_mapping": "Ensembl gene -> symbol via MyGene.info inside run_gsea_analysis",
            "paper_route": "GSEA 2.2.1 preranked on Wald stat, Entrez H + M2 CP + M5, FDR q < 0.05 (S2.10.p2)"}
    try:
        native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg, organism="Mouse",
                         ranking_metric="stat", output_dir=str(out))
        files = native.find_outputs(out, "*GSEA*.csv")
        tab = pd.read_csv(files[0])
        fdr_col = next(c for c in tab.columns if "fdr" in c.lower())
        term_col = "Term" if "Term" in tab.columns else tab.columns[0]
        tab["_fdr"] = pd.to_numeric(tab[fdr_col], errors="coerce")
        sig = tab[tab["_fdr"] < 0.05].sort_values("NES")
        ox = tab[tab[term_col].astype(str).str.contains("OXIDATIVE_PHOSPHORYLATION")]
        gsea[name] = {"files": files, "fdr_lt_0.05": [f"{r[term_col]} NES={float(r['NES']):.2f}" for _, r in sig.iterrows()],
                      "OXPHOS": [{"NES": float(r["NES"]), "FDR": float(r["_fdr"])} for _, r in ox.iterrows()]}
        outs = [case.add_output(f, f"gsea_{name}") for f in files]
        case.decide("enrichment", final={**base, "outputs": files, "n_sets_fdr_lt_0.05": len(sig), "oxphos": gsea[name]["OXPHOS"]},
                    evidence=[item, paper] + outs, paper={"locator": "S2.10.p2; S3.5.p2"}, confidence="medium",
                    execution_status="completed",
                    reasoning="Paper ranks each contrast by Wald stat for preranked GSEA; Hallmark only (M2 CP/M5 not available in the repository tool).")
    except native.NativeToolError as error:
        gsea[name] = {"error": str(error)}
        case.decide("enrichment", final={**base, "execution_error": str(error)}, evidence=[item, paper],
                    paper={"locator": "S2.10.p2"}, confidence="medium", execution_status="failed", reasoning="GSEA failed")
(case.dir / "enrichment_summary.json").write_text(json.dumps(gsea, indent=2, default=str), encoding="utf-8")

# ---------------- summary
comparison = {n: {"role": v["role"], "label": v["label"],
                  "ours": {k: v["threshold"][k] for k in ("n_significant", "n_up", "n_down", "n_tested")},
                  "paper": "not_reported in main text"} for n, v in res.items()}
audit_counts = {n: (v.get("threshold") or {}).get("n_significant", v.get("error")) for n, v in audit.items()}
case.write_json("reproduction_summary.json", {
    "route": "paper_aligned", "threshold": PT, "threshold_source": "paper", "deg_comparison": comparison,
    "audit_two_group_counts": audit_counts, "paper_named_genes": named,
    "named_gene_agreement": "HR vs HC: all 8 named genes in the paper's direction (6 up, Fosb/Junb down) and not changed in LR vs LC; only Ctss and Mpeg1 reach padj < 0.1 in the joint model (Isg20 0.052)",
    "gsea": {k: {"OXPHOS": v.get("OXPHOS"), "n_fdr_lt_0.05": len(v.get("fdr_lt_0.05", []))} if "error" not in v else v for k, v in gsea.items()},
    "paper_gsea_claims": "OXPHOS / complex assembly up in LR vs LC, down in HR vs HC; 284 sets with Frailty x Run interaction at FDR < 0.05 (S3.5.p1-p2)"},
    role="reproduction_summary")
h = res["run_run_vs_sed_frail-high"]["threshold"]
case.decide("study", final={"route": "paper_aligned", "primary_contrasts": ["run_run_vs_sed_frail-low", "run_run_vs_sed_frail-high", "frail_run_high_run_vs_low_sed"],
            "exploratory_contrasts": ["frail_high_vs_low_run-sed", "frail_high_vs_low_run-run"],
            "exploratory_reason": "not planned in the paper (frailty-within-condition comparisons)",
            "deg_comparison": comparison, "audit_two_group_counts": audit_counts,
            "deviations": ["pydeseq2 instead of R DESeq2", "Hallmark-only GSEA via gseapy instead of GSEA 2.2.1 with H + M2 CP + M5"]},
            evidence=[paper, case.evidence_item("tool_output:reproduction_summary.json"), named_item],
            paper={"locator": "S2.10.p1; S3.5.p3"}, confidence="medium",
            reasoning="Planned contrasts executed on the paper's DESeq2 route with the paper's FDR < 0.1 rule; the paper gives no DEG totals in its text, so only named genes and pathway directions can be compared.")
case.finish(n_deg=h["n_significant"], deg_sanity=h["deg_sanity"])
print(run.finish())
print(json.dumps(audit_counts, indent=1))
print(json.dumps({k: (v.get("OXPHOS"), v.get("fdr_lt_0.05", v.get("error"))) for k, v in gsea.items()}, indent=1, default=str))
