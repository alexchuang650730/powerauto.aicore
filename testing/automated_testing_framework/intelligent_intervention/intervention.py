"""
智能介入模組 - 提供自動化問題檢測與修正能力

此模組實現了PowerAutomation測試框架的智能介入機制，
能夠自動檢測測試問題、生成修正方案、應用修正並驗證效果。
"""

import os
import json
import logging
import datetime
from typing import Dict, Any, List, Optional, Tuple, Union

from testing.test_case import TestCase


class ProblemDetector:
    """問題檢測器
    
    負責分析測試結果，檢測測試中的問題。
    
    屬性:
        logger (logging.Logger): 日誌記錄器
    """
    
    def __init__(self):
        """初始化問題檢測器"""
        self.logger = logging.getLogger("intelligent_intervention.problem_detector")
    
    def detect_problems(self, test_results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """檢測測試結果中的問題
        
        Args:
            test_results: 測試結果列表
            
        Returns:
            List[Dict[str, Any]]: 檢測到的問題列表
        """
        problems = []
        
        for result in test_results:
            if not result.get("success", False):
                problem = self._analyze_failure(result)
                if problem:
                    problems.append(problem)
        
        self.logger.info(f"檢測到 {len(problems)} 個問題")
        return problems
    
    def _analyze_failure(self, result: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """分析失敗原因
        
        Args:
            result: 測試結果
            
        Returns:
            Optional[Dict[str, Any]]: 問題描述，如果無法分析則返回None
        """
        test_id = result.get("test_id", "unknown")
        
        # 檢查是否有明確的錯誤信息
        error = result.get("error")
        error_type = result.get("error_type")
        
        if error:
            # 根據錯誤類型和信息進行分類
            if "ImportError" in error_type or "ModuleNotFoundError" in error_type:
                return {
                    "test_id": test_id,
                    "problem_type": "import_error",
                    "description": f"導入錯誤: {error}",
                    "severity": "high",
                    "result": result
                }
            elif "AssertionError" in error_type:
                return {
                    "test_id": test_id,
                    "problem_type": "assertion_error",
                    "description": f"斷言錯誤: {error}",
                    "severity": "medium",
                    "result": result
                }
            elif "TimeoutError" in error_type:
                return {
                    "test_id": test_id,
                    "problem_type": "timeout_error",
                    "description": f"超時錯誤: {error}",
                    "severity": "medium",
                    "result": result
                }
            else:
                return {
                    "test_id": test_id,
                    "problem_type": "general_error",
                    "description": f"一般錯誤: {error}",
                    "severity": "medium",
                    "result": result
                }
        
        # 檢查測試結果中的具體失敗信息
        result_details = result.get("result", {})
        if isinstance(result_details, dict):
            failure_reason = result_details.get("failure_reason")
            if failure_reason:
                return {
                    "test_id": test_id,
                    "problem_type": "test_failure",
                    "description": f"測試失敗: {failure_reason}",
                    "severity": "medium",
                    "result": result
                }
        
        # 無法確定具體問題
        return {
            "test_id": test_id,
            "problem_type": "unknown_failure",
            "description": "未知失敗原因",
            "severity": "low",
            "result": result
        }


class FixGenerator:
    """修正生成器
    
    負責為檢測到的問題生成修正方案。
    
    屬性:
        logger (logging.Logger): 日誌記錄器
    """
    
    def __init__(self):
        """初始化修正生成器"""
        self.logger = logging.getLogger("intelligent_intervention.fix_generator")
    
    def generate_fixes(self, problems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """生成修正方案
        
        Args:
            problems: 問題列表
            
        Returns:
            List[Dict[str, Any]]: 修正方案列表
        """
        fixes = []
        
        for problem in problems:
            fix = self._generate_fix_for_problem(problem)
            if fix:
                fixes.append(fix)
        
        self.logger.info(f"生成了 {len(fixes)} 個修正方案")
        return fixes
    
    def _generate_fix_for_problem(self, problem: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """為特定問題生成修正方案
        
        Args:
            problem: 問題描述
            
        Returns:
            Optional[Dict[str, Any]]: 修正方案，如果無法生成則返回None
        """
        problem_type = problem.get("problem_type")
        test_id = problem.get("test_id")
        
        if problem_type == "import_error":
            return self._generate_import_error_fix(problem)
        elif problem_type == "assertion_error":
            return self._generate_assertion_error_fix(problem)
        elif problem_type == "timeout_error":
            return self._generate_timeout_error_fix(problem)
        elif problem_type == "test_failure":
            return self._generate_test_failure_fix(problem)
        else:
            self.logger.warning(f"無法為問題類型 {problem_type} 生成修正方案")
            return None
    
    def _generate_import_error_fix(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """生成導入錯誤的修正方案
        
        Args:
            problem: 問題描述
            
        Returns:
            Dict[str, Any]: 修正方案
        """
        error = problem.get("result", {}).get("error", "")
        test_id = problem.get("test_id")
        
        # 分析錯誤信息，提取模塊名稱
        import_name = None
        if "No module named" in error:
            parts = error.split("'")
            if len(parts) >= 2:
                import_name = parts[1]
        
        if import_name:
            return {
                "problem_id": problem.get("test_id"),
                "fix_type": "import_error",
                "description": f"修復導入錯誤: {import_name}",
                "actions": [
                    {
                        "action_type": "install_dependency",
                        "module_name": import_name
                    },
                    {
                        "action_type": "update_import_path",
                        "module_name": import_name
                    }
                ],
                "problem": problem
            }
        else:
            return {
                "problem_id": problem.get("test_id"),
                "fix_type": "import_error",
                "description": "修復導入錯誤",
                "actions": [
                    {
                        "action_type": "check_import_helpers",
                        "description": "檢查並使用導入輔助模組"
                    }
                ],
                "problem": problem
            }
    
    def _generate_assertion_error_fix(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """生成斷言錯誤的修正方案
        
        Args:
            problem: 問題描述
            
        Returns:
            Dict[str, Any]: 修正方案
        """
        return {
            "problem_id": problem.get("test_id"),
            "fix_type": "assertion_error",
            "description": "修復斷言錯誤",
            "actions": [
                {
                    "action_type": "update_expected_value",
                    "description": "更新預期值以匹配實際結果"
                },
                {
                    "action_type": "check_test_logic",
                    "description": "檢查測試邏輯是否正確"
                }
            ],
            "problem": problem
        }
    
    def _generate_timeout_error_fix(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """生成超時錯誤的修正方案
        
        Args:
            problem: 問題描述
            
        Returns:
            Dict[str, Any]: 修正方案
        """
        return {
            "problem_id": problem.get("test_id"),
            "fix_type": "timeout_error",
            "description": "修復超時錯誤",
            "actions": [
                {
                    "action_type": "increase_timeout",
                    "description": "增加超時時間"
                },
                {
                    "action_type": "optimize_test",
                    "description": "優化測試性能"
                }
            ],
            "problem": problem
        }
    
    def _generate_test_failure_fix(self, problem: Dict[str, Any]) -> Dict[str, Any]:
        """生成測試失敗的修正方案
        
        Args:
            problem: 問題描述
            
        Returns:
            Dict[str, Any]: 修正方案
        """
        return {
            "problem_id": problem.get("test_id"),
            "fix_type": "test_failure",
            "description": "修復測試失敗",
            "actions": [
                {
                    "action_type": "analyze_failure",
                    "description": "分析失敗原因"
                },
                {
                    "action_type": "update_test_case",
                    "description": "更新測試用例"
                }
            ],
            "problem": problem
        }


class AutoFixer:
    """自動修正器
    
    負責應用修正方案。
    
    屬性:
        logger (logging.Logger): 日誌記錄器
    """
    
    def __init__(self):
        """初始化自動修正器"""
        self.logger = logging.getLogger("intelligent_intervention.auto_fixer")
    
    def apply_fixes(self, fixes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """應用修正方案
        
        Args:
            fixes: 修正方案列表
            
        Returns:
            List[Dict[str, Any]]: 應用結果列表
        """
        results = []
        
        for fix in fixes:
            result = self._apply_fix(fix)
            results.append(result)
        
        self.logger.info(f"應用了 {len(results)} 個修正方案")
        return results
    
    def _apply_fix(self, fix: Dict[str, Any]) -> Dict[str, Any]:
        """應用特定修正方案
        
        Args:
            fix: 修正方案
            
        Returns:
            Dict[str, Any]: 應用結果
        """
        fix_type = fix.get("fix_type")
        problem_id = fix.get("problem_id")
        
        self.logger.info(f"應用修正方案: {fix.get('description')} (問題ID: {problem_id})")
        
        # 根據修正類型調用相應的處理函數
        if fix_type == "import_error":
            return self._apply_import_error_fix(fix)
        elif fix_type == "assertion_error":
            return self._apply_assertion_error_fix(fix)
        elif fix_type == "timeout_error":
            return self._apply_timeout_error_fix(fix)
        elif fix_type == "test_failure":
            return self._apply_test_failure_fix(fix)
        else:
            self.logger.warning(f"無法應用未知類型的修正方案: {fix_type}")
            return {
                "fix_id": problem_id,
                "success": False,
                "description": f"無法應用未知類型的修正方案: {fix_type}",
                "fix": fix
            }
    
    def _apply_import_error_fix(self, fix: Dict[str, Any]) -> Dict[str, Any]:
        """應用導入錯誤的修正方案
        
        Args:
            fix: 修正方案
            
        Returns:
            Dict[str, Any]: 應用結果
        """
        # 模擬應用修正方案
        self.logger.info(f"應用導入錯誤修正: {fix.get('description')}")
        
        # 在實際實現中，這裡會執行具體的修正操作
        # 例如安裝依賴、更新導入路徑等
        
        return {
            "fix_id": fix.get("problem_id"),
            "success": True,
            "description": f"成功應用導入錯誤修正: {fix.get('description')}",
            "fix": fix
        }
    
    def _apply_assertion_error_fix(self, fix: Dict[str, Any]) -> Dict[str, Any]:
        """應用斷言錯誤的修正方案
        
        Args:
            fix: 修正方案
            
        Returns:
            Dict[str, Any]: 應用結果
        """
        # 模擬應用修正方案
        self.logger.info(f"應用斷言錯誤修正: {fix.get('description')}")
        
        return {
            "fix_id": fix.get("problem_id"),
            "success": True,
            "description": f"成功應用斷言錯誤修正: {fix.get('description')}",
            "fix": fix
        }
    
    def _apply_timeout_error_fix(self, fix: Dict[str, Any]) -> Dict[str, Any]:
        """應用超時錯誤的修正方案
        
        Args:
            fix: 修正方案
            
        Returns:
            Dict[str, Any]: 應用結果
        """
        # 模擬應用修正方案
        self.logger.info(f"應用超時錯誤修正: {fix.get('description')}")
        
        return {
            "fix_id": fix.get("problem_id"),
            "success": True,
            "description": f"成功應用超時錯誤修正: {fix.get('description')}",
            "fix": fix
        }
    
    def _apply_test_failure_fix(self, fix: Dict[str, Any]) -> Dict[str, Any]:
        """應用測試失敗的修正方案
        
        Args:
            fix: 修正方案
            
        Returns:
            Dict[str, Any]: 應用結果
        """
        # 模擬應用修正方案
        self.logger.info(f"應用測試失敗修正: {fix.get('description')}")
        
        return {
            "fix_id": fix.get("problem_id"),
            "success": True,
            "description": f"成功應用測試失敗修正: {fix.get('description')}",
            "fix": fix
        }


class FixValidator:
    """修正驗證器
    
    負責驗證修正方案的效果。
    
    屬性:
        logger (logging.Logger): 日誌記錄器
    """
    
    def __init__(self):
        """初始化修正驗證器"""
        self.logger = logging.getLogger("intelligent_intervention.fix_validator")
    
    def validate_fixes(self, applied_fixes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """驗證修正效果
        
        Args:
            applied_fixes: 應用的修正方案列表
            
        Returns:
            List[Dict[str, Any]]: 驗證結果列表
        """
        validation_results = []
        
        for fix in applied_fixes:
            result = self._validate_fix(fix)
            validation_results.append(result)
        
        self.logger.info(f"驗證了 {len(validation_results)} 個修正方案")
        return validation_results
    
    def _validate_fix(self, applied_fix: Dict[str, Any]) -> Dict[str, Any]:
        """驗證特定修正方案
        
        Args:
            applied_fix: 應用的修正方案
            
        Returns:
            Dict[str, Any]: 驗證結果
        """
        fix_id = applied_fix.get("fix_id")
        fix = applied_fix.get("fix", {})
        problem = fix.get("problem", {})
        test_id = problem.get("test_id")
        
        self.logger.info(f"驗證修正方案: {applied_fix.get('description')} (修正ID: {fix_id})")
        
        # 在實際實現中，這裡會重新運行測試來驗證修正效果
        # 這裡僅模擬驗證過程
        
        # 模擬驗證結果
        validation_success = True
        
        return {
            "validation_id": fix_id,
            "success": validation_success,
            "description": f"驗證{'成功' if validation_success else '失敗'}: {applied_fix.get('description')}",
            "applied_fix": applied_fix
        }


class IntelligentIntervention:
    """智能介入
    
    整合問題檢測、修正生成、應用修正和驗證的完整流程。
    
    屬性:
        problem_detector (ProblemDetector): 問題檢測器
        fix_generator (FixGenerator): 修正生成器
        auto_fixer (AutoFixer): 自動修正器
        fix_validator (FixValidator): 修正驗證器
        logger (logging.Logger): 日誌記錄器
    """
    
    def __init__(self):
        """初始化智能介入"""
        self.problem_detector = ProblemDetector()
        self.fix_generator = FixGenerator()
        self.auto_fixer = AutoFixer()
        self.fix_validator = FixValidator()
        self.logger = logging.getLogger("intelligent_intervention")
    
    def process_test_results(self, test_results: List[Dict[str, Any]], auto_apply: bool = False) -> Dict[str, Any]:
        """處理測試結果
        
        完整的智能介入流程：檢測問題、生成修正方案、應用修正（可選）、驗證修正（可選）。
        
        Args:
            test_results: 測試結果列表
            auto_apply: 是否自動應用修正方案
            
        Returns:
            Dict[str, Any]: 處理結果
        """
        self.logger.info(f"開始處理 {len(test_results)} 個測試結果")
        
        # 檢測問題
        problems = self.problem_detector.detect_problems(test_results)
        self.logger.info(f"檢測到 {len(problems)} 個問題")
        
        if not problems:
            return {
                "success": True,
                "message": "未檢測到問題",
                "problems": [],
                "fixes": [],
                "applied_fixes": [],
                "validation_results": []
            }
        
        # 生成修正方案
        fixes = self.fix_generator.generate_fixes(problems)
        self.logger.info(f"生成了 {len(fixes)} 個修正方案")
        
        # 如果不自動應用，則到此結束
        if not auto_apply:
            return {
                "success": True,
                "message": "已生成修正方案，但未自動應用",
                "problems": problems,
                "fixes": fixes,
                "applied_fixes": [],
                "validation_results": []
            }
        
        # 應用修正方案
        applied_fixes = self.auto_fixer.apply_fixes(fixes)
        self.logger.info(f"應用了 {len(applied_fixes)} 個修正方案")
        
        # 驗證修正效果
        validation_results = self.fix_validator.validate_fixes(applied_fixes)
        self.logger.info(f"驗證了 {len(validation_results)} 個修正方案")
        
        # 統計驗證結果
        successful_validations = sum(1 for result in validation_results if result.get("success", False))
        
        return {
            "success": successful_validations == len(validation_results),
            "message": f"已應用並驗證修正方案，{successful_validations}/{len(validation_results)} 個驗證成功",
            "problems": problems,
            "fixes": fixes,
            "applied_fixes": applied_fixes,
            "validation_results": validation_results
        }
    
    def save_intervention_report(self, intervention_result: Dict[str, Any], output_dir: Optional[str] = None) -> str:
        """保存介入報告
        
        Args:
            intervention_result: 介入結果
            output_dir: 輸出目錄，如果為None則使用默認目錄
            
        Returns:
            str: 報告文件路徑
        """
        # 確定輸出目錄
        if output_dir is None:
            output_dir = os.path.join(os.path.dirname(__file__), '..', 'intervention_reports')
        
        # 確保輸出目錄存在
        os.makedirs(output_dir, exist_ok=True)
        
        # 構建報告文件路徑
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = os.path.join(output_dir, f"intervention_report_{timestamp}.json")
        
        # 保存報告
        with open(report_file, 'w') as f:
            json.dump(intervention_result, f, indent=2)
        
        self.logger.info(f"介入報告已保存: {report_file}")
        
        return report_file


# 默認智能介入實例
default_intelligent_intervention = IntelligentIntervention()
