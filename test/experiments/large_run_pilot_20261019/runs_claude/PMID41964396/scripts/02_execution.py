"""Gates 9-11 (execution, enrichment plan, study) + run.finish for PMID41964396. Continues the run with RunRecorder.open."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from pydeseq2.preprocessing import deseq2_norm
from tools import native
from common import RUN, CASES, PAPER_THRESHOLD, COMPARISONS, REPORTED

native.enable_native_mode()
run = native.RunRecorder.open(RUN)
TH = dict(metric="padj", cutoff=PAPER_THRESHOLD["cutoff"], effect_cutoff=PAPER_THRESHOLD["effect_cutoff"])

for case_id, cfg in CASES.items():
    case = run.case(case_id)
    paper = None
    am = case.dir / "aligned" / "aligned_matrix.csv"
    dm = case.dir / "aligned" / "design_metadata.csv"
    res_dir = case.dir / "results"
    res_dir.mkdir(exist_ok=True)
    # Paper prefilter (S2.14.p1): drop features with < 10 DESeq2-normalised counts summed over all samples.
    counts = pd.read_csv(am, index_col=0)
    normed, sf = deseq2_norm(counts.T)
    keep = normed.sum(axis=0) >= 10
    filt = counts.loc[keep.values]
    fpath = res_dir / "counts_prefiltered.csv"
    filt.to_csv(fpath)
    comps = json.loads((case.dir / "suitability" / "suitability.json").read_text(encoding="utf-8"))["comparisons"]
    comps = [c for c in comps if c["name"] in COMPARISONS]
    summary = {"prefilter": {"n_in": int(counts.shape[0]), "n_kept": int(keep.sum())}, "contrasts": {}}
    outputs, exec_err = [], None
    try:
        out = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(fpath), metadata_csv=str(dm),
                               comparisons=comps, output_dir=str(res_dir / "deseq2_subject_time"), covariates=("subject",))
        audit = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(fpath), metadata_csv=str(dm),
                                 comparisons=comps, output_dir=str(res_dir / "audit_deseq2_time_only"), covariates=())
    except native.NativeToolError as e:
        exec_err = str(e)
    if exec_err is None:
        audit_paths = {r["name"]: r["path"] for r in audit["results"]}
        for r in out["results"]:
            n = r["name"]
            ev = case.add_output(r["path"], f"deg_{n}")
            outputs.append(ev)
            ap = case.add_output(audit_paths[n], f"audit_deg_time_only_{n}")
            row = {"paper_rule": native.apply_threshold(r["path"], **TH),
                   "audit_fdr_only": native.apply_threshold(r["path"], metric="padj", cutoff=0.05),
                   "audit_raw_p": native.apply_threshold(r["path"], metric="pvalue", cutoff=0.05),
                   "audit_unblocked_paper_rule": native.apply_threshold(audit_paths[n], **TH),
                   "audit_unblocked_fdr_only": native.apply_threshold(audit_paths[n], metric="padj", cutoff=0.05),
                   "audit_unblocked_raw_p": native.apply_threshold(audit_paths[n], metric="pvalue", cutoff=0.05),
                   "paper_reported": REPORTED[case_id].get(n)}
            t = pd.read_csv(r["path"], index_col=0)
            for feat in ("hsa-miR-146b-5p", "ENSG00000109819"):  # PPARGC1A
                hit = [i for i in t.index if str(i).split(".")[0] == feat]
                if hit:
                    row[feat] = t.loc[hit[0], ["log2FoldChange", "pvalue", "padj"]].to_dict()
            summary["contrasts"][n] = row
        summary["formula"] = out["formula"] + " (cell = time)"
        summary["n_samples"], summary["n_features_tested"] = out["n_samples"], out["n_genes"]
        case.decide("execution",
                    final={"method": "DESeq2 (pydeseq2) joint model ~ subject + time", "formula": "~ subject + time",
                           "outputs": [o["path"] for o in outputs], "prefilter": summary["prefilter"],
                           "counts": {n: summary["contrasts"][n]["paper_rule"] for n in summary["contrasts"]}},
                    evidence=outputs, execution_status="completed", paper={"locator": "S2.14.p1"}, confidence="high",
                    reasoning="Joint DESeq2 fit on all 33 samples with subject block; three Wald contrasts; paper threshold applied with apply_threshold.")
    else:
        case.decide("execution", final={"method": "DESeq2 (pydeseq2) joint model ~ subject + time", "execution_error": exec_err},
                    evidence=[case.add_output(fpath, "counts_prefiltered")], execution_status="failed",
                    paper={"locator": "S2.14.p1"}, confidence="high", reasoning="Executor failed.")
    case.write_json("reproduction_summary.json", summary, role="reproduction_summary")
    case.write_json("reproduction_plan.json", {"route": "paper_aligned", "method": "DESeq2 ~ subject + time, all 33 samples",
                                               "contrasts": COMPARISONS, "threshold": PAPER_THRESHOLD,
                                               "audits": ["FDR<0.05 only", "raw p<0.05", "unblocked ~ time"]},
                    role="reproduction_plan")
    case.decide("enrichment",
                final={"method": "GO BP ORA on mirTarRnaSeq miRNA-mRNA interrelation genes (paper)", "gene_sets": "GO Biological Process",
                       "organism": "Human", "feature_id_type": "Ensembl gene" if cfg["accession"] == "GSE276889" else "miRBase mature miRNA",
                       "reason_not_run": ("paper's pathway analysis is on miRNA-mRNA interrelation gene lists from mirTarRnaSeq + miRanda "
                                          "(S2.15.p1); no repository executor for that, and the request asks for the DE effect")},
                evidence=outputs or [case.add_output(fpath, "counts_prefiltered")], execution_status="not_run",
                paper={"locator": "S2.15.p1"}, confidence="medium", reasoning="Planned per paper; not executable here.")
    if exec_err is None:
        case.decide("study", final={"route": "paper_aligned",
                                    "note": "DESeq2 on deposited counts with paper prefilter and threshold; formula not reported by paper, subject blocking added; unblocked fit as audit"},
                    evidence=outputs, paper={"locator": "S2.14.p1"}, confidence="high", reasoning="Paper route reproduced.")
        total = sum(v["paper_rule"]["n_significant"] for v in summary["contrasts"].values())
        case.finish(n_deg=total, deg_sanity=";".join(sorted({v["paper_rule"]["deg_sanity"] for v in summary["contrasts"].values()})))
    else:
        case.decide("study", final={"route": "paper_aligned"}, evidence=[paper] if paper else outputs or [{"id": "plan", "kind": "tool_output"}],
                    confidence="high", reasoning="Execution failed.")
        case.finish()
    print(case_id, json.dumps({n: {k: (v[k]["n_significant"] if isinstance(v.get(k), dict) and "n_significant" in v[k] else v.get(k))
                                   for k in v} for n, v in summary["contrasts"].items()}, default=str, indent=1))
print(run.finish())
