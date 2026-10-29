"""GSE151066 enrichment (paper: DAVID ORA on up-regulated genes) + study records for both cases + run.finish()."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40693573"
run = native.RunRecorder.open(RUN)

# ================================================================ GSE151066
case = run.case("GSE151066")
paper = case.evidence_item("paper:PMC12248044.paper.json")
res = case.dir / "results"
applied = [r for r in case.records if r["stage"] == "threshold"][-1]["final"]["applied_threshold"]
markers = {"ENSG00000109819": "PPARGC1A", "ENSG00000119508": "NR4A3", "ENSG00000204388": "HSPA1B",
           "ENSG00000204389": "HSPA1A", "ENSG00000123358": "NR4A1", "ENSG00000116299": "CPEB4"}
ex = json.loads((res / "execution_summary.json").read_text(encoding="utf-8"))
marker_check, enr = {}, {}
for name in ["AS_3pe_vs_pre", "AA_3pe_vs_pre"]:
    deg = ex[name]["paper"]["deg_csv"]
    d = pd.read_csv(deg, index_col=0)
    marker_check[name] = {sym: d.loc[e, ["log2FoldChange", "padj"]].round(4).to_dict() if e in d.index else None
                          for e, sym in markers.items()}
    out = res / "enrichment" / name
    idr = native.feature_id_report(deg)
    try:
        msg = native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=deg, organism="Human",
                               padj_cutoff=0.05, log2fc_cutoff=1.5, direction="up", output_dir=str(out))
        files = sorted(str(p) for p in out.glob("*.csv"))
        top = {}
        for f in files:
            t = pd.read_csv(f)
            top[pathlib.Path(f).stem.split("_vs_pre_")[-1]] = t.head(8)[["Term", "Adjusted P-value"]].round(6).values.tolist()
        enr[name] = {"files": files, "top": top, "n_sig_terms_padj05": {pathlib.Path(f).stem: int((pd.read_csv(f)["Adjusted P-value"] < 0.05).sum()) for f in files}}
        outs = [case.add_output(f, f"ora_{name}") for f in files]
        case.decide("enrichment",
                    final={"method": "ORA (Enrichr via gseapy) on up-regulated DEGs", "subset": name,
                           "gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG_2021_Human",
                           "organism": "Human", "feature_id_type": "ensembl_gene",
                           "id_mapping": "Ensembl -> symbol via MyGene.info inside run_enrichment_analysis",
                           "input_threshold": dict(applied, direction="up"), "input_threshold_source": "applied",
                           "outputs": files, "n_significant_terms": enr[name]["n_sig_terms_padj05"],
                           "paper_comparison": "paper: DAVID on up genes, hsAS 204 terms, hsAA 149 terms; common skeletal muscle cell "
                                               "differentiation (GO:0035914), negative regulation of apoptotic process (GO:0043066)",
                           "deviation": "Enrichr libraries instead of DAVID"},
                    evidence=[paper] + outs, paper={"locator": "S2.6.p3"}, confidence="medium",
                    execution_status="completed",
                    reasoning="Paper ran ORA on all significantly up-regulated genes (> 80 genes) for hsAS and hsAA.")
    except native.NativeToolError as e:
        enr[name] = {"error": str(e)[:500]}
        case.decide("enrichment",
                    final={"method": "ORA (Enrichr via gseapy) on up-regulated DEGs", "subset": name,
                           "gene_sets": "Enrichr GO 2023 + KEGG_2021_Human", "organism": "Human", "feature_id_type": "ensembl_gene",
                           "id_mapping": "Ensembl -> symbol via MyGene.info", "input_threshold": dict(applied, direction="up"),
                           "input_threshold_source": "applied", "execution_error": str(e)[:2000]},
                    evidence=[paper], paper={"locator": "S2.6.p3"}, confidence="medium", execution_status="failed",
                    reasoning="ORA failed (network or tool).")
case.write_json("marker_genes_check.json", marker_check, role="marker_genes_check")
print(json.dumps({"markers": marker_check, "enrichment": {k: v.get("top", v) for k, v in enr.items()}}, indent=1, default=str)[:6000])

n_as, n_aa = ex["AS_3pe_vs_pre"]["paper"]["n_significant"], ex["AA_3pe_vs_pre"]["paper"]["n_significant"]
summary1 = {"AS_3pe_vs_pre": {"ours": n_as, "up": ex["AS_3pe_vs_pre"]["paper"]["n_up"], "down": ex["AS_3pe_vs_pre"]["paper"]["n_down"],
                              "paper": 210, "paper_up_down": [201, 9]},
            "AA_3pe_vs_pre": {"ours": n_aa, "up": ex["AA_3pe_vs_pre"]["paper"]["n_up"], "down": ex["AA_3pe_vs_pre"]["paper"]["n_down"],
                              "paper": 116, "paper_up_down": [112, 4]},
            "markers": marker_check, "exploratory": {k: ex[k] for k in ("joint_sed", "joint_act", "paired_change")},
            "enrichment": {k: v.get("n_sig_terms_padj05", v) for k, v in enr.items()}}
case.write_json("reproduction_plan.json", {
    "paper_aligned_route": "per-cohort DESeq2 h3 vs pre on males, BH padj < 0.05 & |log2FC| > 1.5",
    "declared_deviations": ["depositor's RSEM expected counts rounded, no tximport length offsets",
                            "subject blocking added (paper silent on pairing)", "Enrichr libraries instead of DAVID"],
    "exploratory": ["ip vs pre, ip vs h3 per cohort (joint ~subject+time)", "cohort difference in h3-pre change (limma paired_change)"]},
    role="reproduction_plan")
case.write_json("reproduction_summary.json", summary1, role="reproduction_summary")
case.decide("study",
            final={"route": "declared_deviation", "n_deg_by_contrast": {"AS_3pe_vs_pre": n_as, "AA_3pe_vs_pre": n_aa},
                   "paper_counts": {"AS_3pe_vs_pre": 210, "AA_3pe_vs_pre": 116},
                   "n_deg_reported_in_summary": "sum of the two planned contrasts",
                   "exploratory_reason": None,
                   "comparison_note": "direction and marker genes reproduce; counts are higher than the paper's, plausibly from "
                                      "subject blocking and the different quantification/gene universe"},
            evidence=[paper, case.evidence_item("tool_output:reproduction_summary.json")], paper={"locator": "S3.1.p1"},
            confidence="high", execution_status="completed",
            reasoning="Paper route (DESeq2, paper threshold) run on the deposited counts with documented deviations.")
case.finish(n_deg=n_as + n_aa, deg_sanity="ok")

# ================================================================ GSE279359
case = run.case("GSE279359")
paper = case.evidence_item("paper:PMC12248044.paper.json")
ex2 = json.loads((case.dir / "results" / "execution_summary.json").read_text(encoding="utf-8"))
reported = {"ipe_vs_pre": 23, "1pe_vs_pre": 13, "24pe_vs_pre": 31}
gene_syms = set(pd.read_csv(case.dir / "aligned" / "gene_counts_known_symbols.csv", index_col=0).index)
summary2 = {k: {"ours": ex2[k]["paper"], "ours_log2fc1": ex2[k]["audit_log2fc1"], "paper": reported[k],
                "top": ex2[k]["top_sig"]} for k in reported}
summary2["validated_genes_in_deposit"] = {g: g in gene_syms for g in ["Ube2d1", "Fbxo32", "Fos", "Hspa8", "Sirt2", "Hnrnpa3", "Hnrnpa1", "Tia1"]}
summary2["joint"] = ex2["joint"]
case.write_json("reproduction_plan.json", {
    "paper_aligned_route": "Swan gene-level DE per time point vs pre (blocked: no executor)",
    "declared_deviation": "pairwise DESeq2 on gene-summed TALON counts of known genes, paper threshold",
    "exploratory": "joint 20-sample DESeq2 for all six time contrasts"}, role="reproduction_plan")
case.write_json("reproduction_summary.json", summary2, role="reproduction_summary")
print(json.dumps(summary2, indent=1, default=str))
total = sum(ex2[k]["paper"] for k in reported)
case.decide("study",
            final={"route": "declared_deviation", "n_deg_by_contrast": {k: ex2[k]["paper"] for k in reported},
                   "paper_counts": reported, "n_deg_reported_in_summary": "sum of the three planned contrasts",
                   "exploratory_reason": None,
                   "comparison_note": ("paper counts not reproduced (1/1/1 vs 23/13/31): the GEO deposit is an author-filtered "
                                       "TALON transcript set with 2974 known genes (paper detected 5459-6323) and lacks the "
                                       "paper's validated genes Fbxo32 and Fos; libraries are 77k-336k reads")},
            evidence=[paper, case.evidence_item("tool_output:reproduction_summary.json")], paper={"locator": "S3.1.p2"},
            confidence="high", execution_status="completed",
            reasoning="Swan route blocked; DESeq2 run as declared deviation with the paper's threshold.")
case.finish(n_deg=total, deg_sanity="ok")
print(json.dumps(run.finish(), indent=1))
