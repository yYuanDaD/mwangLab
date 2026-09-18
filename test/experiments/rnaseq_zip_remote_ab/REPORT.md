# RNA-seq ZIP 金标准 Benchmark 报告

## 目的

正式目标是验证 agent 能否正确处理 BO 提供的金标准 RNA-seq 数据。`F:\\RNAseqData4Testing.zip` 是正式 benchmark 输入；GEO 远程下载臂只作为小型数据来源差异实验，不参与正式正确性评分。

## 正式输入与覆盖范围

ZIP 中共覆盖 6 个 pairwise contrast：

- GSE194151：FC vs MC、FH vs FC、FH vs MH、MH vs MC
- GSE195482：WMF vs WCF、WMM vs WCM

每个 contrast 使用独立的冻结矩阵和元数据工作区，并记录 SHA-256。所有本地运行均完成，状态为 `completed`。

## 金标准运行结果

| Contrast | Samples | Matrix route | DA method | DEG | GSEA significant | Audit |
|---|---:|---|---|---:|---:|---|
| GSE194151 FC vs MC | 15 | fpkm_or_tpm → log2 + limma | limma | 13,347 | 42 | pass |
| GSE194151 FH vs FC | 14 | fpkm_or_tpm → log2 + limma | limma | 36 | 19 | pass |
| GSE194151 FH vs MH | 15 | fpkm_or_tpm → log2 + limma | limma | 14,448 | 39 | fail: DEG sanity |
| GSE194151 MH vs MC | 16 | fpkm_or_tpm → log2 + limma | limma | 20 | 21 | pass |
| GSE195482 WMF vs WCF | 6 | raw counts | DESeq2 | 1,379 | 42 | pass |
| GSE195482 WMM vs WCM | 6 | raw counts | DESeq2 | 128 | 37 | pass |

Coverage was 89.1% for the independent audits. Five cases passed all blocking checks. GSE194151 FH vs MH triggered the DEG sanity gate because approximately 53% of tested features were significant; this is a scientific review item, not an execution or provenance failure.

## 正式 benchmark 结论

The agent completed all six BO cases with intact artifacts, correct sample alignment, provenance bundles, and method routing consistent with the observed matrix types. Formal acceptance should remain conditional on BO confirming the interpretation of the GSE194151 fractional-count matrix and the unusually large FH vs MH DEG fraction.

## 远程下载小实验（不计入正式评分）

The remote arm also completed six runs, but it did not reproduce the ZIP contrasts:

- GSE194151 remote GEO metadata had 30 samples and used `Control diet` vs `High-fat diet + L-NAME`.
- GSE195482 remote GEO data had 24 samples, was classified as FPKM/TPM, and used `chow` vs `HFPEF`.
- The requested ZIP labels such as FC/FH/MC/MH and WMF/WCF/WMM/WCM were absent remotely, so the contrast-validation fallback selected the nearest biological design.

Therefore the remote arm demonstrates accession-version and metadata-design drift. Its DEG/GSEA differences must not be interpreted as an agent correctness score against the BO gold standard.

## Artifacts

- Local/remote comparison: `output/rnaseq_zip_remote_ab/comparison.csv`
- Frozen input manifest: `output/rnaseq_zip_remote_ab/manifest.json`
- Reproducible runner: `test/experiments/rnaseq_zip_remote_ab/run_experiment.py`
- Branch: `codex/rnaseq-benchmark-gse194151`
