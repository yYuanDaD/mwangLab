import sys, os, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT)); os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()

RUN = str(pathlib.Path(__file__).resolve().parents[1].relative_to(ROOT))
REQ = ("Use the bioinformatics-workflow skill to analyze GSE255280 for the paper 'Skeletal muscle BMAL1 is necessary "
       "for transcriptional adaptation of local and peripheral tissues in response to endurance exercise training' "
       "(PMID 37905004). Determine how exercise affects gene expression as the paper intends.")
run = native.RunRecorder(RUN, request=REQ, platform_name="claude-code",
                         decision_maker="Claude Code subagent (claude-opus-5-5)", case_ids=["case_01"])
case = run.case("case_01", accession="GSE255280")
P = "test/experiments/paper_screen_20261019/papers/"
paper = case.add_input(P + "PMC10614785.paper.json", "paper")
paper_md = case.add_input(P + "PMC10614785.paper.md", "paper")
META = "data/GSE255280/GSE255280_metadata.csv"; MAT = "data/GSE255280/GSE255280_Counts.txt.gz"
meta = case.add_input(META, "metadata"); mat = case.add_input(MAT, "matrix")

paper_threshold = {"metric": "qvalue", "adjustment": "FDR (DESeq2 Wald, Partek Flow; BH assumed)", "cutoff": 0.05,
                   "inclusive": False, "effect_metric": None, "effect_cutoff": None,
                   "source_locator": "S3.1.p1"}
recon = {
  "accessions": ["GSE255280"],
  "other_accessions_in_paper": {"GSE240653": "gastrocnemius training (not this case)",
                                "GSE253735": "peripheral tissue training (not this case)",
                                "GSE255376": "ATAC-seq (not this case)", "locator": "S2.17.p1"},
  "assay": "bulk poly-A RNA-seq, gastrocnemius, NovaSeq 6000 2x150, Novogene (S2.10.p1)",
  "organism": "Mus musculus, male, inducible muscle-specific Bmal1 KO (HSA-Cre; Bmal1 fl/fl) vs vehicle (S2.2.p1)",
  "factors": [{"name": "genotype", "levels": ["Vehicle", "iMSBmal1KO"], "locator": "S2.2.p1"},
              {"name": "exercise", "levels": ["Control (no exercise, time-of-day matched)",
                                               "Acute exercise, 30-min treadmill, 1 h post"],
               "locator": "S2.6.p1; FIG1"}],
  "sample_inclusion": "20 samples sequenced, n=5 per group, ~30 weeks of age (S2.10.p1); of 40 mice in the acute "
                      "experiment only the younger cohort was sequenced",
  "primary_estimand": "acute exercise effect on gastrocnemius gene expression, within each genotype "
                      "(Vehicle Ex vs Vehicle Ctrl; iMSBmal1KO Ex vs iMSBmal1KO Ctrl)",
  "planned_contrasts": [
      {"name": "vehicle_ex_vs_ctrl", "locator": "S3.1.p1; FIG1", "paper_counts": {"total": 989, "up": 600, "down": 389}},
      {"name": "ko_ex_vs_ctrl", "locator": "S3.1.p1; FIG1", "paper_counts": {"total": 517, "up": 250, "down": 267}}],
  "not_planned": "no genotype-by-exercise interaction test is reported; genotype comparison is done by Venn overlap "
                 "of the two DEG lists (117 shared, FIG1D)",
  "repeated_measure_unit": "none (one gastrocnemius per mouse, independent groups)",
  "normalization": "DESeq2 median of ratios within tissue (S2.11.p1)",
  "method": "Partek Flow DESeq2, negative binomial GLM, Wald test (S2.11.p1); STAR to mm10, Ensembl 99 quantification",
  "paper_threshold": paper_threshold,
  "unknown": "whether Partek fitted all 4 groups jointly or each genotype separately (not_reported)",
}
case.write_json("paper_reconstruction.json", recon)
case.decide("paper_reconstruction", final=recon, evidence=[paper, paper_md], confidence="high",
            paper={"locator": "S3.1.p1"},
            reasoning="GSE255280 is the acute-exercise experiment (S2.17.p1). Paper reports DESeq2 exercise DEGs within each "
                      "genotype at q<0.05 with no fold-change cutoff (S3.1.p1, FIG1C).")

m = pd.read_csv(META, index_col=0)
cols = pd.read_csv(MAT, sep=None, engine="python", nrows=2).columns.tolist()
own = {"accession": "GSE255280", "matrix_file": MAT, "metadata_file": META, "owned": True,
       "checks": {"series_id": sorted(m["series_id"].astype(str).unique().tolist()), "n_gsm": len(m),
                  "treatment_counts": m["characteristics_ch1.2.treatment"].value_counts().to_dict(),
                  "tissue": m["characteristics_ch1.0.tissue"].astype(str).unique().tolist(),
                  "n_matrix_sample_columns": len(cols) - 1,
                  "paper": "20 samples, n=5 per group, gastrocnemius (S2.10.p1) — matches"}}
case.decide("ownership", final=own, evidence=[paper, meta, mat], confidence="high", paper={"locator": "S2.17.p1"},
            reasoning="Series GSE255280 is named as the acute exercise dataset; 20 GSMs, 5 per treatment group, gastrocnemius; "
                      "the only supplementary matrix has 20 sample columns.")

aln = native.align_to_metadata(MAT, META, case.dir / "aligned", key_column="description")
print({k: v for k, v in aln.items() if k != "outputs"})
am = case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix")
ameta = case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata")
amap = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")

derived = native.derive_columns(
    aln["outputs"]["aligned_metadata"]["path"], case.dir / "aligned" / "design_metadata.csv",
    aliases={"treat_src": "characteristics_ch1.2.treatment", "time_src": "characteristics_ch1.3.time"},
    patterns={"geno": ("characteristics_ch1.2.treatment", r"^(Vehicle|iMSBmal1KO) \+"),
              "ex": ("characteristics_ch1.2.treatment", r"\+ (No Exercise|Exercise)$")},
    recode={"geno": {"Vehicle": "veh", "iMSBmal1KO": "ko"}, "ex": {"No Exercise": "ctrl", "Exercise": "ex"}})
dm = pd.read_csv(case.dir / "aligned" / "design_metadata.csv", index_col=0)
dm["grp"] = dm["geno"] + "_" + dm["ex"]
dm.to_csv(case.dir / "aligned" / "design_metadata.csv")
print(pd.crosstab(dm["grp"], dm["time_src"]))
print(pd.crosstab(dm["grp"], dm["title"].str.contains("Acute Exercise")))
dmeta = case.add_output(str(case.dir / "aligned" / "design_metadata.csv"), "design_metadata")
derived_rec = {k: v for k, v in derived.items() if k != "outputs"} if isinstance(derived, dict) else str(derived)
derived_rec = json.loads(json.dumps(derived_rec, default=str))
derived_rec["grp"] = "geno + '_' + ex (pandas concatenation after derive_columns)"
case.decide("alignment", final={"method": aln["method"], "key_column": "description", "n_aligned": aln["n_aligned"],
                                "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                                "unmatched": aln.get("unmatched", []), "derived_columns": derived_rec,
                                "label_note": "matrix/description label KO exercised mice 'iMSBmal1KO Exercise Trained 1-5'; "
                                              "GEO title ('iMSBmal1KO Acute Exercise'), treatment ('iMSBmal1KO + Exercise') "
                                              "and time ('ZT13-1 Hour Post') identify them as the acute bout arm"},
            evidence=[mat, meta, am, ameta, amap, dmeta], confidence="high", paper={"locator": "S2.10.p1"},
            reasoning="Matrix column names equal GEO 'description' exactly; exact match on that column, no positional alignment.")

prof = native.profile_matrix(aln["outputs"]["aligned_matrix"]["path"])
json.dump(prof, open(case.dir / "matrix_profile.json", "w", encoding="utf-8"), indent=1, default=str)
print(json.dumps(prof, default=str)[:2500])
x = pd.read_csv(aln["outputs"]["aligned_matrix"]["path"], index_col=0)
print("shape", x.shape, "dup ids", x.index.duplicated().sum(), "ERCC", x.index.astype(str).str.startswith("ERCC").sum())
print("colsums", x.sum().describe().to_dict())
