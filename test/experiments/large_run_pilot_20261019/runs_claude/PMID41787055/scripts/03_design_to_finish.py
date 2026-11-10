import sys, pathlib, json, math; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID41787055"
run = native.RunRecorder.open(RUN); case = run.case("GSE293221")
paper = case.evidence_item("paper:PMC13076624.paper.md")
meta = case.evidence_item("metadata:GSE293221_metadata.csv")
adir = case.dir / "aligned"
MAT = str(adir / "aligned_matrix.csv"); DM = str(adir / "design_metadata.csv")
mat_item = case.add_output(MAT, "aligned_matrix"); dm_item = case.add_output(DM, "design_metadata")
dm = pd.read_csv(DM, index_col=0)
EFF = math.log2(1.5)

# ---------- design
planned = ["grp_EX_vs_CON", "grp_PHAM_vs_CON"]
rep, s_item, summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["grp"], matrix_csv=MAT,
                                       organism="Mouse", subject=None, references={"grp": "CON"}, planned=planned)
print(json.dumps(summary, default=str), [(c["name"], c["analyzable"]) for c in rep["comparisons"]])
contrasts = [
    {"name": "grp_EX_vs_CON", "control": "CON", "treatment": "EX", "role": "primary (request + S2.2.p1)", "route": "paper_aligned (pairwise, as paper)"},
    {"name": "grp_PHAM_vs_CON", "control": "CON", "treatment": "PHAM", "role": "paper's second planned contrast (S2.2.p2); not an exercise effect", "route": "paper_aligned (pairwise, as paper)"},
    {"name": "grp_PHAM_vs_EX", "control": "EX", "treatment": "PHAM", "role": "exploratory, not in paper", "route": "exploratory (joint model only)"},
]
case.decide("design", final={"analysis_type": "one factor, three levels (control reference); paper ran group-pairwise two-arm tests",
    "design_column": "grp", "levels": {"CON": 3, "EX": 3, "PHAM": 3}, "control": "CON", "treatment": "EX",
    "contrasts": contrasts, "estimand_type": "causal (randomized, S4.2.p1)",
    "suitability": summary, "sex_check": "all 9 predicted male from X/Y genes; paper: male TRAMP mice",
    "sensitivity": "all three comparisons also extracted from one DESeq2 model ~ grp on all 9 samples (tools.joint_contrasts), labelled sensitivity/exploratory"},
    evidence=[paper, meta, dm_item, s_item], paper={"locator": "S2.2.p1"}, confidence="high",
    candidates=[{"value": "pool PHAM with CON as 'non-exercise'", "reason_rejected": "pools a distinct active intervention; paper compares each arm to control"},
                {"value": "only joint 3-group model for planned contrasts", "reason_rejected": "paper states group-pairwise DESeq tests (S4.7.p1); joint model kept as sensitivity"}],
    reasoning="Randomized 3-arm design (S4.2.p1); the request is the exercise effect, which the paper estimates as exercise vs control (S2.2.p1). PhAm vs control is the paper's other planned contrast. Suitability: analyzable, 3 per arm, all male.")

# ---------- covariance
dc = native.design_check(dm, ["grp"])
conf = native.confounding_report(dm, "grp", candidates=["description"])
print("design_check", json.dumps(dc, default=str)[:800])
case.decide("covariance", final={"status": "not_required", "blocking_terms": [], "covariates": [
        {"name": "housing (single with wheel vs group housed)", "disposition": "excluded: inseparable component of the paper's exercise arm (S4.2.p1, S4.3.p1), not a recorded metadata column; interpretation caveat"},
        {"name": "description (library name)", "disposition": "excluded: unique per sample, identifier only"},
        {"name": "batch / sequencing run", "disposition": "excluded: not reported in paper or GEO"},
        {"name": "sex", "disposition": "excluded: single level (male)"}],
    "design_check": dc, "confounding": conf},
    evidence=[dm_item, meta, paper], paper={"locator": "S4.2.p1"}, confidence="high",
    reasoning="Independent animals, one tumor each, randomized; no batch, subject, or pairing structure recorded. Single housing of the exercise mice is part of the intervention and cannot be separated.")

# ---------- method
case.decide("method", final={"method": "DESeq2 (pydeseq2 Wald test), two-arm fits per planned contrast", "matrix_type": "raw counts",
    "formula": "~ grp (two arms per fit); sensitivity: ~ grp on all 9 samples", "alpha": 0.05,
    "paper_route": {"method": "R DESeq (original package), group-pairwise, after mean RPKM > 1 filter", "status": "blocked",
                    "reason": "original DESeq is not installed (pydeseq2 implements DESeq2); RPKM filter needs gene lengths for the mm9 annotation, which are not deposited"},
    "deviations": ["DESeq2 dispersion shrinkage and Wald test instead of DESeq negative-binomial exact test", "RPKM > 1 pre-filter not applied; DESeq2 independent filtering only"]},
    evidence=[mat_item, paper], paper={"locator": "S4.7.p1"}, confidence="medium",
    reasoning="Raw HTSeq counts support the DESeq family. The closest available executor is DESeq2 two-arm, matching the paper's pairwise approach.")

# ---------- threshold
pt = {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": EFF,
      "effect_cutoff_original": "fold change > 1.5 (either way)", "inclusive": False,
      "expression_filter": "mean RPKM > 1 in at least one group", "source_locator": "S4.7.p1"}
applied = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": EFF, "inclusive": False}
case.decide("threshold", final={"paper_threshold": pt, "threshold_source": "paper_on_deviation_route", "applied_threshold": applied,
    "deviation_note": "paper FDR method not named (BH applied by executor); RPKM > 1 pre-filter not applied (no gene lengths)",
    "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None, "label": "audit: BH padj < 0.05 without fold-change rule"}},
    evidence=[paper], paper={"locator": "S4.7.p1"}, confidence="high",
    reasoning="S4.7.p1: FDR < 0.05 and fold change > 1.5 either way; log2(1.5) = 0.5849625.")

# ---------- execution
res = case.dir / "results"
counts = {}
units = [("grp_EX_vs_CON", "CON", "EX"), ("grp_PHAM_vs_CON", "CON", "PHAM")]
for name, ctrl, trt in units:
    od = res / name
    try:
        msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=MAT, metadata_csv=DM, design_column="grp",
                               control_group=ctrl, treatment_group=trt, output_dir=str(od), alpha=0.05)
        deg = native.deg_outputs(od)[0]
        c = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=EFF, min_group_n=3)
        a = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None, min_group_n=3)
        counts[name] = {"applied": c, "audit": a, "deg_csv": deg}
        it = case.add_output(deg, f"deg_{name}")
        case.decide("execution", final={"method": "DESeq2 (pydeseq2) two-arm", "subset": name, "formula": "~ grp", "outputs": [deg],
            "n_samples": 6, "applied_counts": c, "audit_counts": a}, evidence=[mat_item, dm_item, it], confidence="high",
            execution_status="completed", reasoning=f"{trt} vs {ctrl}: {c['n_significant']} genes ({c['n_up']} up, {c['n_down']} down) under {c['rule']}.")
        print(name, c, a["n_significant"])
    except native.NativeToolError as e:
        counts[name] = {"error": str(e)}
        case.decide("execution", final={"method": "DESeq2 (pydeseq2) two-arm", "subset": name, "execution_error": str(e)},
                    evidence=[mat_item, dm_item], confidence="high", execution_status="failed", reasoning="executor failed")
        print("ERR", name, e)

# sensitivity: joint model on all 9 samples
jd = res / "joint_all9"
try:
    comps = [c for c in rep["comparisons"]]
    j = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=MAT, metadata_csv=DM, comparisons=comps, output_dir=str(jd))
    jc = {}
    for r in j["results"]:
        c = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=EFF, min_group_n=3)
        jc[r["name"]] = c
        case.add_output(r["path"], f"deg_joint_{r['name']}")
    counts["joint"] = jc
    case.decide("execution", final={"method": "DESeq2 joint model (pydeseq2), sensitivity", "subset": "joint_all9 (all three comparisons)",
        "formula": j["formula"].replace("cell", "grp"), "outputs": [r["path"] for r in j["results"]], "applied_counts": jc, "role": "sensitivity / exploratory"},
        evidence=[mat_item, dm_item], confidence="high", execution_status="completed",
        reasoning="One dispersion fit on all 9 samples; " + "; ".join(f"{k}: {v['n_significant']}" for k, v in jc.items()))
    print("joint", {k: (v["n_significant"], v["n_up"], v["n_down"]) for k, v in jc.items()})
except native.NativeToolError as e:
    case.decide("execution", final={"method": "DESeq2 joint model (pydeseq2), sensitivity", "subset": "joint_all9", "execution_error": str(e)},
                evidence=[mat_item, dm_item], confidence="high", execution_status="failed", reasoning="executor failed")
    print("ERR joint", e)

# paper top-gene check (S2.2.p1, S2.2.p3)
ex = pd.read_csv(counts["grp_EX_vs_CON"]["deg_csv"], index_col=0)
ph = pd.read_csv(counts["grp_PHAM_vs_CON"]["deg_csv"], index_col=0)
genes_ex = ["Lipe", "Plin1", "Slc7a10", "Dgat2l6", "Lman1l", "BB123696", "Bb123696"]
genes_ph = ["Spink3", "Spink5", "Slc26a4", "Slc45a3", "Slc5a8", "Dcx", "Sncb", "Lman1l", "BB123696"]
look = {"EX_vs_CON": ex.reindex([g for g in genes_ex if g in ex.index])[["baseMean", "log2FoldChange", "padj"]].round(4).to_dict("index"),
        "PHAM_vs_CON": ph.reindex([g for g in genes_ph if g in ph.index])[["baseMean", "log2FoldChange", "padj"]].round(4).to_dict("index")}
print(json.dumps(look, default=str))
sig = lambda t: set(t.index[(t["padj"] < 0.05) & (t["log2FoldChange"].abs() > EFF)])
overlap = sorted(sig(ex) & sig(ph))
print("overlap", overlap)

# ---------- enrichment (paper ran GO + gene-set enrichment on DEGs, FIG3C-D)
deg_ex = counts["grp_EX_vs_CON"]["deg_csv"]
fid = native.feature_id_report(deg_ex)
print("fid", json.dumps(fid, default=str)[:400])
ed = res / "enrichment_EX_vs_CON"
try:
    msg = native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=deg_ex, organism="Mouse", padj_cutoff=0.05,
                           log2fc_cutoff=EFF, direction="all", output_dir=str(ed / "ora"))
    outs = [str(p) for p in sorted((ed / "ora").rglob("*.csv"))]
    case.decide("enrichment", final={"method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG_2019_Mouse (Enrichr)",
        "organism": "Mouse", "feature_id_type": "gene_symbol", "subset": "grp_EX_vs_CON",
        "input_threshold": applied, "input_threshold_source": "applied", "outputs": outs, "summary": str(msg)[:1500]},
        evidence=[case.add_output(deg_ex, "deg_for_enrichment")], confidence="high", execution_status="completed",
        reasoning="Paper reports GO for exercise DEGs (FIG3C); ORA on the applied-threshold list.")
    print(str(msg)[:1500])
except native.NativeToolError as e:
    case.decide("enrichment", final={"method": "ORA (Enrichr GO BP/MF/CC + KEGG)", "gene_sets": "GO 2023 + KEGG (Enrichr)", "organism": "Mouse",
        "feature_id_type": "gene_symbol", "subset": "grp_EX_vs_CON", "input_threshold": applied, "input_threshold_source": "applied", "execution_error": str(e)},
        evidence=[mat_item], confidence="high", execution_status="failed", reasoning="enrichment failed")
    print("ERR ora", e)
try:
    msg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=deg_ex, organism="Mouse", ranking_metric="stat", output_dir=str(ed / "gsea"))
    outs = [str(p) for p in sorted((ed / "gsea").rglob("*.csv"))]
    case.decide("enrichment", final={"method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB mouse Hallmark mh.all 2024.1.Mm", "organism": "Mouse",
        "feature_id_type": "gene_symbol", "ranking_metric": "stat", "subset": "grp_EX_vs_CON", "outputs": outs, "summary": str(msg)[:1500]},
        evidence=[case.evidence_item("tool_output:" + pathlib.Path(deg_ex).name) if False else mat_item], confidence="high", execution_status="completed",
        reasoning="Paper shows gene-set enrichment for exercise (FIG3D); Hallmark GSEA on the full Wald-stat ranking.")
    print(str(msg)[:1500])
except native.NativeToolError as e:
    case.decide("enrichment", final={"method": "GSEA preranked (gseapy prerank)", "gene_sets": "MSigDB mouse Hallmark", "organism": "Mouse",
        "feature_id_type": "gene_symbol", "subset": "grp_EX_vs_CON", "execution_error": str(e)},
        evidence=[mat_item], confidence="high", execution_status="failed", reasoning="GSEA failed")
    print("ERR gsea", e)

# ---------- study
exn = counts["grp_EX_vs_CON"]["applied"]
case.decide("study", final={"route": "declared_deviation",
    "deviation": "DESeq2 (pydeseq2) instead of original DESeq; RPKM > 1 filter not applied",
    "results": {k: {"n_deg": v["applied"]["n_significant"], "up": v["applied"]["n_up"], "down": v["applied"]["n_down"], "audit_padj_only": v["audit"]["n_significant"]} for k, v in counts.items() if k in ("grp_EX_vs_CON", "grp_PHAM_vs_CON")},
    "joint_sensitivity": {k: v["n_significant"] for k, v in counts.get("joint", {}).items()},
    "paper_counts": {"grp_EX_vs_CON": 32, "grp_PHAM_vs_CON": 176}, "paper_gene_check": look, "overlap_EX_PHAM": overlap,
    "caveat": "exercise mice were singly housed; housing cannot be separated from wheel running"},
    evidence=[paper, mat_item], paper={"locator": "S2.2.p1"}, confidence="medium", execution_status="completed",
    reasoning="Planned paper contrasts ran on the closest available executor with the paper threshold.")
case.write_json("reproduction_plan.json", {"paper_route": "DESeq group-pairwise on HTSeq counts, RPKM>1, FDR<0.05, FC>1.5",
    "executed_route": "pydeseq2 two-arm per contrast, padj<0.05 & |log2FC|>log2(1.5); joint ~grp sensitivity", "status": "declared_deviation"})
case.write_json("reproduction_summary.json", {"counts": {k: v for k, v in counts.items()}, "paper_counts": {"grp_EX_vs_CON": 32, "grp_PHAM_vs_CON": 176},
    "paper_gene_check": look, "overlap": overlap})
print(case.finish(n_deg=exn["n_significant"], deg_sanity=exn["deg_sanity"]))
print(run.finish())
