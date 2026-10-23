import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID34943951"
run = native.RunRecorder.open(RUN); case = run.case("GSE188236")
P = "test/experiments/paper_screen_20261019/papers/"
paper = case.add_input(P + "PMC8700369.paper.md", "paper")
paperj = case.add_input(P + "PMC8700369.paper.json", "paper")
meta = case.add_input("data/GSE188236/GSE188236_metadata.csv", "metadata")
tar = case.add_input("data/GSE188236/GSE188236_RAW.tar", "matrix")
merged = case.add_input("data/GSE188236/GSE188236_merged_from_tar.csv", "matrix")

# ---------- paper_reconstruction
paper_threshold = {"metric": "pvalue", "adjustment": "none", "cutoff": 0.05, "effect_metric": "fold_change",
                   "effect_cutoff": 0.3785116, "effect_cutoff_original": "FC > |1.3| (log2(1.3)=0.3785116)",
                   "inclusive": False, "source_locator": "S3.1.p1",
                   "applies_to": "GSE188236 long-RNA TGF-beta1 vs vehicle (in vitro), not to exercise"}
study_map = {
    "paper_id": "PMID34943951 / PMC8700369 / doi:10.3390/cells10123443",
    "accessions": ["GSE188236"],
    "other_accessions_in_paper": {"GSE72462": "exercise study 1, Affymetrix HTA 2.0 microarray, pre/post 8-week training muscle biopsies (S2.5.p1)",
                                  "GSE161749": "exercise study 2, Clariom S microarray, pre/post 8-week training muscle biopsies (S2.5.p1)"},
    "assay": "bulk long RNA-seq (SubSeries GSE188234, 15 samples) + small RNA-seq (SubSeries GSE188235, 15 samples) of primary human myotubes in vitro (S2.4.p1)",
    "organism": "Homo sapiens",
    "sample_inclusion": "Primary human myoblasts from n=5 donors, treated 48 h pre-confluence with vehicle, 1 ng/mL TGF-beta1, or TGF-beta1 + 10 uM SB431542, then differentiated 5 d in 2% FBS (S3.1.p1, FIG1)",
    "sample_exclusion": "not_reported",
    "factors": [{"name": "treatment", "levels": ["vehicle control", "TGF-beta1", "TGF-beta1 + SB431542"]},
                {"name": "donor", "levels": "5 donors (implied by n=5 and _1.._5 suffixes; donor identity not in GEO metadata)"}],
    "exercise_factor_in_this_accession": "none: no exercise, training, or responder factor; all 30 samples are cultured cells",
    "primary_estimand": "Effect of TGF-beta1 (and its reversal by ALK4/5/7 inhibition) on long-RNA and miRNA expression in differentiating human myotubes (S3.1.p1). The paper's exercise estimand (training response, low responders vs responders, pre vs post 8-week training) is measured in GSE72462/GSE161749 microarrays and by qPCR, not in GSE188236 (S2.5.p1, S3.3.p1).",
    "planned_contrasts": ["TGF-beta1 vs vehicle control (long RNA; 2066 transcripts)",
                          "TGF-beta1 + SB431542 vs TGF-beta1 (long RNA; 1900 transcripts)",
                          "TGF-beta1 vs vehicle control (small RNA classical; 45 miRNAs)"],
    "exercise_contrasts_in_paper": ["post vs pre 8-week training, LRE vs RE (microarray GSE72462+GSE161749, paired limma) - not in this accession"],
    "repeated_measure_unit": "donor (5 donors x 3 treatments; implied, not stated as a blocking factor)",
    "normalization": "DESeq2 normalization (GEO data_processing); deposited files are DESeq2-normalized counts",
    "paper_method": "not_reported for the RNA-seq contrasts (S2.6.p1 describes limma for the arrays; GEO says DESeq2 normalization)",
    "paper_threshold": paper_threshold,
    "paper_result": {"tgfb_vs_ctrl_long": 2066, "tgfb_sb_vs_tgfb_long": 1900, "overlap_opposite": 1049, "locator": "S3.1.p1"},
}
case.write_json("paper_reconstruction.json", study_map)
case.decide("paper_reconstruction", final=study_map, evidence=[paper, paperj], paper={"locator": "S2.4.p1"}, confidence="high",
    reasoning="Methods S2.4.p1 ties GSE188236 to the in-vitro TGF-beta1 myotube sequencing; S2.5.p1 places the exercise intervention (8-week endurance training, pre/post biopsies) on microarrays deposited as GSE72462 and GSE161749. The only threshold stated for GSE188236 is p<0.05 and FC>|1.3| (S3.1.p1).")

case.write_json("paper_data_discrepancies.json", [
    {"item": "requested estimand (exercise effect) vs accession content", "paper": "exercise data in GSE72462/GSE161749 (microarray)",
     "data": "GSE188236 = in-vitro TGF-beta1 treatment of cultured myotubes, no exercise factor", "disposition": "blocks_reproduction"},
    {"item": "matrix scale", "paper": "STAR + DESeq2 (S2.4.p1, GEO data_processing)", "data": "per-sample files are DESeq2-normalized counts, not raw counts",
     "disposition": "requires_explicit_deviation"},
    {"item": "Data Availability Statement", "paper": "available on request (DA.p1)", "data": "GEO deposit exists (S2.4.p1)", "disposition": "executable_without_change"},
])

# ---------- ownership
m = pd.read_csv(meta["path"], index_col=0)
long_ids = m.index[m["library_strategy"] == "RNA-Seq"].tolist()
small_ids = m.index[m["library_strategy"] == "ncRNA-Seq"].tolist()
case.decide("ownership", final={
    "accession": "GSE188236", "matrix_file": "GSE188236_merged_from_tar.csv (merged from GSE188236_RAW.tar), long-RNA subset (SubSeries GSE188234, 15 GSMs)",
    "metadata_file": "GSE188236_metadata.csv", "owned": True,
    "checks": {"series_id": sorted(m["series_id"].unique().tolist()), "n_gsm": int(len(m)),
               "library_strategy": m["library_strategy"].value_counts().to_dict(),
               "treatment_counts": m["characteristics_ch1.1.treatment"].value_counts().to_dict(),
               "paper_design": "n=5 donors x {vehicle, TGF-beta1, TGF-beta1+SB431542}, long + small RNA (S3.1.p1, FIG1)"},
    "note": "Files belong to the paper, but to its in-vitro arm, not to its exercise arm.",
}, evidence=[meta, tar, merged, paper], paper={"locator": "S2.4.p1"}, confidence="high",
   reasoning="Series GSE188236 (SuperSeries of GSE188234 long RNA and GSE188235 small RNA) is cited in S2.4.p1; 30 GSMs = 2 assays x 3 treatments x 5 replicates, matching FIG1 (n=5).")

# ---------- alignment (long-RNA subset; the tar merge mixed both assays and filled gaps with 0)
mx = native.read_table(merged["path"])
long_cols = [c for c in mx.columns if c.split("_")[0] in set(long_ids)]
lm = mx[long_cols]
versioned = lm.index.astype(str).str.contains(r"\.\d+$")
lm = lm.loc[~versioned]          # drop the small-RNA (versioned ID) rows zero-filled into long samples
adir = case.dir / "aligned"; adir.mkdir(parents=True, exist_ok=True)
lm.to_csv(adir / "long_rna_matrix_from_tar.csv")
m.loc[long_ids].to_csv(adir / "long_rna_metadata.csv")
d0 = native.derive_columns(adir / "long_rna_metadata.csv", adir / "meta_with_key.csv",
        patterns={"tarcol": ("supplementary_file_1", r"/(GSM\d+_[^/]+)\.txt\.gz$")})
aln = native.align_to_metadata(adir / "long_rna_matrix_from_tar.csv", adir / "meta_with_key.csv", adir, key_column="tarcol")
print({k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")})
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], adir / "design_metadata.csv",
    aliases={"trt": "characteristics_ch1.1.treatment"},
    patterns={"rep": ("tarcol", r"_(\d)$")},
    recode={"trt": {"Control": "ctrl", "TGF-beta1": "tgfb", "TGF-beta1 + SB431542": "tgfbsb", "TGF-beta1 + SB431542 inhibitor": "tgfbsb"}})
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(adir / "design_metadata.csv", "design_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
case.decide("alignment", final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
    "coverage": aln["coverage"], "unmatched": [], "subset": "long RNA (library_strategy RNA-Seq, 15 GSMs); small-RNA GSMs (15) not used",
    "rows_dropped": {"versioned_small_rna_ids_zero_filled_by_merge": int(versioned.sum())},
    "key_derivation": d0, "derived_columns": derived},
    evidence=[merged, meta, am, amd, amap], confidence="high",
    reasoning="Tar member names match the file name in GEO supplementary_file_1 exactly (regex key 'tarcol'). The merged tar matrix mixed long-RNA and small-RNA files and zero-filled non-shared rows, so the long-RNA columns and unversioned Ensembl rows were kept. trt recoded; rep = replicate/donor index 1-5 (donor identity is implied, not stated).")

# ---------- matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print(json.dumps(prof, default=str)[:1500])
case.decide("matrix", final={"matrix_type": "normalized counts (DESeq2 size-factor normalized; not raw counts)",
    "recommended_method": "none for exercise (no exercise contrast); for the in-vitro contrast, limma on log2(x+1) as a declared deviation, since DESeq2 needs raw counts",
    "profile": prof, "source": "GEO data_processing: Normalization was done using DESeq2 v1.32.0; Tab-delimited text files with normalized counts for each sample",
    "paper_input": "STAR + DESeq2 (S2.4.p1)"},
    evidence=[am, meta, paper], paper={"locator": "S2.4.p1"}, confidence="medium",
    reasoning="GEO data_processing states the per-sample files hold DESeq2-normalized counts. Integer-looking values do not make them raw counts; count methods on them would treat normalized values as library counts.")

# ---------- design: suitability, then refusal
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)
# matrix_csv omitted: tools/suitability.py:367 check_sex raises IndexError when metadata has no sex column
rep, item, summary = case.suitability(matrix_type="normalized counts", metadata=dm, factors=["trt"],
    organism="Human", subject=None, planned=[])
summary = dict(summary, sex_check="skipped: check_sex crashes without a metadata sex column (tools/suitability.py:367); cultured cells from 5 donors, sex not reported")
print(json.dumps(summary, default=str)[:2500])
comps = [c.get("name") for c in rep.get("comparisons", [])]
print(comps)
case.decide("design", final={"suitability": summary, "available_contrasts": comps},
    evidence=[paper, meta, amd, item], paper={"locator": "S2.5.p1"}, confidence="high",
    candidates=[{"value": "trt: tgfb vs ctrl", "reason_rejected": "TGF-beta1 treatment of cultured myotubes is not exercise; answering the exercise request with it would change the estimand"},
                {"value": "trt: tgfbsb vs tgfb", "reason_rejected": "pharmacological inhibitor contrast, not exercise"},
                {"value": "post vs pre training, LRE vs RE (paper's exercise analysis)", "reason_rejected": "samples are in GSE72462/GSE161749 microarrays, not in GSE188236"}],
    decision_status="refused",
    stop_reason="GSE188236 contains only cultured primary human myotubes treated with vehicle, TGF-beta1, or TGF-beta1+SB431542 (in-vitro arm of the paper, S2.4.p1/S3.1.p1). It has no exercise, training, or responder factor, so it cannot identify how exercise affects gene expression. The paper's exercise analysis (8-week endurance training, pre/post biopsies, responders vs low responders) uses microarrays GSE72462 and GSE161749 (S2.5.p1), outside this request.",
    reasoning="Refused at design: the requested estimand (exercise effect) is not present in the sequenced samples. The in-vitro TGF-beta1 contrasts are analyzable but answer a different question.")
case.write_json("reproduction_plan.json", {"route": "stopped at design (refused)", "reason": "no exercise contrast in GSE188236",
    "possible_follow_up": "analyze GSE72462 + GSE161749 (microarray, paired limma, post vs pre and LRE vs RE) for the exercise question; or run TGF-beta1 vs vehicle on GSE188236 as a separate non-exercise request"})
case.write_json("reproduction_summary.json", {"status": "refused", "gate": "design", "n_deg": None,
    "paper_counts_not_compared": {"tgfb_vs_ctrl_long": 2066, "tgfb_sb_vs_tgfb_long": 1900}})
print(case.finish())
print(run.finish())
