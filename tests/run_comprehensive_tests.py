"""
Comprehensive test runner for the Graph-Enhanced Agentic RAG system.

This script runs all test suites including:
- Unit tests for all agents
- Integration tests for workflows and data consistency
- Performance and load tests
- System resilience tests

Usage:
    python tests/run_comprehensive_tests.py [--suite SUITE] [--verbose] [--report]

This implements task 10: Implement comprehensive testing
Requirements: 4.1, 4.2, 4.3, 4.4, 6.3, 6.4, 4.5, 2.4
"""

import argparse
import subprocess
import sys
import time
import json
from pathlib import Path
from typing import Dict, List, Any
import pytest


class TestSuiteRunner:
    """Manages execution of comprehensive test suites."""
    
    def __init__(self):
        self.test_suites = {
            "unit": {
                "description": "Unit tests for all agents",
                "files": [
                    "tests/test_coordinator_agent.py",
                    "tests/test_graph_navigator_agent.py", 
                    "tests/test_vector_retrieval_agent.py",
                    "tests/test_synthesis_agent.py"
                ],
                "requirements": ["4.1", "4.2", "4.3", "4.4"]
            },
            "integration": {
                "description": "Integration tests for workflows and data consistency",
                "files": [
                    "tests/test_integration_workflows.py",
                    "tests/test_system_resilience.py"
                ],
                "requirements": ["6.3", "6.4", "4.5"]
            },
            "performance": {
                "description": "Performance and load tests",
                "files": [
                    "tests/test_performance_load.py"
                ],
                "requirements": ["2.4"]
            },
            "existing": {
                "description": "Existing test files",
                "files": [
                    "tests/test_api_comprehensive.py",
                    "tests/test_api_endpoints.py",
                    "tests/test_config.py",
                    "tests/test_database_connections.py",
                    "tests/test_database_integration.py",
                    "tests/test_document_processor.py",
                    "tests/test_domain_processor.py",
                    "tests/test_dual_storage_ingestion.py",
                    "tests/test_gemini_integration.py",
                    "tests/test_graph_models.py",
                    "tests/test_interfaces.py",
                    "tests/test_models.py",
                    "tests/test_vector_models.py"
                ],
                "requirements": ["Various"]
            }
        }
        
        self.results = {}
    
    def run_test_suite(self, suite_name: str, verbose: bool = False) -> Dict[str, Any]:
        """Run a specific test suite."""
        if suite_name not in self.test_suites:
            raise ValueError(f"Unknown test suite: {suite_name}")
        
        suite = self.test_suites[suite_name]
        print(f"\n{'='*60}")
        print(f"Running {suite_name.upper()} TEST SUITE")
        print(f"Description: {suite['description']}")
        print(f"Requirements: {', '.join(suite['requirements'])}")
        print(f"{'='*60}")
        
        suite_results = {
            "suite_name": suite_name,
            "description": suite["description"],
            "requirements": suite["requirements"],
            "files": suite["files"],
            "start_time": time.time(),
            "file_results": {},
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "skipped_tests": 0,
            "errors": []
        }
        
        for test_file in suite["files"]:
            print(f"\nRunning {test_file}...")
            
            # Check if test file exists
            if not Path(test_file).exists():
                print(f"  WARNING: Test file {test_file} not found, skipping...")
                suite_results["file_results"][test_file] = {
                    "status": "skipped",
                    "reason": "file_not_found"
                }
                continue
            
            # Run pytest on the file
            file_result = self._run_pytest_file(test_file, verbose)
            suite_results["file_results"][test_file] = file_result
            
            # Aggregate results
            suite_results["total_tests"] += file_result.get("total", 0)
            suite_results["passed_tests"] += file_result.get("passed", 0)
            suite_results["failed_tests"] += file_result.get("failed", 0)
            suite_results["skipped_tests"] += file_result.get("skipped", 0)
            
            if file_result.get("errors"):
                suite_results["errors"].extend(file_result["errors"])
        
        suite_results["end_time"] = time.time()
        suite_results["duration"] = suite_results["end_time"] - suite_results["start_time"]
        suite_results["success_rate"] = (
            suite_results["passed_tests"] / suite_results["total_tests"] 
            if suite_results["total_tests"] > 0 else 0
        )
        
        self._print_suite_summary(suite_results)
        return suite_results
    
    def _run_pytest_file(self, test_file: str, verbose: bool = False) -> Dict[str, Any]:
        """Run pytest on a single test file."""
        cmd = ["python", "-m", "pytest", test_file, "--tb=short", "-q"]
        
        if verbose:
            cmd.append("-v")
        
        # Add JSON report for parsing results
        cmd.extend(["--json-report", "--json-report-file=/tmp/pytest_report.json"])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout per file
            )
            
            # Parse JSON report if available
            try:
                with open("/tmp/pytest_report.json", "r") as f:
                    json_report = json.load(f)
                
                return {
                    "status": "completed",
                    "return_code": result.returncode,
                    "total": json_report["summary"]["total"],
                    "passed": json_report["summary"].get("passed", 0),
                    "failed": json_report["summary"].get("failed", 0),
                    "skipped": json_report["summary"].get("skipped", 0),
                    "duration": json_report["duration"],
                    "stdout": result.stdout,
                    "stderr": result.stderr,
                    "errors": []
                }
            except (FileNotFoundError, json.JSONDecodeError, KeyError):
                # Fallback to parsing stdout
                return self._parse_pytest_output(result)
                
        except subprocess.TimeoutExpired:
            return {
                "status": "timeout",
                "return_code": -1,
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration": 300,
                "stdout": "",
                "stderr": "Test execution timed out",
                "errors": ["Test execution timed out after 5 minutes"]
            }
        except Exception as e:
            return {
                "status": "error",
                "return_code": -1,
                "total": 0,
                "passed": 0,
                "failed": 0,
                "skipped": 0,
                "duration": 0,
                "stdout": "",
                "stderr": str(e),
                "errors": [f"Failed to run test: {str(e)}"]
            }
    
    def _parse_pytest_output(self, result: subprocess.CompletedProcess) -> Dict[str, Any]:
        """Parse pytest output to extract test results."""
        stdout = result.stdout
        stderr = result.stderr
        
        # Simple parsing of pytest output
        total = passed = failed = skipped = 0
        errors = []
        
        # Look for result summary line
        lines = stdout.split('\n')
        for line in lines:
            if "passed" in line or "failed" in line or "skipped" in line:
                # Try to extract numbers
                import re
                numbers = re.findall(r'(\d+)\s+(passed|failed|skipped)', line)
                for num, status in numbers:
                    if status == "passed":
                        passed = int(num)
                    elif status == "failed":
                        failed = int(num)
                    elif status == "skipped":
                        skipped = int(num)
        
        total = passed + failed + skipped
        
        if result.returncode != 0 and stderr:
            errors.append(stderr)
        
        return {
            "status": "completed",
            "return_code": result.returncode,
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": skipped,
            "duration": 0,  # Unknown from simple parsing
            "stdout": stdout,
            "stderr": stderr,
            "errors": errors
        }
    
    def _print_suite_summary(self, suite_results: Dict[str, Any]):
        """Print summary of test suite results."""
        print(f"\n{'-'*40}")
        print(f"SUITE SUMMARY: {suite_results['suite_name'].upper()}")
        print(f"{'-'*40}")
        print(f"Total Tests:    {suite_results['total_tests']}")
        print(f"Passed:         {suite_results['passed_tests']}")
        print(f"Failed:         {suite_results['failed_tests']}")
        print(f"Skipped:        {suite_results['skipped_tests']}")
        print(f"Success Rate:   {suite_results['success_rate']:.1%}")
        print(f"Duration:       {suite_results['duration']:.1f}s")
        
        if suite_results['errors']:
            print(f"\nErrors ({len(suite_results['errors'])}):")
            for error in suite_results['errors'][:5]:  # Show first 5 errors
                print(f"  - {error}")
            if len(suite_results['errors']) > 5:
                print(f"  ... and {len(suite_results['errors']) - 5} more")
    
    def run_all_suites(self, verbose: bool = False) -> Dict[str, Any]:
        """Run all test suites."""
        print("Starting comprehensive test execution...")
        print(f"Test suites: {', '.join(self.test_suites.keys())}")
        
        overall_start = time.time()
        all_results = {
            "start_time": overall_start,
            "suites": {},
            "summary": {
                "total_suites": len(self.test_suites),
                "completed_suites": 0,
                "total_tests": 0,
                "passed_tests": 0,
                "failed_tests": 0,
                "skipped_tests": 0,
                "overall_success_rate": 0.0
            }
        }
        
        for suite_name in self.test_suites.keys():
            try:
                suite_result = self.run_test_suite(suite_name, verbose)
                all_results["suites"][suite_name] = suite_result
                all_results["summary"]["completed_suites"] += 1
                
                # Aggregate totals
                all_results["summary"]["total_tests"] += suite_result["total_tests"]
                all_results["summary"]["passed_tests"] += suite_result["passed_tests"]
                all_results["summary"]["failed_tests"] += suite_result["failed_tests"]
                all_results["summary"]["skipped_tests"] += suite_result["skipped_tests"]
                
            except Exception as e:
                print(f"ERROR: Failed to run suite {suite_name}: {e}")
                all_results["suites"][suite_name] = {
                    "suite_name": suite_name,
                    "status": "error",
                    "error": str(e)
                }
        
        all_results["end_time"] = time.time()
        all_results["total_duration"] = all_results["end_time"] - overall_start
        
        # Calculate overall success rate
        if all_results["summary"]["total_tests"] > 0:
            all_results["summary"]["overall_success_rate"] = (
                all_results["summary"]["passed_tests"] / all_results["summary"]["total_tests"]
            )
        
        self._print_overall_summary(all_results)
        return all_results
    
    def _print_overall_summary(self, all_results: Dict[str, Any]):
        """Print overall test execution summary."""
        summary = all_results["summary"]
        
        print(f"\n{'='*60}")
        print("COMPREHENSIVE TEST EXECUTION SUMMARY")
        print(f"{'='*60}")
        print(f"Total Duration:     {all_results['total_duration']:.1f}s")
        print(f"Suites Completed:   {summary['completed_suites']}/{summary['total_suites']}")
        print(f"Total Tests:        {summary['total_tests']}")
        print(f"Passed:             {summary['passed_tests']}")
        print(f"Failed:             {summary['failed_tests']}")
        print(f"Skipped:            {summary['skipped_tests']}")
        print(f"Overall Success:    {summary['overall_success_rate']:.1%}")
        
        print(f"\nSuite Breakdown:")
        for suite_name, suite_result in all_results["suites"].items():
            if isinstance(suite_result, dict) and "success_rate" in suite_result:
                status = "✓" if suite_result["success_rate"] >= 0.8 else "✗"
                print(f"  {status} {suite_name:12} - {suite_result['success_rate']:.1%} "
                      f"({suite_result['passed_tests']}/{suite_result['total_tests']})")
            else:
                print(f"  ✗ {suite_name:12} - ERROR")
        
        # Overall assessment
        if summary['overall_success_rate'] >= 0.9:
            print(f"\n🎉 EXCELLENT: Test suite is in great shape!")
        elif summary['overall_success_rate'] >= 0.8:
            print(f"\n✅ GOOD: Test suite is mostly passing with minor issues.")
        elif summary['overall_success_rate'] >= 0.6:
            print(f"\n⚠️  NEEDS ATTENTION: Significant test failures need investigation.")
        else:
            print(f"\n❌ CRITICAL: Major test failures require immediate attention.")
    
    def generate_report(self, results: Dict[str, Any], output_file: str = "test_report.json"):
        """Generate detailed test report."""
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nDetailed test report saved to: {output_file}")
        
        # Generate HTML report summary
        html_file = output_file.replace(".json", ".html")
        self._generate_html_report(results, html_file)
        print(f"HTML report saved to: {html_file}")
    
    def _generate_html_report(self, results: Dict[str, Any], output_file: str):
        """Generate HTML test report."""
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Graph-Enhanced Agentic RAG - Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #f0f0f0; padding: 20px; border-radius: 5px; }}
        .suite {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .passed {{ color: green; }}
        .failed {{ color: red; }}
        .skipped {{ color: orange; }}
        .metrics {{ display: flex; gap: 20px; }}
        .metric {{ text-align: center; padding: 10px; background: #f9f9f9; border-radius: 3px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Graph-Enhanced Agentic RAG - Comprehensive Test Report</h1>
        <p>Generated on: {time.strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Total Duration: {results.get('total_duration', 0):.1f} seconds</p>
    </div>
    
    <div class="metrics">
        <div class="metric">
            <h3>Total Tests</h3>
            <p>{results['summary']['total_tests']}</p>
        </div>
        <div class="metric">
            <h3 class="passed">Passed</h3>
            <p>{results['summary']['passed_tests']}</p>
        </div>
        <div class="metric">
            <h3 class="failed">Failed</h3>
            <p>{results['summary']['failed_tests']}</p>
        </div>
        <div class="metric">
            <h3 class="skipped">Skipped</h3>
            <p>{results['summary']['skipped_tests']}</p>
        </div>
        <div class="metric">
            <h3>Success Rate</h3>
            <p>{results['summary']['overall_success_rate']:.1%}</p>
        </div>
    </div>
"""
        
        for suite_name, suite_result in results["suites"].items():
            if isinstance(suite_result, dict) and "description" in suite_result:
                html_content += f"""
    <div class="suite">
        <h2>{suite_name.title()} Test Suite</h2>
        <p><strong>Description:</strong> {suite_result['description']}</p>
        <p><strong>Requirements:</strong> {', '.join(suite_result.get('requirements', []))}</p>
        <p><strong>Duration:</strong> {suite_result.get('duration', 0):.1f}s</p>
        <p>
            <span class="passed">Passed: {suite_result.get('passed_tests', 0)}</span> | 
            <span class="failed">Failed: {suite_result.get('failed_tests', 0)}</span> | 
            <span class="skipped">Skipped: {suite_result.get('skipped_tests', 0)}</span>
        </p>
        <p><strong>Success Rate:</strong> {suite_result.get('success_rate', 0):.1%}</p>
    </div>
"""
        
        html_content += """
</body>
</html>
"""
        
        with open(output_file, "w") as f:
            f.write(html_content)


def main():
    """Main entry point for test runner."""
    parser = argparse.ArgumentParser(
        description="Run comprehensive tests for Graph-Enhanced Agentic RAG system"
    )
    parser.add_argument(
        "--suite", 
        choices=["unit", "integration", "performance", "existing", "all"],
        default="all",
        help="Test suite to run (default: all)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--report", "-r",
        action="store_true",
        help="Generate detailed test report"
    )
    parser.add_argument(
        "--output", "-o",
        default="test_report.json",
        help="Output file for test report (default: test_report.json)"
    )
    
    args = parser.parse_args()
    
    runner = TestSuiteRunner()
    
    try:
        if args.suite == "all":
            results = runner.run_all_suites(verbose=args.verbose)
        else:
            suite_result = runner.run_test_suite(args.suite, verbose=args.verbose)
            results = {
                "suites": {args.suite: suite_result},
                "summary": {
                    "total_suites": 1,
                    "completed_suites": 1,
                    "total_tests": suite_result["total_tests"],
                    "passed_tests": suite_result["passed_tests"],
                    "failed_tests": suite_result["failed_tests"],
                    "skipped_tests": suite_result["skipped_tests"],
                    "overall_success_rate": suite_result["success_rate"]
                }
            }
        
        if args.report:
            runner.generate_report(results, args.output)
        
        # Exit with appropriate code
        success_rate = results["summary"]["overall_success_rate"]
        if success_rate >= 0.8:
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # Failure
            
    except KeyboardInterrupt:
        print("\nTest execution interrupted by user.")
        sys.exit(130)
    except Exception as e:
        print(f"ERROR: Test execution failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()