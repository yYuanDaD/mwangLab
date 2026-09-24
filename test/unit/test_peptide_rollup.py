"""Deterministic tests for peptide-level proteomics roll-up."""

import json
import os
import tempfile
import unittest

import pandas as pd

from tools.proteomics_tools import aggregate_peptides_to_proteins


class PeptideRollupTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.input_path = os.path.join(self.tmp.name, "peptides.csv")
        pd.DataFrame(
            {
                "Sequence": ["AAA", "BBB", "CCC", "DDD", "EEE", "FFF"],
                "Protein IDs": ["P1", "P1", "P2;P3", "DECOY_P4", "P2", "P2"],
                "S1": [10.0, 20.0, 100.0, 999.0, 5.0, 7.0],
                "S2": [11.0, 21.0, 110.0, 999.0, 6.0, 8.0],
                "PEP": [0.01, 0.02, 0.03, 0.04, 0.05, 0.06],
            }
        ).to_csv(self.input_path, index=False)

    def tearDown(self):
        self.tmp.cleanup()

    def test_linear_sum_excludes_shared_and_decoy(self):
        manifest = aggregate_peptides_to_proteins(
            self.input_path, output_dir=self.tmp.name, min_peptides=1,
        )
        out = pd.read_csv(manifest["output"], index_col=0)
        self.assertEqual(list(out.index), ["P1", "P2"])
        self.assertEqual(float(out.loc["P1", "S1"]), 30.0)
        self.assertEqual(float(out.loc["P2", "S1"]), 12.0)
        self.assertEqual(manifest["n_shared_peptides"], 1)
        with open(os.path.join(self.tmp.name, "peptides_protein_abundance.json"), encoding="utf-8") as fh:
            self.assertEqual(json.load(fh)["n_output_proteins"], 2)

    def test_shared_all_explodes_to_each_protein(self):
        manifest = aggregate_peptides_to_proteins(
            self.input_path, output_dir=self.tmp.name, shared_peptides="all",
        )
        out = pd.read_csv(manifest["output"], index_col=0)
        self.assertEqual(float(out.loc["P2", "S1"]), 112.0)
        self.assertEqual(float(out.loc["P3", "S1"]), 100.0)

    def test_log2_sum_is_rejected(self):
        with self.assertRaises(ValueError):
            aggregate_peptides_to_proteins(
                self.input_path, output_dir=self.tmp.name,
                input_scale="log2", aggregation_method="sum",
            )


if __name__ == "__main__":
    unittest.main()
