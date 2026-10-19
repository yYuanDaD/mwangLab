"""case_01: post- vs pre-training within DM1, subject-blocked DESeq2 (declared deviation)."""
import json
import pandas as pd
from common import *  # noqa
from tools import native

native.enable_native_mode()
run = native.RunRecorder.open(RUN_DIR)
case = run.case("case_01")
paper = case.evidence_item("paper:PMC10443797.paper.json")
dmeta_path = case.dir / "aligned" / "design_metadata.csv"
dmeta = case.evidence_item("tool_output:design_metadata.csv")
amat = case.evidence_item("tool_output:aligned_matrix.csv")

dm = pd.read_csv(dmeta_path, index_col=0)
dm1 = dm[dm.grp.isin(["pre", "post"])]
pair = native.pairing_report(dm1, "subject", "grp", ["pre", "post"])
conf = native.confounding_report(dm1, "grp", ["subject"])
dchk = native.design_check(dm1, ["subject", "grp"])
case.write_json("design_checks.json", {"pairing": pair, "confounding": conf, "design_check": dchk})
print(json.dumps(pair), json.dumps(dchk)[:600])

case.decide("design",
            final={"analysis_type": "paired (two timepoints within subject)", "design_column": "grp",
                   "control": "pre", "treatment": "post", "formula": "~ subject + grp",
                   "samples": "18 DM1 samples (9 subjects x pre/post); controls not used in this contrast",
                   "estimand_type": "within-subject change (no untrained DM1 arm; change = training + time)",
                   "relation_to_paper": ("Paper's grouped exercise quantity is Δlog2FC = log2FC(post vs ctrl) - "
                                         "log2FC(pre vs ctrl) from separate unpaired fits (S2.2.p2); this case tests "
                                         "the same difference directly with subject pairing. Declared deviation.")},
            candidates=[{"value": "post vs pre unpaired (~ grp)", "reason_rejected": "ignores 9 complete pre/post pairs"},
                        {"value": "post vs control only", "reason_rejected": "measures disease + training, not training"},
                        {"value": "pool pre+post vs control", "reason_rejected": "answers disease, not exercise"}],
            evidence=[paper, dmeta], paper={"locator": "S2.2.p2"}, confidence="medium",
            reasoning=("The question is how training changes expression; each DM1 participant has a pre and a "
                       "post biopsy, so the direct estimand is the within-subject post-vs-pre change. The paper "
                       "reaches it indirectly via controls; there is no untrained DM1 group, so time and training "
                       "are not separable (same as the paper)."))

case.decide("covariance",
            final={"status": "required", "blocking_terms": ["subject"],
                   "covariates": [{"name": "subject", "disposition": "included"},
                                  {"name": "age", "disposition": "excluded: not in GEO metadata; constant within subject anyway"},
                                  {"name": "sex", "disposition": "excluded: single level (all male)"},
                                  {"name": "sequencing batch/lane", "disposition": "excluded: not in metadata; "
                                   "FastQC file names suggest pre/post of a participant were sequenced together"}],
                   "pairing": {k: pair[k] for k in ("n_subjects", "n_complete", "complete_and_unique")}},
            evidence=[dmeta], confidence="high",
            reasoning="9/9 subjects complete and unique; design ~ subject + grp full rank, residual df "
                      f"{dchk.get('residual_df')}.")

case.decide("method",
            final={"method": "DESeq2 (pydeseq2), Wald test", "matrix_type": "raw counts",
                   "formula": "~ subject + grp", "contrast": "grp: post vs pre",
                   "prefilter": "keep genes with >=10 counts in at least one of the 18 samples (literal reading of "
                                "S4.4.p1 'less than 10 counts in each samples were filtered out')",
                   "paper_route": {"method": "edgeR 3.34.1 QL F-test, each group vs controls, Δlog2FC",
                                   "status": "blocked",
                                   "reason": ("paper has no post-vs-pre test; repository edgeR executor "
                                              "(tools/edger_tools.py) fits only ~ Treatment, no subject blocking, "
                                              "and no TMM. Paper's grouped route is run in case_02.")}},
            candidates=[{"value": "edgeR two-arm", "reason_rejected": "no covariate interface -> cannot block subject"},
                        {"value": "limma on log2(CPM+1) with subject", "reason_rejected": "valid, but DESeq2 is the "
                         "default count method and keeps the NB model family of the paper"}],
            evidence=[amat, paper], paper={"locator": "S4.13.p1"}, confidence="medium",
            reasoning="Raw counts + paired design -> DESeq2 with subject as an additive blocking factor.")

case.decide("threshold",
            final={"paper_threshold": PAPER_THRESHOLD, "threshold_source": "paper_on_deviation_route",
                   "applied_threshold": {"metric": "pvalue", "adjustment": "none", "cutoff": 0.05,
                                         "effect_metric": "log2FC", "effect_cutoff": 2.0, "inclusive": False},
                   "audit_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.05,
                                       "effect_metric": None, "effect_cutoff": None,
                                       "label": "audit (workflow default, BH within contrast)"}},
            evidence=[paper], paper={"locator": "S4.4.p1"}, confidence="medium",
            reasoning=("The paper's DEG rule for the strength-training program (|log2FC|>2, raw P<0.05) is applied "
                       "on the deviation route; it carries no multiple-testing control, so a BH padj<0.05 count "
                       "is reported separately as audit."))

# ---- execution
counts = pd.read_csv(case.dir / "aligned" / "aligned_matrix.csv", index_col=0)
sub = counts[dm1.index]
keep = (sub >= 10).any(axis=1)
filt_path = case.dir / "results" / "counts_dm1_filtered.csv"
filt_path.parent.mkdir(parents=True, exist_ok=True)
sub.loc[keep].to_csv(filt_path)
meta_path = case.dir / "results" / "design_metadata_dm1.csv"
dm1.to_csv(meta_path)
print("genes kept", int(keep.sum()), "of", len(keep))
outdir = case.dir / "results" / "deseq2_paired"
try:
    msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(filt_path),
                           metadata_csv=str(meta_path), design_column="grp", control_group="pre",
                           treatment_group="post", output_dir=str(outdir), covariate_columns="subject")
    print(msg)
    deg = native.deg_outputs(outdir)[0]
    applied = native.apply_threshold(deg, metric="pvalue", cutoff=0.05, effect_cutoff=2.0, min_group_n=9)
    audit = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None, min_group_n=9)
    out = case.add_output(deg, "deg_table")
    case.write_json("threshold_counts.json", {"applied": applied, "audit": audit})
    print(json.dumps(applied), json.dumps(audit))
    case.decide("execution",
                final={"method": "DESeq2 (pydeseq2), Wald test", "formula": "~ subject + grp",
                       "outputs": [deg], "n_genes_tested": applied["n_tested"],
                       "n_genes_after_prefilter": int(keep.sum()),
                       "applied_counts": applied, "audit_counts": audit},
                evidence=[out, amat], confidence="high", execution_status="completed",
                reasoning="DESeq2 completed on 18 samples with subject blocking.")
except native.NativeToolError as e:
    print("FAILED", e)
    case.decide("execution", final={"method": "DESeq2 (pydeseq2), Wald test", "formula": "~ subject + grp",
                                    "execution_error": str(e)},
                evidence=[amat], confidence="high", execution_status="failed", reasoning="executor failed")
