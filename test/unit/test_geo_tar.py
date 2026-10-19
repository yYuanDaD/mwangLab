"""RAW.tar merging (STAR ReadsPerGene, plain tables) and multi-sheet Excel conversion.

From the 2026-10-19 large-run pilot: GSE208639 shipped STAR ReadsPerGene tables in its
_RAW.tar, which no helper could merge, and a 4-sheet edgeR workbook of which only the first
sheet survived download.
"""
import gzip
import io
import os
import tarfile

import pandas as pd

from tools import native
from tools.geo_tools import excel_to_csvs
from tools.omics_semantics import choose_star_strand, read_star_reads_per_gene

GENES = [f"ENSG{i:011d}" for i in range(60)]


def _star(forward_scale: float, reverse_scale: float, seed: int) -> str:
    rows = ["N_unmapped\t100\t100\t100", "N_multimapping\t50\t50\t50",
            "N_noFeature\t10\t900\t20", "N_ambiguous\t5\t1\t1"]
    for i, g in enumerate(GENES):
        base = (i * 37 + seed) % 200
        rows.append(f"{g}\t{base}\t{int(base * forward_scale)}\t{int(base * reverse_scale)}")
    return "\n".join(rows) + "\n"


def _tar(path: str, members: dict) -> None:
    with tarfile.open(path, "w") as t:
        for name, text in members.items():
            data = gzip.compress(text.encode()) if name.endswith(".gz") else text.encode()
            info = tarfile.TarInfo(name)
            info.size = len(data)
            t.addfile(info, io.BytesIO(data))


def test_read_star_and_choose_strand(tmp_path):
    p = tmp_path / "GSM1_S1.ReadsPerGene.out.tab"
    p.write_text(_star(0.05, 0.95, 1))
    t = read_star_reads_per_gene(str(p))
    assert list(t.columns) == ["unstranded", "forward", "reverse"] and len(t) == len(GENES)
    assert "N_unmapped" not in t.index
    assert choose_star_strand([t]).column == "reverse"
    p2 = tmp_path / "u.tab"
    p2.write_text(_star(0.5, 0.48, 2))
    assert choose_star_strand([read_star_reads_per_gene(str(p2))]).column == "unstranded"
    p3 = tmp_path / "m.tab"
    p3.write_text(_star(0.7, 0.3, 3))
    assert choose_star_strand([read_star_reads_per_gene(str(p3))]).column is None   # ratio ~2.3
    q = tmp_path / "plain.txt"
    q.write_text("gene\tcount\nG1\t3\n")
    assert read_star_reads_per_gene(str(q)) is None


def test_merge_raw_tar_star(tmp_path):
    d = tmp_path / "GSE208639"
    d.mkdir()
    _tar(str(d / "GSE208639_RAW.tar"), {
        f"GSM{i}_P{i}.ReadsPerGene.out.tab.gz": _star(0.04, 0.96, i) for i in range(4)})
    res = native.merge_raw_tar(d)
    assert res["n_samples"] == 4 and res["n_genes"] == len(GENES), res
    assert res["samples"] == [f"GSM{i}_P{i}" for i in range(4)], res["samples"]
    merged = pd.read_csv(res["output"], index_col=0)
    star0 = read_star_reads_per_gene(str(d / "_unpacked" / "GSM0_P0.ReadsPerGene.out.tab.gz"))
    assert (merged["GSM0_P0"] == star0["reverse"]).all()


def test_merge_raw_tar_plain_counts(tmp_path):
    d = tmp_path / "GSE1"
    d.mkdir()
    table = "gene\tcount\n" + "".join(f"{g}\t{i}\n" for i, g in enumerate(GENES))
    _tar(str(d / "GSE1_RAW.tar"), {"GSM1_a.txt.gz": table, "GSM2_b.txt.gz": table})
    res = native.merge_raw_tar(d)
    assert res["samples"] == ["GSM1_a", "GSM2_b"] and res["n_genes"] == len(GENES)


def test_excel_every_sheet_kept(tmp_path):
    x = tmp_path / "GSE208639_edgeR_output.xlsx"
    with pd.ExcelWriter(x) as w:
        for name in ("Post vs Pre", "Pre vs Ctrl", "Per patient", "Counts"):
            pd.DataFrame({"gene": ["A", "B"], "v": [1, 2]}).to_excel(w, sheet_name=name, index=False)
    out = excel_to_csvs(str(x))
    names = [os.path.basename(p) for p in out]
    assert names == ["GSE208639_edgeR_output.csv", "GSE208639_edgeR_output__Pre_vs_Ctrl.csv",
                     "GSE208639_edgeR_output__Per_patient.csv", "GSE208639_edgeR_output__Counts.csv"], names
    assert x.exists()
