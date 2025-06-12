"""
Release自動化測試模組 - 提供Release階段的自動化測試與智能介入機制

此模組實現了PowerAutomation測試框架在Release階段的自動化測試與智能介入機制，
能夠自動檢測代碼變更、觸發相應測試、分析結果並進行智能介入。
"""

import os
import sys
import json
import logging
import datetime
import subprocess
from typing import Dict, Any, List, Optional, Tuple, Union

# 添加項目根目錄到Python路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

# 導入測試框架組件
from testing.automated_testing_framework.intelligent_intervention.intervention import IntelligentIntervention
from testing.test_case import TestCase


class ReleaseTestAutomation:
    """Release測試自動化
    
    負責在Release階段自動觸發測試、分析結果並進行智能介入。
    
    屬性:
        logger (logging.Logger): 日誌記錄器
        intelligent_intervention (IntelligentIntervention): 智能介入實例
    """
    
    def __init__(self):
        """初始化Release測試自動化"""
        self.logger = logging.getLogger("release_test_automation")
        self.intelligent_intervention = IntelligentIntervention()
    
    def detect_changes(self, base_commit: str, head_commit: str) -> List[str]:
        """檢測代碼變更
        
        Args:
            base_commit: 基準提交
            head_commit: 目標提交
            
        Returns:
            List[str]: 變更的文件列表
        """
        self.logger.info(f"檢測代碼變更: {base_commit}..{head_commit}")
        
        try:
            # 使用git diff獲取變更的文件列表
            cmd = ["git", "diff", "--name-only", f"{base_commit}..{head_commit}"]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            changed_files = result.stdout.strip().split('\n')
            
            # 過濾空行
            changed_files = [f for f in changed_files if f]
            
            self.logger.info(f"檢測到 {len(changed_files)} 個變更文件")
            return changed_files
        
        except subprocess.CalledProcessError as e:
            self.logger.error(f"檢測代碼變更失敗: {e}")
            return []
    
    def select_tests_for_changes(self, changed_files: List[str]) -> List[str]:
        """根據變更選擇測試
        
        Args:
            changed_files: 變更的文件列表
            
        Returns:
            List[str]: 需要運行的測試ID列表
        """
        self.logger.info(f"根據 {len(changed_files)} 個變更文件選擇測試")
        
        # 在實際實現中，這裡會根據變更文件分析需要運行哪些測試
        # 這裡僅模擬選擇過程
        
        # 模擬選擇結果
        selected_tests = []
        
        for file_path in changed_files:
            # 根據文件路徑選擇相關測試
            if file_path.endswith('.py'):
                # 提取模塊名稱
                module_name = os.path.splitext(os.path.basename(file_path))[0]
                
                # 根據模塊名稱選擇測試
                if 'workflow' in module_name:
                    selected_tests.append('TC_001_workflow_basic')
                elif 'video' in module_name:
                    selected_tests.append('TC_002_video_processing')
                elif 'distributed' in module_name:
                    selected_tests.append('TC_003_distributed_coordination')
        
        # 去重
        selected_tests = list(set(selected_tests))
        
        self.logger.info(f"選擇了 {len(selected_tests)} 個測試")
        return selected_tests
    
    def run_selected_tests(self, test_ids: List[str]) -> List[Dict[str, Any]]:
        """運行選定的測試
        
        Args:
            test_ids: 測試ID列表
            
        Returns:
            List[Dict[str, Any]]: 測試結果列表
        """
        self.logger.info(f"運行 {len(test_ids)} 個選定的測試")
        
        # 在實際實現中，這裡會加載並運行選定的測試
        # 這裡僅模擬運行過程
        
        # 模擬測試結果
        test_results = []
        
        for test_id in test_ids:
            # 模擬測試結果
            result = {
                "test_id": test_id,
                "name": f"Test {test_id}",
                "description": f"Description for {test_id}",
                "success": test_id != 'TC_003_distributed_coordination',  # 模擬一個失敗的測試
                "start_time": datetime.datetime.now().isoformat(),
                "end_time": datetime.datetime.now().isoformat(),
                "duration": 1.5
            }
            
            # 如果測試失敗，添加錯誤信息
            if not result["success"]:
                result["error"] = "ModuleNotFoundError: No module named 'distributed_coordinator'"
                result["error_type"] = "ModuleNotFoundError"
            
            test_results.append(result)
        
        self.logger.info(f"完成 {len(test_results)} 個測試")
        return test_results
    
    def process_test_results(self, test_results: List[Dict[str, Any]], auto_apply: bool = False) -> Dict[str, Any]:
        """處理測試結果
        
        Args:
            test_results: 測試結果列表
            auto_apply: 是否自動應用修正方案
            
        Returns:
            Dict[str, Any]: 處理結果
        """
        self.logger.info(f"處理 {len(test_results)} 個測試結果")
        
        # 使用智能介入處理測試結果
        intervention_result = self.intelligent_intervention.process_test_results(test_results, auto_apply)
        
        return intervention_result
    
    def generate_release_report(self, test_results: List[Dict[str, Any]], intervention_result: Dict[str, Any]) -> Dict[str, Any]:
        """生成Release報告
        
        Args:
            test_results: 測試結果列表
            intervention_result: 智能介入結果
            
        Returns:
            Dict[str, Any]: Release報告
        """
        self.logger.info("生成Release報告")
        
        # 計算測試統計信息
        total_tests = len(test_results)
        successful_tests = sum(1 for result in test_results if result.get("success", False))
        failed_tests = total_tests - successful_tests
        
        # 計算智能介入統計信息
        problems = intervention_result.get("problems", [])
        fixes = intervention_result.get("fixes", [])
        applied_fixes = intervention_result.get("applied_fixes", [])
        validation_results = intervention_result.get("validation_results", [])
        
        successful_validations = sum(1 for result in validation_results if result.get("success", False))
        
        # 構建報告
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "test_summary": {
                "total": total_tests,
                "successful": successful_tests,
                "failed": failed_tests,
                "success_rate": successful_tests / total_tests if total_tests > 0 else 1.0
            },
            "intervention_summary": {
                "problems_detected": len(problems),
                "fixes_generated": len(fixes),
                "fixes_applied": len(applied_fixes),
                "fixes_validated": len(validation_results),
                "successful_validations": successful_validations,
                "validation_success_rate": successful_validations / len(validation_results) if len(validation_results) > 0 else 1.0
            },
            "release_status": "ready" if failed_tests == 0 or successful_validations == len(validation_results) else "blocked",
            "test_results": test_results,
            "intervention_result": intervention_result
        }
        
        return report
    
    def save_release_report(self, report: Dict[str, Any], output_dir: Optional[str] = None) -> str:
        """保存Release報告
        
        Args:
            report: Release報告
            output_dir: 輸出目錄，如果為None則使用默認目錄
            
        Returns:
            str: 報告文件路徑
        """
        # 確定輸出目錄
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'release_reports')
        
        # 確保輸出目錄存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 構建報告文件路徑
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(output_dir, f"release_report_{timestamp}.json")
        
        # 保存報告
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.logger.info(f"Release報告已保存: {report_file}")
        
        return report_file
    
    def run_release_tests(self, base_commit: str, head_commit: str, auto_apply: bool = False, output_dir: Optional[str] = None) -> Dict[str, Any]:
        """運行Release測試
        
        完整的Release測試流程：檢測變更、選擇測試、運行測試、處理結果、生成報告。
        
        Args:
            base_commit: 基準提交
            head_commit: 目標提交
            auto_apply: 是否自動應用修正方案
            output_dir: 輸出目錄
            
        Returns:
            Dict[str, Any]: Release報告
        """
        self.logger.info(f"開始Release測試: {base_commit}..{head_commit}")
        
        # 檢測代碼變更
        changed_files = self.detect_changes(base_commit, head_commit)
        
        # 如果沒有變更，則直接返回
        if not changed_files:
            report = {
                "timestamp": datetime.datetime.now().isoformat(),
                "test_summary": {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "success_rate": 1.0
                },
                "intervention_summary": {
                    "problems_detected": 0,
                    "fixes_generated": 0,
                    "fixes_applied": 0,
                    "fixes_validated": 0,
                    "successful_validations": 0,
                    "validation_success_rate": 1.0
                },
                "release_status": "ready",
                "message": "未檢測到代碼變更",
                "changed_files": [],
                "test_results": [],
                "intervention_result": {}
            }
            
            # 保存報告
            if output_dir:
                self.save_release_report(report, output_dir)
            
            return report
        
        # 根據變更選擇測試
        test_ids = self.select_tests_for_changes(changed_files)
        
        # 如果沒有需要運行的測試，則直接返回
        if not test_ids:
            report = {
                "timestamp": datetime.datetime.now().isoformat(),
                "test_summary": {
                    "total": 0,
                    "successful": 0,
                    "failed": 0,
                    "success_rate": 1.0
                },
                "intervention_summary": {
                    "problems_detected": 0,
                    "fixes_generated": 0,
                    "fixes_applied": 0,
                    "fixes_validated": 0,
                    "successful_validations": 0,
                    "validation_success_rate": 1.0
                },
                "release_status": "ready",
                "message": "未選擇需要運行的測試",
                "changed_files": changed_files,
                "test_results": [],
                "intervention_result": {}
            }
            
            # 保存報告
            if output_dir:
                self.save_release_report(report, output_dir)
            
            return report
        
        # 運行選定的測試
        test_results = self.run_selected_tests(test_ids)
        
        # 處理測試結果
        intervention_result = self.process_test_results(test_results, auto_apply)
        
        # 生成Release報告
        report = self.generate_release_report(test_results, intervention_result)
        
        # 添加變更信息
        report["changed_files"] = changed_files
        
        # 保存報告
        if output_dir:
            self.save_release_report(report, output_dir)
        
        return report


# 默認Release測試自動化實例
default_release_test_automation = ReleaseTestAutomation()


def main():
    """命令行入口函數"""
    import argparse
    
    parser = argparse.ArgumentParser(description='PowerAutomation Release測試自動化')
    parser.add_argument('--base', required=True, help='基準提交')
    parser.add_argument('--head', required=True, help='目標提交')
    parser.add_argument('--auto-apply', action='store_true', help='自動應用修正方案')
    parser.add_argument('--output-dir', help='輸出目錄')
    
    args = parser.parse_args()
    
    # 配置日誌
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 運行Release測試
    automation = ReleaseTestAutomation()
    report = automation.run_release_tests(args.base, args.head, args.auto_apply, args.output_dir)
    
    # 輸出報告摘要
    print(f"Release狀態: {report['release_status']}")
    print(f"測試總數: {report['test_summary']['total']}")
    print(f"成功測試: {report['test_summary']['successful']}")
    print(f"失敗測試: {report['test_summary']['failed']}")
    print(f"檢測到的問題: {report['intervention_summary']['problems_detected']}")
    print(f"生成的修正方案: {report['intervention_summary']['fixes_generated']}")
    print(f"應用的修正方案: {report['intervention_summary']['fixes_applied']}")
    print(f"成功驗證的修正方案: {report['intervention_summary']['successful_validations']}")
    
    # 返回狀態碼
    sys.exit(0 if report['release_status'] == 'ready' else 1)


if __name__ == '__main__':
    main()
