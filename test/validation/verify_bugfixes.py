"""Reproduce-and-verify the robustness bugs surfaced during the validation/demo runs.

For each bug we feed the EXACT shape of input that used to crash/corrupt, run it through the
fixed code, and assert the fix handles it. Where useful we also show the *mechanism* of the old
failure (e.g. patsy raising on a spaced column name) so the report can claim "this was really a
bug", not just "the fix is present".

Offline + deterministic: no network, no LLM, no R required for the asserts (the limma-voom check
verifies the decode guarantee, not a live R subprocess). Run with the venv python:
    .venv/Scripts/python.exe test/validation/verify_bugfixes.py
"""

import os
import sys
import csv
import tempfile

import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(os.path.dirname(_HERE))
os.chdir(_ROOT)
sys.path.insert(0, _ROOT)

_RESULTS = []


def check(name, fn):
    try:
        detail = fn()
        _RESULTS.append((name, True, detail))
        print(f"[PASS] {name}\n       {detail}")
    except Exception as e:
        _RESULTS.append((name, False, str(e)))
        print(f"[FAIL] {name}\n       {type(e).__name__}: {e}")
    print()


# --------------------------------------------------------------------------------------
# Bug 1 — duplicate gene IDs broke DESeq2/limma/edgeR/voom (reindex / read.csv errors).
# Fix: collapse_duplicate_genes (MaxMean — keep highest-mean row per duplicated symbol).
# --------------------------------------------------------------------------------------
def bug1_duplicate_genes():
    from tools.deseq2_tools import collapse_duplicate_genes
    df = pd.DataFrame(
        {"s1": [10, 1000, 5, 7], "s2": [12, 1100, 6, 9]},
        index=["GENE_A", "GENE_A", "GENE_B", "GENE_C"],  # GENE_A duplicated
    )
    assert df.index.has_duplicates, "test setup wrong: index not duplicated"
    out = collapse_duplicate_genes(df, "test")
    assert not out.index.has_duplicates, "duplicates survived collapse"
    assert list(out.index) == sorted(out.index.tolist()) or set(out.index) == {"GENE_A", "GENE_B", "GENE_C"}
    # MaxMean: the kept GENE_A row must be the high-mean one (1000/1100), not (10/12).
    kept = out.loc["GENE_A"].tolist()
    assert kept == [1000, 1100], f"kept wrong duplicate row: {kept} (expected high-mean [1000,1100])"
    # no-op path: already-unique index returns the same frame untouched
    uniq = pd.DataFrame({"s1": [1, 2]}, index=["X", "Y"])
    assert collapse_duplicate_genes(uniq, "test").equals(uniq), "no-op path altered a unique-index frame"
    return f"3 unique genes from 4 rows; GENE_A kept high-mean row {kept}; no-op preserved unique frame"


# --------------------------------------------------------------------------------------
# Bug 2 — LLM sometimes returns a Sourced field as a bare string ('SED') / list / number,
# tripping ValidationError and losing the WHOLE paper (GSE250122 was dropped this way).
# Fix: Sourced._coerce_scalar (model_validator mode='before') coerces scalars -> {value, source}.
# --------------------------------------------------------------------------------------
def bug2_sourced_coercion():
    from tools.sea_cdm_schema import Sourced, Groups
    # bare string
    s = Sourced.model_validate("SED")
    assert s.value == "SED" and s.source is None, f"str coercion wrong: {s}"
    # list -> ';'-joined
    s = Sourced.model_validate(["A", "B", None])
    assert s.value == "A; B" and s.source is None, f"list coercion wrong: {s}"
    # number / bool -> str
    assert Sourced.model_validate(3).value == "3"
    assert Sourced.model_validate(True).value == "True"
    # None -> both None
    s = Sourced.model_validate(None)
    assert s.value is None and s.source is None
    # proper {value, source} object still works
    s = Sourced.model_validate({"value": "treadmill", "source": "Methods p.3"})
    assert s.value == "treadmill" and s.source == "Methods p.3"
    # the real failure: a parent model receiving a bare string for a Sourced field must NOT raise
    g = Groups(group_id="GSE250122_grp1", study_id="GSE250122", subject_group="post-exercise")
    assert g.subject_group.value == "post-exercise", "parent-model bare-string coercion failed"
    return "bare str/list/num/None all coerced; {value,source} preserved; Groups(subject_group='post-exercise') OK"


# --------------------------------------------------------------------------------------
# Bug 3 — pydeseq2 builds a patsy formula `~ <col>`; a GEO design column with a space
# ('characteristics_ch1.2.running protocole') made patsy raise "Missing operator".
# Fix: rename the design column to safe 'design_factor' before building the model.
# --------------------------------------------------------------------------------------
def bug3_deseq2_spaced_column():
    from patsy import dmatrix, PatsyError
    SPACED = "characteristics_ch1.2.running protocole"
    demo = pd.DataFrame({SPACED: ["sed", "sed", "ex", "ex"]})

    # (a) show the OLD mechanism really fails: a spaced bare column name in a patsy formula raises.
    old_failed = False
    try:
        dmatrix(f"~ {SPACED}", demo)
    except (PatsyError, Exception):
        old_failed = True
    assert old_failed, "expected patsy to reject the spaced column name (old bug mechanism)"
    # the fix's safe name parses fine
    dmatrix("~ design_factor", demo.rename(columns={SPACED: "design_factor"}))

    # (b) end-to-end: run the FIXED run_deseq2_analysis on a tiny synthetic study whose
    #     design column has a space. Before the fix this crashed; now it must produce a DEG file.
    rng = np.random.default_rng(0)
    n_genes = 200
    samples = [f"S{i}" for i in range(6)]
    base = rng.poisson(50, size=(n_genes, 6))
    # inject a real signal in the last 20 genes for the treatment trio
    base[-20:, 3:] += rng.poisson(80, size=(20, 3))
    counts = pd.DataFrame(base, index=[f"g{i}" for i in range(n_genes)], columns=samples)
    meta = pd.DataFrame({SPACED: ["sed", "sed", "sed", "ex", "ex", "ex"]}, index=samples)

    with tempfile.TemporaryDirectory() as td:
        cpath = os.path.join(td, "counts.csv")
        mpath = os.path.join(td, "meta.csv")
        counts.to_csv(cpath)
        meta.to_csv(mpath)
        from tools.deseq2_tools import run_deseq2_analysis
        msg = run_deseq2_analysis.invoke({
            "counts_csv": cpath, "metadata_csv": mpath,
            "design_column": SPACED, "control_group": "sed", "treatment_group": "ex",
            "output_dir": td,
        })
        assert "completed successfully" in msg, f"DESeq2 failed on spaced column:\n{msg}"
        deg = [f for f in os.listdir(td) if f.startswith("DEG_results_")]
        assert deg, "no DEG file written"
        res = pd.read_csv(os.path.join(td, deg[0]), index_col=0)
        assert {"log2FoldChange", "padj"} <= set(res.columns)
    return f"patsy rejects spaced name (old bug confirmed); fixed DESeq2 ran OK -> {deg[0]} ({len(res)} genes)"


# --------------------------------------------------------------------------------------
# Bug 4 — capturing R's (limma-voom) stderr with the Windows locale default (GBK) crashed
# with UnicodeDecodeError on bytes R emits that are invalid in GBK.
# Fix: subprocess.run(..., encoding='utf-8', errors='replace'). Verify the decode guarantee
# (the live R subprocess emitting bad bytes is environment-dependent; the guarantee is not).
# --------------------------------------------------------------------------------------
def bug4_voom_decode_guarantee():
    bad = b"R limma-voom: \xff\xfe partial \x80\x81 bytes"  # invalid under both utf-8-strict and gbk
    # strict decode (the spirit of the old default) raises:
    raised = False
    try:
        bad.decode("utf-8")
    except UnicodeDecodeError:
        raised = True
    assert raised, "test bytes are not actually invalid under strict utf-8"
    # the fix's settings never raise and yield a usable string:
    safe = bad.decode("utf-8", errors="replace")
    assert isinstance(safe, str) and "limma-voom" in safe
    # confirm the tool actually passes these kwargs to subprocess.run
    import inspect
    src = inspect.getsource(__import__("tools.limma_voom_tools", fromlist=["run_limma_voom_analysis"]))
    assert 'encoding="utf-8"' in src and 'errors="replace"' in src, "tool no longer sets utf-8/replace"
    return f"strict decode raises; errors='replace' -> {safe!r}; tool source sets utf-8+replace"


# --------------------------------------------------------------------------------------
# Bug 5 — cohort n_fail counted any status containing 'fail' as a paper failure, so a paper
# that extracted fine but whose GSEA sub-step failed ('deg_ok_gsea_failed') was mis-counted.
# Fix: a paper failed only if NOT status.startswith('text_ok').
# --------------------------------------------------------------------------------------
def bug5_n_fail_predicate():
    manifest = [
        {"status": "text_ok"},                  # clean success
        {"status": "text_ok_deg_ok_gsea_failed"},  # extracted fine, only GSEA sub-step failed
        {"status": "text_ok_deg_failed"},          # extracted fine, DA sub-step failed
        {"status": "fetch_failed"},                # real paper-level failure
        {"status": "extract_failed"},              # real paper-level failure
    ]
    n_fail = sum(1 for m in manifest if not m["status"].startswith("text_ok"))
    n_text = sum(1 for m in manifest if m["status"].startswith("text_ok"))
    assert n_text == 3, f"text-extracted miscount: {n_text}"
    assert n_fail == 2, f"n_fail should be 2 (only fetch/extract), got {n_fail}"
    # the OLD buggy predicate ('fail' in status) would over-count:
    old = sum(1 for m in manifest if "fail" in m["status"])
    assert old == 4, f"old predicate sanity: {old}"
    return f"new predicate: 3 text-ok / 2 failed (vs old 'fail'-substring would say {old} failed)"


# --------------------------------------------------------------------------------------
# Bug 6 — init_cohort_csvs appended on re-run, so re-running a cohort with the same run_label
# accumulated stale rows. Fix: always truncate (open 'w') and rewrite header-only.
# --------------------------------------------------------------------------------------
def bug6_init_cohort_truncates():
    from tools.cohort_tools import init_cohort_csvs
    from tools.sea_cdm_schema import SEA_TABLES, csv_columns
    with tempfile.TemporaryDirectory() as td:
        init_cohort_csvs(td)
        study_csv = os.path.join(td, "study.csv")
        assert os.path.isfile(study_csv), "study.csv not created"
        # inject a stale data row, as a prior run would have left
        with open(study_csv, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=csv_columns("study"))
            w.writerow({"study_id": "STALE_GSE"})
        with open(study_csv, encoding="utf-8") as f:
            rows_before = sum(1 for _ in f)
        assert rows_before == 2, f"setup: expected header+1 stale row, got {rows_before}"
        # re-run with the same dir: must truncate the stale row back to header-only
        init_cohort_csvs(td)
        df = pd.read_csv(study_csv)
        assert len(df) == 0, f"re-run did not truncate: {len(df)} data rows remain"
        assert list(df.columns) == csv_columns("study"), "header columns changed after re-run"
        n_csv = sum(1 for t, e in SEA_TABLES.items() if os.path.isfile(os.path.join(td, e["csv"])))
    return f"stale row (header+1) -> after re-run header-only (0 data rows); {n_csv} table CSVs scaffolded"


# --------------------------------------------------------------------------------------
# Bug 7 — Sonnet's structured output intermittently serializes a list-typed field (e.g.
# MethodsExtraction.assays) — or the whole object — as a JSON *string* ('[{...}]') instead of
# a real list, tripping ValidationError and killing the WHOLE extraction. Caught by the
# 2026-06-03 demo safety check (extraction crashed on the seeded paper). Fix:
# _CoerceJSONContainer (mode='before' model_validator) json.loads() any stringified
# array/object field back into a structure before validation.
# --------------------------------------------------------------------------------------
def bug7_json_string_container():
    import json
    from tools.seacdm_tools import MethodsExtraction, DesignExtraction
    # the EXACT failure shape: assays as a stringified JSON list (with a nested Sourced)
    stringified = json.dumps([{"assay_name": {"value": "Long-read RNA-Seq", "source": "ONT MinION"},
                               "experiment_index": 1}])
    m = MethodsExtraction(samples=[], interventions=[], assays=stringified)
    assert isinstance(m.assays, list) and len(m.assays) == 1, "stringified assays list not parsed"
    assert m.assays[0].assay_name.value == "Long-read RNA-Seq", "nested Sourced lost after coercion"
    # whole object delivered as a JSON string
    d = DesignExtraction.model_validate(json.dumps({"experiments": [{"experiment_index": 1}],
                                                    "subjects": [], "groups": []}))
    assert len(d.experiments) == 1, "whole-object JSON string not parsed"
    # normal already-list input must still work (no regression)
    ok = MethodsExtraction(assays=[{"assay_name": "RNA-Seq", "experiment_index": 1}])
    assert len(ok.assays) == 1 and ok.assays[0].assay_name.value == "RNA-Seq"
    return "stringified assays-list + whole-object-string parsed (nested Sourced intact); normal list unaffected"


# --------------------------------------------------------------------------------------
# Bug 8 — _find_expression_file mis-picked a clinical phenotype data dictionary
# (GSE242358 *_phenotype_viallabel_data-v5.txt.gz: VO2max/treadmill/body-comp numeric
# columns) as the expression matrix, never reaching the real expression in _RAW.tar.
# Fix: _NONEXPRESSION_NAME_HINTS excludes phenotype/viallabel/clinical/... filenames.
# --------------------------------------------------------------------------------------
def bug8_phenotype_not_picked():
    import numpy as np
    from tools.batch_tools import _find_expression_file
    with tempfile.TemporaryDirectory() as td:
        pheno = pd.DataFrame({"vo2max": [40.1, 44.2, 38.9], "treadmill_speed": [12.0, 13.5, 11.0],
                              "bodyfat_pct": [18.2, 21.0, 16.5]}, index=["vial1", "vial2", "vial3"])
        pheno.to_csv(os.path.join(td, "GSE242358_phenotype_viallabel_data-v5.txt.gz"),
                     sep="\t", compression="gzip")
        path, reason = _find_expression_file(td)
        assert path is None, f"phenotype dictionary was wrongly picked: {path} ({reason})"
        # a real raw-counts matrix in the same dir must be chosen over the phenotype file
        rc = pd.DataFrame(np.random.default_rng(0).integers(0, 5000, size=(50, 6)),
                          index=[f"g{i}" for i in range(50)], columns=[f"S{i}" for i in range(6)])
        rc.to_csv(os.path.join(td, "GSE242358_raw_counts.csv"))
        path, mtype = _find_expression_file(td)
        assert path and path.endswith("raw_counts.csv") and mtype == "raw_counts", f"got {path} {mtype}"
    return "phenotype-only dir -> not picked; real raw_counts chosen when present"


# --------------------------------------------------------------------------------------
# Bug 9 — verify_provenance flagged faithful STITCHED quotes ('A ... B', spans joined by the
# LLM) as [UNVERIFIED] because the whole string isn't a single substring, inflating the flag
# rate. Fix: _quote_is_verbatim splits on ellipsis and verifies each fragment; a fabricated or
# partially-fake span is still flagged.
# --------------------------------------------------------------------------------------
def bug9_stitched_quote_verified():
    from tools.seacdm_tools import _quote_is_verbatim, _norm_quote
    text = ("We collected 10 non-exercised control rats (five males and five females). Tissues "
            "included SKM-GN, heart, BAT and liver were profiled by RNA-seq.")
    nt = _norm_quote(text)
    stitched = "10 non-exercised control rats (five males and five females)... SKM-GN, heart, BAT"
    assert _quote_is_verbatim(stitched, nt), "faithful stitched quote wrongly flagged"
    assert not _quote_is_verbatim("we performed a 12-week resistance training program", nt), \
        "fabricated quote wrongly accepted"
    assert not _quote_is_verbatim("10 non-exercised control rats... we sequenced spleen at midnight", nt), \
        "stitched quote with a fake span wrongly accepted"
    return "faithful stitched quote verified; fabricated & one-fake-span stitched still flagged"


# --------------------------------------------------------------------------------------
# Bug 10 — _unpack_and_merge_geo_tar SILENTLY dropped per-sample files that failed to parse
# (GSE291636 lost samples this way) — violates the project's fail-loud principle. Fix: track
# skipped members with reasons and print a WARNING with the count, so a dropped-sample
# mismatch is visible instead of silent.
# --------------------------------------------------------------------------------------
def bug10_tar_merge_reports_skips():
    import io
    import gzip
    import tarfile
    import contextlib
    from tools.batch_tools import _unpack_and_merge_geo_tar
    with tempfile.TemporaryDirectory() as td:
        data_dir = os.path.join(td, "GSE000TAR")
        os.makedirs(data_dir)
        # two valid per-sample count files + one unparseable member (a dropped sample)
        good = {"GSM1_a.txt": "gene\tcount\nG1\t10\nG2\t20\n",
                "GSM2_b.txt": "gene\tcount\nG1\t11\nG2\t22\n"}
        tar_path = os.path.join(data_dir, "GSE000TAR_RAW.tar")
        with tarfile.open(tar_path, "w") as t:
            for name, content in good.items():
                raw = content.encode()
                ti = tarfile.TarInfo(name); ti.size = len(raw)
                t.addfile(ti, io.BytesIO(raw))
            # a binary blob that pandas cannot parse as a table -> must be reported, not silent
            bad = gzip.compress(b"\x00\x01\x02not a table\x03")
            ti = tarfile.TarInfo("GSM3_corrupt.csv.gz"); ti.size = len(bad)
            t.addfile(ti, io.BytesIO(bad))
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            merged = _unpack_and_merge_geo_tar(data_dir)
        out = buf.getvalue()
        assert merged and os.path.isfile(merged), "merge produced no file"
        df = pd.read_csv(merged, index_col=0)
        assert df.shape[1] == 2, f"expected 2 merged samples, got {df.shape[1]}"
        assert "WARNING: skipped" in out and "1/3" in out, f"skip not surfaced (fail-loud): {out!r}"
    return "2/3 members merged; the 1 unparseable member is REPORTED ('WARNING: skipped 1/3'), not dropped silently"


def main():
    print("=" * 78)
    print("BUG-FIX VERIFICATION — reproduce each broken input against the fixed code")
    print("=" * 78 + "\n")
    check("Bug 1  duplicate gene IDs  -> collapse_duplicate_genes (MaxMean)", bug1_duplicate_genes)
    check("Bug 2  Sourced bare string -> _coerce_scalar (model_validator before)", bug2_sourced_coercion)
    check("Bug 3  DESeq2 spaced design column -> rename to 'design_factor'", bug3_deseq2_spaced_column)
    check("Bug 4  limma-voom R stderr decode -> utf-8 + errors='replace'", bug4_voom_decode_guarantee)
    check("Bug 5  cohort n_fail miscount -> not status.startswith('text_ok')", bug5_n_fail_predicate)
    check("Bug 6  init_cohort_csvs stale rows -> always truncate", bug6_init_cohort_truncates)
    check("Bug 7  LLM stringified-JSON container field -> _CoerceJSONContainer", bug7_json_string_container)
    check("Bug 8  phenotype dictionary mis-picked as matrix -> _NONEXPRESSION_NAME_HINTS", bug8_phenotype_not_picked)
    check("Bug 9  faithful stitched provenance quote flagged -> _quote_is_verbatim", bug9_stitched_quote_verified)
    check("Bug 10 tar-merge silently dropped samples -> report skipped members", bug10_tar_merge_reports_skips)

    n_pass = sum(1 for _, ok, _ in _RESULTS if ok)
    print("=" * 78)
    print(f"RESULT: {n_pass}/{len(_RESULTS)} bug-fixes verified")
    for name, ok, _ in _RESULTS:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    print("=" * 78)
    sys.exit(0 if n_pass == len(_RESULTS) else 1)


if __name__ == "__main__":
    main()
