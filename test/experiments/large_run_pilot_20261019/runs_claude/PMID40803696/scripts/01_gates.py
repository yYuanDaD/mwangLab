"""Gates 1-5 for GSE295777 / PMID40803696. The sequenced set has no exercise arm -> refused at design."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40803696"
CASE = "PMID40803696"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC12476895.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC12476895.paper.md"
META = "data/GSE295777/GSE295777_metadata.csv"
TAR = "data/GSE295777/GSE295777_RAW.tar"

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE295777 for PMID 40803696 (Transcription factor Yin-Yang 1 governs cardiac metabolic "
             "reprogramming in response to exercise or pathological stress): how exercise affects gene expression "
             "as the paper intends."),
    platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
    case_ids=[CASE])
case = run.case(CASE, accession="GSE295777")
paper = case.add_input(PAPER_JSON, "paper")
case.add_input(PAPER_MD, "paper")
meta_ev = case.add_input(META, "metadata")
tar_ev = case.add_input(TAR, "matrix")

# ---------------------------------------------------------------- 1 paper_reconstruction
paper_threshold = {"metric": "FDR", "adjustment": "not_reported (DESeq2 default BH)", "cutoff": 0.05,
                   "effect_metric": "log2FC", "effect_cutoff": math.log2(1.5),
                   "effect_cutoff_original": "fold change > 1.5", "inclusive": False,
                   "source_locator": "S2.2.p2; FIG3"}
study_map = {
    "paper_id": "PMID40803696 / PMC12476895",
    "accessions": ["GSE295777"], "accession_locator": "DA.p1",
    "assay": "bulk RNA-seq of heart (BGI), STAR mm10 read counts (S2.2.p2)",
    "sample_inclusion": ["RNA-seq: male MerCreMer control vs cYY1 KO mice after TAC, n=4 per group (S2.2.p2; FIG3 n=4)"],
    "sample_exclusion": ["not_reported"],
    "factors": [{"name": "genotype", "levels": ["MerCreMer control", "cYY1 KO"], "locator": "S2.2.p2"},
                {"name": "stress", "levels": ["TAC only in the sequenced set"], "locator": "S2.2.p2, FIG3"}],
    "exercise_arm": ("Two-week swimming (S2.1.p2) was studied only by echocardiography, qPCR of Ppargc1a/Ppara/Esrra, "
                     "citrate synthase and co-IP (S3.1.p1, FIG1, FIG4). No swimming or sedentary heart was sequenced."),
    "primary_estimand": ("RNA-seq estimand: effect of cardiac YY1 deletion on the TAC-stressed heart transcriptome "
                         "(cYY1 KO vs MerCreMer control, both TAC). The exercise effect on gene expression is not an "
                         "RNA-seq estimand in this paper."),
    "planned_contrasts": [{"name": "KO_vs_ctrl_TAC", "definition": "cYY1 KO TAC vs MerCreMer control TAC",
                           "locator": "S2.2.p2, S3.3.p1, FIG3"}],
    "blocking_or_covariance": {"status": "not_required", "note": "one heart per mouse, between-animal arms"},
    "matrix_scale": "STAR read counts (S2.2.p2)",
    "paper_method": "DESeq2 on read counts (S2.2.p2)",
    "paper_formula": "not_reported (two-group)",
    "paper_threshold": paper_threshold,
    "reported_counts": {"KO_vs_ctrl_TAC": "1,825 up, 1,752 down (3,577 total) (S3.3.p1, FIG3)"},
    "enrichment": {"method": "IPA on DEGs, pathway FDR 5% (S2.2.p2); no executor (proprietary IPA)"},
    "internal_discrepancy": "TAC duration: 'one week' (S2.2.p2) vs '10 days after TAC' (FIG3)",
}
case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
case.decide("paper_reconstruction", final=study_map, evidence=[paper],
            paper={"locator": "S2.2.p2; S3.3.p1; FIG3; S2.1.p2; S3.1.p1; DA.p1"},
            reasoning=("Methods S2.2.p2 restricts RNA-seq to male TAC hearts, control vs cYY1 KO, n=4, DESeq2, "
                       "FC>1.5 and FDR 5%. The exercise experiments (S2.1.p2, FIG1) used only echo, qPCR, CS activity."),
            confidence="high")

# ---------------------------------------------------------------- 2 ownership
merged = native.merge_raw_tar("data/GSE295777")
print("merged:", json.dumps(merged, indent=1))
meta = pd.read_csv(META, index_col=0)
own = {"accession": "GSE295777", "matrix_file": merged["output"], "matrix_source": TAR,
       "metadata_file": META, "owned": True,
       "checks": {"series_id": sorted(meta["series_id"].unique().tolist()),
                  "n_samples_geo": len(meta), "n_samples_paper": 8,
                  "groups_geo": meta["title"].str.replace(r" \d+$", "", regex=True).value_counts().to_dict(),
                  "treatment_geo": meta["characteristics_ch1.2.treatment"].unique().tolist(),
                  "processing": "Trimmomatic + STAR mm10, matches S2.2.p2"}}
mat_ev = case.add_output(merged["output"], "merged_matrix")
case.decide("ownership", final=own, evidence=[paper, meta_ev, tar_ev, mat_ev], paper={"locator": "DA.p1; S2.2.p2"},
            reasoning=("Series is the paper's deposit (DA.p1); 8 TAC hearts, 4 MerCreMer control + 4 cYY1 KO, "
                       "matching S2.2.p2 n=4 per group; processing matches."),
            confidence="high")

# ---------------------------------------------------------------- 3 alignment
cols = merged["samples"]
print("matrix columns:", cols)
mat = pd.read_csv(merged["output"], index_col=0)
# Column names come from member file names GSM*_F-*; key them to the GSM accession (the metadata index).
ren = {c: c.split("_")[0] for c in mat.columns}
assert all(v.startswith("GSM") for v in ren.values()), ren
keyed = case.dir / "aligned" / "matrix_gsm_keyed.csv"
keyed.parent.mkdir(parents=True, exist_ok=True)
mat.rename(columns=ren).to_csv(keyed)
aln = native.align_to_metadata(keyed, META, case.dir / "aligned")
print("alignment:", {k: v for k, v in aln.items() if k != "outputs"})
derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    patterns={"grp": ("title", r"^(MerCreMer control|Cardiac-specific YY1 KO) mouse \d$")},
    recode={"grp": {"MerCreMer control": "ctrl", "Cardiac-specific YY1 KO": "ko"}})
aligned_mat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
aligned_meta = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
design_meta = case.add_output(case.dir / "aligned" / "design_metadata.csv", "design_metadata")
case.decide("alignment",
            final={"method": aln["method"] + " (matrix columns keyed by the GSM prefix of each tar member name)",
                   "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                   "column_rename": ren, "derived_columns": derived,
                   "unmatched": aln["unmatched_metadata_samples"] + aln["unmatched_matrix_columns"]},
            evidence=[mat_ev, meta_ev, aligned_mat, aligned_meta, design_meta],
            reasoning="Each tar member is named GSMxxxx_F-n; the GSM prefix matches the metadata index exactly (8/8).",
            confidence="high")

# ---------------------------------------------------------------- 4 matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print("profile:", json.dumps(prof, indent=1, default=str)[:2000])
fid = native.feature_id_report(aln["outputs"]["aligned_matrix"]["path"])
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                   "evidence_summary": {"integer_fraction": prof.get("integer_fraction"),
                                        "min": prof.get("min"), "max": prof.get("max"),
                                        "type_candidates": prof.get("type_candidates"),
                                        "strand_column": "STAR ReadsPerGene column chosen by merge_raw_tar (see merge log)",
                                        "feature_ids": fid.get("id_type")},
                   "paper_input": "read counts (S2.2.p2)"},
            evidence=[aligned_mat, meta_ev, paper], paper={"locator": "S2.2.p2"},
            reasoning="STAR ReadsPerGene integer gene counts; paper used DESeq2 on read counts.",
            confidence="high")

# ---------------------------------------------------------------- 5 design (suitability, then refuse)
dm = pd.read_csv(case.dir / "aligned" / "design_metadata.csv", index_col=0)
rep, item, summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["grp"],
                                      matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Mouse",
                                      subject=None, references={"grp": "ctrl"}, planned=["grp_ko_vs_ctrl"])
print("suitability:", json.dumps(summary, indent=1))
print("comparisons:", [c.get("name") for c in rep["comparisons"]])
print("sex:", json.dumps(rep["checks"].get("sex"), indent=1, default=str)[:1500] if "checks" in rep else rep.keys())
case.decide("design",
            final={"suitability": summary,
                   "available_factor": {"grp": {"ctrl": 4, "ko": 4}, "all_samples_treatment": "TAC"},
                   "requested_estimand": "effect of exercise (swimming) on cardiac gene expression"},
            candidates=[{"value": "grp: ko vs ctrl (all TAC)",
                         "reason_rejected": ("genotype contrast under pressure overload; answers the paper's RNA-seq "
                                             "question but not the requested exercise question")},
                        {"value": "characteristics_ch1.2.treatment", "reason_rejected": "single level (TAC)"}],
            evidence=[paper, meta_ev, design_meta, item], paper={"locator": "S2.2.p2; FIG3; FIG1; S3.1.p1"},
            reasoning=("All 8 sequenced hearts are TAC (GEO treatment = Transaortic constriction; S2.2.p2). No swimming "
                       "or sedentary heart was sequenced; the exercise data (FIG1) are echo/qPCR/CS only. The only "
                       "contrast is cYY1 KO vs control under TAC, a genotype-under-pathological-stress estimand that "
                       "does not identify an exercise effect."),
            confidence="high", decision_status="refused", execution_status="not_run",
            stop_reason=("no exercise contrast in the sequenced samples: GSE295777 is 4 MerCreMer control vs 4 cYY1 KO "
                         "hearts, all after TAC; the paper's swimming experiment was not sequenced"))
discrepancies = [
    {"item": "requested estimand vs deposited data", "paper": "exercise studied by echo/qPCR/CS only (FIG1)",
     "data": "all 8 samples TAC", "disposition": "blocks_reproduction"},
    {"item": "TAC duration", "paper": "one week (S2.2.p2) vs 10 days (FIG3)", "data": "not stated in GEO",
     "disposition": "executable_without_change"},
    {"item": "sex", "paper": "male (S2.2.p2)", "data": "GEO has no sex field; see suitability sex check",
     "disposition": "executable_without_change"},
]
case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")
case.write_json("reproduction_plan.json", {"paper_route": "DESeq2 KO vs ctrl under TAC, FC>1.5 & FDR<0.05",
                                           "requested_route": "exercise vs sedentary", "status": "refused at design"},
                role="reproduction_plan")
case.write_json("reproduction_summary.json", {"status": "refused_design", "n_deg": None,
                                              "reason": "no exercise samples sequenced"}, role="reproduction_summary")
print(case.finish())
print(run.finish())
