"""Execution, study records and finish for PMID33257951."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID33257951"
run = native.RunRecorder.open(RUN)
case = run.case("PMID33257951")
D = case.dir
u = json.loads((D / "execution_summary.json").read_text(encoding="utf-8"))
summ_ev = case.add_output(D / "execution_summary.json", "execution_summary")
rule = {"metric": "FDR", "cutoff": 0.1, "effect_cutoff": None, "source": "paper (FIG4)"}


def brief(unit):
    return {c: {p: {"n_deg": v[p]["paper_FDR0.1"]["n_significant"], "up": v[p]["paper_FDR0.1"]["n_up"],
                    "down": v[p]["paper_FDR0.1"]["n_down"], "audit_padj0.05": v[p]["audit_padj0.05"]["n_significant"]}
                for p in ("all", "genes", "RE")} for c, v in unit["counts"].items()}


specs = [
    ("paper_grp", "all 14 samples, ~ grp (paper-aligned; OEX_vs_O exploratory)", "paper-aligned"),
    ("sens_sex_grp", "all 14 samples, ~ sex + grp (exploratory sensitivity, not paper route)", "exploratory"),
    ("female_grp", "9 female samples (3 per group), ~ grp (exploratory per-sex)", "exploratory"),
]
for key, subset, role in specs:
    unit = u[key]
    outs = [{"path": v["path"], "sha256": native.sha256(v["path"])} for v in unit["counts"].values()]
    case.decide("execution",
                final={"method": "DESeq2 (pydeseq2) joint model via tools.joint_contrasts:run_joint_deseq2",
                       "subset": subset, "role": role, "formula": unit["formula"].replace("cell", "grp"),
                       "executor_formula": unit["formula"], "n_samples": unit["n_samples"],
                       "n_features": unit["n_features"], "applied_threshold": rule,
                       "counts": brief(unit), "outputs": outs},
                evidence=[summ_ev], execution_status="completed", confidence="high",
                reasoning=f"{subset}: completed; counts with native.apply_threshold at padj < 0.1, split by gene vs RE rows.")

att = u["attenuation_check"]
pu = brief(u["paper_grp"])
summary = {
    "paper_aligned": {
        "route": "DESeq2 ~ grp on 14 samples, padj < 0.1 (FIG4)",
        "O_vs_Y": {"ours_genes": pu["O_vs_Y"]["genes"], "ours_RE": pu["O_vs_Y"]["RE"],
                   "paper": "~2500 transcripts changed with aging (FDR<0.1), largely reversed with exercise"},
        "OEX_vs_Y": {"ours_genes": pu["OEX_vs_Y"]["genes"], "ours_RE": pu["OEX_vs_Y"]["RE"], "paper": "not reported (attenuated)"},
        "OEX_vs_O (exploratory)": {"ours_genes": pu["OEX_vs_O"]["genes"], "ours_RE": pu["OEX_vs_O"]["RE"], "paper": "not reported"},
        "attenuation": att,
    },
    "reproduced": "Direction of the gene-level claim: O vs Y gives ~3,300 genes at FDR<0.1 versus ~300 for OEX vs Y; "
                  "97% of O-vs-Y genes move the opposite way in OEX vs O, median OEX/Y effect 0.69x of O/Y.",
    "not_reproduced_or_divergent": [
        "RE global shift: median log2FC of RE rows is +0.12 (O vs Y) but +0.34 (OEX vs Y) and +0.22 (OEX vs O) in the combined-table fit, "
        "so OEX does not show lower global RE than O here, unlike FIG4B. The paper may have normalized RE separately (TEtranscripts/RepEnrich2); not tested.",
        "Paper count is approximate (~2500) and may refer to the reversed subset; ours 3,280 genes / 3,353 features.",
    ],
    "sensitivity": {"sex_adjusted": brief(u["sens_sex_grp"]), "female_only": brief(u["female_grp"]),
                    "note": "OEX_vs_O rises from 656 to 3,058 features with sex adjustment and O_vs_Y falls to 612 in females only: counts are design-sensitive at n=4-5 per group."},
}
case.write_json("reproduction_summary.json", summary, role="reproduction_summary")
case.write_json("reproduction_plan.json", {
    "paper_aligned": "DESeq2 on raw gene+RE counts, ~ grp (Y/O/OEX), contrasts O vs Y and OEX vs Y, FDR < 0.1",
    "exploratory": ["OEX vs O from the same model", "~ sex + grp sensitivity", "female-only ~ grp (3 per group)"],
    "not_run": ["male-only (2/2/1)", "VO2max correlation (no VO2max in GEO)", "enrichment (paper did none for human data; not requested)"]},
    role="reproduction_plan")

case.decide("study",
            final={"route": "paper_aligned",
                   "contrasts": {"O_vs_Y": "paper_aligned", "OEX_vs_Y": "paper_aligned", "OEX_vs_O": "exploratory",
                                 "sex_adjusted": "exploratory", "female_only": "exploratory"},
                   "estimand_type": "associational",
                   "headline_n_deg": {"contrast": "OEX_vs_Y (paper planned exercise contrast), all features, padj<0.1",
                                      "n": pu["OEX_vs_Y"]["all"]["n_deg"]},
                   "exploratory_reason": "OEX_vs_O not reported by the paper; sex-adjusted and female-only fits are sensitivity analyses"},
            evidence=[summ_ev], confidence="medium",
            reasoning="Paper route reproduced (DESeq2, ~ grp, FDR<0.1). Cross-sectional: associations with habitual exercise, not effects of an intervention.")
pa = u["paper_grp"]["counts"]["OEX_vs_Y"]["all"]["paper_FDR0.1"]
case.finish(n_deg=pa["n_significant"], deg_sanity=pa["deg_sanity"])
run.finish()
print("done")
