"""KG-style CSV exporter matching `kg_extraction_results_v8.csv`.

The output is a wide edge table centered on:
    regulated_gene --relationship--> phenotypic_change

It reuses our current artifacts:
  - computed DEG-derived `csv/gene.csv` for regulated genes,
  - paper `studies/<study>_reported_findings.csv` for gene/phenotype claim evidence,
  - computed GSEA-derived `pathway.csv` / `enrichment.csv` for pathway context.
"""

import glob
import os
import re
from collections import defaultdict

import pandas as pd
from langchain_core.tools import tool


KG_COLUMNS = [
    "paper_title", "regulated_gene", "relationship", "phenotypic_change",
    "phenotype_search_term", "hpo_id", "hpo_label", "mp_id", "mp_label",
    "go_bp_id", "go_bp_term", "kegg_pathway", "exercise_type", "exercise_duration",
    "exercise_intensity", "animal_or_human", "species_latin", "age", "sex", "model",
    "tissue", "upstream_gene", "downstream_gene", "mechanism_desc", "mediated_by",
    "paper_section", "evidence", "data_source", "ontology_used",
    "ontology_search_term_ranked", "embedding_similarity", "similarity_strength",
    "ontology_match_source", "ontology_match_reason", "top_candidate_id",
    "top_candidate_label",
]


_GENE_TYPES = {"gene", "protein"}
_PHENO_TYPES = {"phenotype", "other"}
_PATHWAY_TYPES = {"pathway"}


def _read_csv(path: str) -> pd.DataFrame:
    if not path or not os.path.exists(path):
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def _clean(value) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except Exception:
        pass
    return str(value).strip()


def _first_nonempty(*values) -> str:
    for v in values:
        s = _clean(v)
        if s:
            return s
    return ""


def _norm_key(value) -> str:
    return re.sub(r"\s+", " ", _clean(value).lower())


def _is_human(species: str, manifest_row: dict = None) -> bool:
    s = _clean(species).lower()
    if "homo sapiens" in s or s == "human":
        return True
    if manifest_row:
        hay = " ".join(_clean(manifest_row.get(k)) for k in ("title", "organism"))
        return "human" in hay.lower()
    return False


def _relationship_from_direction(direction: str) -> str:
    d = _clean(direction).lower()
    return {
        "up": "upregulates",
        "down": "downregulates",
        "changed": "associated with",
        "unchanged": "not associated with",
        "n/a": "associated with",
    }.get(d, d or "associated with")


def _paper_section_from_source(source: str) -> str:
    s = _clean(source).lower()
    if any(k in s for k in ("result", "increased", "decreased", "upregulated", "downregulated")):
        return "Results"
    return ""


def _manifest_by_study(cohort_dir: str) -> dict[str, dict]:
    papers = _read_csv(os.path.join(cohort_dir, "papers.csv"))
    out = {}
    for _, r in papers.iterrows() if not papers.empty else []:
        row = r.to_dict()
        for key in ("study_id", "chosen_gse", "pmcid"):
            sid = _clean(row.get(key))
            if sid:
                out[sid] = row
    return out


def _study_titles(cohort_dir: str) -> dict[str, str]:
    csv_study = _read_csv(os.path.join(cohort_dir, "csv", "study.csv"))
    titles = {}
    if not csv_study.empty:
        for _, r in csv_study.iterrows():
            sid = _clean(r.get("study_id"))
            if sid:
                titles[sid] = _first_nonempty(r.get("study_name"), r.get("study_description"))
    for sid, row in _manifest_by_study(cohort_dir).items():
        titles.setdefault(sid, _clean(row.get("title")))
    return titles


def _context_by_study(cohort_dir: str) -> dict[str, dict]:
    cdir = os.path.join(cohort_dir, "csv")
    out = defaultdict(dict)
    subjects = _read_csv(os.path.join(cdir, "subject.csv"))
    for _, r in subjects.iterrows() if not subjects.empty else []:
        sid = _study_from_any_id(r.get("experiment_id"))
        ctx = out[sid]
        ctx.setdefault("species_latin", _clean(r.get("species")))
        ctx.setdefault("age", _clean(r.get("organism_age")))
        ctx.setdefault("sex", _clean(r.get("organism_sex")))
        ctx.setdefault("model", _clean(r.get("subject_lineage")))
    samples = _read_csv(os.path.join(cdir, "sample.csv"))
    for _, r in samples.iterrows() if not samples.empty else []:
        sid = _study_from_any_id(r.get("sample_id")) or _study_from_any_id(r.get("organism_id"))
        out[sid].setdefault("tissue", _clean(r.get("biosample_type")))
    interventions = _read_csv(os.path.join(cdir, "interventions.csv"))
    for _, r in interventions.iterrows() if not interventions.empty else []:
        sid = _study_from_any_id(r.get("experiment_id"))
        ctx = out[sid]
        ctx.setdefault("exercise_type", _first_nonempty(r.get("material"), r.get("intervention_type")))
        ctx.setdefault("exercise_duration", _clean(r.get("intervention_time")))
        ctx.setdefault("exercise_intensity", _clean(r.get("dosage")))
    exercises = _read_csv(os.path.join(cdir, "exercise.csv"))
    for _, r in exercises.iterrows() if not exercises.empty else []:
        sid = _clean(r.get("study_id"))
        ctx = out[sid]
        ctx.setdefault("exercise_type", _first_nonempty(r.get("exercise_name"), r.get("exercise_type")))
        ctx.setdefault("exercise_duration", _clean(r.get("exercise_time")))
        ctx.setdefault("exercise_intensity", _clean(r.get("exercise_parameters")))
    return dict(out)


def _study_from_any_id(value) -> str:
    s = _clean(value)
    if not s:
        return ""
    if "_exp" in s:
        return s.split("_exp", 1)[0]
    if "_gene" in s:
        return s.split("_gene", 1)[0]
    if "_deg_gene" in s:
        return s.split("_deg_gene", 1)[0]
    return s.split("_")[0] if s.startswith("GSE") and "_" in s else ""


def _reported_findings_by_study(cohort_dir: str) -> dict[str, pd.DataFrame]:
    studies_dir = os.path.join(cohort_dir, "studies")
    out = {}
    for path in glob.glob(os.path.join(studies_dir, "*_reported_findings.csv")):
        name = os.path.basename(path)
        sid = name[: -len("_reported_findings.csv")]
        out[sid] = _read_csv(path)
    return out


def _phenotypes_for_study(findings: pd.DataFrame) -> list[dict]:
    phenos = []
    for _, r in findings.iterrows() if not findings.empty else []:
        et = _clean(r.get("entity_type")).lower()
        ent = _clean(r.get("entity"))
        if not ent:
            continue
        if et in _PHENO_TYPES and et not in _GENE_TYPES and "pathway" not in ent.lower():
            phenos.append(r.to_dict())
    return phenos


def _gene_claims_for_study(findings: pd.DataFrame) -> list[dict]:
    claims = []
    for _, r in findings.iterrows() if not findings.empty else []:
        if _clean(r.get("entity_type")).lower() in _GENE_TYPES and _clean(r.get("entity")):
            claims.append(r.to_dict())
    return claims


def _best_phenotype_for_gene(gene_row: dict, phenotypes: list[dict]) -> dict:
    if not phenotypes:
        return {}
    comp = _norm_key(gene_row.get("comparison"))
    if comp:
        for p in phenotypes:
            if _norm_key(p.get("comparison")) == comp:
                return p
    return phenotypes[0]


def _pathway_context(cohort_dir: str) -> dict[str, str]:
    cdir = os.path.join(cohort_dir, "csv")
    pathway = _read_csv(os.path.join(cdir, "pathway.csv"))
    enrichment = _read_csv(os.path.join(cdir, "enrichment.csv"))
    analysis = _read_csv(os.path.join(cdir, "analysis.csv"))
    if pathway.empty or enrichment.empty or analysis.empty:
        return {}
    merged = enrichment.merge(pathway, on="pathway_id", how="left").merge(analysis, on="analysis_id", how="left")
    out = {}
    if "fdr" in merged.columns:
        merged["_fdr"] = pd.to_numeric(merged["fdr"], errors="coerce")
        merged = merged.sort_values("_fdr", na_position="last")
    for _, r in merged.iterrows():
        sid = _clean(r.get("study_id"))
        if sid and sid not in out:
            out[sid] = _clean(r.get("pathway_name"))
    return out


def _base_row(study_id: str, cohort_dir: str, titles: dict, context: dict,
              manifest: dict, pathway_by_study: dict) -> dict:
    ctx = context.get(study_id, {})
    man = manifest.get(study_id, {})
    species = _clean(ctx.get("species_latin"))
    animal = "human" if _is_human(species, man) else "mouse" if "mus musculus" in species.lower() else ""
    return {
        "paper_title": _first_nonempty(titles.get(study_id), man.get("title")),
        "go_bp_id": "",
        "go_bp_term": "",
        "kegg_pathway": pathway_by_study.get(study_id, ""),
        "exercise_type": ctx.get("exercise_type", ""),
        "exercise_duration": ctx.get("exercise_duration", ""),
        "exercise_intensity": ctx.get("exercise_intensity", ""),
        "animal_or_human": animal,
        "species_latin": species,
        "age": ctx.get("age", ""),
        "sex": ctx.get("sex", ""),
        "model": ctx.get("model", ""),
        "tissue": ctx.get("tissue", ""),
        "paper_section": "",
        "ontology_used": "",
        "ontology_search_term_ranked": "",
        "embedding_similarity": "",
        "similarity_strength": "",
        "ontology_match_source": "",
        "ontology_match_reason": "",
        "top_candidate_id": "",
        "top_candidate_label": "",
    }


def kg_rows_from_cohort(cohort_dir: str, include_paper_claim_only: bool = True) -> list[dict]:
    titles = _study_titles(cohort_dir)
    manifest = _manifest_by_study(cohort_dir)
    context = _context_by_study(cohort_dir)
    findings_by_study = _reported_findings_by_study(cohort_dir)
    pathway_by_study = _pathway_context(cohort_dir)
    gene = _read_csv(os.path.join(cohort_dir, "csv", "gene.csv"))
    rows = []
    seen_claim_genes = set()

    for _, g in gene.iterrows() if not gene.empty else []:
        gd = g.to_dict()
        study_id = _clean(gd.get("study_id"))
        if not study_id:
            continue
        findings = findings_by_study.get(study_id, pd.DataFrame())
        phenotype = _best_phenotype_for_gene(gd, _phenotypes_for_study(findings))
        row = _base_row(study_id, cohort_dir, titles, context, manifest, pathway_by_study)
        relationship = _relationship_from_direction(gd.get("regulation_direction"))
        evidence = _first_nonempty(gd.get("magnitude"), gd.get("gene_symbol_source"))
        phenotype_name = _clean(phenotype.get("entity"))
        row.update({
            "regulated_gene": _clean(gd.get("gene_symbol")),
            "relationship": relationship,
            "phenotypic_change": phenotype_name,
            "phenotype_search_term": phenotype_name,
            "upstream_gene": "",
            "downstream_gene": "",
            "mechanism_desc": f"{_clean(gd.get('gene_symbol'))} {relationship} in {_clean(gd.get('comparison'))}",
            "mediated_by": "",
            "paper_section": _paper_section_from_source(phenotype.get("source")),
            "evidence": _first_nonempty(phenotype.get("source"), evidence),
            "data_source": "regulated_gene:computed_deg; phenotype:paper_claim" if phenotype_name else "regulated_gene:computed_deg",
        })
        rows.append({c: row.get(c, "") for c in KG_COLUMNS})
        seen_claim_genes.add((study_id, _norm_key(row["regulated_gene"])))

    if include_paper_claim_only:
        for study_id, findings in findings_by_study.items():
            phenotypes = _phenotypes_for_study(findings)
            for claim in _gene_claims_for_study(findings):
                gene_name = _clean(claim.get("entity"))
                if (study_id, _norm_key(gene_name)) in seen_claim_genes:
                    continue
                phenotype = _best_phenotype_for_gene(claim, phenotypes)
                phenotype_name = _clean(phenotype.get("entity"))
                row = _base_row(study_id, cohort_dir, titles, context, manifest, pathway_by_study)
                row.update({
                    "regulated_gene": gene_name,
                    "relationship": _relationship_from_direction(claim.get("direction")),
                    "phenotypic_change": phenotype_name,
                    "phenotype_search_term": phenotype_name,
                    "upstream_gene": "",
                    "downstream_gene": "",
                    "mechanism_desc": _clean(claim.get("comparison")),
                    "mediated_by": "",
                    "paper_section": _paper_section_from_source(claim.get("source")),
                    "evidence": _clean(claim.get("source")),
                    "data_source": "paper_claim_only",
                })
                rows.append({c: row.get(c, "") for c in KG_COLUMNS})
    return rows


def export_kg_style_results_core(
    cohort_dir: str,
    output_csv: str = "",
    include_paper_claim_only: bool = True,
) -> dict:
    rows = kg_rows_from_cohort(cohort_dir, include_paper_claim_only=include_paper_claim_only)
    if not output_csv:
        output_csv = os.path.join(cohort_dir, "kg_extraction_results_style.csv")
    os.makedirs(os.path.dirname(output_csv) or ".", exist_ok=True)
    pd.DataFrame(rows, columns=KG_COLUMNS).to_csv(output_csv, index=False)
    return {"output_csv": output_csv, "n_rows": len(rows), "columns": KG_COLUMNS}


@tool
def export_kg_style_results(
    cohort_dir: str,
    output_csv: str = "",
    include_paper_claim_only: bool = True,
) -> str:
    """Export an Agent A cohort directory to a KG CSV matching kg_extraction_results_v8.csv columns.

    Args:
        cohort_dir: Directory containing `csv/`, `studies/`, and optionally `papers.csv`.
        output_csv: Optional output path. Defaults to `<cohort_dir>/kg_extraction_results_style.csv`.
        include_paper_claim_only: If True, include article gene claims when no computed DEG gene row
            exists for that gene. Such rows are marked `data_source=paper_claim_only`.
    """
    try:
        res = export_kg_style_results_core(cohort_dir, output_csv, include_paper_claim_only)
        return (
            f"KG-style export complete: {res['n_rows']} rows\n"
            f"Output CSV: {res['output_csv']}\n"
            f"Columns matched to kg_extraction_results_v8.csv: {len(res['columns'])}"
        )
    except Exception as e:
        return f"KG-style export failed. Error: {type(e).__name__}: {e}"
