import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/2f2aeb1cc53680f371f7452796ed7c9168968c09"
run = native.RunRecorder.open(RUN); case = run.case("GSE179302")
P = "test/experiments/paper_screen_20261019/papers/"
paper = case.add_input(P + "PMC9722583.paper.md", "paper")
paperj = case.add_input(P + "PMC9722583.paper.json", "paper")
meta = case.add_input("data/GSE179302/GSE179302_metadata.csv", "metadata")
tar = case.add_input("data/GSE179302/GSE179302_RAW.tar", "matrix")
merged = case.add_input("data/GSE179302/GSE179302_merged_from_tar.csv", "matrix")
csvm = case.add_input("data/GSE179302/GSE179302_raw_counts.csv.gz", "matrix")

paper_threshold = {"metric": "padj", "adjustment": "IHW", "cutoff": 0.1, "effect_metric": None,
                   "effect_cutoff": None, "inclusive": False, "source_locator": "S2.5.p1"}
case.decide("paper_reconstruction", final={
    "accessions": ["GSE179302"], "assay": "whole-blood bulk RNA-seq (globin/rRNA depleted, NovaSeq PE146), STAR gene counts, GRCh38",
    "organism": "Homo sapiens",
    "sample_inclusion": "35 RA patients with actigraphy + baseline (pre-COVID) blood RNA-seq (S2.1.p1, S3.p1); tertiles active n=13, intermediate n=14, inactive n=8 (TAB1)",
    "factors": {"activity_tertile": ["inactive (lowest)", "intermediate", "active (highest)"],
                "covariates": ["sex", "age", "race", "ethnicity", "1 surrogate variable (sva)"]},
    "primary_estimand": "association of physical activity with whole-blood gene expression: highest vs lowest tertile of % time in >=moderate activity, adjusted for sex, age, race, ethnicity (+1 SV); cross-sectional/associational",
    "estimand_type": "associational",
    "planned_contrasts": ["active (highest tertile) vs inactive (lowest tertile)"],
    "sensitivity_contrasts": ["same + RADAI disease activity (674 DEGs)", "same + PROMIS physical function (332 DEGs)"],
    "repeated_measure_unit": "none (one baseline blood sample per patient)",
    "normalization": "DESeq2 median-of-ratios; filter genes expressed in <30% of patients in each group; 19,260 genes kept (S2.4.p1)",
    "method": "DESeq2 ~ sex + age + race + ethnicity + SV1; IHW multiple testing (S2.5.p1)",
    "paper_threshold": paper_threshold,
    "paper_result": {"n_deg": 767, "up_in_active": 365, "down_in_active": 402, "locator": ["S3.p3", "FIG1"]},
    "enrichment_in_paper": "IPA (canonical pathways, upstream regulators) on DEGs; not reproducible here (proprietary) (S2.6.p1)",
}, evidence=[paper, paperj], paper={"locator": "S2.5.p1"}, confidence="high",
   reasoning="Abstract, methods S2.2.1/S2.4/S2.5, results S3.p3 and FIG1 define a cross-sectional highest-vs-lowest activity tertile DESeq2 comparison with demographic covariates and IHW padj<0.1. Sensitivity models need RADAI and PROMIS, which GEO does not deposit.")

m = pd.read_csv(meta["path"], index_col=0)
tcol = "characteristics_ch1.1.activity_moderate_tertile"
case.decide("ownership", final={
    "accession": "GSE179302", "matrix_file": "GSE179302_merged_from_tar.csv (merged from GSE179302_RAW.tar, 35 per-GSM STAR reads_per_gene tables)",
    "metadata_file": "GSE179302_metadata.csv", "owned": True,
    "checks": {"series_id": sorted(m.series_id.unique().tolist()), "n_gsm": int(len(m)), "tertile_counts": m[tcol].value_counts().to_dict(),
               "paper_counts": {"active": 13, "intermediate": 14, "inactive": 8},
               "age_mean_by_tertile": m.groupby(tcol)["characteristics_ch1.2.age"].mean().round(1).to_dict(),
               "paper_age_means": {"active": 50, "intermediate": 56, "inactive": 63}},
    "rejected_file": "GSE179302_raw_counts.csv.gz: 88 columns RAZZ_<id>_P1/P2/P3 (38 subjects, longitudinal parent-cohort visits); only 35 of its subjects are GEO GSM samples and the paper uses one baseline sample per patient. The per-GSM tar files are linked to the metadata by supplementary_file_1, so they were used.",
}, evidence=[meta, tar, merged, csvm, paper], paper={"locator": "S2.9.p1"}, confidence="high",
   reasoning="Metadata series_id GSE179302 (cited in S2.9.p1); 35 GSMs with tertile counts 13/14/8 and age means 49.7/55.9/62.9 match TAB1 active/intermediate/inactive. tertile 'three'=active, 'one'=inactive.")

# alignment: tar columns are GSM<id>_<library>_reads_per_gene.star; derive the key from supplementary_file_1
d0 = native.derive_columns(meta["path"], case.dir / "aligned" / "meta_with_key.csv",
        patterns={"tarcol": ("supplementary_file_1", r"/(GSM\d+_[^/]+_reads_per_gene\.star)\.tab\.gz$")})
aln = native.align_to_metadata(merged["path"], case.dir / "aligned" / "meta_with_key.csv", case.dir / "aligned", key_column="tarcol")
print({k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")})
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"tert": tcol, "sex": "characteristics_ch1.3.Sex", "age": "characteristics_ch1.2.age",
             "race": "characteristics_ch1.4.race", "hisp": "characteristics_ch1.5.hispanic"},
    recode={"tert": {"one": "inactive", "two": "intermediate", "three": "active"}})
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(case.dir / "aligned" / "design_metadata.csv", "design_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
    "coverage": aln["coverage"], "unmatched": [], "key_derivation": d0, "derived_columns": derived},
    evidence=[merged, meta, am, amd, amap], confidence="high",
    reasoning="Exact match of tar member names to the file name in GEO supplementary_file_1 (regex-derived key 'tarcol'); formula-safe columns tert/sex/age/race/hisp derived and recoded (one=inactive, three=active per TAB1 counts).")

prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print(json.dumps(prof, default=str)[:1200])
case.decide("matrix", final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
    "profile": prof, "source": "STAR ReadsPerGene unstranded column (merge_raw_tar chose unstranded: forward/reverse ratio 1.02)",
    "paper_input": "STAR gene counts, DESeq2 median-of-ratios (S2.4.p1)",
    "notes": "60,590 Gencode gene IDs incl. 92 ERCC spike-ins; library sizes 3.2e6-2.7e7 assigned reads"},
    evidence=[am, meta, paper], paper={"locator": "S2.4.p1"}, confidence="high",
    reasoning="All values non-negative integers from STAR ReadsPerGene; matches paper's STAR gene counts input.")
