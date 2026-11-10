"""Gate 11 (study) + finish."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42277794"
run = native.RunRecorder.open(RUN)
case = run.case("PMID42277794")
ex = json.loads((case.dir / "results" / "execution_summary.json").read_text(encoding="utf-8"))
prim = ex["primary_joint_all12"]["contrasts"]
n = {v["label"] if v["label"] != "exploratory" else k: v["n_deg_paper_rule"] for k, v in prim.items()}
plan = {"paper_aligned_route": "DESeq2 on STAR counts, all 12 deposited samples, joint ~ cell model, contrasts A/B/C, padj<0.05 & |log2FC|>log2(1.5)",
        "declared_deviations": ["SED-control n=3 (deposited, Methods S2.15.p1) vs n=2 in FIG4A; dropped-sample audit (GSM8187308) reported separately",
                                "GSEA via gseapy prerank on mouse Hallmark mh.all 2024.1 instead of Java GSEA on human h.all 2023.2 via ortholog chip",
                                "IPA (TREM-1 canonical pathway) not reproducible (proprietary)"],
        "exploratory": ["EXT exo vs EXT ctrl", "exercise x exosome interaction"]}
pi = case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
summ = {"n_deg_paper_rule_primary": n,
        "paper_reported_counts": "none in text (volcano plots FIG4A-B only)",
        "audits": {k: ex[k] for k in ("audit_pairwise_6sample", "audit_joint_minus_GSM8187308")},
        "pathway_comparison": {
            "C_SEDexo_vs_SEDctrl": "agrees: TNFa-NFkB (NES 2.18) and inflammatory response (1.74) enriched with exosome in SED (paper S3.4.p1, Fig S5)",
            "B_ExTexo_vs_SEDexo": "partly agrees: TNFa-NFkB lower in ExT (NES -2.45, q<0.001); inflammatory response not reversed (NES +1.45, q 0.04)",
            "metabolic_sets": "exosome in SED raises bile acid / xenobiotic / cholesterol / fatty acid sets; ExT-exo vs SED-exo reverses fatty acid (-1.54) and cholesterol (-1.33, q 0.08) but not bile acid (+1.45) or xenobiotic (+1.84)"},
        "trem1_gene": "Trem1 itself is barely detected (baseMean 1.1); its padj is NaN (independent filtering) in every contrast. The TREM-1 claim rests on IPA, not reproduced."}
si = case.write_json("reproduction_summary.json", summ, role="reproduction_summary")
case.decide("study",
            final={"route": "paper_aligned", "n_deg": n,
                   "declared_deviations": plan["declared_deviations"], "exploratory_contrasts": plan["exploratory"],
                   "threshold": "paper: padj < 0.05 and |log2FC| > 0.5849625 (FC 1.5)"},
            evidence=[pi, si], paper={"locator": "S2.15.p1"},
            reasoning=("Paper method, matrix and threshold reproduced on the deposited 12 samples; the FIG4A n=2 "
                       "discrepancy and enrichment library change are declared and audited separately."),
            confidence="medium", execution_status="completed")
case.finish(n_deg=n["A_ExTctrl_vs_SEDctrl"], deg_sanity=prim["ex_EXT_vs_SED_exo-ctrl"]["deg_sanity"])
run.finish()
print(json.dumps(n, indent=1))
