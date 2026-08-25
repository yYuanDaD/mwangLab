import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

from tools.claim_evidence import (
    AnalysisEvidence,
    ArticleResultCard,
    ClaimEvidenceLink,
    PaperClaim,
)


SCORE_PATH = Path("test/experiments/claim_evidence_alignment/score.py")
SPEC = importlib.util.spec_from_file_location("claim_evidence_score", SCORE_PATH)
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def _card(article: str, *, status: str = "gold", relation: str = "direct_support"):
    return ArticleResultCard(
        article_id=article,
        annotation_status=status,
        claims=[PaperClaim(
            claim_id="C1", statement="Claim", importance="primary",
            source_quote="A verbatim result sentence.", source_locator="Results paragraph 1",
        )],
        evidence=[AnalysisEvidence(
            evidence_id="E1", evidence_type="deg", origin="computed",
            statement="Computed evidence", trustworthy=True,
            source_locator="DEG_results_treatment_vs_control.csv",
        )],
        links=[ClaimEvidenceLink(
            link_id="L1", claim_id="C1", evidence_id="E1",
            relation=relation, rationale="Same scope and endpoint.",
        )],
    )


def test_score_card_detects_false_direct_support():
    gold = _card("P1", relation="secondary_finding")
    pred = _card("P1", status="machine_draft", relation="direct_support")
    score = MOD.score_card(gold, pred)
    assert score["relation_accuracy"] == 0.0
    assert score["false_direct_support"] == 1


def test_benchmark_refuses_unreviewed_templates():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        manifest = root / "gold_manifest.json"
        manifest.write_text(json.dumps({
            "cases": [{
                "case_id": "X", "annotation_status": "unreviewed", "gold_card": "gold/X.json"
            }]
        }), encoding="utf-8")
        report = MOD.score_benchmark(manifest, root / "predictions", repeats=3)
        assert report["verdict"] == "insufficient_gold"
        assert report["gold_case_count"] == 0
def test_six_case_three_repeat_benchmark_passes():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        gold_dir = root / "gold"
        predictions = root / "predictions"
        gold_dir.mkdir()
        cases = []
        for i in range(6):
            case_id = f"CASE{i}"
            gold = _card(f"P{i}")
            (gold_dir / f"{case_id}.json").write_text(
                gold.model_dump_json(indent=2), encoding="utf-8"
            )
            cases.append({
                "case_id": case_id,
                "annotation_status": "gold",
                "gold_card": f"gold/{case_id}.json",
            })
            for repeat in range(1, 4):
                repeat_dir = predictions / f"repeat_{repeat:02d}"
                repeat_dir.mkdir(parents=True, exist_ok=True)
                predicted = _card(f"P{i}", status="machine_draft")
                (repeat_dir / f"{case_id}.json").write_text(
                    predicted.model_dump_json(indent=2), encoding="utf-8"
                )
        manifest = root / "gold_manifest.json"
        manifest.write_text(json.dumps({"cases": cases}), encoding="utf-8")
        report = MOD.score_benchmark(manifest, predictions, repeats=3)
        assert report["verdict"] == "pass", report
        assert report["observed_predictions"] == 18
        assert report["metrics"]["relation_accuracy"] == 1.0
        assert report["metrics"]["stable_case_rate"] == 1.0


if __name__ == "__main__":
    test_score_card_detects_false_direct_support()
    test_benchmark_refuses_unreviewed_templates()
    test_six_case_three_repeat_benchmark_passes()
    print("ALL CLAIM-EVIDENCE SCORER TESTS PASSED")
