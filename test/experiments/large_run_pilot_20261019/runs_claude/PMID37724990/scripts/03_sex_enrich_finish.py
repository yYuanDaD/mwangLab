"""Exploratory female-only analysis, enrichment gate, reproduction artifacts, study record, finish."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json, math
ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder.open(str(RUN))
case = run.case("GSE183150")
paper = case.evidence_item("paper:PMC10618653.paper.json")
a_mat = case.evidence_item("tool_output:library_counts.csv")
a_meta = case.evidence_item("tool_output:design_metadata.csv")
A, R = case.dir / "aligned", case.dir / "results"
dm = pd.read_csv(A / "design_metadata.csv", index_col=0)
norm = native.find_outputs(R / "preprocess", "*_normalized.csv")[0]
PLANNED = "grp_visit_ex_eos_vs_uc_base"
main_deg = R / "paired_change" / "followup_eos" / f"DEG_results_{PLANNED}.csv"
counts = json.load(open(R / "deg_counts.json"))

# ---------------- exploratory: female participants only (suitability split_plan) ----------------
sex = pd.read_csv(case.dir / "suitability" / "library_counts_sex_check.tsv", sep="\t", index_col=0)
sex_by_subject = {i.split("_")[0]: s for i, s in sex["predicted_sex"].items()}
dm["sex_pred"] = dm["subject"].map(sex_by_subject)
fem = dm[dm.sex_pred == "female"]
fd = R / "female_only"; fd.mkdir(parents=True, exist_ok=True)
fem.to_csv(fd / "metadata.csv")
print("female participants per arm:", fem[fem.visit == "eos"].grp.value_counts().to_dict(),
      "male:", dm[(dm.sex_pred == "male") & (dm.visit == "eos")].grp.value_counts().to_dict())
plan = {"analysis_type": "paired_change", "subject_column": "subject", "time_column": "visit",
        "baseline_level": "base", "followup_levels": ["eos"], "group_column": "grp", "formula": "~ 0 + C(grp)",
        "contrasts": [{"name": PLANNED + "__sex-female", "coefficients": {"C(grp)[ex]": 1, "C(grp)[uc]": -1}}]}
already = any(r.get("stage") == "execution" and "female" in str(r.get("final", {}).get("subset", ""))
              for r in json.load(open(case.dir / "decisions.json", encoding="utf-8")))
if already:  # recorded by an earlier, interrupted invocation of this script
    t = native.apply_threshold(fd / "followup_eos" / f"DEG_results_{PLANNED}__sex-female.csv", metric="padj", cutoff=0.05, effect_cutoff=None)
    counts[PLANNED + "__sex-female"] = {k: t.get(k) for k in ("n_significant", "n_up", "n_down", "deg_sanity")}
else:
  try:
      res = native.call_tool("tools.multigroup_tools:run_multigroup_analysis", expression_csv=str(norm),
                             metadata_csv=str(fd / "metadata.csv"), plan=plan, output_dir=str(fd))
      r0 = res["results"][0]
      t = native.apply_threshold(r0["path"], metric="padj", cutoff=0.05, effect_cutoff=None)
      counts[r0["name"]] = {k: t.get(k) for k in ("n_significant", "n_up", "n_down", "deg_sanity")}
      o = case.add_output(r0["path"], f"deg_table:{r0['name']}")
      case.decide("execution", final={"method": "limma paired-change on log2(CPM+1)", "subset": "female participants (exploratory)",
                                      "outputs": [o["path"]], "n_complete_pairs": r0["n_complete_pairs"],
                                      "residual_df": r0["residual_df"], "counts": counts[r0["name"]],
                                      "note": "male participants: 2 exercise, 1 usual care (P21 low-confidence call); not analyzable"},
                  evidence=[a_mat, a_meta, case.evidence_item("tool_output:suitability.json")], execution_status="completed",
                  confidence="high", reasoning="Per-sex exploratory analysis requested by the suitability split plan; females only.")
      print(r0["name"], counts[r0["name"]])
  except native.NativeToolError as e:
      case.decide("execution", final={"method": "limma paired-change on log2(CPM+1)", "subset": "female participants (exploratory)",
                                      "execution_error": str(e)},
                  evidence=[a_mat, a_meta], execution_status="failed", confidence="high", reasoning="executor failed")

# ---------------- audit counts on the planned contrast (labelled audit, not the applied rule) ----------------
audit = {
    "raw_p_lt_0.05": native.apply_threshold(main_deg, metric="pvalue", cutoff=0.05, effect_cutoff=None),
    "raw_p_lt_0.01": native.apply_threshold(main_deg, metric="pvalue", cutoff=0.01, effect_cutoff=None),
    "raw_p_lt_0.05_abs_log2FC_gt_1": native.apply_threshold(main_deg, metric="pvalue", cutoff=0.05, effect_cutoff=1.0),
}
audit = {k: {kk: v.get(kk) for kk in ("n_significant", "n_up", "n_down")} for k, v in audit.items()}
d = pd.read_csv(main_deg, index_col=0)
d["rank"] = range(1, len(d) + 1)
idx = {i.split(".")[0]: i for i in d.index}
paper_genes = {"KCNV1": ("ENSG00000164794", "up"), "ABCG8": ("ENSG00000143921", "up"), "B4GALNT2": ("ENSG00000167080", "up"),
               "C5orf17/LINC02899": ("ENSG00000234292", "up"), "TMPRSS6": ("ENSG00000187045", "down"),
               "PRAC1": ("ENSG00000159182", "down"), "HOXB13": ("ENSG00000159184", "down")}
gene_cmp = {}
for g, (e, dirn) in paper_genes.items():
    if e in idx:
        r = d.loc[idx[e]]
        gene_cmp[g] = {"paper_direction": dirn, "log2FC": round(float(r.log2FoldChange), 3), "pvalue": float(r.pvalue),
                       "padj": float(r.padj), "rank_of_%d" % len(d): int(r["rank"]),
                       "direction_agrees": bool((r.log2FoldChange > 0) == (dirn == "up"))}
    else:
        gene_cmp[g] = {"paper_direction": dirn, "status": "removed by low-expression filter or absent"}
print(json.dumps(audit), json.dumps(gene_cmp, indent=1))

# ---------------- enrichment: GSEA Hallmark on the planned contrast ----------------
fid = native.feature_id_report(main_deg)
print("FID", {k: fid.get(k) for k in ("id_type", "gene_set_ready", "note")})
ed = R / "gsea"
enr_final = {"method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB Hallmark h.all 2024.1.Hs",
             "organism": "Human", "feature_id_type": fid.get("id_type", "ensembl_gene"),
             "ranking_metric": "stat (limma moderated t of the planned interaction contrast)",
             "paper_enrichment": "KEGG + GO BP GSEA ranked by fold change, BIOCARTA IL6 (FIG3 C, SUP15, SUP6); those libraries are not available here, so Hallmark is a declared substitute"}
try:
    native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(main_deg), organism="Human",
                     ranking_metric="stat", output_dir=str(ed))
    gsea = native.find_outputs(ed, "*GSEA_Hallmark.csv")
    outs = [case.add_output(p, "gsea_hallmark") for p in gsea]
    g = pd.read_csv(gsea[0])
    print(g.head(12).to_string())
    enr_final["outputs"] = [o["path"] for o in outs]
    case.decide("enrichment", final=enr_final, evidence=[case.evidence_item(f"tool_output:{main_deg.name}")],
                execution_status="completed", paper={"locator": "FIG3; SUP15; SUP6"}, confidence="medium",
                reasoning="Paper reports pathway results from GSEA; Hallmark GSEA on the full ranking of the planned contrast.")
except native.NativeToolError as e:
    enr_final["execution_error"] = str(e)
    case.decide("enrichment", final=enr_final, evidence=[case.evidence_item(f"tool_output:{main_deg.name}")],
                execution_status="failed", paper={"locator": "FIG3; SUP15; SUP6"}, confidence="medium",
                reasoning="GSEA failed; recorded.")

# ---------------- reproduction artifacts ----------------
disc = [
    {"item": "statistical method and DEG threshold", "paper": "deferred to Supplementary Methods (not retrievable)",
     "data": "-", "disposition": "requires_explicit_deviation",
     "action": "limma paired-change on log2(CPM+1); workflow default BH padj < 0.05"},
    {"item": "DEG count for exercise vs usual care", "paper": "46 (13 up, 33 down; S3.5.p1)",
     "data": f"0 at BH padj < 0.05; audit raw p < 0.01: {audit['raw_p_lt_0.01']['n_significant']}",
     "disposition": "blocks_reproduction", "action": "reported; paper genes rank near the top with the same direction"},
    {"item": "sequencing lanes", "paper": "not described", "data": "each library deposited as two lane GSMs (60 GSMs)",
     "disposition": "executable_without_change", "action": "lanes summed per library"},
    {"item": "participants", "paper": "usual care N=6, exercise N=9 (SUP7)", "data": "6 + 9 participants, all paired",
     "disposition": "executable_without_change", "action": "none"},
    {"item": "pathway libraries", "paper": "KEGG / GO BP / BIOCARTA GSEA", "data": "Hallmark only in repository",
     "disposition": "requires_explicit_deviation", "action": "Hallmark GSEA reported separately"},
]
case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
case.write_json("reproduction_plan.json", {
    "paper_aligned_route": {"estimand": "(ex: eos - base) - (uc: eos - base)", "method": "not_reported", "threshold": "not_reported"},
    "executed_route": {"method": "limma paired-change on log2(CPM+1) (preprocess_counts filter: count >= 10 in >= 3 libraries)",
                       "model": "~ 0 + C(grp) on per-participant change", "threshold": "BH padj < 0.05 (workflow_default)",
                       "status": "declared_deviation"},
    "exploratory": ["visit_eos_vs_base_grp-ex", "visit_eos_vs_base_grp-uc", "grp_ex_vs_uc_visit-base (DESeq2)",
                    "grp_ex_vs_uc_visit-eos (DESeq2)", PLANNED + "__sex-female"]}, role="reproduction_plan")
case.write_json("reproduction_summary.json", {
    "planned_contrast": PLANNED, "applied_threshold": "BH padj < 0.05, no effect cutoff (workflow_default)",
    "deg_counts_applied": counts, "audit_counts_planned_contrast": audit, "paper_count": {"n_up": 13, "n_down": 33},
    "paper_top_genes_in_our_ranking": gene_cmp,
    "conclusion": "Effect directions of the paper's highlighted genes reproduce, and they are among the top-ranked genes, but no gene passes BH FDR 0.05 with 15 participants; the paper's 46 DEGs likely used a looser or different rule that the main text does not state."},
    role="reproduction_summary")
json.dump(counts, open(R / "deg_counts.json", "w"), indent=1, default=str)

# ---------------- study ----------------
case.decide("study", final={"route": "declared_deviation",
                            "reason": "paper's method/threshold not reported in available text; validated limma paired-change route with workflow-default threshold",
                            "planned_contrast": PLANNED, "n_deg_planned": counts[PLANNED]["n_significant"],
                            "exploratory_contrasts": [k for k in counts if k != PLANNED],
                            "exploratory_reason": "female-only subset: usual care 5 participants; other contrasts not planned by the paper"},
            evidence=[paper, case.evidence_item("tool_output:reproduction_summary.json")], confidence="medium",
            reasoning="Planned interaction contrast executed; result and discrepancies recorded.")
case.finish(n_deg=counts[PLANNED]["n_significant"], deg_sanity=counts[PLANNED]["deg_sanity"])
run.finish()
print("finished")
