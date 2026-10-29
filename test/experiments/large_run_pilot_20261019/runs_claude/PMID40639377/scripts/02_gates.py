import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import numpy as np, pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40639377"
run = native.RunRecorder.open(RUN); case = run.case("GSE294230")
P = "test/experiments/paper_screen_20261019/papers/"
paper = case.add_input(P + "PMC12258965.paper.md", "paper")
paperj = case.add_input(P + "PMC12258965.paper.json", "paper")
meta = case.add_input("data/GSE294230/GSE294230_metadata.csv", "metadata")
mat = case.add_input("data/GSE294230/GSE294230_txi_counts_SP230_gene_name.csv.gz", "matrix")

# ---------- paper_reconstruction
paper_threshold = {"metric": "qvalue", "adjustment": "BH", "cutoff": 0.2, "effect_metric": None,
                   "effect_cutoff": None, "inclusive": False, "source_locator": "S5.2.19.p1",
                   "note": "Sleuth q-value (Benjamini-Hochberg adjusted p) < 0.2, no fold-change cutoff; also used for TFEA input (S5.2.20.p1)"}
study_map = {
    "paper_id": "PMID40639377 / PMC12258965 / doi:10.1016/j.cell.2025.06.018",
    "accessions": ["GSE294230"],
    "other_accessions_in_paper": {"PRJNA1245478": "16S rRNA-seq (microbiome, not host expression)",
                                  "PRJNA1246250": "metagenomics of cecum contents (not host expression)"},
    "assay": "bulk RNA-seq (polyA) of in-vitro activated naive mouse CD8 T cells (S5.2.18.p1, S5.2.19.p1, FIG6 L-M)",
    "organism": "Mus musculus",
    "sample_inclusion": "WT naive CD8 T cells from spleen + peripheral lymph nodes, activated 18 h aCD3/aCD28 + IL-12, then 24 h vehicle (PBS) or 2 mM formate (S5.2.18.p1); GEO: 4 PBS + 4 formate",
    "sample_exclusion": "not_reported",
    "factors": [{"name": "treatment", "levels": ["PBS (vehicle)", "2 mM formate 24 h"]}],
    "exercise_factor_in_this_accession": "none directly. The exercise experiments (treadmill/voluntary wheel, tumor-bearing mice) were assayed by 16S, metagenomics, metabolomics and flow cytometry, not RNA-seq. The only host transcriptome in the paper tests formate, which the paper identifies as the exercise-induced microbiota metabolite mediating the antitumor CD8 T-cell effect (title, ABS, S2.4, S2.7.p4).",
    "primary_estimand": "Effect of formate (exercise-induced microbiota metabolite) vs vehicle on the transcriptome of activated CD8 T cells in vitro (S2.7.p4, FIG6 L-M, SUP10 Table S3). This is the paper's mechanistic link between exercise and CD8 T-cell Tc1 programming, not a direct exercise-vs-sedentary contrast.",
    "planned_contrasts": ["2 mM formate vs PBS (CD8 T cells, in vitro)"],
    "repeated_measure_unit": "not_reported for RNA-seq. Other in-vitro CD8 experiments used paired t tests with n = 4-5 mice/group (FIG6 F, N-P), suggesting cells from one mouse split across conditions, but the RNA-seq description does not say so.",
    "blocking_or_covariance": {"status": "not_reported"},
    "matrix_scale": "kallisto transcript abundances (S5.2.19.p1); GEO deposit is tximport gene-level estimated counts (txi_counts)",
    "normalization": "Sleuth internal (not reported in detail)",
    "paper_method": "Kallisto + Sleuth, transcript and gene level (S5.2.19.p1); test (Wald/LRT) and model formula not_reported",
    "paper_formula": "not_reported",
    "paper_threshold": paper_threshold,
    "paper_result": {"n_deg": "not_reported in text (Table S3, SUP10, not retrievable: article not open access in Europe PMC, PMC download blocked)",
                     "reported_genes_up_with_formate": ["Shmt2", "Cth", "mt-Nd4", "Tkt", "Ripk2", "Slc39a8", "Furin", "Parp1", "Ezr", "Irf8"],
                     "locator": "S2.7.p4"},
}
case.write_json("paper_reconstruction.json", study_map)
case.decide("paper_reconstruction", final=study_map, evidence=[paper, paperj], paper={"locator": "S5.2.19.p1"}, confidence="high",
    reasoning="S4.3.p1 names GSE294230 as the paper's RNA-seq. S5.2.18.p1/S5.2.19.p1 and FIG6 L-M show it is PBS vs 2 mM formate on activated CD8 T cells, analysed with Kallisto+Sleuth at q<0.2. No exercise-vs-sedentary host transcriptome exists in the paper; the paper's intended use of this RNA-seq is the formate (exercise-derived metabolite) mechanism.")

case.write_json("paper_data_discrepancies.json", [
    {"item": "requested estimand (exercise effect on gene expression) vs accession content",
     "paper": "exercise acts via microbiota-derived formate; RNA-seq tests formate directly on CD8 T cells (S2.7.p4)",
     "data": "GSE294230 = 4 PBS vs 4 formate in vitro, no exercise factor",
     "disposition": "requires_explicit_deviation",
     "note": "Analysed as the paper intends (formate as the exercise mediator); the result is not a direct exercise effect and is reported as such."},
    {"item": "matrix", "paper": "kallisto transcript abundances into Sleuth", "data": "tximport gene-level estimated counts (70% integer), 8884/35072 rows lack gene_name; EnsemblID unique",
     "disposition": "requires_explicit_deviation"},
    {"item": "method", "paper": "Sleuth (transcript-level, bootstrap-aware)", "data": "no Sleuth executor and no kallisto bootstraps deposited",
     "disposition": "requires_explicit_deviation"},
    {"item": "pairing", "paper": "not stated for RNA-seq", "data": "library numbering S1/S2, S7/S8, S10/S11, S13/S14 alternates control/formate; within-pair Spearman correlations are the highest",
     "disposition": "executable_without_change", "note": "unpaired primary (paper states nothing); pair-blocked exploratory sensitivity"},
    {"item": "GEO data_processing", "paper": "kallisto", "data": "GEO says 'raw counts' though the file name says txi_counts and values are fractional", "disposition": "executable_without_change"},
])

# ---------- ownership
m = pd.read_csv(meta["path"], index_col=0)
case.decide("ownership", final={
    "accession": "GSE294230", "matrix_file": "GSE294230_txi_counts_SP230_gene_name.csv.gz", "metadata_file": "GSE294230_metadata.csv",
    "owned": True, "series_id_in_metadata": sorted(m["series_id"].astype(str).unique()),
    "n_samples_geo": int(len(m)), "groups_geo": m["characteristics_ch1.3.treatment"].value_counts().to_dict(),
    "contact": "Tingting Duan, University of Pittsburgh (paper's institution)"},
    evidence=[meta, mat, paper], paper={"locator": "S4.3.p1"}, confidence="high",
    reasoning="Metadata series_id is GSE294230, cited in the paper's data availability (S4.3.p1). 8 CD8 T-cell samples, PBS vs 2 mM formate 24 h, matching S5.2.18.p1; the supplementary file is the series' only matrix and its 8 columns are the library names in GEO 'description'.")

# ---------- alignment
A = case.dir / "aligned"; A.mkdir(parents=True, exist_ok=True)
raw = pd.read_csv(mat["path"])
assert raw["EnsemblID"].is_unique
genes = raw[["EnsemblID", "gene_name"]].set_index("EnsemblID")
genes.to_csv(A / "gene_annotation.csv")
reidx = raw.drop(columns=["gene_name"]).set_index("EnsemblID")
reidx.to_csv(A / "txi_counts_by_ensembl.csv")  # same values, EnsemblID as the row key (gene_name has 8884 blanks)
reidx_item = case.add_output(A / "txi_counts_by_ensembl.csv", "matrix_reindexed")
lib = native.derive_columns(meta["path"], A / "metadata_libid.csv",
                            patterns={"libid": ("description", r"Library name: Sample\d+,(SP230-S\d+_S\d+)$")})
aln = native.align_to_metadata(A / "txi_counts_by_ensembl.csv", A / "metadata_libid.csv", A, key_column="libid")
print(json.dumps({k: v for k, v in aln.items() if k != "outputs"}, indent=1))
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], A / "design_metadata.csv",
                                aliases={"grp": "characteristics_ch1.3.treatment"},
                                patterns={"libnum": ("libid", r"SP230-S(\d+)_S\d+$")},
                                recode={"grp": {"PBS": "pbs", "2 mM formate for 24 hrs": "formate"}})
dm = pd.read_csv(A / "design_metadata.csv", index_col=0)
blk_map = {"1": "b1", "2": "b1", "7": "b2", "8": "b2", "10": "b3", "11": "b3", "13": "b4", "14": "b4"}
dm["blk"] = dm["libnum"].astype(str).map(blk_map)
dm.to_csv(A / "design_metadata.csv")
aligned_m = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
aligned_meta = case.add_output(A / "design_metadata.csv", "design_metadata")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                                "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                                "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                                "row_key": "EnsemblID (unique); gene_name kept in aligned/gene_annotation.csv",
                                "derived_columns": [lib, derived],
                                "putative_block": {"column": "blk", "mapping": "consecutive library numbers (S1,S2)->b1, (S7,S8)->b2, (S10,S11)->b3, (S13,S14)->b4; inferred, not documented",
                                                   "assignments": dm[["libid", "grp", "blk"]].to_dict(orient="index")}},
    evidence=[mat, meta, reidx_item, aligned_m, aligned_meta], confidence="high",
    reasoning="Matrix columns (SP230-S*_S*) equal the second field of GEO 'description'; extracted as libid and matched exactly, 8/8. Short columns grp (pbs/formate) and libnum derived; blk is a putative mouse/pair label from consecutive library numbering, used only in an exploratory sensitivity fit.")

# ---------- matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
x = pd.read_csv(aln["outputs"]["aligned_matrix"]["path"], index_col=0)
frac = x.values[(x.values != np.round(x.values))]
prof["fractional_values_examples"] = [float(v) for v in frac[:5]]
case.write_json("aligned/matrix_profile.json", prof)
case.decide("matrix", final={"matrix_type": "estimated counts", "recommended_method": "DESeq2 on rounded estimated counts (tximport convention)",
                             "profile": {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction", "negative_values", "missing_values", "candidates")},
                             "provenance": "file name 'txi_counts' (tximport), GEO data_processing 'aligned ... using Kallisto', paper S5.2.19.p1 Kallisto",
                             "paper_input": "kallisto transcript abundances into Sleuth"},
    evidence=[aligned_m, meta, paper], paper={"locator": "S5.2.19.p1"}, confidence="high",
    reasoning="Non-negative, max ~6e5, 70% integer with fractional remainder; file name txi_counts and Kallisto quantification identify tximport gene-level estimated counts, not FPKM/TPM and not exact raw counts. Rounding to integers for DESeq2 is the documented tximport/DESeqDataSetFromTximport convention.")

# ---------- design
rep, sitem, summary = case.suitability(matrix_type="raw_counts", metadata=dm, factors=["grp"],
                                       matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Mouse", subject=None,
                                       references={"grp": "pbs"}, planned=["grp_formate_vs_pbs"])
print(json.dumps(summary, indent=1)); print([c.get("name") for c in rep["comparisons"]])
case.decide("design", final={"analysis_type": "two_group", "design_column": "grp", "control": "pbs", "treatment": "formate",
                             "contrasts": ["grp_formate_vs_pbs"],
                             "estimand": "formate (exercise-induced microbiota metabolite) vs vehicle in activated CD8 T cells in vitro; a mechanistic mediator contrast, not a direct exercise effect",
                             "estimand_type": "mediator_in_vitro",
                             "suitability": summary},
    candidates=[{"value": "exercise vs sedentary", "reason_rejected": "no exercise samples were sequenced in GSE294230 or elsewhere in the paper"},
                {"value": "refuse at design (no exercise contrast)", "reason_rejected": "the request asks for the analysis 'as the paper intends'; the paper's only host RNA-seq tests formate as the exercise mediator (title, S2.7.p4), so the paper-defined contrast is run and labelled as a mediator contrast"}],
    evidence=[aligned_meta, sitem, paper], paper={"locator": "S5.2.18.p1"}, confidence="medium",
    reasoning="Single two-level factor, 4 vs 4, planned by the paper (FIG6 L, Table S3). Suitability report analyzable. Matrix type passed to the suitability check as raw_counts because the route is a count route after documented rounding.")

# ---------- covariance
pr = native.pairing_report(dm, "blk", "grp", ["pbs", "formate"])
cf = native.confounding_report(dm, "grp", ["blk", "libnum"])
dc = native.design_check(dm, ["grp"]); dcb = native.design_check(dm, ["blk", "grp"])
case.write_json("aligned/covariance_reports.json", {"pairing_blk": pr, "confounding": cf, "design_grp": dc, "design_blk_grp": dcb})
case.decide("covariance", final={"status": "not_required", "blocking_terms": [],
                                 "covariates": [{"name": "blk", "disposition": "excluded: putative mouse/pair inferred from library numbering only; pairing not documented in GEO or paper; used in an exploratory pair-blocked sensitivity fit"},
                                                {"name": "tissue/cell type/genotype", "disposition": "excluded: single level"}],
                                 "design_check_primary": dc, "design_check_blocked": dcb, "pairing_report_blk": pr},
    evidence=[aligned_meta], paper={"locator": "S5.2.19.p1"}, confidence="medium",
    reasoning="The paper describes the RNA-seq as PBS vs formate with no pairing or covariates (S5.2.19.p1). The only candidate block is inferred from sample numbering; correlation structure supports it but it is not a documented fact, so the primary model is unblocked (conservative if pairs exist) and the blocked model is exploratory.")

# ---------- method
case.decide("method", final={"method": "DESeq2 (pydeseq2) Wald test on rounded tximport estimated counts", "matrix_type": "estimated counts",
                             "formula": "~ grp", "rounding_documented": "np.round of tximport gene-level estimated counts before DESeq2, as DESeqDataSetFromTximport does",
                             "paper_route": {"method": "Kallisto + Sleuth (transcript-level, bootstrap-aware)", "status": "blocked",
                                             "reason": "no Sleuth executor; only gene-level tximport counts were deposited (no kallisto abundance.h5 bootstraps)"}},
    evidence=[aligned_m, paper], paper={"locator": "S5.2.19.p1"}, confidence="high",
    reasoning="Count-based route matching the estimated-count matrix; DESeq2 is the default raw-count method; run as a declared deviation from Sleuth.")

# ---------- threshold
case.decide("threshold", final={"paper_threshold": paper_threshold, "threshold_source": "paper_on_deviation_route",
                                "applied_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.2, "effect_metric": None, "effect_cutoff": None, "inclusive": False},
                                "deviation_note": "Same BH q < 0.2 rule as the paper, applied to DESeq2 Wald p-values instead of Sleuth's test; DESeq2 independent filtering sets padj NA for low-count genes.",
                                "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None, "label": "audit: workflow default BH<0.05"}},
    evidence=[paper], paper={"locator": "S5.2.19.p1"}, confidence="high",
    reasoning="Paper: q (BH) < 0.2, no effect cutoff (S5.2.19.p1, S5.2.20.p1).")
print("gates recorded")
