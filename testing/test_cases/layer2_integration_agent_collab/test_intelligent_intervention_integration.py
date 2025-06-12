
import unittest
import os
import sys
from unittest.mock import MagicMock, patch
import shutil

# Add the testing directory to the Python path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                '..', '..', '..')))

from testing.intelligent_intervention.intervention import InterventionEngine

class TestIntelligentInterventionIntegration(unittest.TestCase):

    @patch('testing.intelligent_intervention.intervention.ProblemDetector')
    @patch('testing.intelligent_intervention.intervention.FixGenerator')
    @patch('testing.intelligent_intervention.intervention.AutoFixer')
    @patch('testing.intelligent_intervention.intervention.FixValidator')
    def test_intervention_flow(self, MockFixValidator, MockAutoFixer, MockFixGenerator, MockProblemDetector):
        # Mock instances
        mock_problem_detector_instance = MockProblemDetector.return_value
        mock_fix_generator_instance = MockFixGenerator.return_value
        mock_auto_fixer_instance = MockAutoFixer.return_value
        mock_fix_validator_instance = MockFixValidator.return_value

        # Configure mock behaviors
        mock_test_results = MagicMock()
        mock_test_results.wasSuccessful.return_value = False # Simulate a failed test run
        mock_test_results.errors = [('test_error_case', 'Error Traceback')]
        mock_test_results.failures = []

        mock_problem_detector_instance.detect.return_value = [{'problem': 'detected'}]
        mock_fix_generator_instance.generate.return_value = [{'suggestion': 'generated'}]
        mock_auto_fixer_instance.apply.return_value = [{'fix': 'applied'}]
        mock_fix_validator_instance.validate.return_value = [{'validation': 'success'}]

        engine = InterventionEngine()
        
        # Ensure the output directory exists before calling intervene
        output_dir = '/tmp/intervention_test_output'
        os.makedirs(output_dir, exist_ok=True)

        # Call the intervene method
        engine.intervene(mock_test_results, output_dir=output_dir)

        # Assert that each component's method was called
        mock_problem_detector_instance.detect.assert_called_once_with(mock_test_results)
        mock_fix_generator_instance.generate.assert_called_once_with([{'problem': 'detected'}]
)
        mock_auto_fixer_instance.apply.assert_called_once_with([{'suggestion': 'generated'}]
)
        mock_fix_validator_instance.validate.assert_called_once_with([{'fix': 'applied'}]
)

        # Clean up the dummy directory created by InterventionEngine
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

if __name__ == '__main__':
    unittest.main()


