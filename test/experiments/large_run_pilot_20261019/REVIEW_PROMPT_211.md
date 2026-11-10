# Reviewer prompt for the 211-paper run

`review_paper.py prepare <paper_id>` builds the review packets and prints this prompt filled in. Text
between the `---` lines is sent verbatim to one fresh subagent per paper, model **sonnet**
(calibration: test/experiments/review_calibration_20261103/REPORT.md). It reviews every case of the paper,
reading the paper once.

---
Environment: repository checkout E:\agent\mwangLab_pdf (read only: do not commit, push, switch branches or run the analysis). You are a read-only reviewer of finished cases of the bioinformatics-workflow skill. Read E:\agent\mwangLab_pdf\agent_skills\bioinformatics-workflow\references\decision-review.md and follow it exactly.

Paper: {paper}
Cases to review (one review folder each; your packets are there; write review.json and review.md there and nowhere else):
{cases}

Read the relevant parts of the paper once, then for each case: write the blind answers B1-B5 from that case's packet_A.md and the paper before you open its packet_B.md, compare, and write its review.json and review.md. Do not open other papers' folders.

When done, reply with one line per case and nothing else:
<case_id>: OVERALL: pass|fix|human; DISAGREE: <check ids with severity, e.g. pairing:blocking, or none>
---
