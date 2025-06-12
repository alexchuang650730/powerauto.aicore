"""
測試用例基類 - 提供統一的測試用例接口

此模組定義了PowerAutomation測試框架中的測試用例基類，
為所有測試用例提供統一的接口和基本功能。
"""

import os
import json
import logging
import datetime
from typing import Dict, Any, List, Optional, Tuple, Union

from testing.mock_config import MockConfig
from testing.environment import Environment


class TestCase:
    """測試用例基類
    
    為所有測試用例提供統一的接口和基本功能。
    
    屬性:
        test_id (str): 測試用例ID
        name (str): 測試用例名稱
        description (str): 測試用例描述
        layer (int): 測試層級 (1, 2, 或 3)
        environment (Environment): 環境抽象層實例
        logger (logging.Logger): 日誌記錄器
    """
    
    def __init__(self, test_id: str, name: str, description: str, layer: int = 1,
                 mock_config: Optional[MockConfig] = None):
        """初始化測試用例
        
        Args:
            test_id: 測試用例ID
            name: 測試用例名稱
            description: 測試用例描述
            layer: 測試層級 (1, 2, 或 3)
            mock_config: Mock配置對象，如果為None則使用默認配置
        """
        self.test_id = test_id
        self.name = name
        self.description = description
        self.layer = layer
        
        # 驗證層級
        if layer not in [1, 2, 3]:
            raise ValueError(f"無效的測試層級: {layer}，有效值為 1, 2, 或 3")
        
        # 創建環境
        self.environment = Environment(mock_config)
        
        # 配置日誌
        self.logger = logging.getLogger(f"test.{test_id}")
        self.logger.setLevel(logging.INFO)
        
        # 確保日誌目錄存在
        log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs', 'tests')
        os.makedirs(log_dir, exist_ok=True)
        
        # 添加文件處理器
        log_file = os.path.join(log_dir, f"{test_id}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.logger.addHandler(file_handler)
    
    def setup(self) -> None:
        """設置測試環境
        
        在測試執行前準備環境。
        子類可以覆蓋此方法以提供特定的設置邏輯。
        """
        self.logger.info(f"設置測試環境: {self.test_id}")
    
    def teardown(self) -> None:
        """清理測試環境
        
        在測試執行後清理環境。
        子類可以覆蓋此方法以提供特定的清理邏輯。
        """
        self.logger.info(f"清理測試環境: {self.test_id}")
    
    def run(self) -> Tuple[bool, Dict[str, Any]]:
        """運行測試
        
        執行測試用例並返回結果。
        子類必須覆蓋此方法以提供具體的測試邏輯。
        
        Returns:
            Tuple[bool, Dict[str, Any]]: 測試是否通過及詳細結果
        """
        raise NotImplementedError("子類必須實現run方法")
    
    def execute(self) -> Dict[str, Any]:
        """執行完整的測試流程
        
        包括設置環境、運行測試和清理環境。
        
        Returns:
            Dict[str, Any]: 測試結果
        """
        self.logger.info(f"開始執行測試: {self.test_id} - {self.name}")
        
        start_time = datetime.datetime.now()
        
        try:
            # 設置環境
            self.setup()
            
            # 運行測試
            success, result = self.run()
            
            # 清理環境
            self.teardown()
            
            # 計算執行時間
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # 構建結果
            test_result = {
                "test_id": self.test_id,
                "name": self.name,
                "description": self.description,
                "layer": self.layer,
                "success": success,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration": duration,
                "result": result
            }
            
            # 記錄結果
            if success:
                self.logger.info(f"測試通過: {self.test_id} - 耗時 {duration:.2f} 秒")
            else:
                self.logger.error(f"測試失敗: {self.test_id} - 耗時 {duration:.2f} 秒")
            
            return test_result
        
        except Exception as e:
            # 發生異常時，確保清理環境
            self.logger.exception(f"測試執行異常: {self.test_id} - {str(e)}")
            
            try:
                self.teardown()
            except Exception as cleanup_error:
                self.logger.error(f"清理環境時發生異常: {str(cleanup_error)}")
            
            # 計算執行時間
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            
            # 構建錯誤結果
            error_result = {
                "test_id": self.test_id,
                "name": self.name,
                "description": self.description,
                "layer": self.layer,
                "success": False,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "duration": duration,
                "error": str(e),
                "error_type": e.__class__.__name__
            }
            
            return error_result
    
    def save_result(self, result: Dict[str, Any], output_dir: Optional[str] = None) -> str:
        """保存測試結果
        
        Args:
            result: 測試結果
            output_dir: 輸出目錄，如果為None則使用默認目錄
            
        Returns:
            str: 結果文件路徑
        """
        # 確定輸出目錄
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'test_results')
        
        # 確保輸出目錄存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 構建結果文件路徑
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        result_file = os.path.join(output_dir, f"{self.test_id}_{timestamp}.json")
        
        # 保存結果
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
        
        self.logger.info(f"測試結果已保存: {result_file}")
        
        return result_file


class UnitTestCase(TestCase):
    """單元測試用例
    
    第1層測試用例，專注於單元測試和代碼質量。
    """
    
    def __init__(self, test_id: str, name: str, description: str,
                 mock_config: Optional[MockConfig] = None):
        """初始化單元測試用例
        
        Args:
            test_id: 測試用例ID
            name: 測試用例名稱
            description: 測試用例描述
            mock_config: Mock配置對象，如果為None則使用默認配置
        """
        super().__init__(test_id, name, description, layer=1, mock_config=mock_config)


class IntegrationTestCase(TestCase):
    """集成測試用例
    
    第2層測試用例，專注於集成測試和智能體協作。
    """
    
    def __init__(self, test_id: str, name: str, description: str,
                 mock_config: Optional[MockConfig] = None):
        """初始化集成測試用例
        
        Args:
            test_id: 測試用例ID
            name: 測試用例名稱
            description: 測試用例描述
            mock_config: Mock配置對象，如果為None則使用默認配置
        """
        super().__init__(test_id, name, description, layer=2, mock_config=mock_config)


class ComplianceTestCase(TestCase):
    """合規測試用例
    
    第3層測試用例，專注於MCP合規測試和標準化驗證。
    """
    
    def __init__(self, test_id: str, name: str, description: str,
                 mock_config: Optional[MockConfig] = None):
        """初始化合規測試用例
        
        Args:
            test_id: 測試用例ID
            name: 測試用例名稱
            description: 測試用例描述
            mock_config: Mock配置對象，如果為None則使用默認配置
        """
        super().__init__(test_id, name, description, layer=3, mock_config=mock_config)
