"""
Comprehensive Performance Tests for Tactics Master System

This module contains comprehensive performance tests to ensure the system can handle
concurrent requests and large data sets efficiently.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import json
import os
import sys
import time
import threading
import asyncio
from typing import Dict, Any, List
from fastapi.testclient import TestClient
import concurrent.futures
import multiprocessing

# Add the necessary paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

# Mock the hybrid_agent import before importing main
with patch.dict('sys.modules', {'hybrid_agent': Mock()}):
    from main import app

from agent import TacticsMasterAgent
from tools.cricket_api_tools import get_player_stats, get_team_squad, get_matchup_data, get_venue_stats
from tools.tactical_tools import analyze_weaknesses, find_best_matchup, generate_bowling_plan, generate_fielding_plan

class TestPerformanceBasics(unittest.TestCase):
    """Test basic performance metrics"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
        self.sample_query = "Test query"
        self.sample_context = {"team": "India"}
    
    def test_single_request_performance(self):
        """Test single request performance"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Test response",
                "analysis": {},
                "sources": []
            })
            
            start_time = time.time()
            
            request_data = {
                "query": self.sample_query,
                "context": self.sample_context
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            self.assertEqual(response.status_code, 200)
            self.assertLess(execution_time, 5.0)  # Should complete within 5 seconds
            print(f"Single request completed in {execution_time:.3f} seconds")
    
    def test_multiple_sequential_requests_performance(self):
        """Test multiple sequential requests performance"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Test response",
                "analysis": {},
                "sources": []
            })
            
            start_time = time.time()
            
            for i in range(10):
                request_data = {
                    "query": f"Test query {i}",
                    "context": self.sample_context
                }
                
                response = self.client.post("/analyze", json=request_data)
                self.assertEqual(response.status_code, 200)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            self.assertLess(execution_time, 10.0)  # Should complete within 10 seconds
            print(f"10 sequential requests completed in {execution_time:.3f} seconds")
    
    def test_cricket_api_tools_performance(self):
        """Test cricket API tools performance"""
        start_time = time.time()
        
        # Test all cricket API tools
        for i in range(5):
            player_stats = get_player_stats(f"Player {i}")
            team_squad = get_team_squad(f"Team {i}")
            matchup_data = get_matchup_data(f"Team {i}", f"Opponent {i}")
            venue_stats = get_venue_stats(f"Venue {i}")
            
            # Verify responses are valid JSON
            json.loads(player_stats)
            json.loads(team_squad)
            json.loads(matchup_data)
            json.loads(venue_stats)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertLess(execution_time, 5.0)  # Should complete within 5 seconds
        print(f"20 cricket API tool calls completed in {execution_time:.3f} seconds")
    
    def test_tactical_tools_performance(self):
        """Test tactical tools performance"""
        # Prepare test data
        player_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 45.0, "strike_rate": 120.0},
            "weaknesses": {"against_spin": {"average": 25.0}},
            "strengths": {"against_pace": {"average": 50.0}}
        }
        
        start_time = time.time()
        
        # Test all tactical tools
        for i in range(5):
            weakness_analysis = analyze_weaknesses(json.dumps(player_data))
            matchup_analysis = find_best_matchup(json.dumps(player_data), json.dumps(player_data))
            bowling_plan = generate_bowling_plan(json.dumps(player_data), f"Context {i}")
            fielding_plan = generate_fielding_plan(json.dumps(player_data), bowling_plan)
            
            # Verify responses are valid JSON
            json.loads(weakness_analysis)
            json.loads(matchup_analysis)
            json.loads(bowling_plan)
            json.loads(fielding_plan)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        self.assertLess(execution_time, 5.0)  # Should complete within 5 seconds
        print(f"20 tactical tool calls completed in {execution_time:.3f} seconds")

class TestConcurrentPerformance(unittest.TestCase):
    """Test concurrent performance"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
        self.sample_query = "Test query"
        self.sample_context = {"team": "India"}
    
    def test_concurrent_requests_performance(self):
        """Test concurrent requests performance"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Test response",
                "analysis": {},
                "sources": []
            })
            
            def make_request():
                request_data = {
                    "query": f"Test query {threading.current_thread().ident}",
                    "context": self.sample_context
                }
                
                response = self.client.post("/analyze", json=request_data)
                return response.status_code
            
            start_time = time.time()
            
            # Create multiple threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(make_request) for _ in range(10)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Verify all requests succeeded
            self.assertEqual(len(results), 10)
            for status_code in results:
                self.assertEqual(status_code, 200)
            
            self.assertLess(execution_time, 10.0)  # Should complete within 10 seconds
            print(f"10 concurrent requests completed in {execution_time:.3f} seconds")
    
    def test_high_concurrency_performance(self):
        """Test high concurrency performance"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Test response",
                "analysis": {},
                "sources": []
            })
            
            def make_request():
                request_data = {
                    "query": f"Test query {threading.current_thread().ident}",
                    "context": self.sample_context
                }
                
                response = self.client.post("/analyze", json=request_data)
                return response.status_code
            
            start_time = time.time()
            
            # Create many threads
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(make_request) for _ in range(50)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Verify all requests succeeded
            self.assertEqual(len(results), 50)
            for status_code in results:
                self.assertEqual(status_code, 200)
            
            self.assertLess(execution_time, 30.0)  # Should complete within 30 seconds
            print(f"50 concurrent requests completed in {execution_time:.3f} seconds")
    
    def test_cricket_api_tools_concurrent_performance(self):
        """Test cricket API tools concurrent performance"""
        def get_player_data():
            return get_player_stats("Test Player")
        
        def get_team_data():
            return get_team_squad("Test Team")
        
        def get_matchup_data_func():
            return get_matchup_data("Team1", "Team2")
        
        def get_venue_data():
            return get_venue_stats("Test Venue")
        
        start_time = time.time()
        
        # Run tools concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(get_player_data),
                executor.submit(get_team_data),
                executor.submit(get_matchup_data_func),
                executor.submit(get_venue_data)
            ]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify all responses are valid JSON
        for result in results:
            json.loads(result)
        
        self.assertLess(execution_time, 5.0)  # Should complete within 5 seconds
        print(f"4 concurrent cricket API tool calls completed in {execution_time:.3f} seconds")
    
    def test_tactical_tools_concurrent_performance(self):
        """Test tactical tools concurrent performance"""
        player_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 45.0, "strike_rate": 120.0},
            "weaknesses": {"against_spin": {"average": 25.0}},
            "strengths": {"against_pace": {"average": 50.0}}
        }
        
        def analyze_weaknesses_func():
            return analyze_weaknesses(json.dumps(player_data))
        
        def find_matchup_func():
            return find_best_matchup(json.dumps(player_data), json.dumps(player_data))
        
        def generate_bowling_plan_func():
            return generate_bowling_plan(json.dumps(player_data), "Test context")
        
        def generate_fielding_plan_func():
            bowling_plan = generate_bowling_plan(json.dumps(player_data), "Test context")
            return generate_fielding_plan(json.dumps(player_data), bowling_plan)
        
        start_time = time.time()
        
        # Run tools concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            futures = [
                executor.submit(analyze_weaknesses_func),
                executor.submit(find_matchup_func),
                executor.submit(generate_bowling_plan_func),
                executor.submit(generate_fielding_plan_func)
            ]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify all responses are valid JSON
        for result in results:
            json.loads(result)
        
        self.assertLess(execution_time, 5.0)  # Should complete within 5 seconds
        print(f"4 concurrent tactical tool calls completed in {execution_time:.3f} seconds")

class TestLargeDataPerformance(unittest.TestCase):
    """Test performance with large data sets"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
    
    def test_large_context_performance(self):
        """Test performance with large context"""
        large_context = {
            "team": "India",
            "players": [f"Player {i}" for i in range(1000)],
            "match_info": {
                "venue": "Narendra Modi Stadium",
                "conditions": {
                    "pitch": "batting_friendly",
                    "weather": "clear"
                }
            },
            "data": {f"key_{i}": f"value_{i}" for i in range(10000)}
        }
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Test response",
                "analysis": {},
                "sources": []
            })
            
            start_time = time.time()
            
            request_data = {
                "query": "Test query",
                "context": large_context
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            self.assertEqual(response.status_code, 200)
            self.assertLess(execution_time, 10.0)  # Should complete within 10 seconds
            print(f"Large context request completed in {execution_time:.3f} seconds")
    
    def test_large_player_data_performance(self):
        """Test performance with large player data"""
        large_player_data = {
            "player_name": "Test Player",
            "recent_form": {"batting_average": 45.0, "strike_rate": 120.0},
            "weaknesses": {f"weakness_{i}": {"average": i} for i in range(1000)},
            "strengths": {f"strength_{i}": {"average": i} for i in range(1000)},
            "recent_matches": [{"runs": i, "balls": i*2} for i in range(1000)]
        }
        
        start_time = time.time()
        
        # Test weakness analysis with large data
        weakness_analysis = analyze_weaknesses(json.dumps(large_player_data))
        weakness_data = json.loads(weakness_analysis)
        
        # Test bowling plan with large data
        bowling_plan = generate_bowling_plan(json.dumps(large_player_data), "Test context")
        bowling_data = json.loads(bowling_plan)
        
        # Test fielding plan with large data
        fielding_plan = generate_fielding_plan(json.dumps(large_player_data), bowling_plan)
        fielding_data = json.loads(fielding_plan)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify responses are valid
        self.assertIn("player_name", weakness_data)
        self.assertIn("player_name", bowling_data)
        self.assertIn("player_name", fielding_data)
        
        self.assertLess(execution_time, 10.0)  # Should complete within 10 seconds
        print(f"Large player data processing completed in {execution_time:.3f} seconds")
    
    def test_very_large_query_performance(self):
        """Test performance with very large query"""
        large_query = "Test query " + "A" * 10000  # Very large query
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Test response",
                "analysis": {},
                "sources": []
            })
            
            start_time = time.time()
            
            request_data = {
                "query": large_query,
                "context": {"team": "India"}
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Should handle large query gracefully
            self.assertIn(response.status_code, [200, 422])
            if response.status_code == 200:
                self.assertLess(execution_time, 10.0)  # Should complete within 10 seconds
                print(f"Large query request completed in {execution_time:.3f} seconds")
    
    def test_deeply_nested_context_performance(self):
        """Test performance with deeply nested context"""
        # Create deeply nested context
        nested_context = {"level1": {"level2": {"level3": {"level4": {"level5": {"level6": {"level7": {"level8": {"level9": {"level10": {"value": "deep"}}}}}}}}}}
        
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Test response",
                "analysis": {},
                "sources": []
            })
            
            start_time = time.time()
            
            request_data = {
                "query": "Test query",
                "context": nested_context
            }
            
            response = self.client.post("/analyze", json=request_data)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Should handle deep nesting gracefully
            self.assertIn(response.status_code, [200, 422])
            if response.status_code == 200:
                self.assertLess(execution_time, 10.0)  # Should complete within 10 seconds
                print(f"Deeply nested context request completed in {execution_time:.3f} seconds")

class TestMemoryPerformance(unittest.TestCase):
    """Test memory performance"""
    
    def test_memory_usage_with_large_data(self):
        """Test memory usage with large data"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Create large data sets
        large_data_sets = []
        for i in range(100):
            large_data = {
                "player_name": f"Player {i}",
                "recent_form": {"batting_average": 45.0, "strike_rate": 120.0},
                "weaknesses": {f"weakness_{j}": {"average": j} for j in range(100)},
                "strengths": {f"strength_{j}": {"average": j} for j in range(100)},
                "recent_matches": [{"runs": j, "balls": j*2} for j in range(100)]
            }
            large_data_sets.append(large_data)
        
        # Process large data sets
        for data in large_data_sets:
            weakness_analysis = analyze_weaknesses(json.dumps(data))
            json.loads(weakness_analysis)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 100MB)
        self.assertLess(memory_increase, 100.0)
        print(f"Memory usage increased by {memory_increase:.2f} MB")
    
    def test_memory_usage_with_concurrent_requests(self):
        """Test memory usage with concurrent requests"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        def process_data():
            data = {
                "player_name": "Test Player",
                "recent_form": {"batting_average": 45.0, "strike_rate": 120.0},
                "weaknesses": {"against_spin": {"average": 25.0}},
                "strengths": {"against_pace": {"average": 50.0}}
            }
            
            weakness_analysis = analyze_weaknesses(json.dumps(data))
            matchup_analysis = find_best_matchup(json.dumps(data), json.dumps(data))
            bowling_plan = generate_bowling_plan(json.dumps(data), "Test context")
            fielding_plan = generate_fielding_plan(json.dumps(data), bowling_plan)
            
            return {
                "weakness": json.loads(weakness_analysis),
                "matchup": json.loads(matchup_analysis),
                "bowling": json.loads(bowling_plan),
                "fielding": json.loads(fielding_plan)
            }
        
        # Run concurrent processing
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(process_data) for _ in range(50)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable (less than 200MB)
        self.assertLess(memory_increase, 200.0)
        print(f"Memory usage increased by {memory_increase:.2f} MB with concurrent processing")
    
    def test_memory_cleanup_performance(self):
        """Test memory cleanup performance"""
        import gc
        
        # Create and process large data
        for i in range(100):
            large_data = {
                "player_name": f"Player {i}",
                "recent_form": {"batting_average": 45.0, "strike_rate": 120.0},
                "weaknesses": {f"weakness_{j}": {"average": j} for j in range(100)},
                "strengths": {f"strength_{j}": {"average": j} for j in range(100)},
                "recent_matches": [{"runs": j, "balls": j*2} for j in range(100)]
            }
            
            weakness_analysis = analyze_weaknesses(json.dumps(large_data))
            json.loads(weakness_analysis)
        
        # Force garbage collection
        gc.collect()
        
        # Memory should be cleaned up
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        memory_usage = process.memory_info().rss / 1024 / 1024  # MB
        
        # Memory usage should be reasonable (less than 500MB)
        self.assertLess(memory_usage, 500.0)
        print(f"Memory usage after cleanup: {memory_usage:.2f} MB")

class TestStressPerformance(unittest.TestCase):
    """Test stress performance"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
    
    def test_stress_test_sequential_requests(self):
        """Test stress with sequential requests"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Test response",
                "analysis": {},
                "sources": []
            })
            
            start_time = time.time()
            
            for i in range(100):
                request_data = {
                    "query": f"Test query {i}",
                    "context": {"team": "India"}
                }
                
                response = self.client.post("/analyze", json=request_data)
                self.assertEqual(response.status_code, 200)
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            self.assertLess(execution_time, 60.0)  # Should complete within 60 seconds
            print(f"100 sequential requests completed in {execution_time:.3f} seconds")
    
    def test_stress_test_concurrent_requests(self):
        """Test stress with concurrent requests"""
        with patch('backend.main.agent') as mock_agent:
            mock_agent.analyze = AsyncMock(return_value={
                "response": "Test response",
                "analysis": {},
                "sources": []
            })
            
            def make_request():
                request_data = {
                    "query": f"Test query {threading.current_thread().ident}",
                    "context": {"team": "India"}
                }
                
                response = self.client.post("/analyze", json=request_data)
                return response.status_code
            
            start_time = time.time()
            
            # Create many concurrent requests
            with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
                futures = [executor.submit(make_request) for _ in range(100)]
                results = [future.result() for future in concurrent.futures.as_completed(futures)]
            
            end_time = time.time()
            execution_time = end_time - start_time
            
            # Verify all requests succeeded
            self.assertEqual(len(results), 100)
            for status_code in results:
                self.assertEqual(status_code, 200)
            
            self.assertLess(execution_time, 60.0)  # Should complete within 60 seconds
            print(f"100 concurrent requests completed in {execution_time:.3f} seconds")
    
    def test_stress_test_mixed_operations(self):
        """Test stress with mixed operations"""
        def mixed_operation():
            # Mix of different operations
            player_stats = get_player_stats("Test Player")
            team_squad = get_team_squad("Test Team")
            matchup_data = get_matchup_data("Team1", "Team2")
            venue_stats = get_venue_stats("Test Venue")
            
            # Tactical analysis
            weakness_analysis = analyze_weaknesses(player_stats)
            matchup_analysis = find_best_matchup(player_stats, player_stats)
            bowling_plan = generate_bowling_plan(player_stats, "Test context")
            fielding_plan = generate_fielding_plan(player_stats, bowling_plan)
            
            # Verify all responses
            json.loads(player_stats)
            json.loads(team_squad)
            json.loads(matchup_data)
            json.loads(venue_stats)
            json.loads(weakness_analysis)
            json.loads(matchup_analysis)
            json.loads(bowling_plan)
            json.loads(fielding_plan)
            
            return True
        
        start_time = time.time()
        
        # Run mixed operations concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(mixed_operation) for _ in range(50)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify all operations succeeded
        self.assertEqual(len(results), 50)
        for result in results:
            self.assertTrue(result)
        
        self.assertLess(execution_time, 60.0)  # Should complete within 60 seconds
        print(f"50 mixed operations completed in {execution_time:.3f} seconds")
    
    def test_stress_test_large_data_processing(self):
        """Test stress with large data processing"""
        def process_large_data():
            large_data = {
                "player_name": "Test Player",
                "recent_form": {"batting_average": 45.0, "strike_rate": 120.0},
                "weaknesses": {f"weakness_{i}": {"average": i} for i in range(100)},
                "strengths": {f"strength_{i}": {"average": i} for i in range(100)},
                "recent_matches": [{"runs": i, "balls": i*2} for i in range(100)]
            }
            
            # Process large data
            weakness_analysis = analyze_weaknesses(json.dumps(large_data))
            matchup_analysis = find_best_matchup(json.dumps(large_data), json.dumps(large_data))
            bowling_plan = generate_bowling_plan(json.dumps(large_data), "Test context")
            fielding_plan = generate_fielding_plan(json.dumps(large_data), bowling_plan)
            
            # Verify responses
            json.loads(weakness_analysis)
            json.loads(matchup_analysis)
            json.loads(bowling_plan)
            json.loads(fielding_plan)
            
            return True
        
        start_time = time.time()
        
        # Run large data processing concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(process_large_data) for _ in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify all operations succeeded
        self.assertEqual(len(results), 20)
        for result in results:
            self.assertTrue(result)
        
        self.assertLess(execution_time, 60.0)  # Should complete within 60 seconds
        print(f"20 large data processing operations completed in {execution_time:.3f} seconds")

class TestPerformanceBenchmarks(unittest.TestCase):
    """Test performance benchmarks"""
    
    def test_benchmark_single_operation(self):
        """Benchmark single operation performance"""
        start_time = time.time()
        
        # Single operation
        player_stats = get_player_stats("Test Player")
        json.loads(player_stats)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within 1 second
        self.assertLess(execution_time, 1.0)
        print(f"Single operation benchmark: {execution_time:.3f} seconds")
    
    def test_benchmark_workflow_performance(self):
        """Benchmark complete workflow performance"""
        start_time = time.time()
        
        # Complete workflow
        player_stats = get_player_stats("Test Player")
        weakness_analysis = analyze_weaknesses(player_stats)
        matchup_analysis = find_best_matchup(player_stats, player_stats)
        bowling_plan = generate_bowling_plan(player_stats, "Test context")
        fielding_plan = generate_fielding_plan(player_stats, bowling_plan)
        
        # Verify all responses
        json.loads(player_stats)
        json.loads(weakness_analysis)
        json.loads(matchup_analysis)
        json.loads(bowling_plan)
        json.loads(fielding_plan)
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Should complete within 5 seconds
        self.assertLess(execution_time, 5.0)
        print(f"Complete workflow benchmark: {execution_time:.3f} seconds")
    
    def test_benchmark_concurrent_performance(self):
        """Benchmark concurrent performance"""
        def benchmark_operation():
            player_stats = get_player_stats("Test Player")
            weakness_analysis = analyze_weaknesses(player_stats)
            json.loads(player_stats)
            json.loads(weakness_analysis)
            return True
        
        start_time = time.time()
        
        # Run concurrent operations
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(benchmark_operation) for _ in range(20)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Verify all operations succeeded
        self.assertEqual(len(results), 20)
        for result in results:
            self.assertTrue(result)
        
        # Should complete within 10 seconds
        self.assertLess(execution_time, 10.0)
        print(f"Concurrent operations benchmark: {execution_time:.3f} seconds")
    
    def test_benchmark_memory_efficiency(self):
        """Benchmark memory efficiency"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Process many operations
        for i in range(100):
            player_stats = get_player_stats(f"Player {i}")
            weakness_analysis = analyze_weaknesses(player_stats)
            json.loads(player_stats)
            json.loads(weakness_analysis)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        
        # Memory increase should be reasonable
        self.assertLess(memory_increase, 50.0)  # Less than 50MB increase
        print(f"Memory efficiency benchmark: {memory_increase:.2f} MB increase")

if __name__ == '__main__':
    unittest.main()
