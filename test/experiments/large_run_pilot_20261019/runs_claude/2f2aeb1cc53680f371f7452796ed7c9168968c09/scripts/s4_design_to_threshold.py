import sys, pathlib, json; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[6]))
from tools import native
native.enable_native_mode()
import pandas as pd, numpy as np, patsy
RUN = "test/experiments/large_run_pilot_20261019/runs_claude/2f2aeb1cc53680f371f7452796ed7c9168968c09"
run = native.RunRecorder.open(RUN); case = run.case("GSE179302")
E = case.evidence_item
paper, meta, dmd, am = E("paper:PMC9722583.paper.md"), E("metadata:GSE179302_metadata.csv"), E("tool_output:design_metadata.csv"), E("tool_output:aligned_matrix.csv")
DMD = RUN + "/GSE179302/aligned/design_metadata.csv"; d = pd.read_csv(DMD, index_col=0)
s = d.index[d.tert.isin(["active", "inactive"])].tolist()

case.decide("design", final={"analysis_type": "two_group_adjusted", "estimand_type": "associational",
    "design_column": "tert", "control": "inactive", "treatment": "active",
    "formula": "~ sex + age + race + tert", "contrasts": ["active_vs_inactive"],
    "samples": {"active": 13, "inactive": 8, "excluded_intermediate": 14},
    "direction": "log2FC > 0 = higher in the most active tertile"},
    candidates=[{"value": "~ tert with 3 levels, intermediate in the model", "reason_rejected": "paper reports the highest-vs-lowest comparison (S3.p3); the two-arm executors subset to the contrast arms"},
                {"value": "activity as a continuous dose", "reason_rejected": "GEO deposits only tertile labels; paper's primary analysis is tertile-based"},
                {"value": "sensitivity models + RADAI / + PROMIS", "reason_rejected": "RADAI and PROMIS are not in GEO metadata"}],
    evidence=[paper, dmd], paper={"locator": "S3.p3"}, confidence="high",
    reasoning="Cross-sectional observational comparison of physical-activity tertiles (S2.2.1.p1, S3.p3): associational, not an exercise intervention effect.")

conf = native.confounding_report(d, "tert", ["sex", "race", "hisp", "age"], samples=s)
dc_full = native.design_check(d, ["tert", "sex", "race", "hisp"], samples=s)
dc_used = native.design_check(d, ["tert", "sex", "race"], samples=s)
X = patsy.dmatrix("~ C(tert) + C(sex) + age + C(race)", d.loc[s]); rk = int(np.linalg.matrix_rank(np.asarray(X)))
age_check = {"n_columns": int(X.shape[1]), "rank": rk, "residual_df": len(s) - rk}
print(dc_full["rank"], dc_full["n_columns"], dc_used, age_check)
xt = pd.crosstab(d.loc[s, "race"], d.loc[s, "hisp"]).to_dict()
case.decide("covariance", final={"status": "not_required", "blocking_terms": [],
    "covariates": [{"name": "sex", "disposition": "included"}, {"name": "age", "disposition": "included (continuous; limma route only, see method)"},
                   {"name": "race", "disposition": "included"},
                   {"name": "hisp", "disposition": "aliased: identical to race level 'dk' in the 21 contrast samples (all 9 Hispanic patients have race 'dk', no non-Hispanic does); race already carries it"},
                   {"name": "SV1 (sva)", "disposition": "excluded: sva not available in this environment; declared deviation"}],
    "confounding_report": conf, "design_check_with_hisp": dc_full, "design_check_used": dc_used, "rank_with_age": age_check, "race_x_hisp": xt},
    evidence=[dmd, paper], paper={"locator": "S2.5.p1"}, confidence="medium",
    reasoning="One sample per patient, no blocking unit. Paper-named covariates sex, age, race, ethnicity kept; ethnicity is exactly aliased with race='dk' within the contrast (design with both is rank 7/8), so it is represented by race. All 2 males are inactive and actives lack Asian/Black patients: covariates are crossed, not aliased; residual df 13.")

case.decide("method", final={"method": "limma (limma-trend on log2(CPM+1), inmoose)", "matrix_type": "raw counts",
    "transform": "log2(CPM+1)", "formula": "~ sex + age + race + tert",
    "filter": "keep genes with count>0 in >=30% of samples in every activity tertile (computed on all 35) -> 19,260 features, exactly the paper's 19,260 (S2.4.p1)",
    "paper_route": {"method": "DESeq2 ~ sex + age + race + ethnicity + SV1, IHW", "status": "blocked",
                    "reason": "tools/deseq2_tools.py run_deseq2_analysis -> build_multifactor_plan (tools/multifactor_design.py:126) casts every covariate to a categorical string, so continuous age cannot enter a DESeq2 model (18 age levels in 21 samples -> rank deficient); sva and IHW are not installed"},
    "secondary_route": {"method": "DESeq2 ~ sex + race + tert (age omitted), same filter, BH", "role": "sensitivity: paper's count model without age"}},
    candidates=[{"value": "DESeq2 ~ sex + race + tert", "reason_rejected": "omits age, which differs between arms (50 vs 63 y, TAB1 p=0.04) and is a paper covariate; run as secondary sensitivity"}],
    evidence=[am, dmd, paper], paper={"locator": "S2.5.p1"}, confidence="medium",
    reasoning="Raw integer counts support DESeq2, but the executor cannot model continuous age; limma on log2(CPM+1) accepts the full paper covariate set via design_formula. Declared deviation.")

case.decide("threshold", final={"paper_threshold": {"metric": "padj", "adjustment": "IHW", "cutoff": 0.1, "effect_metric": None, "effect_cutoff": None, "inclusive": False, "source_locator": "S2.5.p1"},
    "threshold_source": "paper_on_deviation_route",
    "applied_threshold": {"metric": "padj", "adjustment": "BH", "cutoff": 0.1, "effect_metric": None, "effect_cutoff": None, "inclusive": False},
    "deviation_note": "IHW (independent hypothesis weighting) not available; Benjamini-Hochberg at the same 0.1 cutoff. IHW is typically at least as powerful as BH, so BH counts are expected to be lower or similar."},
    evidence=[paper], paper={"locator": "S2.5.p1"}, confidence="high",
    reasoning="Paper: adjusted p < 0.1 with IHW, no fold-change cutoff.")
