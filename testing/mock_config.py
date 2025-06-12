"""
Mock配置系統 - 提供統一的Mock策略管理

此模組用於解決PowerAutomation測試框架中的Mock與真實環境切換問題，
提供統一的配置機制來控制測試中的Mock行為。
"""

import os
import json
import yaml


class MockConfig:
    """Mock配置管理類
    
    負責加載、解析和提供Mock配置信息，使測試框架能夠統一管理Mock策略。
    
    屬性:
        config (dict): Mock配置信息
        default_mock_level (str): 默認的Mock級別
    """
    
    def __init__(self, config_file=None, default_mock_level="partial", config_data=None):
        """初始化Mock配置
        
        Args:
            config_file (str, optional): 配置文件路徑，如果為None則使用默認配置
            default_mock_level (str, optional): 默認Mock級別，可選值為"none", "partial", "full"
            config_data (dict, optional): 直接提供的配置數據，如果提供則優先使用此數據
        """
        self.default_mock_level = default_mock_level
        if config_data is not None:
            self.config = config_data
        else:
            self.config = self._load_config(config_file)
    
    def _load_config(self, config_file):
        """加載配置文件
        
        Args:
            config_file (str): 配置文件路徑
            
        Returns:
            dict: 配置信息
        """
        if not config_file:
            return {
                "use_mock": True,
                "mock_level": self.default_mock_level,
                "components": {}
            }
        
        if not os.path.exists(config_file):
            print(f"Warning: Mock配置文件 {config_file} 不存在，使用默認配置")
            return {
                "use_mock": True,
                "mock_level": self.default_mock_level,
                "components": {}
            }
        
        try:
            if config_file.endswith(".json"):
                with open(config_file, "r") as f:
                    return json.load(f)
            elif config_file.endswith((".yaml", ".yml")):
                with open(config_file, "r") as f:
                    return yaml.safe_load(f)
            else:
                print(f"Warning: 不支持的配置文件格式 {config_file}，使用默認配置")
                return {
                    "use_mock": True,
                    "mock_level": self.default_mock_level,
                    "components": {}
                }
        except Exception as e:
            print(f"Error: 加載配置文件失敗: {e}，使用默認配置")
            return {
                "use_mock": True,
                "mock_level": self.default_mock_level,
                "components": {}
            }
    
    def should_mock(self, component_name):
        """判斷是否應該mock特定組件
        
        Args:
            component_name (str): 組件名稱
            
        Returns:
            bool: 是否應該mock該組件
        """
        # 如果全局禁用mock，則不mock任何組件
        if not self.config.get("use_mock", True):
            return False
        
        # 如果是完全mock模式，則mock所有組件
        if self.config.get("mock_level") == "full":
            return True
        
        # 如果是無mock模式，則不mock任何組件
        if self.config.get("mock_level") == "none":
            return False
        
        # 對於部分mock模式，根據組件配置決定
        component_config = self.config.get("components", {}).get(component_name, {})
        return component_config.get("mock", False)
    
    def get_mock_data(self, component_name, data_key=None):
        """獲取組件的mock數據
        
        Args:
            component_name (str): 組件名稱
            data_key (str, optional): 數據鍵名，如果為None則返回該組件的所有mock數據
            
        Returns:
            any: Mock數據
        """
        component_config = self.config.get("components", {}).get(component_name, {})
        mock_data = component_config.get("mock_data", {})
        
        if data_key is None:
            return mock_data
        
        return mock_data.get(data_key)
    
    def set_mock_level(self, level):
        """設置全局Mock級別
        
        Args:
            level (str): Mock級別，可選值為"none", "partial", "full"
            
        Returns:
            bool: 設置是否成功
        """
        if level not in ["none", "partial", "full"]:
            print(f"Warning: 無效的Mock級別 {level}，有效值為 none, partial, full")
            return False
        
        self.config["mock_level"] = level
        return True
    
    def enable_component_mock(self, component_name, enable=True):
        """啟用或禁用特定組件的mock
        
        Args:
            component_name (str): 組件名稱
            enable (bool, optional): 是否啟用mock
            
        Returns:
            None
        """
        if "components" not in self.config:
            self.config["components"] = {}
        
        if component_name not in self.config["components"]:
            self.config["components"][component_name] = {}
        
        self.config["components"][component_name]["mock"] = enable
    
    def save_config(self, config_file):
        """保存配置到文件
        
        Args:
            config_file (str): 配置文件路徑
            
        Returns:
            bool: 保存是否成功
        """
        try:
            directory = os.path.dirname(config_file)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            if config_file.endswith(".json"):
                with open(config_file, "w") as f:
                    json.dump(self.config, f, indent=2)
            elif config_file.endswith((".yaml", ".yml")):
                with open(config_file, "w") as f:
                    yaml.dump(self.config, f)
            else:
                print(f"Warning: 不支持的配置文件格式 {config_file}")
                return False
            
            return True
        except Exception as e:
            print(f"Error: 保存配置文件失敗: {e}")
            return False


# 默認配置實例
default_mock_config = MockConfig()


