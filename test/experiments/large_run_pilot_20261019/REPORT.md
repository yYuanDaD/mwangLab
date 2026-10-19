# Large-run pilot, 2026-10-19

Codex is out of quota until 2026-10-26 (see `RESUME.md`), so the owner chose to have Claude
run 2 of the 5 pilot papers first.

## Claude pilot (2 papers)

Each paper was run by a fresh Claude subagent that saw only the request (the same text
`RESUME.md` gives Codex) and the skill. It had no notes from the screening work. The
papers ran one at a time in `E:\agent\mwangLab_pdf` with `.venv-pdf`.

Outputs are in `runs_claude/<paper_id>/`. Decisions, summaries and driver scripts are
committed; matrices and result tables stay local (`runs_claude/.gitignore`), and so does
`data/`.

| Paper | Series | Wall time | Subagent tokens | Tool calls | Status | Validator |
|---|---|---:|---:|---:|---|---|
| PMID39832562, timing of exercise in adolescent rat adipose | GSE283493 (rat, raw counts) | 8.6 min | 190,945 | 28 | 4/5 cases run; LRT case stopped at the `covariance` gate (manual_review) | VALID (50 records) |
| PMID37318869, DM1 strength training | GSE208639 (human, counts in `_RAW.tar`) | 16.0 min | 206,759 | 55 | 3/3 cases run | VALID (33 records) |

No external LLM calls were made. The subagent token counts come from the Agent tool; they
are total tokens, without an input/cached/output split.

### Comparisons, compared with the paper

**PMID39832562 (GSE283493).** The paper ran DESeq2 Wald tests of exercise vs control within
each tissue and time of day, with 2 SVA surrogate variables, apeglm shrinkage, and
padj < 0.1 plus |log2FC| > 0.5. It also ran a phase × training LRT. It removed 4 outliers.
The run reproduced the 4 Wald contrasts, removed the same 4 outliers, and declared a
deviation: no SVs and no shrinkage.

| Contrast | n (control / exercise) | DEGs: run (up / down) | DEGs: paper |
|---|---|---|---|
| SAT early active phase | 6 / 6 | 0 | 7 |
| SAT late active phase | 6 / 4 | 497 (299 / 198) | 353 |
| VAT early active phase | 5 / 5 | 2 (1 / 1) | 2 |
| VAT late active phase | 6 / 6 | 37 (34 / 3) | 14 |
| phase × training LRT | – | not run | 632 |

The paper's main pattern holds: late-active-phase exercise changes far more genes than
early-active-phase exercise, and more in SAT than in VAT. The named genes in SAT late phase
change in the same direction as the paper's figures. GSEA (Hallmark, mapped from rat to
mouse symbols) ran for all 4 contrasts.

**PMID37318869 (GSE208639).** The paper compared DM1 patients with controls before and after
training using edgeR QL, raw P < 0.05 and |log2FC| > 2. It also did n = 1 analyses per
patient. It never tested post vs pre directly.

| Case | Route | DEGs under the paper rule (up / down) | Note |
|---|---|---|---|
| case_01 | post vs pre, DESeq2 `~ subject + grp` (9 pairs) | 20 (18 / 2) | Declared deviation: tests the paper's Δlog2FC directly. Top genes are ECM genes, matching S2.3.p1 |
| case_02 | pre vs control | 475 (223 / 252) | Paper rule. The authors' deposited table has 176 at the same rule; logFC r = 0.926 |
| case_02 | post vs control | 512 (377 / 135) | 274/448 genes "rescued" |
| case_03 | per-patient n = 1, limma `~0 + unit` | 0–516 per patient | Labelled exploratory. Patient ranking of % rescue matches the paper (523 highest, 2005 lowest) |

GSEA and ORA ran on case_01 and were labelled as additions, because the paper does no
pathway analysis.

### Pipeline problems to fix before the Codex runs

| # | Problem | Where | Effect |
|---|---|---|---|
| 1 | Supplementary `.xlsx` is converted from its **first sheet only**, then the xlsx is deleted. `GSE208639_edgeR_output.xlsx` had 4 sheets; 3 were lost silently | `tools/geo_tools.py:85` (`pd.read_excel`), `:89` (`os.remove`) | Data loss without warning |
| 2 | No helper merges a `_RAW.tar` of STAR `ReadsPerGene.out.tab`. The generic reader would take the `N_unmapped` row as the header, and the 3 strand columns are "ambiguous". The agent wrote its own merge and picked the reverse strand from the data and the kit | `tools/batch_tools.py:348`, `tools/omics_semantics.py:48` | Every tar-sourced paper needs bespoke code. The screen found STAR tables in several tar papers |
| 3 | No TMM normalisation in the edgeR executor (inmoose has no `calcNormFactors`) | `tools/edger_tools.py` (module docstring) | About 0.27 log2 composition shift in disease-vs-control; inflates DEG counts (475 vs the authors' 176) |
| 4 | No log2FC shrinkage (apeglm) in DESeq2 | `tools/deseq2_tools.py:136-152` | Thresholds use MLE log2FC; more DEGs at small n |
| 5 | No surrogate-variable (SVA) or likelihood-ratio-test executor | – | Paper designs with SVs or an LRT become deviations or stop |
| 6 | Executors print their own DEG summary at padj < 0.05 and \|log2FC\| > 1, ignoring the paper's rule | `tools/deseq2_tools.py:160-166` | Misleading log lines; both agents ignored them |
| 7 | GSEA and ORA accept only Mouse/Human; rat needs a private helper (`_query_symbols(..., "rat")`) and symbol identity mapping | `tools/enrichment_tools.py:202`, `:329` | 10 rat papers in the 47-paper list |
| 8 | The validator compares `effect_metric` exactly, so the skill gives no way to record "same metric, different estimator" (shrunken vs MLE) | `tools/decision_contract.py:266-270` | Agent used an extra field as a workaround |
| 9 | The minimum of 2 replicates per group blocks n = 1 designs | `tools/analysis_policy.py:16` | The paper's per-patient analysis needed a limma workaround |
| 10 | The skill's driver-script prelude assumes `output/<run>/scripts/` (`parents[3]`); deeper run directories break imports | `.agents/skills/bioinformatics-workflow/SKILL.md:38` | One failed script, then fixed |
| 11 | Matrix columns are library names stored only in GEO `description` ("Library name: …") | data | Solved with `native.derive_columns`; worth a note in the skill |

Paper-vs-GEO notes:
- GSE283493 is public, but the paper says the data are available on request.
- The AM/PM labels had to be matched to early/late phase from the outlier pattern.
- GSE208639 has no age column in GEO, although the paper notes that the controls are younger.

### Estimate for the 47-paper run

These two papers averaged 12.3 min and about 199k subagent tokens each. For 47 papers that is
about **9.6 hours and 9.3 M tokens**, in Claude subagent terms. Papers with a `_RAW.tar` or a
multi-factor design took about twice as long.

Two of the problems above recur across the list and would cut both time and errors before the
Codex run:
- the STAR `_RAW.tar` merge (#2);
- the lost xlsx sheets (#1).

I can't read the Codex 5-hour window share from here: the CLI reported no usage before it
refused the call.
