"""Self-test of the bioinformatics-workflow skill on this machine.

Runs a small native run on synthetic data with planted effects, through every
route this environment supports, and checks that each executor recovers the
planted genes with the right sign. Every case is recorded with RunRecorder,
validated against the decision contract, and audited.

Usage:
    python scripts/skill_selftest.py                 # offline routes
    python scripts/skill_selftest.py --network       # also GSEA and ORA (needs network)
    python scripts/skill_selftest.py --require-all   # a skipped route counts as a failure

Result per route: PASS, SKIP (a package or network is missing; the reason is
shown), or FAIL. Exit code 1 when any route fails, or when --require-all is
given and any route was skipped. The report is written to
<out>/selftest_report.json (default output/skill_selftest_<timestamp>).
"""

from __future__ import annotations

import argparse
import json
import runpy
import sys
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from tools import decision_contract, native  # noqa: E402

AUDIT_SCRIPT = ROOT / ".agents" / "skills" / "evaluate-bioinformatics-agent" / "scripts" / "audit_run.py"
WORKFLOW_DEFAULT = {"metric": "padj", "adjustment": "BH", "cutoff": 0.05,
                    "effect_metric": None, "effect_cutoff": None}
# Real human symbols for the network enrichment check: an interferon block that
# should lead the ranking, plus housekeeping filler.
INTERFERON = ["ISG15", "IFI6", "IFI27", "IFI44", "IFI44L", "IFIT1", "IFIT2", "IFIT3", "IFITM1",
              "IFITM3", "MX1", "MX2", "OAS1", "OAS2", "OAS3", "OASL", "RSAD2", "STAT1", "IRF7",
              "IRF9", "ISG20", "HERC5", "CMPK2", "EPSTI1", "XAF1", "BST2", "IFIH1", "USP18",
              "PARP9", "PARP14", "SAMD9L", "LY6E", "PLSCR1", "TRIM22", "SP110", "LAP3", "GBP1",
              "GBP4", "CXCL10", "DDX60"]
FILLER = ["ACTB", "GAPDH", "TUBB", "RPLP0", "RPL13A", "B2M", "HPRT1", "TBP", "PPIA", "YWHAZ",
          "SDHA", "UBC", "GUSB", "HMBS", "PGK1", "ALDOA", "ENO1", "LDHA", "PKM", "TPI1", "EEF1A1",
          "EEF2", "HSPA8", "HSP90AB1", "CALM2", "CFL1", "PFN1", "MYL6", "TMSB4X", "FTL", "FTH1",
          "NPM1", "NCL", "HNRNPA1", "SRSF3", "PTMA", "ATP5F1A", "COX4I1", "NDUFA4", "UQCRH",
          "TPT1", "RACK1", "SERBP1", "SOD1", "PRDX1", "GSTP1", "ANXA2", "S100A10", "VIM", "CD74",
          "COL1A1", "COL1A2", "COL3A1", "FN1", "SPARC", "MYH7", "ACTA1", "CKM", "MB", "DES"]


class Route:
    """Result of one route: PASS, SKIP, or FAIL with details."""

    def __init__(self, name: str):
        self.name, self.status, self.detail, self.metrics = name, "PASS", "", {}

    def skip(self, why: str) -> "Route":
        self.status, self.detail = "SKIP", why
        return self

    def fail(self, why: str) -> "Route":
        self.status, self.detail = "FAIL", why
        return self

    def as_dict(self) -> dict:
        return {"route": self.name, "status": self.status, "detail": self.detail, "metrics": self.metrics}


# ---------------------------------------------------------------- synthetic data

def _nb(rng, mu, dispersion=0.1):
    shape = 1.0 / dispersion
    return rng.poisson(rng.gamma(shape, mu / shape))


def _planted(rng, n_genes, n_de, size=2.0):
    effect = np.zeros(n_genes)
    hit = rng.choice(n_genes, n_de, replace=False)
    effect[hit] = rng.choice([-size, size], n_de)
    return effect


def bulk_paired(rng, n_genes=600, n_subjects=8):
    genes = [f"G{i:04d}" for i in range(n_genes)]
    base = np.exp(rng.normal(5.0, 1.0, n_genes))
    effect = _planted(rng, n_genes, 40)
    subject = rng.normal(0, 0.5, (n_subjects, n_genes))
    cols, rows = {}, []
    for s in range(n_subjects):
        for t, label in ((0, "pre"), (1, "post")):
            sample = f"S{s + 1:02d}_{label}"
            cols[sample] = _nb(rng, base * rng.uniform(0.8, 1.2) * np.exp(subject[s]) * 2 ** (t * effect))
            rows.append({"sample": sample, "subject": f"S{s + 1:02d}", "time": label})
    return pd.DataFrame(cols, index=genes), pd.DataFrame(rows).set_index("sample"), effect


def fpkm_two_arm(rng, n_genes=600, n=5):
    genes = [f"G{i:04d}" for i in range(n_genes)]
    base = np.exp(rng.normal(5.0, 1.0, n_genes))
    length = rng.integers(800, 6000, n_genes)
    effect = _planted(rng, n_genes, 40)
    cols, rows = {}, []
    for i in range(2 * n):
        grp = "trt" if i >= n else "ctrl"
        counts = _nb(rng, base * 2 ** ((grp == "trt") * effect), 0.05)
        cols[f"X{i + 1}"] = np.round(counts / (length / 1e3) / (counts.sum() / 1e6), 4)
        rows.append({"sample": f"X{i + 1}", "grp": grp})
    return pd.DataFrame(cols, index=genes), pd.DataFrame(rows).set_index("sample"), effect


def multilevel(rng, n_genes=600, n=4):
    genes = [f"P{i:04d}" for i in range(n_genes)]
    base = rng.normal(8.0, 1.5, n_genes)
    effects = {"ctrl": np.zeros(n_genes), **{lv: _planted(rng, n_genes, 30) for lv in ("t1", "t2", "t3")}}
    cols, rows = {}, []
    for level, effect in effects.items():
        for r in range(n):
            sample = f"{level}_{r + 1}"
            cols[sample] = base + effect + rng.normal(0, 0.25, n_genes)
            rows.append({"sample": sample, "grp": level})
    return pd.DataFrame(cols, index=genes), pd.DataFrame(rows).set_index("sample"), effects


def methylation(rng, n_sites=800, n=5):
    sites = [f"cg{i:08d}" for i in range(n_sites)]
    base = rng.beta(2, 2, n_sites)
    shift = np.zeros(n_sites)
    hit = rng.choice(n_sites, 40, replace=False)
    shift[hit] = rng.choice([-0.25, 0.25], 40)
    cols, rows = {}, []
    for i in range(2 * n):
        grp = "trt" if i >= n else "ctrl"
        cols[f"M{i + 1}"] = np.clip(base + (grp == "trt") * shift + rng.normal(0, 0.03, n_sites), 0.001, 0.999)
        rows.append({"sample": f"M{i + 1}", "grp": grp})
    sign = np.sign(shift)  # beta up = M up
    return pd.DataFrame(cols, index=sites), pd.DataFrame(rows).set_index("sample"), sign


def proteomics(rng, n_proteins=400, n=6):
    ids = [f"Q{i:05d}" for i in range(n_proteins)]
    base = rng.normal(24.0, 2.0, n_proteins)
    effect = _planted(rng, n_proteins, 30)
    cols, rows = {}, []
    for i in range(2 * n):
        grp = "trt" if i >= n else "ctrl"
        log2 = base + (grp == "trt") * effect + rng.normal(0, 0.3, n_proteins)
        values = 2 ** log2
        # Missing not at random: the least abundant proteins drop out, as MinProb assumes.
        values[log2 < np.quantile(log2, 0.05)] = np.nan
        cols[f"LFQ intensity R{i + 1}"] = values
        rows.append({"sample": f"LFQ intensity R{i + 1}", "grp": grp})
    table = pd.DataFrame(cols)
    table.insert(0, "Protein IDs", ids)
    return table, pd.DataFrame(rows).set_index("sample"), pd.Series(effect, index=ids)


def single_cell(rng, n_genes=600, donors=6, cells=25):
    genes = [f"C{i:04d}" for i in range(n_genes)]
    base = np.exp(rng.normal(0.5, 1.0, n_genes))
    # 5% of genes change, so library-size normalization stays close to neutral
    effect = _planted(rng, n_genes, 30, size=1.5)
    donor_effect = rng.normal(0, 0.4, (donors, n_genes))
    cols, rows = {}, []
    for d in range(donors):
        for condition in ("ctrl", "stim"):
            for cell_type in ("typeA", "typeB"):
                mu = base * np.exp(donor_effect[d])
                if cell_type == "typeA" and condition == "stim":
                    mu = mu * 2 ** effect
                for c in range(cells):
                    cell = f"d{d + 1}_{condition}_{cell_type}_{c}"
                    cols[cell] = rng.poisson(mu * rng.uniform(0.5, 1.5))
                    rows.append({"cell": cell, "donor": f"d{d + 1}", "condition": condition,
                                 "cell_type": cell_type})
    return pd.DataFrame(cols, index=genes), pd.DataFrame(rows).set_index("cell"), effect


# ---------------------------------------------------------------- checks

def recovery(deg_csv: str, truth: pd.Series, *, cutoff=0.05) -> dict:
    """Planted-effect recovery at padj < cutoff. truth: +1/-1 for planted, 0 for null."""
    table = pd.read_csv(deg_csv, index_col=0)
    table.index = table.index.astype(str)
    truth = truth.reindex(table.index).fillna(0)
    padj = pd.to_numeric(table["padj"], errors="coerce")
    lfc = pd.to_numeric(table["log2FoldChange"], errors="coerce")
    sig = padj < cutoff
    planted = truth != 0
    hits = sig & planted
    sens = float(hits.sum() / planted.sum()) if planted.sum() else 0.0
    sign_ok = float((np.sign(lfc[hits]) == np.sign(truth[hits])).mean()) if hits.any() else 0.0
    fpr = float((sig & ~planted).sum() / max(1, (~planted).sum()))
    return {"sensitivity": round(sens, 3), "sign_agreement": round(sign_ok, 3),
            "null_false_positive_rate": round(fpr, 4), "n_tested": int(padj.notna().sum())}


def judge(route: Route, metrics: dict) -> Route:
    route.metrics.update(metrics)
    if metrics["sensitivity"] < 0.5 or metrics["sign_agreement"] < 0.95 \
            or metrics["null_false_positive_rate"] > 0.05:
        return route.fail(f"planted effects not recovered as expected: {metrics}")
    return route


def call(route: Route, case, evidence: dict, method: str, tool: str, **kwargs):
    """Run an executor; a missing package skips the route, any other failure fails it.

    On failure the execution is recorded as valid + failed, the planned route is
    recorded, and the case is finished.
    """
    try:
        return native.call_tool(tool, **kwargs)
    except native.NativeToolError as error:
        text = str(error)
        case.decide("execution", final={"method": method, "execution_error": text[:800]},
                    evidence=[evidence], reasoning="executor raised", confidence="high",
                    execution_status="failed")
        case.decide("study", final={"route": "paper_aligned"}, evidence=[evidence],
                    reasoning="planned route; execution failed", confidence="high")
        case.finish()
        if text.startswith("cannot import") or "No module named" in text:
            route.skip(f"missing package: {text.split(':', 2)[-1].strip()[:160]}")
        else:
            route.fail(text[:400])
        return None


def gates(case, *, spec: dict, inputs: list[dict], matrix_type: str, design: dict, covariance: dict,
          method: dict, threshold: dict = WORKFLOW_DEFAULT, n: int):
    case.decide("paper_reconstruction", evidence=[spec], confidence="high",
                reasoning="synthetic self-test specification",
                final={"accessions": ["SYNTHETIC"], "primary_estimand": design.get("estimand", "planted effect"),
                       "planned_contrasts": design.get("contrasts") or [f"{design['treatment']} vs {design['control']}"],
                       "paper_threshold": threshold})
    case.decide("ownership", evidence=inputs, confidence="high", reasoning="generated by the self-test",
                final={"accession": "SYNTHETIC", "matrix_file": inputs[0]["path"],
                       "metadata_file": inputs[-1]["path"], "owned": True})
    case.decide("alignment", evidence=inputs, confidence="high", reasoning="sample IDs match exactly",
                final={"method": "exact:metadata_index", "n_aligned": n, "n_metadata": n, "coverage": 1.0})
    case.decide("matrix", evidence=inputs[:1], confidence="high", reasoning="generated scale",
                final={"matrix_type": matrix_type, "recommended_method": method["method"]})
    design = {k: v for k, v in design.items() if k != "estimand"}
    blocking = covariance.get("blocking_terms") or []
    _, report, summary = case.suitability(
        matrix_type=matrix_type, metadata=pd.read_csv(inputs[-1]["path"], index_col=0),
        factors=[design["design_column"]], subject=blocking[0] if blocking else None, covariate_candidates=[])
    case.decide("design", evidence=inputs + [report], confidence="high", reasoning="planted design",
                final={**design, "suitability": summary})
    case.decide("covariance", evidence=inputs, confidence="high", reasoning="planted structure", final=covariance)
    case.decide("method", evidence=inputs[:1], confidence="high", reasoning="matrix-method policy",
                final={"matrix_type": matrix_type, **method})
    case.decide("threshold", evidence=[spec], confidence="high", reasoning="workflow default for the self-test",
                final={"paper_threshold": threshold, "threshold_source": "paper", "applied_threshold": threshold})


def complete(case, route: Route, method: str, deg: str, route_label="paper_aligned"):
    output = case.add_output(deg, "deg_table")
    counts = native.apply_threshold(deg, metric="padj", cutoff=0.05)
    case.decide("execution", evidence=[output], confidence="high", reasoning="executor completed",
                execution_status="completed", final={"method": method, "outputs": [deg]})
    case.decide("study", evidence=[output], confidence="high", reasoning="self-test",
                final={"route": route_label})
    case.finish(n_deg=counts["n_significant"], deg_sanity=counts["deg_sanity"])


def stage_inputs(case, workdir: Path, name: str, matrix: pd.DataFrame, meta: pd.DataFrame,
                 index_matrix=True) -> list[dict]:
    folder = workdir / name
    folder.mkdir(parents=True, exist_ok=True)
    matrix_path, meta_path, spec_path = folder / "matrix.csv", folder / "metadata.csv", folder / "spec.json"
    matrix.to_csv(matrix_path, index=index_matrix)
    meta.to_csv(meta_path)
    spec_path.write_text(json.dumps({"route": name, "synthetic": True}), encoding="utf-8")
    spec = case.add_input(spec_path, "user", "self-test specification")
    return [spec, case.add_input(matrix_path, "matrix"), case.add_input(meta_path, "metadata")]


def route_deseq2_paired(run, workdir, rng) -> Route:
    route, case = Route("deseq2_paired_blocking"), run.case("deseq2_paired_blocking", "SYNTHETIC")
    counts, meta, effect = bulk_paired(rng)
    spec, *inputs = stage_inputs(case, workdir, route.name, counts, meta)
    gates(case, spec=spec, inputs=inputs, matrix_type="raw counts", n=len(meta),
          design={"analysis_type": "paired within-subject", "design_column": "time", "formula": "~ subject + time",
                  "control": "pre", "treatment": "post"},
          covariance={"status": "required", "blocking_terms": ["subject"], "covariates": []},
          method={"method": "DESeq2", "formula": "~ subject + time"})
    out = workdir / route.name / "results"
    result = call(route, case, spec, "DESeq2", "tools.deseq2_tools:run_deseq2_analysis",
                  counts_csv=inputs[0]["path"], metadata_csv=inputs[1]["path"], design_column="time",
                  control_group="pre", treatment_group="post", output_dir=str(out), covariate_columns="subject")
    if result is None:
        return route
    deg = native.deg_outputs(out)[0]
    judge(route, recovery(deg, pd.Series(np.sign(effect), index=counts.index)))
    complete(case, route, "DESeq2", deg)
    return route


def route_limma_fpkm(run, workdir, rng) -> Route:
    route, case = Route("limma_fpkm_log2"), run.case("limma_fpkm_log2", "SYNTHETIC")
    fpkm, meta, effect = fpkm_two_arm(rng)
    spec, *inputs = stage_inputs(case, workdir, route.name, fpkm, meta)
    gates(case, spec=spec, inputs=inputs, matrix_type="FPKM", n=len(meta),
          design={"analysis_type": "two-arm", "design_column": "grp", "control": "ctrl", "treatment": "trt"},
          covariance={"status": "not_required", "blocking_terms": [], "covariates": []},
          method={"method": "limma", "transform": "log2(x+1)"})
    log_path = workdir / route.name / "matrix_log2.csv"
    native.log_transform(inputs[0]["path"], log_path)
    out = workdir / route.name / "results"
    result = call(route, case, spec, "limma", "tools.limma_tools:run_limma_analysis",
                  normalized_csv=str(log_path), metadata_csv=inputs[1]["path"], design_column="grp",
                  control_group="ctrl", treatment_group="trt", output_dir=str(out))
    if result is None:
        return route
    deg = native.deg_outputs(out)[0]
    judge(route, recovery(deg, pd.Series(np.sign(effect), index=fpkm.index)))
    complete(case, route, "limma", deg)
    return route


def route_multilevel(run, workdir, rng) -> Route:
    route, case = Route("limma_multilevel"), run.case("limma_multilevel", "SYNTHETIC")
    expr, meta, effects = multilevel(rng)
    spec, *inputs = stage_inputs(case, workdir, route.name, expr, meta)
    contrasts = [{"name": f"{lv}_vs_ctrl", "coefficients": {f"C(grp)[{lv}]": 1, "C(grp)[ctrl]": -1}}
                 for lv in ("t1", "t2", "t3")]
    gates(case, spec=spec, inputs=inputs, matrix_type="log2 expression", n=len(meta),
          design={"analysis_type": "multilevel", "formula": "~ 0 + C(grp)", "design_column": "grp",
                  "contrasts": [c["name"] for c in contrasts]},
          covariance={"status": "not_required", "blocking_terms": [], "covariates": []},
          method={"method": "limma", "formula": "~ 0 + C(grp)"})
    out = workdir / route.name / "results"
    plan = {"analysis_type": "multilevel", "formula": "~ 0 + C(grp)", "contrasts": contrasts}
    result = call(route, case, spec, "limma", "tools.multigroup_tools:run_multigroup_analysis",
                  expression_csv=inputs[0]["path"], metadata_csv=inputs[1]["path"], plan=plan,
                  output_dir=str(out))
    if result is None:
        return route
    worst = None
    for level in ("t1", "t2", "t3"):
        deg = str(out / f"DEG_results_{level}_vs_ctrl.csv")
        metrics = recovery(deg, pd.Series(np.sign(effects[level]), index=expr.index))
        route.metrics[level] = metrics
        if worst is None or metrics["sensitivity"] < worst["sensitivity"]:
            worst = metrics
    judge(route, dict(worst))
    complete(case, route, "limma", str(out / "DEG_results_t2_vs_ctrl.csv"))
    return route


def route_methylation(run, workdir, rng) -> Route:
    route, case = Route("methylation_beta_to_m"), run.case("methylation_beta_to_m", "SYNTHETIC")
    beta, meta, sign = methylation(rng)
    spec, *inputs = stage_inputs(case, workdir, route.name, beta, meta)
    m_path = workdir / route.name / "mvalues_native.csv"
    native.beta_to_m(inputs[0]["path"], m_path)
    gates(case, spec=spec, inputs=inputs, matrix_type="methylation beta", n=len(meta),
          design={"analysis_type": "two-arm", "design_column": "grp", "control": "ctrl", "treatment": "trt"},
          covariance={"status": "not_required", "blocking_terms": [], "covariates": []},
          method={"method": "limma", "transform": "beta-to-M"})
    out = workdir / route.name / "results"
    result = call(route, case, spec, "limma", "tools.methylation_tools:run_methylation_da",
                  beta_matrix_csv=inputs[0]["path"], metadata_csv=inputs[1]["path"], design_column="grp",
                  control_group="ctrl", treatment_group="trt", output_dir=str(out))
    if result is None:
        return route
    deg = native.deg_outputs(out)[0]
    judge(route, recovery(deg, pd.Series(sign, index=beta.index)))
    complete(case, route, "limma", deg)
    return route


def route_proteomics(run, workdir, rng) -> Route:
    route, case = Route("proteomics_label_free"), run.case("proteomics_label_free", "SYNTHETIC")
    table, meta, effect = proteomics(rng)
    spec, *inputs = stage_inputs(case, workdir, route.name, table, meta, index_matrix=False)
    out = workdir / route.name / "results"
    out.mkdir(parents=True, exist_ok=True)
    gates(case, spec=spec, inputs=inputs, matrix_type="linear LFQ intensity", n=len(meta),
          design={"analysis_type": "two-arm", "design_column": "grp", "control": "ctrl", "treatment": "trt"},
          covariance={"status": "not_required", "blocking_terms": [], "covariates": []},
          method={"method": "limma", "transform": "log2, missingness filter 50%, MinProb imputation, median centering"})
    result = call(route, case, spec, "proteomics preprocessing", "tools.proteomics_tools:preprocess_proteomics_matrix",
                  quant_path=inputs[0]["path"], labeling="label_free", output_dir=str(out))
    if result is None:
        return route
    preprocessed = next(out.glob("*_preprocessed.csv"))
    route.metrics["preprocessed_profile"] = {k: native.profile_matrix(preprocessed)[k]
                                             for k in ("n_features", "n_samples", "max", "missing_values")}
    result = call(route, case, spec, "limma", "tools.limma_tools:run_limma_analysis",
                  normalized_csv=str(preprocessed), metadata_csv=inputs[1]["path"], design_column="grp",
                  control_group="ctrl", treatment_group="trt", output_dir=str(out))
    if result is None:
        if route.status == "SKIP":
            route.detail = "preprocessing PASS; limma " + route.detail
        return route
    deg = native.deg_outputs(out)[0]
    judge(route, recovery(deg, pd.Series(np.sign(effect.values), index=effect.index)))
    complete(case, route, "limma", deg)
    return route


def route_single_cell(run, workdir, rng) -> Route:
    route, case = Route("single_cell_paired_pseudobulk"), run.case("single_cell_paired_pseudobulk", "SYNTHETIC")
    counts, cells, effect = single_cell(rng)
    spec, *inputs = stage_inputs(case, workdir, route.name, counts, cells)
    gates(case, spec=spec, inputs=inputs, matrix_type="single-cell raw UMI counts", n=len(cells),
          design={"analysis_type": "paired donors, per cell type", "design_column": "condition",
                  "formula": "~ sample + condition", "control": "ctrl", "treatment": "stim"},
          covariance={"status": "required", "blocking_terms": ["sample"], "covariates": []},
          method={"method": "limma", "transform": "log2(CPM+1) of pseudobulk", "formula": "~ sample + condition"})
    dropped: dict = {}
    manifest = call(route, case, spec, "pseudobulk aggregation", "tools.scrna_tools:aggregate_pseudobulk",
                    matrix_path=inputs[0]["path"], sample_col="donor", celltype_col="cell_type",
                    condition_col="condition", cell_metadata_path=inputs[1]["path"], min_cells=10,
                    output_dir=str(workdir / route.name / "pseudobulk"), report=dropped)
    if manifest is None:
        return route
    entry = manifest["typeA"]
    route.metrics["pseudobulk"] = {ct: {"n_pb_samples": v["n_pb_samples"], "conditions": v["conditions"]}
                                   for ct, v in manifest.items()}
    norm_dir = workdir / route.name / "typeA_preprocess"
    result = call(route, case, spec, "preprocess_counts", "tools.preprocess_tools:preprocess_counts",
                  counts_csv=entry["counts_csv"], output_dir=str(norm_dir), min_count=1, min_samples=1)
    if result is None:
        return route
    normalized = next(norm_dir.glob("*_normalized.csv"))
    out = workdir / route.name / "typeA_results"
    result = call(route, case, spec, "limma", "tools.limma_tools:run_limma_analysis",
                  normalized_csv=str(normalized), metadata_csv=entry["metadata_csv"], design_column="condition",
                  control_group="ctrl", treatment_group="stim", output_dir=str(out),
                  design_formula="~ C(sample) + Treatment", coefficient="Treatment")
    if result is None:
        if route.status == "SKIP":
            route.detail = "pseudobulk aggregation PASS; limma " + route.detail
        return route
    deg = native.deg_outputs(out)[0]
    judge(route, recovery(deg, pd.Series(np.sign(effect), index=counts.index)))
    complete(case, route, "limma", deg)
    return route


def route_enrichment(workdir, rng, network: bool) -> Route:
    """Connectivity check of GSEA and ORA on real human symbols (not recorded as a case)."""
    route = Route("gsea_and_ora")
    if not network:
        return route.skip("network checks not requested (use --network)")
    genes = INTERFERON + FILLER
    stat = np.r_[rng.normal(8, 1, len(INTERFERON)), rng.normal(0, 1, len(FILLER))]
    deg_table = pd.DataFrame({"log2FoldChange": stat / 4, "stat": stat,
                              "pvalue": np.where(stat > 4, 1e-6, 0.5), "padj": np.where(stat > 4, 1e-5, 0.8)},
                             index=pd.Index(genes, name="gene"))
    folder = workdir / route.name
    folder.mkdir(parents=True, exist_ok=True)
    deg = folder / "DEG_results_ifn_vs_ctrl.csv"
    deg_table.to_csv(deg)
    ids = native.feature_id_report(deg)
    route.metrics["feature_ids"] = {k: ids[k] for k in ("dominant_type", "gene_set_ready")}
    for method, tool, kwargs in (
            ("GSEA", "tools.enrichment_tools:run_gsea_analysis",
             {"deg_csv": str(deg), "organism": "Human", "ranking_metric": "stat", "output_dir": str(folder / "gsea")}),
            ("ORA", "tools.enrichment_tools:run_enrichment_analysis",
             {"deg_csv": str(deg), "organism": "Human", "padj_cutoff": 0.05, "log2fc_cutoff": 0.0,
              "output_dir": str(folder / "ora")})):
        try:
            native.call_tool(tool, **kwargs)
        except native.NativeToolError as error:
            text = str(error)
            if text.startswith("cannot import") or "No module named" in text:
                return route.skip(f"missing package: {text.split(':', 2)[-1].strip()[:160]}")
            return route.fail(f"{method}: {text[:300]}")
        route.metrics[method] = "completed"
    return route


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Self-test of the workflow skill on this machine.")
    parser.add_argument("--out", type=Path, default=None)
    parser.add_argument("--network", action="store_true", help="also run GSEA and ORA (needs network)")
    parser.add_argument("--require-all", action="store_true", help="treat skipped routes as failures")
    args = parser.parse_args(argv)
    stamp = datetime.now().strftime("%Y%m%dT%H%M%S")
    run_dir = args.out or ROOT / "output" / f"skill_selftest_{stamp}"
    workdir = run_dir / "_inputs"

    native.enable_native_mode()
    run = native.RunRecorder(run_dir, request="skill self-test", platform_name="selftest",
                             decision_maker="scripts/skill_selftest.py (fixed plans)")
    rng = np.random.default_rng(20261011)
    routes = []
    for check in (route_deseq2_paired, route_limma_fpkm, route_multilevel, route_methylation,
                  route_proteomics, route_single_cell):
        try:
            routes.append(check(run, workdir, rng))
        except Exception as exc:  # report the route, continue with the others
            routes.append(Route(check.__name__.replace("route_", "")).fail(f"{type(exc).__name__}: {exc}"))
    try:
        routes.append(route_enrichment(workdir, rng, args.network))
    except Exception as exc:
        routes.append(Route("gsea_and_ora").fail(f"{type(exc).__name__}: {exc}"))
    finished = run.finish()

    n_records, contract_errors = decision_contract.validate(sorted(run_dir.glob("*/decisions.json")))
    audit = {}
    if AUDIT_SCRIPT.exists():
        audit_module = runpy.run_path(str(AUDIT_SCRIPT))
        report = audit_module["audit_run"](run_dir)
        audit = {k: report.get(k) for k in ("verdict", "score", "coverage", "blocking_findings",
                                             "environment_blocked")}
    checks = {
        "decision_contract": {"records": n_records, "errors": contract_errors},
        "external_llm_attempts": finished["external_llm_blocked_attempts"],
        "audit": audit,
    }
    failed = [r for r in routes if r.status == "FAIL"]
    skipped = [r for r in routes if r.status == "SKIP"]
    infra_ok = not contract_errors and finished["external_llm_blocked_attempts"] == 0
    report = {
        "run_dir": str(run_dir),
        "packages": native.package_versions(),
        "routes": [r.as_dict() for r in routes],
        "checks": checks,
        "result": "FAIL" if failed or not infra_ok or (args.require_all and skipped) else
                  "PASS_WITH_SKIPS" if skipped else "PASS",
    }
    (run_dir / "selftest_report.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    width = max(len(r.name) for r in routes)
    for r in routes:
        print(f"{r.name:<{width}}  {r.status:<4}  {r.detail}")
    print(f"decision contract: {n_records} records, {len(contract_errors)} errors; "
          f"external LLM attempts: {finished['external_llm_blocked_attempts']}; audit: {audit.get('verdict')}")
    print(f"result: {report['result']}  ({run_dir / 'selftest_report.json'})")
    return 1 if report["result"] == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
