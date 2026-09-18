"""Paired classification-only probe; BO numerical outputs are never sent to the model."""
from pathlib import Path
import json
import sys
from datetime import datetime

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from tools.batch_tools import _matrix_stats_preview
from tools.llm_helpers import classify_matrix_with_llm, llm_usage_summary
from tools.evidence import file_sha256


def main():
    source = ROOT / "_rnaseq_benchmark_input" / "GSE194151"
    matrix = source / "FH_vs_MH.rawcount.txt"
    stats, preview = _matrix_stats_preview(str(matrix))
    # Read provenance, never execute these scripts. DESeq2.r and gold results are excluded:
    # this experiment tests recognition of the measurement, not imitation of a gold answer.
    sources = [source / "prep_pairwise_input.py", source / "count_2_cpm.r"]
    provenance = "\n\n".join(f"SOURCE {p.name} (sha256={file_sha256(str(p))}):\n{p.read_text()}" for p in sources)
    out = ROOT / "output" / ("matrix_semantics_probe_" + datetime.now().strftime("%Y%m%d_%H%M%S"))
    out.mkdir(parents=True, exist_ok=False)
    records = []
    for repeat in range(3):
        for arm in (["numeric_only", "with_provenance"] if repeat % 2 == 0 else ["with_provenance", "numeric_only"]):
            result = classify_matrix_with_llm(
                filename=matrix.name, platform="", value_stats=stats, preview_text=preview,
                heuristic_label="fpkm_or_tpm", organism="Mouse",
                provenance=provenance if arm == "with_provenance" else "",
            )
            records.append({"repeat": repeat + 1, "arm": arm,
                            "decision": result.model_dump() if result else None})
            (out / "results.json").write_text(json.dumps({
                "matrix": str(matrix), "matrix_sha256": file_sha256(str(matrix)),
                "provenance": provenance, "records": records, "usage": llm_usage_summary(),
            }, ensure_ascii=False, indent=2), encoding="utf-8")
            print(json.dumps(records[-1], ensure_ascii=False), flush=True)
    print(out, flush=True)


if __name__ == "__main__":
    main()
