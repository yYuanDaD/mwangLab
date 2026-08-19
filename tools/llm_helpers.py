"""LLM fallback utilities for the batch pipeline.

Two fallback hooks:

1. Contrast validation (`validate_contrast_with_llm`) — given a Python heuristic's
   pick (or absence of pick) for (design_column, control_value, treatment_value),
   let Claude double-check it against the user's stated intent and the actual
   metadata content. Catches silent bugs where keyword matching technically
   succeeds but picked the wrong column or wrong values.

2. Sample alignment fallback (`align_samples_with_llm_fallback`) — wraps
   `tools.sample_align.align_samples`. When all three string-based strategies
   (exact / substring / token-overlap) fail, asks Claude to decode the
   abbreviation pattern between counts column names and metadata sample IDs
   (e.g. 'HC_F1_TL_S54_L003' <-> 'HomeCage1_Female1_TotalLysate'). Result is
   validated against the input lists before being accepted.
"""

import json
import math
from typing import Optional

import pandas as pd
from pydantic import BaseModel, Field

from tools.model_factory import create_structured_chat_model


class ContrastValidationResult(BaseModel):
    """LLM response schema for contrast validation."""
    is_valid: bool = Field(
        description="True ONLY when you are confirming the Python heuristic's proposed pick unchanged. "
                    "False when you are replacing it, proposing one where none was given, or no clean "
                    "contrast exists. (The actual contrast to use is always in the three fields below.)"
    )
    design_column: Optional[str] = Field(
        default=None,
        description="The metadata column of your RECOMMENDED contrast. ALWAYS fill this whenever a clean "
                    "2-group split exists — whether confirming, replacing, or proposing one where none was "
                    "given. Null ONLY when no clean contrast exists.",
    )
    control_value: Optional[str] = Field(
        default=None,
        description="Control group value of the recommended contrast (must appear verbatim in that column's "
                    "unique values). ALWAYS fill when a clean contrast exists; null only when none exists.",
    )
    treatment_value: Optional[str] = Field(
        default=None,
        description="Treatment group value of the recommended contrast (must appear verbatim in that column's "
                    "unique values). ALWAYS fill when a clean contrast exists; null only when none exists.",
    )
    reasoning: str = Field(
        description="One or two sentences explaining the decision."
    )


def _get_validation_llm():
    """Configured provider, or None when its API key is unavailable."""
    return create_structured_chat_model(required=False)


class RawDAMethodChoice(BaseModel):
    """LLM choice of DA method for a raw-counts study (mentor's matrix: any of three)."""
    method: str = Field(description="exactly one of: 'deseq2', 'edger', 'limma-voom'")
    reasoning: str = Field(
        description="1-2 sentences justifying the pick RELATIVE TO THE OTHER TWO methods — i.e. "
                    "why this one is preferable here over DESeq2/edgeR/limma-voom specifically, not "
                    "just why it is valid. Reference the concrete study facts (n per group, etc.)."
    )


def choose_raw_da_method_with_llm(
    accession: str,
    n_samples: Optional[int],
    organism: str = "",
    notes: str = "",
) -> Optional[RawDAMethodChoice]:
    """Ask Claude to pick a raw-counts DA method (deseq2 / edger / limma-voom).

    Returns None if the LLM is unavailable or the call fails — caller defaults to deseq2.
    All three are valid for raw integer counts (the mentor's matrix); the choice is a soft
    preference, recorded in analysis.da_method for provenance.
    """
    llm = _get_validation_llm()
    if llm is None:
        return None
    structured_llm = llm.with_structured_output(RawDAMethodChoice)
    prompt = f"""Pick ONE differential-expression method for a RAW-count RNA-seq study.

Study: {accession} | organism: {organism or 'unknown'} | total samples: {n_samples if n_samples is not None else 'unknown'}
{f'Notes: {notes}' if notes else ''}

All three are valid for raw integer counts. Choose with these guidelines:
- 'deseq2'     — robust default; negative-binomial with strong per-gene shrinkage; great for SMALL n
                 (2-4/group); conservative LFC estimates; the safe pick when unsure.
- 'edger'      — negative-binomial GLM + quasi-likelihood F-test; small n ok; tends to call slightly
                 MORE genes than DESeq2 at the same cutoff; pick it for an NB cross-check of DESeq2 or
                 when you want edgeR's QL error-rate control.
- 'limma-voom' — observation-level precision weights from a mean-variance trend; shines with LARGER n
                 and UNEVEN library sizes (roughly >=4-5 samples/group); most flexible for complex
                 designs; can be conservative / underpowered on tiny noisy datasets.

In `reasoning`, explain WHY the chosen method beats the OTHER TWO for THIS study specifically
(cite n-per-group / library-size evenness / design complexity) — e.g. "edgeR over DESeq2 because ...,
and over limma-voom because n is too small for stable voom weights."
Return exactly one of 'deseq2' / 'edger' / 'limma-voom'.
"""
    try:
        res = structured_llm.invoke(prompt)
        res.method = (res.method or "").lower().strip()
        return res
    except Exception as e:
        print(f"  [da-method-select] call failed: {type(e).__name__}: {e}")
        return None


def choose_raw_da_method_rule(n_samples: Optional[int] = None) -> tuple[str, str]:
    """Deterministic, zero-cost counterpart to `choose_raw_da_method_with_llm` (meeting req #1).

    For RAW integer counts all three methods (DESeq2 / edgeR / limma-voom) are valid; DESeq2 is
    the robust negative-binomial default and — given only the total n, which is all the LLM picker
    sees — the LLM almost never deviates from it. So we pick by rule and skip the per-study LLM
    call. edgeR / limma-voom remain selectable explicitly via `raw_da_method=`; per-study LLM
    deliberation is still available via `raw_da_method='auto-llm'`.

    Returns (method, reason). No network, no tokens, no failure mode.
    """
    reason = (
        "rule-based default for raw counts: DESeq2 (robust negative-binomial with per-gene "
        "shrinkage; the standard for integer counts, strong at small n). Per-study LLM "
        "method-picker skipped to cut cost (req #1); pass raw_da_method='auto-llm' to restore it, "
        "or name a method explicitly (edger / limma-voom)."
    )
    return "deseq2", reason


class MatrixTypeClassification(BaseModel):
    """LLM decision on what KIND of expression matrix a file holds (req #1: use the LLM to
    determine the data type, then derive the DA method). The heuristic `_classify_matrix` is
    fast but has an explicit 'ambiguous' bucket, a brittle FPKM-vs-log decimal boundary, and NO
    concept of proteomics intensities or methylation β — this fills those gaps."""
    matrix_type: str = Field(
        description="EXACTLY one of: "
                    "'raw_counts' (integer read counts, wide range, no decimals/negatives → DESeq2/edgeR/voom); "
                    "'fpkm_or_tpm' (LINEAR normalized expression — decimals, wide dynamic range, housekeeping "
                    "genes in the thousands → log2 then limma); "
                    "'log_transformed' (ALREADY log-scale expression: log2(CPM+1)/log-FPKM/vst/rlog, small max "
                    "~<30, may have negatives → limma as-is); "
                    "'proteomics_intensity' (mass-spec protein/peptide abundances, LFQ/TMT/DIA → limma); "
                    "'methylation_beta' (DNA-methylation β fractions in [0,1] or 0-100%, sites×samples → β→M→limma); "
                    "or 'ambiguous' (genuinely cannot tell)."
    )
    already_log_scale: bool = Field(
        description="True iff the values are ALREADY on a log scale (no further log2 needed before limma). "
                    "raw_counts/fpkm_or_tpm/methylation_beta → typically False; log_transformed → True; "
                    "log-scale proteomics intensities → True."
    )
    confidence: str = Field(description="'high' / 'medium' / 'low' — only high/medium are acted on.")
    reasoning: str = Field(
        description="1-2 sentences citing the CONCRETE evidence (value range, integer-ness, sign, fraction in "
                    "[0,1], filename, platform) that fixes the type and rules out the nearest neighbor."
    )


def classify_matrix_with_llm(
    filename: str,
    platform: str,
    value_stats: dict,
    preview_text: str,
    heuristic_label: str,
    organism: str = "",
) -> Optional[MatrixTypeClassification]:
    """Ask Claude what kind of expression matrix this is, given a compact numeric profile +
    a small text preview + the filename/platform hints + the heuristic's own guess.

    Returns None if the LLM is unavailable or the call fails — caller keeps the heuristic answer
    (fail-soft, never blocks).
    """
    llm = _get_validation_llm()
    if llm is None:
        return None
    structured_llm = llm.with_structured_output(MatrixTypeClassification)
    prompt = f"""Classify the DATA TYPE of one expression matrix so the right differential-analysis
method can be picked. This is a {organism or 'unknown-organism'} omics study.

File: {filename}
Platform / assay hints (from GEO metadata): {platform or 'none'}
Fast heuristic's guess (may be wrong on the FPKM-vs-log boundary, and is BLIND to proteomics &
methylation): {heuristic_label!r}

Numeric profile of the matrix (sampled rows):
{json.dumps(value_stats, indent=2, ensure_ascii=False)}

Text preview (first rows x first columns):
{preview_text}

Decide the single best `matrix_type`. Discriminators:
- raw_counts: frac_integer_of_nonzero ~1.0, no negatives, large max (hundreds–millions). Row IDs are genes.
- fpkm_or_tpm: decimals present, NON-negative, wide range (housekeeping genes can exceed 10,000), NOT log.
- log_transformed: small max (typically < ~30), decimals, MAY contain negatives (vst/rlog/centered).
- proteomics_intensity: filename/platform mention LFQ/TMT/DIA/MaxQuant/proteome/intensity; rows are
  proteins/peptides (UniProt-like IDs). Set already_log_scale by whether values look logged (small max).
- methylation_beta: ~all values within [0,1] (frac_in_0_1 ≈ 1.0) or 0-100%; rows are CpG sites/probes
  (cgNNNNNN / chr:pos); platform mentions 450K/EPIC/RRBS/WGBS/bisulfite/methylation.

Use the filename and platform hints heavily — they disambiguate proteomics & methylation, which the
numeric profile alone can resemble (β looks like a small-max log matrix). If you truly cannot tell,
return 'ambiguous' with low confidence. Report your decision via the structured schema.
"""
    try:
        res = structured_llm.invoke(prompt)
        res.matrix_type = (res.matrix_type or "").lower().strip()
        res.confidence = (res.confidence or "").lower().strip()
        return res
    except Exception as e:
        print(f"  [datatype-llm] call failed: {type(e).__name__}: {e}")
        return None


def summarize_metadata_for_llm(metadata_csv: str, max_cols: int = 15) -> dict:
    """Compact JSON-friendly view of a metadata CSV for LLM consumption.

    Keeps only columns whose names look design-related and that have 2..12
    unique values, with per-value sample counts.
    """
    try:
        df = pd.read_csv(metadata_csv, index_col=0)
    except Exception:
        return {}
    name_hints = (
        "characteristics", "title", "source", "treatment", "group", "condition",
        "phenotype", "agent", "stimulus", "tissue", "diet", "genotype",
        "intervention", "exposure",
    )
    summary: dict = {}
    for col in df.columns:
        col_low = str(col).lower()
        if not any(h in col_low for h in name_hints):
            continue
        vals = df[col].dropna().astype(str)
        unique = vals.unique().tolist()
        if not (2 <= len(unique) <= 12):
            continue
        counts = vals.value_counts().to_dict()
        summary[str(col)] = {
            "unique_values": unique,
            "counts": {str(k): int(v) for k, v in counts.items()},
        }
        if len(summary) >= max_cols:
            break
    return summary


def validate_contrast_with_llm(
    accession: str,
    metadata_columns_summary: dict,
    treatment_keywords: list[str],
    control_keywords: list[str],
    proposed: Optional[tuple[str, str, str]],
) -> Optional[ContrastValidationResult]:
    """Ask Claude to validate or replace a control-vs-treatment pick.

    Returns None if the LLM is unavailable or the call fails — caller should
    fall back to the Python heuristic's original answer in that case.
    """
    if not metadata_columns_summary:
        return None
    llm = _get_validation_llm()
    if llm is None:
        return None

    structured_llm = llm.with_structured_output(ContrastValidationResult)

    if proposed is not None:
        proposed_str = (
            f"Python heuristic picked:\n"
            f"  design_column = {proposed[0]!r}\n"
            f"  control_value = {proposed[1]!r}\n"
            f"  treatment_value = {proposed[2]!r}"
        )
    else:
        proposed_str = "Python heuristic found NO clean contrast."

    prompt = f"""You are validating a control-vs-treatment contrast for RNA-seq differential expression analysis.

Study: {accession}
User intent — control keywords: {control_keywords}
User intent — treatment keywords: {treatment_keywords}

{proposed_str}

Candidate metadata columns and their unique values (with per-value sample counts):
{json.dumps(metadata_columns_summary, indent=2, ensure_ascii=False)}

Your job:
1. If a contrast was proposed above, decide whether it is biologically sensible for the user's intent.
   If NO contrast was proposed (the Python heuristic found none), find the best 2-group contrast yourself.
2. Common failure modes to catch:
   - Wrong column type (e.g. picked 'genotype' when 'treatment' would be cleaner)
   - Wrong values (e.g. picked 'untreated' as control when the real control is 'baseline')
   - Ambiguous values (e.g. 'sedentary control' counted as both — could pollute either group)
   - Multi-factor / time-course design: pick the single 2-group pair that best answers the user's
     intent (e.g. baseline/pre vs the primary treated/post group). Do NOT give up just because a
     column has more than two values — choose the most meaningful pair from it.
3. ALWAYS report your recommended contrast in design_column / control_value / treatment_value whenever
   a clean 2-group split exists — whether you are confirming the proposed pick, replacing it, or
   proposing one where none was given. The values MUST appear verbatim in that column's unique_values.
4. Set is_valid=true ONLY when you are confirming the proposed pick unchanged. Set is_valid=false when
   you are replacing it, or when no pick was proposed and you are proposing a new one.
5. If no column has a clean 2-group split that matches the user's intent, set is_valid=false and leave
   all three fields null.
6. Prefer columns where both groups have at least 3 samples (DESeq2 needs replicates).

Return your decision via the structured schema.
"""
    try:
        return structured_llm.invoke(prompt)
    except Exception as e:
        print(f"  [llm-validation] call failed: {type(e).__name__}: {e}")
        return None


class SampleAlignmentResult(BaseModel):
    """LLM response schema for sample-name alignment."""
    mapping: dict[str, str] = Field(
        description="Mapping from metadata sample ID (key) to counts column name (value). "
                    "Each counts column appears AT MOST ONCE across all values. "
                    "Skip pairs you are not confident about — partial mappings are fine. "
                    "Values MUST come verbatim from the provided counts columns list (no edits, no fabrication)."
    )
    reasoning: str = Field(
        description="One or two sentences describing the abbreviation/naming pattern you decoded "
                    "(e.g. 'HC=HomeCage, F=Female, TL=TotalLysate; trailing _Snn_Lnnn are sequencer lane suffixes')."
    )


class EvaluationJudgeResult(BaseModel):
    """LLM response schema for repeated subset/rerun evaluation."""
    verdict: str = Field(description="Exactly one of: stable, mixed, unstable.")
    confidence: str = Field(description="Exactly one of: high, medium, low.")
    reasoning: str = Field(
        description="Two or three sentences explaining whether the repeated subset/rerun outputs "
                    "support the same biological interpretation. Mention both ranking stability "
                    "(correlations) and threshold sensitivity (Jaccard overlap) when available."
    )
    recommended_action: str = Field(
        description="One concise next step, e.g. accept result, report as sensitivity-qualified, "
                    "increase sample size, relax threshold, or manually inspect discordant genes/pathways."
    )


def judge_evaluation_with_llm(summary: dict) -> Optional[EvaluationJudgeResult]:
    """Ask a separate structured LLM judge to interpret repeated-run stability metrics.

    Returns None if the LLM is unavailable or the call fails; callers should fall back to
    deterministic thresholds. This hook intentionally consumes only numeric summaries, not
    raw matrices or paper text, so it is cheap and avoids leaking irrelevant context into the
    verdict.
    """
    llm = _get_validation_llm()
    if llm is None:
        return None
    structured_llm = llm.with_structured_output(EvaluationJudgeResult)
    prompt = f"""You are an independent evaluation judge for a bioinformatics AI pipeline.

The same study/contrast was run multiple times, typically on sample subsets or repeated
pipeline runs. Interpret the stability metrics below.

Guidelines:
- High log2FC / NES Pearson correlations mean the ranked biological signal is stable.
- Significant-gene/pathway Jaccard can be lower because FDR thresholds are brittle; do not
  over-penalize low Jaccard if correlations are high and significant counts are small.
- Call "stable" only when the same broad biological story is supported.
- Call "mixed" when rankings are stable but thresholded discoveries vary, or DEG and GSEA
  disagree in stability.
- Call "unstable" when correlations and overlaps are both poor.

Metrics:
{json.dumps(summary, indent=2, ensure_ascii=False)}

Return the structured verdict.
"""
    try:
        res = structured_llm.invoke(prompt)
        res.verdict = (res.verdict or "").lower().strip()
        res.confidence = (res.confidence or "").lower().strip()
        if res.verdict not in {"stable", "mixed", "unstable"}:
            res.verdict = "mixed"
        if res.confidence not in {"high", "medium", "low"}:
            res.confidence = "low"
        return res
    except Exception as e:
        print(f"  [evaluation-judge] call failed: {type(e).__name__}: {e}")
        return None


def _summarize_metadata_for_alignment(metadata_df: pd.DataFrame, max_cols: int = 8) -> dict:
    """Build a {sample_id: {col: value, ...}} dict for LLM alignment input.

    Picks descriptive columns (title / source / characteristics / geo_accession);
    falls back to the first `max_cols` columns if none of the hints match.
    """
    name_hints = ("title", "source", "characteristics", "geo_accession",
                  "description", "label", "sample_name")
    cols = [c for c in metadata_df.columns if any(h in str(c).lower() for h in name_hints)]
    if not cols:
        cols = list(metadata_df.columns)[:max_cols]
    else:
        cols = cols[:max_cols]
    sub = metadata_df[cols].astype(str)
    return {str(idx): {str(c): sub.at[idx, c] for c in cols} for idx in sub.index}


def _llm_align_samples(counts_cols: list[str], metadata_df: pd.DataFrame) -> dict[str, str]:
    """Ask Claude to map metadata sample IDs to counts columns. Returns {} on
    any failure — caller falls back to 'no_match'."""
    llm = _get_validation_llm()
    if llm is None:
        return {}
    meta_compact = _summarize_metadata_for_alignment(metadata_df)
    if not meta_compact:
        return {}

    structured_llm = llm.with_structured_output(SampleAlignmentResult)
    prompt = f"""You are aligning RNA-seq counts matrix columns to GEO metadata sample IDs.

String-based alignment (exact / substring / token-overlap) already failed. The likely cause is that
counts columns use abbreviations or sequencer-pipeline-generated names while metadata uses full words.

Counts matrix columns ({len(counts_cols)} total):
{json.dumps(counts_cols, ensure_ascii=False)}

Metadata samples (sample_id -> descriptive columns):
{json.dumps(meta_compact, indent=2, ensure_ascii=False)}

Your job: produce a mapping {{metadata_sample_id -> counts_column}}.

Common patterns to decode:
- Abbreviations: HC=HomeCage, F1=Female1, TL=TotalLysate, KO=Knockout, WT=WildType, IP=Immunoprecipitation, etc.
- Trailing sequencer suffixes: _S54, _L003, _R1, _001 — these encode lane/sample-sheet position and should be ignored
- Sample numbering: rep1/rep2 vs _1/_2 vs _A/_B
- Counts may use the GSM accession directly while metadata index is a custom label, or vice versa

Rules:
- Each counts column appears AT MOST ONCE in your mapping (one-to-one only)
- Skip pairs you are uncertain about — a partial high-confidence mapping beats a complete low-confidence one
- The values in your mapping MUST come verbatim from the counts column list above (no string edits)
- Provide a short reasoning describing the abbreviation pattern you used
"""
    try:
        result = structured_llm.invoke(prompt)
        print(f"  [llm-align] proposed {len(result.mapping)} pairs | {result.reasoning}")
        return result.mapping
    except Exception as e:
        print(f"  [llm-align] call failed: {type(e).__name__}: {e}")
        return {}


def align_samples_with_llm_fallback(counts_cols, metadata_df,
                                    min_match_fraction: float = 0.5,
                                    token_threshold: int = 3):
    """Drop-in replacement for `tools.sample_align.align_samples` that adds an
    LLM-mediated 4th strategy when the 3 string-based strategies all fail.

    Same return contract: (mapping, method_str). `method_str` will be 'llm
    (k/n)' when LLM fallback succeeds, or 'no_match' / 'no_match_llm_too_few'
    when it does not.
    """
    from tools.sample_align import align_samples
    mapping, method = align_samples(counts_cols, metadata_df, min_match_fraction, token_threshold)
    if method != "no_match":
        return mapping, method

    counts_cols = list(counts_cols)
    raw = _llm_align_samples(counts_cols, metadata_df)
    if not raw:
        return {}, "no_match"

    valid = {}
    used_counts = set()
    counts_set = set(counts_cols)
    meta_idx_set = set(str(x) for x in metadata_df.index)
    dropped = 0
    for meta_id, counts_col in raw.items():
        meta_id, counts_col = str(meta_id), str(counts_col)
        if meta_id not in meta_idx_set:
            dropped += 1; continue
        if counts_col not in counts_set:
            dropped += 1; continue
        if counts_col in used_counts:
            dropped += 1; continue
        valid[meta_id] = counts_col
        used_counts.add(counts_col)
    if dropped:
        print(f"  [llm-align] dropped {dropped} invalid pairs (unknown id/col or duplicate)")

    # Require coverage of the smaller side, not merely survival of whatever tiny
    # subset the LLM chose to propose. This still accepts a six-sample metadata
    # table matched against a matrix with extra numeric statistic columns
    # (target=min(13, 6)=6), while rejecting a misleading 2/20 proposal.
    target_n = min(len(counts_cols), len(meta_idx_set))
    required_n = max(1, int(math.ceil(target_n * min_match_fraction)))
    if len(valid) >= required_n:
        return valid, f"llm ({len(valid)}/{target_n})"
    return {}, f"no_match_llm_too_few ({len(valid)}/{target_n}; required={required_n})"
