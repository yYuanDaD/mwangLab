"""Unified, machine-readable provenance model for agent and pipeline outputs."""

from __future__ import annotations

from datetime import datetime
import hashlib
import json
import os
from typing import Any, Literal

from pydantic import BaseModel, Field


SCHEMA_VERSION = "1.0"
EvidenceOrigin = Literal["user", "metadata", "paper", "rule", "llm", "computation", "artifact", "external_api"]
DecisionMethod = Literal["user", "rule", "llm", "computation", "hybrid"]


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class EvidenceSource(BaseModel):
    source_id: str
    origin: EvidenceOrigin
    label: str
    uri: str | None = None
    locator: str | None = None
    captured_at: str = Field(default_factory=_now)
    sha256: str | None = None
    attributes: dict[str, Any] = Field(default_factory=dict)


class EvidenceClaim(BaseModel):
    claim_id: str
    subject: str
    predicate: str
    value: Any
    statement: str
    evidence_ids: list[str] = Field(default_factory=list)
    method: DecisionMethod
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    status: Literal["asserted", "computed", "inferred", "rejected"] = "asserted"


class EvidenceDecision(BaseModel):
    decision_id: str
    step: str
    selected: Any
    reason: str = ""
    method: DecisionMethod
    alternatives: list[Any] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)
    confidence: float | None = Field(default=None, ge=0.0, le=1.0)
    details: dict[str, Any] = Field(default_factory=dict)
    recorded_at: str = Field(default_factory=_now)


class EvidenceArtifact(BaseModel):
    artifact_id: str
    path: str
    role: str
    produced_by: str | None = None
    media_type: str | None = None
    sha256: str | None = None
    evidence_ids: list[str] = Field(default_factory=list)
    attributes: dict[str, Any] = Field(default_factory=dict)


class EvidenceBundle(BaseModel):
    schema_version: str = SCHEMA_VERSION
    run_id: str
    subject_id: str | None = None
    created_at: str = Field(default_factory=_now)
    finished_at: str | None = None
    status: str | None = None
    error: str | None = None
    sources: list[EvidenceSource] = Field(default_factory=list)
    claims: list[EvidenceClaim] = Field(default_factory=list)
    decisions: list[EvidenceDecision] = Field(default_factory=list)
    artifacts: list[EvidenceArtifact] = Field(default_factory=list)

    def validate_references(self) -> None:
        source_ids = {x.source_id for x in self.sources}
        claim_ids = {x.claim_id for x in self.claims}
        decision_ids = {x.decision_id for x in self.decisions}
        artifact_ids = {x.artifact_id for x in self.artifacts}
        expected_total = len(self.sources) + len(self.claims) + len(self.decisions) + len(self.artifacts)
        if len(source_ids | claim_ids | decision_ids | artifact_ids) != expected_total:
            raise ValueError("Evidence bundle contains duplicate record IDs.")
        valid = source_ids | claim_ids | artifact_ids
        dangling = []
        for kind, records in (("claim", self.claims), ("decision", self.decisions),
                              ("artifact", self.artifacts)):
            for record in records:
                for evidence_id in record.evidence_ids:
                    if evidence_id not in valid:
                        dangling.append(f"{kind}:{evidence_id}")
        for artifact in self.artifacts:
            if artifact.produced_by and artifact.produced_by not in decision_ids:
                dangling.append(f"artifact.produced_by:{artifact.produced_by}")
        if dangling:
            raise ValueError(f"Evidence bundle contains dangling references: {dangling}")


def file_sha256(path: str) -> str | None:
    if not os.path.isfile(path):
        return None
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class EvidenceRecorder:
    """Small builder used by workflows; IDs are stable and local to one bundle."""

    def __init__(self, run_id: str, subject_id: str | None = None):
        self.bundle = EvidenceBundle(run_id=run_id, subject_id=subject_id)
        self._source_keys: dict[tuple, str] = {}
        self._artifact_paths: dict[str, str] = {}

    def add_source(self, origin: EvidenceOrigin, label: str, *, uri: str | None = None,
                   locator: str | None = None, attributes: dict | None = None) -> str:
        key = (origin, label, uri, locator)
        if key in self._source_keys:
            return self._source_keys[key]
        source_id = f"SRC-{len(self.bundle.sources) + 1:04d}"
        self.bundle.sources.append(EvidenceSource(
            source_id=source_id, origin=origin, label=label, uri=uri, locator=locator,
            attributes=attributes or {},
        ))
        self._source_keys[key] = source_id
        return source_id

    def add_decision(self, step: str, selected: Any, *, reason: str = "",
                     method: DecisionMethod = "rule", evidence_ids: list[str] | None = None,
                     alternatives: list[Any] | None = None, confidence: float | None = None,
                     details: dict | None = None) -> str:
        decision_id = f"DEC-{len(self.bundle.decisions) + 1:04d}"
        self.bundle.decisions.append(EvidenceDecision(
            decision_id=decision_id, step=step, selected=selected, reason=reason,
            method=method, evidence_ids=evidence_ids or [], alternatives=alternatives or [],
            confidence=confidence, details=details or {},
        ))
        return decision_id

    def add_claim(self, subject: str, predicate: str, value: Any, statement: str, *,
                  method: DecisionMethod, evidence_ids: list[str] | None = None,
                  confidence: float | None = None, status: str = "asserted") -> str:
        claim_id = f"CLM-{len(self.bundle.claims) + 1:04d}"
        self.bundle.claims.append(EvidenceClaim(
            claim_id=claim_id, subject=subject, predicate=predicate, value=value,
            statement=statement, method=method, evidence_ids=evidence_ids or [],
            confidence=confidence, status=status,
        ))
        return claim_id

    def add_artifact(self, path: str, role: str, *, produced_by: str | None = None,
                     evidence_ids: list[str] | None = None, attributes: dict | None = None) -> str:
        normalized = os.path.normpath(str(path))
        if normalized in self._artifact_paths:
            return self._artifact_paths[normalized]
        artifact_id = f"ART-{len(self.bundle.artifacts) + 1:04d}"
        ext = os.path.splitext(normalized)[1].lower()
        media = {".csv": "text/csv", ".tsv": "text/tab-separated-values", ".json": "application/json",
                 ".png": "image/png", ".pdf": "application/pdf"}.get(ext)
        self.bundle.artifacts.append(EvidenceArtifact(
            artifact_id=artifact_id, path=normalized, role=role, produced_by=produced_by,
            media_type=media, sha256=file_sha256(normalized), evidence_ids=evidence_ids or [],
            attributes=attributes or {},
        ))
        self._artifact_paths[normalized] = artifact_id
        return artifact_id

    def finish(self, status: str | None = None, error: str | None = None) -> None:
        self.bundle.finished_at = _now()
        self.bundle.status = status
        self.bundle.error = error

    def save(self, path: str) -> str:
        self.bundle.validate_references()
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(self.bundle.model_dump(mode="json"), fh, indent=2, ensure_ascii=False)
        return path
