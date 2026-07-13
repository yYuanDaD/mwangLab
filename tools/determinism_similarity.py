"""Text-similarity helpers for SEA-CDM determinism audits.

The determinism scripts compare multiple LLM extractions of the same source text.
For descriptive fields, exact string equality is too strict: two outputs can differ
slightly in wording while still describing the same content. ROUGE-L F1 gives a
simple, dependency-free way to quantify that drift.
"""

import itertools
import re
from statistics import mean


_TOKEN_RE = re.compile(r"[A-Za-z0-9]+|[\u4e00-\u9fff]")


def tokenize_for_rouge(text) -> list[str]:
    """Tokenize English words/numbers and Chinese characters for ROUGE-L."""
    if text is None:
        return []
    return [m.group(0).lower() for m in _TOKEN_RE.finditer(str(text))]


def lcs_len(a: list[str], b: list[str]) -> int:
    """Return longest common subsequence length using O(min(n, m)) memory."""
    if len(a) < len(b):
        short, long = a, b
    else:
        short, long = b, a
    prev = [0] * (len(short) + 1)
    for tok_long in long:
        curr = [0]
        left_up = 0
        for j, tok_short in enumerate(short, 1):
            up = prev[j]
            left = curr[j - 1]
            curr.append(left_up + 1 if tok_long == tok_short else max(left, up))
            left_up = up
        prev = curr
    return prev[-1]


def rouge_l_f1(reference, candidate) -> float:
    """Compute ROUGE-L F1 between two strings."""
    ref = tokenize_for_rouge(reference)
    cand = tokenize_for_rouge(candidate)
    if not ref and not cand:
        return 1.0
    if not ref or not cand:
        return 0.0
    lcs = lcs_len(ref, cand)
    precision = lcs / len(cand)
    recall = lcs / len(ref)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def pairwise_rouge_l(values) -> dict:
    """Summarize pairwise ROUGE-L F1 for all run values of one field."""
    vals = ["" if v is None else str(v) for v in values]
    if len(vals) < 2:
        return {"mean": 1.0, "min": 1.0, "scores": []}
    scores = [rouge_l_f1(a, b) for a, b in itertools.combinations(vals, 2)]
    return {"mean": mean(scores), "min": min(scores), "scores": scores}


def summarize_rouge_l(field_items, threshold: float = 0.90) -> dict:
    """Summarize ROUGE-L over iterable `(table, row, field, values)` items."""
    scored = []
    for table, row, field, values in field_items:
        if not all(isinstance(v, str) or v is None for v in values):
            continue
        score = pairwise_rouge_l(values)
        scored.append({
            "table": table,
            "row": row,
            "field": field,
            "rouge_l_f1_mean": round(score["mean"], 4),
            "rouge_l_f1_min": round(score["min"], 4),
            "values": values,
        })
    if not scored:
        return {
            "fields_scored": 0,
            "mean_rouge_l_f1": None,
            "min_rouge_l_f1": None,
            "below_threshold": [],
        }
    return {
        "fields_scored": len(scored),
        "mean_rouge_l_f1": round(mean(x["rouge_l_f1_mean"] for x in scored), 4),
        "min_rouge_l_f1": min(x["rouge_l_f1_min"] for x in scored),
        "threshold": threshold,
        "below_threshold": [
            x for x in scored if x["rouge_l_f1_min"] < threshold
        ],
    }
