import sys, pathlib, json; sys.path.insert(0, str(next(p for p in pathlib.Path(__file__).resolve().parents if (p / "tools" / "native.py").exists())))  # repository root
import os; os.chdir(sys.path[0])
from tools import native
native.enable_native_mode()
import pandas as pd
from tools import suitability as su
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/PMID31350552"
run = native.RunRecorder.open(RUN); case = run.case("GSE129962")
paper = case.evidence_item("paper:PMC7177479.paper.md")
meta = case.evidence_item("metadata:GSE129962_metadata.csv")
adir = case.dir / "aligned"
aligned = case.evidence_item("tool_output:aligned_matrix.csv")
design_item = case.evidence_item("tool_output:design_metadata.csv")
dm = pd.read_csv(adir / "design_metadata.csv", index_col=0)

# ---------- design
PLANNED = ["cond_EX6_vs_RA6_geno-WT", "cond_EX6_vs_RA6_geno-DH", "geno_cond_DH_EX6_vs_WT_RA6"]
rep, s_item, s_summary = case.suitability(matrix_type="raw counts", metadata=dm, factors=["geno", "cond"],
    matrix_csv=str(adir / "aligned_matrix.csv"), organism="Mouse", subject=None,
    references={"geno": "WT", "cond": "RA6"}, planned=PLANNED)
print(json.dumps(s_summary, default=str))
names = [c["name"] for c in rep["comparisons"]]
assert all(p in names for p in PLANNED), names
sexchk = rep["checks"]["sex"]
sex_tab = pd.read_csv(sexchk["table"], sep="\t", index_col=0)
dm["sex"] = sex_tab.loc[dm.index, "predicted_sex"]
dm["grp"] = dm["geno"] + "_" + dm["cond"]
dm.to_csv(adir / "design_metadata_sex.csv")
dsex = case.add_output(adir / "design_metadata_sex.csv", "design_metadata_sex")
sex_cells = pd.crosstab(dm["grp"], dm["sex"]).to_dict()
print("sex per cell", sex_cells)
case.decide("design", final={
    "analysis_type": "factorial (2 genotypes x 3 conditions RA3/RA6/EX6), between-animal",
    "formula": "~ 0 + cell (cell = geno x cond; one model on all 30 samples) for the joint DESeq2 route; two-arm ~ grp for the paper's edgeR route",
    "design_column": "grp", "factors": {"geno": ["WT (ref)", "DH"], "cond": ["RA6 (ref)", "EX6", "RA3"]},
    "contrasts": [
        {"name": "cond_EX6_vs_RA6_geno-WT", "role": "planned (paper S6.4.p4)", "control": "WT_RA6", "treatment": "WT_EX6"},
        {"name": "cond_EX6_vs_RA6_geno-DH", "role": "planned (paper S6.4.p5)", "control": "DH_RA6", "treatment": "DH_EX6"},
        {"name": "geno_cond_DH_EX6_vs_WT_RA6", "role": "planned interaction (paper S6.4.p11): (DH_EX6 - WT_EX6) - (DH_RA6 - WT_RA6)"},
        {"name": "other 8 comparisons from the suitability report", "role": "exploratory (genotype and age effects, context for rescue)"}],
    "estimand_type": "causal (randomized exercise allocation at 3 months, S5.5.p1)",
    "suitability": s_summary, "sex_by_cell": sex_cells,
    "sex_split": "both sexes present (18 male, 12 female, no metadata sex to compare): per-sex analyses added as exploratory (only male cells have >=3 per arm for the exercise contrasts)"},
    evidence=[paper, meta, s_item, design_item, dsex], paper={"locator": "S6.4.p4"}, confidence="high",
    candidates=[{"value": "pool EX6 vs all RA samples", "reason_rejected": "RA3 is a different age; pooling changes the estimand"},
                {"value": "exercise main effect pooled over genotypes", "reason_rejected": "paper reports exercise effect within each genotype plus their interaction"},
                {"value": "6-month samples only (20)", "reason_rejected": "skill prefers one model on all samples; RA3 cells share the same cell-means model without biasing 6-month contrasts"}],
    reasoning="Randomized 2x2 at 6 months (genotype x activity) plus a 3-month baseline per genotype. Paper's exercise estimand is EX6 vs RA6 within each genotype (S6.4.p4/p5) and the genotype-by-exercise interaction (S6.4.p11). Every cell has n=5.")

# ---------- covariance
e = pd.read_csv(adir / "aligned_matrix.csv", index_col=0)
e = e[e.index.str.startswith("ERCC")]
pat = e.isna().apply(lambda c: "".join("1" if x else "0" for x in c))
codes = {p: f"run{i}" for i, p in enumerate(sorted(pat.unique()))}
dm["count_run"] = pat.map(codes)
dm.to_csv(adir / "design_metadata_sex.csv")
dsex = case.add_output(adir / "design_metadata_sex.csv", "design_metadata_sex")
conf = native.confounding_report(dm, "grp", candidates=["sex", "count_run"])
conf6 = native.confounding_report(dm[dm["cond"] != "RA3"], "cond", candidates=["count_run", "sex"])
dchk = native.design_check(dm, ["geno", "cond"], interactions=[("geno", "cond")])
dchk_sex = native.design_check(dm, ["geno", "cond", "sex"], interactions=[("geno", "cond")])
print(json.dumps({"conf": conf, "conf6": conf6, "dchk": dchk, "dchk_sex": dchk_sex}, default=str)[:3000])
run_tab = pd.crosstab(dm["grp"], dm["count_run"]).to_dict()
case.decide("covariance", final={"status": "not_required", "blocking_terms": [], "covariates": [
        {"name": "subject/animal", "disposition": "excluded: one sample per mouse, nested in group (between-animal design)"},
        {"name": "sex", "disposition": "excluded: paper pooled sex-matched animals (S5.7.p1) and did not adjust; crossed with group; per-sex exploratory analyses instead"},
        {"name": "count_run (inferred from which ERCC IDs are missing in the combined featureCounts table)",
         "disposition": "excluded: undocumented; aliased with cond within 6 months (all EX6 = run3, RA6 = run1/run2), crossed with genotype. ERCC counts are ~0, so it marks separate counting/annotation runs, not spike-in normalization. Cannot be modelled; caveat on EX6 vs RA6 simple contrasts, the interaction is unaffected",
         "table": run_tab}],
    "confounding_report": conf, "confounding_6m_cond": conf6, "design_check": dchk, "design_check_with_sex": dchk_sex},
    evidence=[dsex, aligned, paper], paper={"locator": "S5.5.p1"}, confidence="medium",
    reasoning="Different mice per group, randomized to activity (S5.5.p1): no blocking. Sex is crossed with group and was not adjusted in the paper. A processing-run pattern inferred from missing ERCC rows is aliased with exercise at 6 months but is not a documented batch (no spike-in reads, paper states randomization); it is recorded as a limitation rather than a stop. Factorial design full rank, residual df 24.")

# ---------- method
case.decide("method", final={"method": "edgeR (QL F-test, TMM) two-arm per planned simple contrast; DESeq2 joint cell-means model for the interaction and exploratory comparisons",
    "matrix_type": "raw counts",
    "formula": "edgeR: ~ grp on the two compared groups; DESeq2: ~ cell (cell = geno x cond, 6 levels, all 30 samples); interaction contrast (DH_EX6 - WT_EX6) - (DH_RA6 - WT_RA6)",
    "feature_filter": "drop 23 ERCC spike-in rows (missing in some samples, ~0 counts); edgeR route: keep genes with CPM >= 1 in >= 5 of the compared samples (paper reports ~11.1-11.9k genes analysed but not its rule; this gives 12.6-12.9k). DESeq2 route: pydeseq2 independent filtering",
    "paper_route": {"method": "edgeR genotype-by-exercise interaction", "status": "blocked",
                    "reason": "repository edgeR executor fits only ~ Treatment on two arms (tools/edger_tools.py:110-115); interaction run with DESeq2 joint model as declared deviation"},
    "rejected": ["limma-voom: not the paper's method", "RUVr: no executor; only relevant to cross-age exploratory contrasts"]},
    evidence=[aligned, paper], paper={"locator": "S5.7.p2"}, confidence="medium",
    reasoning="Paper used edgeR on featureCounts (S5.7.p2). The repository edgeR executor reproduces the two-arm exercise contrasts; the interaction needs a multi-term model, which only the joint DESeq2 executor provides for counts.")

# ---------- threshold
pth = {"metric": "qvalue", "adjustment": "not_reported", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None,
       "inclusive": False, "source_locator": "S5.7.p2"}
case.decide("threshold", final={"paper_threshold": pth, "threshold_source": "paper",
    "applied_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.05, "effect_metric": None, "effect_cutoff": None, "inclusive": False},
    "note": "same rule on the DESeq2 deviation route (interaction, exploratory)"},
    evidence=[paper], paper={"locator": "S5.7.p2"}, confidence="high",
    reasoning="Paper: 'Significance level for the DEGs was set at q<0.05'; no fold-change cutoff. edgeR topTags reports BH FDR.")

# ---------- execution
cnt = pd.read_csv(adir / "aligned_matrix.csv", index_col=0)
cnt = cnt[~cnt.index.str.startswith("ERCC")].astype(int)
cnt.to_csv(adir / "counts_noERCC.csv")
case.add_output(adir / "counts_noERCC.csv", "counts_noERCC")
results = {}
cpm = cnt / cnt.sum() * 1e6
for name, ctrl, trt in [("cond_EX6_vs_RA6_geno-WT", "WT_RA6", "WT_EX6"), ("cond_EX6_vs_RA6_geno-DH", "DH_RA6", "DH_EX6")]:
    od = case.dir / "results" / "edger" / name
    od.mkdir(parents=True, exist_ok=True)
    s = dm.index[dm["grp"].isin([ctrl, trt])]
    keep = ((cpm[s] >= 1).sum(axis=1) >= 5)
    cnt.loc[keep, s].to_csv(od / "counts_filtered.csv")
    dm.loc[s].to_csv(od / "metadata.csv")
    try:
        msg = native.call_tool("tools.edger_tools:run_edger_analysis", counts_csv=str(od / "counts_filtered.csv"),
                               metadata_csv=str(od / "metadata.csv"), design_column="grp", control_group=ctrl,
                               treatment_group=trt, output_dir=str(od))
        deg = native.deg_outputs(od)[0]
        thr = native.apply_threshold(deg, metric="padj", cutoff=0.05, effect_cutoff=None)
        o = case.add_output(deg, f"deg_edger_{name}")
        results[name] = {"route": "edgeR", "n_genes_tested": int(keep.sum()), **{k: thr[k] for k in thr if k in ("n_significant", "n_up", "n_down", "deg_sanity")}}
        case.decide("execution", final={"method": "edgeR QL (two-arm)", "subset": name, "outputs": [o],
            "n_genes_tested": int(keep.sum()), "threshold_counts": thr},
            evidence=[o, aligned], confidence="high", execution_status="completed",
            reasoning=f"edgeR {trt} vs {ctrl}, padj<0.05.")
    except native.NativeToolError as err:
        results[name] = {"route": "edgeR", "error": str(err)}
        case.decide("execution", final={"method": "edgeR QL (two-arm)", "subset": name, "execution_error": str(err)},
                    evidence=[aligned], confidence="high", execution_status="failed", reasoning="edgeR failed")
    print(name, results[name])

# joint DESeq2: all comparisons (planned interaction = declared deviation; the rest exploratory)
od = case.dir / "results" / "deseq2_joint"
try:
    jr = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(adir / "counts_noERCC.csv"),
                          metadata_csv=str(adir / "design_metadata_sex.csv"), comparisons=rep["comparisons"], output_dir=str(od))
    outs, per = [], {}
    for r in jr["results"]:
        thr = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=None)
        o = case.add_output(r["path"], f"deg_joint_{r['name']}")
        outs.append(o)
        per[r["name"]] = {k: thr[k] for k in thr if k in ("n_significant", "n_up", "n_down", "deg_sanity")}
        results["joint:" + r["name"]] = {"route": "DESeq2 joint", **per[r["name"]]}
    case.write_json("results/deseq2_joint/joint_summary.json", {**{k: v for k, v in jr.items() if k != "results"}, "per_comparison": per})
    case.decide("execution", final={"method": "DESeq2 joint cell-means model", "subset": "all 11 suitability comparisons (interaction planned; others exploratory)",
        "formula": jr["formula"], "outputs": outs, "threshold_counts": per, "skipped": jr["skipped"]},
        evidence=outs[:3] + [aligned], confidence="high", execution_status="completed",
        reasoning="One DESeq2 fit on 30 samples, contrasts per comparison, padj<0.05.")
except native.NativeToolError as err:
    case.decide("execution", final={"method": "DESeq2 joint cell-means model", "subset": "all comparisons", "execution_error": str(err)},
                evidence=[aligned], confidence="high", execution_status="failed", reasoning="joint DESeq2 failed")
    print("joint ERR", err)

# per-sex exploratory (joint model with sex strata)
sex_comps = [c for c in su.enumerate_comparisons(dm, ["geno", "cond"], strata=["sex"], references={"geno": "WT", "cond": "RA6"}) if c["analyzable"]]
print("per-sex analyzable:", [c["name"] for c in sex_comps])
od = case.dir / "results" / "deseq2_joint_by_sex"
try:
    jr = native.call_tool("tools.joint_contrasts:run_joint_deseq2", counts_csv=str(adir / "counts_noERCC.csv"),
                          metadata_csv=str(adir / "design_metadata_sex.csv"), comparisons=sex_comps, output_dir=str(od))
    outs, per = [], {}
    for r in jr["results"]:
        thr = native.apply_threshold(r["path"], metric="padj", cutoff=0.05, effect_cutoff=None)
        outs.append(case.add_output(r["path"], f"deg_sex_{r['name']}"))
        per[r["name"]] = {k: thr[k] for k in thr if k in ("n_significant", "n_up", "n_down")}
        results["sex:" + r["name"]] = {"route": "DESeq2 joint by sex", **per[r["name"]]}
    case.decide("execution", final={"method": "DESeq2 joint cell-means model (geno x cond x sex)", "subset": "per-sex exploratory comparisons",
        "formula": jr["formula"], "outputs": outs, "threshold_counts": per},
        evidence=outs[:3] + [aligned], confidence="medium", execution_status="completed",
        reasoning="Exploratory per-sex contrasts (skill split plan); male 3 vs 3 at 6 months.")
except native.NativeToolError as err:
    case.decide("execution", final={"method": "DESeq2 joint (by sex)", "subset": "per-sex exploratory", "execution_error": str(err)},
                evidence=[aligned], confidence="medium", execution_status="failed", reasoning="per-sex joint DESeq2 failed")
    print("sex ERR", err)

json.dump(results, open(case.dir / "results" / "deg_counts.json", "w"), indent=2, default=str)
print(json.dumps(results, indent=1, default=str))
