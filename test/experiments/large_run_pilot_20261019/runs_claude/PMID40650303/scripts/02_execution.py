"""Gate 9 execution: DESeq2 ~ cell on all 24 samples (joint), plus pairwise 12-sample audits."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID40650303"
run = native.RunRecorder.open(RUN)
case = run.case("PMID40650303", accession="GSE298775")
cdir = case.dir
aligned = cdir / "aligned" / "aligned_matrix.csv"
design = cdir / "aligned" / "design_metadata.csv"
res_dir = cdir / "results"; res_dir.mkdir(parents=True, exist_ok=True)
sym = pd.read_csv(cdir / "aligned" / "gene_symbols.csv", index_col=0)["gene_symbol"]

sc = json.loads((cdir / "suitability_comparisons.json").read_text(encoding="utf-8"))
rep = json.loads((cdir / "suitability" / "suitability.json").read_text(encoding="utf-8"))
allc = {c["name"]: c for c in rep["comparisons"]}
names = sc["planned"] + sc["exploratory"]
comparisons = [allc[n] for n in names]
LABEL = {"dis_CC_vs_Ctl_ex-Sed": "CC_in_Sed", "dis_CC_vs_Ctl_ex-Ex": "CC_in_Ex",
         "ex_Ex_vs_Sed_dis-Ctl": "Ex_in_Ctl", "ex_Ex_vs_Sed_dis-CC": "Ex_in_CC",
         "dis_ex_CC_Ex_vs_Ctl_Sed": "CCxEx_interaction"}
PAPER = {"CC_in_Sed": {"n": 145, "up": 131, "down": 14, "abstract_n": 114}, "CC_in_Ex": {"n": 18, "up": 16, "down": 2}}

out = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(aligned), metadata_csv=str(design),
                       comparisons=comparisons, output_dir=str(res_dir / "joint_deseq2"))
print(json.dumps({k: out[k] for k in ("method", "formula", "n_samples", "n_genes", "cells")}, default=str))

RULE = dict(metric="padj", cutoff=0.05, effect_cutoff=1.0, inclusive=True)  # |LFC|>=1; padj==0.05 checked below
short = lambda d: {k: d[k] for k in ("n_significant", "n_up", "n_down")}


def sigset(path):
    tb = pd.read_csv(path, index_col=0)
    return tb, set(tb.index[(tb.padj < 0.05) & (tb.log2FoldChange.abs() >= 1)])


counts_out, outputs, sigsets, tops = {}, [], {}, {}
for r in out["results"]:
    lab = LABEL[r["name"]]
    t = native.apply_threshold(r["path"], **RULE)
    tb, s = sigset(r["path"])
    assert len(s) == t["n_significant"], (lab, len(s), t["n_significant"])
    assert not (tb.padj == 0.05).any()
    sigsets[lab] = s
    counts_out[lab] = {"paper_rule": t, "audit_padj0.05_only": short(native.apply_threshold(r["path"], metric="padj", cutoff=0.05)),
                       "paper": PAPER.get(lab, "not_reported"),
                       "role": "paper_planned" if r["name"] in sc["planned"] else "exploratory"}
    sig = tb.loc[sorted(s)].assign(symbol=lambda d: d.index.map(sym)).sort_values("log2FoldChange")
    tops[lab] = {"up": sig[sig.log2FoldChange > 0].sort_values("log2FoldChange", ascending=False).symbol.head(8).tolist(),
                 "down": sig[sig.log2FoldChange < 0].symbol.head(8).tolist()}
    item = case.add_output(r["path"], f"deg_{lab}")
    outputs.append({"contrast": lab, "suitability_name": r["name"], "path": r["path"], "sha256": item.get("sha256")})

# audit: pairwise 12-sample fits for the planned contrasts
dm = pd.read_csv(design, index_col=0)
cm = pd.read_csv(aligned, index_col=0)
pairwise = {}
for lab, ex in (("CC_in_Sed", "Sed"), ("CC_in_Ex", "Ex")):
    sub = dm[dm.ex == ex]
    pdir = res_dir / f"audit_pairwise_{lab}"; pdir.mkdir(exist_ok=True)
    mp, cp = pdir / "metadata.csv", pdir / "counts.csv"
    sub.to_csv(mp); cm[sub.index].to_csv(cp)
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(cp), metadata_csv=str(mp),
                         design_column="dis", control_group="Ctl", treatment_group="CC", output_dir=str(pdir))
        p = native.deg_outputs(pdir)[0]
        pairwise[lab] = short(native.apply_threshold(p, **RULE))
        _, ps = sigset(p)
        pairwise[lab]["jaccard_vs_joint"] = round(len(ps & sigsets[lab]) / max(1, len(ps | sigsets[lab])), 3)
        case.add_output(p, f"audit_pairwise_{lab}")
    except native.NativeToolError as e:
        pairwise[lab] = {"error": str(e)[:500]}

overlap = sorted(sigsets["CC_in_Sed"] & sigsets["CC_in_Ex"])
summary = {"n_genes_input": out["n_genes"], "formula": out["formula"], "cells": out["cells"],
           "counts": counts_out, "top_genes": tops,
           "overlap_CC_in_Sed_CC_in_Ex": {"n": len(overlap), "symbols": [sym.get(g) for g in overlap], "paper": 13},
           "audit_pairwise_paper_rule": pairwise}
case.write_json("results/deg_counts.json", summary, role="deg_counts")
print(json.dumps({k: {"ours": short(v["paper_rule"]), "paper": v["paper"]} for k, v in counts_out.items()}, indent=1))
print(json.dumps({"overlap": summary["overlap_CC_in_Sed_CC_in_Ex"], "pairwise": pairwise, "tops": tops}, indent=1, default=str))

case.decide("execution",
            final={"method": "DESeq2 (pydeseq2) ~ cell on 24 samples, Wald contrasts, BH with independent filtering per contrast",
                   "outputs": outputs, "n_genes_input": out["n_genes"], "rounding_documented": True,
                   "deg_counts_paper_rule": {k: short(v["paper_rule"]) for k, v in counts_out.items()},
                   "deg_sanity": {k: v["paper_rule"].get("deg_sanity") for k, v in counts_out.items()},
                   "audit_pairwise": pairwise},
            evidence=[case.add_output(cdir / "results" / "deg_counts.json", "deg_counts_summary")],
            reasoning="Approved route ran on all 24 samples; counts from native.apply_threshold under padj<0.05 & |log2FC|>=1.",
            confidence="high", execution_status="completed", decision_status="valid")
