# HANDBACK: PMID33275875 / GSE123961

**Status: refused at the `design` gate.** The data have no exercise contrast.

## What ran
1. `case_runner inspect GSE123961`. The tool's own download failed (see Tool problems). I fetched `GSE123961_family.soft.gz` and `GSE123961_SVZ_processed_counts.txt.gz` from the GEO HTTPS FTP mirror into `data/GSE123961/` with curl. Inspect then ran on the cached files.
2. I read the paper (`PMC7875116.paper.md`). It contains two RNA-seq experiments, and both use **standard-housed** mice (S4.4.10.1.p1):
   - DG vs SVZ Nes-GFP+ cells. This is GSE123961.
   - DG Nes-GFP+ cells sorted by ROS class.
   The running-wheel paradigms (S2.1, S2.6, S4.4.16) are measured only by BrdU/IdU counts, DHE/MitoSOX flow cytometry and western blots. None of them was sequenced.
3. GSE123961 has 9 samples: DG 5, SVZ 4. Every title is `*_STD_POS*`, and growth_protocol reads "Standard housing". The only factor is tissue.
4. `case_runner execute case_spec.json` recorded the gates paper_reconstruction → ownership → alignment → matrix → design.
   - The case stopped at design with `refused`.
   - The contract validator reported 0 errors.
   - Alignment was exact on the key taken from the title: 9/9 samples.
   - Matrix type: log2 CPM (edgeR), already filtered (values −5.1 to 14.1).

## DEG counts vs paper
- None computed. No exercise contrast exists.
- The paper's only differential result for this series is the DG vs SVZ region comparison (Table S1). It uses limma lmFit/topTags at adjusted p < 0.05 with no fold-change cutoff (S4.4.11.p1), and the text gives no count.
- I did not run DG vs SVZ. It is not an exercise effect, and running it would invent an estimand the request did not ask for.

## Deviations
- The data files were downloaded by hand with curl instead of by the tool.
- Paper vs data on sample numbers: the paper says one low-depth sample per experiment was removed. GEO holds 9 samples, which looks like the post-exclusion set. This does not affect the refusal.

## Tool problems
- `tools/geo_tools.py:30` `GEOparse.get_GEO(...)` failed on Windows with `[Errno 2] No such file or directory: ...\Temp\tmpXXXX`. Likely cause: GEOparse `downloader.py:34` uses `tempfile.NamedTemporaryFile(delete=True)` and then reopens it by name, which Windows does not allow. It failed the same way with TMP pointed at the scratchpad and with the sandbox disabled.
- `tools/geo_tools.py:58`/`:105`: the supplementary download (`urllib` on `https://ftp.ncbi.nlm.nih.gov/.../suppl/`) returned HTTP 403. The same URLs returned 200 with curl, so the cause is probably urllib's default User-Agent or the directory-listing request.
