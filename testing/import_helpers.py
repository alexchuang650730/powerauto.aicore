"""
導入輔助模組 - 提供統一的導入路徑管理

此模組用於解決PowerAutomation測試框架中的導入路徑問題，
提供統一的方法將項目根目錄添加到Python路徑中，
確保所有測試模組可以使用一致的導入方式。
"""

import sys
import os


def add_project_root_to_path():
    """
    將項目根目錄添加到Python路徑
    
    這個函數會將PowerAutomation項目的根目錄添加到sys.path中，
    使得所有模組都可以使用絕對導入路徑。
    
    使用方法:
    ```python
    from testing.import_helpers import add_project_root_to_path
    add_project_root_to_path()
    
    # 現在可以使用絕對導入
    from powerauto.ai_0.53.shared_core.engines import workflow_engine
    ```
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
        print(f"Added {project_root} to Python path")


def get_absolute_path(relative_path):
    """
    獲取相對於項目根目錄的絕對路徑
    
    Args:
        relative_path: 相對於項目根目錄的路徑
        
    Returns:
        str: 絕對路徑
    """
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    return os.path.join(project_root, relative_path)


def get_test_data_path(test_case_id=None):
    """
    獲取測試數據目錄的路徑
    
    Args:
        test_case_id: 可選的測試用例ID
        
    Returns:
        str: 測試數據目錄的絕對路徑
    """
    test_data_path = get_absolute_path('test_data')
    if test_case_id:
        return os.path.join(test_data_path, test_case_id)
    return test_data_path
