import os
import GEOparse
from langchain_core.tools import tool
import requests
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd


@tool
def download_geo_data(geo_accession: str, base_dir: str = "./data") -> str:
    """Download GEO metadata for a given accession."""
    save_dir = os.path.join(base_dir, geo_accession)
    os.makedirs(save_dir, exist_ok=True)
    metadata_path = os.path.join(save_dir, f"{geo_accession}_metadata.csv")

    # skip-if-exists: once the metadata CSV is on disk, the SOFT download + parse + re-write are all
    # redundant on a repeated cohort run. Delete the file (or run clean.py) to force a refresh.
    if os.path.exists(metadata_path) and os.path.getsize(metadata_path) > 0:
        try:
            n = max(0, sum(1 for _ in open(metadata_path, encoding="utf-8", errors="ignore")) - 1)
        except Exception:
            n = -1
        return f"Metadata already present at {metadata_path} (skipped re-download). It has {n} samples."

    try:
        print(f"Downloading GEO data for {geo_accession}...")
        gse = GEOparse.get_GEO(geo=geo_accession, destdir=save_dir, silent=True)

        # Pull phenotype_data directly — bypasses the GEO probe matrix, which we
        # don't want and which can be huge/malformed for some series.
        if hasattr(gse, "phenotype_data") and not gse.phenotype_data.empty:
            metadata_df = gse.phenotype_data
            metadata_df.to_csv(metadata_path)
            return f"Successfully downloaded metadata to {metadata_path}. It has {len(metadata_df)} samples."
        else:
            return f"Warning: Downloaded {geo_accession}, but no metadata/phenotype_data was found in the GEO object."

    except Exception as e:
        return f"Failed to download GEO metadata. Error: {str(e)}"
    
    
    
@tool
def download_supplementary_files(geo_accession: str, base_dir: str = "./data") -> str:
    """
    Specifically designed to download supplementary files from GEO projects.
    When raw Count matrices for RNA-Seq (like Excel or TXT formats) are needed, this tool must be called.
    It automatically converts downloaded Excel files to standard CSV format.
    """
    target_dir = os.path.join(base_dir, geo_accession)
    os.makedirs(target_dir, exist_ok=True)

    # GEO FTP layout: GSE266241 lives under GSE266nnn/.
    prefix = geo_accession[:-3] + "nnn"
    ftp_url = f"https://ftp.ncbi.nlm.nih.gov/geo/series/{prefix}/{geo_accession}/suppl/"

    try:
        response = requests.get(ftp_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        downloaded_files = []
        converted_files = []
        skipped_files = []

        for link in soup.find_all("a"):
            href = link.get("href")
            if href and href.startswith(geo_accession):
                file_url = ftp_url + href
                file_path = os.path.join(target_dir, href)
                # skip-if-exists: a repeated cohort run must not re-download (matrices can be
                # 100s of MB). An .xlsx is deleted after conversion, so its .csv sibling counts.
                csv_sibling = file_path.rsplit(".", 1)[0] + ".csv"
                if os.path.exists(file_path) or (
                        file_path.endswith((".xlsx", ".xls")) and os.path.exists(csv_sibling)):
                    skipped_files.append(file_path)
                    continue

                urllib.request.urlretrieve(file_url, file_path)
                downloaded_files.append(file_path)

                if file_path.endswith(".xlsx") or file_path.endswith(".xls"):
                    try:
                        df = pd.read_excel(file_path)
                        csv_path = file_path.rsplit(".", 1)[0] + ".csv"
                        df.to_csv(csv_path, index=False)
                        converted_files.append(csv_path)
                        os.remove(file_path)
                    except Exception:
                        pass

        if not downloaded_files and not skipped_files:
            return f"Target {geo_accession} has no supplementary files provided."

        res_str = (f"Supplementary files ready in {target_dir}: "
                   f"{len(downloaded_files)} downloaded, {len(skipped_files)} already present (skipped).\n")
        if converted_files:
            res_str += f"Automatically converted {len(converted_files)} Excel files to CSV format for downstream use:\n"
            res_str += "\n".join(converted_files)

        return res_str

    except Exception as e:
        return f"Failed to download supplementary files. Error: {str(e)}"


_EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
_ORGANISM_TAXA = {"Mouse": "Mus musculus", "Human": "Homo sapiens"}


@tool
def search_geo_studies(
    keyword: str,
    organism: str = "Mouse",
    min_samples: int = 6,
    max_samples: int = 200,
    max_results: int = 50,
    output_dir: str = "./output",
) -> str:
    """
    Search GEO via NCBI E-utilities for RNA-seq series matching a keyword, with hard
    filters on organism, study type, and sample-size range. Returns a curated list
    suitable for batch analysis triage — does NOT download any data.

    Args:
        keyword: Free-text search term (e.g. 'Exercise', 'ischemia spinal cord').
                 Goes into the [All Fields] slot of an Entrez query.
        organism: 'Mouse', 'Human', or 'Any'. 'Any' skips the organism filter.
        min_samples: Minimum sample count (inclusive). Studies with fewer samples
                     usually can't support DESeq2 (need at least 3 per group).
        max_samples: Maximum sample count (inclusive). Very large studies are slow
                     to process and often heterogeneous.
        max_results: Cap on the number of UIDs to summarise. NCBI rate-limit friendly
                     up to a few hundred.
        output_dir: Directory where the result CSV is written.
    """
    try:
        if organism not in ("Mouse", "Human", "Any"):
            return f"Error: organism must be 'Mouse', 'Human', or 'Any', got '{organism}'."

        term_parts = [
            f'"{keyword}"[All Fields]',
            '"expression profiling by high throughput sequencing"[DataSet Type]',
            'gse[Entry Type]',
            f'"{min_samples}"[Number of Samples] : "{max_samples}"[Number of Samples]',
        ]
        if organism != "Any":
            term_parts.append(f'"{_ORGANISM_TAXA[organism]}"[Organism]')
        term = " AND ".join(term_parts)

        common = {"tool": "mwangLab-agent", "retmode": "json"}
        print(f"Searching GEO: {term}")
        r = requests.get(
            f"{_EUTILS}/esearch.fcgi",
            params={**common, "db": "gds", "term": term, "retmax": max_results},
            timeout=30,
        )
        r.raise_for_status()
        ids = r.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return f"No GEO series match '{keyword}' with organism={organism}, samples in [{min_samples}, {max_samples}]."

        print(f"Fetching summaries for {len(ids)} candidate UIDs...")
        r = requests.get(
            f"{_EUTILS}/esummary.fcgi",
            params={**common, "db": "gds", "id": ",".join(ids)},
            timeout=60,
        )
        r.raise_for_status()
        result = r.json().get("result", {})
        uids = result.get("uids", [])

        rows = []
        for uid in uids:
            rec = result.get(uid, {})
            # esummary on gds returns GSM/GPL too despite our entry-type filter; double-check here.
            if rec.get("entrytype") != "GSE":
                continue
            supp = rec.get("suppfile") or ""  # comma-separated extensions, e.g. "CSV,TXT"
            rows.append({
                "accession": rec.get("accession", ""),
                "title": rec.get("title", "").strip(),
                "organism": rec.get("taxon", ""),
                "n_samples": int(rec.get("n_samples", 0) or 0),
                "gdsType": rec.get("gdsType", ""),
                "pubmed_id": ";".join(str(x) for x in (rec.get("pubmedids") or [])),
                "supp_file_types": supp,
                "has_counts_like_supp": any(
                    ext.lower() in supp.lower() for ext in ("CSV", "TXT", "TSV", "XLSX", "TAB")
                ),
                "summary": rec.get("summary", "").strip()[:400],
            })

        if not rows:
            return f"Search returned {len(ids)} UIDs but none were GSE entries after filtering."

        rows.sort(key=lambda d: (not d["has_counts_like_supp"], -d["n_samples"]))

        os.makedirs(output_dir, exist_ok=True)
        safe_kw = "".join(c if c.isalnum() else "_" for c in keyword).strip("_")
        out_path = os.path.join(output_dir, f"geo_search_{safe_kw}.csv")
        pd.DataFrame(rows).to_csv(out_path, index=False)

        n_with_counts = sum(1 for r in rows if r["has_counts_like_supp"])
        lines = [
            f"Found {len(rows)} GEO series matching '{keyword}' "
            f"(organism={organism}, samples in [{min_samples}, {max_samples}]).",
            f"{n_with_counts}/{len(rows)} have supplementary files in counts-friendly formats "
            f"(CSV/TXT/TSV/XLSX) — these are the batch-analysis candidates.",
            "",
            f"### Top {min(10, len(rows))} hits (sorted by has-counts then sample count):",
        ]
        for r in rows[:10]:
            flag = "[counts]" if r["has_counts_like_supp"] else "[no-counts]"
            lines.append(
                f"- {r['accession']} {flag} | n={r['n_samples']} | {r['title'][:90]}"
            )
        lines.append("")
        lines.append(f"Full result table saved to: {out_path}")
        return "\n".join(lines)

    except Exception as e:
        return f"GEO search failed. Error: {type(e).__name__}: {e}"


@tool
def fetch_geo_description(geo_accession: str) -> str:
    """
    Fetch the Summary and Overall Design text from the GEO website for a given accession ID.
    This is useful for understanding the experimental context without manual input.
    """
    url = f"https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc={geo_accession}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        summary_text = ""
        design_text = ""

        cells = soup.find_all("td")
        for i, cell in enumerate(cells):
            if "Summary" in cell.get_text():
                summary_text = cells[i + 1].get_text(strip=True)
            if "Overall design" in cell.get_text():
                design_text = cells[i + 1].get_text(strip=True)

        full_description = f"Project Summary: {summary_text}\n\nOverall Design: {design_text}"
        return full_description if summary_text else "Could not find description on the page."

    except Exception as e:
        return f"Error fetching page: {str(e)}"
