"""Article-level claim-to-evidence mapping and result-card utilities.

The existing :mod:`tools.agreement_tools` reconciles individual reported genes
with computed DEG tables.  This module operates one level higher: it records
what a paper claims, what a particular accession/contrast can actually test,
and whether a computed or paper-reported finding directly supports the claim,
only partially supports it, is a secondary finding, contradicts it, or cannot
evaluate it.

The important invariant is that an untrustworthy analysis may be documented,
but it can never be promoted to support for a paper claim or to a secondary
finding.  Rejection applies to the inference, not to the whole article: every
article can still receive a descriptive or paper-reported result card.
"""

from __future__ import annotations

import hashlib
import json
import os
from typing import Literal

from pydantic import BaseModel, Field, model_validator


SCHEMA_VERSION = "1.0"

ClaimImportance = Literal["primary", "secondary"]
EvidenceType = Literal[
    "deg", "gsea", "reported_result", "phenotype", "qc", "metadata", "other"
]
EvidenceOrigin = Literal["computed", "paper_reported", "descriptive"]
EvidenceRelation = Literal[
    "direct_support",
    "partial_support",
    "secondary_finding",
    "contradictory",
    "not_evaluable",
]
DimensionVerdict = Literal["match", "partial", "mismatch", "unknown", "not_applicable"]
AnnotationStatus = Literal["machine_draft", "human_reviewed", "gold"]
DeliverableLevel = Literal[
    "full_reanalysis",
    "partial_reanalysis",
    "published_result_extraction",
    "descriptive_result",
]


class BiologicalScope(BaseModel):
    organism: str | None = None
    population_or_model: str | None = None
    tissue_or_cell: str | None = None
    intervention: str | None = None
    comparator: str | None = None
    timepoint: str | None = None
    endpoint: str | None = None
    mechanism: str | None = None


class PaperClaim(BaseModel):
    claim_id: str
    statement: str = Field(min_length=1)
    importance: ClaimImportance = "primary"
    source_quote: str = Field(min_length=1)
    source_uri: str | None = None
    source_locator: str | None = None
    scope: BiologicalScope = Field(default_factory=BiologicalScope)


class AnalysisEvidence(BaseModel):
    evidence_id: str
    accession: str | None = None
    evidence_type: EvidenceType
    origin: EvidenceOrigin
    statement: str = Field(min_length=1)
    contrast: str | None = None
    trustworthy: bool
    sanity_flags: list[str] = Field(default_factory=list)
    artifact_paths: list[str] = Field(default_factory=list)
    artifact_sha256: dict[str, str] = Field(default_factory=dict)
    source_locator: str | None = None
    scope: BiologicalScope = Field(default_factory=BiologicalScope)


class ClaimEvidenceLink(BaseModel):
    link_id: str
    claim_id: str
    evidence_id: str | None = None
    relation: EvidenceRelation
    rationale: str = Field(min_length=1)
    dimension_alignment: dict[str, DimensionVerdict] = Field(default_factory=dict)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def relation_requires_evidence(self):
        if self.relation != "not_evaluable" and not self.evidence_id:
            raise ValueError(f"{self.relation} requires evidence_id")
        return self


class SecondaryFinding(BaseModel):
    finding_id: str
    statement: str = Field(min_length=1)
    evidence_ids: list[str] = Field(min_length=1)
    rationale: str = Field(min_length=1)


class ArticleResultCard(BaseModel):
    schema_version: str = SCHEMA_VERSION
    article_id: str
    accessions: list[str] = Field(default_factory=list)
    annotation_status: AnnotationStatus = "machine_draft"
    claims: list[PaperClaim] = Field(default_factory=list)
    evidence: list[AnalysisEvidence] = Field(default_factory=list)
    links: list[ClaimEvidenceLink] = Field(default_factory=list)
    secondary_findings: list[SecondaryFinding] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    deliverable_level: DeliverableLevel | None = None

    @model_validator(mode="after")
    def validate_ids_and_references(self):
        claim_ids = [x.claim_id for x in self.claims]
        evidence_ids = [x.evidence_id for x in self.evidence]
        link_ids = [x.link_id for x in self.links]
        finding_ids = [x.finding_id for x in self.secondary_findings]
        for label, values in (
            ("claim", claim_ids),
            ("evidence", evidence_ids),
            ("link", link_ids),
            ("secondary finding", finding_ids),
        ):
            if len(values) != len(set(values)):
                raise ValueError(f"duplicate {label} IDs")

        claim_set, evidence_set = set(claim_ids), set(evidence_ids)
        evidence_by_id = {x.evidence_id: x for x in self.evidence}
        for link in self.links:
            if link.claim_id not in claim_set:
                raise ValueError(f"link {link.link_id} references unknown claim {link.claim_id}")
            if link.evidence_id and link.evidence_id not in evidence_set:
                raise ValueError(
                    f"link {link.link_id} references unknown evidence {link.evidence_id}"
                )
            if link.evidence_id and link.relation != "not_evaluable":
                ev = evidence_by_id[link.evidence_id]
                if not ev.trustworthy:
                    raise ValueError(
                        f"untrustworthy evidence {ev.evidence_id} cannot be labeled "
                        f"{link.relation}"
                    )
        for finding in self.secondary_findings:
            for evidence_id in finding.evidence_ids:
                if evidence_id not in evidence_set:
                    raise ValueError(
                        f"secondary finding {finding.finding_id} references unknown evidence "
                        f"{evidence_id}"
                    )
                if not evidence_by_id[evidence_id].trustworthy:
                    raise ValueError(
                        f"secondary finding {finding.finding_id} uses untrustworthy evidence "
                        f"{evidence_id}"
                    )
        self.deliverable_level = infer_deliverable_level(self)
        return self


def _sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def infer_deliverable_level(card: ArticleResultCard) -> DeliverableLevel:
    trustworthy = [x for x in card.evidence if x.trustworthy]
    computed = {x.evidence_type for x in trustworthy if x.origin == "computed"}
    if {"deg", "gsea"}.issubset(computed):
        return "full_reanalysis"
    if computed & {"deg", "gsea", "phenotype"}:
        return "partial_reanalysis"
    if any(x.origin == "paper_reported" for x in trustworthy):
        return "published_result_extraction"
    return "descriptive_result"


def audit_result_card(card: ArticleResultCard, *, base_dir: str = "",
                      verify_artifacts: bool = True) -> dict:
    """Return deterministic coverage/provenance checks for one result card."""
    blocking: list[str] = []
    warnings: list[str] = []
    primary = [x for x in card.claims if x.importance == "primary"]
    linked_claims = {x.claim_id for x in card.links}
    uncovered = [x.claim_id for x in primary if x.claim_id not in linked_claims]
    if not primary:
        blocking.append("no_primary_claim")
    if uncovered:
        blocking.append("primary_claims_unmapped")

    placeholder = lambda s: not s or "SOURCE REQUIRED" in s or "TODO" in s
    incomplete_sources = [
        x.claim_id for x in card.claims
        if placeholder(x.source_quote) or placeholder(x.source_locator)
    ]
    if card.annotation_status == "gold" and incomplete_sources:
        blocking.append("gold_claim_source_incomplete")
    elif incomplete_sources:
        warnings.append("claim_source_incomplete")

    missing_artifacts, hash_mismatches = [], []
    if verify_artifacts:
        for evidence in card.evidence:
            for raw_path in evidence.artifact_paths:
                path = raw_path if os.path.isabs(raw_path) else os.path.join(base_dir, raw_path)
                if not os.path.isfile(path):
                    missing_artifacts.append(raw_path)
                    continue
                expected = evidence.artifact_sha256.get(raw_path)
                if expected and _sha256(path) != expected:
                    hash_mismatches.append(raw_path)
    if missing_artifacts:
        blocking.append("artifact_missing")
    if hash_mismatches:
        blocking.append("artifact_hash_mismatch")

    relation_counts = {name: 0 for name in (
        "direct_support", "partial_support", "secondary_finding",
        "contradictory", "not_evaluable",
    )}
    for link in card.links:
        relation_counts[link.relation] += 1

    return {
        "verdict": "pass" if not blocking else "fail",
        "blocking": sorted(set(blocking)),
        "warnings": sorted(set(warnings)),
        "annotation_status": card.annotation_status,
        "deliverable_level": card.deliverable_level,
        "primary_claim_count": len(primary),
        "primary_claim_coverage": (
            (len(primary) - len(uncovered)) / len(primary) if primary else 0.0
        ),
        "uncovered_primary_claims": uncovered,
        "relation_counts": relation_counts,
        "missing_artifacts": missing_artifacts,
        "hash_mismatches": hash_mismatches,
    }


def render_result_card_markdown(card: ArticleResultCard) -> str:
    audit = audit_result_card(card, verify_artifacts=False)
    lines = [
        f"# Article result card: {card.article_id}",
        "",
        f"- Annotation status: `{card.annotation_status}`",
        f"- Deliverable level: `{card.deliverable_level}`",
        f"- Accessions: {', '.join(card.accessions) if card.accessions else 'none recorded'}",
        f"- Deterministic audit: `{audit['verdict']}`",
        "",
        "## Paper claims",
        "",
    ]
    for claim in card.claims:
        lines.extend([
            f"### {claim.claim_id} ({claim.importance})",
            "",
            claim.statement,
            "",
            f"> {claim.source_quote}",
            "",
            f"Source: {claim.source_locator or claim.source_uri or 'not recorded'}",
            "",
        ])

    evidence_by_id = {x.evidence_id: x for x in card.evidence}
    lines.extend(["## Claim-evidence map", ""])
    for link in card.links:
        evidence = evidence_by_id.get(link.evidence_id) if link.evidence_id else None
        lines.extend([
            f"- `{link.relation}` — {link.claim_id} ← "
            f"{link.evidence_id or 'no applicable evidence'}: {link.rationale}",
        ])
        if evidence:
            lines.append(f"  Evidence: {evidence.statement}")
    if not card.links:
        lines.append("- No claim-evidence links recorded.")

    lines.extend(["", "## Secondary findings", ""])
    if card.secondary_findings:
        for finding in card.secondary_findings:
            lines.append(f"- {finding.statement} ({', '.join(finding.evidence_ids)})")
    else:
        lines.append("- None recorded.")

    lines.extend(["", "## Limitations", ""])
    lines.extend([f"- {x}" for x in card.limitations] or ["- None recorded."])
    lines.append("")
    return "\n".join(lines)


def save_result_card(card: ArticleResultCard, json_path: str, markdown_path: str | None = None) -> str:
    os.makedirs(os.path.dirname(json_path) or ".", exist_ok=True)
    with open(json_path, "w", encoding="utf-8") as fh:
        json.dump(card.model_dump(mode="json"), fh, indent=2, ensure_ascii=False)
    if markdown_path:
        os.makedirs(os.path.dirname(markdown_path) or ".", exist_ok=True)
        with open(markdown_path, "w", encoding="utf-8") as fh:
            fh.write(render_result_card_markdown(card))
    return json_path
