"""Gates 1-4 (paper_reconstruction, ownership, alignment, matrix) for all 19 tissue cases of
GSE243060 / PMID 39232281."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import os, json
from common import *
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
shared = pathlib.Path(RUN) / "shared"
KEYED = shared / "metadata_keyed.csv"
checks = json.loads((shared / "shared_checks.json").read_text(encoding="utf-8"))

run = native.RunRecorder(
    RUN,
    request=("Analyze GSE243060 for PMID 39232281 (Multi-organ transcriptome atlas of a mouse model of relative "
             "energy deficiency in sport): how exercise affects gene expression as the paper intends."),
    platform_name="claude-code",
    decision_maker="Claude Code subagent (Claude Opus 5.5, claude-opus-5-5[1m])",
    case_ids=list(TISSUES),
)

study_map = {
    "paper_id": "PMID 39232281 / PMC11378950",
    "accessions": ["GSE243060"],
    "accession_locator": "S4.1.3.p1, TAB2 (GSE228967 hypothalamus data is reused from an earlier paper, S4.3.16.p1, not analysed here)",
    "assay": "bulk polyA RNA-seq (TruSeq stranded mRNA, NovaSeq PE100), STAR to GRCm38, gene counts (S4.3.11.p1, S4.3.12.p1, TAB1)",
    "organism": "Mus musculus CBA/CaJ, 40 female + 40 male (S4.2.1.p1)",
    "intervention": ("'exercise-for-food': food pellets earned by wheel running. Control (Ctrl) = low workload, ~100 revolutions "
                     "per pellet (ad libitum-like); Deficient = high workload increased daily until weight loss, 3 weeks "
                     "(S4.2.2.p1, S2.1.p1). Both groups run (Ctrl F 14.6, Def F 12.2, Ctrl M 4.7, Def M 8.4 km/day)."),
    "sample_inclusion": "19 tissues collected at ZT5 or ZT17 after 3 weeks; samples with <10 M reads removed; 419 samples passed QC (S4.3.5.p1, S4.3.11.p1)",
    "sample_exclusion": "libraries < 10 M reads (S4.3.11.p1); identities not listed",
    "factors": [{"name": "treatment", "levels": ["Control (low workload)", "Deficient (high workload)"]},
                {"name": "sex", "levels": ["female", "male"]},
                {"name": "zeitgeber time", "levels": ["ZT5", "ZT17"]},
                {"name": "tissue", "levels": list(TISSUES)}],
    "primary_estimand": ("Effect of exercise-linked energy deficiency (high- vs low-workload exercise-for-food) on gene "
                         "expression, per tissue and per sex, irrespective of time of day (S2.3.p1, FIG3, S4.3.13.p1)"),
    "secondary_estimand": "Same contrast at ZT5 and at ZT17 separately (S2.4.p1, Table S5)",
    "planned_contrasts": [
        {"name": "Deficient vs Control within each sex, time-independent", "locator": "S2.3.p1; S4.3.13.p1; FIG3A"},
        {"name": "Deficient vs Control within each sex at ZT5 and at ZT17", "locator": "S2.4.p1; SUP5"},
    ],
    "paper_method": "DESeq2 v1.34.0 per tissue, 'a design that accounted for energy deficiency', then contrasts (sex, energy deficiency, zeitgeber time) (S4.3.13.p1, TAB2)",
    "paper_formula": "not_reported",
    "normalization": "DESeq2 per tissue, females and males together (S4.3.12.p1)",
    "gene_filter": "genes expressed if normalized average count >= 10; ~15,077 expressed per tissue (S4.3.13.p1)",
    "repeated_measure_unit": "mouse; tissues share mice, but within a tissue each mouse gives one sample (no blocking within a tissue)",
    "blocking_or_covariance": {"status": "not_reported / not_required within tissue"},
    "matrix_scale": "raw STAR gene counts deposited (S4.1.3.p1, GEO data_processing)",
    "paper_threshold": PAPER_THRESHOLD,
    "reported_results": {
        "per_tissue_counts_in_text": {f"{t}_{s}": v for (t, s), v in PAPER_COUNTS.items()},
        "unions_in_text": {f"{t}_{s}": v for (t, s), v in PAPER_UNIONS.items()},
        "per_tissue_counts_full": "Figure 3A (image) and Table S2 (Mendeley, not available locally)",
        "direction_claims": ["Oxtr down in 13/18 female tissues (S2.3.p2)", "P4ha1 down in 11/18 female tissues (S2.3.p3)",
                             "Pcif1 up 14/18 female, 1/17 male (S2.3.p5)", "Igf1r up 10/18 female, 3/17 male (S2.3.p5)",
                             "Foxo3 up in all muscles; Loxl2 down in all muscles (S2.6.p3)",
                             "uterus Spp1 log2FC -4.6, Aoc1 -8.0, Cldn8 +4.0, Nr1h4 +4.9 (S2.7.p3)",
                             "male kidney Ace log2FC -2.1, Gc +2.4 (S2.7.p5)"],
    },
    "limitations": "Female controls mostly in estrus, deficient females mostly in diestrus at sacrifice: estrous stage may contribute to uterus/ovary DE genes (S3.1.p1)",
}
discrepancies = [
    {"item": "estimand vs request", "paper": "Deficient vs Control, both groups wheel-running; Deficient run for less food (S2.1.p1)",
     "data": "GEO treatment Control/Deficient; library codes L/H (low/high workload)",
     "disposition": "executable_without_change",
     "resolution": "the exercise question is answered as the paper frames it: exercise-linked energy deficiency vs low-workload exercise; this is not exercise vs sedentary and is reported that way"},
    {"item": "matrix column names", "paper": "n/a",
     "data": f"raw matrix: {checks['raw_column_forms']} column forms (R make.names 'X' prefix on 326 of 419); GEO description gives the library name without prefix",
     "disposition": "executable_without_change", "resolution": "each GEO library name resolved to the single raw column equal to it with or without 'X' (never both); see shared/metadata_keyed.csv"},
    {"item": "sequenced animals", "paper": "80 mice phenotyped (S4.2.1.p1); 419 samples passed QC (S4.3.11.p1)",
     "data": "36 distinct mouse numbers in library names; 3 mice per sex x treatment x ZT cell per tissue; 419 GSM",
     "disposition": "executable_without_change", "resolution": "noted; n=6 per sex x treatment for the time-independent contrast, n=3 per cell for the time-specific one"},
    {"item": "Tibialis anterior tendon", "paper": "samples <10 M reads removed (S4.3.11.p1)", "data": "23 of 24 libraries",
     "disposition": "executable_without_change", "resolution": "the missing cell is reported in the TAt case"},
    {"item": "DESeq2 formula", "paper": "'design that accounted for energy deficiency', then contrasts by sex, energy deficiency, ZT; normalized per tissue with both sexes (S4.3.12.p1, S4.3.13.p1)",
     "data": "formula not reported",
     "disposition": "requires_explicit_deviation",
     "resolution": "per tissue, one DESeq2 model on all samples of the tissue: ~ cell (sex x treatment) for the time-independent contrasts (ZT not modelled: 'irrespective of the time of day', S2.3.p1); ~ cell (sex x treatment x ZT) for the time-specific contrasts"},
    {"item": "expressed-gene filter", "paper": "normalized average gene counts >= 10 (S4.3.13.p1)",
     "data": f"deposited normalized counts equal per-tissue DESeq2 median-of-ratios on raw counts (max relative size-factor difference {checks['normalized_counts']['max_rel_diff']:.1e}); rule gives {checks['expressed_genes_mean_over_tissues']:.0f} expressed genes per tissue on average vs the paper's 15,077",
     "disposition": "executable_without_change", "resolution": "raw counts restricted to genes with mean deposited normalized count >= 10 over the tissue's samples before DESeq2"},
    {"item": "DESeq2 implementation", "paper": "R DESeq2 1.34.0 (TAB2)", "data": "pydeseq2 0.5.4 (tools.joint_contrasts)",
     "disposition": "executable_without_change", "resolution": "noted; small numerical differences expected"},
    {"item": "per-tissue paper counts", "paper": "Figure 3A and Table S2 (Mendeley)", "data": "only uterus, ovary, male kidney and muscle/tendon/all-tissue unions stated in text",
     "disposition": "executable_without_change", "resolution": "compared where stated"},
]

meta_all = pd.read_csv(KEYED, index_col=0)
for cid, tissue in TISSUES.items():
    case = run.case(cid, accession="GSE243060")
    paper = case.add_input(PAPER_JSON, "paper")
    case.add_input(PAPER_MD, "paper")
    meta_ev = case.add_input(META, "metadata")
    soft = case.add_input(SOFT, "metadata")
    raw_ev = case.add_input(RAW, "matrix")
    norm_ev = case.add_input(NORM, "matrix")
    keyed_ev = case.add_output(KEYED, "metadata_keyed_shared")
    chk_ev = case.add_output(shared / "shared_checks.json", "shared_checks")
    case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
    case.write_json("paper_data_discrepancies.json", discrepancies, role="paper_data_discrepancies")

    sub = meta_all[meta_all["characteristics_ch1.1.tissue"] == tissue]
    sexes = sorted(sub["characteristics_ch1.2.Sex"].unique())
    sx = {"female": "F", "male": "M"}
    planned = []
    for s in sexes:
        planned.append({"name": f"{cid} {s}: Deficient vs Control (time-independent)", "locator": "S2.3.p1; FIG3A; S4.3.13.p1",
                        "paper_count": PAPER_COUNTS.get((cid, sx[s]))})
        for z in ("ZT5", "ZT17"):
            planned.append({"name": f"{cid} {s} {z}: Deficient vs Control", "locator": "S2.4.p1; SUP5"})
    case.decide("paper_reconstruction", final={
        "accessions": ["GSE243060"], "tissue": tissue,
        "primary_estimand": (f"{tissue}: effect of exercise-linked energy deficiency (high- vs low-workload exercise-for-food) "
                             "on gene expression within each sex, irrespective of time of day; secondary: the same at ZT5 and ZT17"),
        "planned_contrasts": planned, "paper_threshold": PAPER_THRESHOLD,
        "paper_method": study_map["paper_method"], "paper_formula": "not_reported",
        "gene_filter": study_map["gene_filter"], "normalization": study_map["normalization"],
        "matrix_scale": study_map["matrix_scale"], "sample_exclusion": study_map["sample_exclusion"],
        "estimand_note": "Both groups run on wheels; the contrast is energy deficiency induced by a higher running cost per food pellet, not exercise vs sedentary",
    }, evidence=[paper], paper={"locator": "S4.3.13.p1"}, confidence="high",
        reasoning=("S4.3.13.p1: DESeq2 per tissue, contrasts by sex, energy deficiency and ZT, BH padj < 0.05, expressed = normalized mean >= 10. "
                   "S2.3.p1/FIG3A: the main result is Deficient vs Control per tissue and sex irrespective of time of day; S2.4.p1/Table S5 adds "
                   "ZT5- and ZT17-specific contrasts. S4.1.3.p1 deposits raw and normalized counts as GSE243060."))

    case.decide("ownership", final={
        "accession": "GSE243060", "matrix_file": RAW, "metadata_file": META, "owned": True,
        "checks": ["series_id GSE243060 named in S4.1.3.p1 and TAB2 as this paper's deposit",
                   "contact van Rosmalen, Salk Institute (corresponding author Panda, Salk, S4.1.1.p1)",
                   "419 GSM = 419 samples passing QC (S4.3.11.p1)",
                   "19 tissues = the paper's 19 RNA-seq tissues (TAB1)",
                   "characteristics: CBA/CaJ, sex, Control/Deficient, ZT05/ZT17 match S4.2.1.p1, S4.3.5.p1",
                   "data_processing: STAR v2.7.10a to mm10, DESeq2 v1.34.0 per tissue, matching S4.3.12.p1 and TAB2",
                   f"{tissue}: {len(sub)} samples"],
    }, evidence=[meta_ev, soft, raw_ev, paper], paper={"locator": "S4.1.3.p1"}, confidence="high",
        reasoning="The paper names GSE243060 as its own deposit of raw and normalized counts; GEO sample counts, tissues, factors and processing match the Methods.")

    aln_dir = case.dir / "aligned"
    aln_dir.mkdir(parents=True, exist_ok=True)
    sub_path = aln_dir / "metadata_tissue_keyed.csv"
    sub.to_csv(sub_path)
    aln = native.align_to_metadata(RAW, sub_path, aln_dir, key_column="raw_matrix_column")
    derived = native.derive_columns(
        aln["outputs"]["aligned_metadata"]["path"], aln_dir / "design_metadata.csv",
        aliases={"sex": "characteristics_ch1.2.Sex", "trt": "characteristics_ch1.3.treatment",
                 "zt": "characteristics_ch1.4.zeitgeber time", "mouse": "lib_mouse", "libstyle": "lib_name_style"},
        recode={"sex": {"female": "F", "male": "M"}, "trt": {"Control": "ctrl", "Deficient": "def"},
                "zt": {"ZT05": "zt05", "ZT17": "zt17"}})
    dm = pd.read_csv(aln_dir / "design_metadata.csv", index_col=0)
    wl_ok = bool(((dm["lib_workload"] == "H") == (dm["trt"] == "def")).all())
    sex_ok = bool((dm["lib_sex"] == dm["sex"]).all())
    zt_ok = bool((dm["lib_zt"].astype(int).isin([4, 5]) == (dm["zt"] == "zt05")).all())
    aligned_ev = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
    design_ev = case.add_output(aln_dir / "design_metadata.csv", "design_metadata")
    map_ev = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
    cells = dm.groupby(["sex", "trt", "zt"]).size().to_dict()
    case.decide("alignment", final={
        "method": aln["method"] + " (raw_matrix_column = GEO library name from 'description', with or without the R 'X' prefix, exact)",
        "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
        "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
        "n_matrix_columns_of_other_tissues": len(aln["unmatched_matrix_columns"]),
        "annotation_columns_dropped": aln["annotation_columns_dropped"],
        "derived_columns": derived,
        "consistency_checks": {"library_workload_code_equals_treatment": wl_ok, "library_sex_equals_sex": sex_ok,
                               "library_zt_equals_zt": zt_ok, "one_sample_per_mouse": bool(dm["mouse"].is_unique)},
        "cells_sex_trt_zt": {"/".join(k): int(v) for k, v in cells.items()},
    }, evidence=[raw_ev, meta_ev, keyed_ev, aligned_ev, design_ev, map_ev], paper={"locator": "S4.3.5.p1"}, confidence="high",
        reasoning=(f"All {aln['n_aligned']} {tissue} GSM samples match one raw-matrix column exactly (coverage {aln['coverage']}). "
                   "Library codes (sex, L/H workload, ZT) agree with the GEO characteristics for every sample; each mouse gives one "
                   "sample in this tissue. Derived formula-safe columns: sex (F/M), trt (ctrl/def), zt (zt05/zt17), mouse, libstyle."))

    prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
    prof_ev = case.write_json("matrix_profile.json", prof, role="matrix_profile")
    case.decide("matrix", final={
        "matrix_type": "raw counts", "recommended_method": "DESeq2",
        "provenance": "STAR v2.7.10a gene counts (GEO data_processing: 'csv file includes raw counts for each sample'; file name raw_counts)",
        "profile": {k: prof.get(k) for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                              "missing_values", "negative_values", "candidates")},
        "paper_input": "raw counts into DESeq2, normalized per tissue (S4.3.12.p1, S4.3.13.p1)",
        "normalized_file_check": checks["normalized_counts"],
    }, evidence=[prof_ev, raw_ev, norm_ev, chk_ev, meta_ev, paper], paper={"locator": "S4.3.12.p1"}, confidence="high",
        reasoning=("All values are non-negative integers with no missing values; GEO and the paper call the file raw STAR counts; "
                   "the companion normalized file equals these counts divided by per-tissue median-of-ratios size factors, "
                   "which confirms they are the counts the authors gave DESeq2."))
    print(cid, aln["n_aligned"], aln["coverage"], wl_ok, sex_ok, zt_ok, prof.get("integer_fraction"), cells, flush=True)
print("gates 1-4 done")
