"""Reproduction artifacts, study record, finish."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40650303"
run = native.RunRecorder.open(RUN)
case = run.case("PMID40650303", accession="GSE298775")
cdir = case.dir
deg = json.loads((cdir / "results" / "deg_counts.json").read_text(encoding="utf-8"))
shr = json.loads((cdir / "results" / "audit_lfcshrink" / "summary.json").read_text(encoding="utf-8"))
case.add_output(cdir / "results" / "audit_lfcshrink" / "summary.json", "audit_lfcshrink_summary")
cnt = {k: {x: v["paper_rule"][x] for x in ("n_significant", "n_up", "n_down")} for k, v in deg["counts"].items()}

plan = {"paper_route": "DESeq2 v1.44.0 on tximport gene counts; CC-Sed vs Sed and CC-Ex vs Ex; BH padj<0.05 & |log2FC|>=1 (S4.6.p2)",
        "executed_route": "DESeq2 (pydeseq2) ~ cell on all 24 deposited integer counts, Wald contrasts, BH + independent filtering, same threshold",
        "deviations": ["no tximport length offsets (not deposited)", "pydeseq2 instead of R DESeq2",
                       "one 4-cell model (fit structure not reported); pairwise fits as audit"],
        "contrasts": {"paper_planned": ["CC_in_Sed", "CC_in_Ex"],
                      "exploratory": ["Ex_in_Ctl", "Ex_in_CC", "CCxEx_interaction"]},
        "enrichment": "not run: paper used rat GO/KEGG ORA (clusterProfiler); repository libraries are Mouse/Human only"}
case.write_json("reproduction_plan.json", plan, role="reproduction_plan")
summary = {
    "deg_counts_paper_rule": cnt,
    "paper_counts": {"CC_in_Sed": "145 (131 up, 14 down; abstract says 114)", "CC_in_Ex": "18 (16 up, 2 down)", "overlap": 13},
    "overlap_ours": deg["overlap_CC_in_Sed_CC_in_Ex"]["n"],
    "audits": {"pairwise_deseq2": deg["audit_pairwise_paper_rule"], "pairwise_lfc_shrink": shr,
               "padj_only": {k: v["audit_padj0.05_only"]["n_significant"] for k, v in deg["counts"].items()}},
    "agreement": ("Direction of the paper's conclusion reproduced: the CC signature is larger in sedentary than in trained "
                  "rats (joint 318 vs 214; pairwise 363 vs 133), and both are up-dominated as in the paper. Absolute counts "
                  "are 2.2x (Sed) and 12x (Ex) the paper's and are not explained by LFC shrinkage (233 / 88) or by pairwise "
                  "fitting. Paper genes: Nr4a3, Dgat2, Pnpla2, Socs2 (down), Hopx (down), Prodh, Fbxo32, Glul, Acss1 "
                  "reproduce in sign and significance; Tnnc1/Tpm3/Tnni1/Myl3 have log2FC 1.6-2.0 in CC_in_Sed but padj "
                  "0.18-0.33 (bimodal per-sample expression, likely slow-fibre content varying between dissections); "
                  "Hbb/Hba-a1/Hba-a3 in CC_in_Ex log2FC 1.4-1.5, padj 0.058-0.075 (just short). The paper's outlier removal "
                  "(mentioned for WGCNA, S2.4.p1) or an unreported filter may account for the gap."),
    "exercise_effect": ("Training itself (Ex vs Sed within saline or within CC) gives 0 DEGs under the paper rule, and the "
                        "disease x training interaction gives 0 DEGs. The paper's 'training mitigates the CC signature' is an "
                        "inference from comparing two separately thresholded lists; the formal interaction test does not "
                        "support a gene-level training x disease effect at n=6."),
}
s_ev = case.write_json("reproduction_summary.json", summary, role="reproduction_summary")
print(json.dumps(summary, indent=1, default=str))
case.decide("study",
            final={"route": "paper_aligned",
                   "summary": "paper contrasts, method family and threshold on the deposited counts (joint 4-cell DESeq2); training contrasts and interaction exploratory",
                   "deg_counts_paper_rule": cnt, "paper_counts": summary["paper_counts"],
                   "exploratory": plan["contrasts"]["exploratory"],
                   "exploratory_reason": "not tested in the paper; added to answer the exercise question",
                   "deviations": plan["deviations"]},
            evidence=[s_ev], paper={"locator": "S2.2.p2"}, confidence="medium",
            reasoning="All gates valid; DESeq2 as in the paper on the authors' deposited counts. Counts differ from the paper (see reproduction_summary).",
            execution_status="completed", decision_status="valid")
print(case.finish(n_deg=cnt["CC_in_Sed"]["n_significant"], deg_sanity="ok"))
print(run.finish())
