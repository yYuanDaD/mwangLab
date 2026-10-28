# Subagent prompt for the 211-paper run

`prompt_for.py <n>` fills this template for row `n` of `queue_211.csv`. Text between the
`---` lines is sent verbatim; `{paper_files}` is one of the two variants below.

---
Environment: repository checkout E:\agent\mwangLab_pdf (do not commit, push or switch branches). Run every command from E:\agent\mwangLab_pdf with E:\agent\mwangLab_pdf\.venv-pdf\Scripts\python.exe and PYTHONIOENCODING=utf-8. GEO data are cached in E:\agent\mwangLab_pdf\data (pass --data-root E:/agent/mwangLab_pdf/data to inspect; download there if missing). {paper_files} Do not open other papers' folders under test\experiments\large_run_pilot_20261019\runs_claude. Give commands that may run longer than 2 minutes a longer timeout.

Task: load the bioinformatics-workflow skill (E:\agent\mwangLab_pdf\.claude\skills\bioinformatics-workflow\SKILL.md) and follow it. Analyze {gse_list} for {paper_ref} ({title}): how exercise affects gene expression as the paper intends. Run directory: test/experiments/large_run_pilot_20261019/runs_claude/{paper_id} (run label {paper_id}). Skip the preflight. You make every scientific decision. If the data do not support an exercise comparison, refuse at the right gate and record why.

When done, write HANDBACK.md in the run directory: what ran, DEG counts vs the paper's (with the paper's threshold), deviations, and tool problems (with file:line where you can). Then reply with exactly three lines and nothing else:
STATUS: finished | refused | failed
VS_PAPER: <one line of at most 200 characters, e.g. "2/2 contrasts; DEGs 120/45 vs paper 130/50">
PROBLEMS: <one line of at most 200 characters naming tool problems, or none>
---

Full text available: `Paper files: E:\agent\mwangLab_pdf\{paper_md} and the .paper.json next to it.`

No full text: `No full text is available for this paper. Read its PubMed abstract (NCBI E-utilities efetch) and the GEO series description, and say in HANDBACK.md that the comparison with the paper rests on the abstract only.`
