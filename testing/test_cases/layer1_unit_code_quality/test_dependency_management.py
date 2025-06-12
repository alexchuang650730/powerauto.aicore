
import unittest
import os
import sys
from unittest.mock import patch, MagicMock

# Add the testing directory to the Python path to allow absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                '..', '..', '..')))

from testing.dependency_manager import DependencyManager

class TestDependencyManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Instantiate DependencyManager to get the correct requirements_dir
        cls.manager_instance = DependencyManager()
        cls.REQUIREMENTS_DIR = cls.manager_instance.requirements_dir

        os.makedirs(cls.REQUIREMENTS_DIR, exist_ok=True)
        with open(os.path.join(cls.REQUIREMENTS_DIR, 'requirements-core.txt'), 'w') as f:
            f.write('core_dep==1.0.0')
        with open(os.path.join(cls.REQUIREMENTS_DIR, 'requirements-test.txt'), 'w') as f:
            f.write('test_dep==1.0.0')
        with open(os.path.join(cls.REQUIREMENTS_DIR, 'requirements-full.txt'), 'w') as f:
            f.write('full_dep==1.0.0')

    @classmethod
    def tearDownClass(cls):
        # Clean up dummy requirements files and directory
        for f in os.listdir(cls.REQUIREMENTS_DIR):
            os.remove(os.path.join(cls.REQUIREMENTS_DIR, f))
        os.rmdir(cls.REQUIREMENTS_DIR)

    @patch('psutil.virtual_memory')
    @patch('os.cpu_count')
    @patch('platform.system')
    def test_select_requirements_file_low_memory(self, mock_platform_system, mock_cpu_count, mock_virtual_memory):
        # Simulate low memory (e.g., 2GB)
        mock_virtual_memory.return_value = MagicMock(total=2 * (1024**3)) # 2GB
        mock_cpu_count.return_value = 2
        mock_platform_system.return_value = 'Linux'

        manager = DependencyManager() # Instantiate DependencyManager
        resources = manager.get_system_resources() # Get resources via manager
        selected_file = manager.get_requirements_file(manager.select_dependency_level(resources))
        self.assertEqual(selected_file, os.path.join(self.REQUIREMENTS_DIR, 'requirements-core.txt'))

    @patch('psutil.virtual_memory')
    @patch('os.cpu_count')
    @patch('platform.system')
    def test_select_requirements_file_medium_memory(self, mock_platform_system, mock_cpu_count, mock_virtual_memory):
        # Simulate medium memory (e.g., 6GB)
        mock_virtual_memory.return_value = MagicMock(total=6 * (1024**3)) # 6GB
        mock_cpu_count.return_value = 4
        mock_platform_system.return_value = 'Linux'

        manager = DependencyManager() # Instantiate DependencyManager
        resources = manager.get_system_resources() # Get resources via manager
        selected_file = manager.get_requirements_file(manager.select_dependency_level(resources))
        self.assertEqual(selected_file, os.path.join(self.REQUIREMENTS_DIR, 'requirements-test.txt'))

    @patch('psutil.virtual_memory')
    @patch('os.cpu_count')
    @patch('platform.system')
    def test_select_requirements_file_high_memory(self, mock_platform_system, mock_cpu_count, mock_virtual_memory):
        # Simulate high memory (e.g., 16GB)
        mock_virtual_memory.return_value = MagicMock(total=16 * (1024**3)) # 16GB
        mock_cpu_count.return_value = 8
        mock_platform_system.return_value = 'Linux'

        manager = DependencyManager() # Instantiate DependencyManager
        resources = manager.get_system_resources() # Get resources via manager
        selected_file = manager.get_requirements_file(manager.select_dependency_level(resources))
        self.assertEqual(selected_file, os.path.join(self.REQUIREMENTS_DIR, 'requirements-full.txt'))

if __name__ == '__main__':
    unittest.main()


