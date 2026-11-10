"""Execution for GSE312780: primary joint DESeq2 (16 subjects) + exploratory units."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json; os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41610852"
run = native.RunRecorder.open(RUN)
case = run.case("GSE312780")
D = case.dir
sub = D / "aligned/primary_16subjects"
pm = pd.read_csv(sub / "design_metadata.csv", index_col=0)
full_meta = pd.read_csv(D / "aligned/design_metadata.csv", index_col=0)
counts_all = native.read_table(D / "aligned/aligned_matrix.csv")
rep = json.load(open(D / "suitability/suitability.json"))
THR = dict(metric="padj", cutoff=0.05, effect_cutoff=0.585)
AUDIT = dict(metric="pvalue", cutoff=0.05, effect_cutoff=0.585)


def tcomps(levels):
    c = []
    if "post_BFRT" in levels:
        c.append({"name": "time_post_vs_pre_arm-BFRT", "kind": "simple", "analyzable": True,
                  "cells": [{"cell": {"tcell": "post_BFRT"}}, {"cell": {"tcell": "base"}}]})
    if "post_CREST" in levels:
        c.append({"name": "time_post_vs_pre_arm-CREST", "kind": "simple", "analyzable": True,
                  "cells": [{"cell": {"tcell": "post_CREST"}}, {"cell": {"tcell": "base"}}]})
    if {"post_BFRT", "post_CREST"} <= set(levels):
        # with subject blocking, tcell[post_BFRT] - tcell[post_CREST] = (BFRT post-pre) - (CREST post-pre)
        c.append({"name": "arm_time_BFRT_post_vs_CREST_pre", "kind": "simple", "analyzable": True,
                  "cells": [{"cell": {"tcell": "post_BFRT"}}, {"cell": {"tcell": "post_CREST"}}]})
    return c


def prepare(meta, label):
    d = D / "results" / label
    d.mkdir(parents=True, exist_ok=True)
    cnt = counts_all.loc[:, meta.index]
    cnt = cnt[cnt.sum(axis=1) >= 10]          # paper: drop genes with < 10 total counts
    cpath, mpath = d / "counts_filtered.csv", d / "design_metadata.csv"
    cnt.to_csv(cpath); meta.to_csv(mpath)
    return d, cpath, mpath, int(len(cnt))


summary = {}


def unit(label, meta, comps, covariates, method_text, formula):
    d, cpath, mpath, ngenes = prepare(meta, label)
    try:
        res = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(cpath), metadata_csv=str(mpath),
                               comparisons=comps, output_dir=str(d), covariates=covariates,
                               round_estimated_counts=True)
    except native.NativeToolError as e:
        case.decide("execution", final={"method": method_text, "subset": label, "execution_error": str(e)},
                    evidence=[case.add_output(mpath, f"metadata_{label}")], reasoning="executor failed",
                    confidence="high", execution_status="failed")
        summary[label] = {"error": str(e)}
        return
    json.dump(res, open(d / "joint_result.json", "w"), indent=1, default=str)
    outs, counts = [], {}
    for r in res["results"]:
        o = case.add_output(r["path"], f"deg_{label}_{r['name']}")
        outs.append(o)
        a = native.apply_threshold(r["path"], **THR)
        b = native.apply_threshold(r["path"], **AUDIT)
        tab = pd.read_csv(r["path"], index_col=0)
        ties = int(((tab["log2FoldChange"].abs() - 0.585).abs() < 1e-9).sum())
        counts[r["name"]] = {"applied": a, "audit_raw_p": b, "padj_only_0.05": r["n_padj_0.05"], "lfc_ties_at_0.585": ties}
    summary[label] = {"formula": res["formula"], "n_samples": res["n_samples"], "n_genes_tested_input": ngenes,
                      "cells": res["cells"], "counts": counts, "skipped": res["skipped"]}
    case.decide("execution",
                final={"method": method_text, "subset": label, "formula": formula,
                       "outputs": [o["path"] for o in outs], "n_samples": res["n_samples"],
                       "n_genes": res["n_genes"],
                       "counts_applied": {k: {kk: v["applied"][kk] for kk in ("rule", "n_tested", "n_significant", "n_up", "n_down", "deg_sanity")}
                                          for k, v in counts.items()}},
                evidence=outs + [case.add_output(d / "joint_result.json", f"joint_result_{label}")],
                reasoning=f"{label}: run_joint_deseq2 completed.", confidence="high", execution_status="completed")


M = "DESeq2 (pydeseq2 joint model, rounded salmon counts, MLE LFC)"
unit("primary_16subjects", pm, tcomps(set(pm["tcell"])), ["subject"], M, "~ subject + tcell")
arm_comps = [c for c in rep["comparisons"] if c["name"].startswith("arm_BFRT_vs_CREST")]
unit("exploratory_between_arm", pm, arm_comps, [], M + ", no subject block", "~ cell (arm x time)")
fm = full_meta.copy()
unit("exploratory_sensitivity_17subjects", fm, tcomps(set(fm["tcell"])), ["subject"], M, "~ subject + tcell")
male = pm[pm["sex"] == "male"]
unit("exploratory_male", male, tcomps(set(male["tcell"])), ["subject"], M, "~ subject + tcell")
fem = pm[pm["sex"] == "female"]
unit("exploratory_female_CREST", fem, tcomps(set(fem["tcell"])), ["subject"], M, "~ subject + tcell")

json.dump(summary, open(D / "results/execution_summary.json", "w"), indent=1, default=str)
for k, v in summary.items():
    print(k, v.get("formula"), v.get("n_samples"))
    for n, c in v.get("counts", {}).items():
        print("   ", n, c["applied"]["n_significant"], f"(up {c['applied']['n_up']}, down {c['applied']['n_down']})",
              "| padj<0.05 only:", c["padj_only_0.05"], "| audit raw p:", c["audit_raw_p"]["n_significant"], "| ties", c["lfc_ties_at_0.585"])
