"""Score model runs against the Opus reference runs (no LLM).

    python test/experiments/model_compare_20261103/score.py sonnet [haiku ...]

Writes scores.csv (one row per reference comparison) and scores.md. Comparisons are
matched by their GSM sets, not their names, so label choices do not count as differences.
Transcript paths come from transcripts.csv (model,paper_id,path).
"""
import csv
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
MC = HERE.parents[2]
sys.path.insert(0, str(MC))
from tools import decision_contract  # noqa: E402

REF = Path("E:/agent/mwangLab_pdf/test/experiments/large_run_pilot_20261019/runs_claude")
PAPERS = [("PMID41835150", "GSE319603", "run"), ("PMID39393048", "GSE267512", "run"),
          ("b06f79d81bb9463e3b902b4b8b96b865e96758a2", "GSE164890", "run"),
          ("PMID34142717", "GSE178262", "run"), ("PMID34358431", "GSE174785", "refuse"),
          ("PMID42679010", "GSE344550", "refuse")]


def load(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def final(gates, name):
    return (gates.get(name) or {}).get("final") or {}


def comparisons(run):
    """Every result in a run with its GSM sets and the decisions behind it."""
    spec = load(run / "case_spec.json")
    if spec is None:
        return from_decisions(run)
    out = []
    for case in spec.get("cases", []):
        cdir = run / case["case_id"]
        repro = load(cdir / "reproduction_summary.json") or {}
        meta = None
        for name in ("design_metadata.csv", "aligned_metadata.csv"):
            if (cdir / "aligned" / name).exists():
                meta = pd.read_csv(cdir / "aligned" / name, index_col=0, dtype=str)
                break
        gates = case.get("gates", {})
        design = gates.get("design") or {}
        method = final(gates, "method")
        cov = final(gates, "covariance")
        thr = final(gates, "threshold")
        execs = {e.get("name"): e for e in case.get("executions") or []}
        planned = set(design.get("planned") or [])
        planned |= {c.get("name") for c in final(gates, "design").get("contrasts") or []}
        for key, res in (repro.get("results") or {}).items():
            ename, _, cname = key.partition("/")
            ex = execs.get(ename, {})
            args = ex.get("args") or {}
            ctrl, trt = gsm_sets(meta, cname, args, ex.get("subset"))
            out.append({
                "case": case["case_id"], "key": key, "role": ex.get("role", ""),
                "planned": (cname or ename) in planned or not cname, "ctrl": ctrl, "trt": trt,
                "method": method.get("method", ""), "formula": method.get("formula", ""),
                "covariance": cov.get("status", ""), "blocking": cov.get("blocking_terms") or [],
                "threshold": thr.get("applied_threshold") or {},
                "rule": res.get("rule", ""), "n_deg": res.get("n_deg"), "up": res.get("up"),
                "down": res.get("down"),
                "paper": ((repro.get("comparison") or {}).get(key) or {}).get("paper"),
            })
    return out


def from_decisions(run):
    """A run that bypassed case_runner: read decisions.json and summary.csv instead."""
    out = []
    for path in sorted(run.glob("*/decisions.json")):
        cdir = path.parent
        recs = {r.get("stage"): r.get("final") or {} for r in load(path) or []}
        design, cov = recs.get("design", {}), recs.get("covariance", {})
        method, thr = recs.get("method", {}), recs.get("threshold", {})
        if not design.get("design_column"):
            continue
        meta = pd.read_csv(cdir / "aligned" / "design_metadata.csv", index_col=0, dtype=str)
        args = {"design_column": design["design_column"], "control_group": design.get("control"),
                "treatment_group": design.get("treatment")}
        ctrl, trt = gsm_sets(meta, "", args, None)
        rows = {r["case_id"]: r for r in csv.DictReader(open(run / "summary.csv", encoding="utf-8"))}
        out.append({"case": cdir.name, "key": f"{design['treatment']}_vs_{design['control']}", "role": "primary",
                    "planned": True, "ctrl": ctrl, "trt": trt, "method": method.get("method", ""),
                    "formula": method.get("formula", ""), "covariance": cov.get("status", ""),
                    "blocking": cov.get("blocking_terms") or [], "threshold": thr.get("applied_threshold") or {},
                    "rule": "", "n_deg": rows.get(cdir.name, {}).get("n_deg"), "up": None, "down": None, "paper": None})
    return out


def gsm_sets(meta, cname, args, subset):
    if meta is None:
        return None, None
    df = meta
    for col, vals in (subset or {}).items():
        if col in df:
            df = df[df[col].isin(vals if isinstance(vals, list) else [vals])]
    col = args.get("design_column")
    a, b = args.get("treatment_group"), args.get("control_group")
    if cname:
        for factor in sorted(df.columns, key=len, reverse=True):
            m = re.match(rf"^{re.escape(factor)}_(.+?)_vs_(.+?)((?:_[^_-]+-[^_]+)*)$", cname)
            if m:
                col, a, b = factor, m.group(1), m.group(2)
                for f, v in re.findall(r"_([^_-]+)-([^_]+)", m.group(3)):
                    if f in df:
                        df = df[df[f] == v]
                break
    if col not in df or a is None or b is None:
        return None, None
    return frozenset(df.index[df[col] == b]), frozenset(df.index[df[col] == a])


def jaccard(x, y):
    return len(x & y) / len(x | y) if x | y else 0.0


def best_match(ref, cands):
    best, tag, score = None, "missing", -1.0
    if not ref["ctrl"] or not ref["trt"]:
        return None, "reference groups unresolved"
    for c in cands:
        if not c["ctrl"] or not c["trt"]:
            continue
        same = (jaccard(ref["ctrl"], c["ctrl"]) + jaccard(ref["trt"], c["trt"])) / 2
        flip = (jaccard(ref["ctrl"], c["trt"]) + jaccard(ref["trt"], c["ctrl"])) / 2
        s = max(same, flip) + (0.001 if c["planned"] and c["role"] != "sensitivity" else 0)
        if s > score:
            best, score = c, s
            tag = ("exact" if same == 1 else "flipped" if flip == 1 else
                   f"partial(J={same:.2f})" if same >= flip else f"partial_flipped(J={flip:.2f})")
    return (best, tag) if score > 0.3 else (None, "missing")


def thr_key(t):
    metric = {"fdr": "padj"}.get(str(t.get("metric")).lower(), str(t.get("metric")).lower())
    return (metric, t.get("cutoff"), t.get("effect_cutoff") or 0)


def form(s):
    return re.sub(r"\s+", "", str(s).split("(")[0]).lower()


def run_state(run):
    path = run / "summary.csv"
    if not path.exists():
        return "no_summary", ""
    rows = list(csv.DictReader(open(path, encoding="utf-8")))
    states = sorted({r.get("decision_status", "") + "/" + r.get("execution_status", "") for r in rows})
    stops = sorted({r.get("stop_stage", "") for r in rows if r.get("stop_stage")})
    state = "refused" if rows and all(r.get("decision_status") == "refused" for r in rows) else "ran"
    return state, ";".join(states) + (" stop=" + ",".join(stops) if stops else "")


def validator(run):
    paths = sorted(run.glob("*/decisions.json"))
    if not paths:
        return "no decisions.json"
    n, errors = decision_contract.validate(paths)
    return f"{n} records, {len(errors)} errors" + (": " + errors[0][:160] if errors else "")


def tool_inputs(obj):
    if isinstance(obj, dict):
        if obj.get("type") == "tool_use":
            yield obj.get("name"), json.dumps(obj.get("input"), ensure_ascii=False)
        for v in obj.values():
            yield from tool_inputs(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from tool_inputs(v)


def forbidden(model, pid, transcripts):
    path = transcripts.get((model, pid))
    if not path or not os.path.exists(path):
        return "transcript not available"
    hits = []
    own = f"model_compare_20261103/runs/{model}/{pid}".lower()
    for line in open(path, encoding="utf-8", errors="replace"):
        try:
            rec = json.loads(line)
        except ValueError:
            continue
        for name, text in tool_inputs(rec):
            t = re.sub(r"\\+", "/", text).lower().replace(own, "")
            if re.search(r"large_run_pilot_20261019/runs_claude|experiments/case_runner_|model_compare_20261103", t):
                hits.append(f"{name}: {text[:140]}")
    return f"{len(hits)} hit(s)" + (" | " + " | ".join(hits[:3]) if hits else "")


def main(models):
    transcripts = {}
    if (HERE / "transcripts.csv").exists():
        for r in csv.DictReader(open(HERE / "transcripts.csv", encoding="utf-8")):
            transcripts[(r["model"], r["paper_id"])] = r["path"]
    rows, papers = [], []
    for model in models:
        for pid, gse, expected in PAPERS:
            run, ref = HERE / "runs" / model / pid, REF / pid
            state, detail = run_state(run)
            ref_state, _ = run_state(ref)
            papers.append({"model": model, "paper_id": pid, "gse": gse, "expected": expected, "state": state,
                           "opus_state": ref_state, "right": state == {"run": "ran", "refuse": "refused"}[expected],
                           "route": "case_spec" if (run / "case_spec.json").exists() else "custom_scripts",
                           "detail": detail, "validator": validator(run), "forbidden": forbidden(model, pid, transcripts)})
            got = comparisons(run)
            refs = comparisons(ref)
            refs = [c for c in refs if c["role"] != "sensitivity" and c["planned"]] or [c for c in refs if c["role"] != "sensitivity"]
            for r in refs:
                m, tag = best_match(r, got)
                row = {"model": model, "paper_id": pid, "gse": gse, "opus_key": r["key"], "match": tag,
                       "n_ctrl_opus": len(r["ctrl"] or []), "n_trt_opus": len(r["trt"] or []),
                       "opus_formula": r["formula"], "opus_method": r["method"], "opus_rule": r["rule"],
                       "opus_deg": r["n_deg"], "paper_deg": r["paper"]}
                if m:
                    row.update({"key": m["key"], "role": m["role"], "n_ctrl": len(m["ctrl"]), "n_trt": len(m["trt"]),
                                "formula": m["formula"], "formula_same": form(m["formula"]) == form(r["formula"]),
                                "method": m["method"], "covariance": m["covariance"], "opus_covariance": r["covariance"],
                                "blocking": ";".join(map(str, m["blocking"])), "opus_blocking": ";".join(map(str, r["blocking"])),
                                "rule": m["rule"], "threshold_same": thr_key(m["threshold"]) == thr_key(r["threshold"]),
                                "deg": m["n_deg"], "up": m["up"], "down": m["down"], "opus_up": r["up"], "opus_down": r["down"],
                                "paper_deg_own": m["paper"]})
                rows.append(row)
    fields = ["model", "paper_id", "gse", "opus_key", "match", "key", "role", "n_ctrl", "n_ctrl_opus", "n_trt", "n_trt_opus",
              "formula", "opus_formula", "formula_same", "method", "opus_method", "covariance", "opus_covariance", "blocking",
              "opus_blocking", "rule", "opus_rule", "threshold_same", "deg", "opus_deg", "paper_deg", "paper_deg_own", "up",
              "opus_up", "down", "opus_down"]
    with open(HERE / "scores.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fields)
        w.writeheader()
        w.writerows(rows)
    md = ["# Scores against the Opus reference", "", "Comparisons are the reference's planned non-sensitivity ones, matched by GSM sets.", "",
          "## Papers", "", "| model | paper | expected | state | Opus | right | route | validator | forbidden reads |", "|---|---|---|---|---|---|---|---|---|"]
    for p in papers:
        md.append(f"| {p['model']} | {p['paper_id'][:12]} ({p['gse']}) | {p['expected']} | {p['state']} | {p['opus_state']} | {p['right']} | {p['route']} | {p['validator']} | {p['forbidden'].split(' | ')[0]} |")
    md += ["", "## Comparisons", "", "| model | paper | Opus comparison | match | n ctrl/trt (Opus) | formula (Opus) | threshold same | DEGs | Opus | paper |", "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        md.append(f"| {r['model']} | {r['paper_id'][:12]} | {r['opus_key']} | {r['match']} | {r.get('n_ctrl', '-')}/{r.get('n_trt', '-')} ({r['n_ctrl_opus']}/{r['n_trt_opus']}) | {r.get('formula', '-')} ({r['opus_formula']}) | {r.get('threshold_same', '-')} | {r.get('deg', '-')} | {r['opus_deg']} | {r['paper_deg'] or '-'} |")
    hits = [p for p in papers if not p["forbidden"].startswith(("0 hit", "transcript"))]
    if hits:
        md += ["", "## Forbidden path hits", ""] + [f"- {p['model']} {p['paper_id']}: {p['forbidden']}" for p in hits]
    (HERE / "scores.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main(sys.argv[1:] or ["sonnet"])
