import sys, pathlib, json; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os; os.chdir(ROOT)
from tools import native
native.enable_native_mode()

RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID32625117"
PAPER_JSON = "test/experiments/paper_screen_20261019/papers/PMC7311784.paper.json"
PAPER_MD = "test/experiments/paper_screen_20261019/papers/PMC7311784.paper.md"
MAT = "data/GSE140089/GSE140089_featureCounts.txt.gz"
META = "data/GSE140089/GSE140089_metadata.csv"

run = native.RunRecorder(RUN, request="Analyze GSE140089 for PMID 32625117 (RT in Parkinson's disease skeletal muscle): how exercise affects gene expression as the paper intends.",
                         platform_name="claude-code", decision_maker="Claude Opus 5.5 (claude-opus-5-5) native session",
                         case_ids=["PMID32625117"])
case = run.case("PMID32625117", accession="GSE140089")
pj = case.add_input(PAPER_JSON, "paper")
pm = case.add_input(PAPER_MD, "paper")
meta = case.add_input(META, "metadata")
mat = case.add_input(MAT, "matrix")

paper_threshold = {"metric": "FDR", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None,
                   "inclusive": False, "source_locator": "S2.6.p1; S3.1.p1; FIG1",
                   "note": "706 DEGs (304 up / 402 down) are called at FDR<0.05 alone (S3.1.p1, FIG1). S2.6.p1 additionally limits interpretation to |log2FC|>1 (FIG1: 42 up / 29 down; S3.1.p1 says 31 down) - recorded as a secondary paper-stated audit rule."}
recon = {
    "accessions": ["GSE140089"],
    "assay": "bulk RNA-seq, vastus lateralis, NuGEN Universal Plus mRNA-Seq, NovaSeq 2x50, STAR hg38 GENCODE + featureCounts (S2.4.p1, S2.5.p1)",
    "sample_inclusion": "DE analysis uses only the 5 PD exercisers, pre and post 16-wk RT (10 samples) (S2.1.p1, S2.6.p1). The other 31 GEO samples (7 basal PD, 12 OA, 12 YA) are for the exploratory PLIER analysis only.",
    "factors": {"time": ["pre-RT", "post-RT (16 wk)"], "subject": "5 PD participants"},
    "primary_estimand": "Within-subject change in skeletal muscle gene expression after 16-week high-intensity resistance training in PD (post vs pre)",
    "planned_contrasts": [{"name": "post_vs_pre", "treatment": "post-RT", "control": "pre-RT", "locator": "S2.6.p1"}],
    "repeated_measure_unit": "subject (paired pre/post; 'compared within the five PD subjects', S2.6.p1)",
    "normalization": "low-expression filter (unspecified) + voom (S2.6.p1)",
    "method": "limma-voom, BH FDR (S2.6.p1)",
    "paper_threshold": paper_threshold,
    "paper_counts": {"FDR<0.05": {"up": 304, "down": 402, "total": 706},
                     "FDR<0.05 & |log2FC|>=1": {"up": 42, "down": "29 (FIG1) / 31 (S3.1.p1, TAB3)"}},
    "out_of_scope": "PLIER latent-variable analysis across PD/OA/YA (S2.7, S3.2) is not a gene-level DE contrast of exercise",
}
case.write_json("paper_reconstruction.json", recon, role="paper_reconstruction")
case.write_json("paper_data_discrepancies.json", [
    {"item": "number of downregulated genes with |log2FC|>=1", "FIG1": 29, "S3.1.p1": 31, "impact": "reporting only; does not change estimand"},
    {"item": "matrix values", "paper": "featureCounts gene counts (S2.5.p1); GEO: 'counts of reads'", "data": "7.8% of values are non-integer with 2 decimals (fractional featureCounts counts)", "impact": "count-integer executors refuse; see matrix gate"},
    {"item": "pairing", "paper": "within-subject (S2.6.p1), blocking not spelled out", "data": "subject_id PD-0x-0 / PD-0x-16 gives 5 complete pairs", "impact": "none"}])
case.decide("paper_reconstruction", final=recon, evidence=[pj, pm], confidence="high", paper={"locator": "S2.6.p1"},
            reasoning="Abstract, S2.1, S2.4-S2.6, S3.1, FIG1 and S6 read. Primary DE = paired pre vs post 16-wk RT in 5 PD subjects, limma-voom, BH FDR<0.05; |log2FC|>1 only for interpretation tables.")

# ownership
import pandas as pd
m = pd.read_csv(META, index_col=0)
own = {"accession": "GSE140089", "matrix_file": MAT, "metadata_file": META, "owned": True,
       "checks": {"series_id": sorted(m["series_id"].unique().tolist()), "n_samples": int(len(m)),
                  "paper_n_samples": "41 (S2.4.p1)", "groups": m["source_name_ch1"].value_counts().to_dict(),
                  "post_training_samples": int((m["source_name_ch1"] == "Post-Training_Parkinsons_Disease").sum()),
                  "matrix_columns": 41}}
case.decide("ownership", final=own, evidence=[meta, mat, pm], confidence="high", paper={"locator": "S2.5.p1"},
            reasoning="Series file GSE140089 named in S2.5.p1/S6.p1; 41 samples = 41 in S2.4.p1; 12 basal PD (5 with -0 suffix are exercisers) + 5 post-training PD + 12 OA + 12 YA match S2.1.p1.")

# alignment: matrix columns M-M-xx appear only inside title 'Skeletal Muscle, M-M-xx'
al = case.dir / "aligned"
keyed = native.derive_columns(META, al / "metadata_keyed.csv", patterns={"library": ("title", r"^Skeletal Muscle, (M-M-\d+)$")})
aln = native.align_to_metadata(MAT, al / "metadata_keyed.csv", al, key_column="library")
print("align", aln["method"], aln["n_aligned"], aln["n_metadata"], aln["coverage"])
derived = native.derive_columns(aln["outputs"]["aligned_metadata"]["path"], al / "design_metadata_all.csv",
    patterns={"subject": ("characteristics_ch1.4.subject_id", r"^([A-Z]+-\d+)")},
    aliases={"grp_src": "source_name_ch1"},
    recode={"grp_src": {"Basal_Parkinsons_Disease": "PDpre", "Post-Training_Parkinsons_Disease": "post",
                        "Basal_Older_Adult": "OA", "Basal_Young_Adult": "YA"}})
# time: pre for basal PD, post for post-training; non-PD flagged 'none'
d = pd.read_csv(al / "design_metadata_all.csv", index_col=0)
d["time"] = d["grp_src"].map({"PDpre": "pre", "post": "post", "OA": "none", "YA": "none"})
d.to_csv(al / "design_metadata_all.csv")
pairs = native.complete_pairs_subset(aln["outputs"]["aligned_matrix"]["path"], al / "design_metadata_all.csv", al / "pd_pairs",
                                     subject_column="subject", condition_column="time", levels=["pre", "post"])
print("pairs", json.dumps({k: v for k, v in pairs.items() if k != "outputs"}, default=str)[:1500])
print(pairs.get("outputs"))
outs = [case.add_output(aln["outputs"]["aligned_matrix"]["path"], "aligned_matrix"),
        case.add_output(aln["outputs"]["aligned_metadata"]["path"], "aligned_metadata"),
        case.add_output(al / "design_metadata_all.csv", "design_metadata")]
case.write_json("alignment_derivations.json", {"keyed": keyed, "derived": derived, "time_rule": "grp_src PDpre->pre, post->post, OA/YA->none", "pairs": pairs}, role="derivations")
case.decide("alignment", final={"method": aln["method"], "key_column": "library (regex on title)", "n_aligned": aln["n_aligned"],
                                "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                                "derived_columns": ["subject", "time", "grp_src"],
                                "analysis_subset": "5 complete PD pre/post pairs (10 samples) via complete_pairs_subset"},
            evidence=[mat, meta] + outs, confidence="high", paper={"locator": "S2.6.p1"},
            reasoning="Matrix column names M-M-01..41 equal the suffix of GEO title; exact match on derived 'library' column. subject from subject_id prefix (PD-02-0/PD-02-16 -> PD-02); time from source_name.")
run_state = {"pairs": pairs, "aln": {k: aln[k] for k in ("method", "n_aligned", "n_metadata", "coverage")}}
(case.dir / "stage2_state.json").write_text(json.dumps(run_state, default=str, indent=1), encoding="utf-8")
