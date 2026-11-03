"""Deterministic review packet for one finished case (no LLM calls).

    python -m tools.case_review packet <case_dir> --out <dir> [--paper <paper.md>] [--metadata <csv>]
                                       [--spec <case_spec.json>] [--no-expr]

<case_dir> is one case folder of a run (the one holding decisions.json). The packet is what a
reviewer subagent reads after the analysis (see agent_skills/bioinformatics-workflow/references/
decision-review.md):

- packet_A.md: facts only, no decisions (metadata columns and levels, per-sample names, exercise
  words per column, candidate pairing keys, the paper's outline). The reviewer answers its blind
  questions from this and the paper before it opens packet B.
- packet_B.md: the analysis' decisions per gate, the samples in each group, and mechanical flags.
- flags.json: the same flags, machine-readable.

Flags are prompts for the reviewer, not verdicts. The checks come from errors seen in the large
runs: a stated rule whose counts are far from the paper while another rule matches; a
subject-like column or a pairing key the model does not use; a reversed contrast; p-values piled
up near 1; a "the data have no X" stop reason that a wider search contradicts.
"""

from __future__ import annotations

import argparse
import itertools
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

from tools.suitability import REFERENCE_WORDS, SUBJECT_COLUMN

EXERCISE_WORDS = re.compile(
    r"exercis|train(ed|ing)?\b|running|runners?\b|treadmill|wheel|swim|cycling|sprint|endurance|resistance|"
    r"aerobic|hiit|interval|sedentar|\bsed\b|athlet|\bbouts?\b|physical(ly)? (activ|inactiv)|detrain|unload|"
    r"immobili|bed ?rest|hindlimb|disuse|overload|contraction|electrical stimulation|(^|[_\-\s])(ex|exe|exp|run)"
    r"([_\-\s\d]|$)", re.I)
STOP_CLAIMS = {
    "pairing": re.compile(r"no (animal|subject|donor|participant|pair\w*|mouse|rat|individual)[- ]?(id|key|label)?|"
                          r"cannot be (paired|verified)|not (be )?paired|unknown pairing|pairing (is )?unknown|"
                          r"no (repeated|within)", re.I),
    "exercise_arm": re.compile(r"no exercise|not (an? )?exercise|no (training|trained|exercised)|sedentary only|"
                               r"exercise .* not sequenced|never sequenced", re.I),
    "raw_counts": re.compile(r"no raw count|normali[sz]ed only|only (fpkm|tpm|rpkm|normali)|counts? (are )?not "
                             r"(deposited|available)", re.I),
    "sample_size": re.compile(r"n ?= ?[12]\b|fewer than 3|too few|n < ?3", re.I),
}
SPLIT = re.compile(r"[_\-\s.:/|,;()]+")
RULES = [("padj", 0.05, None), ("padj", 0.05, 0.5849625), ("padj", 0.05, 1.0), ("padj", 0.1, None),
         ("pvalue", 0.05, None), ("pvalue", 0.05, 0.5849625), ("pvalue", 0.05, 1.0), ("pvalue", 0.01, None)]


def _path(p) -> Path | None:
    """Paths in records use the writer's separators and may be relative to the repository root."""
    if not p:
        return None
    return Path(str(p).replace("\\", "/"))


def _short(obj, n: int = 1200) -> str:
    s = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False, default=str)
    return s if len(s) <= n else s[:n] + f" ... [{len(s) - n} more characters]"


def load_records(case_dir: Path) -> list[dict]:
    return json.loads((case_dir / "decisions.json").read_text(encoding="utf-8"))


def _by_stage(records: list[dict]) -> dict:
    out: dict = {}
    for r in records:
        out.setdefault(r["stage"], []).append(r)
    return out


def load_metadata(case_dir: Path, metadata: str | None = None) -> tuple[pd.DataFrame | None, pd.DataFrame | None]:
    """(full GEO metadata, design metadata with derived columns), whichever exist."""
    full = design = None
    if metadata:
        full = pd.read_csv(metadata, index_col=0, dtype=str)
    elif (case_dir / "aligned" / "aligned_metadata.csv").exists():
        full = pd.read_csv(case_dir / "aligned" / "aligned_metadata.csv", index_col=0, dtype=str)
    if (case_dir / "aligned" / "design_metadata.csv").exists():
        design = pd.read_csv(case_dir / "aligned" / "design_metadata.csv", index_col=0, dtype=str)
    if full is not None and design is not None:
        extra = [c for c in design.columns if c not in full.columns]
        full = full.join(design[extra], how="left")
    return (full if full is not None else design), design


# ---------------------------------------------------------------------------
# Facts (packet A)
# ---------------------------------------------------------------------------

def metadata_facts(meta: pd.DataFrame, max_levels: int = 24) -> dict:
    n = len(meta)
    grouping, per_sample, constant, other = {}, [], {}, []
    for c in meta.columns:
        vals = meta[c].fillna("").astype(str)
        k = vals.nunique()
        if k <= 1:
            constant[c] = _short(vals.iloc[0] if n else "", 300)
        elif k >= max(n * 0.9, 2) and k == n:
            per_sample.append(c)
        elif k <= max_levels:
            grouping[c] = vals.value_counts().to_dict()
        else:
            other.append(c)
    return {"n_samples": n, "grouping_columns": grouping, "per_sample_columns": per_sample,
            "constant_columns": constant, "other_columns": other}


def exercise_hits(meta: pd.DataFrame) -> dict:
    hits = {}
    for c in meta.columns:
        vals = sorted({str(v) for v in meta[c].dropna() if EXERCISE_WORDS.search(str(v))})
        if vals:
            hits[c] = vals[:12]
    return hits


def _strip_levels(value: str, drop: set[str]) -> str:
    toks = [t for t in SPLIT.split(str(value)) if t and t.lower() not in drop]
    return "_".join(toks)


def _suffix(value: str) -> str | None:
    m = re.search(r"(?:^|[_\-\s.])([A-Za-z]|\d{1,3}|rep\d{1,3}|[A-Za-z]\d{1,2})$", str(value).strip())
    return m.group(1) if m else None


def _key_stats(keys: pd.Series, across: pd.Series) -> dict:
    df = pd.DataFrame({"key": keys, "across": across}).dropna()
    df = df[df["key"].astype(str) != ""]
    levels = sorted(df["across"].unique())
    cells = df.groupby(["key", "across"]).size()
    dup_keys = sorted({k for (k, _), n in cells.items() if n > 1})
    per_key = df.groupby("key")["across"].nunique()
    linked = per_key[(per_key >= 2) & ~per_key.index.isin(dup_keys)]
    complete = per_key[(per_key == len(levels)) & ~per_key.index.isin(dup_keys)]
    n_linked_samples = int(df["key"].isin(linked.index).sum())
    return {"levels": [str(x) for x in levels], "n_keys": int(per_key.size), "keys_with_duplicates_in_a_level":
            len(dup_keys), "keys_in_every_level_once": int(complete.size), "keys_in_2plus_levels_once":
            int(linked.size), "samples_linked": n_linked_samples, "n_samples": int(len(df)),
            "example_keys": [str(k) for k in list(complete.index[:4]) or list(linked.index[:4])]}


def pairing_search(meta: pd.DataFrame, max_across_levels: int = 4) -> list[dict]:
    """Candidate keys that would put the samples of one animal/person together across a factor.

    For each `across` column (2..max_across_levels levels, such as tissue or time), try:
    a per-sample name with the across level removed (SAT_AM_Cont_a -> AM_Cont_a); the trailing
    replicate token of a per-sample name, alone and combined with each grouping column (the
    grouping value also has the across level removed); and existing repeated columns. A key that
    is right appears at most once per across level and links most samples.
    """
    n = len(meta)
    facts = metadata_facts(meta)
    grouping = {c: v for c, v in facts["grouping_columns"].items()}
    per_sample = list(facts["per_sample_columns"])
    out = []
    across_cols = [c for c, lv in grouping.items() if 2 <= len(lv) <= max_across_levels and min(lv.values()) >= 2]
    for across in across_cols:
        acr = meta[across].fillna("").astype(str)
        drop = {t.lower() for v in acr.unique() for t in [v, *SPLIT.split(v)] if t}
        cands: dict[str, pd.Series] = {}
        for c in per_sample:
            stripped = meta[c].fillna("").astype(str).map(lambda v: _strip_levels(v, drop))
            if stripped.nunique() < n:
                cands[f"{c} without the {across} level"] = stripped
            suf = meta[c].fillna("").astype(str).map(_suffix)
            if suf.notna().mean() >= 0.8 and suf.nunique() >= 2:
                cands[f"suffix of {c}"] = suf
                for g in grouping:
                    if g == across:
                        continue
                    gv = meta[g].fillna("").astype(str).map(lambda v: _strip_levels(v, drop))
                    if gv.nunique() >= 2 and not (gv == acr).all():
                        cands[f"{g} (without {across}) + suffix of {c}"] = gv + "|" + suf.fillna("")
        for g, lv in grouping.items():
            if g != across and len(lv) > max_across_levels and max(lv.values()) <= 2 * len(acr.unique()):
                cands[g] = meta[g].fillna("").astype(str)
        for name, keys in cands.items():
            st = _key_stats(keys, acr)
            st.update({"key": name, "across": across})
            out.append(st)
    out = [c for c in out if c["n_keys"] > 1]
    out.sort(key=lambda c: (c["keys_with_duplicates_in_a_level"] == 0, c["samples_linked"]), reverse=True)
    return out


def paper_outline(paper: Path | None, limit: int = 80) -> list[str]:
    if not paper or not paper.exists():
        return []
    heads = [ln.strip() for ln in paper.read_text(encoding="utf-8", errors="replace").splitlines()
             if ln.startswith("#")]
    return heads[:limit]


# ---------------------------------------------------------------------------
# Decisions and flags (packet B)
# ---------------------------------------------------------------------------

def used_columns(by: dict) -> set[str]:
    used: set[str] = set()
    for r in by.get("covariance", []):
        f = r.get("final") or {}
        used |= set(f.get("blocking_terms") or [])
        used |= {c.get("name") for c in f.get("covariates") or [] if isinstance(c, dict)}
    for r in by.get("design", []) + by.get("execution", []) + by.get("method", []):
        f = r.get("final") or {}
        for key in ("formula", "design_formula"):
            if isinstance(f.get(key), str):
                used |= set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", f[key]))
        if f.get("design_column"):
            used.add(f["design_column"])
    return {u for u in used if u}


def _design_factors(by: dict) -> list[str]:
    for r in by.get("covariance", []):
        lv = ((r.get("final") or {}).get("design_check") or {}).get("levels")
        if lv:
            return list(lv)
    for r in by.get("design", []):
        f = r.get("final") or {}
        if f.get("design_column"):
            return [f["design_column"]]
    return []


def flag_unused_subject(design: pd.DataFrame | None, full: pd.DataFrame | None, used: set[str]) -> list[dict]:
    flags = []
    meta = design if design is not None else full
    if meta is None:
        return flags
    n = len(meta)
    for c in meta.columns:
        if c in used:
            continue
        vals = meta[c].dropna().astype(str)
        k = vals.nunique()
        counts = vals.value_counts()
        named = bool(SUBJECT_COLUMN.search(c))
        repeated = 2 <= k <= n / 2 and counts.min() >= 2 and counts.max() <= 6 and k >= 3
        if named and k < n or repeated and (named or k >= n / 4):
            flags.append({"flag": "unused_subject_like_column", "column": c, "n_values": int(k),
                          "max_repeat": int(counts.max()),
                          "note": "repeated per-sample key not in the model; check whether it is the animal/person"})
    return flags


def flag_numeric_blocking(design: pd.DataFrame | None, used: set[str], by: dict) -> list[dict]:
    if design is None:
        return []
    blocking = set()
    for r in by.get("covariance", []):
        blocking |= set((r.get("final") or {}).get("blocking_terms") or [])
    return [{"flag": "numeric_blocking_ids", "column": c,
             "note": "blocking IDs are all numbers; confirm the executor treated them as categories"}
            for c in blocking if c in design.columns and design[c].dropna().astype(str).str.fullmatch(r"\d+").all()]


def flag_direction(by: dict) -> list[dict]:
    flags = []
    for r in by.get("design", []):
        for c in (r.get("final") or {}).get("contrasts") or []:
            if not isinstance(c, dict):
                continue
            ctrl, trt = str(c.get("control", "")), str(c.get("treatment", ""))
            if (REFERENCE_WORDS.search(trt) and not REFERENCE_WORDS.search(ctrl)) or \
               (EXERCISE_WORDS.search(ctrl) and not EXERCISE_WORDS.search(trt)):
                flags.append({"flag": "possible_reversed_contrast", "contrast": c.get("name"), "control": ctrl,
                              "treatment": trt, "note": "the control side reads as exercise or the test side as control"})
    return flags


def _table_files(by: dict) -> dict:
    files = {}
    for r in by.get("execution", []):
        f = r.get("final") or {}
        outs = [_path(o) for o in f.get("outputs") or []]
        for table in (f.get("counts") or {}):
            if len(outs) == 1:
                files[table] = outs[0]
            else:
                tail = table.split("/")[-1]
                hit = [o for o in outs if tail in o.name]
                if hit:
                    files[table] = hit[0]
    return files


def _count(df: pd.DataFrame, metric: str, cutoff: float, lfc: float | None) -> int | None:
    if metric not in df.columns:
        return None
    m = pd.to_numeric(df[metric], errors="coerce") < cutoff
    if lfc is not None:
        if "log2FoldChange" not in df.columns:
            return None
        m &= pd.to_numeric(df["log2FoldChange"], errors="coerce").abs() > lfc
    return int(m.sum())


def threshold_check(by: dict, root: Path) -> tuple[list[dict], list[dict]]:
    """Counts of each result table with a paper count under several rules, and flags."""
    paper_counts = {}
    applied_counts = {}
    for r in by.get("study", []):
        f = r.get("final") or {}
        paper_counts.update({k: v for k, v in (f.get("paper_counts") or {}).items() if isinstance(v, (int, float))})
        for k, v in (f.get("results") or {}).items():
            if isinstance(v, dict) and "n_deg" in v:
                applied_counts[k] = (v["n_deg"], v.get("rule"))
    rows, flags = [], []
    files = _table_files(by)
    for table, paper_n in paper_counts.items():
        path = files.get(table)
        row = {"table": table, "paper": paper_n, "applied": applied_counts.get(table, (None, None))[0],
               "applied_rule": applied_counts.get(table, (None, None))[1], "file": str(path) if path else None}
        df = None
        if path is not None:
            p = path if path.is_absolute() else root / path
            if p.exists():
                df = pd.read_csv(p, index_col=0)
        if df is not None:
            for metric, cut, lfc in RULES:
                row[f"{metric}<{cut}" + (f" & |lfc|>{lfc:g}" if lfc else "")] = _count(df, metric, cut, lfc)
            if "pvalue" in df.columns:
                p = pd.to_numeric(df["pvalue"], errors="coerce").dropna()
                row["frac_p_gt_0.9"] = round(float((p > 0.9).mean()), 3) if len(p) else None
                row["frac_p_lt_0.05"] = round(float((p < 0.05).mean()), 3) if len(p) else None
                if len(p) and (p > 0.9).mean() > 0.2 and (p < 0.05).mean() < 0.05:
                    flags.append({"flag": "pvalues_piled_near_1", "table": table,
                                  "frac_p_gt_0.9": row["frac_p_gt_0.9"],
                                  "note": "p-value histogram piled up near 1: normalization or model may be wrong"})
        rows.append(row)
        applied = row["applied"]
        alts = {k: v for k, v in row.items() if ("<" in k and isinstance(v, int))}
        if paper_n and applied is not None and alts:
            def err(x):
                return abs(np.log((x + 1) / (paper_n + 1)))
            best_rule, best_n = min(alts.items(), key=lambda kv: err(kv[1]))
            if err(applied) > np.log(1.5) and err(best_n) < np.log(1.15) and err(best_n) < err(applied) / 3:
                flags.append({"flag": "other_rule_matches_paper", "table": table, "paper": paper_n,
                              "applied": applied, "applied_rule": row["applied_rule"], "closest_rule": best_rule,
                              "closest_n": best_n,
                              "note": "the paper's numbers fit another rule; check the paper's stated rule and "
                                      "whether the discrepancy is recorded"})
    return rows, flags


def stop_claims(records: list[dict]) -> list[dict]:
    out = []
    for r in records:
        reason = r.get("stop_reason") or ""
        if r.get("decision_status") in ("refused", "manual_review", "unresolved") or reason:
            kinds = [k for k, rx in STOP_CLAIMS.items() if rx.search(reason)]
            out.append({"stage": r["stage"], "status": r.get("decision_status"), "kinds": kinds,
                        "stop_reason": reason})
    return out


def suitability_lines(case_dir: Path) -> list[str]:
    p = case_dir / "suitability" / "suitability.md"
    if not p.exists():
        return []
    keep = re.compile(r"sex|confound|warn|fail|between|check|not_analyzable|partial|mismatch", re.I)
    return [ln.strip() for ln in p.read_text(encoding="utf-8", errors="replace").splitlines()
            if keep.search(ln)][:40]


def group_samples(meta: pd.DataFrame | None, factors: list[str], show: list[str]) -> dict:
    if meta is None:
        return {}
    out = {}
    for f in factors:
        if f not in meta.columns:
            continue
        out[f] = {}
        for lv, idx in meta.groupby(meta[f].fillna("NA").astype(str)).groups.items():
            out[f][lv] = [" / ".join([str(s)] + [str(meta.at[s, c])[:40] for c in show if c in meta.columns])
                          for s in idx]
    return out


def pairing_expression_check(case_dir: Path, meta: pd.DataFrame, cand: dict) -> dict | None:
    """Residual-correlation support for the best pairing candidate (tools.pairing_check)."""
    mpath = case_dir / "aligned" / "aligned_matrix.csv"
    if not mpath.exists():
        return None
    try:
        from tools.pairing_check import check_pairing_key
        mat = pd.read_csv(mpath, index_col=0)
        mat = mat.apply(pd.to_numeric, errors="coerce").dropna(how="all")
        cols = [c for c in meta.index if c in mat.columns]
        if len(cols) < 4:
            return None
        mat = mat[cols].fillna(0)
        if float(np.nanmax(mat.values)) > 50:          # counts-like: log2 CPM
            mat = np.log2(mat / mat.sum() * 1e6 + 1)
        m = meta.loc[cols].copy()
        m["_cand_key"] = cand["_keys"].loc[cols]
        m["_across"] = cand["_across"].loc[cols]
        within = []
        if "+" in cand["key"]:
            m["_within"] = m["_cand_key"].str.split("|").str[0]
            within = ["_within"]
        res = check_pairing_key(mat, m, ["_cand_key"], "_across", within, n_perm=2000)
        res["key"] = cand["key"]
        return res
    except Exception as exc:                            # informative only; never blocks the packet
        return {"status": "error", "error": f"{type(exc).__name__}: {exc}"}


def build(case_dir: Path, out: Path, *, paper: str | None = None, metadata: str | None = None,
          spec: str | None = None, root: Path | None = None, expr: bool = True) -> dict:
    root = root or Path.cwd()
    records = load_records(case_dir)
    by = _by_stage(records)
    full, design = load_metadata(case_dir, metadata)
    paper_path = _path(paper)
    if paper_path is None and spec:
        s = json.loads(Path(spec).read_text(encoding="utf-8"))
        for c in s.get("cases", []):
            if (c.get("case_id") or "") == case_dir.name and (c.get("inputs") or {}).get("paper"):
                paper_path = _path(c["inputs"]["paper"][0])
    out.mkdir(parents=True, exist_ok=True)

    # ---- facts
    facts = metadata_facts(full) if full is not None else {}
    hits = exercise_hits(full) if full is not None else {}
    pairs = pairing_search(full) if full is not None else []
    show = [c for c in (facts.get("per_sample_columns") or []) if c.lower() in ("title", "description")][:2] \
        or (facts.get("per_sample_columns") or [])[:2]

    flags: list[dict] = []
    used = used_columns(by)
    flags += flag_unused_subject(design, full, used)
    flags += flag_numeric_blocking(design, used, by)
    flags += flag_direction(by)
    thr_rows, thr_flags = threshold_check(by, root)
    flags += thr_flags
    claims = stop_claims(records)
    good_pairs = [p for p in pairs if p["keys_with_duplicates_in_a_level"] == 0 and
                  p["samples_linked"] >= 0.5 * p["n_samples"] and p["keys_in_2plus_levels_once"] >= 3]
    pairing_used = bool(used & {"subject", "animal", "donor", "pair", "rat", "mouse", "patient", "id"}) or any(
        (r.get("final") or {}).get("blocking_terms") for r in by.get("covariance", []))
    expr_check = None
    if good_pairs and (not pairing_used or any("pairing" in c["kinds"] for c in claims)):
        best = good_pairs[0]
        flags.append({"flag": "pairing_key_candidate", "key": best["key"], "across": best["across"],
                      "pairs_or_sets": best["keys_in_2plus_levels_once"], "samples_linked": best["samples_linked"],
                      "note": "a label combination links samples across this factor once each; check the paper "
                              "for repeated samples per animal/person"})
        if expr and full is not None:
            acr = full[best["across"]].fillna("").astype(str)
            drop = {t.lower() for v in acr.unique() for t in [v, *SPLIT.split(v)] if t}
            keys = _rebuild_key(full, best["key"], drop)
            if keys is not None:
                expr_check = pairing_expression_check(case_dir, full, {"key": best["key"], "_keys": keys,
                                                                       "_across": acr})
    for c in claims:
        if "exercise_arm" in c["kinds"] and hits:
            flags.append({"flag": "refusal_vs_exercise_words", "stage": c["stage"],
                          "columns": {k: v[:5] for k, v in hits.items()},
                          "note": "the stop reason says no exercise arm, yet these values carry exercise words"})
        if "pairing" in c["kinds"] and good_pairs:
            flags.append({"flag": "stop_reason_vs_pairing_search", "stage": c["stage"],
                          "note": "the stop reason says pairing is unknown; the search found candidate keys"})

    # ---- packet A
    a = [f"# Review packet A (facts only): {case_dir.name}", "",
         "Answer the blind questions from this file and the paper before opening packet B.", ""]
    a += [f"Paper: `{paper_path}`" if paper_path else "Paper: not found (use the abstract or GEO description)."]
    outline = paper_outline(paper_path if paper_path and paper_path.is_absolute() else
                            (root / paper_path if paper_path else None))
    if outline:
        a += ["", "## Paper outline", ""] + [f"- {h}" for h in outline]
    if facts:
        a += ["", f"## Metadata ({facts['n_samples']} samples)", "", "### Grouping columns (level: count)", ""]
        for c, lv in facts["grouping_columns"].items():
            a.append(f"- `{c}`: " + "; ".join(f"{k}: {v}" for k, v in list(lv.items())[:24]))
        a += ["", "### Constant columns", ""] + [f"- `{c}`: {v}" for c, v in facts["constant_columns"].items()]
        a += ["", "### Per-sample columns", "", ", ".join(f"`{c}`" for c in facts["per_sample_columns"]),
              "", "### Samples", "", "| sample | " + " | ".join(show) + " |", "|---|" + "---|" * len(show)]
        for s in full.index[:120]:
            a.append(f"| {s} | " + " | ".join(str(full.at[s, c])[:60] for c in show) + " |")
    a += ["", "## Values with exercise words (by column)", ""]
    a += [f"- `{c}`: {', '.join(v)}" for c, v in hits.items()] or ["- none found"]
    a += ["", "## Candidate pairing keys", "",
          "A key that marks one animal/person appears at most once in each level of the `across` factor. "
          "`keys_with_duplicates_in_a_level` > 0 means the key cannot be the animal on its own.", "",
          "| key | across | keys | linked samples / all | keys in every level once | duplicates in a level |",
          "|---|---|---|---|---|---|"]
    for p in pairs[:8]:
        a.append(f"| {p['key']} | {p['across']} | {p['n_keys']} | {p['samples_linked']}/{p['n_samples']} | "
                 f"{p['keys_in_every_level_once']} | {p['keys_with_duplicates_in_a_level']} |")
    if not pairs:
        a.append("| none | | | | | |")
    if expr_check:
        a += ["", "Expression check of the best candidate (residual correlation of same-key pairs, "
              "tools/pairing_check.py): " + _short(expr_check, 600)]

    # ---- packet B
    b = [f"# Review packet B (the analysis' decisions): {case_dir.name}", ""]
    b += ["## Mechanical flags", ""]
    b += [f"- **{f['flag']}**: " + _short({k: v for k, v in f.items() if k != 'flag'}, 500) for f in flags] \
        or ["- none"]
    if claims:
        b += ["", "## Stop reasons", ""] + [f"- {c['stage']} ({c['status']}; claim type: "
                                            f"{', '.join(c['kinds']) or 'other'}): {c['stop_reason']}" for c in claims]
    if thr_rows:
        b += ["", "## DEG counts under other rules vs the paper", ""]
        keys = [k for k in thr_rows[0] if k not in ("file",)]
        b += ["| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
        for r in thr_rows:
            b.append("| " + " | ".join(str(r.get(k, "")) for k in keys) + " |")
    factors = _design_factors(by)
    groups = group_samples(design if design is not None else full, factors, show)
    if groups:
        b += ["", "## Samples per design level", ""]
        for f, lv in groups.items():
            b.append(f"### `{f}`")
            for level, samples in lv.items():
                b.append(f"- **{level}** ({len(samples)}): " + "; ".join(samples[:40]))
            b.append("")
    b += ["## Gates", ""]
    for r in records:
        b += [f"### {r['stage']} ({r.get('decision_status')}, {r.get('execution_status')})", "",
              "final: " + _short(r.get("final"), 1500), ""]
        if r.get("reasoning"):
            b += ["reasoning: " + _short(r["reasoning"], 700), ""]
        if r.get("candidates"):
            b += ["rejected alternatives: " + _short(r["candidates"], 500), ""]
    sl = suitability_lines(case_dir)
    if sl:
        b += ["## Suitability report lines (sex, confounding, warnings)", ""] + [f"- {x}" for x in sl]
    disc = case_dir / "paper_data_discrepancies.json"
    if disc.exists():
        b += ["", "## Recorded paper-data discrepancies", "", _short(disc.read_text(encoding="utf-8"), 1500)]
    handback = case_dir.parent / "HANDBACK.md"
    if handback.exists():
        b += ["", "## HANDBACK.md (start)", "", _short(handback.read_text(encoding="utf-8", errors="replace"), 2500)]

    (out / "packet_A.md").write_text("\n".join(a) + "\n", encoding="utf-8")
    (out / "packet_B.md").write_text("\n".join(b) + "\n", encoding="utf-8")
    summary = {"case_dir": str(case_dir), "paper": str(paper_path) if paper_path else None,
               "flags": flags, "stop_claims": claims, "pairing_candidates": pairs[:8],
               "pairing_expression_check": expr_check, "threshold_table": thr_rows,
               "packet_A": str(out / "packet_A.md"), "packet_B": str(out / "packet_B.md")}
    (out / "flags.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1, default=str),
                                    encoding="utf-8")
    return summary


def _rebuild_key(meta: pd.DataFrame, name: str, drop: set[str]) -> pd.Series | None:
    m = re.fullmatch(r"(.+) \(without .+\) \+ suffix of (.+)", name)
    if m:
        g, c = m.groups()
        return meta[g].fillna("").astype(str).map(lambda v: _strip_levels(v, drop)) + "|" + \
            meta[c].fillna("").astype(str).map(_suffix).fillna("")
    m = re.fullmatch(r"(.+) without the .+ level", name)
    if m:
        return meta[m.group(1)].fillna("").astype(str).map(lambda v: _strip_levels(v, drop))
    m = re.fullmatch(r"suffix of (.+)", name)
    if m:
        return meta[m.group(1)].fillna("").astype(str).map(_suffix)
    return meta[name].fillna("").astype(str) if name in meta.columns else None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("packet", help="write packet_A.md, packet_B.md and flags.json for one case")
    p.add_argument("case_dir")
    p.add_argument("--out", required=True)
    p.add_argument("--paper")
    p.add_argument("--metadata")
    p.add_argument("--spec")
    p.add_argument("--no-expr", action="store_true", help="skip the expression check of the pairing key")
    args = ap.parse_args(argv)
    s = build(Path(args.case_dir), Path(args.out), paper=args.paper, metadata=args.metadata, spec=args.spec,
              expr=not args.no_expr)
    print(json.dumps({"flags": [f["flag"] for f in s["flags"]], "stop_claims": [c["kinds"] for c in s["stop_claims"]],
                      "packet_A": s["packet_A"], "packet_B": s["packet_B"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
