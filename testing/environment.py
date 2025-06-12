"""
環境抽象層 - 提供統一的環境接口

此模組用於解決PowerAutomation測試框架中的真實環境與Mock環境切換問題，
提供統一的環境抽象層，使測試代碼可以無縫切換不同環境。
"""

from testing.mock_config import default_mock_config


class Environment:
    """環境抽象層
    
    為測試提供統一的環境接口，根據配置自動切換真實環境或Mock環境。
    
    屬性:
        mock_config: Mock配置對象
    """
    
    def __init__(self, mock_config=None):
        """初始化環境抽象層
        
        Args:
            mock_config: Mock配置對象，如果為None則使用默認配置
        """
        self.mock_config = mock_config or default_mock_config
    
    def get_file_system(self):
        """獲取文件系統接口
        
        根據配置返回真實文件系統或Mock文件系統
        
        Returns:
            FileSystem: 文件系統接口
        """
        if self.mock_config.should_mock("file_system"):
            from testing.mocks.file_system import MockFileSystem
            return MockFileSystem()
        else:
            from shared_core.io.file_system import FileSystem
            return FileSystem()
    
    def get_network(self):
        """獲取網絡接口
        
        根據配置返回真實網絡或Mock網絡
        
        Returns:
            Network: 網絡接口
        """
        if self.mock_config.should_mock("network"):
            from testing.mocks.network import MockNetwork
            return MockNetwork()
        else:
            from shared_core.io.network import Network
            return Network()
    
    def get_database(self):
        """獲取數據庫接口
        
        根據配置返回真實數據庫或Mock數據庫
        
        Returns:
            Database: 數據庫接口
        """
        if self.mock_config.should_mock("database"):
            from testing.mocks.database import MockDatabase
            return MockDatabase()
        else:
            from shared_core.storage.database import Database
            return Database()
    
    def get_video_processor(self):
        """獲取視頻處理器
        
        根據配置返回真實視頻處理器或Mock視頻處理器
        
        Returns:
            VideoProcessor: 視頻處理器
        """
        if self.mock_config.should_mock("video_processor"):
            from testing.mocks.video_processor import MockVideoProcessor
            return MockVideoProcessor()
        else:
            from shared_core.media.video_processor import VideoProcessor
            return VideoProcessor()
    
    def get_workflow_engine(self):
        """獲取工作流引擎
        
        根據配置返回真實工作流引擎或Mock工作流引擎
        
        Returns:
            WorkflowEngine: 工作流引擎
        """
        if self.mock_config.should_mock("workflow_engine"):
            from testing.mocks.workflow_engine import MockWorkflowEngine
            return MockWorkflowEngine()
        else:
            from shared_core.engines.workflow_engine import WorkflowEngine
            return WorkflowEngine()
    
    def get_distributed_coordinator(self):
        """獲取分布式協調器
        
        根據配置返回真實分布式協調器或Mock分布式協調器
        
        Returns:
            DistributedCoordinator: 分布式協調器
        """
        if self.mock_config.should_mock("distributed_coordinator"):
            from testing.mocks.distributed_coordinator import MockDistributedCoordinator
            return MockDistributedCoordinator()
        else:
            from shared_core.engines.distributed_coordinator.coordinator import DistributedCoordinator
            return DistributedCoordinator()


# 默認環境實例
default_environment = Environment()
