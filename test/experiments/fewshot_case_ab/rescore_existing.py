"""Re-score saved A/B model outputs without making any LLM calls."""

from __future__ import annotations

import argparse
from datetime import datetime
import hashlib
import importlib.util
import json
from pathlib import Path
import statistics
import sys


HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("fewshot_ab_runner", HERE / "run_experiment.py")
MOD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MOD
SPEC.loader.exec_module(MOD)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir")
    args = parser.parse_args()
    out = Path(args.output_dir).resolve()
    gold = json.loads((HERE / "gold_target.json").read_text(encoding="utf-8"))
    target = MOD.TARGET_PAPER.read_text(encoding="utf-8")
    records = []
    previous = json.loads((out / "scores.json").read_text(encoding="utf-8")) if (out / "scores.json").exists() else {}
    bundle_path = out / "condition_b_runtime_skill_bundle.txt"
    condition_b_sha256 = (
        hashlib.sha256(bundle_path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
        if bundle_path.exists()
        else previous.get("condition_b_sha256")
    )
    a_files = sorted(out.glob("condition_a_no_example_r*.json"))
    for a_path in a_files:
        repeat = int(a_path.stem.rsplit("r", 1)[1])
        b_candidates = sorted(out.glob(f"condition_b_*_r{repeat}.json"))
        if len(b_candidates) != 1:
            raise SystemExit(f"Expected one condition B file for repeat {repeat}, found {len(b_candidates)}")
        b_path = b_candidates[0]
        a = json.loads(a_path.read_text(encoding="utf-8"))
        b = json.loads(b_path.read_text(encoding="utf-8"))
        a["score"] = MOD._score(MOD.PaperWorkflowExtraction.model_validate(a["output"]), target, gold)
        b["score"] = MOD._score(MOD.PaperWorkflowExtraction.model_validate(b["output"]), target, gold)
        for condition in (a, b):
            usage = condition.get("usage", {})
            usage["estimated_usd"] = round(
                int(usage.get("input_tokens", 0)) * 3 / 1_000_000
                + int(usage.get("output_tokens", 0)) * 15 / 1_000_000, 6
            )
        MOD._write_json(a_path, a)
        MOD._write_json(b_path, b)
        records.append({
            "repeat": repeat, "condition_a": a, "condition_b": b,
            "delta_b_minus_a": round(b["score"]["total"] - a["score"]["total"], 2),
        })
    if not records:
        raise SystemExit(f"No saved condition files in {out}")
    aggregate = {
        "experiment": previous.get("experiment", "same target paper; condition A vs condition B"),
        "model": MOD.MODEL, "temperature": 0, "repeats": len(records),
        "target_paper": str(MOD.TARGET_PAPER.relative_to(MOD.ROOT)),
        "condition_b": previous.get("condition_b", "curated example"),
        "condition_b_sha256": condition_b_sha256,
        "records": records,
        "mean_score_a": round(statistics.mean(x["condition_a"]["score"]["total"] for x in records), 2),
        "mean_score_b": round(statistics.mean(x["condition_b"]["score"]["total"] for x in records), 2),
        "mean_delta_b_minus_a": round(statistics.mean(x["delta_b_minus_a"] for x in records), 2),
    }
    aggregate["acceptance"] = MOD._acceptance(records)
    MOD._write_json(out / "scores.json", aggregate)
    total_cost = sum(
        item[condition]["usage"].get("estimated_usd", 0.0)
        for item in records
        for condition in ("condition_a", "condition_b")
    )
    report = [
        "# Runtime-context A/B result (rescored)", "", f"- Model: `{MOD.MODEL}`",
        f"- Repeats: {len(records)}", f"- Condition B: **{aggregate['condition_b']}**",
        f"- Condition B SHA-256: `{condition_b_sha256}`" if condition_b_sha256 else "- Condition B SHA-256: unavailable",
        f"- Mean A (no added context): **{aggregate['mean_score_a']}**",
        f"- Mean B: **{aggregate['mean_score_b']}**",
        f"- Mean delta B-A: **{aggregate['mean_delta_b_minus_a']:+.2f}**", "",
        f"- Acceptance verdict: **{aggregate['acceptance']['verdict']}**",
        f"- Paired wins/ties/losses: **{aggregate['acceptance']['paired_wins']}/"
        f"{aggregate['acceptance']['paired_ties']}/{aggregate['acceptance']['paired_losses']}**",
        f"- Delta sample SD: **{aggregate['acceptance']['delta_sample_stdev']}**", "",
        f"- Total estimated model cost: **${total_cost:.4f}**", "",
        "A positive delta supports condition B only when blocking safety checks do not regress.",
    ]
    (out / "comparison.md").write_text("\n".join(report), encoding="utf-8")
    status_path = out / "run_status.json"
    if status_path.exists():
        status = json.loads(status_path.read_text(encoding="utf-8"))
        status.update({
            "status": "completed",
            "stage": "completed",
            "current_tool": None,
            "llm_calls": 2 * len(records),
            "estimated_cost_usd": round(total_cost, 6),
            "message": f"rescored mean delta={aggregate['mean_delta_b_minus_a']:+.2f}",
            "updated_at": datetime.now().isoformat(timespec="seconds"),
        })
        MOD._write_json(status_path, status)
    print(json.dumps({k: aggregate[k] for k in ("mean_score_a", "mean_score_b", "mean_delta_b_minus_a")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
