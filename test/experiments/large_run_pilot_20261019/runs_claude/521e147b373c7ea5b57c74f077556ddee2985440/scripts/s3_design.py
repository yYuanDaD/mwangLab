import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import pandas as pd
from tools import native
native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder.open(str(RUN))
case = run.case("GSE164798")
paper = case.evidence_item("paper:PMC8004053.paper.json")
DM = case.dir / "aligned" / "design_metadata.csv"
dmi = case.evidence_item("tool_output:design_metadata.csv")
recon = json.load(open(case.dir / "paper_reconstruction.json", encoding="utf-8"))
contrasts = [{"name": c["name"], "treatment": c["treatment"], "control": c["control"]} for c in recon["planned_contrasts"]]

dm = pd.read_csv(DM, index_col=0)
dc_full = native.design_check(dm, ["grp"])
dc_pairs = {}
for c in contrasts:
    sub = dm[dm["grp"].isin([c["control"], c["treatment"]])]
    dc_pairs[c["name"]] = native.design_check(sub, ["grp"])
conf = native.confounding_report(dm, "grp", ["characteristics_ch1.3.Sex", "characteristics_ch1.2.age", "characteristics_ch1.1.tissue"])
print("full:", {k: dc_full[k] for k in dc_full if k in ("rank", "n_columns", "residual_df", "full_rank")})
print("pair:", {n: {k: v[k] for k in v if k in ("rank", "residual_df", "full_rank")} for n, v in dc_pairs.items()})
print("conf:", json.dumps(conf, default=str)[:600])
case.write_json("design_checks.json", {"full_6group": dc_full, "pairwise": dc_pairs, "confounding": conf})

case.decide("design", final={
    "analysis_type": "pairwise_two_group", "design_column": "grp",
    "contrasts": contrasts, "estimand_type": "causal (randomized assignment to activity groups, S2.1.p1)",
    "model_scope": "each contrast fit on the 8 samples of its two groups (executor subsets to control+treatment)",
    "genotype_handling": "contrasts stay within genotype; grp = genotype_activity; no pooling of genotypes or activity levels"},
    candidates=[{"value": "~ genotype + activity (additive, pooled genotypes)", "reason_rejected": "paper analyses activity within each genotype separately and reports genotype-specific responses (WT responds, 5xFAD does not); pooling would average them"},
                {"value": "single 6-level ~ grp fit on all 24 samples", "reason_rejected": "paper does not state a joint fit; pairwise within-genotype DESeq2 (8 samples per fit) matches 'pairwise combinations ... in either 5xFAD or wild-type mice'. Scope is not_reported, so this is a medium-confidence reading"},
                {"value": "5xFAD vs WT per activity level", "reason_rejected": "genotype estimand, not the exercise question; secondary (S3.3.3)"}],
    evidence=[paper, dmi], reasoning="Six within-genotype pairwise activity contrasts in the paper's direction (chronic vs sed, acute vs sed, acute vs chronic), FIG6 / S3.3.1.p1. Each cell n=4.",
    confidence="medium", paper={"locator": "S3.3.1.p1; FIG6"})

case.decide("covariance", final={
    "status": "not_required", "blocking_terms": [],
    "covariates": [{"name": "Sex", "disposition": "excluded: constant (all male)"},
                   {"name": "age", "disposition": "excluded: constant (3 months)"},
                   {"name": "tissue", "disposition": "excluded: constant (right hemisphere)"},
                   {"name": "genotype", "disposition": "excluded: constant within every contrast (nested in grp)"},
                   {"name": "library processing (merged technical replicates / down-sampled sample 16)", "disposition": "excluded: technical read handling, not a design factor; all 24 libraries pooled on one flow cell (S2.4.p1); paper does not adjust"}]},
    evidence=[dmi, paper], reasoning="One brain sample per mouse, independent randomized groups; no subject repeated across groups, so no blocking. Constant or nested columns cannot enter the model; full and pairwise designs are full rank with residual df >= 6.",
    confidence="high", paper={"locator": "S2.1.p1; S2.4.p1; S2.5.p2"})

case.decide("method", final={
    "method": "DESeq2 (pydeseq2 0.5.4, Wald test, BH)", "matrix_type": "raw counts", "formula": "~ grp",
    "preprocessing": "remove Psen1, App, Thy1 rows before fitting (paper S2.5.p2); executor then drops all-zero genes; pydeseq2 independent filtering/Cook's outlier refit as in DESeq2 defaults",
    "deviation_notes": "pydeseq2 instead of R DESeq2 1.30.0; log2FoldChange reported as MLE (shrunken in separate column) - shrinkage does not change padj"},
    evidence=[paper, case.evidence_item("tool_output:aligned_matrix.csv")],
    reasoning="Paper used DESeq2 on featureCounts raw counts; matrix is integer raw counts, so the paper route runs directly.",
    confidence="high", paper={"locator": "S2.5.p2"})

thr = recon["paper_threshold"]
case.decide("threshold", final={"paper_threshold": thr, "threshold_source": "paper",
    "applied_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None, "inclusive": False}},
    evidence=[paper], reasoning="Paper: BH adjusted p < 0.05, no fold-change cutoff.", confidence="high", paper={"locator": "S2.5.p2"})
