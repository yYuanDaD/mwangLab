"""Build data/GSE144109/GSE144109_metadata.csv from the family SOFT downloaded manually.

download_geo_data failed here (GEOparse temp-file error + ftp.ncbi.nlm.nih.gov 403);
the SOFT was fetched from the ftp.ncbi.nih.gov mirror. Same output as
tools/geo_tools.py:35-36 (gse.phenotype_data.to_csv).
Usage: python -I prep_metadata.py <family.soft.gz> <out.csv>
"""
import sys
import GEOparse

gse = GEOparse.get_GEO(filepath=sys.argv[1], silent=True)
gse.phenotype_data.to_csv(sys.argv[2])
print(gse.phenotype_data.shape)
