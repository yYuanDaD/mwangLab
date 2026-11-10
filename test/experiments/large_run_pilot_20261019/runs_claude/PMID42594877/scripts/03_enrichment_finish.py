"""Enrichment (Hallmark GSEA on planned contrasts), study record, reproduction files, finish."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42594877"
run = native.RunRecorder.open(RUN)
state = json.load(open(pathlib.Path(RUN) / "scripts" / "plan_state.json"))
overview = {}
disc = [
    {"item": "technical duplicates", "paper": "each plasma time point per individual run in duplicate (S9.3.18.p1)",
     "data": "one column per donor x time in both media-swap matrices", "disposition": "executable_without_change (unit = plasma donor x time; duplicates presumably merged before deposit)"},
    {"item": "3 h donor labels", "paper": "-", "data": "matrix uses donor numbers (X01_Pre); GEO title uses initials (1CB_Pre); description links them",
     "disposition": "executable_without_change (aligned via GEO description; number check passes)"},
    {"item": "gene annotation", "paper": "Salmon + Ensembl", "data": "3 h matrix has 32,673 genes, adipose and 12 h matrices ~59,700",
     "disposition": "executable_without_change"},
    {"item": "executor covariate dtype (tool bug)", "paper": "subject as a blocking factor",
     "data": "tools/deseq2_tools.py passes covariates with their CSV dtype; numeric subject IDs became a continuous covariate in a first attempt (adipose 1,105 DEGs; male subset 'Singular matrix')",
     "disposition": "worked around: subject labels prefixed with 's' (categorical); final adipose fit 2,819 DEGs"},
    {"item": "DESeq2 implementation", "paper": "R DESeq2 1.42.1/1.44.0", "data": "pydeseq2 0.5.4", "disposition": "executable_without_change"},
]
for cid, st in state.items():
    case = run.case(cid)
    dc = json.loads((case.dir / "results" / "deg_counts.json").read_text(encoding="utf-8"))
    units, reported = dc["units"], dc["paper_reported"]
    planned = [k for k in units if k in reported]
    outputs, summaries, errors = [], {}, {}
    fid = None
    for name in planned:
        u = units[name]
        if "path" not in u:
            errors[name] = "no completed DE table"
            continue
        fid = fid or native.feature_id_report(u["path"])
        od = case.dir / "results" / "enrichment" / name
        try:
            native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=u["path"], organism="Human",
                             ranking_metric="stat", top_n=10, output_dir=str(od))
            for f in native.find_outputs(od, "*GSEA_Hallmark*.csv"):
                it = case.add_output(f, f"gsea_{name}")
                outputs.append({"contrast": name, "kind": "GSEA", "path": str(f), "sha256": it.get("sha256")})
                tb = pd.read_csv(f)
                sig = tb[pd.to_numeric(tb["FDR q-val"], errors="coerce") < 0.05].sort_values("NES", ascending=False)
                summaries[name] = {"n_sets": int(len(tb)), "n_fdr_lt_0.05": int(len(sig)),
                                   "up": [f"{r.Term} ({r.NES:.2f})" for r in sig.itertuples() if r.NES > 0],
                                   "down": [f"{r.Term} ({r.NES:.2f})" for r in sig.itertuples() if r.NES < 0]}
        except native.NativeToolError as e:
            errors[name] = str(e)
    gs = case.write_json("results/enrichment/enrichment_summary.json",
                         {"summaries": summaries, "errors": errors, "feature_ids": fid}, role="enrichment_summary")
    print(cid, json.dumps(summaries, indent=1)[:2500], "ERRORS", errors)
    final = {"method": "GSEA preranked (gseapy.prerank) on the DESeq2 Wald statistic",
             "gene_sets": "MSigDB Hallmark h.all v2024.1.Hs", "organism": "Human",
             "feature_id_type": "ensembl_gene", "id_mapping": "Ensembl gene ID -> HGNC symbol via MyGene.info inside run_gsea_analysis",
             "contrasts": planned,
             "paper_enrichment": "clusterProfiler GSEA on GO BP (msigdbr) with the Wald statistic (S9.3.15.p1); Hallmark instead of GO BP is a declared deviation",
             "summaries": summaries, "outputs": outputs}
    if errors:
        final["execution_error"] = json.dumps(errors)
    case.decide("enrichment", final=final, evidence=[gs], paper={"locator": "S9.3.15.p1; FIG4E"}, confidence="medium",
                reasoning="Paper ranks genes by the DESeq2 Wald statistic for GSEA; same ranking, Hallmark sets available here.",
                execution_status="completed" if outputs else "failed", decision_status="valid")

    # ---------------- study
    def row(k):
        a = units[k].get("applied", {})
        return {"role": units[k].get("role"), "n_deg_applied": a.get("n_significant"), "up": a.get("n_up"),
                "down": a.get("n_down"), "paper_reported": reported.get(k), "error": units[k].get("execution_error")}
    summary = {k: row(k) for k in units}
    small = {k: v for k, v in units.items() if v.get("n_pairs") is not None and v["n_pairs"] < 3}
    final = {"route": "paper_aligned", "summary": summary,
             "exploratory_contrasts": [k for k in units if k not in reported],
             "exploratory_reason": ("not reported in the paper: " + ", ".join(k for k in units if k not in reported)
                                    + ("" if not small else "; fewer than 3 pairs: " + ", ".join(small))),
             "threshold": "padj < 0.05 (BH), no effect cutoff; paper S2.4.p2 / S2.4.p4"}
    case.decide("study", final=final, evidence=[gs],
                paper={"locator": "S2.4.p2; S2.4.p4"}, confidence="high",
                reasoning="Paper route (paired DESeq2 on deposited counts, FDR < 0.05) ran for every planned contrast.")
    case.write_json("reproduction_plan.json", {
        "paper_aligned": "DESeq2 ~ subject + time on deposited tximport counts, per experiment / intensity, padj < 0.05",
        "exploratory": final["exploratory_contrasts"],
        "enrichment": "Hallmark GSEA on Wald stat (deviation from GO BP clusterProfiler GSEA)"}, role="reproduction_plan")
    case.write_json("reproduction_summary.json", {"route": "paper_aligned", "counts": summary, "enrichment": summaries},
                    role="reproduction_summary")
    case.write_json("paper_data_discrepancies.json", disc, role="paper_data_discrepancies")
    main = planned[0]
    a = units[main].get("applied", {})
    case.finish(n_deg=a.get("n_significant"), deg_sanity=a.get("deg_sanity"))
    overview[cid] = summary

run.finish()
print(json.dumps(overview, indent=1))
