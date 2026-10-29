import sys, pathlib, json; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()

REL = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41142228"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12545138.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12545138.paper.md"
ACC = "GSE308626"
run = native.RunRecorder(REL, request=("Analyze GSE308626 for PMID 41142228 (Forced intensity-controlled endurance training on a "
    "small-animal treadmill machine inducing murine cardiac hypertrophy: insights and comparison to voluntary running): "
    "how exercise affects gene expression as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=[ACC])
case = run.case(ACC, accession=ACC)
paper = case.add_input(PAPER_JSON, "paper"); paper_md = case.add_input(PAPER_MD, "paper")
meta = case.add_input(f"data/{ACC}/{ACC}_metadata.csv", "metadata")
tar = case.add_input(f"data/{ACC}/{ACC}_RAW.tar", "matrix")
merged = case.add_input(f"data/{ACC}/{ACC}_merged_from_tar.csv", "matrix")

# ---------------- 1. paper_reconstruction
PT = {"metric": "FDR", "adjustment": "BH", "cutoff": 0.1, "effect_metric": None, "effect_cutoff": None,
      "inclusive": False, "source_locator": "S2.8.p3; FIG4"}
recon = {
    "paper_id": "PMID41142228 / PMC12545138",
    "accessions": [ACC],
    "accession_roles": {ACC: "bulk RNA-seq, whole heart, 8-week forced treadmill training vs sedentary (this case, S7.p1)",
                        "PRJNA811435": "external voluntary-running dataset (Lerchenmueller et al., 2022), raw SRA only; used by the paper only for the forced-vs-voluntary comparison (S2.8.p2, S3.4.p1)"},
    "assay": "bulk RNA-seq, NEBNext Ultra II Directional, NovaSeq 6000 1x100 SE; STAR 2.7.10a on GRCm39.107; RSEM 1.3.3 TPM (S2.8.p2, S2.8.p3)",
    "organism": "Mus musculus, male C57BL/6 WT, 8 weeks old at start (ABS.p1)",
    "sample_inclusion": ["10 samples: 5 mice after 8 weeks of forced treadmill training, 5 age-matched sedentary mice (S2.8.p2)"],
    "sample_exclusion": ["not_reported"],
    "factors": [{"name": "group", "levels": ["Sedentary (reference)", "Exercise (8-week forced treadmill)"]}],
    "primary_estimand": "Effect of 8 weeks of forced, intensity-controlled treadmill training on whole-heart gene expression vs age-matched sedentary controls (Exercise vs Sedentary)",
    "planned_contrasts": ["grp_ex_vs_sed"],
    "not_planned_here": {"forced_vs_voluntary": "Figure 4A/5 compare training effects against the external voluntary-running dataset PRJNA811435 (different lab, age, protocol, library prep; raw reads only). Not part of GSE308626 and not identifiable as a single within-study contrast; out of scope for this case."},
    "blocking_or_covariance": {"status": "not_required", "reason": "independent animals, one heart per mouse, one library pool (S2.8.p2)"},
    "normalization": "DESeq2 default (size factors); TPM from RSEM reported as expression values (S2.8.p3)",
    "matrix_scale": "not_reported which counts entered DESeq2; GEO provides STAR ReadsPerGene (integer) and RSEM genes.results (expected_count + TPM)",
    "paper_method": "DESeq2 1.36.0, R 4.2.0, default parameters (S2.8.p3)",
    "paper_formula": "not_reported (two-group, ~ group implied)",
    "paper_threshold": PT,
    "paper_reported_deg_counts": "not_reported (no DEG total given; only heatmaps of selected genes, FIG4)",
    "paper_enrichment": {"GSEA": "fgsea 1.22.0, msigdbr 7.5.1 GO BP, gene sets 15-500, ranked by DESeq2 statistic (S2.8.p3); results shown only for forced vs voluntary (FIG5)"},
    "paper_findings_to_compare": ["Myh7, Foxp1, Gata6, Akap13 up after training (S3.4.p4, S4.p20)",
                                  "Plin5, Fabp3, Gck, Acsf2 down; Col4a2 down (S3.4.p3)",
                                  "OXPHOS / aerobic respiration / ETC gene sets decreased after training (S3.4.p3, S4.p8)"],
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
case.decide("paper_reconstruction", final={"accessions": [ACC], "primary_estimand": recon["primary_estimand"],
            "planned_contrasts": recon["planned_contrasts"], "paper_threshold": PT, "paper_method": recon["paper_method"],
            "assay": recon["assay"], "matrix_scale": recon["matrix_scale"], "paper_reported_deg_counts": "not_reported",
            "out_of_scope": recon["not_planned_here"]},
            evidence=[paper, paper_md], paper={"locator": "S2.8.p2; S2.8.p3; S3.4.p1; FIG4; S7.p1"}, confidence="high",
            reasoning=("S2.8.p2: 5 trained vs 5 sedentary hearts after 8 weeks; S2.8.p3: STAR/RSEM, DESeq2 1.36 defaults, FDR < 0.1, "
                       "fgsea GO BP ranked by the DESeq2 statistic. No fold-change cutoff is stated and no DEG total is reported. "
                       "The forced-vs-voluntary comparison uses an external SRA project and is not part of this accession."))

# ---------------- 2. ownership
case.decide("ownership", final={"accession": ACC, "matrix_file": f"data/{ACC}/{ACC}_RAW.tar (STAR ReadsPerGene members, merged to {ACC}_merged_from_tar.csv)",
            "metadata_file": f"data/{ACC}/{ACC}_metadata.csv", "owned": True,
            "checks": {"series_id": f"{ACC} in metadata series_id; paper S7.p1 names {ACC}",
                       "samples": "10 GSMs: titles 'Exercise mouse 1-5', 'Control mouse 1-5'; treatment Exercise/Sedentary = paper's 5+5 (S2.8.p2)",
                       "tissue": "whole heart, WT, Mus musculus (S2.8.p1)",
                       "protocol": "NEBNext Ultra II Directional, NovaSeq 6000 1x100, STAR 2.7.10a GRCm39.107, RSEM 1.3.3 - matches S2.8.p2-p3 verbatim",
                       "contact": "Maximilian Fischer, LMU University Munich (author affiliation)"},
            "files_in_tar": "per GSM one STAR ReadsPerGene.out.tab and one RSEM genes.results"},
            evidence=[meta, tar, merged, paper], paper={"locator": "S7.p1; S2.8.p2"}, confidence="high",
            reasoning="Series ID, sample count, group labels, tissue, strain and processing text all match the paper's Methods.")

# ---------------- 3. alignment
adir = case.dir / "aligned"
derived = native.derive_columns(f"data/{ACC}/{ACC}_metadata.csv", adir / "derived_metadata_full.csv",
    patterns={"count_col": ("supplementary_file_1", r"/(GSM\d+_22066-\d+)\.ReadsPerGene\.out\.tab\.gz$"),
              "grp": ("characteristics_ch1.2.treatment", r"^(.+)$")},
    recode={"grp": {"Exercise": "ex", "Sedentary": "sed"}})
aln = native.align_to_metadata(merged["path"], adir / "derived_metadata_full.csv", adir, key_column="count_col")
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
dmeta = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], adir / "design_metadata.csv",
                              aliases={"sample_title": "title"})
dm = case.add_output(dmeta["output"], "design_metadata")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
            "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
            "unmatched_metadata_samples": aln["unmatched_metadata_samples"], "derived_columns": derived["columns"],
            "levels": derived["levels"]},
            evidence=[merged, meta, am, amd, amap, dm], paper={"locator": "S2.8.p2"}, confidence="high",
            reasoning="Merged matrix columns are the GSM-prefixed ReadsPerGene file stems; the same stem is in each GSM's supplementary_file_1. Extracted it as count_col and aligned exactly. grp from characteristics treatment (Exercise=ex, Sedentary=sed).")

# ---------------- 4. matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
prof_item = case.write_json("matrix_profile.json", prof, role="matrix_profile")
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
            "integer_fraction": prof.get("integer_fraction"), "min": prof.get("min"), "max": prof.get("max"),
            "missing_values": prof.get("missing_values"),
            "source": "STAR --quantMode GeneCounts ReadsPerGene.out.tab, column 4 (reverse strand); N_* summary rows excluded by merge_raw_tar",
            "strand_evidence": "forward total 17.1M vs reverse 354M reads over 10 samples (ratio 20.8) - consistent with dUTP NEBNext Ultra II Directional",
            "feature_ids": "Ensembl mouse gene IDs (GRCm39.107)",
            "paper_input": "not_reported (paper names STAR, RSEM TPM and DESeq2)"},
            candidates=[{"value": "RSEM expected_count (rounded)", "reason_rejected": "estimated counts; rounding recipe not documented in the paper; STAR integer gene counts from the same alignment are deposited"},
                        {"value": "RSEM TPM", "reason_rejected": "normalized linear values; DESeq2 requires counts"}],
            evidence=[am, prof_item, meta, paper], paper={"locator": "S2.8.p3"}, confidence="medium",
            reasoning="All values are non-negative integers from STAR GeneCounts on uniquely mapped reads; the reverse column matches the dUTP stranded kit. These are genuine read counts suitable for DESeq2. The paper does not say whether DESeq2 used STAR counts or RSEM expected counts, so confidence is medium.")

# ---------------- 5. design
md = pd.read_csv(dmeta["output"], index_col=0)
rep, s_item, s_summary = case.suitability(matrix_type="raw counts", metadata=md, factors=["grp"],
    matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Mouse", subject=None,
    references={"grp": "sed"}, planned=["grp_ex_vs_sed"])
print("suitability", json.dumps(s_summary), [c.get("name") for c in rep["comparisons"]])
dchk = native.design_check(dmeta["output"], ["grp"])
dc_item = case.write_json("design_check.json", dchk, role="design_check")
case.decide("design", final={"analysis_type": "two_group (independent animals)", "design_column": "grp",
            "formula": "~ grp", "control": "sed", "treatment": "ex",
            "contrasts": [{"name": "grp_ex_vs_sed", "control": "sed", "treatment": "ex",
                           "description": "8-week forced treadmill training vs sedentary, whole heart"}],
            "estimand_type": "causal (randomised intervention, GEO overall design)", "suitability": s_summary,
            "levels": dchk.get("levels")},
            candidates=[{"value": "forced vs voluntary running (vs PRJNA811435)", "reason_rejected": "external study, not in this accession; between-study differences (age, protocol, lab, library) are aliased with the model"}],
            evidence=[dm, dc_item, s_item, paper], paper={"locator": "S2.8.p2; S3.4.p1"}, confidence="high",
            reasoning="Two randomised groups of 5 independent mice; the paper's within-study DE is training vs sedentary at 8 weeks.")

# ---------------- 6. covariance
case.decide("covariance", final={"status": "not_required", "blocking_terms": [], "covariates": [],
            "considered": "metadata has no batch, sex, or lane column varying within the series (all male WT whole heart; one library pool, one sequencing run per S2.8.p2)",
            "rank": dchk.get("rank"), "residual_df": dchk.get("residual_df")},
            evidence=[dm, dc_item, paper], paper={"locator": "S2.8.p2"}, confidence="high",
            reasoning="Each GSM is a different mouse; no repeated measures and no batch structure is described or present in metadata.")

# ---------------- 7. method
case.decide("method", final={"method": "DESeq2 (pydeseq2, Wald test)", "matrix_type": "raw counts", "formula": "~ grp",
            "effect_size": "MLE log2FoldChange, no shrinkage (DESeq2 results() default)",
            "pre_filter": "executor default; DESeq2 independent filtering of padj",
            "paper_route_note": "paper used R DESeq2 1.36.0 defaults; pydeseq2 implements the same model (implementation difference only)"},
            evidence=[prof_item, dc_item, paper], paper={"locator": "S2.8.p3"}, confidence="high",
            reasoning="Integer counts support the paper's DESeq2 route directly; two-group design with no covariates.")

# ---------------- 8. threshold
case.decide("threshold", final={"paper_threshold": PT, "threshold_source": "paper", "applied_threshold": dict(PT)},
            evidence=[paper], paper={"locator": "S2.8.p3; FIG4"}, confidence="high",
            reasoning="Paper: adjusted p-value (FDR) < 0.1 classifies significant genes; no fold-change cutoff stated. Applied as BH padj < 0.1 with no effect cutoff.")

case.write_json("reproduction_plan.json", {"executor": "tools.deseq2_tools:run_deseq2_analysis", "counts_csv": aln["outputs"]["aligned_matrix"]["path"],
    "metadata_csv": dmeta["output"], "contrast": "ex vs sed", "threshold": PT,
    "enrichment": "GSEA Hallmark (repository) ranked by stat - declared deviation from paper's fgsea GO BP"}, role="reproduction_plan")
case.write_json("paper_data_discrepancies.json", [
    {"item": "count input", "paper": "STAR + RSEM TPM; DESeq2 input not stated", "data": "STAR ReadsPerGene and RSEM genes.results both deposited", "disposition": "executable_without_change", "action": "STAR reverse-strand integer counts used"},
    {"item": "forced vs voluntary comparison", "paper": "FIG4A/FIG5 vs PRJNA811435", "data": "external raw SRA project, not in GSE308626", "disposition": "out_of_scope", "action": "not analysed"},
    {"item": "GSEA gene sets", "paper": "fgsea GO BP (msigdbr 7.5.1), 15-500 genes", "data": "repository GSEA uses MSigDB Hallmark", "disposition": "requires_explicit_deviation", "action": "Hallmark GSEA as declared deviation"},
    {"item": "age", "paper": "8 weeks old at start (ABS.p1)", "data": "GEO summary says 5-8 weeks old", "disposition": "executable_without_change", "action": "noted only"},
], role="paper_data_discrepancies")

# ---------------- 9. execution
rdir = case.dir / "results"
method = "DESeq2 (pydeseq2, Wald test) ~ grp"
try:
    msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=aln["outputs"]["aligned_matrix"]["path"],
                           metadata_csv=dmeta["output"], design_column="grp", control_group="sed", treatment_group="ex",
                           output_dir=str(rdir))
    print(msg[-1500:])
    deg = native.deg_outputs(rdir)[0]
    thr = native.apply_threshold(deg, metric="padj", cutoff=0.1, effect_cutoff=None)
    thr05 = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
    deg_item = case.add_output(deg, "deg_table")
    case.write_json("results/threshold_counts.json", {"applied_padj_0.1": thr, "audit_padj_0.05": thr05}, role="threshold_counts")
    case.decide("execution", final={"method": method, "outputs": [str(deg)], "n_deg": thr["n_significant"],
                "n_up": thr.get("n_up"), "n_down": thr.get("n_down"), "audit_padj_0.05_n_deg": thr05["n_significant"],
                "deg_sanity": thr.get("deg_sanity")},
                evidence=[am, dm, deg_item], confidence="high", execution_status="completed",
                reasoning="DESeq2 ran on 5 vs 5 aligned samples; threshold applied with native.apply_threshold.")
    ok = True
except native.NativeToolError as e:
    case.decide("execution", final={"method": method, "execution_error": str(e)}, evidence=[am, dm], confidence="high",
                execution_status="failed", reasoning="executor failed")
    ok = False; thr = {"n_significant": None, "deg_sanity": None}

# paper findings check
if ok:
    d = pd.read_csv(deg, index_col=0)
    print(d.columns.tolist()[:12]); print(d.head(3))
    json.dump({"deg": str(deg)}, open(case.dir / "results" / "_deg_path.json", "w"))
json.dump({"ok": ok, "thr": thr}, open(case.dir / "_stage1.json", "w"), default=str)
