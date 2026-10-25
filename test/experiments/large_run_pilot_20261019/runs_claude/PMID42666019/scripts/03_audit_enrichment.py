"""Audit: paper-style pairwise DESeq2 refit for the two planned contrasts; then ORA (GO BP + KEGG) per planned contrast."""
import sys, pathlib; ROOT = next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists()); sys.path.insert(0, str(ROOT))
import os, json
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID42666019"
CASE = "PMID42666019"
run = native.RunRecorder.open(RUN)
case = run.case(CASE)
ALIGNED = str(case.dir / "aligned" / "aligned_matrix.csv")
DESIGN = str(case.dir / "aligned" / "design_metadata.csv")
al_mat = case.add_output(ALIGNED, "aligned_matrix")
al_meta = case.add_output(DESIGN, "design_metadata")
JOINT = case.dir / "results" / "deseq2_joint"
summary = {}

# ---- audit: two-group refits (the vendor route the paper most likely used)
for name, ctrl, trt in [("grp_CE_vs_SED", "SED", "CE"), ("grp_EE_vs_CE", "CE", "EE")]:
    out = case.dir / "results" / f"audit_pairwise_{name}"
    meta = pd.read_csv(DESIGN, index_col=0)
    sub = meta[meta.grp.isin([ctrl, trt])]
    sub_meta = out / "metadata_pair.csv"; out.mkdir(parents=True, exist_ok=True)
    sub.to_csv(sub_meta)
    mat = pd.read_csv(ALIGNED, index_col=0)[sub.index]
    sub_mat = out / "counts_pair.csv"; mat.to_csv(sub_mat)
    try:
        native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(sub_mat), metadata_csv=str(sub_meta),
                         design_column="grp", control_group=ctrl, treatment_group=trt, output_dir=str(out), alpha=0.05)
        deg = native.deg_outputs(str(out))[0]
        c = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=1.0, min_group_n=3)
        summary[f"audit_pairwise_{name}"] = c
        case.decide("execution",
                    final={"method": "DESeq2 (pydeseq2) two-group refit ~ grp on the 6 samples of the pair",
                           "subset": f"audit_pairwise_{name}", "role": "audit (paper's likely vendor route)",
                           "outputs": [deg], "threshold_counts": c},
                    evidence=[al_mat, al_meta, case.add_output(deg, f"audit_deg_{name}")], confidence="high",
                    execution_status="completed",
                    reasoning=f"Audit refit {name}: {c['n_significant']} DEGs ({c['n_up']} up / {c['n_down']} down) under {c['rule']}.")
    except native.NativeToolError as error:
        case.decide("execution", final={"method": "DESeq2 two-group refit", "subset": f"audit_pairwise_{name}",
                                        "execution_error": str(error)},
                    evidence=[al_mat, al_meta], confidence="high", execution_status="failed",
                    reasoning="audit refit failed")

# ---- enrichment: ORA GO BP/MF/CC + KEGG on the applied-threshold DEG list (paper: GO + KEGG, S2.16.p1)
for name in ["grp_CE_vs_SED", "grp_EE_vs_CE"]:
    src = JOINT / f"DEG_results_{name}.csv"
    t = pd.read_csv(src, index_col=0)
    t.index = t.index.str.replace(r"^(gene|rna)-", "", regex=True)
    t = t[~t.index.duplicated(keep="first")]
    sym = case.dir / "results" / "enrichment" / name / f"DEG_results_{name}_symbols.csv"
    sym.parent.mkdir(parents=True, exist_ok=True)
    t.to_csv(sym)
    idr = native.feature_id_report(sym)
    sym_ev = case.add_output(sym, f"deg_symbols_{name}")
    base = {"method": "ORA (Enrichr via gseapy) on |log2FC|>1 & padj<0.05 genes, both directions",
            "gene_sets": "GO_Biological_Process_2023, GO_Molecular_Function_2023, GO_Cellular_Component_2023, KEGG_2019_Mouse",
            "organism": "Mouse", "feature_id_type": "gene symbol (StringTie 'gene-'/'rna-' prefix stripped)",
            "input_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FC", "effect_cutoff": 1.0},
            "input_threshold_source": "applied", "subset": name, "feature_id_report": idr}
    try:
        native.call_tool("tools.enrichment_tools:run_enrichment_analysis", deg_csv=str(sym), organism="Mouse",
                         padj_cutoff=0.05, log2fc_cutoff=1.0, direction="all", top_n=10, output_dir=str(sym.parent))
        outs = sorted(str(p) for p in sym.parent.glob("*.csv") if p != sym)
        tops = {}
        for p in outs:
            e = pd.read_csv(p)
            col = next((c for c in ("Adjusted P-value", "padj") if c in e.columns), None)
            tops[pathlib.Path(p).name] = e.sort_values(col).head(5)["Term"].tolist() if col and "Term" in e.columns else []
        summary[f"ora_{name}"] = tops
        case.decide("enrichment", final={**base, "outputs": outs, "top_terms": tops},
                    evidence=[sym_ev] + [case.add_output(p, "ora_table") for p in outs], confidence="medium",
                    execution_status="completed",
                    reasoning=f"ORA on {name} DEGs (applied threshold); enrichment kept separate from the DE result.")
    except native.NativeToolError as error:
        case.decide("enrichment", final={**base, "execution_error": str(error)}, evidence=[sym_ev],
                    confidence="medium", execution_status="failed", reasoning="ORA failed (network or library)")
        summary[f"ora_{name}"] = str(error)
print(json.dumps(summary, indent=1, default=str))
