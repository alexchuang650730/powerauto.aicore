"""
測試用例註冊表 - 提供統一的測試用例管理

此模組實現了PowerAutomation測試框架的測試用例註冊表，
用於管理所有測試用例，支持按層級、類型等方式查詢和運行測試。
"""

import os
import json
import logging
from typing import Dict, Any, List, Optional, Type, Union

from testing.test_case import TestCase, UnitTestCase, IntegrationTestCase, ComplianceTestCase


class TestRegistry:
    """測試用例註冊表
    
    負責管理所有測試用例，支持按層級、類型等方式查詢和運行測試。
    
    屬性:
        logger (logging.Logger): 日誌記錄器
        test_cases (Dict[str, Type[TestCase]]): 測試用例字典，鍵為測試ID，值為測試用例類
    """
    
    def __init__(self):
        """初始化測試用例註冊表"""
        self.logger = logging.getLogger("test_registry")
        self.test_cases = {}
    
    def register(self, test_id: str, test_case_class: Type[TestCase]) -> None:
        """註冊測試用例
        
        Args:
            test_id: 測試用例ID
            test_case_class: 測試用例類
        """
        if test_id in self.test_cases:
            self.logger.warning(f"測試用例 {test_id} 已存在，將被覆蓋")
        
        self.test_cases[test_id] = test_case_class
        self.logger.info(f"註冊測試用例: {test_id}")
    
    def get_test_case(self, test_id: str) -> Optional[Type[TestCase]]:
        """獲取測試用例
        
        Args:
            test_id: 測試用例ID
            
        Returns:
            Optional[Type[TestCase]]: 測試用例類，如果不存在則返回None
        """
        return self.test_cases.get(test_id)
    
    def get_test_cases_by_layer(self, layer: int) -> Dict[str, Type[TestCase]]:
        """獲取特定層級的測試用例
        
        Args:
            layer: 測試層級 (1, 2, 或 3)
            
        Returns:
            Dict[str, Type[TestCase]]: 測試用例字典，鍵為測試ID，值為測試用例類
        """
        result = {}
        
        for test_id, test_case_class in self.test_cases.items():
            # 創建測試用例實例以獲取層級
            # 注意：這裡假設測試用例類的構造函數接受test_id, name, description參數
            test_case = test_case_class(test_id, f"Test {test_id}", f"Description for {test_id}")
            
            if test_case.layer == layer:
                result[test_id] = test_case_class
        
        return result
    
    def get_all_test_cases(self) -> Dict[str, Type[TestCase]]:
        """獲取所有測試用例
        
        Returns:
            Dict[str, Type[TestCase]]: 測試用例字典，鍵為測試ID，值為測試用例類
        """
        return self.test_cases.copy()
    
    def load_from_directory(self, directory: str) -> int:
        """從目錄加載測試用例
        
        Args:
            directory: 測試用例目錄
            
        Returns:
            int: 加載的測試用例數量
        """
        self.logger.info(f"從目錄加載測試用例: {directory}")
        
        count = 0
        
        # 遍歷目錄
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith('.py') and not file.startswith('__'):
                    # 構建模塊路徑
                    file_path = os.path.join(root, file)
                    module_path = os.path.relpath(file_path, os.path.dirname(directory))
                    module_name = os.path.splitext(module_path)[0].replace(os.path.sep, '.')
                    
                    try:
                        # 導入模塊
                        module = __import__(module_name, fromlist=['*'])
                        
                        # 查找測試用例類
                        for attr_name in dir(module):
                            attr = getattr(module, attr_name)
                            
                            # 檢查是否是TestCase的子類
                            if isinstance(attr, type) and issubclass(attr, TestCase) and attr != TestCase and attr != UnitTestCase and attr != IntegrationTestCase and attr != ComplianceTestCase:
                                # 獲取測試ID
                                if hasattr(attr, 'TEST_ID'):
                                    test_id = getattr(attr, 'TEST_ID')
                                else:
                                    # 使用類名作為測試ID
                                    test_id = attr.__name__
                                
                                # 註冊測試用例
                                self.register(test_id, attr)
                                count += 1
                    
                    except Exception as e:
                        self.logger.error(f"加載測試用例模塊 {module_name} 失敗: {e}")
        
        self.logger.info(f"從目錄加載了 {count} 個測試用例")
        return count
    
    def save_to_json(self, file_path: str) -> bool:
        """保存測試用例註冊表到JSON文件
        
        Args:
            file_path: JSON文件路徑
            
        Returns:
            bool: 保存是否成功
        """
        self.logger.info(f"保存測試用例註冊表到: {file_path}")
        
        try:
            # 構建測試用例信息
            test_cases_info = {}
            
            for test_id, test_case_class in self.test_cases.items():
                # 創建測試用例實例以獲取信息
                test_case = test_case_class(test_id, f"Test {test_id}", f"Description for {test_id}")
                
                test_cases_info[test_id] = {
                    "name": test_case.name,
                    "description": test_case.description,
                    "layer": test_case.layer,
                    "class": f"{test_case_class.__module__}.{test_case_class.__name__}"
                }
            
            # 確保目錄存在
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # 保存到JSON文件
            with open(file_path, 'w') as f:
                json.dump(test_cases_info, f, indent=2)
            
            self.logger.info(f"測試用例註冊表已保存: {file_path}")
            return True
        
        except Exception as e:
            self.logger.error(f"保存測試用例註冊表失敗: {e}")
            return False
    
    def load_from_json(self, file_path: str) -> int:
        """從JSON文件加載測試用例註冊表
        
        Args:
            file_path: JSON文件路徑
            
        Returns:
            int: 加載的測試用例數量
        """
        self.logger.info(f"從JSON文件加載測試用例註冊表: {file_path}")
        
        try:
            # 檢查文件是否存在
            if not os.path.exists(file_path):
                self.logger.error(f"文件不存在: {file_path}")
                return 0
            
            # 從JSON文件加載
            with open(file_path, 'r') as f:
                test_cases_info = json.load(f)
            
            count = 0
            
            for test_id, info in test_cases_info.items():
                try:
                    # 解析類路徑
                    class_path = info.get("class", "")
                    if not class_path:
                        self.logger.warning(f"測試用例 {test_id} 缺少類路徑")
                        continue
                    
                    module_name, class_name = class_path.rsplit('.', 1)
                    
                    # 導入模塊
                    module = __import__(module_name, fromlist=[class_name])
                    
                    # 獲取類
                    test_case_class = getattr(module, class_name)
                    
                    # 註冊測試用例
                    self.register(test_id, test_case_class)
                    count += 1
                
                except Exception as e:
                    self.logger.error(f"加載測試用例 {test_id} 失敗: {e}")
            
            self.logger.info(f"從JSON文件加載了 {count} 個測試用例")
            return count
        
        except Exception as e:
            self.logger.error(f"加載測試用例註冊表失敗: {e}")
            return 0


# 默認測試用例註冊表實例
default_test_registry = TestRegistry()
