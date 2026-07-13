# test.py
import os, sys
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(_PROJECT_ROOT)
sys.path.insert(0, _PROJECT_ROOT)

# 1. Import tools directly from the tools module
from tools.seacdm_tools import extract_sea_cdm_conditions
from tools.geo_tools import download_geo_data

if __name__ == "__main__":
    print("========================================")
    print("   Agent Tool Chain - Local Unit Test")
    print("========================================\n")

    # ------------------------------------------
    # Test 1: SEA CDM extraction tool
    # ------------------------------------------
    print("Testing [SEA CDM extraction tool]...")

    # Mock input simulating LLM-generated parameters
    mock_sea_cdm_input = {
        "study_id": "GSE266241",
        "study_objective": "Investigate the molecular mechanisms of delayed paraplegia in a mouse spinal cord ischemic injury model.",
        "experiments": [
            {
                "subject_species": "Mus musculus",
                "treatment_group": "ACC 4h (aortic cross-clamping for 4 hours)",
                "control_group": "Sham 4h (sham surgery for 4 hours)",
                "tissue_or_cell": "Spinal Cord (thoracic-lumbar Th-Lu)"
            }
        ],
        "assays": [
            {
                "assay_type": "RNA-Seq",
                "platform": "Illumina NovaSeq 6000"
            }
        ]
    }

    # Execute the tool via .invoke() and capture the result
    try:
        result_1 = extract_sea_cdm_conditions.invoke(mock_sea_cdm_input)
        print(f"[PASS] Result:\n{result_1}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

    # ------------------------------------------
    # Test 2: GEO data download tool
    # ------------------------------------------
    print("\nTesting [GEO data download tool]...")

    # Mock input; using the small GSE12345 dataset to keep test fast
    mock_geo_input = {
        "geo_accession": "GSE12345",
        "output_dir": "./data"
    }

    # Execute the tool via .invoke()
    try:
        result_2 = download_geo_data.invoke(mock_geo_input)
        print(f"[PASS] Result:\n{result_2}")
    except Exception as e:
        print(f"[FAIL] Error: {e}")

    print("\n========================================")
    print("Tests finished! Check the project directory for generated files.")
    print("========================================")
