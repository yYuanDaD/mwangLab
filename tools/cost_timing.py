"""Per-stage wall-clock + LLM token/$ accounting for a cohort run.

User directive (2026-06-23): give EVERY pipeline stage a timer + a cost estimate, so each run
surfaces where time and money went instead of having to read the billing dashboard.

Design:
- Wall time is recorded for EVERY stage (free-CPU stages — DA / GSEA / #6 / #7 / #7b / split /
  download — show $0 but real seconds, which is what you actually want to see for those).
- LLM token cost is recorded only for stages that call the model (extraction — which now also
  carries the #5 findings via the one-pass merge — and the standalone #5 call). Tokens come from
  the existing `_UsageCapturingStructured` capture (with_structured_output(include_raw=True)).
- `$` is an ESTIMATE = input_tokens*$3/Mtok + output_tokens*$15/Mtok (Claude Sonnet 4.6 fixed
  rates), NOT a billing reconcile. Accurate to the model tier; if a cheaper model is ever used for
  some call, key the rate per call.

Known gap (documented, not hidden): LLM calls INSIDE run_batch_geo_pipeline (the gated contrast
validation, the opt-in da-method picker) are not token-captured here — the batch is timed as one
black-box stage. Those calls are gated/opt-in and individually ~$0.001-0.005, so the batch stage's
$ is wall-time only; its LLM spend is small and bounded. (Extraction + #5 are ~90% of the LLM $.)
"""

import csv
import os
import time

# Claude Sonnet 4.6 list price, USD per token.
SONNET_IN_PER_TOK = 3.0 / 1_000_000
SONNET_OUT_PER_TOK = 15.0 / 1_000_000


def usd_for(in_tok: int, out_tok: int) -> float:
    """USD estimate for a number of input/output tokens at Sonnet 4.6 rates."""
    return (in_tok or 0) * SONNET_IN_PER_TOK + (out_tok or 0) * SONNET_OUT_PER_TOK


class RunProfiler:
    """Accumulates {stage -> wall_s, n_llm_calls, input_tokens, output_tokens}. Stage names repeat
    across a per-paper loop (each call accumulates into the same slot). Free-CPU stages have 0
    tokens → $0 but still carry wall time."""

    def __init__(self):
        self._stages = {}
        self._order = []

    def _slot(self, name: str) -> dict:
        if name not in self._stages:
            self._stages[name] = {"wall_s": 0.0, "n_llm": 0, "in_tok": 0, "out_tok": 0}
            self._order.append(name)
        return self._stages[name]

    def stage(self, name: str):
        """Context manager that adds the elapsed wall time to `name` (accumulates)."""
        return _StageTimer(self, name)

    def add_time(self, name: str, seconds: float) -> None:
        self._slot(name)["wall_s"] += float(seconds)

    def add_llm_usage(self, name: str, usage_list) -> None:
        """Fold a list of {input_tokens, output_tokens} (from _UsageCapturingStructured) into a
        stage. Each entry counts as one LLM call."""
        s = self._slot(name)
        for u in usage_list or []:
            s["n_llm"] += 1
            s["in_tok"] += int(u.get("input_tokens") or 0)
            s["out_tok"] += int(u.get("output_tokens") or 0)

    # ---- aggregates ----
    def total_wall(self) -> float:
        return sum(s["wall_s"] for s in self._stages.values())

    def total_in(self) -> int:
        return sum(s["in_tok"] for s in self._stages.values())

    def total_out(self) -> int:
        return sum(s["out_tok"] for s in self._stages.values())

    def total_llm(self) -> int:
        return sum(s["n_llm"] for s in self._stages.values())

    def total_usd(self) -> float:
        return usd_for(self.total_in(), self.total_out())

    # ---- output ----
    def rows(self):
        for name in self._order:
            s = self._stages[name]
            yield (name, round(s["wall_s"], 2), s["n_llm"], s["in_tok"], s["out_tok"],
                   round(usd_for(s["in_tok"], s["out_tok"]), 4))

    def write_csv(self, path: str) -> str:
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["stage", "wall_s", "n_llm_calls", "input_tokens", "output_tokens", "usd_est"])
            for r in self.rows():
                w.writerow(r)
            w.writerow(["TOTAL", round(self.total_wall(), 2), self.total_llm(),
                        self.total_in(), self.total_out(), round(self.total_usd(), 4)])
        return path

    def summary_lines(self):
        """Pretty per-stage table for the run log / report."""
        out = [f"  {'stage':22s} {'wall_s':>8s} {'llm':>4s} {'in_tok':>8s} {'out_tok':>8s} {'$est':>8s}"]
        for name, wall, n, it, ot, usd in self.rows():
            out.append(f"  {name:22s} {wall:8.1f} {n:4d} {it:8d} {ot:8d} {usd:8.4f}")
        out.append(f"  {'TOTAL':22s} {self.total_wall():8.1f} {self.total_llm():4d} "
                   f"{self.total_in():8d} {self.total_out():8d} {self.total_usd():8.4f}")
        return out


class _StageTimer:
    def __init__(self, prof: RunProfiler, name: str):
        self.prof, self.name, self.t0 = prof, name, None

    def __enter__(self):
        self.t0 = time.perf_counter()
        return self

    def __exit__(self, *exc):
        self.prof.add_time(self.name, time.perf_counter() - self.t0)
        return False
