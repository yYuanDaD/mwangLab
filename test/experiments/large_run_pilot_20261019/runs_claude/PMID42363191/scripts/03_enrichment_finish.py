"""Raw-p audit, enrichment (GSEA Hallmark + ORA GO/KEGG), study record, finish."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42363191"
run = native.RunRecorder.open(RUN)
case = run.case("PMID42363191")
cdir = case.dir
dc = json.loads((cdir / "results" / "deg_counts.json").read_text(encoding="utf-8"))
exe = [d for d in json.loads((cdir / "decisions.json").read_text(encoding="utf-8")) if d["stage"] == "execution"][-1]
paths = {o["contrast"]: o["path"] for o in exe["final"]["outputs"]}
labels = {o["contrast"]: o["paper_label"] for o in exe["final"]["outputs"]}
EFF = math.log2(2.0)

# ---- audit: raw p < 0.05 & |log2FC| > 1 (hypothesis: paper's "q" was a raw p-value)
rawp = {}
for name, p in paths.items():
    r = native.apply_threshold(p, metric="pvalue", cutoff=0.05, effect_cutoff=EFF)
    rawp[name] = {"paper_label": labels[name], "n": r["n_significant"], "up": r.get("n_up"), "down": r.get("n_down")}
for lab, v in dc["pairwise_audit"].items():
    r = native.apply_threshold(v["path"], metric="pvalue", cutoff=0.05, effect_cutoff=EFF)
    rawp["pairwise_" + lab] = {"n": r["n_significant"], "up": r.get("n_up"), "down": r.get("n_down")}
audit_item = case.write_json("results/audit_rawp_counts.json",
                             {"rule": "AUDIT ONLY: raw pvalue < 0.05 and |log2FC| > 1 (not the paper's stated q-value rule)",
                              "paper_reported": {"T_vs_C": "486 (273 up, 213 down)", "TE_vs_T": "270 (165 up, 105 down)"},
                              "counts": rawp}, role="audit_rawp_counts")
print(json.dumps(rawp, indent=1))

# ---- enrichment on the planned contrasts + E vs C (exploratory)
enrich_names = [n for n, l in labels.items() if l] + ["ex_ex_vs_sed_tumor-no"]
fid = native.feature_id_report(paths[enrich_names[0]])
print(json.dumps(fid, default=str)[:600])
outputs, summaries, errors = [], {}, {}
for name in enrich_names:
    od = cdir / "results" / "enrichment" / name
    try:
        msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=str(paths[name]), organism="Mouse",
                               ranking_metric="stat", top_n=10, output_dir=str(od / "gsea"))
        for f in native.find_outputs(od / "gsea", "*GSEA_Hallmark*.csv"):
            it = case.add_output(f, f"gsea_{name}")
            outputs.append({"contrast": name, "kind": "GSEA", "path": str(f), "sha256": it.get("sha256")})
            tb = pd.read_csv(f)
            sig = tb[pd.to_numeric(tb["FDR q-val"], errors="coerce") < 0.05].sort_values("NES", ascending=False)
            summaries.setdefault(name, {})["gsea"] = {
                "n_sets": int(len(tb)), "n_fdr_lt_0.05": int(len(sig)),
                "up": [f"{r.Term} ({r.NES:.2f})" for r in sig.itertuples() if r.NES > 0],
                "down": [f"{r.Term} ({r.NES:.2f})" for r in sig.itertuples() if r.NES < 0]}
    except native.NativeToolError as e:
        errors[f"gsea_{name}"] = str(e)
    n_applied = dc["joint"][name]["applied"]["n_significant"]
    if n_applied >= 10:
        try:
            msg = native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=str(paths[name]),
                                   organism="Mouse", padj_cutoff=0.05, log2fc_cutoff=EFF, direction="all", top_n=10,
                                   output_dir=str(od / "ora"))
            ora = {}
            for f in native.find_outputs(od / "ora", "*.csv"):
                it = case.add_output(f, f"ora_{name}_{pathlib.Path(f).stem}")
                outputs.append({"contrast": name, "kind": "ORA", "path": str(f), "sha256": it.get("sha256")})
                tb = pd.read_csv(f)
                pcol = next((c for c in ("Adjusted P-value", "P-value") if c in tb.columns), None)
                if pcol:
                    ora[pathlib.Path(f).stem] = tb.sort_values(pcol)["Term"].head(5).tolist()
            summaries.setdefault(name, {})["ora_top_terms"] = ora
        except native.NativeToolError as e:
            errors[f"ora_{name}"] = str(e)
    else:
        summaries.setdefault(name, {})["ora"] = f"not run: only {n_applied} DEGs under the applied threshold"
gs = case.write_json("results/enrichment/enrichment_summary.json",
                     {"summaries": summaries, "errors": errors, "feature_ids": fid}, role="enrichment_summary")
print(json.dumps(summaries, indent=1)[:4000]); print("ERRORS", errors)
final = {"method": "GSEA preranked (gseapy.prerank, DESeq2 Wald stat) + ORA (Enrichr GO BP/MF/CC, KEGG) on applied DEG lists",
         "gene_sets": "MSigDB Hallmark mh.all v2024.1.Mm; Enrichr GO 2023 + KEGG 2019 Mouse",
         "organism": "Mouse", "feature_id_type": "gene_symbol", "contrasts": enrich_names,
         "input_threshold": {"metric": "qvalue", "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": EFF,
                             "inclusive": False}, "input_threshold_source": "applied",
         "paper_enrichment": "clusterProfiler GO/KEGG ORA (p<0.05) and GSEA software with GO sets (S2.7.p2, S2.8.p1); different libraries: declared deviation",
         "summaries": summaries, "outputs": outputs}
if errors:
    final["execution_error"] = json.dumps(errors)
case.decide("enrichment", final=final, evidence=[gs], paper={"locator": "S2.7.p2; S2.8.p1; S3.4.p2"}, confidence="medium",
            reasoning=("Paper runs GO/KEGG ORA on DEGs and GSEA. Repository runs Enrichr ORA and Hallmark GSEA; ORA skipped "
                       "when fewer than 10 DEGs (TE vs T)."),
            execution_status="completed" if outputs else "failed", decision_status="valid")

# ---- study
j = dc["joint"]
case.decide("study",
            final={"route": "paper_aligned",
                   "summary": {n: {"paper_label": v["paper_label"], "role": v["role"],
                                   "n_deg_applied": v["applied"]["n_significant"], "up": v["applied"].get("n_up"),
                                   "down": v["applied"].get("n_down"), "paper_reported": v["paper_reported"]} for n, v in j.items()},
                   "exploratory_contrasts": [n for n, v in j.items() if v["role"] == "exploratory"],
                   "exploratory_reason": "E vs C, TE vs E and the tumor x exercise interaction are not reported in the paper",
                   "discrepancy": ("Paper TE vs T = 270 DEGs, here 4 (joint) / 6 (pairwise) under q<0.05 & |log2FC|>1; "
                                   "T vs C 486 vs 106/124. Raw p<0.05 & |log2FC|>1 gives 464/296 (joint), close to "
                                   "the paper's 486/270: the paper's counts look like raw-p counts (audit only). The TE vs T exercise "
                                   "effect is weak at FDR level (PCA: no clear T/TE separation; TSA4 outlier)."),
                   "audits": ["results/audit_rawp_counts.json", "pairwise DESeq2 fits (deg_counts.json)"]},
            evidence=[audit_item, gs], paper={"locator": "S3.3.p3"}, confidence="medium",
            reasoning="Paper route (DESeq2 on deposited counts, paper threshold) ran; counts differ from the paper, documented.")
case.write_json("paper_data_discrepancies.json", [
    {"item": "DEG counts", "paper": "T vs C 486, TE vs T 270 at q<0.05 & FC>2/<0.5",
     "data": "joint DESeq2 106 / 4; pairwise 124 / 6 at padj<0.05 & |log2FC|>1; raw p<0.05 gives 464 / 296",
     "disposition": "executable_without_change; reported as non-reproduction, likely raw-p threshold in paper"},
    {"item": "PCA separation", "paper": "T and TE clearly separated (S3.3.p2)",
     "data": "log2CPM PCA (top 2000 genes) shows no clean T/TE split; TSA4 deviates", "disposition": "executable_without_change"},
    {"item": "DESeq2 implementation", "paper": "R DESeq2 (version not reported)", "data": "pydeseq2 0.5.4",
     "disposition": "executable_without_change"}], role="paper_data_discrepancies")
case.write_json("reproduction_plan.json", {
    "paper_aligned": "DESeq2 on HTSeq raw counts, 16 samples, one model ~ cell (C/E/T/TE), Wald contrasts T vs C and TE vs T, padj<0.05 & |log2FC|>1",
    "exploratory": ["E vs C", "TE vs E", "tumor x exercise interaction"],
    "audits": ["padj<0.05 only", "pairwise two-group DESeq2 fits", "raw p<0.05 & |log2FC|>1"],
    "enrichment": "Hallmark GSEA + Enrichr GO/KEGG ORA (deviation from clusterProfiler/GO GSEA)"}, role="reproduction_plan")
case.write_json("reproduction_summary.json", {"route": "paper_aligned", "counts": j, "rawp_audit": rawp,
                                              "enrichment": summaries}, role="reproduction_summary")
case.finish(n_deg=j["ex_ex_vs_sed_tumor-yes"]["applied"]["n_significant"],
            deg_sanity=j["ex_ex_vs_sed_tumor-yes"]["applied"].get("deg_sanity"))
run.finish()
print("done")
