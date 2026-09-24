"""Regression test for donor-paired single-cell pseudobulk analysis."""

import os
import tempfile
import unittest

import numpy as np
import pandas as pd

from tools.scrna_tools import run_scrna_pseudobulk_da


class PairedScrnaTests(unittest.TestCase):
    def test_complete_donor_pairs_use_blocked_limma(self):
        with tempfile.TemporaryDirectory() as out:
            cells, obs_rows = [], []
            for donor in ("D1", "D2", "D3"):
                for condition in ("ctrl", "treat"):
                    for rep in range(2):
                        cell = f"{donor}_{condition}_{rep}"
                        cells.append(cell)
                        obs_rows.append({"cell": cell, "donor": donor, "celltype": "T",
                                         "condition": condition})
            counts = pd.DataFrame(
                np.arange(3 * len(cells)).reshape(3, len(cells)) + 10,
                index=["g1", "g2", "g3"], columns=cells,
            )
            metadata = pd.DataFrame(obs_rows).set_index("cell")
            counts_path = os.path.join(out, "counts.csv")
            metadata_path = os.path.join(out, "metadata.csv")
            counts.to_csv(counts_path)
            metadata.to_csv(metadata_path)

            result = run_scrna_pseudobulk_da.invoke({
                "matrix_path": counts_path,
                "sample_col": "donor",
                "celltype_col": "celltype",
                "condition_col": "condition",
                "control_group": "ctrl",
                "treatment_group": "treat",
                "cell_metadata_path": metadata_path,
                "min_cells": 1,
                "min_samples_per_group": 2,
                "run_gsea": False,
                "paired": True,
                "output_dir": out,
            })
            self.assertIn("DA: limma", result)
            summary = pd.read_csv(os.path.join(out, "scrna_pseudobulk_summary.csv"))
            self.assertEqual(int(summary.loc[0, "n_complete_pairs"]), 3)
            self.assertEqual(summary.loc[0, "status"], "deg_ok_paired")


if __name__ == "__main__":
    unittest.main()
