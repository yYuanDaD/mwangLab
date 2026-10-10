"""Score control/treatment decisions against the ExerGeneDB sample-level gold.

Decision sources scored on the same GEO metadata:
    name_match           keyword matching on group names (_auto_detect_contrasts), all levels
    llm                  external validator triple, accepted only with intent_match and
                         high/medium confidence (the production acceptance rule)
    llm_raw              the validator triple regardless of confidence, to see whether
                         uncertain answers were in fact right
    production_default   batch policy: confident Python pick skips the LLM
    production_strict    batch policy with llm_contrast_strict=True
    external             optional decisions CSV (Codex or manual review)

Decisions are made on the full GEO metadata table. Production first restricts
metadata to the samples present in the expression matrix, which can change a
pick for series whose matrix covers only part of the GEO samples.

The LLM sources run only with --llm. Every LLM call is written to
llm_records.jsonl with its exact inputs, output, model configuration, usage, and
a hash of the validator source for replay.

Run the gold export first:
    python scripts/fetch_exergenedb_labels.py
Then:
    python test/experiments/exergenedb_gold_contrast_eval/run_eval.py --limit 10
    python test/experiments/exergenedb_gold_contrast_eval/run_eval.py --llm
    python test/experiments/exergenedb_gold_contrast_eval/run_eval.py --decisions codex_decisions.csv

The external decisions CSV has columns accession, design_column, control_value,
treatment_value; one row per contrast; a row with an empty design_column records a refusal.
"""
from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

from tools.batch_tools import _auto_detect_contrasts, _python_pick_is_confident  # noqa: E402
from tools.contrast_gold import (  # noqa: E402
    llm_accepts, llm_triple, load_gold, production_route, score_contrast_set,
)
from tools.geo_tools import download_geo_data  # noqa: E402
from tools.llm_helpers import (  # noqa: E402
    llm_usage_checkpoint, llm_usage_summary, summarize_metadata_for_llm, validate_contrast_with_llm,
)
from tools.model_factory import resolve_model_config  # noqa: E402

# Identical to exergenedb_50_semantic_review/run_review.py so results are comparable.
TREATMENT = [
    "exercise", "exercised", "post", "after", "trained", "training",
    "running", "run", "treadmill", "swimming", "wheel", "acute",
    "endurance", "resistance", "active",
]
CONTROL = [
    "sedentary", "control", "pre", "before", "rest", "sham",
    "baseline", "untrained", "inactive", "non-exercise", "nonexercise",
]
VERDICTS = ["correct", "reversed", "mixed", "refused", "unresolvable", "unscorable"]
GOLD_DIR = ROOT / "test" / "validation" / "exergenedb_gold"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def git_commit() -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                              text=True, check=True).stdout.strip()
    except Exception:
        return "unknown"


def format_contrasts(contrasts) -> str:
    return "; ".join(f"{c} | {a} vs {b}" for c, a, b in contrasts)


def fetch_metadata(accession: str, data_dir: Path, allow_download: bool) -> tuple[Path | None, str]:
    path = data_dir / accession / f"{accession}_metadata.csv"
    if path.exists() and path.stat().st_size > 0:
        return path, "cached"
    if not allow_download:
        return None, "missing"
    args = {"geo_accession": accession, "base_dir": str(data_dir)}
    message = (download_geo_data.invoke(args) if hasattr(download_geo_data, "invoke")
               else download_geo_data(**args))
    if path.exists() and path.stat().st_size > 0:
        return path, "downloaded"
    return None, f"download_failed: {str(message)[:200]}"


def load_external_decisions(path: str | None) -> dict[str, list[tuple[str, str, str]]]:
    if not path:
        return {}
    table = pd.read_csv(path, dtype=str).fillna("")
    decisions: dict[str, list[tuple[str, str, str]]] = {}
    for row in table.itertuples(index=False):
        contrasts = decisions.setdefault(row.accession, [])
        if row.design_column:
            contrasts.append((row.design_column, row.control_value, row.treatment_value))
    return decisions


def add_scored(row: dict, prefix: str, scored: dict) -> None:
    row[f"{prefix}_verdict"] = scored["verdict"]
    row[f"{prefix}_purity"] = scored["purity"]
    row[f"{prefix}_n_contrasts"] = scored["n_contrasts"]
    row[f"{prefix}_max_gold_strata"] = scored["max_gold_strata"]
    row[f"{prefix}_pairing_signal"] = ";".join(scored["pairing_signal"])
    row[f"{prefix}_executable"] = scored.get("all_columns_executable")
    row[f"{prefix}_contrasts"] = "; ".join(c["contrast"] for c in scored["contrasts"])


def evaluate_series(series: dict, gold, meta_path: Path, args, external, llm_log) -> dict:
    accession = series["accession"]
    meta = pd.read_csv(meta_path, index_col=0)
    meta.index = meta.index.astype(str)
    series_gold = gold[gold["series_id"] == accession]
    roles = series_gold["role"]
    overlap = int(meta.index.isin(series_gold.index).sum())
    row = {
        "accession": accession,
        "organism": series.get("organism"),
        "seqtech": series.get("seqtech"),
        "design_class": series.get("design_class"),
        "n_gold_samples": len(series_gold),
        "n_metadata_samples": len(meta),
        "n_metadata_in_gold": overlap,
        "metadata_sha256": sha256_file(meta_path),
    }
    if overlap == 0:
        row["status"] = "no_gold_overlap"
        return row
    row["status"] = "evaluated"

    python_contrasts = [tuple(c) for c in _auto_detect_contrasts(str(meta_path), TREATMENT, CONTROL)]
    design = python_contrasts[0] if python_contrasts else None
    confident = bool(_python_pick_is_confident(str(meta_path), design, TREATMENT, CONTROL))
    row["python_contrasts"] = format_contrasts(python_contrasts)
    row["python_confident"] = confident
    add_scored(row, "name_match", score_contrast_set(meta, roles, python_contrasts, series_gold))

    llm = None
    if args.llm:
        summary = summarize_metadata_for_llm(str(meta_path))
        checkpoint = llm_usage_checkpoint()
        result = validate_contrast_with_llm(
            accession=accession, metadata_columns_summary=summary,
            treatment_keywords=TREATMENT, control_keywords=CONTROL, proposed=design)
        llm = result.model_dump() if result is not None else None
        usage = llm_usage_summary(checkpoint)
        llm_log.write(json.dumps({
            "accession": accession,
            "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "metadata_sha256": row["metadata_sha256"],
            "inputs": {"metadata_columns_summary": summary, "treatment_keywords": TREATMENT,
                       "control_keywords": CONTROL, "proposed": list(design) if design else None},
            "output": llm,
            "usage": {k: v for k, v in usage.items() if k != "calls"},
        }, ensure_ascii=False) + "\n")
        row["llm_called"] = True
        row["llm_available"] = llm is not None
        row["llm_triple"] = format_contrasts([llm_triple(llm)]) if llm_triple(llm) else ""
        row["llm_is_valid"] = (llm or {}).get("is_valid")
        row["llm_confidence"] = (llm or {}).get("confidence")
        row["llm_intent_match"] = (llm or {}).get("intent_match")
        row["llm_reasoning"] = (llm or {}).get("reasoning")
        row["llm_accepted"] = llm_accepts(llm)
        raw = [llm_triple(llm)] if llm_triple(llm) else []
        add_scored(row, "llm_raw", score_contrast_set(meta, roles, raw, series_gold))
        accepted = raw if llm_accepts(llm) else []
        add_scored(row, "llm", score_contrast_set(meta, roles, accepted, series_gold))
        for prefix, strict in (("production_default", False), ("production_strict", True)):
            contrasts, route = production_route(python_contrasts, confident, llm, strict=strict)
            row[f"{prefix}_route"] = route
            add_scored(row, prefix, score_contrast_set(meta, roles, contrasts, series_gold))
    else:
        row["llm_called"] = False
        if confident:
            contrasts, route = production_route(python_contrasts, confident, None)
            row["production_default_route"] = route
            add_scored(row, "production_default", score_contrast_set(meta, roles, contrasts, series_gold))
        else:
            row["production_default_route"] = "needs_llm_not_called"

    if accession in external:
        add_scored(row, "external", score_contrast_set(meta, roles, external[accession], series_gold))
    return row


def verdict_counts(frame: pd.DataFrame, prefix: str) -> dict:
    column = f"{prefix}_verdict"
    if column not in frame.columns:
        return {}
    scored = frame[frame[column].notna()]
    counts = {v: int((scored[column] == v).sum()) for v in VERDICTS}
    n = len(scored)
    counts["n"] = n
    counts["accuracy"] = round(counts["correct"] / n, 4) if n else None
    counts["wrong_rate"] = round((counts["reversed"] + counts["mixed"]) / n, 4) if n else None
    counts["refusal_rate"] = round(counts["refused"] / n, 4) if n else None
    return counts


def build_summary(frame: pd.DataFrame, methods: list[str]) -> dict:
    evaluated = frame[frame["status"] == "evaluated"]
    summary = {
        "n_series": len(frame),
        "n_evaluated": len(evaluated),
        "status_counts": frame["status"].value_counts().to_dict(),
        "methods": {},
    }
    for method in methods:
        overall = verdict_counts(evaluated, method)
        if not overall:
            continue
        by_class = {cls: verdict_counts(group, method)
                    for cls, group in evaluated.groupby("design_class")}
        summary["methods"][method] = {"overall": overall, "by_design_class": by_class}

    if "python_confident" not in evaluated.columns:
        evaluated = evaluated.assign(python_confident=False, name_match_verdict=None,
                                     name_match_contrasts=None)
    confident = evaluated[evaluated["python_confident"] == True]  # noqa: E712
    summary["name_match_direct_pass"] = {
        "python_confident": len(confident),
        "confident_and_correct": int((confident["name_match_verdict"] == "correct").sum()),
        "share_of_evaluated_correct_without_llm": (
            round(int((confident["name_match_verdict"] == "correct").sum()) / len(evaluated), 4)
            if len(evaluated) else None),
        "confident_but_not_correct": confident.loc[
            confident["name_match_verdict"] != "correct",
            ["accession", "name_match_verdict", "name_match_contrasts"]].to_dict("records"),
    }
    if "llm_accepted" in evaluated.columns:
        uncertain = evaluated[evaluated["llm_accepted"] != True]  # noqa: E712
        summary["llm_not_accepted"] = {
            "n": len(uncertain),
            "raw_verdict_counts": uncertain["llm_raw_verdict"].value_counts().to_dict(),
            "cases": uncertain[["accession", "design_class", "llm_confidence", "llm_intent_match",
                                "llm_raw_verdict", "llm_reasoning"]].to_dict("records"),
        }
    for prefix in ("production_default", "production_strict"):
        column = f"{prefix}_verdict"
        if prefix not in methods or column not in evaluated.columns:
            continue
        correct = evaluated[evaluated[column] == "correct"]
        summary[f"{prefix}_covariance_flags"] = {
            "correct_contrast_sets": len(correct),
            "with_pairing_signal": int((correct[f"{prefix}_pairing_signal"].fillna("") != "").sum()),
            "mixing_gold_strata": int((correct[f"{prefix}_max_gold_strata"] > 1).sum()),
            "non_executable_column": int((correct[f"{prefix}_executable"] == False).sum()),  # noqa: E712
        }
    return summary


def markdown_table(header: list[str], rows: list[list]) -> str:
    lines = ["| " + " | ".join(header) + " |", "|" + "---|" * len(header)]
    lines += ["| " + " | ".join("" if v is None else str(v) for v in r) + " |" for r in rows]
    return "\n".join(lines)


def render_markdown(summary: dict, manifest: dict) -> str:
    header = ["method", "n", "correct", "reversed", "mixed", "refused", "unresolvable",
              "unscorable", "accuracy", "wrong_rate"]
    overall_rows, class_rows = [], []
    for method, block in summary["methods"].items():
        o = block["overall"]
        overall_rows.append([method] + [o.get(k) for k in header[1:]])
        for cls, c in block["by_design_class"].items():
            class_rows.append([f"{method} / {cls}"] + [c.get(k) for k in header[1:]])
    direct = summary["name_match_direct_pass"]
    parts = [
        "# ExerGeneDB control/treatment gold evaluation",
        f"Gold: `{manifest['gold_samples']}` (sha256 `{manifest['gold_sha256'][:12]}`); "
        f"commit `{manifest['git_commit'][:10]}`; LLM: {manifest['llm']}",
        f"Series: {summary['n_series']}, evaluated: {summary['n_evaluated']}, "
        f"status: {summary['status_counts']}",
        "## Overall", markdown_table(header, overall_rows),
        "## By design class", markdown_table(header, class_rows),
        "## Name matching without the LLM",
        f"Confident Python picks: {direct['python_confident']}; correct: "
        f"{direct['confident_and_correct']}; share of evaluated series classified correctly "
        f"without the LLM: {direct['share_of_evaluated_correct_without_llm']}.",
        f"Confident but not correct (these skip the LLM in production): "
        f"{len(direct['confident_but_not_correct'])}",
    ]
    if direct["confident_but_not_correct"]:
        parts.append(markdown_table(
            ["accession", "verdict", "contrasts"],
            [[r["accession"], r["name_match_verdict"], r["name_match_contrasts"]]
             for r in direct["confident_but_not_correct"]]))
    if "llm_not_accepted" in summary:
        block = summary["llm_not_accepted"]
        parts += ["## LLM answers not accepted",
                  f"{block['n']} cases; raw-triple verdicts: {block['raw_verdict_counts']}. "
                  "Categorize each reason in llm_records.jsonl as insufficient evidence "
                  "(acceptable) or a model error."]
    for prefix in ("production_default", "production_strict"):
        key = f"{prefix}_covariance_flags"
        if key in summary:
            parts += [f"## Covariance flags on correct {prefix} contrasts", json.dumps(summary[key])]
    return "\n\n".join(parts) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score contrast decisions against ExerGeneDB gold.")
    parser.add_argument("--gold-dir", default=str(GOLD_DIR))
    parser.add_argument("--data-dir", default=str(ROOT / "data"))
    parser.add_argument("--out-dir", default=None)
    parser.add_argument("--accessions", nargs="*", default=None)
    parser.add_argument("--design-class", default=None,
                        help="simple, multi_time, multi_strata, or multi_time_and_strata")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--llm", action="store_true", help="call the configured external validator")
    parser.add_argument("--decisions", default=None, help="external decisions CSV to score")
    parser.add_argument("--no-download", action="store_true")
    args = parser.parse_args(argv)

    gold_dir = Path(args.gold_dir)
    samples_csv = gold_dir / "exergenedb_samples.csv"
    series_csv = gold_dir / "exergenedb_series.csv"
    if not samples_csv.exists() or not series_csv.exists():
        print(f"gold files not found in {gold_dir}; run scripts/fetch_exergenedb_labels.py first")
        return 2
    if args.llm:
        from tools.llm_helpers import _get_validation_llm
        if _get_validation_llm() is None:
            print("--llm was requested but the validator is unavailable (check provider and API key)")
            return 2

    gold = load_gold(str(samples_csv))
    series = pd.read_csv(series_csv, dtype={"accession": str})
    series = series[series["is_geo_series"].astype(str).str.lower() == "true"]
    if args.accessions:
        series = series[series["accession"].isin(args.accessions)]
    if args.design_class:
        series = series[series["design_class"] == args.design_class]
    if args.limit:
        series = series.head(args.limit)

    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = Path(args.out_dir or ROOT / "output" / f"exergenedb_gold_contrast_eval_{stamp}")
    out_dir.mkdir(parents=True, exist_ok=True)
    external = load_external_decisions(args.decisions)
    config = resolve_model_config() if args.llm else None
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "git_commit": git_commit(),
        "gold_samples": str(samples_csv.relative_to(ROOT) if samples_csv.is_relative_to(ROOT) else samples_csv),
        "gold_sha256": sha256_file(samples_csv),
        "series_selected": series["accession"].tolist(),
        "treatment_keywords": TREATMENT,
        "control_keywords": CONTROL,
        "llm": f"{config.provider}:{config.model}" if config else "not called",
        "validator_source_sha256": hashlib.sha256(
            inspect.getsource(validate_contrast_with_llm).encode("utf-8")).hexdigest(),
        "external_decisions": args.decisions,
    }

    rows = []
    start = llm_usage_checkpoint()
    with (out_dir / "llm_records.jsonl").open("w", encoding="utf-8") as llm_log:
        for record in series.to_dict("records"):
            accession = record["accession"]
            meta_path, how = fetch_metadata(accession, Path(args.data_dir), not args.no_download)
            if meta_path is None:
                rows.append({"accession": accession, "design_class": record.get("design_class"),
                             "status": "metadata_unavailable", "metadata_note": how})
                print(f"{accession}: metadata unavailable ({how})")
                continue
            try:
                row = evaluate_series(record, gold, meta_path, args, external, llm_log)
            except Exception as exc:
                row = {"accession": accession, "design_class": record.get("design_class"),
                       "status": "error", "metadata_note": f"{type(exc).__name__}: {exc}"}
            rows.append(row)
            print(f"{accession}: {row.get('status')} | name_match={row.get('name_match_verdict')} "
                  f"| production={row.get('production_default_verdict')}")

    frame = pd.DataFrame(rows)
    frame.to_csv(out_dir / "per_series.csv", index=False)
    # Without --llm, production_default is only defined on the confident subset,
    # which name_match_direct_pass already reports.
    methods = ["name_match", "external"]
    if args.llm:
        methods[1:1] = ["llm", "llm_raw", "production_default", "production_strict"]
    summary = build_summary(frame, methods)
    usage = llm_usage_summary(start)
    summary["llm_usage"] = {k: v for k, v in usage.items() if k != "calls"}
    (out_dir / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False, default=str),
                                          encoding="utf-8")
    (out_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    (out_dir / "summary.md").write_text(render_markdown(summary, manifest), encoding="utf-8")
    print(f"wrote {out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
