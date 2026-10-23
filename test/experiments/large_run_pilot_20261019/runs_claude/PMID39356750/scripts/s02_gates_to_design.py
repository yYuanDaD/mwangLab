import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import json, os
import pandas as pd
from tools import native

ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())
os.chdir(ROOT)
native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID39356750"
REQUEST = ("Analyze GSE270400 for PMID 39356750 (Collagen denaturation in post-run Achilles tendons and "
           "Achilles tendinopathy: In vivo mechanophysiology and magnetic resonance imaging): how exercise "
           "affects gene expression as the paper intends.")
run = native.RunRecorder(RUN, request=REQUEST, platform_name="claude-code",
                         decision_maker="Claude Opus 5.5 (claude-opus-5-5[1m]) subagent", case_ids=["GSE270400_12h_vs_NC"])
case = run.case("GSE270400_12h_vs_NC", accession="GSE270400")

paper_json = "test/experiments/paper_screen_20261019/papers/PMC11446262.paper.json"
paper = case.add_input(paper_json, "paper")
paper_md = case.add_input("test/experiments/paper_screen_20261019/papers/PMC11446262.paper.md", "paper")
meta = case.add_input("data/GSE270400/GSE270400_metadata.csv", "metadata")
counts = case.add_input("data/GSE270400/GSE270400_All.count.txt.gz", "matrix")
fpkm = case.add_input("data/GSE270400/GSE270400_Expression.All.fpkm.anno.txt.gz", "matrix")
authdeg = case.add_input("data/GSE270400/GSE270400_DifGene.12hVSNC.All.fpkm.anno.txt.gz", "matrix")

# ---------------- 1. paper_reconstruction
paper_threshold = {"metric": "padj", "adjustment": "BH (FDR)", "cutoff": 0.05,
                   "effect_metric": "log2FC", "effect_cutoff": 1.0, "effect_cutoff_original": "fold change >= 2",
                   "inclusive": True, "source_locator": "S4.6.p1; S2.4.p1; FIG4",
                   "note": "fold change >= 2 (inclusive) and FDR-adjusted P < 0.05; paper counts only protein-coding genes"}
study_map = {
    "paper_id": "PMID39356750 / PMC11446262",
    "accessions": ["GSE270400", "GSE269529"],
    "accession_roles": {
        "GSE270400": "12 h post-run (1 h treadmill) vs naive cage control, rat Achilles tendon; GEO 4 + 4 samples (fig. S16, S2.4.p2)",
        "GSE269529": "0 h post-run vs NC (Fig. 4, S2.4.p1); not part of this request"},
    "assay": "bulk RNA-seq (polyA, Illumina NovaSeq 6000), rat (Rattus norvegicus) Achilles tendon",
    "sample_inclusion": ["right-leg Achilles tendon from male SD rats: naive control (NC) and 12 h post 1-h treadmill run (S4.6.p1, S4.1.1.p1)"],
    "sample_exclusion": "not_reported",
    "factors": [{"name": "exercise_state", "levels": ["NC (cage control)", "12h p.r."]}],
    "primary_estimand": "effect of a single 1-h treadmill run on Achilles tendon gene expression 12 h after running, vs naive cage controls (between-animal)",
    "planned_contrasts": ["12h p.r. vs NC"],
    "blocking_or_covariance": {"status": "not_required", "reason": "independent animals per group; no pairing described"},
    "matrix_scale": "featureCounts read counts (S4.6.p1)",
    "paper_method": "DESeq2 v1.30.1 (R)",
    "paper_formula": "not_reported (two-group design implied)",
    "paper_threshold": paper_threshold,
    "paper_reported_counts": {"12h_vs_NC": {"up": 51, "down": 42, "total": 93, "scope": "protein-coding genes", "locator": "S2.4.p2"},
                              "0h_vs_NC (GSE269529, not this case)": {"up": 358, "down": 281, "scope": "protein-coding genes", "locator": "S2.4.p1"}},
    "group_size_note": "Methods state n = 6 per group for the one-time running study (S4.1.1.p1); RNA-seq n per group not stated in paper; GEO has 4 per group.",
}
case.write_json("paper_reconstruction.json", study_map, role="paper_reconstruction")
case.decide("paper_reconstruction",
            final={"accessions": ["GSE270400"], "primary_estimand": study_map["primary_estimand"],
                   "planned_contrasts": ["12h p.r. vs NC (cage control)"], "paper_threshold": paper_threshold,
                   "paper_method": "DESeq2 v1.30.1 on featureCounts counts", "assay": study_map["assay"],
                   "blocking": "not_required", "paper_reported_n_deg": {"up": 51, "down": 42, "total": 93, "scope": "protein-coding"},
                   "related_accessions": {"GSE269529": "0 h p.r. vs NC (Fig. 4), out of scope for this request"}},
            evidence=[paper, paper_md], paper={"locator": "S2.4.p2; S4.6.p1; S4.1.1.p1; S5.4.p1"},
            reasoning=("The paper deposits two RNA-seq series (S5.4.p1). GSE270400's GEO records describe the 12 h post-run "
                       "vs control experiment, which the paper reports in S2.4.p2/fig. S16 (51 up, 42 down protein-coding genes). "
                       "Methods S4.6.p1: featureCounts -> DESeq2, DEG = fold change >= 2 and FDR-adjusted P < 0.05."),
            confidence="high")

# ---------------- 2. ownership
m = pd.read_csv(meta["path"], index_col=0)
own = {"accession": "GSE270400", "matrix_file": "GSE270400_All.count.txt.gz",
       "metadata_file": "GSE270400_metadata.csv", "owned": True,
       "checks": {"series_id": sorted(m["series_id"].unique().tolist()), "organism": sorted(m["organism_ch1"].unique().tolist()),
                  "n_samples": int(len(m)), "groups": m["characteristics_ch1.2.treatment"].value_counts().to_dict(),
                  "matrix_columns": ["12h-01-R", "12h-02-R", "12h-03-R", "12h-04-R", "NC-01-R", "NC-02-R", "NC-03-R", "NC-04-R"],
                  "data_processing": "Hisat2 Rnor_6.0 + featureCounts, matches S4.6.p1",
                  "accession_in_paper": "S5.4.p1"}}
case.decide("ownership", final=own, evidence=[meta, counts, paper], paper={"locator": "S5.4.p1; S4.6.p1"},
            reasoning=("Supplementary files carry the GSE270400 prefix; metadata series_id is GSE270400, organism Rattus norvegicus, "
                       "Achilles tendon, 4 x '12 h after 1 h treadmill running' + 4 x control; processing text matches S4.6.p1."),
            confidence="high")

# ---------------- 3. alignment
# Matrix uses author labels '12h-0k-R' / 'NC-0k-R'; GEO titles are '..., exercised 1 h and sacrificed 12 h after running, repk'
# and '..., control, repk'. Build an explicit label column from title (group + replicate number), then align exactly on it.
lab = native.derive_columns(meta["path"], case.dir / "aligned" / "metadata_with_label.csv",
                            patterns={"grp_raw": ("title", r"Achilles tendon, (control|exercised 1 h and\s+sacrificed 12 h after running), rep\d"),
                                      "rep": ("title", r"rep(\d)$")},
                            recode={"grp_raw": {"control": "NC", "exercised 1 h and  sacrificed 12 h after running": "12h"}})
mm = pd.read_csv(lab["output"], index_col=0)
mm["matrix_label"] = mm["grp_raw"] + "-0" + mm["rep"].astype(str) + "-R"
mm.to_csv(case.dir / "aligned" / "metadata_with_label.csv")
lab["columns"]["matrix_label"] = {"rule": "grp_raw + '-0' + rep + '-R'", "values": dict(zip(mm.index, mm["matrix_label"]))}
labelled = case.add_output(case.dir / "aligned" / "metadata_with_label.csv", "metadata_with_label")
aln = native.align_to_metadata(counts["path"], case.dir / "aligned" / "metadata_with_label.csv", case.dir / "aligned",
                               key_column="matrix_label")
print(json.dumps({k: v for k, v in aln.items() if k != "outputs"}, indent=1))
amat = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
ameta = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
der = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
                            patterns={"grp": ("characteristics_ch1.2.treatment", r"^(control|sacrificed 12 h)")},
                            recode={"grp": {"control": "NC", "sacrificed 12 h": "h12"}})
dmeta = case.add_output(der["output"], "design_metadata")
case.decide("alignment",
            final={"method": aln["method"] + " (label derived from GEO title: group word + replicate number)",
                   "n_aligned": aln["n_aligned"], "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                   "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                   "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                   "label_derivation": lab, "derived_columns": der},
            evidence=[counts, meta, labelled, amat, ameta, amap, dmeta], paper={"locator": "S4.6.p1"},
            reasoning=("Matrix columns use author labels (12h-0k-R, NC-0k-R). Each GEO title names the group (control vs 12 h after "
                       "running) and replicate k; the label is rebuilt from those two fields and matched exactly, not by position. "
                       "Group also cross-checked against characteristics 'treatment'. grp: NC (control) / h12 (12 h post-run)."),
            confidence="high")
print(der["levels"])

# ---------------- 4. matrix
prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
print(json.dumps(prof, indent=1))
case.write_json("matrix_profile.json", prof, role="matrix_profile")
case.decide("matrix",
            final={"matrix_type": "raw counts", "recommended_method": "DESeq2",
                   "profile": {k: prof[k] for k in ("n_features", "n_samples", "min", "max", "median", "integer_fraction",
                                                    "negative_values", "missing_values", "duplicated_feature_ids", "candidates")},
                   "paper_input": "featureCounts read counts (S4.6.p1)"},
            evidence=[amat, counts], paper={"locator": "S4.6.p1"},
            reasoning=("File GSE270400_All.count.txt.gz; Ensembl rat gene IDs; all non-negative integers; GEO data_processing and "
                       "Methods name featureCounts. Matches the paper's DESeq2 input. FPKM and author DEG tables are kept as reference only."),
            confidence="high")

# ---------------- 5. design (suitability)
dm = pd.read_csv(der["output"], index_col=0)
rep, item, summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["grp"],
                                      matrix_csv=aln["outputs"]["aligned_matrix"]["path"], organism="Rat",
                                      subject=None, references={"grp": "NC"}, planned=["grp_h12_vs_NC"])
print(json.dumps(summary, indent=1))
print([c.get("name") for c in rep["comparisons"]])
json.dump({"summary": summary, "comparisons": rep["comparisons"]}, open(case.dir / "suitability_summary_tmp.json", "w"), default=str, indent=1)
