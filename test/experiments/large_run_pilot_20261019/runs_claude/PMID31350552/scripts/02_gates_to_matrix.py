import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID31350552"
run = native.RunRecorder.open(RUN); case = run.case("GSE129962")
P = "test/experiments/paper_screen_20261019/papers/"
D = "data/GSE129962/"
paper = case.add_input(P + "PMC7177479.paper.md", "paper")
paperj = case.add_input(P + "PMC7177479.paper.json", "paper")
meta = case.add_input(D + "GSE129962_metadata.csv", "metadata")
matf = case.add_input(D + "GSE129962_DSP.combined.RAW.featureCounts.txt.gz", "matrix")

# ---------- paper_reconstruction
paper_threshold = {"metric": "qvalue", "adjustment": "not_reported (edgeR q-value; executor applies BH)", "cutoff": 0.05,
                   "effect_metric": None, "effect_cutoff": None, "inclusive": False, "source_locator": "S5.7.p2"}
study_map = {
    "paper_id": "PMID31350552 / PMC7177479 / doi:10.1093/cvr/cvz199",
    "accessions": ["GSE129962"],
    "assay": "bulk total RNA-seq (rRNA-depleted, stranded, PE, HiSeq 4000) of isolated adult cardiac myocytes (S5.7.p1, S5.6)",
    "organism": "Mus musculus",
    "sample_inclusion": "N=5 per group, matched for age and sex (S5.7.p1, S6.1.p3, FIG2); groups: WT and Myh6-Cre:Dsp W/F at 3 months (regular activity), at 6 months regular activity, and at 6 months after 3 months of daily treadmill exercise started at 3 months (S5.5.p1, S6.4.p3)",
    "sample_exclusion": "none for RNA-seq: one Myh6-Cre:Dsp W/F exercised mouse stopped exercising at 2.5 months (severe LV dysfunction) and was still sequenced and shown in Fig 3A (S6.4.p3, S6.4.p6); qPCR used N=4 (FIG2)",
    "factors": [{"name": "genotype", "levels": ["WT", "Myh6-Cre:Dsp W/F"]},
                {"name": "activity", "levels": ["regular activity", "treadmill exercise (60 min/day, 5.5 kJ, 3 months)"]},
                {"name": "age", "levels": ["3 months", "6 months"], "note": "exercise only at 6 months"}],
    "primary_estimand": "effect of 3 months of treadmill exercise vs regular activity on cardiac myocyte gene expression at 6 months, within WT and within Myh6-Cre:Dsp W/F mice (S6.4.p4, S6.4.p5); secondary: genotype-by-exercise interaction (S6.4.p11) and rescue of the 6-month genotype DEGs (S6.4.p6)",
    "planned_contrasts": [
        "WT exercise vs WT regular activity at 6 months: 2529 DEGs (1390 up, 1139 down), q<0.05 (S6.4.p4)",
        "Dsp exercise vs Dsp regular activity at 6 months: 2391 DEGs (867 up, 1524 down), q<0.05 (S6.4.p5, FIG2)",
        "genotype-by-exercise interaction: 65 genes (19 up, 46 down), q<0.05 (S6.4.p11)"],
    "context_contrasts_non_exercise": [
        "Dsp vs WT at 3 months: 56 DEGs (S6.1.p4)", "Dsp vs WT at 6 months regular activity: 781 DEGs (614 up, 167 down) (S6.1.p5)",
        "WT 6 vs 3 months: 310 DEGs (S6.2.p1, RUVr)", "Dsp 6 vs 3 months: 1643 DEGs (S6.2.p2, RUVr)",
        "rescue: Dsp-Ex vs WT not different for 492/781 genotype DEGs (S6.4.p6)"],
    "repeated_measure_unit": "none; each sample is a different mouse, randomized to activity (S5.5.p1)",
    "blocking_or_covariance": {"status": "not_required", "note": "between-animal design; sex and age matched (S5.7.p1)"},
    "matrix_scale": "featureCounts raw read counts (S5.7.p2)",
    "normalization": "TopHat2 -> featureCounts; edgeR; RUVr for comparisons across time points only (S5.7.p2)",
    "paper_method": "edgeR (test and model formula not reported) (S5.7.p2)",
    "paper_formula": "not_reported",
    "paper_threshold": paper_threshold,
    "paper_pathway": "GSEA 2.2.3, MSigDB hallmark + canonical pathways, q<0.05 (S5.8.p1); exercise in Dsp: protein secretion, PI3K/AKT/MTOR, mitotic spindle up; inflammation, EMT, OXPHOS down (S6.4.p5)",
}
case.write_json("paper_reconstruction.json", study_map)
case.decide("paper_reconstruction", final=study_map, evidence=[paper, paperj], paper={"locator": "S5.7.p2"}, confidence="high",
    reasoning="S5.1.p1 names GSE129962. S5.5/S6.4 define the exercise design (WT and Dsp mice randomized at 3 months to regular activity or treadmill for 3 months). S5.7.p2 gives edgeR on featureCounts with q<0.05 and no fold-change cutoff. Exercise counts in S6.4.p4/p5, interaction in S6.4.p11.")

# ---------- ownership
m = pd.read_csv(meta["path"], index_col=0)
raw = pd.read_csv(matf["path"], sep="\t")
grp_tab = pd.crosstab(m["characteristics_ch1.1.genotype/variation"], [m["title"].str.extract(r"^(\dM)")[0], m["characteristics_ch1.2.exercise"]])
chk = {"series_id": sorted(m["series_id"].unique().tolist()), "n_gsm": int(len(m)), "cell_type": sorted(m["characteristics_ch1.0.cell type"].unique().tolist()),
       "genotype_x_age_x_exercise": {str(k): v for k, v in grp_tab.to_dict().items()},
       "matrix_sample_columns": int(raw.shape[1] - 3), "matrix_annotation_columns": ["GeneID", "GeneSymbol", "GeneBiotype"],
       "paper_design": "N=5 per group, 6 groups (S5.7.p1, S6.1.p3, FIG2)"}
print(json.dumps(chk, default=str))
case.decide("ownership", final={"accession": "GSE129962", "matrix_file": "GSE129962_DSP.combined.RAW.featureCounts.txt.gz",
    "metadata_file": "GSE129962_metadata.csv", "owned": True, "checks": chk},
    evidence=[meta, matf, paper], paper={"locator": "S5.1.p1"}, confidence="high",
    reasoning="Series GSE129962 is the paper's deposit (S5.1.p1). 30 cardiac-myocyte GSMs = 6 groups x 5 (WT/Dsp x 3M RA / 6M RA / 6M EX), matching the paper; matrix has 30 sample columns named by the GEO title prefix.")

case.write_json("paper_data_discrepancies.json", [
    {"item": "edgeR model and test", "paper": "edgeR, model/test not reported (S5.7.p2)", "data": "raw featureCounts available",
     "disposition": "executable_without_change (edgeR QL two-arm executor; whether the paper fitted pairwise or a joint GLM is unknown)"},
    {"item": "genotype-by-exercise interaction", "paper": "edgeR interaction, 65 genes (S6.4.p11)",
     "data": "repository edgeR executor has no interaction interface", "disposition": "requires_explicit_deviation (DESeq2 joint cell-means model, interaction contrast)"},
    {"item": "RUVr normalization for cross-time-point comparisons", "paper": "RUVr (S5.7.p2)", "data": "no RUVr executor in the repository",
     "disposition": "requires_explicit_deviation for age contrasts (not exercise contrasts; exploratory only)"},
    {"item": "the Dsp exercised mouse that stopped at 2.5 months", "paper": "sequenced and included (S6.4.p3, S6.4.p6)",
     "data": "metadata does not say which DH-EX replicate it is", "disposition": "executable_without_change (kept, as in the paper)"},
    {"item": "sex", "paper": "sex-matched (S5.7.p1), sexes not reported", "data": "no sex field in GEO", "disposition": "executable_without_change (checked by X/Y genes in suitability)"},
])

# ---------- alignment
adir = case.dir / "aligned"; adir.mkdir(parents=True, exist_ok=True)
print("dup GeneID:", int(raw["GeneID"].duplicated().sum()))
cnt = raw.drop(columns=["GeneSymbol", "GeneBiotype"]).set_index("GeneID")
cnt.to_csv(adir / "counts_by_ensembl.csv")
raw[["GeneID", "GeneSymbol", "GeneBiotype"]].to_csv(adir / "gene_annotation.csv", index=False)
key = native.derive_columns(meta["path"], adir / "meta_key.csv", patterns={"libkey": ("title", r"^([^:]+):")})
aln = native.align_to_metadata(adir / "counts_by_ensembl.csv", adir / "meta_key.csv", adir, key_column="libkey")
print({k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")})
der = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], adir / "design_metadata.csv",
    aliases={"genotype_src": "characteristics_ch1.1.genotype/variation", "exercise_src": "characteristics_ch1.2.exercise"},
    patterns={"geno": ("title", r"^\dM-(?:EX-)?(WT|DH|Het)\d"), "cond": ("title", r"^(\dM-(?:EX-)?)")},
    recode={"geno": {"WT": "WT", "DH": "DH", "Het": "DH"}, "cond": {"3M-": "RA3", "6M-": "RA6", "6M-EX-": "EX6"}})
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)
# consistency: title-derived labels vs characteristics
cons = {"geno_vs_characteristics": bool(((dm["geno"] == "WT") == (dm["genotype_src"] == "Wildtype")).all()),
        "cond_vs_exercise": bool(((dm["cond"] == "EX6") == (dm["exercise_src"] == "yes")).all()),
        "cells": pd.crosstab(dm["geno"], dm["cond"]).to_dict()}
print(cons)
outs = [case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix"),
        case.add_output(adir / "design_metadata.csv", "design_metadata"),
        case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")]
case.decide("alignment", final={"method": "exact on derived key 'libkey' (GEO title prefix before ':')", "n_aligned": aln["n_aligned"],
    "n_metadata": aln["n_metadata"], "coverage": aln["coverage"], "unmatched": [], "key_derivation": key, "derived_columns": der,
    "label_consistency": cons},
    evidence=[matf, meta] + outs, confidence="high",
    reasoning="Matrix columns (e.g. 6M-EX-WT5, 3M-Het6) equal the GEO title prefix before ':'. Exact match, full coverage. geno (WT / DH = Myh6-Cre:Dsp W/F; 'Het' and 'DH' both denote Dsp W/F) and cond (RA3, RA6, EX6) derived from the title and cross-checked against the genotype and exercise characteristics.")

# ---------- matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print(json.dumps(prof, default=str)[:2000])
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "edgeR (paper) / DESeq2",
    "profile": prof, "source": "file name 'RAW.featureCounts'; GEO data_processing (featureCounts); S5.7.p2",
    "paper_input": "featureCounts read counts into edgeR (S5.7.p2)"},
    evidence=outs[:1] + [matf, meta, paper], paper={"locator": "S5.7.p2"}, confidence="high",
    reasoning="Non-negative integers, featureCounts output named RAW; paper used them in edgeR.")

# suitability preview (recorded in the design gate by the next script)
from tools import suitability as su
rep = su.report(case_id="preview", out_dir=str(case.dir / "_suitability_preview"), matrix_type="raw counts", metadata=dm,
                factors=["geno", "cond"], matrix_csv=str(aln["outputs"]["aligned_matrix"]["path"]), organism="Mouse",
                subject=None, references={"geno": "WT", "cond": "RA6"})
print(rep["verdict"], rep["failed"], rep["warnings"])
print(json.dumps(rep["checks"].get("sex", {}), default=str)[:1500])
for c in rep["comparisons"]:
    print(c["name"], c["kind"], c["analyzable"], [x["n"] for x in c["cells"]])
