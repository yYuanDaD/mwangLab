"""Gates 1-4 (paper_reconstruction, ownership, alignment, matrix) and a first suitability pass."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os, json, math
import pandas as pd
from tools import native

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40295575"
REQUEST = ("Analyze GSE283250 for PMID 40295575 (Differential behavior responses and genetic alteration underpinning "
           "exercise effectiveness in stress-susceptible mice): how exercise affects gene expression as the paper intends.")
CASE = "GSE283250"
run = native.RunRecorder(RUN, request=REQUEST, platform_name="claude-code",
                         decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=[CASE])
case = run.case(CASE, accession="GSE283250")

P = "test/experiments/paper_screen_20261019/papers/"
META = "data/GSE283250/GSE283250_metadata.csv"
TAR = "data/GSE283250/GSE283250_RAW.tar"
MERGED = RUN + "/GSE283250_merge/GSE283250_counts_by_transcript.csv"
paper = case.add_input(P + "PMC12038050.paper.json", "paper")
paper_md = case.add_input(P + "PMC12038050.paper.md", "paper")
meta = case.add_input(META, "metadata")
tar = case.add_input(TAR, "matrix")
merged = case.add_output(MERGED, "merged_matrix")
merge_log = case.add_output(RUN + "/GSE283250_merge/merge_log.json", "merge_log")
symmap = case.add_output(RUN + "/GSE283250_merge/transcript_to_symbol.csv", "transcript_to_symbol")

# ---------------- 1. paper_reconstruction
FC = 1.3
PT = {"metric": "pvalue", "adjustment": "none", "cutoff": 0.05, "effect_metric": "log2FC",
      "effect_cutoff": math.log2(FC), "effect_cutoff_original": "fold change 1.3 (|FC| >= 1.3)",
      "inclusive": False, "test": "unpaired two-tailed Student's t-test per gene (ExDEGA)",
      "source_locator": "S4.11.p2; S2.3.p1; FIG3",
      "note": "paper wording 'cutoff of 1.3 x fold change (p < 0.05)'; p is strict; whether FC = 1.3 itself counts is "
              "not stated - applied as strict (> log2 1.3); no multiple-testing correction"}
CONTRASTS = [
    {"name": "grp_SS_vs_CON", "label": "Con versus SS (stress effect; not exercise)", "treatment": "SS", "control": "CON",
     "paper_n_deg": {"total": 2305, "up": 1301, "down": 1004, "locator": "S2.3.p1"}, "role": "planned (stress)"},
    {"name": "grp_SES_vs_SS", "label": "SS versus SES (exercise effect in effective responders)", "treatment": "SES", "control": "SS",
     "paper_n_deg": "not_reported (volcano FIG3c only)", "role": "planned (exercise)"},
    {"name": "grp_SER_vs_SES", "label": "SES versus SER (ineffective vs effective responders)", "treatment": "SER", "control": "SES",
     "paper_n_deg": "not_reported (volcano FIG3d only)", "role": "planned (responder)"},
]
recon = {
    "paper_id": "PMID40295575 / PMC12038050",
    "accessions": ["GSE283250"],
    "assay": "bulk poly(A) mRNA-seq, NEBNext Ultra II Directional, NovaSeq 6000 PE100, TopHat/mm10, cufflinks read counts, "
             "cuffdiff FPKM with geometric normalization (S4.11.p1-p2)",
    "tissue": "ventral hippocampus (vHPC), male C57BL/6J (S4.1.p1, S2.3.p1)",
    "sample_inclusion": ["n = 3 animals per group for CON, SS, SES, SER (FIG3 legend; S2.2.p3: 3 mice from each of SES and SER "
                         "meeting stringent criteria; S4.11.p3: 4 groups x 3 replicates)"],
    "sample_exclusion": ["SR (stress-resilient) mice and SS sedentary-vs-VWR remaining animals were not sequenced (S2.2.p3)"],
    "factors": [{"name": "group", "levels": ["CON (naive, no stress, sedentary)", "SS (stress-susceptible, sedentary)",
                                              "SES (SS + 4-wk VWR, effective responder)", "SER (SS + 4-wk VWR, ineffective responder)"],
                 "locator": "S4.11.p2; FIG3"}],
    "responder_definition": "SES/SER assigned post hoc from behaviour (>= 4 favourable of 10 behaviour matrices, k-means) (S2.2.p3, S4.3.p2)",
    "primary_estimand": ("Effect of 4-week voluntary wheel running on the vHPC transcriptome of stress-susceptible mice, split "
                         "by behavioural response: SES vs SS (effective exercise response) and SER vs SES (ineffective vs "
                         "effective); Con vs SS gives the stress signature the exercise is meant to reverse"),
    "planned_contrasts": [c["name"] for c in CONTRASTS],
    "planned_contrast_labels": {c["name"]: c["label"] for c in CONTRASTS},
    "blocking_or_covariance": {"status": "not_required", "reason": "independent animals, one sample per animal; no batch reported"},
    "matrix_scale": "FPKM (cuffdiff geometric normalization) used for testing; read counts deposited (S4.11.p2, GEO data_processing)",
    "paper_method": "unpaired two-tailed Student's t-test per gene on normalized FPKM (ExDEGA), separate 2-group comparisons",
    "paper_threshold": PT,
    "paper_reported_deg_counts": {c["name"]: c["paper_n_deg"] for c in CONTRASTS},
    "paper_total_features": {"value": 33299, "locator": "S2.3.p1"},
    "paper_enrichment": {"ORA": "iDEP k-means clustering of DEGs + GO BP (S4.11.p3)",
                         "GSEA": "Broad GSEA, MSigDB M5 (GO), gene-set permutation x1000, FDR < 25% (S4.11.p4)"},
    "label_renaming": "GEO libraries: C=CON, RS=SS, RES=SES, RER=SER (S4.11.p2)",
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE283250"], "primary_estimand": recon["primary_estimand"],
                   "planned_contrasts": recon["planned_contrasts"], "paper_threshold": PT,
                   "paper_method": recon["paper_method"], "assay": recon["assay"], "matrix_scale": recon["matrix_scale"],
                   "paper_reported_n_deg": recon["paper_reported_deg_counts"]},
            evidence=[paper, paper_md], paper={"locator": "S4.11.p2; S2.2.p3; S2.3.p1; FIG3; S4.11.p4"}, confidence="high",
            reasoning=("Methods S4.11.p2: TopHat/cufflinks, FPKM by cuffdiff geometric normalization, ExDEGA unpaired Student's "
                       "t-test, cutoff FC 1.3 and p < 0.05, GSE283250. FIG3 legend lists the three comparisons Con vs SS, "
                       "SS vs SES, SES vs SER with n = 3 per group. The exercise question is answered by SES vs SS (and, as an "
                       "exploratory complement, SER vs SS); SES vs SER contrasts responders. Only Con vs SS has a DEG count in "
                       "the text (2305: 1301 up, 1004 down)."))

# ---------------- 2. ownership
case.decide("ownership",
            final={"accession": "GSE283250", "matrix_file": TAR, "metadata_file": META, "owned": True,
                   "matrix_used": MERGED,
                   "checks": {"series_id": "GSE283250 in metadata series_id; S4.11.p2 and DA.p1 name GSE283250",
                              "samples": "12 GSMs, ventral hippocampus, male C57BL/6J WT; libraries C2/C8/C12, RS18/19/21, "
                                         "RES9/10/12, RER6/19/20 = CON/SS/SES/SER x 3 (paper renaming S4.11.p2)",
                              "protocol": "TopHat mm10, cufflinks, NovaSeq 6000, NEBNext Ultra II Directional - matches S4.11.p1-p2",
                              "contact": "Dong-Joo Hwang, Korea National Sport University (first author, S4.1.p1 institution)",
                              "rows": "33,299 transcript rows per sample = paper's '33,299 genes annotated' (S2.3.p1)"},
                   "discrepancy": "GEO titles say 'Voluntary wheel running 14d'; paper says 4-week VWR (S2.1.p2, S4.4.p1)"},
            evidence=[meta, tar, merged, merge_log, paper], paper={"locator": "S4.11.p2; DA.p1"}, confidence="high",
            reasoning=("Series ID, contact, tissue, strain, sex, pipeline, group labels and 3 per group all match the paper. "
                       "The tar holds 12 per-sample tables (Gene symbol, Transcript ID, count). They were merged on the unique "
                       "RefSeq Transcript ID by scripts/s02_merge.py (no value changed); the repository tar merger keys on the "
                       "first column (symbol) and would drop 10,116 duplicate-symbol rows."))

# ---------------- 3. alignment
aligned_dir = case.dir / "aligned"
aln = native.align_to_metadata(MERGED, META, aligned_dir)
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
amd = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], aligned_dir / "design_metadata.csv",
                                patterns={"grp": ("description", r"^Library name: ([A-Z]+)\d+$"),
                                          "lib": ("description", r"^Library name: ([A-Z]+\d+)$")},
                                recode={"grp": {"C": "CON", "RS": "SS", "RES": "SES", "RER": "SER"}})
dm = case.add_output(derived["output"], "design_metadata")
dmeta = pd.read_csv(derived["output"], index_col=0)
# cross-check against title / characteristics
chk = pd.DataFrame({"grp": dmeta["grp"], "title": dmeta["title"], "treatment": dmeta["characteristics_ch1.2.treatment"]})
expect = {"CON": (None, "nan"), "SS": ("Restraint stress 14d(Stress-susceptible", "Restraint stress"),
          "SES": ("(Effective response to VWR)", "Restraint stress & Voluntary wheel running"),
          "SER": ("(Ineffective response to VWR)", "Restraint stress & Voluntary wheel running")}
for s, r in chk.iterrows():
    frag, trt = expect[r.grp]
    assert str(r.treatment) == trt, (s, r.treatment)
    if frag:
        assert frag in r.title, (s, r.title)
    else:
        assert "," not in r.title, (s, r.title)
case.decide("alignment",
            final={"method": aln["method"], "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"],
                   "coverage": aln["coverage"], "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                   "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                   "derived_columns": derived["columns"], "levels": derived["levels"],
                   "cross_check": "grp agrees with characteristics treatment and title for all 12 samples"},
            evidence=[merged, meta, am, amd, amap, dm], paper={"locator": "S4.11.p2"}, confidence="high",
            reasoning=("The merge named each column by the GSM prefix of its tar member, so alignment is exact on the metadata "
                       "index (12/12). grp is extracted from the GEO library name and recoded with the paper's own renaming "
                       "(C=CON, RS=SS, RES=SES, RER=SER, S4.11.p2), then cross-checked against title and treatment."))

# ---------------- 4. matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
prof_item = case.write_json("matrix_profile.json", prof, role="matrix_profile")
fid = native.feature_id_report(aln["outputs"]["aligned_matrix"]["path"])
fid_item = case.write_json("feature_id_report.json", fid, role="feature_id_report")
case.decide("matrix",
            final={"matrix_type": "estimated counts (cufflinks transcript-level read counts, deposited as integers; rounding not documented)",
                   "recommended_method": "limma on log2(CPM+1)",
                   "integer_fraction": prof.get("integer_fraction"), "min": prof.get("min"), "max": prof.get("max"),
                   "missing_values": prof.get("missing_values"), "feature_level": "RefSeq transcript (NM_/NR_), 33,299 rows, 23,183 symbols",
                   "library_sizes": "9.3-15.7 M per sample",
                   "paper_input": "cuffdiff geometric-normalized FPKM (not deposited)", "rounding_documented": False},
            candidates=[{"value": "raw counts -> DESeq2", "reason_rejected": "counts come from cufflinks (EM-estimated per-isoform fragment counts); "
                                                                          "the integer rounding is not documented, so integer-only count models are not justified"},
                        {"value": "FPKM", "reason_rejected": "values are integers summing to 9-16 M per sample; GEO says 'Read count values'"}],
            evidence=[am, prof_item, fid_item, meta, merge_log, paper], paper={"locator": "S4.11.p2"}, confidence="medium",
            reasoning=("Non-negative integers, library totals 9-16 M, rows are RefSeq transcripts (isoforms of one gene carry "
                       "different counts). GEO data_processing: 'FPKM calculation using Cufflink ... Read count values'. Paper: "
                       "'read counts were calculated using cufflinks'. Cufflinks counts are EM estimates over isoforms, so this "
                       "is treated as estimated counts. Route: log2(CPM+1) then limma, which needs no integer model."))
print(json.dumps(prof, indent=1, default=str)[:1500])
print(json.dumps(fid, indent=1, default=str)[:800])
