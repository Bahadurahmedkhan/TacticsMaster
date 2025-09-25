"""
Comprehensive Test Runner for Tactics Master System

This module provides a comprehensive test runner that executes all unit tests
and provides detailed reporting on test coverage and performance.
"""

import unittest
import sys
import os
import time
import json
from typing import Dict, Any, List
import subprocess
import coverage

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

class TestRunner:
    """Comprehensive test runner for the Tactics Master system"""
    
    def __init__(self):
        """Initialize the test runner"""
        self.test_results = {}
        self.coverage_results = {}
        self.performance_results = {}
        self.start_time = None
        self.end_time = None
    
    def run_all_tests(self) -> Dict[str, Any]:
        """Run all tests and return comprehensive results"""
        print("🚀 Starting Comprehensive Test Suite for Tactics Master System")
        print("=" * 80)
        
        self.start_time = time.time()
        
        # Test modules to run
        test_modules = [
            'test_comprehensive_agent',
            'test_comprehensive_cricket_api_tools',
            'test_comprehensive_tactical_tools',
            'test_comprehensive_backend_api',
            'test_comprehensive_hybrid_agent',
            'test_comprehensive_integration',
            'test_comprehensive_error_handling',
            'test_comprehensive_performance'
        ]
        
        # Run each test module
        for module_name in test_modules:
            print(f"\n📋 Running {module_name}...")
            self._run_test_module(module_name)
        
        self.end_time = time.time()
        
        # Generate comprehensive report
        report = self._generate_report()
        
        print("\n" + "=" * 80)
        print("✅ Test Suite Completed Successfully!")
        print(f"⏱️  Total Execution Time: {self.end_time - self.start_time:.2f} seconds")
        print("=" * 80)
        
        return report
    
    def _run_test_module(self, module_name: str):
        """Run a specific test module"""
        try:
            # Import the test module
            module = __import__(module_name)
            
            # Create test suite
            loader = unittest.TestLoader()
            suite = loader.loadTestsFromModule(module)
            
            # Run tests
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            
            # Store results
            self.test_results[module_name] = {
                'tests_run': result.testsRun,
                'failures': len(result.failures),
                'errors': len(result.errors),
                'skipped': len(result.skipped) if hasattr(result, 'skipped') else 0,
                'success_rate': (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100 if result.testsRun > 0 else 0
            }
            
            print(f"✅ {module_name}: {result.testsRun} tests, {len(result.failures)} failures, {len(result.errors)} errors")
            
        except Exception as e:
            print(f"❌ Error running {module_name}: {e}")
            self.test_results[module_name] = {
                'tests_run': 0,
                'failures': 0,
                'errors': 1,
                'skipped': 0,
                'success_rate': 0,
                'error': str(e)
            }
    
    def run_coverage_analysis(self) -> Dict[str, Any]:
        """Run coverage analysis on the codebase"""
        print("\n📊 Running Coverage Analysis...")
        
        try:
            # Initialize coverage
            cov = coverage.Coverage()
            cov.start()
            
            # Run all tests
            self.run_all_tests()
            
            # Stop coverage
            cov.stop()
            cov.save()
            
            # Generate coverage report
            coverage_data = cov.get_data()
            
            # Get coverage summary
            total_lines = coverage_data.n_lines
            covered_lines = coverage_data.n_executed_lines
            coverage_percentage = (covered_lines / total_lines * 100) if total_lines > 0 else 0
            
            self.coverage_results = {
                'total_lines': total_lines,
                'covered_lines': covered_lines,
                'coverage_percentage': coverage_percentage,
                'missing_lines': total_lines - covered_lines
            }
            
            print(f"📈 Coverage: {coverage_percentage:.2f}% ({covered_lines}/{total_lines} lines)")
            
            return self.coverage_results
            
        except Exception as e:
            print(f"❌ Coverage analysis failed: {e}")
            return {'error': str(e)}
    
    def run_performance_benchmarks(self) -> Dict[str, Any]:
        """Run performance benchmarks"""
        print("\n⚡ Running Performance Benchmarks...")
        
        try:
            # Import performance test module
            from test_comprehensive_performance import TestPerformanceBasics, TestConcurrentPerformance, TestLargeDataPerformance
            
            # Run performance tests
            performance_tests = [
                TestPerformanceBasics,
                TestConcurrentPerformance,
                TestLargeDataPerformance
            ]
            
            for test_class in performance_tests:
                print(f"Running {test_class.__name__}...")
                
                # Create test instance
                test_instance = test_class()
                
                # Run performance tests
                for method_name in dir(test_instance):
                    if method_name.startswith('test_'):
                        method = getattr(test_instance, method_name)
                        if callable(method):
                            start_time = time.time()
                            try:
                                method()
                                end_time = time.time()
                                execution_time = end_time - start_time
                                
                                self.performance_results[method_name] = {
                                    'execution_time': execution_time,
                                    'status': 'success'
                                }
                                
                                print(f"  ✅ {method_name}: {execution_time:.3f}s")
                                
                            except Exception as e:
                                self.performance_results[method_name] = {
                                    'execution_time': 0,
                                    'status': 'failed',
                                    'error': str(e)
                                }
                                
                                print(f"  ❌ {method_name}: {e}")
            
            return self.performance_results
            
        except Exception as e:
            print(f"❌ Performance benchmarks failed: {e}")
            return {'error': str(e)}
    
    def _generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive test report"""
        total_tests = sum(result['tests_run'] for result in self.test_results.values())
        total_failures = sum(result['failures'] for result in self.test_results.values())
        total_errors = sum(result['errors'] for result in self.test_results.values())
        total_skipped = sum(result['skipped'] for result in self.test_results.values())
        
        overall_success_rate = ((total_tests - total_failures - total_errors) / total_tests * 100) if total_tests > 0 else 0
        
        report = {
            'summary': {
                'total_tests': total_tests,
                'total_failures': total_failures,
                'total_errors': total_errors,
                'total_skipped': total_skipped,
                'overall_success_rate': overall_success_rate,
                'execution_time': self.end_time - self.start_time if self.end_time and self.start_time else 0
            },
            'module_results': self.test_results,
            'coverage': self.coverage_results,
            'performance': self.performance_results,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return report
    
    def save_report(self, report: Dict[str, Any], filename: str = 'test_report.json'):
        """Save test report to file"""
        try:
            with open(filename, 'w') as f:
                json.dump(report, f, indent=2)
            print(f"📄 Test report saved to {filename}")
        except Exception as e:
            print(f"❌ Failed to save report: {e}")
    
    def print_summary(self, report: Dict[str, Any]):
        """Print test summary"""
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY")
        print("=" * 80)
        
        summary = report['summary']
        print(f"Total Tests: {summary['total_tests']}")
        print(f"Failures: {summary['total_failures']}")
        print(f"Errors: {summary['total_errors']}")
        print(f"Skipped: {summary['total_skipped']}")
        print(f"Success Rate: {summary['overall_success_rate']:.2f}%")
        print(f"Execution Time: {summary['execution_time']:.2f} seconds")
        
        if report['coverage']:
            coverage = report['coverage']
            print(f"Coverage: {coverage['coverage_percentage']:.2f}%")
            print(f"Covered Lines: {coverage['covered_lines']}/{coverage['total_lines']}")
        
        print("\n📋 MODULE RESULTS:")
        for module, result in report['module_results'].items():
            status = "✅" if result['success_rate'] == 100 else "❌"
            print(f"  {status} {module}: {result['tests_run']} tests, {result['success_rate']:.1f}% success")
        
        if report['performance']:
            print("\n⚡ PERFORMANCE RESULTS:")
            for test, result in report['performance'].items():
                if result['status'] == 'success':
                    print(f"  ✅ {test}: {result['execution_time']:.3f}s")
                else:
                    print(f"  ❌ {test}: {result['error']}")

def main():
    """Main function to run all tests"""
    runner = TestRunner()
    
    # Run all tests
    report = runner.run_all_tests()
    
    # Print summary
    runner.print_summary(report)
    
    # Save report
    runner.save_report(report)
    
    # Run coverage analysis
    print("\n" + "=" * 80)
    print("📊 COVERAGE ANALYSIS")
    print("=" * 80)
    coverage_results = runner.run_coverage_analysis()
    
    # Run performance benchmarks
    print("\n" + "=" * 80)
    print("⚡ PERFORMANCE BENCHMARKS")
    print("=" * 80)
    performance_results = runner.run_performance_benchmarks()
    
    # Update report with coverage and performance
    report['coverage'] = coverage_results
    report['performance'] = performance_results
    
    # Save updated report
    runner.save_report(report, 'comprehensive_test_report.json')
    
    # Print final summary
    runner.print_summary(report)
    
    return report

if __name__ == '__main__':
    main()
