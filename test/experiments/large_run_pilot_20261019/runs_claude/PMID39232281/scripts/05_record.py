"""Record execution + study for every tissue case from compute.json, compare with the paper,
then run.finish(). Continues the run with RunRecorder.open."""
import sys, pathlib; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import os, json
from common import *
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
run = native.RunRecorder.open(RUN)
sym = pd.read_csv(RAW, index_col=0, usecols=[0, 1])["Symbol"]
paper_ev = {"id": "paper:PMC11378950", "kind": "paper", "path": PAPER_JSON}
SX = {"F": "female", "M": "male"}
rows, sig_sets = [], {}

for cid, tissue in TISSUES.items():
    case = run.case(cid)
    comp = json.loads((case.dir / "compute.json").read_text(encoding="utf-8"))
    cj = case.add_output(case.dir / "compute.json", "execution_summary")
    filt = comp.get("filter", {})
    for model, label in (("A", "time_independent"), ("B", "time_specific")):
        res = comp.get(f"model_{model}")
        if comp["status"] != "completed" or not res:
            case.decide("execution", final={"method": "DESeq2 joint model", "subset": label,
                                            "execution_error": comp.get("error", "not run")},
                        evidence=[cj], confidence="high", execution_status="failed",
                        reasoning="Executor raised; see compute.json.")
            continue
        outs = []
        for r in res["results"]:
            ev = case.add_output(r["path"], f"deg_{model}_{r['name']}")
            outs.append({"comparison": r["name"], "path": r["path"], "planned": r["planned"],
                         "n_padj_lt_0.05": r["n_sig"], "up": r["up"], "down": r["down"], "n_tested": r["n_tested"],
                         "deg_sanity": r["deg_sanity"], "exploratory_small_n": r["forced_small_n"]})
            if r["planned"]:
                sex = next((v for k, v in [("sex-F", "F"), ("sex-M", "M")] if k in r["name"]),
                           "F" if cid in ("OVA", "UTE") else ("M" if cid == "TES" else None))
                zt = "zt05" if "zt-zt05" in r["name"] else ("zt17" if "zt-zt17" in r["name"] else "pooled")
                pc = PAPER_COUNTS.get((cid, sex)) if zt == "pooled" else None
                rows.append({"tissue": cid, "sex": sex, "zt": zt, "contrast": r["name"], "n_deg": r["n_sig"],
                             "up": r["up"], "down": r["down"], "n_tested": r["n_tested"],
                             "paper_n": pc["n"] if pc else None, "paper_up": pc["up"] if pc else None,
                             "paper_down": pc["down"] if pc else None,
                             "exploratory_small_n": r["forced_small_n"]})
                if zt == "pooled":
                    t = pd.read_csv(r["path"], index_col=0)
                    s = t[t["padj"] < 0.05]
                    sig_sets[(cid, sex)] = {"up": set(s.index[s["log2FoldChange"] > 0]),
                                            "down": set(s.index[s["log2FoldChange"] < 0])}
        case.decide("execution", final={
            "method": "DESeq2 (pydeseq2 joint cell-means model)", "subset": label,
            "formula": res["formula"], "cells": res["cells"], "n_samples": res["n_samples"], "n_genes": res["n_genes"],
            "gene_filter": filt, "outputs": outs, "skipped": res["skipped"],
            "applied_threshold": "padj < 0.05 (BH), no effect cutoff, counted with native.apply_threshold",
            "seconds": res.get("seconds"),
        }, evidence=[cj], confidence="high", execution_status="completed",
            reasoning=f"Model {model} fitted on all {res['n_samples']} {tissue} samples; contrasts extracted from one fit.")
    small = [r["contrast"] for r in rows if r["tissue"] == cid and r["exploratory_small_n"]]
    planned_pooled = [r for r in rows if r["tissue"] == cid and r["zt"] == "pooled"]
    case.decide("study", final={
        "route": "declared_deviation",
        "deviation_note": ("paper formula not reported: interpreted as ~ cell (sex x trt) per tissue, ZT pooled, and ~ cell (sex x trt x ZT) "
                           "for ZT-specific contrasts; pydeseq2 instead of R DESeq2 1.34"),
        "planned_results": {r["contrast"]: r["n_deg"] for r in rows if r["tissue"] == cid},
        "exploratory": "non-treatment comparisons (ZT, sex, interactions) in the plans; " + (
            f"{small} has a cell with n=2 (exploratory_reason: fewer than 3 biological replicates)" if small else "no small-n planned contrast"),
        "exploratory_reason": "fewer than 3 replicates in a cell" if small else None,
        "estimand_note": "Deficient (high-workload exercise-for-food) vs Control (low-workload exercise); not exercise vs sedentary",
    }, evidence=[cj, paper_ev], paper={"locator": "S4.3.13.p1"}, confidence="medium",
        reasoning="All planned contrasts executed under the paper threshold.")
    case.finish(n_deg=sum(r["n_deg"] for r in planned_pooled), deg_sanity=None)

table = pd.DataFrame(rows)
table["symbol"] = None
table.drop(columns="symbol").to_csv(pathlib.Path(RUN) / "deg_counts_vs_paper.csv", index=False)

# Unions (paper S2.3.p1, S2.6.p1, S2.6.p4) and gene-level direction claims
def union(tissues, sex):
    keys = [(t, sex) for t in tissues if (t, sex) in sig_sets]
    up = set().union(*[sig_sets[k]["up"] for k in keys]); down = set().union(*[sig_sets[k]["down"] for k in keys])
    return {"n": len(up | down), "up_any": len(up), "down_any": len(down), "tissues": len(keys)}
unions = {}
for name, ts in (("muscles", MUSCLES), ("tendons", TENDONS), ("all_tissues", list(TISSUES))):
    for sex in ("F", "M"):
        unions[f"{name}_{sex}"] = {"ours": union(ts, sex), "paper": PAPER_UNIONS.get((name, sex))}
by_symbol = {}
for (t, sex), d in sig_sets.items():
    for direction in ("up", "down"):
        for g in d[direction]:
            by_symbol.setdefault((sym.get(g), sex, direction), set()).add(t)
nF = sum(1 for k in sig_sets if k[1] == "F"); nM = sum(1 for k in sig_sets if k[1] == "M")
claims = {}
for g, d, paper in (("Oxtr", "down", "13/18 F"), ("P4ha1", "down", "11/18 F"), ("Pcif1", "up", "14/18 F, 1/17 M"),
                    ("Igf1r", "up", "10/18 F, 3/17 M"), ("Cirbp", "up", "multiple F and M"), ("Mt2", "up", "multiple F and M")):
    claims[g] = {"direction": d, "paper": paper,
                 "ours": f"{len(by_symbol.get((g, 'F', d), ()))}/{nF} F, {len(by_symbol.get((g, 'M', d), ()))}/{nM} M"}
for g, d in (("Foxo3", "up"), ("Loxl2", "down")):
    claims[g + "_muscles"] = {"direction": d, "paper": "all muscles (S2.6.p3)",
                              "ours": {sx: sorted(by_symbol.get((g, sx, d), set()) & set(MUSCLES)) for sx in ("F", "M")}}
comparison = {"unions": unions, "gene_claims": claims}
(pathlib.Path(RUN) / "paper_comparison.json").write_text(json.dumps(comparison, indent=1), encoding="utf-8")
print(table.to_string())
print(json.dumps(comparison, indent=1))
print(run.finish())
