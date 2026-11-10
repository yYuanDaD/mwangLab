import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID35456380"
run = native.RunRecorder.open(RUN); case = run.case("GSE164890")
P = "test/experiments/paper_screen_20261019/papers/"
SCR = pathlib.Path(RUN) / "author_code"
paper = case.add_input(P + "PMC9027771.paper.md", "paper")
paperj = case.add_input(P + "PMC9027771.paper.json", "paper")
author_r = case.add_input(str(SCR / "all_analysis_and_figures.R"), "paper")
author_cond = case.add_input(str(SCR / "Conditions.txt"), "paper")
meta = case.add_input("data/GSE164890/GSE164890_metadata.csv", "metadata")
counts = case.add_input("data/GSE164890/GSE164890_rsem.genes.counts.tsv.gz", "matrix")
tpm = case.add_input("data/GSE164890/GSE164890_rsem.genes.TPM.tsv.gz", "matrix")

# ---------- paper_reconstruction
paper_threshold = {"metric": "padj", "adjustment": "BH (DESeq2 results() default)", "cutoff": 0.1,
                   "effect_metric": None, "effect_cutoff": None, "inclusive": True,
                   "source_locator": "S2.5.p1; FIG1 legend ('reported at 10% FDR'); author script all_analysis_and_figures.R:83-84 (padj <= 0.1)"}
study_map = {
    "paper_id": "PMID35456380 / PMC9027771 / doi:10.3390/genes13040574",
    "accessions": ["GSE164890"],
    "other_accessions_in_paper": {"GSE149938": "public scRNA-seq used for cell-type signatures (S2.6.p1), not exercise DE",
                                  "8 microarray studies": "sea-level exercise reanalysis (S2.7.p1), not this deposit"},
    "assay": "bulk RNA-seq, globin-depleted whole blood, stranded polyA, HiSeq 4000 PE150 (S2.3.p1)",
    "organism": "Homo sapiens",
    "sample_inclusion": "7 female elite speed skaters, day 18 of altitude camp (1850 m), whole blood before and after an intense 1 h skating bout; 14 samples (S2.1.p1, S2.1.p2, S2.3.p1)",
    "sample_exclusion": "none reported",
    "factors": [{"name": "exercise", "levels": ["before", "after"]},
                {"name": "donor", "levels": "7 skaters (d1..d7), each sampled before and after"}],
    "primary_estimand": "Within-skater change in whole-blood gene expression after vs before an intense 1 h skating bout at altitude (S2.5.p1, FIG1)",
    "planned_contrasts": ["after vs before exercise, donor-blocked (DESeq2 ~ donor + exercise); 2516 up / 1542 down at 10% FDR (S3.2.p2)"],
    "repeated_measure_unit": "donor (skater); paired pre/post (FIG1 'donor + exercise' design; S3.2.p1)",
    "blocking_or_covariance": {"status": "required", "term": "donor"},
    "matrix_scale": "RSEM gene-level expected counts (S2.4.p1), rounded with round(x, 0) before DESeq2 (author script line 66)",
    "normalization": "DESeq2 size factors; rlog + ComBat only for PCA/plots (S2.5.p1)",
    "paper_method": "DESeq2 v1.18.1 (S2.5.p1)",
    "paper_formula": "~ donor + exercise, contrast exercise after vs before (FIG1; author script lines 66-69)",
    "gene_filter": "none before DESeq2 (author script line 66 uses the full table; DESeq2 independent filtering at default alpha 0.1)",
    "paper_threshold": paper_threshold,
    "paper_result": {"up": 2516, "down": 1542, "total": 4058, "more_than_twofold": {"up": 104, "down": 58}, "locator": "S3.2.p2"},
    "enrichment_in_paper": "ORA (clusterProfiler) with MSigDB H and CP collections, plus fGSEA (S2.5.p1, S3.3.p1)",
    "author_code": "https://github.com/apredeus/skater_rnaseq (cited in S2.7.p1 and S10.p1); all_analysis_and_figures.R and data/Conditions.txt saved in author_code/",
}
case.write_json("paper_reconstruction.json", study_map)
case.decide("paper_reconstruction", final=study_map, evidence=[paper, paperj, author_r, author_cond], paper={"locator": "S2.5.p1"}, confidence="high",
    reasoning="S2.3.p1 and S10.p1 name GSE164890 as the paper's deposit (14 samples, 7 skaters before/after). S2.5.p1 and FIG1 give DESeq2 with a 'donor + exercise' design and 10% FDR; S3.2.p2 gives 2516 up / 1542 down. The authors' script, cited by the paper, confirms round(counts,0), no prefilter, relevel to 'before', results() with default alpha and padj <= 0.1.")

case.write_json("paper_data_discrepancies.json", [
    {"item": "matrix values", "paper": "DESeq2 on the RSEM per-gene table (S2.5.p1)",
     "data": "GSE164890_rsem.genes.counts.tsv.gz holds RSEM expected counts; 5,889 of 58,233 genes have non-integer values",
     "disposition": "executable_without_change", "note": "the authors' script rounds with round(x, 0) (line 66); the same rounding is applied here and recorded as rounding_documented"},
    {"item": "donor key", "paper": "donor d1..d7 (author Conditions.txt)", "data": "GEO title 'Skater N - before/after exercise' and description 'Nbefore/Nafter'",
     "disposition": "executable_without_change"},
    {"item": "DESeq2 implementation", "paper": "R DESeq2 v1.18.1", "data": "pydeseq2 executor (tools/deseq2_tools.py)",
     "disposition": "executable_without_change", "note": "same model and Wald test; small numerical differences in dispersion fitting and independent filtering expected"},
])

# ---------- ownership
m = pd.read_csv(meta["path"], index_col=0)
case.decide("ownership", final={
    "accession": "GSE164890", "matrix_file": "GSE164890_rsem.genes.counts.tsv.gz", "metadata_file": "GSE164890_metadata.csv", "owned": True,
    "checks": {"series_id": sorted(m["series_id"].astype(str).unique().tolist()), "n_gsm": int(len(m)),
               "time_point_counts": m["characteristics_ch1.1.time point"].value_counts().to_dict(),
               "titles": "Skater 1..7 x before/after exercise",
               "paper_design": "7 skaters x before/after = 14 samples (S2.3.p1)",
               "author_repo_counts_file": "data/rsem.genes.counts.tsv.gz in the authors' repo has the same name stem; column names 1after..7before match Conditions.txt"}},
    evidence=[meta, counts, paper, author_cond], paper={"locator": "S2.3.p1"}, confidence="high",
    reasoning="GSE164890 is cited as the paper's deposit; 14 GSMs = 7 skaters x 2 time points, as in S2.3.p1. Matrix columns (1after..7before) equal the GEO description field and the authors' Conditions.txt sample names.")

# ---------- alignment
adir = case.dir / "aligned"; adir.mkdir(parents=True, exist_ok=True)
raw = pd.read_csv(counts["path"], sep="\t", index_col=0)
ann = raw[["Symbol", "Gene_type"]]
ann.to_csv(adir / "gene_annotation.csv")
raw.drop(columns=["Symbol", "Gene_type"]).to_csv(adir / "counts_numeric.csv")
aln = native.align_to_metadata(adir / "counts_numeric.csv", meta["path"], adir, key_column="description")
print({k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")})
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], adir / "design_metadata.csv",
    aliases={"time": "characteristics_ch1.1.time point"},
    patterns={"subject": ("description", r"^(\d)(?:before|after)$")},
    recode={"time": {"before exercise": "pre", "after exercise": "post"},
            "subject": {str(i): f"d{i}" for i in range(1, 8)}})
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)
dm["sex"] = "female"   # paper S2.1.p1: seven female skaters; GEO has no sex column
dm.to_csv(adir / "design_metadata.csv")
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(adir / "design_metadata.csv", "design_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
annot = case.add_output(adir / "gene_annotation.csv", "gene_annotation")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
    "coverage": aln["coverage"], "unmatched": [], "key_column": "description",
    "annotation_columns_removed": ["Symbol", "Gene_type"], "derived_columns": derived,
    "added_columns": {"sex": "female for all samples, from paper S2.1.p1 (GEO metadata has no sex field)"}},
    evidence=[counts, meta, am, amd, amap, paper], paper={"locator": "S2.1.p1"}, confidence="high",
    reasoning="Exact match of matrix columns to GEO 'description'. subject = skater number (d1..d7, as in the authors' Conditions.txt); time pre/post from the time point characteristic.")

# ---------- matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print(json.dumps(prof, default=str)[:1500])
case.decide("matrix", final={"matrix_type": "estimated counts (RSEM expected counts)",
    "recommended_method": "DESeq2 on round(x, 0) counts, rounding documented by the authors",
    "rounding_documented": True,
    "rounding_recipe": "round(exp, 0) in R (round half to even) on the full RSEM gene table before DESeqDataSetFromMatrix (author all_analysis_and_figures.R line 66)",
    "profile": prof,
    "n_genes_non_integer": int((raw.drop(columns=['Symbol', 'Gene_type']) % 1 != 0).any(axis=1).sum()),
    "source": "GEO data_processing: RSEM v1.2.31; 'expression table of raw read counts per gene'; paper S2.4.p1",
    "paper_input": "RSEM per-gene table into DESeq2 (S2.5.p1)"},
    evidence=[am, meta, paper, author_r], paper={"locator": "S2.4.p1"}, confidence="high",
    reasoning="Values are non-negative, mostly integer-valued but with fractional RSEM expected counts in ~5.9k genes; library sums 9.7-35 M match the reported 12-41 M reads with 68-83% assigned. These are estimated counts, not TPM (the TPM table is a separate file). The authors' published script rounds them to integers before DESeq2, which documents the rounding recipe.")

# ---------- design
rep, item, summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["time"],
    matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Human", subject="subject", planned=["time_post_vs_pre"],
    references={"time": "pre"})
print(json.dumps(summary, default=str)[:2500])
comps = [c.get("name") for c in rep.get("comparisons", [])]
print(comps)
json.dump({"comps": comps}, open(case.dir / "_comps.json", "w"))
