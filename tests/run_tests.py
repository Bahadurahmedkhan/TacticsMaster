#!/usr/bin/env python3
"""
Comprehensive Test Runner for Tactics Master System

This module provides a comprehensive test runner that executes all tests,
generates detailed reports, and provides various testing options.
"""

import os
import sys
import subprocess
import argparse
import json
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

# Add project paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))


class TestRunner:
    """Comprehensive test runner for Tactics Master system"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.test_dir = self.project_root / "tests"
        self.reports_dir = self.project_root / "test_reports"
        self.reports_dir.mkdir(exist_ok=True)
        
        # Test categories
        self.test_categories = {
            "unit": "tests/unit/",
            "integration": "tests/integration/",
            "all": "tests/"
        }
        
        # Test markers
        self.test_markers = {
            "unit": "unit",
            "integration": "integration",
            "slow": "slow",
            "api": "api",
            "performance": "performance",
            "error_handling": "error_handling",
            "data_validation": "data_validation",
            "unicode": "unicode",
            "concurrent": "concurrent"
        }
    
    def run_tests(
        self,
        category: str = "all",
        markers: Optional[List[str]] = None,
        verbose: bool = False,
        coverage: bool = False,
        parallel: bool = False,
        html_report: bool = False,
        json_report: bool = False,
        benchmark: bool = False
    ) -> Dict[str, Any]:
        """
        Run tests with specified options
        
        Args:
            category: Test category to run (unit, integration, all)
            markers: List of test markers to include/exclude
            verbose: Enable verbose output
            coverage: Enable coverage reporting
            parallel: Run tests in parallel
            html_report: Generate HTML report
            json_report: Generate JSON report
            benchmark: Run performance benchmarks
            
        Returns:
            Dict containing test results and metadata
        """
        print(f"🧪 Starting Tactics Master Test Suite")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        # Build pytest command
        cmd = self._build_pytest_command(
            category, markers, verbose, coverage, parallel, 
            html_report, json_report, benchmark
        )
        
        # Run tests
        start_time = time.time()
        result = self._execute_tests(cmd)
        end_time = time.time()
        
        # Generate reports
        reports = self._generate_reports(result, start_time, end_time)
        
        # Display results
        self._display_results(result, reports)
        
        return {
            "result": result,
            "reports": reports,
            "duration": end_time - start_time,
            "timestamp": datetime.now().isoformat()
        }
    
    def _build_pytest_command(
        self,
        category: str,
        markers: Optional[List[str]],
        verbose: bool,
        coverage: bool,
        parallel: bool,
        html_report: bool,
        json_report: bool,
        benchmark: bool
    ) -> List[str]:
        """Build pytest command with specified options"""
        cmd = ["python", "-m", "pytest"]
        
        # Add test path
        if category == "all":
            cmd.append(str(self.test_dir))
        else:
            cmd.append(str(self.test_dir / self.test_categories[category]))
        
        # Add markers
        if markers:
            marker_expr = " and ".join(markers)
            cmd.extend(["-m", marker_expr])
        
        # Add verbosity
        if verbose:
            cmd.append("-v")
        else:
            cmd.append("-q")
        
        # Add coverage
        if coverage:
            cmd.extend([
                "--cov=app",
                "--cov=backend",
                "--cov-report=term-missing",
                "--cov-report=html:test_reports/coverage_html"
            ])
        
        # Add parallel execution
        if parallel:
            cmd.extend(["-n", "auto"])
        
        # Add HTML report
        if html_report:
            cmd.extend([
                "--html=test_reports/report.html",
                "--self-contained-html"
            ])
        
        # Add JSON report
        if json_report:
            cmd.extend(["--json-report", "--json-report-file=test_reports/report.json"])
        
        # Add benchmark
        if benchmark:
            cmd.extend(["--benchmark-only", "--benchmark-sort=mean"])
        
        # Add additional options
        cmd.extend([
            "--tb=short",
            "--strict-markers",
            "--disable-warnings",
            "--color=yes",
            "--durations=10"
        ])
        
        return cmd
    
    def _execute_tests(self, cmd: List[str]) -> Dict[str, Any]:
        """Execute pytest command and return results"""
        print(f"🔧 Running command: {' '.join(cmd)}")
        print()
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=1800  # 30 minutes timeout
            )
            
            return {
                "returncode": result.returncode,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "success": result.returncode == 0
            }
        except subprocess.TimeoutExpired:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": "Test execution timed out after 30 minutes",
                "success": False
            }
        except Exception as e:
            return {
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "success": False
            }
    
    def _generate_reports(self, result: Dict[str, Any], start_time: float, end_time: float) -> Dict[str, Any]:
        """Generate test reports"""
        reports = {
            "summary": {
                "success": result["success"],
                "returncode": result["returncode"],
                "duration": end_time - start_time,
                "timestamp": datetime.now().isoformat()
            },
            "coverage": self._get_coverage_info(),
            "performance": self._get_performance_info(result),
            "files": self._get_test_files_info()
        }
        
        # Save reports
        self._save_reports(reports)
        
        return reports
    
    def _get_coverage_info(self) -> Dict[str, Any]:
        """Get coverage information"""
        coverage_file = self.reports_dir / "coverage_html" / "index.html"
        if coverage_file.exists():
            return {
                "available": True,
                "file": str(coverage_file),
                "url": f"file://{coverage_file.absolute()}"
            }
        return {"available": False}
    
    def _get_performance_info(self, result: Dict[str, Any]) -> Dict[str, Any]:
        """Get performance information from test results"""
        stdout = result.get("stdout", "")
        
        # Extract duration information
        duration_info = {}
        if "durations" in stdout:
            lines = stdout.split('\n')
            for line in lines:
                if "durations" in line.lower():
                    duration_info["summary"] = line.strip()
                    break
        
        return {
            "durations": duration_info,
            "output_size": len(stdout),
            "error_size": len(result.get("stderr", ""))
        }
    
    def _get_test_files_info(self) -> Dict[str, Any]:
        """Get information about test files"""
        test_files = {
            "unit": list((self.test_dir / "unit").glob("test_*.py")),
            "integration": list((self.test_dir / "integration").glob("test_*.py")),
            "all": list(self.test_dir.glob("**/test_*.py"))
        }
        
        return {
            "unit_count": len(test_files["unit"]),
            "integration_count": len(test_files["integration"]),
            "total_count": len(test_files["all"]),
            "files": {
                "unit": [str(f.relative_to(self.project_root)) for f in test_files["unit"]],
                "integration": [str(f.relative_to(self.project_root)) for f in test_files["integration"]]
            }
        }
    
    def _save_reports(self, reports: Dict[str, Any]) -> None:
        """Save reports to files"""
        # Save JSON report
        json_file = self.reports_dir / "test_results.json"
        with open(json_file, 'w') as f:
            json.dump(reports, f, indent=2)
        
        # Save summary report
        summary_file = self.reports_dir / "test_summary.txt"
        with open(summary_file, 'w') as f:
            f.write(f"Tactics Master Test Results\n")
            f.write(f"Generated: {reports['summary']['timestamp']}\n")
            f.write(f"Success: {reports['summary']['success']}\n")
            f.write(f"Duration: {reports['summary']['duration']:.2f} seconds\n")
            f.write(f"Return Code: {reports['summary']['returncode']}\n")
            f.write(f"Test Files: {reports['files']['total_count']}\n")
    
    def _display_results(self, result: Dict[str, Any], reports: Dict[str, Any]) -> None:
        """Display test results"""
        print("\n" + "=" * 60)
        print("📊 TEST RESULTS SUMMARY")
        print("=" * 60)
        
        # Success status
        if result["success"]:
            print("✅ All tests passed!")
        else:
            print("❌ Some tests failed!")
        
        # Basic info
        print(f"⏱️  Duration: {reports['summary']['duration']:.2f} seconds")
        print(f"📁 Test files: {reports['files']['total_count']}")
        print(f"🔢 Return code: {result['returncode']}")
        
        # Coverage info
        if reports['coverage']['available']:
            print(f"📈 Coverage report: {reports['coverage']['url']}")
        
        # Performance info
        if reports['performance']['durations']:
            print(f"⚡ Performance: {reports['performance']['durations'].get('summary', 'N/A')}")
        
        # Output summary
        if result["stdout"]:
            print(f"📝 Output size: {len(result['stdout'])} characters")
        
        if result["stderr"]:
            print(f"⚠️  Errors: {len(result['stderr'])} characters")
            print("\nError details:")
            print(result["stderr"][:500] + "..." if len(result["stderr"]) > 500 else result["stderr"])
        
        # Report files
        print(f"\n📄 Reports saved to: {self.reports_dir}")
        print(f"📊 JSON report: {self.reports_dir / 'test_results.json'}")
        print(f"📋 Summary: {self.reports_dir / 'test_summary.txt'}")
        
        if reports['coverage']['available']:
            print(f"📈 Coverage: {reports['coverage']['file']}")
    
    def run_unit_tests(self, **kwargs) -> Dict[str, Any]:
        """Run unit tests only"""
        return self.run_tests(category="unit", **kwargs)
    
    def run_integration_tests(self, **kwargs) -> Dict[str, Any]:
        """Run integration tests only"""
        return self.run_tests(category="integration", **kwargs)
    
    def run_performance_tests(self, **kwargs) -> Dict[str, Any]:
        """Run performance tests"""
        return self.run_tests(markers=["performance"], **kwargs)
    
    def run_error_handling_tests(self, **kwargs) -> Dict[str, Any]:
        """Run error handling tests"""
        return self.run_tests(markers=["error_handling"], **kwargs)
    
    def run_unicode_tests(self, **kwargs) -> Dict[str, Any]:
        """Run unicode handling tests"""
        return self.run_tests(markers=["unicode"], **kwargs)
    
    def run_concurrent_tests(self, **kwargs) -> Dict[str, Any]:
        """Run concurrent tests"""
        return self.run_tests(markers=["concurrent"], **kwargs)
    
    def run_slow_tests(self, **kwargs) -> Dict[str, Any]:
        """Run slow tests"""
        return self.run_tests(markers=["slow"], **kwargs)
    
    def run_api_tests(self, **kwargs) -> Dict[str, Any]:
        """Run API tests"""
        return self.run_tests(markers=["api"], **kwargs)
    
    def run_data_validation_tests(self, **kwargs) -> Dict[str, Any]:
        """Run data validation tests"""
        return self.run_tests(markers=["data_validation"], **kwargs)
    
    def run_benchmark_tests(self, **kwargs) -> Dict[str, Any]:
        """Run benchmark tests"""
        return self.run_tests(benchmark=True, **kwargs)
    
    def run_all_tests(self, **kwargs) -> Dict[str, Any]:
        """Run all tests"""
        return self.run_tests(category="all", **kwargs)
    
    def clean_reports(self) -> None:
        """Clean test reports directory"""
        import shutil
        if self.reports_dir.exists():
            shutil.rmtree(self.reports_dir)
        self.reports_dir.mkdir(exist_ok=True)
        print(f"🧹 Cleaned reports directory: {self.reports_dir}")
    
    def list_tests(self) -> None:
        """List all available tests"""
        print("📋 Available Tests:")
        print("=" * 40)
        
        for category, path in self.test_categories.items():
            if category == "all":
                continue
                
            test_dir = self.test_dir / path
            if test_dir.exists():
                test_files = list(test_dir.glob("test_*.py"))
                print(f"\n{category.upper()} TESTS ({len(test_files)} files):")
                for test_file in test_files:
                    print(f"  📄 {test_file.name}")
        
        print(f"\n📊 Total test files: {len(list(self.test_dir.glob('**/test_*.py')))}")
    
    def validate_environment(self) -> bool:
        """Validate test environment"""
        print("🔍 Validating test environment...")
        
        # Check Python version
        python_version = sys.version_info
        if python_version < (3, 8):
            print("❌ Python 3.8+ required")
            return False
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        
        # Check required packages
        required_packages = [
            "pytest", "pytest-asyncio", "pytest-cov", "pytest-mock",
            "fastapi", "httpx", "requests", "pydantic"
        ]
        
        missing_packages = []
        for package in required_packages:
            try:
                __import__(package.replace("-", "_"))
                print(f"✅ {package}")
            except ImportError:
                missing_packages.append(package)
                print(f"❌ {package}")
        
        if missing_packages:
            print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
            print("Install with: pip install -r tests/requirements.txt")
            return False
        
        # Check test files
        test_files = list(self.test_dir.glob("**/test_*.py"))
        if not test_files:
            print("❌ No test files found")
            return False
        print(f"✅ {len(test_files)} test files found")
        
        print("✅ Environment validation passed!")
        return True


def main():
    """Main entry point for test runner"""
    parser = argparse.ArgumentParser(description="Tactics Master Test Runner")
    parser.add_argument("--category", choices=["unit", "integration", "all"], 
                       default="all", help="Test category to run")
    parser.add_argument("--markers", nargs="+", help="Test markers to include")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--coverage", "-c", action="store_true", help="Enable coverage")
    parser.add_argument("--parallel", "-p", action="store_true", help="Run in parallel")
    parser.add_argument("--html-report", action="store_true", help="Generate HTML report")
    parser.add_argument("--json-report", action="store_true", help="Generate JSON report")
    parser.add_argument("--benchmark", "-b", action="store_true", help="Run benchmarks")
    parser.add_argument("--clean", action="store_true", help="Clean reports directory")
    parser.add_argument("--list", "-l", action="store_true", help="List available tests")
    parser.add_argument("--validate", action="store_true", help="Validate environment")
    
    # Special test runners
    parser.add_argument("--unit", action="store_true", help="Run unit tests only")
    parser.add_argument("--integration", action="store_true", help="Run integration tests only")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--error-handling", action="store_true", help="Run error handling tests")
    parser.add_argument("--unicode", action="store_true", help="Run unicode tests")
    parser.add_argument("--concurrent", action="store_true", help="Run concurrent tests")
    parser.add_argument("--slow", action="store_true", help="Run slow tests")
    parser.add_argument("--api", action="store_true", help="Run API tests")
    parser.add_argument("--data-validation", action="store_true", help="Run data validation tests")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    # Handle special commands
    if args.clean:
        runner.clean_reports()
        return
    
    if args.list:
        runner.list_tests()
        return
    
    if args.validate:
        success = runner.validate_environment()
        sys.exit(0 if success else 1)
    
    # Determine test category and markers
    if args.unit:
        category = "unit"
    elif args.integration:
        category = "integration"
    else:
        category = args.category
    
    markers = args.markers
    if args.performance:
        markers = ["performance"]
    elif args.error_handling:
        markers = ["error_handling"]
    elif args.unicode:
        markers = ["unicode"]
    elif args.concurrent:
        markers = ["concurrent"]
    elif args.slow:
        markers = ["slow"]
    elif args.api:
        markers = ["api"]
    elif args.data_validation:
        markers = ["data_validation"]
    
    # Run tests
    try:
        result = runner.run_tests(
            category=category,
            markers=markers,
            verbose=args.verbose,
            coverage=args.coverage,
            parallel=args.parallel,
            html_report=args.html_report,
            json_report=args.json_report,
            benchmark=args.benchmark
        )
        
        # Exit with appropriate code
        sys.exit(0 if result["result"]["success"] else 1)
        
    except KeyboardInterrupt:
        print("\n⚠️  Test execution interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
