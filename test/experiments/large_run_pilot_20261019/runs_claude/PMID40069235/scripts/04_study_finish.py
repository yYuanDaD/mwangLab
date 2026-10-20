"""Gate 11 study + reproduction artifacts + run.finish()."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40069235"
run = native.RunRecorder.open(RUN)
case = run.case("case_01")
summ = json.loads((case.dir / "results" / "execution_summary.json").read_text(encoding="utf-8"))

disc = [
    {"item": "matrix scale", "paper": "RPKM, filtered/floored (S5.6.p2)", "data": "GSE273041_raw_counts.txt.gz holds RPKM (decimals, floor ~0.109) despite its name",
     "disposition": "executable_without_change"},
    {"item": "gene count", "paper": "25,282 genes reliably sequenced (S2.1.p1)", "data": "25,262 rows", "disposition": "executable_without_change"},
    {"item": "sample label typo", "paper": "-", "data": "GSM8417462 description CC39020003_1_IP20 / participant id 1_IP20; timepoint field IP120",
     "disposition": "executable_without_change (timepoint field used)"},
    {"item": "statistical method", "paper": "mixed-effect ANOVA (car Type I, subject random) + Tukey post-hoc, BH FDR (S5.6.p3)",
     "data": "limma on log2(RPKM+1), ~ subject + tgrp (fixed subject block), moderated t, BH per contrast",
     "disposition": "requires_explicit_deviation"},
    {"item": "log2FC definition", "paper": "log2 fold-change (scale not stated; RPKM-based)", "data": "limma coefficient on log2(RPKM+1); compresses low-expression fold changes",
     "disposition": "requires_explicit_deviation"},
    {"item": "reported DEG counts", "paper": "S2.3.p2-p6: HC-only 330 (timepoint unclear), LC H0 161, shared H0 198, HC H2 222, LC H2 193, shared H2 100",
     "data": "text does not say which are totals vs diet-unique; direction split only in FIG4", "disposition": "executable_without_change (compared qualitatively)"},
    {"item": "pathway method", "paper": "WebGestaltR GO ORA on UpSet intersections; clusterProfiler", "data": "Enrichr GO/KEGG ORA per contrast + MSigDB Hallmark GSEA",
     "disposition": "requires_explicit_deviation"},
]
case.write_json("paper_data_discrepancies.json", disc, role="discrepancies")
plan = {"paper_route": "mixed ANOVA diet*time + Tukey, FDR<0.05 & |log2FC|>1 (blocked: no executor)",
        "run_route": "declared_deviation: limma on log2(RPKM+1), ~ subject + tgrp, 4 within-diet contrasts vs BL, "
                     "paper threshold FDR<0.05 & |log2FC|>1 (paper_on_deviation_route)",
        "contrasts": ["HC_H0_vs_BL", "HC_H2_vs_BL", "LC_H0_vs_BL", "LC_H2_vs_BL"],
        "not_run": ["diet contrasts at BL/H0/H2 (associational, not the exercise question)", "omnibus ANOVA F tests", "trait linear models (S2.4)"]}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
paper_counts = {"HC_H0_vs_BL": "330 'HC only' (S2.3.p2; timepoint ambiguous)", "LC_H0_vs_BL": "161 (S2.3.p2)",
                "HC_H2_vs_BL": "222 (S2.3.p6)", "LC_H2_vs_BL": "193 (S2.3.p6)",
                "shared_H0": "198 (S2.3.p3)", "shared_H2": "100 (S2.3.p6)"}
rs = {"route": "declared_deviation", "threshold": "FDR<0.05 & |log2FC|>1 (paper_on_deviation_route)",
      "ours": {k: {"n": v["paper_rule"]["n_significant"], "up": v["paper_rule"]["n_up"], "down": v["paper_rule"]["n_down"]}
               for k, v in summ["counts"].items()},
      "ours_overlaps": summ["overlaps_paper_rule"], "paper_reported": paper_counts,
      "audit_fdr_only": {k: v["audit_fdr_only"] for k, v in summ["counts"].items()},
      "comparison": ("Same order of magnitude (hundreds per contrast) and same qualitative picture: a large, largely shared "
                     "H0 response in both diets and a more diet-divergent H2 response. Exact counts differ; the paper's "
                     "text does not state whether its numbers are totals or diet-unique intersections."),
      "pathway_agreement": ("ORA LC_H0 includes angiogenesis/FOXO1/NOS3/transcription-regulation terms (paper S2.3.p3-p4); "
                            "H2 lists include metallothionein / response-to-metal-ion terms (paper S2.3.p6 shared H2).")}
case.write_json("reproduction_summary.json", rs, role="reproduction_summary")
case.decide("study", final={"route": "declared_deviation", "execution_outcome": "completed",
                            "deviation": "limma on log2(RPKM+1) with fixed subject block instead of mixed ANOVA + Tukey",
                            "exploratory": False, "exploratory_reason": "not exploratory: 10 subjects per diet, residual df 36"},
            evidence=[case.add_output(case.dir / "reproduction_summary.json", "reproduction_summary_ref")],
            confidence="high", paper={"locator": "S5.6.p3"},
            reasoning="Planned paper contrasts run on a validated alternative method with the paper threshold.")
case.finish(n_deg=None, deg_sanity="ok")
print(run.finish())
