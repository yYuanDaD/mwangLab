"""Offline integration checks for strict semantic review (no provider calls)."""

import os
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import pandas as pd

from tools import batch_tools as bt
from tools.llm_helpers import ContrastValidationResult


class StrictSemanticRoutingTests(unittest.TestCase):
    def run_case(self, result, strict=True):
        with tempfile.TemporaryDirectory() as tmp:
            original_cwd = os.getcwd()
            try:
                os.chdir(tmp)
                folder = Path('data/GSETEST')
                folder.mkdir(parents=True)
                metadata = folder / 'GSETEST_metadata.csv'
                pd.DataFrame({'condition': ['ctrl'] * 3 + ['drugA'] * 3 + ['drugB'] * 3},
                             index=[f'S{i}' for i in range(9)]).to_csv(metadata)
                matrix = folder / 'expression.csv'
                pd.DataFrame([[1.1] * 9, [2.2] * 9],
                             columns=[f'S{i}' for i in range(9)]).to_csv(matrix)
                with (
                    patch.object(bt, 'download_geo_data', MagicMock()),
                    patch.object(bt, 'download_supplementary_files', MagicMock()),
                    patch.object(bt, '_find_expression_file', return_value=(str(matrix), 'log_transformed')),
                    patch.object(bt, 'sample_qc_summary', MagicMock()),
                    patch.object(bt, '_run_sex_check', return_value={
                        'n_mismatch': 0, 'mismatched': [], 'verdict': 'skipped', 'summary': 'test'}),
                    patch.object(bt, '_align_metadata_to_expression', return_value=(str(metadata), {})),
                    patch.object(bt, '_python_pick_is_confident', return_value=True) as gate,
                    patch.object(bt, 'validate_contrast_with_llm', return_value=result) as validator,
                    patch.object(bt, '_run_contrast_da', return_value={
                        'control': 'ctrl', 'treatment': 'drugA', 'n_deg': None,
                        'n_gsea_sig': None, 'status': 'deg_failed'}) as da,
                ):
                    bt.run_batch_geo_pipeline.func(
                        accessions=['GSETEST'], treatment_keywords=['drug'],
                        control_keywords=['ctrl'], llm_datatype=False,
                        llm_contrast_strict=strict, run_label='strict_test')
                    calls = da.call_args_list
                    evidence = json.loads(Path(
                        'output/cohort_strict_test/GSETEST/evidence.json').read_text(encoding='utf-8'))
                    if calls:
                        dispatch = next(d for d in evidence['decisions'] if d['step'] == 'execution_plan')
                        self.assertEqual(dispatch['details']['control'], 'ctrl')
                        self.assertEqual(dispatch['details']['treatment'], 'drugA')
                        known_ids = {d['decision_id'] for d in evidence['decisions']}
                        self.assertTrue(set(dispatch['details']['upstream_decision_ids']) <= known_ids)
                        semantic_id = next(d['decision_id'] for d in evidence['decisions']
                                           if d['step'] == 'llm_contrast_validation')
                        self.assertIn(semantic_id, dispatch['details']['upstream_decision_ids'])
                    return validator.call_count, gate.call_count, calls
            finally:
                os.chdir(original_cwd)

    def test_strict_reviews_confident_pick_and_only_executes_reviewed_triple(self):
        result = ContrastValidationResult(is_valid=True, design_column='condition',
                                         control_value='ctrl', treatment_value='drugA',
                                         intent_match=True, confidence='high', reasoning='reviewed')
        validator_calls, gate_calls, da_calls = self.run_case(result)
        self.assertEqual(validator_calls, 1)
        self.assertEqual(gate_calls, 0)
        self.assertEqual(len(da_calls), 1)
        self.assertEqual(da_calls[0].args[4:7], ('condition', 'ctrl', 'drugA'))

    def test_missing_validator_blocks_confident_pick_in_strict_mode(self):
        validator_calls, _, da_calls = self.run_case(None)
        self.assertEqual(validator_calls, 1)
        self.assertEqual(len(da_calls), 0)

    def test_boolean_without_triple_cannot_confirm_python_pick(self):
        result = ContrastValidationResult(is_valid=True, reasoning='missing required semantic decision')
        _, _, da_calls = self.run_case(result)
        self.assertEqual(len(da_calls), 0)

    def test_unrelated_triple_is_blocked_despite_high_confidence(self):
        result = ContrastValidationResult(is_valid=False, design_column='condition',
                                         control_value='ctrl', treatment_value='drugA',
                                         intent_match=False, confidence='high', reasoning='unrelated axis')
        _, _, calls = self.run_case(result)
        self.assertEqual(calls, [])

    def test_missing_intent_confirmation_is_blocked(self):
        result = ContrastValidationResult(is_valid=True, design_column='condition',
                                         control_value='ctrl', treatment_value='drugA',
                                         confidence='high', reasoning='legacy response lacks intent evidence')
        _, _, calls = self.run_case(result)
        self.assertEqual(calls, [])

    def test_low_confidence_intent_matching_triple_is_blocked(self):
        result = ContrastValidationResult(is_valid=True, design_column='condition',
                                         control_value='ctrl', treatment_value='drugA',
                                         intent_match=True, confidence='low', reasoning='uncertain')
        _, _, calls = self.run_case(result)
        self.assertEqual(calls, [])


if __name__ == '__main__':
    unittest.main()
