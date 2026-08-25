import os
import sys
import tempfile
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_ROOT = _HERE.parents[1]
os.chdir(_ROOT)
sys.path.insert(0, str(_ROOT))

from test.experiments.claim_evidence_alignment import prefill
from tools.claim_evidence import (
    AnalysisEvidence, ArticleResultCard, BiologicalScope, ClaimEvidenceLink,
    PaperClaim,
)


def test_quote_verification_and_excerpt_are_deterministic():
    paper = "Abstract\nA primary result was observed.\n\nResults\nPathway A increased.\n"
    assert prefill.verify_quote(paper, "A primary result   was observed.") is not None
    assert prefill.verify_quote(paper, "A result that was never written.") is None
    assert prefill.build_paper_excerpt(paper, 8000) == prefill.build_paper_excerpt(paper, 8000)


def test_unverified_machine_quotes_are_discarded():
    raw = prefill.PaperExtraction(claims=[
        prefill.ExtractedClaim(
            statement="Verified claim", importance="primary",
            source_quote="The intervention improved recovery.",
            source_locator="Abstract", scope=BiologicalScope(),
        ),
        prefill.ExtractedClaim(
            statement="Hallucinated claim", importance="secondary",
            source_quote="This sentence is absent from the paper.",
            source_locator="Results", scope=BiologicalScope(),
        ),
    ])
    claims, _, limitations = prefill.verified_extraction(
        raw, "Abstract: The intervention improved recovery.", "paper.txt"
    )
    assert [x.statement for x in claims] == ["Verified claim"]
    assert any("unverified claim quote" in x for x in limitations)


def test_unsafe_relation_is_downgraded():
    claim = PaperClaim(
        claim_id="CLM-1", statement="Claim", importance="primary",
        source_quote="A sufficiently long source quote.", source_locator="Abstract",
    )
    evidence = AnalysisEvidence(
        evidence_id="E-BAD", evidence_type="deg", origin="computed",
        statement="Untrustworthy DEG.", trustworthy=False,
    )
    raw = prefill.RelationExtraction(links=[prefill.ProposedLink(
        claim_id="CLM-1", evidence_id="E-BAD", relation="direct_support",
        rationale="Machine proposed unsafe support.",
    )])
    links, _, limitations = prefill.validated_links(raw, [claim], [evidence])
    assert links[0].relation == "not_evaluable"
    assert links[0].evidence_id is None
    assert any("Downgraded unsafe relation" in x for x in limitations)


def test_budget_reservation_is_hard_stop_without_call():
    prefill.reset_llm_usage()
    controller = prefill.BudgetController(
        budget_usd=0.000001, max_calls=1,
        checkpoint=prefill.llm_usage_checkpoint(),
        provider="deepseek", model="deepseek-v4-pro",
    )
    try:
        controller.reserve("x" * 1000)
        raise AssertionError("tiny budget did not block the call")
    except prefill.BudgetExceeded:
        pass
    assert controller.usage()["llm_calls"] == 0


def test_failed_da_becomes_descriptive_not_supporting_evidence():
    original_root = prefill.ROOT
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        run_dir = root / "output" / "cohort_GSE1" / "GSE1"
        run_dir.mkdir(parents=True)
        (run_dir.parent / "summary.csv").write_text(
            "accession,status,n_samples,contrasts,deg_sanity\n"
            "GSE1,deg_failed,8,Treatment vs Control,ok\n", encoding="utf-8"
        )
        (run_dir / "GSE1_sample_qc.tsv").write_text("sample\tdepth\nS1\t10\n", encoding="utf-8")
        try:
            prefill.ROOT = root
            evidence, limitations = prefill.build_computed_evidence({
                "case_id": "GSE1", "run_dir": "output/cohort_GSE1/GSE1"
            })
        finally:
            prefill.ROOT = original_root
    block = next(x for x in evidence if x.evidence_id == "E-DA-BLOCK")
    assert block.origin == "descriptive"
    assert not any(x.evidence_type in {"deg", "gsea"} for x in evidence)
    assert any("rejected" in x for x in limitations)


def test_finalizer_downgrades_weak_direct_and_keeps_computed_secondary():
    claim = PaperClaim(
        claim_id="CLM-1", statement="Compound claim", importance="primary",
        source_quote="A sufficiently long source quote.", source_locator="Abstract",
    )
    paper_ev = AnalysisEvidence(
        evidence_id="E-PAPER", evidence_type="reported_result",
        origin="paper_reported", statement="One component was reported.",
        trustworthy=True,
    )
    gsea_ev = AnalysisEvidence(
        evidence_id="E-GSEA", evidence_type="gsea", origin="computed",
        statement="An unrelated pathway was enriched.", trustworthy=True,
    )
    card = ArticleResultCard(
        article_id="PMID1", claims=[claim], evidence=[paper_ev, gsea_ev],
        links=[ClaimEvidenceLink(
            link_id="LNK-1", claim_id="CLM-1", evidence_id="E-PAPER",
            relation="direct_support", rationale="One component matches.",
            confidence=0.85,
        )],
    )
    final = prefill.conservative_finalize_card(card)
    assert final.links[0].relation == "partial_support"
    assert final.secondary_findings[0].evidence_ids == ["E-GSEA"]

if __name__ == "__main__":
    test_quote_verification_and_excerpt_are_deterministic()
    test_unverified_machine_quotes_are_discarded()
    test_unsafe_relation_is_downgraded()
    test_budget_reservation_is_hard_stop_without_call()
    test_failed_da_becomes_descriptive_not_supporting_evidence()
    test_finalizer_downgrades_weak_direct_and_keeps_computed_secondary()
    print("ALL CLAIM-EVIDENCE PREFILL TESTS PASSED")
