
import unittest
import os
import sys

# Add the testing directory to the Python path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                '..', '..', '..')))

from testing.mock_config import MockConfig
from testing.environment import Environment

# Import the actual mock and real implementations
from testing.mocks.file_system import MockFileSystem
from shared_core.io.file_system import FileSystem as RealFileSystem
from testing.mocks.network import MockNetwork
from shared_core.io.network import Network as RealNetwork
from testing.mocks.database import MockDatabase
from shared_core.storage.database import Database as RealDatabase

class TestMockEnvironment(unittest.TestCase):

    def test_mock_config_default(self):
        # Test default behavior: use_mock=True, mock_level="partial"
        config = MockConfig()
        # In partial mock level, should_mock returns False unless component is explicitly mocked
        self.assertFalse(config.should_mock("any_component"))

    def test_mock_config_no_mock(self):
        # Test explicit no mock
        config = MockConfig(config_data={"use_mock": False})
        self.assertFalse(config.should_mock("any_component"))

    def test_mock_config_partial_mock(self):
        # Test partial mock level
        config = MockConfig(config_data={
            "use_mock": True,
            "mock_level": "partial",
            "components": {
                "file_system": {"mock": True},
                "network": {"mock": False}
            }
        })
        self.assertTrue(config.should_mock("file_system"))
        self.assertFalse(config.should_mock("network"))
        self.assertFalse(config.should_mock("database")) # Default to False if not specified

    def test_environment_with_full_mock(self):
        # Test Environment with full mock config
        mock_config = MockConfig(config_data={
            "use_mock": True,
            "mock_level": "full"
        })
        env = Environment(mock_config=mock_config)

        self.assertIsInstance(env.get_file_system(), MockFileSystem)
        self.assertIsInstance(env.get_network(), MockNetwork)
        self.assertIsInstance(env.get_database(), MockDatabase)

    def test_environment_with_no_mock(self):
        # Test Environment with no mock config
        mock_config = MockConfig(config_data={
            "use_mock": False
        })
        env = Environment(mock_config=mock_config)

        self.assertIsInstance(env.get_file_system(), RealFileSystem)
        self.assertIsInstance(env.get_network(), RealNetwork)
        self.assertIsInstance(env.get_database(), RealDatabase)

    def test_environment_with_partial_mock(self):
        # Test Environment with partial mock config
        mock_config = MockConfig(config_data={
            "use_mock": True,
            "mock_level": "partial",
            "components": {
                "file_system": {"mock": True},
                "network": {"mock": False}
            }
        })
        env = Environment(mock_config=mock_config)

        self.assertIsInstance(env.get_file_system(), MockFileSystem)
        self.assertIsInstance(env.get_network(), RealNetwork)
        self.assertIsInstance(env.get_database(), RealDatabase) # Default to Real if not specified

if __name__ == '__main__':
    unittest.main()


