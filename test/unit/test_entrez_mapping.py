"""Entrez gene IDs: mapped to symbols through MyGene (entrezgene scope) only when declared."""
import os
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from tools import case_runner  # noqa: E402
from tools import enrichment_tools as et  # noqa: E402


class _FakeMyGene:
    calls = []

    def querymany(self, ids, scopes=None, **kwargs):
        ids = list(ids)
        self.calls.append((scopes, tuple(ids)))
        return [{"query": i, "symbol": f"Gene{i}"} for i in ids if i != "999"]


class EntrezMappingTests(unittest.TestCase):
    def setUp(self):
        self._mg = et.mygene.MyGeneInfo
        et.mygene.MyGeneInfo = _FakeMyGene
        _FakeMyGene.calls = []
        et._SYMBOL_CACHE.clear()

    def tearDown(self):
        et.mygene.MyGeneInfo = self._mg
        et._SYMBOL_CACHE.clear()

    def test_entrez_scope_and_cache(self):
        self.assertEqual(et._entrez_to_symbol_map(["12", "13", "999"], "Mouse"), {"12": "Gene12", "13": "Gene13"})
        self.assertEqual(et._entrez_to_symbol_map(["12"], "Mouse"), {"12": "Gene12"})
        self.assertEqual(_FakeMyGene.calls, [("entrezgene", ("12", "13", "999"))])
        # an Ensembl lookup of the same string is a separate cache entry
        et._ensembl_to_symbol_map(["12"], "Mouse")
        self.assertEqual(_FakeMyGene.calls[-1][0], "ensembl.gene")

    def test_ora_refuses_undeclared_integer_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            deg = os.path.join(tmp, "DEG_results_a_vs_b.csv")
            pd.DataFrame({"padj": [0.01] * 10, "log2FoldChange": [2.0] * 10, "pvalue": [0.001] * 10},
                         index=[str(i) for i in range(100, 110)]).to_csv(deg)
            message = et.run_enrichment_analysis.invoke({"deg_csv": deg, "output_dir": tmp})
            self.assertIn("id_type='entrez'", message)

    def test_paper_gene_lookup_maps_entrez_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            deg = os.path.join(tmp, "DEG.csv")
            pd.DataFrame({"log2FoldChange": [1.5, -0.2], "padj": [0.001, 0.9]}, index=[12, 13]).to_csv(deg)
            look = case_runner._gene_lookup(deg, ["Gene12", "Nope"], "Mouse", "entrez")
            self.assertEqual(look["Gene12"]["log2FoldChange"], 1.5)
            self.assertIsNone(look["Nope"])


if __name__ == "__main__":
    unittest.main()
