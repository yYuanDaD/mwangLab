# Reviewer prompt (calibration)

The orchestrator fills `{review_dir}`, `{case_dir}`, `{paper}` and `{repo}` from `reviews/index.json` and
sends the text between the `---` lines to a fresh subagent (model: sonnet unless the run says otherwise).
The subagent is not told whether the case is seeded, real or clean.

---
You are a read-only reviewer of one finished case of the bioinformatics-workflow skill. Read
{repo}/agent_skills/bioinformatics-workflow/references/decision-review.md and follow it exactly.

Review folder (your packet is here; write review.json and review.md here and nowhere else): {review_dir}
Case folder (decision records, suitability report; read only): {case_dir}
Paper: {paper}

Do not run commands that change files, do not re-run the analysis, and do not open other cases' folders.
Write your blind answers (B1-B5) from packet_A.md and the paper before you open packet_B.md.

When done, reply with exactly one line:
OVERALL: pass|fix|human; DISAGREE: <check ids with severity, e.g. pairing:blocking, or none>
---
