"""Gates 5-11 (design ... study) for GSE283493 / PMID 39832562."""
import sys, pathlib; ROOT = pathlib.Path(__file__).resolve().parents[6]; sys.path.insert(0, str(ROOT))  # repository root
import os, json, math
os.chdir(ROOT)
import pandas as pd
from tools import native

native.enable_native_mode()
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID39832562"
run = native.RunRecorder.open(RUN)
OUTLIERS = ["SAT_PM_Exp_d", "SAT_PM_Exp_f", "VAT_AM_Cont_e", "VAT_AM_Exp_c"]
WALD = {
    "sat_ea": dict(tissue="SAT", phase="EA", ctrl="EAC", trt="EAE", n_paper=7),
    "sat_la": dict(tissue="SAT", phase="LA", ctrl="LAC", trt="LAE", n_paper=353),
    "vat_ea": dict(tissue="VAT", phase="EA", ctrl="EAC", trt="EAE", n_paper=2),
    "vat_la": dict(tissue="VAT", phase="LA", ctrl="LAC", trt="LAE", n_paper=14),
}
PAPER_THR = {"metric": "padj", "adjustment": "not_reported (DESeq2 default BH assumed by executor)", "cutoff": 0.1,
             "effect_metric": "log2FC", "effect_estimator": "apeglm-shrunken log2 fold change",
             "effect_cutoff": 0.5, "inclusive": False, "source_locator": "S2.9.p2; S3.p1"}
APPLIED_THR = {"metric": "padj", "adjustment": "BH (pydeseq2 default, with independent filtering)", "cutoff": 0.1,
               "effect_metric": "log2FC", "effect_estimator": "unshrunken MLE log2 fold change",
               "effect_cutoff": 0.5, "inclusive": False}
results = {}

# Rat Ensembl -> rat symbol mapping (MyGene.info), used only for enrichment and named-gene checks.
from tools.enrichment_tools import _query_symbols
aligned0 = pd.read_csv(run.run_dir / "sat_ea" / "aligned" / "aligned_matrix.csv", index_col=0)
ens = [i.split(".")[0] for i in aligned0.index.astype(str)]
sym = _query_symbols(ens, "rat")
map_path = run.run_dir / "shared_rat_ensembl_to_symbol.csv"
pd.DataFrame({"symbol": pd.Series(sym)}).rename_axis("ensembl_gene").to_csv(map_path)
print(f"rat symbols mapped: {len(sym)}/{len(ens)}")

for cid, spec in WALD.items():
    case = run.case(cid)
    paper = case.evidence_item("paper:PMC11810837.paper.json")
    dm_path = case.dir / "aligned" / "design_metadata.csv"
    dm = pd.read_csv(dm_path, index_col=0)
    dm_ev = case.evidence_item("tool_output:design_metadata.csv")
    in_cell = dm[(dm.tissue == spec["tissue"]) & (dm.phase == spec["phase"])]
    excluded = in_cell[in_cell.library.isin(OUTLIERS)]
    keep = in_cell[~in_cell.library.isin(OUTLIERS)]
    sub_path = case.dir / "aligned" / "case_metadata.csv"
    keep.to_csv(sub_path)
    sub_ev = case.add_output(sub_path, "case_metadata_subset")
    n_by_arm = keep.training.value_counts().to_dict()
    design_chk = native.design_check(sub_path, ["training"])
    conf = native.confounding_report(sub_path, "training", candidates=["rep_letter", "libphase", "tissue", "phase"])

    case.decide("design", final={
        "analysis_type": "two_group", "design_column": "training", "control": "ctrl", "treatment": "ex",
        "contrast_label": f"{spec['tissue']}_{spec['phase']}: {spec['trt']} vs {spec['ctrl']}",
        "samples": keep.index.tolist(), "n_per_arm": n_by_arm,
        "excluded_samples": [{"sample": s, "library": l, "reason": "paper-stated outlier (higher number of expressed genes, S2.9.p2); identified by n genes > 10 counts"}
                             for s, l in zip(excluded.index, excluded.library)],
        "derived_column_source": "training from characteristics_ch1.2.group (control->ctrl, exercise->ex)",
    }, evidence=[paper, dm_ev, sub_ev], paper={"locator": "S2.9.p2"}, confidence="high",
        candidates=[
            {"value": "pool EA and LA phases (exercise vs control)", "reason_rejected": "paper tests exercise separately per phase; pooling mixes two estimands"},
            {"value": "one model across tissues with tissue term", "reason_rejected": "paper Wald tests are per tissue; SAT and VAT share rats with no animal ID to block"},
            {"value": "grp (EAE vs LAE) phase contrast", "reason_rejected": "time-of-day comparison, not the exercise effect"}],
        reasoning=(f"S2.9.p2: Wald test of exercise vs control within each tissue and time-of-day. Subset = {spec['tissue']} x {spec['phase']}, "
                   f"{len(excluded)} paper outlier(s) removed, arms {n_by_arm}. Different rats per arm (S2.1.p1)."))

    case.decide("covariance", final={
        "status": "not_required", "blocking_terms": [],
        "covariates": [
            {"name": "surrogate_variables_1_2", "disposition": "excluded: paper adds 2 sva SVs; no sva executor in the repository (declared deviation)"},
            {"name": "rep_letter", "disposition": "excluded: library replicate letter, not an animal ID; arms contain different rats"},
            {"name": "tissue", "disposition": "excluded: constant within this subset"},
            {"name": "phase", "disposition": "excluded: constant within this subset"},
            {"name": "cage", "disposition": "excluded: 3 rats per cage (S2.1.p1) but cage IDs are not deposited"}],
        "design_check": design_chk, "confounding_report": conf,
    }, evidence=[sub_ev, paper], paper={"locator": "S2.9.p2"}, confidence="medium",
        reasoning=("Each rat contributes one sample to this tissue-by-phase contrast, so there is no repeated-measure key to block. "
                   f"Design ~ training is full rank, residual df {design_chk['residual_df']}. The paper's 2 SVs cannot be estimated with "
                   "available executors; recorded as a deviation. Confidence medium because the SV adjustment is missing."))

    case.decide("method", final={
        "method": "DESeq2 Wald test (pydeseq2), ~ training, no SVs, no LFC shrinkage",
        "matrix_type": "raw counts", "formula": "~ training",
        "gene_filter": "keep genes with >= 10 reads in >= 6 of the 44 retained libraries (paper rule S2.9.p2, applied to all retained samples before subsetting)",
        "paper_route": {"method": "DESeq2 Wald, ~ SV1 + SV2 + training, apeglm lfcShrink", "status": "blocked",
                        "reason": "no sva executor and run_deseq2_analysis has no lfcShrink/apeglm (tools/deseq2_tools.py:136-152)"},
    }, evidence=[case.evidence_item("tool_output:matrix_profile.json"), paper], paper={"locator": "S2.9.p2"}, confidence="high",
        reasoning="Raw integer counts support DESeq2, the paper's method. The SV terms and apeglm shrinkage cannot run here, so DESeq2 without them is a declared deviation.")

    case.decide("threshold", final={
        "paper_threshold": PAPER_THR, "threshold_source": "paper_on_deviation_route", "applied_threshold": APPLIED_THR,
        "deviation_note": ("Same numeric rule (padj < 0.1 and |log2FC| > 0.5) but the effect size is the unshrunken MLE log2FC because "
                           "the executor has no apeglm shrinkage; the paper filtered on apeglm-shrunken LFC, so counts here are expected to be >= the paper's."),
    }, evidence=[paper], paper={"locator": "S2.9.p2"}, confidence="high",
        reasoning="S2.9.p2 and S3.p1 state padj < 0.1 and absolute shrunken log2FC > 0.5 for the Wald test.")

    # ---------------- execution
    res_dir = case.dir / "results"
    res_dir.mkdir(parents=True, exist_ok=True)
    full = pd.read_csv(case.dir / "aligned" / "aligned_matrix.csv", index_col=0)
    retained = dm.index[~dm.library.isin(OUTLIERS)]
    keep_genes = (full[retained] >= 10).sum(axis=1) >= 6
    filt = full.loc[keep_genes, keep.index]
    filt_path = res_dir / "counts_filtered_case.csv"
    filt.to_csv(filt_path)
    filt_ev = case.add_output(filt_path, "filtered_counts")
    try:
        msg = native.call_tool("tools.deseq2_tools:run_deseq2_analysis", counts_csv=str(filt_path), metadata_csv=str(sub_path),
                               design_column="training", control_group="ctrl", treatment_group="ex", output_dir=str(res_dir))
        deg = native.deg_outputs(str(res_dir))[0]
        deg_ev = case.add_output(deg, "deg_table")
        thr = native.apply_threshold(deg, metric="padj", cutoff=0.1, effect_cutoff=0.5,
                                     min_group_n=min(n_by_arm.values()))
        audit_padj = native.apply_threshold(deg, metric="padj", cutoff=0.1)
        audit_p = native.apply_threshold(deg, metric="pvalue", cutoff=0.05, effect_cutoff=0.5)
        case.decide("execution", final={
            "method": "DESeq2 (pydeseq2) Wald, ~ training", "outputs": [deg], "n_genes_after_filter": int(keep_genes.sum()),
            "n_samples": int(len(keep)), "threshold_counts": thr,
            "audit_counts": {"padj<0.1_no_effect_cutoff": audit_padj, "raw_p<0.05_and_|LFC|>0.5 (paper FIG2/FIG3 colouring rule)": audit_p},
            "tool_message": msg[:600],
        }, evidence=[filt_ev, sub_ev, deg_ev], paper={"locator": "S2.9.p2"}, confidence="high",
            execution_status="completed", reasoning="Executor completed on the approved subset and filtered counts.")
        results[cid] = dict(spec, deg=deg, thr=thr, audit_padj=audit_padj, audit_p=audit_p, n=n_by_arm, n_genes=int(keep_genes.sum()))
    except native.NativeToolError as e:
        case.decide("execution", final={"method": "DESeq2 (pydeseq2) Wald, ~ training", "execution_error": str(e)},
                    evidence=[filt_ev, sub_ev], confidence="high", execution_status="failed",
                    reasoning="Executor failed; plan remains valid.")
        results[cid] = dict(spec, error=str(e))

    # ---------------- enrichment (paper ran GSEA, S2.9.p2 / FIG1 H)
    if "deg" in results[cid]:
        deg = results[cid]["deg"]
        idrep = native.feature_id_report(deg)
        tab = pd.read_csv(deg, index_col=0)
        tab.index = [i.split(".")[0] for i in tab.index.astype(str)]
        tab_path = res_dir / "deg_for_mapping.csv"
        tab.to_csv(tab_path)
        coll = native.collapse_to_genes(tab_path, res_dir / "deg_rat_symbols.csv", mapping_csv=str(map_path),
                                        mapping_column="symbol", rule="max_mean")
        coll_ev = case.add_output(coll["output"], "deg_collapsed_to_rat_symbol")
        gsea_dir = res_dir / "gsea"
        enr_final = {"method": "GSEA preranked (gseapy prerank, 1000 permutations, seed 42)",
                     "gene_sets": "MSigDB mouse Hallmark mh.all 2024.1.Mm", "organism": "Rat",
                     "feature_id_type": idrep["dominant_type"], "ranking_metric": "stat (DESeq2 Wald statistic)",
                     "id_mapping": {"ensembl_to_rat_symbol": "MyGene.info querymany scopes=ensembl.gene species=rat",
                                    "mapping_file": str(map_path), **coll["mapping_record"],
                                    "n_features": coll["n_features"], "n_unmapped": coll["n_unmapped"], "n_genes": coll["n_genes"]},
                     "ortholog_mapping": {"rule": "rat (RGD) symbol used as the mouse (MGI) symbol by identity; no ortholog table",
                                          "limitation": "rat-specific or differently named genes are lost; one-to-many orthologs ignored"},
                     "paper_route": {"method": "fgsea on apeglm-shrunken log2FC against KEGG", "status": "blocked",
                                     "reason": "no shrinkage and repository gene sets are MSigDB Hallmark (Mouse/Human)"}}
        try:
            gmsg = native.call_tool("tools.enrichment_tools:run_gsea_analysis", deg_csv=coll["output"], organism="Mouse",
                                    ranking_metric="stat", output_dir=str(gsea_dir))
            gout = native.find_outputs(str(gsea_dir), "*_GSEA_Hallmark.csv")
            g = pd.read_csv(gout[0])
            top = g.sort_values("FDR q-val").head(8)[["Term", "NES", "NOM p-val", "FDR q-val"]].to_dict("records")
            enr_final.update(outputs=gout, n_sets_fdr_lt_0_25=int((g["FDR q-val"] < 0.25).sum()),
                             n_sets_fdr_lt_0_1=int((g["FDR q-val"] < 0.1).sum()), top_by_fdr=top)
            for o in gout:
                case.add_output(o, "gsea_hallmark")
            case.decide("enrichment", final=enr_final, evidence=[coll_ev], paper={"locator": "S2.9.p2"}, confidence="medium",
                        execution_status="completed", reasoning="Paper reports GSEA (FIG1 H); run as declared deviation on Hallmark with Wald-stat ranking.")
            results[cid]["gsea"] = top
            results[cid]["gsea_n"] = enr_final["n_sets_fdr_lt_0_1"]
        except native.NativeToolError as e:
            enr_final["execution_error"] = str(e)
            case.decide("enrichment", final=enr_final, evidence=[coll_ev], confidence="medium",
                        execution_status="failed", reasoning="GSEA failed; DE result unaffected.")
            results[cid]["gsea_error"] = str(e)

        # named-gene direction check against FIG2/FIG3 claims
        sym_tab = pd.read_csv(coll["output"], index_col=0)
        named = ["Hmgcr", "Hmgcs1", "Sqle", "Ldlr", "Fasn", "Dgat2", "Gpd1", "Fabp4", "Cpt1a", "Pkm", "Ldha", "Hk2", "Slc2a4", "Mdh1", "Acly"]
        results[cid]["named"] = {g: (round(float(sym_tab.loc[g, "log2FoldChange"]), 3), float(f"{sym_tab.loc[g, 'pvalue']:.3g}"))
                                 for g in named if g in sym_tab.index}

    route = "declared_deviation"
    small = min(n_by_arm.values()) < 3
    case.decide("study", final={"route": route, "exploratory": small,
                                "exploratory_reason": None if not small else "an arm has < 3 replicates",
                                "deviations": ["no surrogate variables", "no apeglm shrinkage (threshold on MLE log2FC)",
                                               "outlier identities inferred from the paper's stated criterion"]},
                evidence=[paper], paper={"locator": "S2.9.p2"}, confidence="high",
                execution_status=("completed" if "deg" in results[cid] else "failed"),
                reasoning="Paper's Wald contrast reproduced on DESeq2 without SVs or shrinkage.")
    r = results[cid]
    case.write_json("reproduction_plan.json", {
        "paper_route": "DESeq2 Wald ~ SV1 + SV2 + training, apeglm, padj<0.1 & |shrunken LFC|>0.5, after removing outliers and filtering (>=10 reads in >=6 samples)",
        "executed_route": "pydeseq2 Wald ~ training, unshrunken LFC, same thresholds, same outlier removal and gene filter",
        "declared_deviations": ["no SVs", "no apeglm", "Hallmark GSEA (Wald stat) instead of KEGG fgsea (shrunken LFC)"]}, role="reproduction_plan")
    case.write_json("reproduction_summary.json", {k: v for k, v in r.items() if k != "deg"} | {
        "paper_reported_deg": spec["n_paper"], "threshold_used": APPLIED_THR, "threshold_source": "paper_on_deviation_route"},
        role="reproduction_summary")
    thr = r.get("thr")
    case.finish(n_deg=thr["n_significant"] if thr else None, deg_sanity=thr["deg_sanity"] if thr else None)

# ---------------------------------------------------------------- interaction case (stops at covariance)
case = run.case("interaction_lrt")
paper = case.evidence_item("paper:PMC11810837.paper.json")
dm_path = case.dir / "aligned" / "design_metadata.csv"
dm = pd.read_csv(dm_path, index_col=0)
keep = dm[~dm.library.isin(OUTLIERS)]
sub_path = case.dir / "aligned" / "case_metadata.csv"
keep.to_csv(sub_path)
sub_ev = case.add_output(sub_path, "case_metadata_subset")
dchk = native.design_check(sub_path, ["tissue", "phase", "training"], interactions=[("phase", "training")])
case.decide("design", final={
    "analysis_type": "factorial", "formula": "~ tissue + phase + training + phase:training",
    "contrasts": [{"name": "phase:training interaction", "coefficient": "phase[T.LA]:training[T.ex]", "test": "LRT vs ~ tissue + phase + training (paper)"}],
    "design_check": dchk, "n_samples": int(len(keep)),
}, evidence=[paper, sub_ev], paper={"locator": "S2.9.p2"}, confidence="high",
    reasoning="S2.9.p2 LRT: SVs + Tissue + Phase + Training + Phase:Training vs reduced model; the interaction is the estimand.")
pair = native.pairing_report(sub_path, "rep_letter", "tissue", ["SAT", "VAT"])
case.decide("covariance", final={
    "status": "unresolved", "blocking_terms": [],
    "covariates": [{"name": "animal", "disposition": "unresolved: SAT and VAT come from the same rats (S2.5.p1, S2.9.p1) but no animal ID is deposited; replicate letters a-f are not documented as animal IDs"},
                   {"name": "surrogate_variables_1_2", "disposition": "excluded: no sva executor"}],
    "pairing_report_if_letter_were_animal": {k: pair[k] for k in ("n_subjects", "n_complete", "complete_and_unique")},
}, evidence=[paper, sub_ev], paper={"locator": "S2.5.p1"}, confidence="medium",
    decision_status="manual_review",
    stop_reason=("Model pools SAT and VAT from the same rats, so animal is a repeated-measure key, but GEO has no animal ID "
                 "(replicate letters cannot be verified as rats). In addition no DESeq2 LRT executor exists. "
                 "Unblock with an animal-to-library table from the authors and an LRT or limma interaction route."),
    reasoning="Repeated tissues per rat require blocking; the key is unknown, so the interaction model cannot be specified safely.")
case.write_json("reproduction_plan.json", {"paper_route": "DESeq2 LRT full ~ SVs + Tissue + Phase + Training + Phase:Training vs reduced",
                                           "status": "not run: stopped at covariance (manual_review)"}, role="reproduction_plan")
case.write_json("reproduction_summary.json", {"paper_reported": 632, "reproduced": None,
                                              "reason": "animal key across tissues unknown; no LRT executor"}, role="reproduction_summary")
case.finish()

run.finish()
out = {k: {kk: vv for kk, vv in v.items() if kk != "deg"} for k, v in results.items()}
(run.run_dir / "results_overview.json").write_text(json.dumps(out, indent=2, default=str), encoding="utf-8")
print(json.dumps(out, indent=1, default=str))
