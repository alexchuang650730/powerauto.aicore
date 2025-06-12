#!/usr/bin/env python
"""
智能引擎CLI - PowerAutomation測試框架的統一入口

此模組提供命令行界面，作為PowerAutomation測試框架的統一入口點，
支持測試執行、智能介入、結果分析等功能。
"""

import os
import sys
import argparse
import logging
import unittest
import json
from datetime import datetime

# 添加項目根目錄到Python路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 
                                                '..', '..')))

# 導入測試框架組件
from testing.import_helpers import add_project_root_to_path
from testing.mock_config import MockConfig
from testing.environment import Environment
from testing.intelligent_intervention.intervention import InterventionEngine, ProblemDetector, FixGenerator, AutoFixer, FixValidator


# 配置日誌
log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
os.makedirs(log_dir, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(log_dir, 
                                        f'cli_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'))
    ]
)

logger = logging.getLogger('intelligent_engine_cli')


class IntelligentEngineCLI:
    """智能引擎命令行界面
    
    為PowerAutomation測試框架提供統一的命令行入口，
    支持測試執行、智能介入、結果分析等功能。
    """
    
    def __init__(self):
        """初始化CLI"""
        self.parser = self._create_parser()
        self.mock_config = MockConfig()
        self.environment = Environment(self.mock_config)
        self.intervention_engine = InterventionEngine() # 初始化智能介入引擎
        self.problem_detector = ProblemDetector()
        self.fix_generator = FixGenerator()
        self.auto_fixer = AutoFixer()
        self.fix_validator = FixValidator()
    
    def _create_parser(self):
        """創建命令行參數解析器
        
        Returns:
            argparse.ArgumentParser: 參數解析器
        """
        parser = argparse.ArgumentParser(
            description='PowerAutomation 智能測試引擎 CLI',
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog='''
示例:
  # 運行所有測試
  python -m testing.cli.intelligent_engine_cli run-tests --all
  
  # 運行特定層級的測試
  python -m testing.cli.intelligent_engine_cli run-tests --layer 1
  
  # 啟用智能介入
  python -m testing.cli.intelligent_engine_cli run-tests --all --intelligent-intervention
  
  # 使用特定的Mock配置
  python -m testing.cli.intelligent_engine_cli run-tests --all --mock-config path/to/config.yaml
'''
        )
        
        subparsers = parser.add_subparsers(dest='command', help='可用命令')
        
        # run-tests 命令
        run_tests_parser = subparsers.add_parser('run-tests', help='運行測試')
        run_tests_parser.add_argument('--all', action='store_true', help='運行所有測試')
        run_tests_parser.add_argument('--layer', type=int, choices=[1, 2, 3], help='運行特定層級的測試')
        run_tests_parser.add_argument('--test-id', help='運行特定ID的測試')
        run_tests_parser.add_argument('--intelligent-intervention', action='store_true', 
                                     help='啟用智能介入')
        run_tests_parser.add_argument('--mock-config', help='指定Mock配置文件路徑')
        run_tests_parser.add_argument('--output', help='指定輸出目錄')
        
        # analyze-results 命令
        analyze_parser = subparsers.add_parser('analyze-results', help='分析測試結果')
        analyze_parser.add_argument('--results-dir', required=True, help='測試結果目錄')
        analyze_parser.add_argument('--output', help='分析報告輸出路徑')
        
        # fix-issues 命令
        fix_parser = subparsers.add_parser('fix-issues', help='修復測試問題')
        fix_parser.add_argument('--results-dir', required=True, help='測試結果目錄')
        fix_parser.add_argument('--auto-apply', action='store_true', help='自動應用修復')
        fix_parser.add_argument('--output', help='修復報告輸出路徑')
        
        # validate-fixes 命令
        validate_parser = subparsers.add_parser('validate-fixes', help='驗證修復效果')
        validate_parser.add_argument('--fixes-dir', required=True, help='修復方案目錄')
        validate_parser.add_argument('--output', help='驗證報告輸出路徑')
        
        return parser
    
    def run(self, args=None):
        """運行CLI
        
        Args:
            args: 命令行參數，如果為None則從sys.argv解析
            
        Returns:
            int: 退出碼
        """
        args = self.parser.parse_args(args)
        
        if not args.command:
            self.parser.print_help()
            return 1
        
        try:
            # 根據命令調用相應的處理函數
            if args.command == 'run-tests':
                return self._handle_run_tests(args)
            elif args.command == 'analyze-results':
                return self._handle_analyze_results(args)
            elif args.command == 'fix-issues':
                return self._handle_fix_issues(args)
            elif args.command == 'validate-fixes':
                return self._handle_validate_fixes(args)
            else:
                logger.error(f"未知命令: {args.command}")
                return 1
        except Exception as e:
            logger.exception(f"執行命令 {args.command} 時發生錯誤: {e}")
            return 1
    
    def _handle_run_tests(self, args):
        """處理run-tests命令
        
        Args:
            args: 命令行參數
            
        Returns:
            int: 退出碼
        """
        logger.info("開始運行測試...")
        
        # 加載Mock配置
        if args.mock_config:
            logger.info(f"使用Mock配置: {args.mock_config}")
            self.mock_config = MockConfig(config_file=args.mock_config)
            self.environment = Environment(self.mock_config)
        
        # 確定要運行的測試
        if args.all:
            logger.info("運行所有測試")
            test_results = self._run_all_tests(args.intelligent_intervention, args.output)
        elif args.layer:
            logger.info(f"運行第{args.layer}層測試")
            test_results = self._run_layer_tests(args.layer, args.intelligent_intervention, args.output)
        elif args.test_id:
            logger.info(f"運行測試: {args.test_id}")
            test_results = self._run_specific_test(args.test_id, args.intelligent_intervention, args.output)
        else:
            logger.error("請指定要運行的測試 (--all, --layer 或 --test-id)")
            return 1
        
        logger.info("測試運行完成")
        return 0 if test_results.wasSuccessful() else 1
    
    def _handle_analyze_results(self, args):
        """處理analyze-results命令
        
        Args:
            args: 命令行參數
            
        Returns:
            int: 退出碼
        """
        logger.info(f"分析測試結果: {args.results_dir}")
        
        # 在實際應用中，這裡會解析測試報告文件，例如JUnit XML或JSON格式
        # 為了演示，我們假設results_dir中包含一個名為 'test_results.json' 的文件
        # 該文件包含測試失敗和錯誤的簡化信息
        results_file_path = os.path.join(args.results_dir, 'test_results.json')
        mock_test_results = unittest.TestResult()

        if os.path.exists(results_file_path):
            try:
                with open(results_file_path, 'r') as f:
                    data = json.load(f)
                    # 假設data中包含 'errors' 和 'failures' 列表
                    for error in data.get('errors', []):
                        mock_test_results.errors.append((error['test'], error['message']))
                    for failure in data.get('failures', []):
                        mock_test_results.failures.append((failure['test'], failure['message']))
            except Exception as e:
                logger.error(f"加載測試結果文件失敗: {e}")
                return 1
        else:
            logger.warning(f"未找到測試結果文件: {results_file_path}，將使用模擬數據進行分析。")
            # 為了演示，我們手動添加一些失敗和錯誤
            mock_test_results.failures.append(("test_module.TestClass.test_failed_case", "AssertionError: Expected X but got Y"))
            mock_test_results.errors.append(("test_module.TestClass.test_error_case", "TypeError: Unsupported operand type"))

        detected_problems = self.problem_detector.detect(mock_test_results)
        
        output_path = args.output or os.path.join(args.results_dir, "analysis_report.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(detected_problems, f, indent=2)
        logger.info(f"分析報告已保存到: {output_path}")
        return 0
    
    def _handle_fix_issues(self, args):
        """處理fix-issues命令
        
        Args:
            args: 命令行參數
            
        Returns:
            int: 退出碼
        """
        logger.info(f"修復測試問題: {args.results_dir}")
        
        # 從results_dir加載問題報告
        problem_report_path = os.path.join(args.results_dir, 'analysis_report.json')
        problems = []
        if os.path.exists(problem_report_path):
            try:
                with open(problem_report_path, 'r') as f:
                    problems = json.load(f)
            except Exception as e:
                logger.error(f"加載問題報告文件失敗: {e}")
                return 1
        else:
            logger.warning(f"未找到問題報告文件: {problem_report_path}，將使用模擬數據生成修正建議。")
            # 為了演示，我們手動添加一些問題
            problems = [
                {"type": "failure", "test": "test_module.TestClass.test_failed_case", "message": "AssertionError: Expected X but got Y"},
                {"type": "error", "test": "test_module.TestClass.test_error_case", "message": "TypeError: Unsupported operand type"}
            ]

        fix_suggestions = self.fix_generator.generate(problems)
        
        if args.auto_apply:
            logger.info("自動應用修正...")
            applied_fixes = self.auto_fixer.apply(fix_suggestions)
            output_path = args.output or os.path.join(args.results_dir, "applied_fixes_report.json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(applied_fixes, f, indent=2)
            logger.info(f"已應用修正報告已保存到: {output_path}")
        else:
            output_path = args.output or os.path.join(args.results_dir, "fix_suggestions_report.json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                json.dump(fix_suggestions, f, indent=2)
            logger.info(f"修正建議報告已保存到: {output_path}")
        return 0
    
    def _handle_validate_fixes(self, args):
        """處理validate-fixes命令
        
        Args:
            args: 命令行參數
            
        Returns:
            int: 退出碼
        """
        logger.info(f"驗證修復效果: {args.fixes_dir}")
        
        # 從fixes_dir加載已應用的修正
        applied_fixes_path = os.path.join(args.fixes_dir, 'applied_fixes_report.json')
        applied_fixes = []
        if os.path.exists(applied_fixes_path):
            try:
                with open(applied_fixes_path, 'r') as f:
                    applied_fixes = json.load(f)
            except Exception as e:
                logger.error(f"加載已應用修正文件失敗: {e}")
                return 1
        else:
            logger.warning(f"未找到已應用修正文件: {applied_fixes_path}，將使用模擬數據進行驗證。")
            # 為了演示，我們手動添加一些已應用的修正
            applied_fixes = [
                {"suggestion": {"problem": {"type": "failure", "test": "test_module.TestClass.test_failed_case"}, "suggestion": "嘗試修正 test_module.TestClass.test_failed_case 相關問題。"}, "status": "applied"}
            ]

        validation_results = self.fix_validator.validate(applied_fixes)
        
        output_path = args.output or os.path.join(args.fixes_dir, "validation_report.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(validation_results, f, indent=2)
        logger.info(f"驗證報告已保存到: {output_path}")
        return 0
    
    def _run_all_tests(self, intelligent_intervention=False, output_dir=None):
        """運行所有測試
        
        Args:
            intelligent_intervention (bool): 是否啟用智能介入
            output_dir (str): 輸出目錄
            
        Returns:
            unittest.TestResult: 測試結果對象
        """
        logger.info("運行所有層級的測試...")
        
        test_suite = unittest.TestSuite()
        test_loader = unittest.TestLoader()
        
        # 發現所有測試用例
        test_suite.addTests(test_loader.discover(
            os.path.join(os.path.dirname(__file__), '..', 'test_cases'),
            pattern='test_*.py'
        ))
        
        # 運行測試
        runner = unittest.TextTestRunner(verbosity=2)
        results = runner.run(test_suite)
        
        if intelligent_intervention and not results.wasSuccessful():
            logger.info("檢測到測試失敗，啟用智能介入...")
            self.intervention_engine.intervene(results, output_dir) # 傳遞測試結果給介入引擎
            
        return results
    
    def _run_layer_tests(self, layer, intelligent_intervention=False, output_dir=None):
        """運行特定層級的測試
        
        Args:
            layer (int): 層級 (1, 2, 或 3)
            intelligent_intervention (bool): 是否啟用智能介入
            output_dir (str): 輸出目錄
            
        Returns:
            unittest.TestResult: 測試結果對象
        """
        logger.info(f"運行第{layer}層測試...")
        
        # 根據層級確定測試目錄
        if layer == 1:
            test_dir_name = "layer1_unit_code_quality"
        elif layer == 2:
            test_dir_name = "layer2_integration_agent_collab"
        elif layer == 3:
            test_dir_name = "layer3_mcp_compliance_standard"
        else:
            logger.error(f"無效的層級: {layer}")
            return unittest.TestResult() # 返回一個空的結果對象
        
        test_path = os.path.join(os.path.dirname(__file__), '..', 'test_cases', test_dir_name)
        
        test_suite = unittest.TestSuite()
        test_loader = unittest.TestLoader()
        
        # 發現指定目錄下的測試用例
        test_suite.addTests(test_loader.discover(
            test_path,
            pattern='test_*.py'
        ))
        
        # 運行測試
        runner = unittest.TextTestRunner(verbosity=2)
        results = runner.run(test_suite)
        
        if intelligent_intervention and not results.wasSuccessful():
            logger.info("檢測到測試失敗，啟用智能介入...")
            self.intervention_engine.intervene(results, output_dir) # 傳遞測試結果給介入引擎
            
        return results
    
    def _run_specific_test(self, test_id, intelligent_intervention=False, output_dir=None):
        """運行特定ID的測試
        
        Args:
            test_id (str): 測試ID (例如: module.ClassName.test_method)
            intelligent_intervention (bool): 是否啟用智能介入
            output_dir (str): 輸出目錄
            
        Returns:
            unittest.TestResult: 測試結果對象
        """
        logger.info(f"運行測試: {test_id}")
        
        test_suite = unittest.TestSuite()
        test_loader = unittest.TestLoader()
        
        try:
            # 嘗試加載特定測試
            test_suite.addTest(test_loader.loadTestsFromName(test_id))
        except Exception as e:
            logger.error(f"無法加載測試 {test_id}: {e}")
            return unittest.TestResult()
        
        # 運行測試
        runner = unittest.TextTestRunner(verbosity=2)
        results = runner.run(test_suite)
        
        if intelligent_intervention and not results.wasSuccessful():
            logger.info("檢測到測試失敗，啟用智能介入...")
            self.intervention_engine.intervene(results, output_dir) # 傳遞測試結果給介入引擎
            
        return results


def main():
    """CLI主入口函數"""
    # 確保日誌目錄存在
    log_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 運行CLI
    cli = IntelligentEngineCLI()
    sys.exit(cli.run())


if __name__ == '__main__':
    main()


