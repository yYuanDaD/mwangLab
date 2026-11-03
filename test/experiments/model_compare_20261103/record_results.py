"""Write results.csv from the Agent results of each run, plus the Opus figures from runs_claude/progress.csv."""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROWS = [
    ("sonnet", "PMID41835150", "GSE319603", 295662, 149472, 20, "claude-sonnet-5-5",
     "STATUS: finished",
     "VS_PAPER: 2/2 contrasts, paper threshold padj<0.05 & |log2FC|>=0.5; HM vs H (exercise) 534 (191/343) vs paper 563 (213/350); H vs C 476 vs 458",
     "PROBLEMS: none"),
    ("sonnet", "PMID39393048", "GSE267512", 236612, 107687, 16, "claude-sonnet-5-5",
     "STATUS: finished",
     "VS_PAPER: 1/1 contrast POST vs PRE (DESeq2 ~subject+time, FDR<0.05, no LFC cutoff); DEGs 218 (126 up/92 down) vs paper 214 (122/92); 57 of 62 samples deposited",
     "PROBLEMS: none"),
    ("sonnet", "b06f79d81bb9463e3b902b4b8b96b865e96758a2", "GSE164890", 385255, 145859, 30, "claude-sonnet-5-5",
     "STATUS: finished",
     "VS_PAPER: 1/1 contrast (after vs before, ~subject+ex); DEGs 2588 up/1655 down (4243) vs paper 2516/1542 (4058), padj<0.1 no FC cutoff",
     "PROBLEMS: deseq2_tools.py:194 summary text hardcodes padj<0.05 & |lfc|>1 regardless of alpha; joint_contrasts.py:71 treats numeric subject as continuous"),
    ("sonnet", "PMID34142717", "GSE178262", 339765, 149705, 23, "claude-sonnet-5-5",
     "STATUS: finished",
     "VS_PAPER: 6/6 planned contrasts; wheel DEGs 2430/258 vs paper 2094/368 (FDR<=0.05); treadmill 677-2192, paper gives no counts in text; Venn overlap 28-30% vs ~25%",
     "PROBLEMS: Entrez-keyed matrix blocks gene lookups and enrichment; inspect misses the two-lanes-per-sample structure (prep script needed); benign pydeseq2 str-index warning"),
    ("sonnet", "PMID34358431", "GSE174785", 149082, 123070, 21, "claude-sonnet-5-5",
     "STATUS: refused",
     "VS_PAPER: Refused at design: GSE174785 is soleus vs EDL ECs x WT/Atf4-KO, no exercise arm; paper's 782 DEGs (padj<0.05, logFC>1) are a muscle-bed contrast, not run",
     "PROBLEMS: none blocking; align_to_metadata (tools/native.py:287) needed a derived key because matrix columns are GSM_label; merged tar matrix is transcript-level"),
    ("sonnet", "PMID42679010", "GSE344550", 104155, 119954, 18, "claude-sonnet-5-5",
     "STATUS: refused",
     "VS_PAPER: 0/0 contrasts run; refused at design (no exercise factor; macrophage infection by C. parapsilosis BP/LBP). Paper: edgeR |log2FC|>1, no DEG counts in text",
     "PROBLEMS: tools/case_runner.py:993 crashes with raw JSONDecodeError traceback on an invalid spec instead of spec_error; otherwise none"),
]
OPUS = [
    ("PMID41835150", "GSE319603", 4.2, 121050, "finished"),
    ("PMID39393048", "GSE267512", 6.8, 128886, "finished"),
    ("b06f79d81bb9463e3b902b4b8b96b865e96758a2", "GSE164890", 4.3, 122787, "finished"),
    ("PMID34142717", "GSE178262", 10.6, 164653, "finished"),
    ("PMID34358431", "GSE174785", 3.1, 110114, "refused"),
    ("PMID42679010", "GSE344550", 3.1, 104955, "refused"),
]
with open(HERE / "results.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["model", "paper_id", "gse", "wall_minutes", "total_tokens", "tool_uses", "actual_model", "status", "vs_paper", "problems"])
    for m, pid, gse, ms, tok, uses, actual, *reply in ROWS:
        w.writerow([m, pid, gse, round(ms / 60000, 2), tok, uses, actual, *reply])
    for pid, gse, minutes, tok, status in OPUS:
        w.writerow(["opus_reference", pid, gse, minutes, tok, "", "", f"STATUS: {status}", "see runs_claude/progress.csv", ""])
