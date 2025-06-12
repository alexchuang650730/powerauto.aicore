
import unittest
import os
import sys
import json
import shutil
from unittest.mock import patch, MagicMock

# Add the testing directory to the Python path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                '..', '..', '..')))

from testing.cli.intelligent_engine_cli import IntelligentEngineCLI

class TestCLIAnalysisIntegration(unittest.TestCase):

    def setUp(self):
        self.test_results_dir = '/tmp/cli_test_results'
        os.makedirs(self.test_results_dir, exist_ok=True)
        self.cli = IntelligentEngineCLI()

    def tearDown(self):
        if os.path.exists(self.test_results_dir):
            shutil.rmtree(self.test_results_dir)

    def test_analyze_results_with_mock_data(self):
        # Simulate running analyze-results command with mock data
        args = MagicMock(command='analyze-results', results_dir=self.test_results_dir, output=None)
        
        # Create a dummy test_results.json for the CLI to read
        dummy_test_results = {
            "errors": [
                {"test": "test_module.TestClass.test_error_case", "message": "TypeError: Unsupported operand type"}
            ],
            "failures": [
                {"test": "test_module.TestClass.test_failed_case", "message": "AssertionError: Expected X but got Y"}
            ]
        }
        with open(os.path.join(self.test_results_dir, 'test_results.json'), 'w') as f:
            json.dump(dummy_test_results, f)

        exit_code = self.cli._handle_analyze_results(args)
        self.assertEqual(exit_code, 0)

        # Verify that the analysis report was created
        analysis_report_path = os.path.join(self.test_results_dir, 'analysis_report.json')
        self.assertTrue(os.path.exists(analysis_report_path))

        with open(analysis_report_path, 'r') as f:
            report = json.load(f)
            self.assertIsInstance(report, list)
            self.assertGreater(len(report), 0)
            # Check for expected content in the report
            self.assertIn({'type': 'error', 'test': 'test_module.TestClass.test_error_case', 'message': 'TypeError: Unsupported operand type'}, report)
            self.assertIn({'type': 'failure', 'test': 'test_module.TestClass.test_failed_case', 'message': 'AssertionError: Expected X but got Y'}, report)

    def test_fix_issues_auto_apply(self):
        # Simulate running fix-issues command with auto-apply
        args = MagicMock(command='fix-issues', results_dir=self.test_results_dir, auto_apply=True, output=None)

        # Create a dummy analysis_report.json for the CLI to read
        dummy_analysis_report = [
            {"type": "failure", "test": "test_module.TestClass.test_failed_case", "message": "AssertionError: Expected X but got Y"}
        ]
        with open(os.path.join(self.test_results_dir, 'analysis_report.json'), 'w') as f:
            json.dump(dummy_analysis_report, f)

        exit_code = self.cli._handle_fix_issues(args)
        self.assertEqual(exit_code, 0)

        # Verify that the applied fixes report was created
        applied_fixes_report_path = os.path.join(self.test_results_dir, 'applied_fixes_report.json')
        self.assertTrue(os.path.exists(applied_fixes_report_path))

        with open(applied_fixes_report_path, 'r') as f:
            report = json.load(f)
            self.assertIsInstance(report, list)
            self.assertGreater(len(report), 0)
            self.assertEqual(report[0]['status'], 'applied')

    def test_validate_fixes(self):
        # Simulate running validate-fixes command
        args = MagicMock(command='validate-fixes', fixes_dir=self.test_results_dir, output=None)

        # Create a dummy applied_fixes_report.json for the CLI to read
        dummy_applied_fixes = [
            {"suggestion": {"problem": {"type": "failure", "test": "test_module.TestClass.test_failed_case"}, "suggestion": "嘗試修正 test_module.TestClass.test_failed_case 相關問題。"}, "status": "applied"}
        ]
        with open(os.path.join(self.test_results_dir, 'applied_fixes_report.json'), 'w') as f:
            json.dump(dummy_applied_fixes, f)

        exit_code = self.cli._handle_validate_fixes(args)
        self.assertEqual(exit_code, 0)

        # Verify that the validation report was created
        validation_report_path = os.path.join(self.test_results_dir, 'validation_report.json')
        self.assertTrue(os.path.exists(validation_report_path))

        with open(validation_report_path, 'r') as f:
            report = json.load(f)
            self.assertIsInstance(report, list)
            self.assertGreater(len(report), 0)
            self.assertEqual(report[0]['validation_status'], 'success')

if __name__ == '__main__':
    unittest.main()


