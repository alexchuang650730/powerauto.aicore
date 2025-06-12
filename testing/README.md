# PowerAutomation 測試框架遷移指南

## 概述

本文檔提供了將PowerAutomation測試框架從原始倉庫(powerauto.ai_0.53)遷移到新倉庫(powerauto.aicore)的詳細指南。新的測試框架採用三層結構設計，並實現了完整的智能測試介入閉環機制。

## 目錄結構

```
testing/
├── automated_testing_framework/        # 自動化測試框架核心
│   ├── intelligent_intervention/       # 智能介入模組
│   │   ├── __init__.py
│   │   └── intervention.py             # 智能介入核心邏輯
│   └── release_automation/             # Release自動化測試
│       ├── __init__.py
│       └── release_test_automation.py  # Release自動化核心邏輯
├── cli/                                # 命令行工具
│   ├── __init__.py
│   └── intelligent_engine_cli.py       # 智能引擎CLI入口
├── test_cases/                         # 測試用例目錄
│   ├── layer1_unit_code_quality/       # 第1層：單元測試 + 代碼質量
│   ├── layer2_integration_agent_collab/ # 第2層：集成測試 + 智能體協作
│   └── layer3_mcp_compliance_standard/  # 第3層：MCP合規測試 + 標準化驗證
├── dependency_manager.py               # 依賴管理模組
├── environment.py                      # 環境抽象層
├── import_helpers.py                   # 導入輔助模組
├── mock_config.py                      # Mock配置系統
├── test_case.py                        # 測試用例基類
├── test_registry.py                    # 測試用例註冊表
└── README.md                           # 本文檔
```

## 核心組件說明

### 1. 三層測試結構

測試框架採用三層結構設計，每層專注於不同級別的測試：

- **第1層：單元測試 + 代碼質量**
  - 驗證各個組件的獨立功能
  - 檢查代碼質量、風格和文檔覆蓋率
  - 位於 `test_cases/layer1_unit_code_quality/`

- **第2層：集成測試 + 智能體協作**
  - 驗證多個組件之間的協作與交互
  - 測試智能體之間的協同工作
  - 位於 `test_cases/layer2_integration_agent_collab/`

- **第3層：MCP合規測試 + 標準化驗證**
  - 確保系統符合MCP合規標準
  - 驗證系統是否滿足各種標準化要求
  - 位於 `test_cases/layer3_mcp_compliance_standard/`

### 2. 智能測試介入閉環

測試框架實現了完整的智能測試介入閉環機制：

```
Release發現問題 → 智能引擎主動介入 → 修正test cases並移除錯誤代碼 → 重新測試 → 問題解決 → 交給Release Manager
```

核心組件包括：

- **問題檢測器**：分析測試結果，檢測問題
- **修正生成器**：為檢測到的問題生成修正方案
- **自動修正器**：應用修正方案
- **修正驗證器**：驗證修正效果

### 3. 基礎設施模組

- **import_helpers.py**：解決路徑引用問題，提供統一的導入方式
- **mock_config.py**：提供統一的Mock策略管理，支持不同級別的Mock
- **environment.py**：實現真實環境與Mock環境的無縫切換
- **dependency_manager.py**：提供分層依賴結構和智能化的安裝機制
- **test_case.py**：測試用例基類，提供統一的測試用例接口
- **test_registry.py**：測試用例註冊表，提供統一的測試用例管理

### 4. 智能引擎CLI

智能引擎CLI是整個測試框架的統一入口，位於 `cli/intelligent_engine_cli.py`，提供以下功能：

- 測試用例的發現、註冊和運行
- 智能介入的配置和控制
- Release自動化測試的觸發和監控
- 測試結果的分析和報告生成

## 引用路徑調整

由於測試框架從原始倉庫遷移到新倉庫，需要調整以下引用路徑：

1. **絕對路徑調整**：
   - 從 `from powerauto.ai_0.53.tests.xxx import yyy` 
   - 改為 `from powerauto.aicore.testing.xxx import yyy`

2. **相對路徑調整**：
   - 從 `from ...tests.xxx import yyy` 
   - 改為 `from ...testing.xxx import yyy`

3. **文件路徑調整**：
   - 從 `/path/to/powerauto.ai_0.53/tests/xxx` 
   - 改為 `/path/to/powerauto.aicore/testing/xxx`

## 使用方法

### 1. 運行單個測試用例

```bash
cd /path/to/powerauto.aicore
python -m testing.cli.intelligent_engine_cli run --test-id TC_001_workflow_engine_unit
```

### 2. 運行特定層級的測試

```bash
cd /path/to/powerauto.aicore
python -m testing.cli.intelligent_engine_cli run --layer 1  # 運行第1層測試
```

### 3. 啟動Release自動化測試

```bash
cd /path/to/powerauto.aicore
python -m testing.cli.intelligent_engine_cli release --version v1.0.0
```

### 4. 啟用智能介入

```bash
cd /path/to/powerauto.aicore
python -m testing.cli.intelligent_engine_cli run --enable-intervention
```

## 環境適配建議

1. **依賴管理**：
   - 使用 `testing/dependency_manager.py` 進行依賴安裝
   - 根據需要選擇輕量級或完整依賴安裝

2. **環境變量**：
   - 設置 `POWERAUTO_ROOT` 環境變量指向倉庫根目錄
   - 設置 `POWERAUTO_ENV` 環境變量指定運行環境（dev/test/prod）

3. **資源需求**：
   - 建議使用至少8GB RAM的環境
   - 存儲空間至少需要20GB
   - 如需運行完整的機器學習相關測試，建議使用GPU環境

## 常見問題

1. **導入錯誤**：
   - 問題：`ModuleNotFoundError: No module named 'powerauto.aicore'`
   - 解決：確保Python路徑中包含倉庫根目錄，或使用 `import_helpers.py` 中的輔助函數

2. **依賴缺失**：
   - 問題：`ImportError: No module named 'xxx'`
   - 解決：使用 `dependency_manager.py` 安裝缺失的依賴

3. **權限問題**：
   - 問題：無法訪問或修改測試數據目錄
   - 解決：確保當前用戶對 `testing` 目錄及其子目錄有讀寫權限

## 後續擴展

1. **添加新測試用例**：
   - 繼承 `test_case.py` 中的適當基類
   - 實現 `setup`、`run` 和 `teardown` 方法
   - 使用 `test_registry.py` 註冊新測試用例

2. **擴展智能介入能力**：
   - 在 `intelligent_intervention` 目錄下添加新的檢測器或修正器
   - 更新 `intervention.py` 中的介入策略

3. **自定義Release自動化流程**：
   - 修改 `release_test_automation.py` 中的自動化流程
   - 添加新的Release階段或檢查點

## 聯繫與支持

如有任何問題或需要支持，請聯繫PowerAutomation測試框架維護團隊。
