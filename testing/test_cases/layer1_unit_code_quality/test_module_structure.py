
import unittest
import os
import sys

# Add the testing directory to the Python path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                '..', '..', '..')))

from shared_core.interfaces.test_coordinator_interface import TestCoordinatorInterface
from shared_core.implementations.distributed_coordinator import DistributedTestCoordinator

class TestModuleStructure(unittest.TestCase):

    def test_distributed_coordinator_implements_interface(self):
        # Verify that DistributedTestCoordinator implements TestCoordinatorInterface
        coordinator = DistributedTestCoordinator()
        self.assertIsInstance(coordinator, TestCoordinatorInterface)
        self.assertTrue(hasattr(coordinator, 'initialize'))
        self.assertTrue(hasattr(coordinator, 'get_status'))

    def test_distributed_coordinator_methods(self):
        # Verify the methods of DistributedTestCoordinator
        coordinator = DistributedTestCoordinator()
        self.assertIsNone(coordinator.initialize()) # initialize method does not return anything
        self.assertEqual(coordinator.get_status(), "Distributed Coordinator Status: OK")

if __name__ == '__main__':
    unittest.main()


