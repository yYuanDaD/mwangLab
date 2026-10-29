import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID31197156"
run = native.RunRecorder.open(RUN); case = run.case("GSE124819")
paper = case.evidence_item("paper:PMC6565704.paper.md")
meta = case.evidence_item("metadata:GSE124819_metadata.csv")
adir = case.dir / "aligned"
aligned = case.evidence_item("tool_output:aligned_matrix.csv")
design_item = case.evidence_item("tool_output:design_metadata.csv")
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)

# ---------- design
PLANNED = ["cond_large_vs_cont_set-act", "cond_swim_vs_cont_set-ex", "cond_sww_vs_cont_set-ex"]
rep, s_item, s_summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["set", "cond"],
    matrix_csv=str(adir / "aligned_matrix.csv"), organism="Rat", subject=None,
    references={"set": "ex", "cond": "cont"}, planned=PLANNED)
print(json.dumps(s_summary, default=str))
analyzable = [c for c in rep["comparisons"] if c["analyzable"]]
names = [c["name"] for c in analyzable]
assert all(p in names for p in PLANNED), names
case.decide("design", final={
    "analysis_type": "multilevel, two independent sample sets (set x cond with missing cells), between-animal",
    "formula": "~ cell (cell = set x cond, 8 observed cells; one DESeq2 model on all 37 samples)",
    "design_column": "grp", "factors": {"set": ["ex (ref)", "act"], "cond": ["cont (ref)", "nosci", "large", "swim", "sww", "tx"]},
    "contrasts": [
        {"name": "cond_large_vs_cont_set-act", "role": "planned: in-cage activity effect after CONT SCI (S1.p3, S4.3.p1)", "control": "act_cont", "treatment": "act_large"},
        {"name": "cond_swim_vs_cont_set-ex", "role": "planned: swimming effect after CONT SCI, tiny cages (S1.p3, S4.3.p2)", "control": "ex_cont", "treatment": "ex_swim"},
        {"name": "cond_sww_vs_cont_set-ex", "role": "planned: shallow-water-walking effect after CONT SCI, tiny cages (S1.p3, S4.3.p2)", "control": "ex_cont", "treatment": "ex_sww"},
        {"name": "13 other analyzable comparisons from the suitability report", "role": "exploratory (injury, TX, SWIM vs SWW, between-set)"}],
    "estimand_type": "causal (random assignment to groups, S2.2.p1)",
    "suitability": s_summary,
    "sex_split": "all 37 female (metadata; rat X/Y markers unavailable in the sex check): no split"},
    evidence=[paper, meta, s_item, design_item], paper={"locator": "S2.2.p1"}, confidence="high",
    candidates=[{"value": "pool SWIM and SWW into one exercise arm", "reason_rejected": "distinct paradigms (S1.p3); pooling changes the estimand"},
                {"value": "pool CONT tiny of both sets as one control", "reason_rejected": "sets are separate experiments (different housing of No SCI, read depth, TAB1); each exercise contrast uses its own set's control"},
                {"value": "large vs No SCI standard cage", "reason_rejected": "mixes injury and housing; kept only as exploratory"}],
    reasoning="Rats were randomized within each sample set (S2.2.p1). The exercise/activity estimands are within contusion-injured rats and within a set: Large vs Tiny cage (act set), SWIM vs CONT and SWW vs CONT (ex set, all tiny cages). Every planned cell has n >= 4; residual df 29.")

# ---------- covariance
conf = native.confounding_report(dm, "grp", candidates=["set", "dpi"])
dchk = native.design_check(dm, ["grp"])
print(json.dumps({"conf": conf, "dchk": dchk}, default=str)[:3000])
case.decide("covariance", final={"status": "not_required", "blocking_terms": [], "covariates": [
        {"name": "animal", "disposition": "excluded: one liver per rat, nested in group (between-animal design)"},
        {"name": "set (sample set / sequencing batch)", "disposition": "nested: every cell belongs to one set; the cell-means model absorbs it; each planned contrast is within one set"},
        {"name": "dpi (time post-injury)", "disposition": "excluded: GEO records 11.5 weeks for every contusion group (constant within each planned contrast); TX 8.5 weeks. Paper text says exercised rats were collected at 13.5 weeks (S4.4.p1): if so it is aliased with SWIM/SWW by design and cannot be modelled - recorded as caveat"},
        {"name": "cage-mate pairs (doubly housed, S2.2.p1)", "disposition": "excluded: cage IDs not deposited"},
        {"name": "sex", "disposition": "excluded: single level (female)"}],
    "confounding_report": conf, "design_check": dchk},
    evidence=[design_item, aligned, paper], paper={"locator": "S4.4.p1"}, confidence="medium",
    reasoning="Different rats per group, randomized within set: no blocking. Set is nested in cells. Time post-injury is constant within the planned contrasts per GEO but conflicts with the paper's 13.5-week statement for exercised rats; noted as a limitation, not modelled.")

# ---------- method
case.decide("method", final={"method": "DESeq2 joint cell-means model (Wald test per contrast, RLE size factors)",
    "matrix_type": "raw counts", "formula": "~ cell (cell = set x cond, 8 levels, all 37 samples)",
    "paper_route": {"method": "no differential-expression test in the paper", "status": "blocked",
                    "reason": "Data Descriptor reports no DE method; DESeq2 chosen because the paper normalized with DESeq2 RLE (S2.5.p3)"},
    "rejected": ["two-arm DESeq2 per contrast: refits on 8-10 samples and loses dispersion information",
                 "separate model per set: possible but the skill prefers one model on all samples; sets are nested in cells"]},
    evidence=[aligned, paper], paper={"locator": "S2.5.p3"}, confidence="medium",
    reasoning="Raw HTSeq counts; the paper's only stated statistics are DESeq2 RLE normalization, so DESeq2 is the closest route.")

# ---------- threshold
case.decide("threshold", final={"paper_threshold": {"metric": "not_reported", "cutoff": None, "effect_metric": None, "effect_cutoff": None,
                                                    "source_locator": "not_reported"},
    "threshold_source": "workflow_default",
    "applied_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None, "inclusive": False},
    "multiplicity": "BH within each contrast"},
    evidence=[paper], confidence="high",
    reasoning="The paper reports no DE threshold; workflow default BH padj < 0.05, no fold-change cutoff.")

# ---------- execution
od = case.dir / "results" / "deseq2_joint"
results = {}
try:
    jr = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(adir / "aligned_matrix.csv"),
                          metadata_csv=str(adir / "design_metadata.csv"), comparisons=rep["comparisons"], output_dir=str(od))
    outs, per = [], {}
    for r in jr["results"]:
        thr = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=None)
        o = case.add_output(r["path"], f"deg_joint_{r['name']}")
        outs.append(o)
        per[r["name"]] = {k: thr[k] for k in thr if k in ("n_significant", "n_up", "n_down", "deg_sanity")}
    results = per
    case.write_json("results/deseq2_joint/joint_summary.json", {**{k: v for k, v in jr.items() if k != "results"}, "per_comparison": per})
    case.decide("execution", final={"method": "DESeq2 joint cell-means model", "subset": "all 16 analyzable suitability comparisons (3 planned, 13 exploratory)",
        "formula": jr["formula"], "outputs": outs, "threshold_counts": per, "skipped": jr["skipped"], "n_genes": jr["n_genes"]},
        evidence=outs[:3] + [aligned], confidence="high", execution_status="completed",
        reasoning="One DESeq2 fit on 37 samples; contrasts per comparison; BH padj < 0.05.")
    exec_ok = True
except native.NativeToolError as err:
    case.decide("execution", final={"method": "DESeq2 joint cell-means model", "subset": "all comparisons", "execution_error": str(err)},
                evidence=[aligned], confidence="high", execution_status="failed", reasoning="joint DESeq2 failed")
    print("joint ERR", err)
    exec_ok = False
json.dump(results, open(case.dir / "results" / "deg_counts.json", "w"), indent=2, default=str)
print(json.dumps(results, indent=1, default=str))

# ---------- study
case.write_json("reproduction_plan.json", {
    "paper_aligned": ["sample sets, groups and contrasts as defined in S2.2.p1/S1.p3; DESeq2 RLE normalization (S2.5.p3)"],
    "declared_deviation": ["DE test (DESeq2 Wald, joint cell-means model) and threshold (workflow default BH padj<0.05): paper reports none"],
    "exploratory": ["injury (CONT/TX vs No SCI), SWIM vs SWW, TX vs exercise, between-set comparisons"]})
case.write_json("reproduction_summary.json", {"status": "finished" if exec_ok else "execution_failed", "deg_counts": results,
    "paper_counts": "none reported (Data Descriptor)",
    "notes": ["between-set comparisons (set_act_vs_ex_*) mix sequencing batch and, for nosci, cage size",
              "GEO and paper disagree on exercise schedule and sacrifice time (paper_data_discrepancies.json)"]})
planned_counts = {k: results.get(k, {}).get("n_significant") for k in PLANNED}
case.decide("study", final={"route": "declared_deviation",
    "components": {"declared_deviation": PLANNED, "exploratory": [n for n in names if n not in PLANNED]},
    "deg_counts_applied_threshold": {k: v.get("n_significant") for k, v in results.items()}, "paper_counts": "not reported",
    "exploratory_reason": "non-exercise comparisons are context only; between-set comparisons are confounded with batch/housing"},
    evidence=[paper], paper={"locator": "S1.p3"}, confidence="medium",
    reasoning="Paper-defined exercise/activity contrasts run with DESeq2 and the workflow-default threshold because the paper reports no DE test.")
main = results.get("cond_swim_vs_cont_set-ex", {})
print(case.finish(n_deg=main.get("n_significant"), deg_sanity=main.get("deg_sanity")))
print(run.finish())
