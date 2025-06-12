"""
依賴管理模組 - 提供智能化的依賴安裝與管理

此模組用於解決PowerAutomation測試框架中的依賴管理問題，
提供分層依賴結構和智能化的安裝機制，根據系統資源自動選擇合適的依賴集。
"""

import os
import sys
import platform
import subprocess
import logging
from typing import Dict, Any, List, Optional

# 配置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dependency_manager")

# 依賴層級定義
DEPENDENCY_LEVELS = {
    "core": "最小核心依賴，僅包含運行基本測試所需的包",
    "test": "測試相關依賴，包含pytest等測試框架",
    "ml": "機器學習相關依賴，包含torch等大型機器學習庫",
    "visual": "視覺分析相關依賴，包含opencv等視覺處理庫",
    "full": "完整依賴集合，包含所有功能所需的依賴"
}

# 依賴層級順序（從小到大）
DEPENDENCY_LEVEL_ORDER = ["core", "test", "ml", "visual", "full"]


class DependencyManager:
    """依賴管理器
    
    負責管理PowerAutomation測試框架的依賴，提供智能化的安裝機制。
    
    屬性:
        project_root (str): 項目根目錄路徑
        requirements_dir (str): 依賴文件目錄路徑
    """
    
    def __init__(self, project_root: Optional[str] = None):
        """初始化依賴管理器
        
        Args:
            project_root: 項目根目錄路徑，如果為None則自動檢測
        """
        if project_root is None:
            # 自動檢測項目根目錄
            self.project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        else:
            self.project_root = os.path.abspath(project_root)
        
        # 依賴文件目錄
        self.requirements_dir = os.path.join(self.project_root, 'requirements')
        
        # 確保依賴文件目錄存在
        os.makedirs(self.requirements_dir, exist_ok=True)
    
    def get_system_resources(self) -> Dict[str, Any]:
        """獲取系統資源信息
        
        Returns:
            Dict[str, Any]: 系統資源信息，包含內存、CPU核心數和平台
        """
        try:
            import psutil
            mem = psutil.virtual_memory()
            memory_gb = mem.total / (1024**3)
        except ImportError:
            # 如果psutil不可用，使用保守估計
            memory_gb = 4.0
        
        return {
            "memory_gb": memory_gb,
            "cpu_count": os.cpu_count() or 2,
            "platform": platform.system()
        }
    
    def select_dependency_level(self, resources: Dict[str, Any]) -> str:
        """根據系統資源選擇合適的依賴級別
        
        Args:
            resources: 系統資源信息
            
        Returns:
            str: 依賴級別名稱
        """
        memory_gb = resources["memory_gb"]
        
        if memory_gb < 4:
            return "core"
        elif memory_gb < 8:
            return "test"
        elif memory_gb < 16:
            return "ml"
        else:
            return "full"
    
    def get_requirements_file(self, level: str) -> str:
        """獲取指定級別的依賴文件路徑
        
        Args:
            level: 依賴級別名稱
            
        Returns:
            str: 依賴文件路徑
        """
        if level not in DEPENDENCY_LEVELS:
            raise ValueError(f"無效的依賴級別: {level}，有效值為: {', '.join(DEPENDENCY_LEVELS.keys())}")
        
        return os.path.join(self.requirements_dir, f"requirements-{level}.txt")
    
    def create_requirements_files(self) -> None:
        """創建分層依賴文件
        
        如果依賴文件不存在，則創建基本的依賴文件結構。
        """
        # 核心依賴
        core_file = self.get_requirements_file("core")
        if not os.path.exists(core_file):
            with open(core_file, 'w') as f:
                f.write("# PowerAutomation 核心依賴\n")
                f.write("# 最小運行集，僅包含基本功能所需的依賴\n\n")
                f.write("fastapi>=0.68.0\n")
                f.write("uvicorn>=0.15.0\n")
                f.write("pydantic>=1.8.2\n")
                f.write("sqlalchemy>=1.4.23\n")
                f.write("requests>=2.26.0\n")
                f.write("aiohttp>=3.7.4\n")
        
        # 測試依賴
        test_file = self.get_requirements_file("test")
        if not os.path.exists(test_file):
            with open(test_file, 'w') as f:
                f.write("# PowerAutomation 測試依賴\n")
                f.write("# 包含測試框架和工具所需的依賴\n\n")
                f.write("-r requirements-core.txt\n\n")
                f.write("pytest>=6.2.5\n")
                f.write("pytest-asyncio>=0.15.1\n")
                f.write("pytest-mock>=3.6.1\n")
                f.write("coverage>=5.5\n")
                f.write("flake8>=3.9.2\n")
                f.write("black>=21.8b0\n")
        
        # 機器學習依賴
        ml_file = self.get_requirements_file("ml")
        if not os.path.exists(ml_file):
            with open(ml_file, 'w') as f:
                f.write("# PowerAutomation 機器學習依賴\n")
                f.write("# 包含機器學習相關功能所需的依賴\n\n")
                f.write("-r requirements-test.txt\n\n")
                f.write("numpy>=1.21.2\n")
                f.write("pandas>=1.3.2\n")
                f.write("scikit-learn>=0.24.2\n")
                f.write("torch>=1.9.0\n")
                f.write("transformers>=4.9.2\n")
        
        # 視覺分析依賴
        visual_file = self.get_requirements_file("visual")
        if not os.path.exists(visual_file):
            with open(visual_file, 'w') as f:
                f.write("# PowerAutomation 視覺分析依賴\n")
                f.write("# 包含視覺處理和分析功能所需的依賴\n\n")
                f.write("-r requirements-ml.txt\n\n")
                f.write("opencv-python>=4.5.3\n")
                f.write("pillow>=8.3.1\n")
                f.write("matplotlib>=3.4.3\n")
                f.write("seaborn>=0.11.2\n")
        
        # 完整依賴
        full_file = self.get_requirements_file("full")
        if not os.path.exists(full_file):
            with open(full_file, 'w') as f:
                f.write("# PowerAutomation 完整依賴\n")
                f.write("# 包含所有功能所需的依賴\n\n")
                f.write("-r requirements-visual.txt\n\n")
                f.write("# 額外依賴\n")
                f.write("flask>=2.0.1\n")
                f.write("django>=3.2.6\n")
                f.write("celery>=5.1.2\n")
    
    def install_dependencies(self, level: Optional[str] = None, pip_args: Optional[List[str]] = None) -> bool:
        """安裝依賴
        
        Args:
            level: 依賴級別名稱，如果為None則自動選擇
            pip_args: 額外的pip參數
            
        Returns:
            bool: 安裝是否成功
        """
        # 確保依賴文件存在
        self.create_requirements_files()
        
        # 如果未指定級別，則根據系統資源自動選擇
        if level is None:
            resources = self.get_system_resources()
            level = self.select_dependency_level(resources)
            logger.info(f"根據系統資源自動選擇依賴級別: {level} (內存: {resources['memory_gb']:.1f}GB)")
        
        # 獲取依賴文件路徑
        requirements_file = self.get_requirements_file(level)
        if not os.path.exists(requirements_file):
            logger.error(f"依賴文件不存在: {requirements_file}")
            return False
        
        # 構建pip命令
        cmd = [sys.executable, "-m", "pip", "install", "-r", requirements_file]
        if pip_args:
            cmd.extend(pip_args)
        
        # 執行pip安裝
        logger.info(f"開始安裝依賴: {level}")
        logger.info(f"執行命令: {' '.join(cmd)}")
        
        try:
            subprocess.run(cmd, check=True)
            logger.info(f"依賴安裝成功: {level}")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"依賴安裝失敗: {e}")
            return False
    
    def install_dependencies_progressively(self, target_level: str = "full", pip_args: Optional[List[str]] = None) -> bool:
        """逐步安裝依賴
        
        從低級別開始，逐步安裝到目標級別，這樣可以在資源不足時及時停止。
        
        Args:
            target_level: 目標依賴級別
            pip_args: 額外的pip參數
            
        Returns:
            bool: 安裝是否成功
        """
        if target_level not in DEPENDENCY_LEVELS:
            raise ValueError(f"無效的依賴級別: {target_level}，有效值為: {', '.join(DEPENDENCY_LEVELS.keys())}")
        
        # 確定需要安裝的級別
        target_index = DEPENDENCY_LEVEL_ORDER.index(target_level)
        levels_to_install = DEPENDENCY_LEVEL_ORDER[:target_index + 1]
        
        # 逐步安裝
        for level in levels_to_install:
            logger.info(f"開始安裝 {level} 級別依賴...")
            success = self.install_dependencies(level, pip_args)
            if not success:
                logger.error(f"安裝 {level} 級別依賴失敗，停止後續安裝")
                return False
        
        return True


# 默認依賴管理器實例
default_dependency_manager = DependencyManager()


def main():
    """命令行入口函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PowerAutomation 依賴管理工具')
    parser.add_argument('--level', choices=DEPENDENCY_LEVELS.keys(), help='依賴級別')
    parser.add_argument('--progressive', action='store_true', help='逐步安裝依賴')
    parser.add_argument('--no-cache-dir', action='store_true', help='禁用pip緩存')
    
    args = parser.parse_args()
    
    # 準備pip參數
    pip_args = []
    if args.no_cache_dir:
        pip_args.append('--no-cache-dir')
    
    # 創建依賴管理器
    manager = DependencyManager()
    
    # 安裝依賴
    if args.progressive:
        target_level = args.level or "full"
        success = manager.install_dependencies_progressively(target_level, pip_args)
    else:
        success = manager.install_dependencies(args.level, pip_args)
    
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
