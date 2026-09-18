# RNA-seq ZIP 金标准 Benchmark 报告

## 目的

正式目标是验证 agent 能否正确处理 BO 提供的金标准 RNA-seq 数据。`F:\\RNAseqData4Testing.zip` 是正式 benchmark 输入；本报告只记录 ZIP 冻结输入的结果。

## 正式输入与覆盖范围

ZIP 中共覆盖 6 个 pairwise contrast：

- GSE194151：FC vs MC、FH vs FC、FH vs MH、MH vs MC
- GSE195482：WMF vs WCF、WMM vs WCM

每个 contrast 使用独立的冻结矩阵和元数据工作区，并记录 SHA-256。6 个本地运行均完成，状态为 `deg_gsea_ok`。

## 金标准运行结果

| Contrast | Samples | Matrix route | DA method | DEG | GSEA significant | Audit |
|---|---:|---|---|---:|---:|---|
| GSE194151 FC vs MC | 15 | kallisto estimated counts -> explicit round -> raw-count route | DESeq2 | 10,776 | 33 | warning: DEG sanity |
| GSE194151 FH vs FC | 14 | kallisto estimated counts -> explicit round -> raw-count route | DESeq2 | 1,617 | 46 | pass |
| GSE194151 FH vs MH | 15 | kallisto estimated counts -> explicit round -> raw-count route | DESeq2 | 11,035 | 37 | warning: DEG sanity |
| GSE194151 MH vs MC | 16 | kallisto estimated counts -> explicit round -> raw-count route | DESeq2 | 274 | 26 | pass |
| GSE195482 WMF vs WCF | 6 | raw counts | DESeq2 | 1,379 | 42 | pass |
| GSE195482 WMM vs WCM | 6 | raw counts | DESeq2 | 128 | 37 | pass |

All six cases completed with intact artifacts and provenance. This rerun used strict semantic confirmation: the four GSE194151 cases were classified as estimated counts, and both GSE195482 integer matrices were independently confirmed as raw counts. GSE194151 FC vs MC and FH vs MH triggered the existing DEG sanity gate because approximately 51% and 53% of tested features were significant. Those are scientific review items, not execution or provenance failures.

## 数据类型判断修复

The numeric profile alone is insufficient to distinguish FPKM/TPM from estimated counts. The ZIP's `prep_pairwise_input.py` identifies the source as kallisto counts, and `DESeq2.r` explicitly rounds the same pairwise files before DESeq2. The agent reproduces that documented recipe by writing a rounded-count artifact; it does not generalize rounding to estimated-count matrices without matching provenance.

This keeps the fast code path for clear integer raw counts. The LLM is called only for decimal or otherwise ambiguous cases, where it reads bounded nearby scripts and notes. If provenance cannot support a safe route, the run fails closed instead of silently choosing log2 + limma or blind rounding.

## 正式 benchmark 结论

The agent completed all six BO cases with intact artifacts, correct sample alignment, provenance bundles, and method routing consistent with the processing recipes shipped in the ZIP. Formal acceptance should remain conditional on BO confirming the interpretation of the fractional-count matrix and the two DEG-sanity warnings.

## Artifacts

- Local benchmark outputs: `output/rnaseq_zip_remote_ab/output_local/`
- Frozen input manifest: `output/rnaseq_zip_remote_ab/manifest.json`
- Reproducible runner: `test/experiments/rnaseq_zip_remote_ab/run_experiment.py`
- Semantic probe: `test/experiments/rnaseq_zip_remote_ab/probe_semantics.py`
- Branch: `codex/rnaseq-benchmark-gse194151`
