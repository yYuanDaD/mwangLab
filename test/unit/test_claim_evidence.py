import json
import os
import sys
import tempfile

from pydantic import ValidationError

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.claim_evidence import (
    AnalysisEvidence,
    ArticleResultCard,
    BiologicalScope,
    ClaimEvidenceLink,
    PaperClaim,
    SecondaryFinding,
    audit_result_card,
    save_result_card,
)


def _claim():
    return PaperClaim(
        claim_id="CLM-1",
        statement="Exercise improves muscle oxidative metabolism.",
        importance="primary",
        source_quote="Exercise increased oxidative capacity in skeletal muscle.",
        source_uri="paper.txt",
        source_locator="Results paragraph 2",
        scope=BiologicalScope(tissue_or_cell="skeletal muscle", intervention="exercise"),
    )


def test_full_card_and_artifact_hash():
    with tempfile.TemporaryDirectory() as tmp:
        deg = os.path.join(tmp, "deg.csv")
        gsea = os.path.join(tmp, "gsea.csv")
        open(deg, "w", encoding="utf-8").write("gene,log2FC\nA,1\n")
        open(gsea, "w", encoding="utf-8").write("term,NES\nOXPHOS,2\n")
        card = ArticleResultCard(
            article_id="PMID1",
            accessions=["GSE1"],
            annotation_status="gold",
            claims=[_claim()],
            evidence=[
                AnalysisEvidence(
                    evidence_id="E-DEG", accession="GSE1", evidence_type="deg",
                    origin="computed", statement="Oxidative genes increased.",
                    trustworthy=True, artifact_paths=[deg],
                ),
                AnalysisEvidence(
                    evidence_id="E-GSEA", accession="GSE1", evidence_type="gsea",
                    origin="computed", statement="Oxidative phosphorylation was enriched.",
                    trustworthy=True, artifact_paths=[gsea],
                ),
            ],
            links=[ClaimEvidenceLink(
                link_id="L-1", claim_id="CLM-1", evidence_id="E-GSEA",
                relation="partial_support", rationale="Same tissue and intervention; molecular endpoint only.",
            )],
        )
        assert card.deliverable_level == "full_reanalysis"
        audit = audit_result_card(card)
        assert audit["verdict"] == "pass"
        assert audit["primary_claim_coverage"] == 1.0

        out_json = os.path.join(tmp, "card.json")
        out_md = os.path.join(tmp, "card.md")
        save_result_card(card, out_json, out_md)
        assert json.load(open(out_json, encoding="utf-8"))["deliverable_level"] == "full_reanalysis"
        assert "partial_support" in open(out_md, encoding="utf-8").read()


def test_untrustworthy_evidence_cannot_support_or_be_secondary():
    bad = AnalysisEvidence(
        evidence_id="E-BAD", accession="GSE2", evidence_type="deg",
        origin="computed", statement="67% of genes significant in a 2v2 contrast.",
        trustworthy=False, sanity_flags=["tiny_n_per_group", "implausible_sig_fraction"],
    )
    try:
        ArticleResultCard(
            article_id="PMID2", claims=[_claim()], evidence=[bad],
            links=[ClaimEvidenceLink(
                link_id="L-BAD", claim_id="CLM-1", evidence_id="E-BAD",
                relation="direct_support", rationale="Must be rejected.",
            )],
        )
        raise AssertionError("untrustworthy evidence was allowed to support a claim")
    except ValidationError as exc:
        assert "untrustworthy evidence" in str(exc)
    try:
        ArticleResultCard(
            article_id="PMID2", claims=[_claim()], evidence=[bad],
            links=[ClaimEvidenceLink(
                link_id="L-NE", claim_id="CLM-1", relation="not_evaluable",
                rationale="This contrast is not trustworthy.",
            )],
            secondary_findings=[SecondaryFinding(
                finding_id="F-BAD", statement="A false discovery.",
                evidence_ids=["E-BAD"], rationale="Must be rejected.",
            )],
        )
        raise AssertionError("untrustworthy evidence was allowed as a secondary finding")
    except ValidationError as exc:
        assert "untrustworthy evidence" in str(exc)


def test_rejection_of_inference_still_yields_descriptive_card():
    card = ArticleResultCard(
        article_id="PMID3",
        annotation_status="human_reviewed",
        claims=[_claim()],
        evidence=[AnalysisEvidence(
            evidence_id="E-QC", accession="GSE3", evidence_type="qc",
            origin="descriptive", statement="Four samples passed QC.", trustworthy=True,
        )],
        links=[ClaimEvidenceLink(
            link_id="L-NE", claim_id="CLM-1", relation="not_evaluable",
            rationale="The available accession measures liver, not skeletal muscle.",
            dimension_alignment={"tissue_or_cell": "mismatch"},
        )],
        limitations=["No compatible molecular evidence for the primary claim."],
    )
    assert card.deliverable_level == "descriptive_result"
    assert audit_result_card(card, verify_artifacts=False)["verdict"] == "pass"


def test_gold_placeholders_are_blocking():
    claim = _claim().model_copy(update={"source_locator": "SOURCE REQUIRED"})
    card = ArticleResultCard(
        article_id="PMID4", annotation_status="gold", claims=[claim],
        links=[ClaimEvidenceLink(
            link_id="L-NE", claim_id="CLM-1", relation="not_evaluable",
            rationale="No accession can test this endpoint.",
        )],
    )
    assert "gold_claim_source_incomplete" in audit_result_card(
        card, verify_artifacts=False
    )["blocking"]
if __name__ == "__main__":
    test_full_card_and_artifact_hash()
    test_untrustworthy_evidence_cannot_support_or_be_secondary()
    test_rejection_of_inference_still_yields_descriptive_card()
    test_gold_placeholders_are_blocking()
    print("ALL CLAIM-EVIDENCE TESTS PASSED")
