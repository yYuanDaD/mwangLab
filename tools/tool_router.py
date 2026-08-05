"""Deterministic request router for per-run tool exposure.

The router does not decide scientific results. It only narrows the tools shown
to the ReAct model when the requested modality/workflow is explicit. Ambiguous
requests deliberately fall back to the complete registry so routing cannot
silently remove a needed capability.
"""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Iterable, Sequence

from langchain_core.tools import BaseTool


PROFILE_TO_TOOL_NAMES: dict[str, tuple[str, ...]] = {
    "paper_cohort": ("run_agent_a_cohort",),
    "paper_utility": ("search_papers", "fetch_paper_text", "extract_geo_accession"),
    "sea_cdm": ("extract_sea_cdm_tables", "fetch_paper_text", "extract_geo_accession"),
    "geo_batch": (
        "search_geo_studies", "fetch_geo_description", "run_batch_geo_pipeline",
        "evaluate_repeated_subset_results", "export_kg_style_results",
    ),
    "bulk_expression": (
        "search_geo_studies", "download_geo_data", "download_supplementary_files",
        "fetch_geo_description", "inspect_metadata", "preprocess_counts",
        "run_pca", "sample_correlation_heatmap", "sample_qc_summary",
        "infer_sex_from_expression", "run_deseq2_analysis", "run_limma_analysis",
        "run_enrichment_analysis", "run_gsea_analysis", "run_batch_geo_pipeline",
        "evaluate_repeated_subset_results",
    ),
    "single_cell": (
        "run_scrna_pseudobulk_da", "run_enrichment_analysis", "run_gsea_analysis",
        "evaluate_repeated_subset_results",
    ),
    "methylation": (
        "run_methylation_da", "run_enrichment_analysis", "run_gsea_analysis",
        "evaluate_repeated_subset_results",
    ),
    "proteomics": (
        "identify_proteomics_labeling", "download_pride_project",
        "preprocess_proteomics_matrix", "inspect_metadata", "run_limma_analysis",
        "run_enrichment_analysis", "run_gsea_analysis", "evaluate_repeated_subset_results",
    ),
    "evaluation": ("evaluate_repeated_subset_results",),
    "kg_export": ("export_kg_style_results",),
}


@dataclass(frozen=True)
class RoutingDecision:
    profiles: tuple[str, ...]
    tool_names: tuple[str, ...]
    fallback_to_all: bool
    reason: str


def _has(text: str, terms: Sequence[str]) -> bool:
    return any(term in text for term in terms)


def route_request(query: str, all_tool_names: Iterable[str]) -> RoutingDecision:
    """Classify an explicit request into one or more capability profiles."""
    text = " ".join(str(query).lower().split())
    profiles: list[str] = []

    is_proteomics = _has(text, ("proteomic", "proteomics", "protein abundance", "mass spec",
                                "mass-spec", "质谱", "蛋白组", "pxd", "pride"))
    is_single_cell = _has(text, ("single-cell", "single cell", "scrna", "sc-rna", "单细胞",
                                 "pseudobulk", "伪批量"))
    is_methylation = _has(text, ("methylation", "methylome", "甲基化", "rrbs", "wgbs",
                                 "bisulfite", "450k", "epic array"))
    is_sea = _has(text, ("sea-cdm", "sea cdm", "seacdm", "standardized expression anatomy"))
    is_kg = _has(text, ("knowledge graph", "kg-style", "kg style", "知识图谱"))
    is_eval = _has(text, ("subset stability", "repeated subset", "stability evaluation",
                         "稳定性评估", "重复子集", "一致性评估"))
    is_paper = _has(text, ("paper", "papers", "literature", "pubmed", "pmc", "论文", "文献"))
    is_cohort = _has(text, ("cohort", "队列", "批量论文", "多篇论文", "top papers"))

    # Specific modalities take precedence over generic words such as expression/analysis.
    if is_paper and is_cohort:
        profiles.append("paper_cohort")
    elif is_proteomics:
        profiles.append("proteomics")
    elif is_single_cell:
        profiles.append("single_cell")
    elif is_methylation:
        profiles.append("methylation")
    elif is_sea:
        profiles.append("sea_cdm")
        if is_paper:
            profiles.append("paper_utility")
    elif is_paper:
        profiles.append("paper_utility")
    else:
        has_gse = bool(re.search(r"\bgse\d+\b", text))
        is_geo = has_gse or _has(text, ("geo", "gene expression omnibus", "基因表达数据库"))
        is_bulk = _has(text, (
            "rna-seq", "rnaseq", "bulk rna", "counts", "expression matrix", "表达矩阵",
            "差异表达", "deseq", "limma", "pca", "相关性", "富集", "gsea",
            "download", "下载", "preprocess", "预处理", "quality control", "质控",
        ))
        is_batch = _has(text, ("batch", "cohort", "批量", "队列", "多个研究", "多研究"))
        if is_geo and (has_gse or is_batch) and not is_bulk:
            profiles.append("geo_batch")
        elif is_geo or is_bulk:
            profiles.append("bulk_expression")

    if is_eval and "evaluation" not in profiles:
        profiles.append("evaluation")
    if is_kg and "kg_export" not in profiles:
        profiles.append("kg_export")

    available = tuple(dict.fromkeys(all_tool_names))
    if not profiles:
        return RoutingDecision(
            profiles=("general",), tool_names=available, fallback_to_all=True,
            reason="request modality is ambiguous; retained the complete tool registry",
        )

    requested_names: list[str] = []
    for profile in profiles:
        requested_names.extend(PROFILE_TO_TOOL_NAMES[profile])
    requested = set(requested_names)
    selected = tuple(name for name in available if name in requested)
    if not selected:
        return RoutingDecision(
            profiles=tuple(profiles), tool_names=available, fallback_to_all=True,
            reason="profile matched but no registered tools were available; used safe fallback",
        )
    return RoutingDecision(
        profiles=tuple(profiles), tool_names=selected, fallback_to_all=False,
        reason=f"explicit request matched: {', '.join(profiles)}",
    )


def select_tools(query: str, registry: Sequence[BaseTool]) -> tuple[list[BaseTool], RoutingDecision]:
    """Return tools in registry order plus an auditable routing decision."""
    by_name = {tool.name: tool for tool in registry}
    if len(by_name) != len(registry):
        raise ValueError("Tool registry contains duplicate tool names.")
    configured = {name for names in PROFILE_TO_TOOL_NAMES.values() for name in names}
    missing = sorted(configured - set(by_name))
    if missing:
        raise ValueError(f"Tool routing profiles reference unregistered tools: {missing}")
    decision = route_request(query, by_name.keys())
    return [by_name[name] for name in decision.tool_names], decision
