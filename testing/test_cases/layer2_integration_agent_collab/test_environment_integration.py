
import unittest
import os
import sys
from unittest.mock import patch

# Add the testing directory to the Python path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                '..', '..', '..')))

from testing.mock_config import MockConfig
from testing.environment import Environment

# Import mock and real components
from testing.mocks.file_system import MockFileSystem
from shared_core.io.file_system import FileSystem as RealFileSystem
from testing.mocks.network import MockNetwork
from shared_core.io.network import Network as RealNetwork
from testing.mocks.database import MockDatabase
from shared_core.storage.database import Database as RealDatabase

class TestEnvironmentIntegration(unittest.TestCase):

    def test_mixed_environment_interaction(self):
        # Scenario: FileSystem is mocked, Network and Database are real
        mock_config_data = {
            "use_mock": True,
            "mock_level": "partial",
            "components": {
                "file_system": {"mock": True},
                "network": {"mock": False},
                "database": {"mock": False}
            }
        }
        mock_config = MockConfig(config_data=mock_config_data)
        env = Environment(mock_config=mock_config)

        # Verify component types
        self.assertIsInstance(env.get_file_system(), MockFileSystem)
        self.assertIsInstance(env.get_network(), RealNetwork)
        self.assertIsInstance(env.get_database(), RealDatabase)

        # Simulate a simple workflow interaction
        # (In a real scenario, these would be more complex interactions)
        file_system = env.get_file_system()
        network = env.get_network()
        database = env.get_database()

        # Assert that the names are as expected (from our dummy classes)
        self.assertEqual(file_system.name, "MockFileSystem")
        self.assertEqual(network.name, "RealNetwork")
        self.assertEqual(database.name, "RealDatabase")

    def test_full_real_environment_interaction(self):
        # Scenario: All components are real
        mock_config_data = {"use_mock": False}
        mock_config = MockConfig(config_data=mock_config_data)
        env = Environment(mock_config=mock_config)

        # Verify component types
        self.assertIsInstance(env.get_file_system(), RealFileSystem)
        self.assertIsInstance(env.get_network(), RealNetwork)
        self.assertIsInstance(env.get_database(), RealDatabase)

        # Simulate a simple workflow interaction
        file_system = env.get_file_system()
        network = env.get_network()
        database = env.get_database()

        self.assertEqual(file_system.name, "RealFileSystem")
        self.assertEqual(network.name, "RealNetwork")
        self.assertEqual(database.name, "RealDatabase")

    def test_full_mock_environment_interaction(self):
        # Scenario: All components are mocked
        mock_config_data = {"use_mock": True, "mock_level": "full"}
        mock_config = MockConfig(config_data=mock_config_data)
        env = Environment(mock_config=mock_config)

        # Verify component types
        self.assertIsInstance(env.get_file_system(), MockFileSystem)
        self.assertIsInstance(env.get_network(), MockNetwork)
        self.assertIsInstance(env.get_database(), MockDatabase)

        # Simulate a simple workflow interaction
        file_system = env.get_file_system()
        network = env.get_network()
        database = env.get_database()

        self.assertEqual(file_system.name, "MockFileSystem")
        self.assertEqual(network.name, "MockNetwork")
        self.assertEqual(database.name, "MockDatabase")

if __name__ == '__main__':
    unittest.main()


