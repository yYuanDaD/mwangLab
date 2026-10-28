"""Fixed executor for native runs: the agent writes one case spec, this runs the rest.

The 45-paper run showed that about 40% of each paper's tokens went to re-reading the
skill and ``tools/native.py`` and to writing the same driver scripts again. Here the
agent only makes the decisions, in a JSON case spec; the mechanical steps are fixed:

    python -m tools.case_runner inspect GSE123456 --out <run_dir>/inspect_GSE123456.json
    python -m tools.case_runner execute <run_dir>/case_spec.json
    python -m tools.case_runner template          # print an example spec

``inspect`` downloads the series (skipped when cached), lists candidate matrices with
their numeric profile, summarizes the metadata columns, and reports which metadata
column matches the matrix column names. It records nothing.

``execute`` validates the spec, then for each case: registers inputs, records the
paper_reconstruction / ownership gates, aligns the matrix to the metadata and derives
formula-safe columns, profiles the matrix, runs the suitability report, design check
and confounding report, applies the stated transform, runs every listed executor,
applies the applied (and audit) threshold, looks up the paper's named genes, runs
ORA/GSEA, records the study, finishes the run and validates the decision contract.
Every decision record is the agent's ``final`` + ``reasoning`` plus the computed facts.

A gate with ``decision_status`` other than ``valid`` is recorded and stops that case.
Rerunning ``execute`` moves the previous attempt's records to ``<run_dir>/_previous/``
(nothing is deleted), so a spec can be fixed and run again.
"""

from __future__ import annotations

import argparse
import contextlib
import inspect
import json
import math
import re
import shutil
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal, Optional

import pandas as pd
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from tools import decision_contract, native
from tools.analysis_policy import numeric_matrix

Confidence = Literal["high", "medium", "low"]
Status = Literal["valid", "unresolved", "manual_review", "refused"]
MATRIX_KWARGS = ("counts_csv", "normalized_csv", "expression_csv")
Transform = Literal["log2(x+1)", "log2(CPM+1)", "beta_to_m", "round"]
RECORD_FILES = ("run_manifest.json", "run_status.json", "summary.csv", "workflow.log")
_EXTENSIONS = (".csv", ".tsv", ".txt", ".csv.gz", ".tsv.gz", ".txt.gz", ".xlsx")


# ---------------------------------------------------------------- spec


class Gate(BaseModel):
    """One decision gate: the agent's choice and why. Computed facts are added by the runner."""
    model_config = ConfigDict(extra="forbid")
    final: dict[str, Any] = Field(default_factory=dict)
    reasoning: str
    confidence: Confidence = "high"
    locator: Optional[str] = None
    candidates: list[dict] = Field(default_factory=list)
    decision_status: Status = "valid"
    stop_reason: Optional[str] = None

    @model_validator(mode="after")
    def _stop_reason(self):
        if self.decision_status != "valid" and not self.stop_reason:
            raise ValueError("a gate that is not valid needs stop_reason")
        return self


class AlignmentGate(Gate):
    key_column: Optional[str] = None
    aliases: dict[str, str] = Field(default_factory=dict)
    patterns: dict[str, tuple[str, str]] = Field(default_factory=dict)
    combine: dict[str, list[str]] = Field(default_factory=dict)
    recode: dict[str, dict[str, str]] = Field(default_factory=dict)
    key_patterns: dict[str, tuple[str, str]] = Field(
        default_factory=dict, description="derive the key_column itself from metadata before aligning")
    exclude_samples: dict[str, str] = Field(default_factory=dict, description="sample id -> reason")


class MatrixGate(Gate):
    matrix_type: str
    recommended_method: str


class DesignGate(Gate):
    factors: list[str] = Field(default_factory=list)
    references: dict[str, str] = Field(default_factory=dict)
    subject: Optional[str] = None
    covariate_candidates: Optional[list[str]] = None
    organism: str = "Mouse"
    planned: list[str] = Field(default_factory=list)
    strata: list[str] = Field(
        default_factory=list, description="columns analyzed separately (e.g. cell fraction); comparisons stay within one")


class CovarianceGate(Gate):
    confounding_candidates: Optional[list[str]] = None


class MethodGate(Gate):
    transform: Optional[Transform] = None
    pseudocount: float = 1.0


class Execution(BaseModel):
    model_config = ConfigDict(extra="forbid")
    name: str
    tool: str = Field(description="module:function, for example tools.deseq2_tools:run_deseq2_analysis")
    args: dict[str, Any] = Field(default_factory=dict)
    matrix: Literal["analysis", "aligned"] = "analysis"
    transform: Optional[Transform] = Field(
        None, description="transform for this execution only (applied to the aligned matrix after subsetting)")
    subset: dict[str, list[str]] = Field(default_factory=dict, description="column -> kept values")
    complete_pairs: Optional[dict[str, Any]] = Field(
        None, description="{subject, condition, levels}: keep subjects with one sample at every level")
    role: str = "primary"
    reasoning: str = ""
    confidence: Confidence = "high"


class Enrichment(BaseModel):
    model_config = ConfigDict(extra="forbid")
    execution: str = Field(description="name of an execution, or execution/comparison for joint models")
    ora: bool = True
    gsea: bool = True
    direction: Literal["all", "up", "down"] = "all"
    ranking_metric: str = "stat"
    reasoning: str = ""
    ortholog_mapping: Optional[str] = None


class StudyGate(Gate):
    paper_counts: dict[str, Any] = Field(default_factory=dict, description="execution name -> paper's DEG count")
    paper_genes: dict[str, list[str]] = Field(default_factory=dict, description="execution name -> genes to look up")


class Inputs(BaseModel):
    model_config = ConfigDict(extra="forbid")
    paper: list[str] = Field(default_factory=list)
    metadata: str
    matrix: Optional[str] = None
    raw_tar: bool = False
    prep_scripts: list[str] = Field(default_factory=list)

    @model_validator(mode="after")
    def _one_matrix(self):
        if bool(self.matrix) == self.raw_tar:
            raise ValueError("give exactly one of inputs.matrix or inputs.raw_tar: true")
        return self


class Gates(BaseModel):
    model_config = ConfigDict(extra="forbid")
    paper_reconstruction: Gate
    ownership: Gate
    alignment: Optional[AlignmentGate] = None
    matrix: Optional[MatrixGate] = None
    design: Optional[DesignGate] = None
    covariance: Optional[CovarianceGate] = None
    method: Optional[MethodGate] = None
    threshold: Optional[Gate] = None
    study: Optional[StudyGate] = None


class Case(BaseModel):
    model_config = ConfigDict(extra="forbid")
    case_id: str
    accession: str
    inputs: Inputs
    gates: Gates
    discrepancies: list[dict] = Field(default_factory=list)
    executions: list[Execution] = Field(default_factory=list)
    enrichment: list[Enrichment] = Field(default_factory=list)

    @model_validator(mode="after")
    def _complete(self):
        order = ["paper_reconstruction", "ownership", "alignment", "matrix", "design", "covariance",
                 "method", "threshold", "study"]
        gates = {name: getattr(self.gates, name) for name in order}
        for i, name in enumerate(order):
            gate = gates[name]
            if gate is None:
                earlier_stop = any(gates[n] is not None and gates[n].decision_status != "valid" for n in order[:i])
                if not earlier_stop:
                    raise ValueError(f"case {self.case_id}: gate {name!r} is missing and no earlier gate stops")
            elif gate.decision_status != "valid":
                break
        stopped = any(g is not None and g.decision_status != "valid" for g in gates.values())
        if not stopped and not self.executions:
            raise ValueError(f"case {self.case_id}: no executions listed")
        names = [e.name for e in self.executions]
        if len(names) != len(set(names)):
            raise ValueError(f"case {self.case_id}: execution names must be unique")
        return self


class Spec(BaseModel):
    model_config = ConfigDict(extra="forbid")
    run_dir: str
    request: str
    decision_maker: str
    platform: str = "claude-code"
    data_root: Optional[str] = Field(
        None, description="relative inputs.metadata / inputs.matrix are read from here, e.g. GSE1/GSE1_metadata.csv")
    cases: list[Case]

    @model_validator(mode="after")
    def _resolve_inputs(self):
        if self.data_root:
            for case in self.cases:
                for field in ("metadata", "matrix"):
                    value = getattr(case.inputs, field)
                    if value and not Path(value).is_absolute():
                        setattr(case.inputs, field, str(Path(self.data_root) / value))
        return self


# ---------------------------------------------------------------- inspect


def _short(value: Any, n: int = 80) -> str:
    text = re.sub(r"\s+", " ", str(value))
    return text if len(text) <= n else text[: n - 3] + "..."


def metadata_summary(metadata_csv: str | Path, *, max_levels: int = 12) -> dict:
    """Compact view of GEO metadata: grouping-like columns with counts, the rest by shape."""
    meta = pd.read_csv(metadata_csv, index_col=0)
    grouping, identifiers, constant, other = {}, {}, {}, {}
    for column in meta.columns:
        values = meta[column].dropna().astype(str)
        n = values.nunique()
        if n == 0:
            continue
        if n == 1:
            keep = 400 if any(k in column for k in ("data_processing", "protocol", "description")) else 100
            constant[column] = _short(values.iloc[0], keep)
        elif n == len(meta):
            identifiers[column] = [_short(v, 60) for v in values.iloc[:3]]
        elif n <= max_levels:
            grouping[column] = {_short(k): int(v) for k, v in values.value_counts().items()}
        else:
            other[column] = {"n_levels": int(n), "examples": [_short(v, 60) for v in values.iloc[:3]]}
    return {"n_samples": int(len(meta)), "sample_ids": [str(s) for s in meta.index[:4]],
            "grouping_columns": grouping, "per_sample_columns": identifiers,
            "constant_columns": constant, "other_columns": other}


def _key_matches(columns: list[str], meta: pd.DataFrame) -> list[dict]:
    """Which metadata column (or the index) equals the matrix column names, also as file basenames."""
    cols = set(map(str, columns))
    candidates = {"(index)": meta.index.astype(str)}
    for column in meta.columns:
        values = meta[column].dropna().astype(str)
        if values.nunique() == len(meta):
            candidates[column] = values
            base = values.map(lambda v: re.sub(r"(\.(txt|tsv|csv|tab|bam))?(\.gz)?$", "", v.rsplit("/", 1)[-1]))
            if not base.equals(values) and base.nunique() == len(meta):
                candidates[f"{column} (file basename)"] = base
    # GEO tar members are named GSM<id>_<label>; execute renames such columns to the GSM id.
    gsm = {re.match(r"(GSM\d+)_", c).group(1) for c in cols if re.match(r"(GSM\d+)_", c)}
    if len(gsm) == len(cols):
        cols = gsm
    out = []
    for name, values in candidates.items():
        hits = int(values.isin(cols).sum())
        if hits:
            out.append({"key": name, "matched": hits, "of_metadata": int(len(meta)), "of_matrix": len(cols)})
    if not any(d["matched"] == len(cols) for d in out):
        out += _contained_keys(cols, meta)
    return sorted(out, key=lambda d: -d["matched"])


def _contained_keys(cols: set[str], meta: pd.DataFrame) -> list[dict]:
    """Metadata columns whose text holds exactly one matrix column name as a whole token
    (``Library name: CN2``): derive the key with ``alignment.key_patterns``."""
    out = []
    names = sorted(cols, key=len, reverse=True)
    for column in meta.columns:
        values = meta[column].dropna().astype(str)
        if values.nunique() != len(meta):
            continue
        found = {}
        for idx, text in values.items():
            hit = [c for c in names if re.search(rf"(?<![A-Za-z0-9]){re.escape(c)}(?![A-Za-z0-9])", text)]
            if len(hit) == 1:
                found[idx] = hit[0]
        if len(found) >= max(2, len(meta) // 2) and len(set(found.values())) == len(found):
            example = next(iter(found))
            out.append({"key": f"{column} (contains the name)", "matched": len(found),
                        "of_metadata": int(len(meta)), "of_matrix": len(cols),
                        "example": {"value": _short(values[example], 80), "matrix_column": found[example]},
                        "use": f'alignment.key_patterns {{"key": ["{column}", "<regex with one group>"]}}, '
                               'then key_column "key"'})
    return out


def _candidate_files(data_dir: Path) -> list[Path]:
    files = [p for p in sorted(data_dir.iterdir()) if p.is_file()
             and p.name.lower().endswith(_EXTENSIONS) and "metadata" not in p.name.lower()]
    return files


def inspect_series(accession: str, *, data_root: str = "data", merge_tar: bool = False,
                   download: bool = True) -> dict:
    """Facts the agent needs before writing a spec. Downloads only what is not cached."""
    native.enable_native_mode()
    data_dir = Path(data_root) / accession
    notes = []
    if download:
        for tool in ("tools.geo_tools:download_geo_data", "tools.geo_tools:download_supplementary_files"):
            try:
                native.call_tool(tool, geo_accession=accession)
            except native.NativeToolError as exc:
                notes.append(f"{tool.split(':')[1]}: {_short(exc, 300)}")
    metadata_csv = data_dir / f"{accession}_metadata.csv"
    if not metadata_csv.exists():
        return {"accession": accession, "error": f"no metadata at {metadata_csv}", "notes": notes}
    meta = pd.read_csv(metadata_csv, index_col=0)
    meta.index = meta.index.astype(str)
    files = [{"file": p.name, "bytes": p.stat().st_size} for p in sorted(data_dir.iterdir()) if p.is_file()]
    tars = [p for p in data_dir.glob("*_RAW.tar")]
    matrices = []
    paths = _candidate_files(data_dir)
    if tars and (merge_tar or not paths):
        try:
            merged = native.merge_raw_tar(data_dir)
            paths.append(Path(merged["output"]))
            notes.append(f"merged {tars[0].name}: {merged['n_genes']} genes x {merged['n_samples']} samples")
        except native.NativeToolError as exc:
            notes.append(f"merge_raw_tar: {_short(exc, 300)}")
    for path in dict.fromkeys(paths):
        entry: dict[str, Any] = {"file": str(path)}
        try:
            prof = native.profile_matrix(path)
            entry.update({k: prof[k] for k in ("n_features", "n_samples", "integer_fraction", "min", "max",
                                                "median", "missing_values", "duplicated_feature_ids",
                                                "candidates")})
            entry["annotation_columns"] = prof["annotation_columns_dropped"][:8]
            entry["sample_columns"] = prof["sample_columns"][:6] + (["..."] if prof["n_samples"] > 6 else [])
            entry["feature_examples"] = native.feature_id_report(path)["examples"]
            entry["alignment_keys"] = _key_matches(prof["sample_columns"], meta)
        except Exception as exc:  # an unreadable file is a fact to report, not a crash
            entry["error"] = _short(f"{type(exc).__name__}: {exc}", 300)
        matrices.append(entry)
    return {"accession": accession, "data_dir": str(data_dir), "files": files, "matrices": matrices,
            "metadata_csv": str(metadata_csv), "metadata": metadata_summary(metadata_csv), "notes": notes}


# ---------------------------------------------------------------- execute helpers


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _move_previous_attempt(run_dir: Path, case_ids: list[str]) -> Optional[Path]:
    """Move an earlier attempt's records aside so RunRecorder can start fresh. Deletes nothing."""
    present = [run_dir / f for f in RECORD_FILES if (run_dir / f).exists()]
    present += [run_dir / c for c in case_ids if (run_dir / c).is_dir()]
    if not present:
        return None
    target = run_dir / "_previous" / _now()
    target.mkdir(parents=True, exist_ok=True)
    for path in present:
        shutil.move(str(path), str(target / path.name))
    return target


def _signature(tool: str) -> set[str]:
    obj = native.load_tool(tool)
    function = getattr(obj, "func", None) or obj
    return set(inspect.signature(function).parameters)


def _group_n(meta: pd.DataFrame, args: dict) -> Optional[int]:
    column = args.get("design_column")
    if not column or column not in meta.columns:
        return None
    values = meta[column].astype(str)
    sizes = [int((values == str(args[k])).sum()) for k in ("control_group", "treatment_group") if args.get(k)]
    return min(sizes) if sizes else None


def _threshold_kwargs(rule: dict) -> dict:
    metric = decision_contract._metric(rule.get("metric", "padj"))
    return {"metric": "pvalue" if metric == "pvalue" else "padj", "cutoff": float(rule.get("cutoff", 0.05)),
            "effect_cutoff": rule.get("effect_cutoff"), "inclusive": bool(rule.get("inclusive", False))}


def _gene_lookup(deg_csv: str, genes: list[str], organism: str = "Mouse") -> dict:
    table = pd.read_csv(deg_csv, index_col=0)
    upper = {str(i).upper(): i for i in table.index}
    if genes and not any(g.upper() in upper for g in genes) and             str(table.index[0]).upper().startswith("ENS"):
        # Ensembl-indexed table: paper genes are symbols, so map the index to symbols first.
        from tools import enrichment_tools
        stripped = {str(i).split(".")[0]: i for i in table.index}
        species = "rat" if organism.lower() == "rat" else ("human" if organism.lower() == "human" else "mouse")
        try:
            symbols = enrichment_tools._query_symbols(list(stripped), species)
        except Exception:
            symbols = {}
        for ens, sym in symbols.items():
            if sym and str(sym).upper() not in upper:
                upper[str(sym).upper()] = stripped[ens]
    cols = [c for c in ("baseMean", "AveExpr", "log2FoldChange", "logFC", "padj", "adj.P.Val", "pvalue")
            if c in table.columns]
    out = {}
    for gene in genes:
        key = upper.get(gene.upper())
        out[gene] = (None if key is None else
                     {c: (None if pd.isna(v) else round(float(v), 4)) for c, v in table.loc[key, cols].items()})
    return out


class CaseRun:
    """Runs one case of a spec against an open RunRecorder."""

    def __init__(self, run: native.RunRecorder, spec: Case):
        self.spec = spec
        self.case = run.case(spec.case_id, accession=spec.accession)
        self.items: dict[str, dict] = {}
        self.outputs: dict[str, dict] = {}   # execution or execution/comparison -> threshold result
        self.result: dict[str, Any] = {"case_id": spec.case_id, "accession": spec.accession}

    # -- recording
    def decide(self, stage: str, gate: Gate, final: dict, evidence: list[dict], **kwargs) -> bool:
        """Record a gate; return False when it stops the case."""
        status = gate.decision_status
        self.case.decide(stage, final=final, evidence=[e for e in evidence if e], reasoning=gate.reasoning,
                         confidence=gate.confidence, decision_status=status, candidates=gate.candidates,
                         stop_reason=gate.stop_reason, paper={"locator": gate.locator} if gate.locator else None,
                         **kwargs)
        if status != "valid":
            self.result["stopped"] = {"stage": stage, "decision_status": status, "stop_reason": gate.stop_reason}
            return False
        return True

    def run(self) -> dict:
        s, g, case = self.spec, self.spec.gates, self.case
        papers = [case.add_input(p, "paper") for p in s.inputs.paper]
        meta_item = case.add_input(s.inputs.metadata, "metadata")
        for script in s.inputs.prep_scripts:
            case.add_input(script, "user", label=f"prep script {Path(script).name}")
        matrix_path = self._matrix_input()
        matrix_item = case.add_input(matrix_path, "matrix")
        paper_ev = papers or [meta_item]

        case.write_json("paper_reconstruction.json", g.paper_reconstruction.final)
        case.write_json("paper_data_discrepancies.json", s.discrepancies)
        if not self.decide("paper_reconstruction", g.paper_reconstruction, g.paper_reconstruction.final, paper_ev):
            return self._finish()
        own = {"matrix_file": str(matrix_path), **g.ownership.final, "accession": s.accession,
               "metadata_file": s.inputs.metadata}
        if not self.decide("ownership", g.ownership, own, [meta_item, matrix_item, *papers]):
            return self._finish()

        # alignment
        a = g.alignment
        adir = case.dir / "aligned"
        metadata = Path(s.inputs.metadata)
        if a.key_patterns:
            keyed = native.derive_columns(metadata, adir / "metadata_keyed.csv", patterns=a.key_patterns)
            metadata = Path(keyed["output"])
        aln = native.align_to_metadata(matrix_path, metadata, adir, key_column=a.key_column)
        aligned_meta = Path(aln["outputs"]["aligned_metadata"]["path"])
        if a.exclude_samples:
            kept = pd.read_csv(aligned_meta, index_col=0)
            unknown = sorted(set(a.exclude_samples) - set(kept.index.astype(str)))
            if unknown:
                raise native.NativeToolError(f"alignment.exclude_samples not in the aligned metadata: {unknown}")
            kept = kept.loc[[i for i in kept.index.astype(str) if i not in a.exclude_samples]]
            aligned_meta = adir / "aligned_metadata_kept.csv"
            kept.to_csv(aligned_meta)
        derived = native.derive_columns(aligned_meta, adir / "design_metadata.csv", aliases=a.aliases,
                                        patterns=a.patterns, combine=a.combine, recode=a.recode)
        self.dm_path = adir / "design_metadata.csv"
        self.mat_path = Path(aln["outputs"]["aligned_matrix"]["path"])
        self.dm = pd.read_csv(self.dm_path, index_col=0)
        self.dm.index = self.dm.index.astype(str)
        mat_item = case.add_output(self.mat_path, "aligned_matrix")
        dm_item = case.add_output(self.dm_path, "design_metadata")
        map_item = case.add_output(aln["outputs"]["alignment_map"]["path"], "alignment_map")
        self.items.update(matrix=mat_item, design_metadata=dm_item)
        # computed facts last: the spec explains them, it cannot overwrite them
        align_final = {**a.final, "method": aln["method"], "n_aligned": aln["n_aligned"],
                       "n_metadata": aln["n_metadata"], "coverage": aln["coverage"],
                       "unmatched_matrix_columns": aln["unmatched_matrix_columns"],
                       "unmatched_metadata_samples": aln["unmatched_metadata_samples"],
                       "excluded_samples": a.exclude_samples, "derived_columns": derived}
        self.result["alignment"] = {k: align_final[k] for k in ("method", "n_aligned", "n_metadata", "coverage")}
        self.result["levels"] = derived.get("levels")
        if not self.decide("alignment", a, align_final, [matrix_item, meta_item, mat_item, dm_item, map_item]):
            return self._finish()

        m = g.matrix
        prof = native.profile_matrix(self.mat_path, sample_columns=list(self.dm.index))
        prof = {k: v for k, v in prof.items() if k not in ("sample_columns", "note")}
        matrix_final = {**m.final, "matrix_type": m.matrix_type, "recommended_method": m.recommended_method,
                        "profile": prof}
        if not self.decide("matrix", m, matrix_final, [mat_item, meta_item, *papers]):
            return self._finish()

        # design (suitability report first: a valid design needs its verdict)
        d = g.design
        rep, suit_item, summary = case.suitability(
            matrix_type=m.matrix_type, metadata=self.dm, factors=d.factors, matrix_csv=str(self.mat_path),
            organism=d.organism, subject=d.subject, covariate_candidates=d.covariate_candidates,
            references=d.references or None, planned=d.planned, strata=d.strata)
        self.comparisons = rep["comparisons"]
        self.result["suitability"] = summary
        design_final = {**d.final, "suitability": summary}
        if not self.decide("design", d, design_final, [*paper_ev, dm_item, suit_item]):
            return self._finish()

        c = g.covariance
        terms = list(dict.fromkeys(d.factors + [str(t) for t in c.final.get("blocking_terms") or []
                                                 if str(t) in self.dm.columns]))
        primary = d.final.get("design_column") or (d.factors[0] if d.factors else None)
        cov_final = dict(c.final)
        if terms:
            cov_final["design_check"] = native.design_check(self.dm, terms)
        if primary in self.dm.columns:
            cov_final["confounding"] = native.confounding_report(self.dm, primary, candidates=c.confounding_candidates)
        if not self.decide("covariance", c, cov_final, [dm_item, meta_item, *papers]):
            return self._finish()

        me = g.method
        self.analysis_path = self._transform(self.mat_path, me.transform, case.dir / "transformed", me.pseudocount)
        method_final = {"matrix_type": m.matrix_type, **me.final}
        if me.transform:
            method_final.setdefault("transform", me.transform)
        if not self.decide("method", me, method_final, [mat_item, *paper_ev]):
            return self._finish()

        t = g.threshold
        self.applied = t.final.get("applied_threshold") or {}
        self.audit = t.final.get("audit_threshold")
        if not self.decide("threshold", t, t.final, paper_ev):
            return self._finish()

        for execution in s.executions:
            self._execute(execution)
        for enrichment in s.enrichment:
            self._enrich(enrichment)
        self._study(g.study, paper_ev, mat_item)
        return self._finish()

    # -- steps
    def _matrix_input(self) -> Path:
        inputs = self.spec.inputs
        if inputs.matrix:
            return Path(inputs.matrix)
        merged = native.merge_raw_tar(Path(inputs.metadata).parent)
        self.result["raw_tar"] = {k: merged[k] for k in ("output", "n_genes", "n_samples")}
        # Tar members are named GSM<id>_<label>; keep the GSM id so exact alignment to the
        # metadata index works. Written in the case dir; the cached merge stays untouched.
        gsm = [re.match(r"(GSM\d+)_", c) for c in merged["samples"]]
        if not all(gsm) or len({m.group(1) for m in gsm}) != len(gsm):
            return Path(merged["output"])
        table = native.read_table(merged["output"])
        table.columns = [m.group(1) for m in gsm]
        path = self.case.dir / "input" / "merged_from_tar_gsm.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(path)
        self.result["raw_tar"]["renamed_to_gsm"] = str(path)
        return path

    def _transform(self, source: Path, transform: Optional[str], tdir: Path, pseudocount: float = 1.0) -> Path:
        if transform == "log2(x+1)":
            path = tdir / "log2_matrix.csv"
            native.log_transform(source, path, pseudocount=pseudocount)
        elif transform == "log2(CPM+1)":
            native.call_tool("tools.preprocess_tools:preprocess_counts", counts_csv=str(source),
                             output_dir=str(tdir))
            path = Path(native.find_outputs(tdir, "*_normalized.csv")[0])
        elif transform == "beta_to_m":
            path = tdir / "m_values.csv"
            native.beta_to_m(source, path)
        elif transform == "round":  # estimated counts; numpy rounds half to even, as R's round()
            path = tdir / "rounded_counts.csv"
            tdir.mkdir(parents=True, exist_ok=True)
            numeric_matrix(native.read_table(source), label=str(source)).round().astype(int).to_csv(path)
        else:
            return source
        self.case.add_output(path, "transformed_matrix")
        return path

    def _inputs_for(self, ex: Execution, out: Path) -> tuple[Path, Path, pd.DataFrame]:
        matrix = self.analysis_path if ex.matrix == "analysis" and not ex.transform else self.mat_path
        meta = self.dm
        if not ex.subset and not ex.complete_pairs:
            return self._transform(matrix, ex.transform, out / "input"), self.dm_path, meta
        idir = out / "input"
        idir.mkdir(parents=True, exist_ok=True)
        for column, values in ex.subset.items():
            if column not in meta.columns:
                raise native.NativeToolError(f"subset column {column!r} not in design metadata")
            meta = meta[meta[column].astype(str).isin([str(v) for v in values])]
        if meta.empty:
            raise native.NativeToolError(f"subset {ex.subset} keeps no sample")
        meta_path = idir / "metadata.csv"
        meta.to_csv(meta_path)
        table = native.read_table(matrix)
        table.columns = table.columns.astype(str)
        matrix_path = idir / "matrix.csv"
        table.loc[:, list(meta.index)].to_csv(matrix_path)
        if ex.complete_pairs:
            cp = ex.complete_pairs
            pairs = native.complete_pairs_subset(matrix_path, meta_path, cp["subject"], cp["condition"],
                                                 cp["levels"], idir / "paired")
            self.result.setdefault("pairs", {})[ex.name] = {k: pairs[k] for k in ("n_samples", "n_complete_pairs",
                                                                                 "excluded_subjects")}
            matrix_path, meta_path = Path(pairs["matrix"]), Path(pairs["metadata"])
            meta = pd.read_csv(meta_path, index_col=0)
        return self._transform(matrix_path, ex.transform, idir), meta_path, meta

    def _execute(self, ex: Execution) -> None:
        out = self.case.dir / "results" / ex.name
        final: dict[str, Any] = {"method": ex.args.get("method_label") or ex.tool.split(":")[1], "subset": ex.name,
                                 "role": ex.role, "tool": ex.tool}
        try:
            matrix, meta_path, meta = self._inputs_for(ex, out)
            params = _signature(ex.tool)
            kwargs = {k: v for k, v in ex.args.items() if k != "method_label"}
            matrix_kw = next((k for k in MATRIX_KWARGS if k in params), None)
            if matrix_kw is None:
                raise native.NativeToolError(f"{ex.tool} takes none of {MATRIX_KWARGS}")
            kwargs.update({matrix_kw: str(matrix), "metadata_csv": str(meta_path), "output_dir": str(out)})
            if "comparisons" in params:
                kwargs["comparisons"] = self._comparisons(kwargs.get("comparisons", "planned"))
            final.update(n_samples=int(len(meta)), matrix=str(matrix))
            transform = ex.transform or (self.spec.gates.method.transform if ex.matrix == "analysis" else None)
            if transform:
                final["transform"] = transform
            for key in ("formula", "design_formula"):
                if key in ex.args:
                    final["formula"] = ex.args[key]
            message = native.call_tool(ex.tool, **kwargs)
            tables = self._tables(ex, message, out, meta)
            counts = {}
            for name, (path, group_n) in tables.items():
                counts[name] = {"applied": native.apply_threshold(path, min_group_n=group_n,
                                                                  **_threshold_kwargs(self.applied))}
                if self.audit:
                    counts[name]["audit"] = native.apply_threshold(path, **_threshold_kwargs(self.audit))
                self.outputs[name] = {"deg_csv": path, **counts[name]}
                self.case.add_output(path, f"deg_{name}")
            if isinstance(message, dict) and message.get("formula"):
                final.setdefault("formula", message["formula"])
            if isinstance(message, dict) and message.get("skipped"):
                final["skipped"] = message["skipped"]
            if "formula" not in final and ex.args.get("design_column"):
                cov = ex.args.get("covariate_columns")
                cov = [cov] if isinstance(cov, str) else list(cov or [])
                final["formula"] = "~ " + " + ".join([*cov, ex.args["design_column"]])
            final.update(outputs=[p for p, _ in tables.values()], counts={
                k: {kk: {f: v[kk][f] for f in ("rule", "n_tested", "n_significant", "n_up", "n_down", "deg_sanity")}
                    for kk in v} for k, v in counts.items()})
            self.case.decide("execution", final=final, evidence=[self.items["matrix"], self.items["design_metadata"]],
                             reasoning=ex.reasoning or f"{ex.role} run of {ex.name}", confidence=ex.confidence,
                             execution_status="completed")
            self.result.setdefault("executions", {})[ex.name] = {
                k: {"n": v["applied"]["n_significant"], "up": v["applied"]["n_up"], "down": v["applied"]["n_down"],
                    **({"audit_n": v["audit"]["n_significant"]} if "audit" in v else {})} for k, v in counts.items()}
        except (native.NativeToolError, OSError, ValueError, KeyError) as exc:
            final["execution_error"] = _short(f"{type(exc).__name__}: {exc}", 1500)
            self.case.decide("execution", final=final, evidence=[self.items["matrix"], self.items["design_metadata"]],
                             reasoning=ex.reasoning or f"{ex.role} run of {ex.name}", confidence=ex.confidence,
                             execution_status="failed")
            self.result.setdefault("executions", {})[ex.name] = {"error": final["execution_error"]}

    def _comparisons(self, choice: Any) -> list[dict]:
        if choice == "all":
            return self.comparisons
        names = self.spec.gates.design.planned if choice == "planned" else list(choice)
        by_name = {c["name"]: c for c in self.comparisons}
        missing = [n for n in names if n not in by_name]
        if missing:
            raise native.NativeToolError(f"comparisons not in the suitability report: {missing}; "
                                         f"known: {sorted(by_name)[:30]}")
        return [by_name[n] for n in names]

    def _tables(self, ex: Execution, message: Any, out: Path,
                meta: pd.DataFrame) -> dict[str, tuple[str, Optional[int]]]:
        """Result tables of one execution: {name: (path, smallest group n)}."""
        if isinstance(message, dict) and isinstance(message.get("results"), list):
            by_name = {c["name"]: c for c in self.comparisons}
            tables = {}
            for r in message["results"]:
                cells = by_name.get(r["name"], {}).get("cells") or []
                tables[f"{ex.name}/{r['name']}"] = (r["path"], min((c["n"] for c in cells), default=None))
            if not tables:
                raise native.NativeToolError(f"{ex.tool} returned no result table")
            return tables
        found = native.deg_outputs(out)
        if not found:
            raise native.NativeToolError(f"{ex.tool} wrote no DEG_results_*.csv in {out}: {_short(message, 500)}")
        return {ex.name: (found[0], _group_n(meta, ex.args))}

    def _enrich(self, en: Enrichment) -> None:
        source = self.outputs.get(en.execution)
        organism = self.spec.gates.design.organism
        base = {"organism": organism, "subset": en.execution}
        if organism.lower() == "rat":
            base["ortholog_mapping"] = en.ortholog_mapping or (
                "rat symbols matched to mouse gene sets by identical symbol (tools/enrichment_tools.py); "
                "overlap reported by the tool")
        evidence = [self.items["matrix"]]
        if source is None:
            for method in (["ORA (Enrichr GO + KEGG)"] if en.ora else []) + (["GSEA preranked"] if en.gsea else []):
                self.case.decide("enrichment", final={**base, "method": method, "gene_sets": "not run",
                                 "feature_id_type": "unknown", "reason_not_run": f"no completed result for {en.execution}"},
                                 evidence=evidence, reasoning=en.reasoning or "planned enrichment",
                                 confidence="high", execution_status="not_run")
            return
        deg = source["deg_csv"]
        evidence = [self.case.add_output(deg, "deg_for_enrichment")]
        ids = native.feature_id_report(deg)
        base["feature_id_type"] = ids["dominant_type"]
        out = self.case.dir / "results" / ("enrichment_" + re.sub(r"[^A-Za-z0-9._-]+", "_", en.execution))
        status = self.result.setdefault("enrichment", {})
        if not ids["gene_set_ready"]:
            for method in (["ORA (Enrichr GO + KEGG)"] if en.ora else []) + (["GSEA preranked"] if en.gsea else []):
                self.case.decide("enrichment", final={**base, "method": method, "gene_sets": "not run",
                                 "reason_not_run": f"feature IDs are {ids['dominant_type']}, not gene-set ready"},
                                 evidence=evidence, reasoning=en.reasoning or "planned enrichment",
                                 confidence="high", execution_status="not_run")
            status[en.execution] = f"not_run: feature ids {ids['dominant_type']}"
            return
        runs = []
        if en.ora:
            ora_dir = "ora" if en.direction == "all" else f"ora_{en.direction}"  # up and down never share files
            rule = _threshold_kwargs(self.applied)
            as_applied = rule["metric"] == "padj"
            input_threshold = (self.applied if as_applied else
                               {"metric": "padj", "cutoff": 0.05, "effect_cutoff": self.applied.get("effect_cutoff")})
            runs.append(("ORA (Enrichr GO BP/MF/CC + KEGG)", "tools.enrichment_tools:run_enrichment_analysis",
                         {"deg_csv": deg, "organism": organism, "padj_cutoff": float(input_threshold.get("cutoff", 0.05)),
                          "log2fc_cutoff": float(input_threshold.get("effect_cutoff") or 0.0),
                          "direction": en.direction, "output_dir": str(out / ora_dir)},
                         {"gene_sets": "Enrichr GO_Biological_Process_2023, GO_Molecular_Function_2023, "
                                       "GO_Cellular_Component_2023, KEGG",
                          "input_threshold": input_threshold, "direction": en.direction,
                          "input_threshold_source": "applied" if as_applied else "audit"}, out / ora_dir))
        if en.gsea:
            runs.append(("GSEA preranked (gseapy prerank)", "tools.enrichment_tools:run_gsea_analysis",
                         {"deg_csv": deg, "organism": organism, "ranking_metric": en.ranking_metric,
                          "output_dir": str(out / "gsea")},
                         {"gene_sets": "MSigDB Hallmark", "ranking_metric": en.ranking_metric}, out / "gsea"))
        for method, tool, kwargs, extra, odir in runs:
            final = {**base, "method": method, **extra}
            try:
                message = native.call_tool(tool, **kwargs)
                final.update(outputs=[str(p) for p in sorted(odir.rglob("*.csv"))], summary=_short(message, 1500))
                if not final["outputs"]:
                    raise native.NativeToolError(f"no output written: {_short(message, 500)}")
                self.case.decide("enrichment", final=final, evidence=evidence, reasoning=en.reasoning or method,
                                 confidence="high", execution_status="completed")
                label = method.split()[0] + ("" if method.startswith("GSEA") or en.direction == "all"
                                             else f" {en.direction}")
                status[f"{en.execution} {label}"] = "completed"
            except native.NativeToolError as exc:
                final["execution_error"] = _short(exc, 1500)
                self.case.decide("enrichment", final=final, evidence=evidence, reasoning=en.reasoning or method,
                                 confidence="high", execution_status="failed")
                status[f"{en.execution} {method.split()[0]}"] = "failed: " + _short(exc, 200)

    def _study(self, st: StudyGate, paper_ev: list[dict], mat_item: dict) -> None:
        genes = {}
        for name, wanted in st.paper_genes.items():
            if name in self.outputs:
                genes[name] = _gene_lookup(self.outputs[name]["deg_csv"], wanted,
                                             self.spec.gates.design.organism)
        results = {name: {"n_deg": o["applied"]["n_significant"], "up": o["applied"]["n_up"],
                          "down": o["applied"]["n_down"], "rule": o["applied"]["rule"],
                          **({"audit_n": o["audit"]["n_significant"]} if "audit" in o else {})}
                   for name, o in self.outputs.items()}
        comparison = {name: {"ours": results.get(name, {}).get("n_deg"), "paper": paper}
                      for name, paper in st.paper_counts.items()}
        final = {**st.final, "results": results, "paper_counts": st.paper_counts, "comparison": comparison,
                 "paper_gene_check": genes}
        executions = [r for r in self.case.records if r["stage"] == "execution"]
        status = "completed" if any(r["execution_status"] == "completed" for r in executions) else "failed"
        self.decide("study", st, final, [*paper_ev, mat_item], execution_status=status)
        self.case.write_json("reproduction_summary.json", {"results": results, "comparison": comparison,
                                                           "paper_gene_check": genes})
        self.result["comparison"] = comparison
        if genes:
            self.result["paper_gene_check"] = genes

    def _finish(self) -> dict:
        primary = next((n for n, e in ((e.name, e) for e in self.spec.executions) if e.role == "primary"), None)
        hit = next((o for k, o in self.outputs.items() if primary and (k == primary or k.startswith(primary + "/"))),
                   None)
        applied = hit["applied"] if hit else None
        self.result["finish"] = self.case.finish(n_deg=applied["n_significant"] if applied else None,
                                                 deg_sanity=applied["deg_sanity"] if applied else None)
        return self.result


def execute(spec_path: str | Path) -> dict:
    spec = Spec.model_validate(json.loads(Path(spec_path).read_text(encoding="utf-8")))
    native.enable_native_mode()
    run_dir = Path(spec.run_dir)
    moved = _move_previous_attempt(run_dir, [c.case_id for c in spec.cases])
    run = native.RunRecorder(run_dir, request=spec.request, platform_name=spec.platform,
                             decision_maker=spec.decision_maker, case_ids=[c.case_id for c in spec.cases])
    # Keep the exact spec of this attempt next to its records.
    shutil.copy(spec_path, run_dir / f"case_spec.used.{_now()}.json")
    results = []
    for case_spec in spec.cases:
        runner = CaseRun(run, case_spec)
        try:
            results.append(runner.run())
        except Exception as exc:  # report where it broke; the spec is fixed and execute rerun
            runner.result["error"] = {"type": type(exc).__name__, "message": _short(exc, 2000),
                                      "where": traceback.format_exc(limit=-2).strip().splitlines()[-3:]}
            results.append(runner.result)
    finished = run.finish()
    n_records, errors = decision_contract.validate(sorted(run_dir.glob("*/decisions.json")))
    return {"run_dir": str(run_dir), "previous_attempt": str(moved) if moved else None, "run": finished,
            "validator": {"records": n_records, "errors": errors}, "cases": results}


# ---------------------------------------------------------------- template

TEMPLATE = {
    "run_dir": "test/experiments/<run>/<paper_id>",
    "request": "Analyze GSE000000 for PMID 0 (<title>): how exercise affects gene expression as the paper intends.",
    "decision_maker": "<model> session",
    "platform": "claude-code",
    "data_root": "data",
    "cases": [{
        "case_id": "GSE000000",
        "accession": "GSE000000",
        "inputs": {"paper": ["<papers>/PMC0.paper.md"], "metadata": "GSE000000/GSE000000_metadata.csv",
                   "matrix": "GSE000000/GSE000000_counts.csv.gz", "raw_tar": False, "prep_scripts": []},
        "gates": {
            "paper_reconstruction": {"final": {"accessions": ["GSE000000"], "primary_estimand": "...",
                                               "planned_contrasts": ["EX vs SED (S2.1.p1; paper: 120 DEGs)"],
                                               "paper_threshold": {"metric": "FDR", "cutoff": 0.05,
                                                                   "effect_metric": "log2FoldChange",
                                                                   "effect_cutoff": 1.0, "source_locator": "S4.5.p1"},
                                               "paper_method": "DESeq2 ~ group"},
                                     "reasoning": "...", "locator": "S4.5.p1"},
            "ownership": {"final": {"owned": True}, "reasoning": "DA.p1 names GSE000000; ..."},
            "alignment": {"key_column": None, "patterns": {"grp": ["title", "^(SED|EX)_\\d+$"]},
                          "recode": {}, "aliases": {}, "exclude_samples": {}, "reasoning": "..."},
            "matrix": {"matrix_type": "raw counts", "recommended_method": "DESeq2", "reasoning": "integer counts; GEO data_processing: featureCounts"},
            "design": {"factors": ["grp"], "references": {"grp": "SED"}, "organism": "Mouse", "planned": ["grp_EX_vs_SED"],
                       "final": {"analysis_type": "two-group", "design_column": "grp", "control": "SED", "treatment": "EX",
                                 "contrasts": [{"name": "grp_EX_vs_SED", "control": "SED", "treatment": "EX", "role": "primary"}]},
                       "reasoning": "..."},
            "covariance": {"final": {"status": "not_required", "blocking_terms": [], "covariates": []},
                           "confounding_candidates": None, "reasoning": "independent animals; no batch recorded"},
            "method": {"final": {"method": "DESeq2 (pydeseq2 Wald)", "formula": "~ grp"}, "transform": None, "reasoning": "..."},
            "threshold": {"final": {"paper_threshold": {"metric": "FDR", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0},
                                    "threshold_source": "paper",
                                    "applied_threshold": {"metric": "padj", "cutoff": 0.05, "effect_metric": "log2FoldChange", "effect_cutoff": 1.0},
                                    "audit_threshold": {"metric": "padj", "cutoff": 0.05, "effect_cutoff": None}},
                          "reasoning": "S4.5.p1: FDR < 0.05 and |log2FC| > 1"},
            "study": {"final": {"route": "paper_aligned"}, "paper_counts": {"grp_EX_vs_SED": 120},
                      "paper_genes": {"grp_EX_vs_SED": ["Ppargc1a", "Nr4a3"]}, "reasoning": "..."},
        },
        "discrepancies": [{"item": "...", "paper": "...", "data": "...", "disposition": "executable_without_change"}],
        "executions": [{"name": "grp_EX_vs_SED", "tool": "tools.deseq2_tools:run_deseq2_analysis",
                        "args": {"design_column": "grp", "control_group": "SED", "treatment_group": "EX", "alpha": 0.05},
                        "role": "primary", "reasoning": "paper's two-group DESeq2"}],
        "enrichment": [{"execution": "grp_EX_vs_SED", "ora": True, "gsea": True, "reasoning": "paper reports GO terms"}],
    }],
}


@contextlib.contextmanager
def _quiet(log: Path):
    """Send the tools' own printing (pydeseq2 tables, progress bars) to a log, not the agent's context."""
    log.parent.mkdir(parents=True, exist_ok=True)
    with open(log, "a", encoding="utf-8") as handle, contextlib.redirect_stdout(handle), \
            contextlib.redirect_stderr(handle):
        print(f"--- {_now()} {' '.join(sys.argv)}")
        yield


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m tools.case_runner", description=__doc__.split("\n\n")[0])
    sub = parser.add_subparsers(dest="command", required=True)
    p_inspect = sub.add_parser("inspect", help="download (if needed) and summarize one GEO series")
    p_inspect.add_argument("accession")
    p_inspect.add_argument("--data-root", default="data")
    p_inspect.add_argument("--merge-tar", action="store_true", help="also merge a _RAW.tar when other matrices exist")
    p_inspect.add_argument("--no-download", action="store_true")
    p_inspect.add_argument("--out", help="also write the JSON here")
    p_exec = sub.add_parser("execute", help="run a case spec")
    p_exec.add_argument("spec")
    sub.add_parser("template", help="print an example case spec")
    sub.add_parser("schema", help="print the case spec JSON schema")
    args = parser.parse_args(argv)
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass
    if args.command == "template":
        print(json.dumps(TEMPLATE, indent=2, ensure_ascii=False))
        return 0
    if args.command == "schema":
        print(json.dumps(Spec.model_json_schema(), indent=1))
        return 0
    if args.command == "inspect":
        log = Path(args.out).with_suffix(".log") if args.out else Path(args.data_root) / f"inspect_{args.accession}.log"
        with _quiet(log):
            result = inspect_series(args.accession, data_root=args.data_root, merge_tar=args.merge_tar,
                                    download=not args.no_download)
        result["log"] = str(log)
        text = json.dumps(result, indent=1, ensure_ascii=False, default=str)
        if args.out:
            Path(args.out).parent.mkdir(parents=True, exist_ok=True)
            Path(args.out).write_text(text, encoding="utf-8")
        print(text)
        return 0 if "error" not in result else 1
    try:
        spec_run_dir = Path(json.loads(Path(args.spec).read_text(encoding="utf-8")).get("run_dir", "."))
        log = spec_run_dir / "case_runner.log"
        with _quiet(log):
            result = execute(args.spec)
        result["log"] = str(log)
    except ValidationError as exc:
        print(json.dumps({"spec_error": [f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in exc.errors()]},
                         indent=1))
        return 2
    print(json.dumps(result, indent=1, ensure_ascii=False, default=str))
    bad = result["validator"]["errors"] or any("error" in c for c in result["cases"])
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main())
