"""Gates 1-4 (paper_reconstruction, ownership, alignment, matrix) for GSE283493 / PMID 39832562."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))  # repository root
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID39832562"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC11810837.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC11810837.paper.md"
META = "data/GSE283493/GSE283493_metadata.csv"
SOFT = "data/GSE283493/GSE283493_family.soft.gz"
MAT = "data/GSE283493/GSE283493_Salmon_Gene_table_counts.csv.gz"

CASES = {
    "sat_ea": dict(tissue="SAT", phase="EA", ctrl="EAC", trt="EAE"),
    "sat_la": dict(tissue="SAT", phase="LA", ctrl="LAC", trt="LAE"),
    "vat_ea": dict(tissue="VAT", phase="EA", ctrl="EAC", trt="EAE"),
    "vat_la": dict(tissue="VAT", phase="LA", ctrl="LAC", trt="LAE"),
    "interaction_lrt": dict(tissue="SAT+VAT", phase="EA+LA", ctrl=None, trt=None),
}

run = native.RunRecorder(
    RUN,
    request=("Use the bioinformatics-workflow skill to analyze GSE283493 for the paper 'Timing of exercise "
             "differentially impacts adipose tissue gain in male adolescent rats' (PMID 39832562, PMC11810837). "
             "Determine how exercise affects gene expression as the paper intends."),
    platform_name="claude-code",
    decision_maker="Claude Code subagent (Claude Opus 5.5, claude-opus-5-5[1m])",
    case_ids=list(CASES),
)

# ---------------------------------------------------------------- shared evidence
outlier_rule_threshold = 10
counts = pd.read_csv(MAT, index_col=0)
expressed = (counts > outlier_rule_threshold).sum()
qc_rows = []
for tissue in ("SAT", "VAT"):
    cols = [c for c in counts.columns if c.startswith(tissue)]
    s = expressed[cols]
    med = s.median(); mad = 1.4826 * (s - med).abs().median()
    for c in cols:
        qc_rows.append({"library": c, "tissue": tissue, "n_genes_gt10": int(s[c]),
                        "library_size": int(counts[c].sum()), "robust_z_within_tissue": round((s[c] - med) / mad, 3)})
qc = pd.DataFrame(qc_rows).sort_values(["tissue", "n_genes_gt10"])
qc_path = pathlib.Path(RUN) / "shared_qc_expressed_genes.csv"
qc.to_csv(qc_path, index=False)
OUTLIERS = ["SAT_PM_Exp_d", "SAT_PM_Exp_f", "VAT_AM_Cont_e", "VAT_AM_Exp_c"]

paper_threshold_wald = {
    "metric": "padj", "adjustment": "not_reported (DESeq2 default BH assumed by executor)", "cutoff": 0.1,
    "effect_metric": "log2FC", "effect_estimator": "apeglm-shrunken log2 fold change",
    "effect_cutoff": 0.5, "inclusive": False, "source_locator": "S2.9.p2; S3.p1",
}
paper_threshold_lrt = {
    "metric": "padj", "adjustment": "not_reported", "cutoff": 0.1, "effect_metric": None,
    "effect_cutoff": None, "inclusive": False, "source_locator": "S2.9.p2; FIG1",
}

study_map = {
    "paper_id": "PMID 39832562 / PMC11810837",
    "accessions": ["GSE283493"],
    "accession_locator": "S2.9.p1 (DA.p1 says 'Data will be made available on request')",
    "assay": "bulk polyA RNA-seq, HiSeq2500 50-nt SE, Salmon 1.4.0 to Ensembl rn6 (S2.9.p1, S2.9.p2)",
    "organism": "Rattus norvegicus, male Sprague-Dawley (S2.1.p1)",
    "sample_inclusion": "SAT (inguinal) and VAT (pararenal) from EAC, EAE, LAC, LAE rats, n=6 per group, P61, 24 h after last session (S2.9.p1, S2.5.p1)",
    "sample_exclusion": "4 PCA outliers with a higher number of expressed genes: 2 SAT LAE, 1 VAT EAE, 1 VAT EAC (S2.9.p2); identities given only in Supplementary 4D (SUP8, PDF not available here)",
    "factors": [{"name": "training", "levels": ["control", "exercise"]},
                {"name": "phase", "levels": ["EA (ZT13)", "LA (ZT23)"]},
                {"name": "tissue", "levels": ["SAT", "VAT"]}],
    "primary_estimand": "Effect of forced-wheel exercise (vs handled cage control) on adipose transcriptome, separately by tissue and time of day; plus the phase-by-training interaction",
    "planned_contrasts": [
        {"name": "SAT_EA: EAE vs EAC", "test": "DESeq2 Wald, apeglm shrinkage", "locator": "S2.9.p2"},
        {"name": "SAT_LA: LAE vs LAC", "test": "DESeq2 Wald, apeglm shrinkage", "locator": "S2.9.p2"},
        {"name": "VAT_EA: EAE vs EAC", "test": "DESeq2 Wald, apeglm shrinkage", "locator": "S2.9.p2"},
        {"name": "VAT_LA: LAE vs LAC", "test": "DESeq2 Wald, apeglm shrinkage", "locator": "S2.9.p2"},
        {"name": "phase:training interaction across tissues", "test": "DESeq2 LRT: SVs + Tissue + Phase + Training + Phase:Training vs reduced without interaction", "locator": "S2.9.p2"},
    ],
    "reported_results": {"wald_deg_counts": {"SAT_EA": 7, "SAT_LA": 353, "VAT_EA": 2, "VAT_LA": 14, "locator": "S3.p1"},
                         "lrt_deg_count": {"n": 632, "locator": "S3.p1; FIG1"},
                         "gsea": "fgsea on shrunken log2FC, KEGG; only LAE-LAC enriched (energy, carbohydrate, lipid metabolism), EA none (S3.p1, FIG1 H)",
                         "direction_claims": "LAE up: cholesterol biosynthesis, glycerolipid synthesis, glycolysis, TCA/ETC, NADH shuttle; Cpt1a down in LAE (S3.1.p1-S3.4.p1, FIG2, FIG3)"},
    "repeated_measure_unit": "rat; SAT and VAT come from the same rats (S2.5.p1, S2.9.p1); within one tissue each rat contributes one sample",
    "blocking_or_covariance": {"status": "not_required within a tissue-by-phase Wald contrast; paper adds 2 surrogate variables (sva, top 3000 variable genes) to the models (S2.9.p2)"},
    "matrix_scale": "Salmon gene-level raw counts (S2.9.p2); GEO data_processing: 'Comma separated file with raw gene counts'",
    "paper_method": "DESeq2 (Wald + apeglm; LRT for interaction) with 2 SVs",
    "gene_filter": "genes removed if reads < 10 in fewer than 6 samples (S2.9.p2)",
    "paper_threshold": {"wald": paper_threshold_wald, "lrt": paper_threshold_lrt},
    "enrichment": "harmonic-mean p combination per KEGG pathway + Bonferroni; GSEA (fgsea) on shrunken log2FC with KEGG; Fisher ORA (clusterProfiler) on LRT genes (S2.9.p2)",
}

discrepancies = [
    {"item": "matrix column names vs GEO sample IDs", "paper": "n/a", "data": "matrix columns are library names (e.g. SAT_AM_Cont_a); GEO GSM rows carry them only inside 'description' ('Library name: ...')",
     "disposition": "executable_without_change", "resolution": "derived library_name from description by regex, exact match"},
    {"item": "phase labels", "paper": "EA = ZT13, LA = ZT23", "data": "library names use AM/PM; GEO titles map AM -> 'early active', PM -> 'late active'. ZT13/ZT23 in clock time depends on lights-on time, so AM/PM alone is ambiguous",
     "disposition": "executable_without_change", "resolution": "GEO title mapping used; independently confirmed: the 4 libraries with the most expressed genes are SAT_PM_Exp x2 and VAT_AM_Exp + VAT_AM_Cont, exactly the paper's stated outliers (2 SAT LAE, 1 VAT EAE, 1 VAT EAC) only if PM = late and AM = early"},
    {"item": "outlier identities", "paper": "4 outliers removed, identities in Supplementary 4D only (S2.9.p2)", "data": f"identified by the paper's stated criterion (number of genes > 10 raw counts, Supp 4 A-D): {OUTLIERS}; robust z > 2.9 within tissue, all others < 1.7",
     "disposition": "requires_explicit_deviation", "resolution": "excluded; identity inferred from the stated criterion and group composition, not read from Supplementary 4D"},
    {"item": "surrogate variables", "paper": "2 SVs (sva on top 3000 variable genes) added to every DESeq2 model (S2.9.p2)", "data": "no sva executor in the repository",
     "disposition": "requires_explicit_deviation", "resolution": "Wald contrasts run without SVs as a declared deviation"},
    {"item": "log2FC shrinkage", "paper": "apeglm-shrunken log2FC with |LFC| > 0.5 (S2.9.p2)", "data": "run_deseq2_analysis returns unshrunken MLE log2FC (tools/deseq2_tools.py:136-152, no lfc_shrink)",
     "disposition": "requires_explicit_deviation", "resolution": "paper cutoffs applied to MLE log2FC; counts expected to be >= the paper's because shrinkage reduces |LFC|"},
    {"item": "LRT interaction", "paper": "DESeq2 LRT (full vs reduced) across both tissues (S2.9.p2)", "data": "no DESeq2 LRT executor; SAT and VAT come from the same rats but GEO has no animal ID",
     "disposition": "blocks_reproduction", "resolution": "interaction case stopped (manual_review)"},
    {"item": "Ensembl release", "paper": "Ensembl release 104, rn6 (S2.9.p2)", "data": "GEO data_processing says release-104 and also 'Assembly: rn6 (ensembl release 105)'",
     "disposition": "executable_without_change", "resolution": "noted only"},
    {"item": "data availability", "paper": "DA.p1: 'Data will be made available on request'", "data": "GSE283493 public, PubMed ID 39832562 in SOFT header",
     "disposition": "executable_without_change", "resolution": "noted only"},
]

for cid, spec in CASES.items():
    case = run.case(cid, accession="GSE283493")
    paper = case.add_input(PAPER_JSON, "paper")
    case.add_input(PAPER_MD, "paper")
    meta = case.add_input(META, "metadata")
    soft = case.add_input(SOFT, "metadata")
    mat = case.add_input(MAT, "matrix")
    qc_ev = case.add_output(qc_path, "qc_expressed_genes_per_library")
    case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
    case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")

    if cid == "interaction_lrt":
        planned = [study_map["planned_contrasts"][4]]
        pthr = paper_threshold_lrt
        estimand = "Genes whose exercise response differs between ZT13 and ZT23 (phase:training interaction), modelled across SAT and VAT with tissue as an additive term"
    else:
        planned = [c for c in study_map["planned_contrasts"] if c["name"].startswith(f"{spec['tissue']}_{spec['phase']}")]
        pthr = paper_threshold_wald
        estimand = (f"Effect of exercise in {spec['tissue']} for rats trained in the {spec['phase']} phase: "
                    f"{spec['trt']} vs {spec['ctrl']}")
    case.decide("paper_reconstruction", final={
        "accessions": ["GSE283493"], "primary_estimand": estimand, "planned_contrasts": planned,
        "paper_threshold": pthr, "paper_method": study_map["paper_method"],
        "sample_exclusion": study_map["sample_exclusion"], "gene_filter": study_map["gene_filter"],
        "matrix_scale": study_map["matrix_scale"], "design_note": "2 x 2 x 2 (training x phase x tissue), n=6 rats per group; SAT and VAT from the same rats",
    }, evidence=[paper], paper={"locator": "S2.9.p2"}, confidence="high",
        reasoning=("S2.9.p1 deposits GSE283493 with EAC/EAE/LAC/LAE n=6 each for SAT and VAT. S2.9.p2 defines two DE approaches: "
                   "DESeq2 Wald exercise-vs-control per tissue and phase (padj<0.1 and |shrunken LFC|>0.5, apeglm) and an LRT for "
                   "Phase:Training (padj<0.1), both with 2 SVs, after removing 4 outliers and filtering genes with <10 reads in <6 samples. "
                   "S3.p1 reports 7/353/2/14 Wald DEGs and 632 LRT genes."))

    case.decide("ownership", final={
        "accession": "GSE283493", "matrix_file": MAT, "metadata_file": META, "owned": True,
        "checks": ["SOFT !Series_pubmed_id = 39832562", "series title equals paper title",
                   "48 GSM = 2 tissues x 4 groups x 6 reps, matching S2.9.p1",
                   "matrix 23481 Ensembl rat genes x 48 libraries whose names encode tissue/AM-PM/Cont-Exp/rep",
                   "data_processing: Salmon 1.4.0, raw gene counts, matching S2.9.p2"],
    }, evidence=[meta, soft, mat, paper], paper={"locator": "S2.9.p1"}, confidence="high",
        reasoning="GEO series cites PMID 39832562, has the paper's title, the paper's 4 groups x 2 tissues x n=6, and is the only accession named in Methods (S2.9.p1).")

    # alignment: exact match of matrix columns to the library name recorded in GEO 'description'
    aln_dir = case.dir / "aligned"
    aln_dir.mkdir(parents=True, exist_ok=True)
    keyed = native.derive_columns(META, aln_dir / "metadata_with_library_name.csv",
                                  patterns={"library_name": ("description", r"^Library name: (\S+)$")})
    aln = native.align_to_metadata(MAT, aln_dir / "metadata_with_library_name.csv", aln_dir, key_column="library_name")
    derived = native.derive_columns(
        aln["outputs"]["aligned_metadata"]["path"], aln_dir / "design_metadata.csv",
        aliases={"library": "library_name"},
        patterns={"tissue": ("characteristics_ch1.0.tissue", r"\((SAT|VAT)\)"),
                  "grp": ("characteristics_ch1.2.group", r"\((EAC|EAE|LAC|LAE)\)"),
                  "phase": ("characteristics_ch1.2.group", r"^(early|late) active"),
                  "training": ("characteristics_ch1.2.group", r"(control|exercise)"),
                  "libphase": ("library_name", r"^[SV]AT_(AM|PM)_"),
                  "rep_letter": ("library_name", r"_([a-f])$")},
        recode={"phase": {"early": "EA", "late": "LA"}, "training": {"control": "ctrl", "exercise": "ex"}})
    dm = pd.read_csv(aln_dir / "design_metadata.csv", index_col=0)
    cross = pd.crosstab(dm["libphase"], dm["phase"]).to_dict()
    lib_tissue_ok = bool((dm["library"].str[:3] == dm["tissue"]).all())
    lib_train_ok = bool(((dm["library"].str.contains("_Exp_")) == (dm["training"] == "ex")).all())
    aligned_ev = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
    aligned_meta_ev = case.add_output(aln_dir / "design_metadata.csv", "design_metadata")
    map_ev = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
    case.decide("alignment", final={
        "method": aln["method"] + " (library_name derived from GEO 'description' by regex ^Library name: (\\S+)$)",
        "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
        "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
        "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
        "derived_columns": {"key": keyed["columns"] if "columns" in keyed else keyed, "design": derived},
        "consistency_checks": {"library_prefix_equals_tissue": lib_tissue_ok,
                               "library_Exp_equals_exercise_group": lib_train_ok,
                               "library_AMPM_vs_title_phase": cross},
    }, evidence=[mat, meta, aligned_ev, aligned_meta_ev, map_ev], paper={"locator": "S2.9.p1"}, confidence="high",
        reasoning=("All 48 matrix columns match exactly one GEO 'Library name' (coverage 1.0). Library prefix agrees with the "
                   "tissue characteristic and Cont/Exp agrees with the group characteristic for all 48. AM libraries are "
                   "titled 'early active' and PM 'late active' (one-to-one). Derived formula-safe columns: tissue, grp, phase, training."))

    prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
    prof_ev = case.write_json("matrix_profile.json", prof, role="matrix_profile")
    case.decide("matrix", final={
        "matrix_type": "raw counts", "recommended_method": "DESeq2",
        "provenance": "Salmon 1.4.0 gene-level counts; GEO: 'raw gene counts'; all values integer",
        "profile": {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                          "missing_values", "negative_values", "candidates")},
        "paper_input": "raw counts into DESeq2 (S2.9.p2)",
    }, evidence=[prof_ev, mat, meta, paper], paper={"locator": "S2.9.p2"}, confidence="high",
        reasoning=("integer_fraction 1.0, non-negative, no missing values, max in the hundreds of thousands; file name 'Salmon_Gene_table_counts' "
                   "and GEO processing state raw gene counts; the paper fits DESeq2 on these counts. Salmon output is estimated "
                   "counts summed to genes, but the deposited file is already integer, matching what the authors fed DESeq2."))

print(json.dumps({"qc": qc.tail(4).to_dict("records")}, indent=1))
print("setup done")
