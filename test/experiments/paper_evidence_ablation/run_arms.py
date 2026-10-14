"""Paper-evidence ablation: does the article text improve control/treatment decisions?

Same model, same prompt, same metadata summary and Python proposal in every arm; only
the paper evidence block changes:

    metadata     no paper text (production validator inputs)
    abstract     title + abstract
    structured   abstract + Methods + data availability + all tables + all figure legends,
                 with block IDs (tools.paper_structure)
    flat         the historical flat .txt (whole JATS text joined on spaces), same char cap

Every decision is scored against the ExerGeneDB sample-level gold with the scorer used by
exergenedb_gold_contrast_eval (tools.contrast_gold.score_contrast_set). Each call is logged
with its exact prompt hash, evidence size, output, token usage, and wall time, and runs
resume from the log.

    python test/experiments/paper_evidence_ablation/run_arms.py --repeats 1 --limit 4   # pilot
    python test/experiments/paper_evidence_ablation/run_arms.py --repeats 3              # full
    python test/experiments/paper_evidence_ablation/run_arms.py --score-only
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import pandas as pd
from pydantic import Field

ROOT = Path(__file__).resolve().parents[3]
os.chdir(ROOT)
sys.path.insert(0, str(ROOT))

try:  # This experiment never runs differential expression. batch_tools imports inmoose at
    import inmoose  # noqa: F401  module load, so stub it when the package is not installed.
except ImportError:
    import importlib.abc
    import importlib.machinery
    import types

    class _Stub(types.ModuleType):
        def __getattr__(self, name):
            if name.startswith("__"):
                raise AttributeError(name)
            return lambda *a, **k: (_ for _ in ()).throw(RuntimeError("inmoose stub: DE is not run here"))

    class _StubFinder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
        def find_spec(self, fullname, path, target=None):
            if fullname == "inmoose" or fullname.startswith("inmoose."):
                return importlib.machinery.ModuleSpec(fullname, self, is_package=True)
            return None

        def create_module(self, spec):
            mod = _Stub(spec.name)
            mod.__path__ = []
            return mod

        def exec_module(self, module):
            pass

    sys.meta_path.insert(0, _StubFinder())

from tools import paper_structure as ps  # noqa: E402
from tools.batch_tools import _auto_detect_contrasts, _python_pick_is_confident  # noqa: E402
from tools.contrast_gold import llm_accepts, llm_triple, load_gold, score_contrast_set  # noqa: E402
from tools.llm_helpers import (  # noqa: E402
    ContrastValidationResult, _invoke_structured, estimate_llm_cost_usd, summarize_metadata_for_llm,
)
from tools.model_factory import create_structured_chat_model, resolve_model_config  # noqa: E402
from tools.paper_tools import _flatten_jats  # noqa: E402

HERE = Path(__file__).parent
GOLD = ROOT / "test" / "validation" / "exergenedb_gold" / "exergenedb_samples.csv"
ARMS = ("metadata", "abstract", "structured", "flat")
CHAR_CAP = 100_000  # same cap for structured and flat, about 25k tokens

# Identical to exergenedb_gold_contrast_eval so the metadata arm is comparable.
TREATMENT = ["exercise", "exercised", "post", "after", "trained", "training", "running", "run",
             "treadmill", "swimming", "wheel", "acute", "endurance", "resistance", "active"]
CONTROL = ["sedentary", "control", "pre", "before", "rest", "sham", "baseline", "untrained",
           "inactive", "non-exercise", "nonexercise"]


class AblationDecision(ContrastValidationResult):
    pairing: str = Field(
        default="unknown",
        description="Exactly one of: required, not_required, unknown. 'required' when the same "
                    "subjects/animals contribute samples to both groups (pre/post, before/after in the "
                    "same person), so the analysis must block on subject.")
    pairing_column: Optional[str] = Field(
        default=None, description="Metadata column that identifies the subject when pairing is required.")
    paper_locators: list[str] = Field(
        default_factory=list,
        description="Block IDs from the PAPER EVIDENCE (e.g. 'S2.3.p1', 'TAB1', 'FIG2') that support the "
                    "decision. Empty when no paper evidence was given or none was used.")


def evidence_for(arm: str, paper_json: str) -> tuple[str, dict]:
    if arm == "metadata":
        return "", {"chars": 0}
    doc = ps.load(paper_json)
    title = doc.get("title") or ""
    if arm == "abstract":
        text = f"Title: {title}\n\n" + ps.read_section(doc, "abstract")
    elif arm == "structured":
        text = f"Title: {title}\n\n" + ps.read_section(
            doc, "abstract,methods,data_availability,tables,figures")
    elif arm == "flat":
        xml = Path(paper_json[: -len(".paper.json")] + ".jats.xml").read_bytes()
        text = _flatten_jats(xml)
    else:
        raise ValueError(arm)
    info = {"chars": len(text), "truncated": len(text) > CHAR_CAP}
    return text[:CHAR_CAP], info


def build_prompt(accession: str, summary: dict, proposed, evidence: str) -> str:
    if proposed is not None:
        proposed_str = (f"Python heuristic picked:\n  design_column = {proposed[0]!r}\n"
                        f"  control_value = {proposed[1]!r}\n  treatment_value = {proposed[2]!r}")
    else:
        proposed_str = "Python heuristic found NO clean contrast."
    if evidence:
        paper = ("PAPER EVIDENCE (the article that deposited this series). Block IDs are in [brackets].\n"
                 "<paper>\n" + evidence + "\n</paper>\n\n"
                 "Use the paper to decide which GEO groups are the exercise arm and which are the control "
                 "(sedentary, pre-exercise, sham, baseline), and whether the same subjects appear in both. "
                 "The contrast must still use a metadata column and values listed below. Cite the blocks you "
                 "relied on in paper_locators.\n")
    else:
        paper = "PAPER EVIDENCE: none provided.\n"
    return f"""You are validating a control-vs-treatment contrast for RNA-seq differential expression analysis.

Study: {accession}
User intent — control keywords: {CONTROL}
User intent — treatment keywords: {TREATMENT}

{proposed_str}

Candidate metadata columns and their unique values (with per-value sample counts):
{json.dumps(summary, indent=2, ensure_ascii=False)}

{paper}
Your job:
1. If a contrast was proposed above, decide whether it is biologically sensible for the user's intent.
   If NO contrast was proposed, find the best 2-group contrast yourself.
2. Common failure modes to catch:
   - Wrong column type (e.g. picked 'genotype' when 'treatment' would be cleaner)
   - Wrong values (e.g. picked 'untreated' as control when the real control is 'baseline')
   - Ambiguous values (e.g. 'sedentary control' counted as both)
   - Multi-factor / time-course design: pick the single 2-group pair that best answers the user's
     intent (e.g. baseline/pre vs the primary treated/post group).
3. Report your recommended contrast in design_column / control_value / treatment_value when a clean
   2-group split exists that matches the user's intent. The values MUST appear verbatim in that
   column's unique_values. Leave all three fields null when the study has no matching intent axis.
4. Set is_valid=true ONLY when you are confirming the proposed pick unchanged.
5. Prefer columns where both groups have at least 3 samples.
6. Set intent_match=true only when the recommended contrast directly tests exercise versus its control.
   Do not substitute a disease, genotype, diet or drug contrast.
7. Set pairing (required / not_required / unknown) and, when required, pairing_column.

Return your decision via the structured schema.
"""


def series_inputs(rec: dict) -> dict:
    meta_csv = str(ROOT / rec["metadata_csv"])
    proposals = [tuple(c) for c in _auto_detect_contrasts(meta_csv, TREATMENT, CONTROL)]
    design = proposals[0] if proposals else None
    return {"summary": summarize_metadata_for_llm(meta_csv), "proposed": design,
            "python_confident": bool(_python_pick_is_confident(meta_csv, design, TREATMENT, CONTROL))}


def call_once(llm, prompt: str) -> tuple[Optional[dict], dict]:
    t0 = time.time()
    try:
        runnable = llm.with_structured_output(AblationDecision, include_raw=True)
        resp = runnable.invoke(prompt)
        raw, parsed, err = resp.get("raw"), resp.get("parsed"), resp.get("parsing_error")
        usage = dict(getattr(raw, "usage_metadata", None) or {})
        out = parsed.model_dump() if parsed is not None and err is None else None
        status = "ok" if out else f"parse_error: {err}"
    except Exception as e:  # network/provider errors are logged, not fatal
        out, usage, status = None, {}, f"error: {type(e).__name__}: {str(e)[:200]}"
    return out, {"status": status, "seconds": round(time.time() - t0, 2),
                 "input_tokens": int(usage.get("input_tokens", 0) or 0),
                 "output_tokens": int(usage.get("output_tokens", 0) or 0)}


def run(args) -> None:
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    series = manifest["series"][: args.limit] if args.limit else manifest["series"]
    log_path = HERE / args.log
    done = set()
    if log_path.exists():
        for line in log_path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if r["call"]["status"] == "ok":
                done.add((r["accession"], r["arm"], r["repeat"]))
    cfg = resolve_model_config()
    llm = create_structured_chat_model()
    model_info = {"provider": cfg.provider, "model": cfg.model}
    print(f"model: {model_info}; series: {len(series)}; arms: {args.arms}; repeats: {args.repeats}; "
          f"already done: {len(done)}", flush=True)

    jobs = []
    for rec in series:
        inputs = series_inputs(rec)
        for arm in args.arms:
            evidence, info = evidence_for(arm, str(ROOT / rec["paper_json"]))
            prompt = build_prompt(rec["accession"], inputs["summary"], inputs["proposed"], evidence)
            for rep in range(args.repeats):
                if (rec["accession"], arm, rep) not in done:
                    jobs.append((rec, arm, rep, prompt, info, inputs))
    print(f"calls to make: {len(jobs)}", flush=True)
    lock = threading.Lock()

    def work(job):
        rec, arm, rep, prompt, info, inputs = job
        out, call = call_once(llm, prompt)
        entry = {"accession": rec["accession"], "arm": arm, "repeat": rep,
                 "timestamp": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                 "model": model_info, "prompt_sha256": hashlib.sha256(prompt.encode()).hexdigest(),
                 "evidence": info, "proposed": list(inputs["proposed"]) if inputs["proposed"] else None,
                 "python_confident": inputs["python_confident"], "output": out, "call": call}
        with lock, log_path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        return rec["accession"], arm, rep, call["status"]

    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(work, j) for j in jobs]
        for i, fut in enumerate(as_completed(futures), 1):
            acc, arm, rep, status = fut.result()
            print(f"[{i}/{len(jobs)}] {acc} {arm} r{rep}: {status}", flush=True)


def score(args) -> None:
    manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
    recs = {r["accession"]: r for r in manifest["series"]}
    gold = load_gold(str(GOLD))
    entries = [json.loads(l) for l in (HERE / args.log).read_text(encoding="utf-8").splitlines()]
    latest: dict = {}
    for e in entries:  # keep the last ok entry per key; otherwise the last attempt
        key = (e["accession"], e["arm"], e["repeat"])
        if e["call"]["status"] == "ok" or key not in latest or latest[key]["call"]["status"] != "ok":
            latest[key] = e
    meta_cache, docs = {}, {}
    rows = []
    for (acc, arm, rep), e in sorted(latest.items()):
        rec = recs[acc]
        if acc not in meta_cache:
            m = pd.read_csv(ROOT / rec["metadata_csv"], index_col=0)
            m.index = m.index.astype(str)
            meta_cache[acc] = m
            docs[acc] = ps.load(str(ROOT / rec["paper_json"]))
        meta = meta_cache[acc]
        sg = gold[gold["series_id"] == acc]
        out = e["output"]
        raw = [llm_triple(out)] if out and llm_triple(out) else []
        accepted = raw if out and llm_accepts(out) else []
        s_raw = score_contrast_set(meta, sg["role"], raw, sg)
        s_acc = score_contrast_set(meta, sg["role"], accepted, sg)
        locs = (out or {}).get("paper_locators") or []
        resolved = [l for l in locs if ps.resolve_locator(docs[acc], l)]
        cost = estimate_llm_cost_usd(e["model"]["provider"], e["model"]["model"],
                                     e["call"]["input_tokens"], e["call"]["output_tokens"])
        rows.append({
            "accession": acc, "design_class": rec["design_class"], "arm": arm, "repeat": rep,
            "call_status": e["call"]["status"], "evidence_chars": e["evidence"].get("chars", 0),
            "evidence_truncated": e["evidence"].get("truncated", False),
            "triple": " | ".join(raw[0]) if raw else "", "confidence": (out or {}).get("confidence"),
            "intent_match": (out or {}).get("intent_match"), "accepted": bool(accepted),
            "raw_verdict": s_raw["verdict"], "raw_purity": s_raw["purity"],
            "accepted_verdict": s_acc["verdict"], "pairing": (out or {}).get("pairing"),
            "pairing_column": (out or {}).get("pairing_column"),
            "pairing_signal": ";".join(s_raw["pairing_signal"]),
            "n_locators": len(locs), "n_locators_resolved": len(resolved),
            "input_tokens": e["call"]["input_tokens"], "output_tokens": e["call"]["output_tokens"],
            "cost_usd": cost, "seconds": e["call"]["seconds"],
            "python_confident": e["python_confident"], "reasoning": (out or {}).get("reasoning"),
        })
    df = pd.DataFrame(rows)
    df.to_csv(HERE / "scored_calls.csv", index=False)

    def arm_summary(g: pd.DataFrame) -> dict:
        n = len(g)
        ok = g[g["call_status"] == "ok"]
        rv, av = ok["raw_verdict"], ok["accepted_verdict"]
        return {
            "calls": n, "ok_calls": len(ok),
            "raw_correct": round((rv == "correct").mean(), 3) if len(ok) else None,
            "raw_wrong": round(rv.isin(["reversed", "mixed"]).mean(), 3) if len(ok) else None,
            "raw_refused": round((rv == "refused").mean(), 3) if len(ok) else None,
            "accepted_rate": round(ok["accepted"].mean(), 3) if len(ok) else None,
            "accepted_correct": round((av == "correct").mean(), 3) if len(ok) else None,
            "accepted_wrong": round(av.isin(["reversed", "mixed"]).mean(), 3) if len(ok) else None,
            "manual_review_rate": round(1 - ok["accepted"].mean(), 3) if len(ok) else None,
            "pairing_required": round((ok["pairing"] == "required").mean(), 3) if len(ok) else None,
            "locator_resolve_rate": (round(ok["n_locators_resolved"].sum() / ok["n_locators"].sum(), 3)
                                     if ok["n_locators"].sum() else None),
            "mean_input_tokens": int(ok["input_tokens"].mean()) if len(ok) else None,
            "total_cost_usd": round(float(ok["cost_usd"].sum()), 4),
            "mean_seconds": round(float(ok["seconds"].mean()), 1) if len(ok) else None,
        }

    summary = {"arms": {a: arm_summary(g) for a, g in df.groupby("arm")},
               "by_design_class": {f"{a} / {c}": arm_summary(g)
                                   for (a, c), g in df.groupby(["arm", "design_class"])}}
    # Stability: share of series whose triple is identical across repeats, per arm.
    stab = {}
    for a, g in df[df["call_status"] == "ok"].groupby("arm"):
        per = g.groupby("accession")["triple"].nunique()
        stab[a] = round(float((per == 1).mean()), 3) if len(per) else None
    summary["stability_identical_triple"] = stab
    # Series where arms disagree on the raw verdict (majority over repeats).
    maj = (df[df["call_status"] == "ok"].groupby(["accession", "arm"])["raw_verdict"]
           .agg(lambda s: s.value_counts().index[0]).unstack())
    summary["disagreements"] = maj[maj.nunique(axis=1) > 1].reset_index().to_dict("records")
    (HERE / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary["arms"], indent=1))
    print("stability:", stab)
    print(f"series with arm disagreement: {len(summary['disagreements'])}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--arms", nargs="*", default=list(ARMS), choices=ARMS)
    ap.add_argument("--repeats", type=int, default=3)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--log", default="calls.jsonl")
    ap.add_argument("--score-only", action="store_true")
    args = ap.parse_args(argv)
    if not args.score_only:
        run(args)
    score(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
