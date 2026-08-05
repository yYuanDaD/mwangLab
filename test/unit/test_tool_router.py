import unittest
from types import SimpleNamespace

from tools.tool_router import select_tools


ALL_NAMES = [
    "run_agent_a_cohort", "search_papers", "fetch_paper_text", "extract_geo_accession",
    "extract_sea_cdm_tables", "search_geo_studies", "download_geo_data",
    "download_supplementary_files", "fetch_geo_description", "inspect_metadata",
    "preprocess_counts", "run_pca", "sample_correlation_heatmap", "sample_qc_summary",
    "infer_sex_from_expression", "run_deseq2_analysis", "run_limma_analysis",
    "run_enrichment_analysis", "run_gsea_analysis", "run_batch_geo_pipeline",
    "run_scrna_pseudobulk_da", "run_methylation_da", "identify_proteomics_labeling",
    "download_pride_project", "preprocess_proteomics_matrix",
    "evaluate_repeated_subset_results", "export_kg_style_results",
]


class ToolRouterTests(unittest.TestCase):
    def setUp(self):
        self.registry = [SimpleNamespace(name=name) for name in ALL_NAMES]

    def names(self, query):
        tools, decision = select_tools(query, self.registry)
        return {t.name for t in tools}, decision

    def test_known_gse_gets_high_level_geo_tools(self):
        names, decision = self.names("分析 GSE279359")
        self.assertEqual(decision.profiles, ("geo_batch",))
        self.assertIn("run_batch_geo_pipeline", names)
        self.assertNotIn("run_scrna_pseudobulk_da", names)

    def test_explicit_gse_download_exposes_low_level_download(self):
        names, decision = self.names("只下载 GSE279359 数据")
        self.assertEqual(decision.profiles, ("bulk_expression",))
        self.assertIn("download_geo_data", names)
        self.assertIn("download_supplementary_files", names)

    def test_single_cell_excludes_bulk_da(self):
        names, decision = self.names("对单细胞 RNA-seq 做 pseudobulk 差异分析")
        self.assertEqual(decision.profiles, ("single_cell",))
        self.assertIn("run_scrna_pseudobulk_da", names)
        self.assertNotIn("run_deseq2_analysis", names)

    def test_proteomics_includes_only_valid_da_path(self):
        names, _ = self.names("分析 PRIDE PXD123456 蛋白组")
        self.assertIn("identify_proteomics_labeling", names)
        self.assertIn("run_limma_analysis", names)
        self.assertNotIn("run_deseq2_analysis", names)

    def test_paper_cohort_exposes_only_orchestrator(self):
        names, _ = self.names("构建 exercise 文献队列，分析 top papers")
        self.assertEqual(names, {"run_agent_a_cohort"})

    def test_paper_seacdm_single_study_composes_profiles(self):
        names, decision = self.names("从这篇论文提取 SEA-CDM")
        self.assertEqual(decision.profiles, ("sea_cdm", "paper_utility"))
        self.assertIn("extract_sea_cdm_tables", names)
        self.assertIn("search_papers", names)

    def test_ambiguous_request_falls_back_to_all(self):
        names, decision = self.names("帮我看看这个项目")
        self.assertTrue(decision.fallback_to_all)
        self.assertEqual(names, set(ALL_NAMES))


if __name__ == "__main__":
    unittest.main()
