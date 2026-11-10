import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
from tools import native
native.enable_native_mode()
RUN = pathlib.Path(__file__).resolve().parents[1]
run = native.RunRecorder.open(str(RUN))
case = run.case("GSE164798")
rs = json.load(open(case.dir / "reproduction_summary.json", encoding="utf-8"))
ev = case.evidence_item("tool_output:reproduction_summary.json") if "tool_output:reproduction_summary.json" in json.load(open(case.dir / "case_state.json", encoding="utf-8"))["source_ids"] else case.evidence_item("paper:PMC8004053.paper.json")
per = {k: {"n_up": v["n_up"], "n_down": v["n_down"], "n_deg": v["n_significant"], "paper": v["paper_n_deg"]} for k, v in rs.items()}
case.write_json("reproduction_plan.json", {"route": "paper_aligned", "method": "DESeq2 pairwise within genotype, Psen1/App/Thy1 removed, BH padj<0.05", "contrasts": list(per)})
case.decide("study", final={"route": "paper_aligned", "per_contrast": per,
    "comparison_to_paper": "Qualitative pattern reproduced: only WT acute differs (vs sedentary and vs chronic); WT chronic vs sed and all three 5xFAD activity contrasts have 0 DEGs. Counts differ: WT acute vs sed 3828 vs paper 835, WT acute vs chronic 2028 vs paper 1617 (ranking of the two contrasts reversed). Chgb LFC matches (-0.274 / -0.256 vs paper -0.275 / -0.258) but padj ~1 here vs 0.02 in paper, suggesting the paper fit more samples per model (e.g. all 24 or per genotype) - model scope is not reported; pydeseq2 vs R DESeq2 1.30 may also contribute.",
    "deviations": ["pydeseq2 0.5.4 instead of R DESeq2 1.30.0", "per-contrast 8-sample fits (paper model scope not reported)"],
    "enrichment": "GSEA Hallmark + Enrichr ORA up/down for the two WT acute contrasts; up: mRNA splicing/RNA processing, down: neuronal/synaptic and mitochondrial terms, consistent with S3.3.2.p2"},
    evidence=[ev], reasoning="Paper route ran on paper threshold; n=4 per arm, residual df 6 (>=4), so not exploratory.",
    confidence="medium", paper={"locator": "S3.3.1.p1; S3.3.2.p2"})
c = rs["wt_acute_vs_wt_sed"]
print(case.finish(n_deg=c["n_significant"], deg_sanity=c["deg_sanity"]))
print(run.finish())
