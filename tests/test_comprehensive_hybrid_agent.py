"""
Comprehensive Unit Tests for HybridTacticsMasterAgent

This module contains comprehensive unit tests for the HybridTacticsMasterAgent class
including API integration, fallback mechanisms, and async analysis methods.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, AsyncMock
import json
import os
import sys
import asyncio
from typing import Dict, Any, List
import requests

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from hybrid_agent import HybridTacticsMasterAgent

class TestHybridTacticsMasterAgentComprehensive(unittest.TestCase):
    """Comprehensive test cases for HybridTacticsMasterAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_query = "Analyze Virat Kohli's batting weaknesses"
        self.sample_context = {
            "team": "India",
            "opponent": "Australia",
            "venue": "Narendra Modi Stadium"
        }
        
        # Mock cricket data response
        self.mock_cricket_data = {
            "matches": [
                {
                    "name": "India vs Australia",
                    "status": "Live",
                    "venue": "Narendra Modi Stadium"
                }
            ],
            "players": [
                {
                    "name": "Virat Kohli",
                    "stats": {"batting_average": 50.0}
                }
            ]
        }
        
        # Mock AI analysis response
        self.mock_ai_response = {
            "response": "AI-generated analysis response",
            "analysis": {
                "ai_generated": True,
                "data_sources": ["CricAPI", "Gemini AI"],
                "confidence": "High"
            },
            "sources": ["CricAPI", "Gemini AI Analysis"]
        }
        
        # Mock fallback response
        self.mock_fallback_response = {
            "response": "Fallback analysis response",
            "analysis": {
                "data_driven": True,
                "real_cricket_data": True,
                "match_count": 1,
                "confidence": "High"
            },
            "sources": ["CricAPI Real Data", "Cricket Analytics Database"]
        }
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_gemini_key', 'CRICKET_API_KEY': 'test_cricket_key'})
    def test_agent_initialization_with_both_keys(self):
        """Test agent initialization with both API keys"""
        agent = HybridTacticsMasterAgent()
        
        self.assertEqual(agent.cricket_api_key, 'test_cricket_key')
        self.assertEqual(agent.gemini_api_key, 'test_gemini_key')
        self.assertIsNotNone(agent.llm)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'test_gemini_key'})
    def test_agent_initialization_with_gemini_only(self):
        """Test agent initialization with only Gemini API key"""
        agent = HybridTacticsMasterAgent()
        
        self.assertIsNone(agent.cricket_api_key)
        self.assertEqual(agent.gemini_api_key, 'test_gemini_key')
        self.assertIsNotNone(agent.llm)
    
    @patch.dict(os.environ, {'CRICKET_API_KEY': 'test_cricket_key'})
    def test_agent_initialization_with_cricket_only(self):
        """Test agent initialization with only cricket API key"""
        agent = HybridTacticsMasterAgent()
        
        self.assertEqual(agent.cricket_api_key, 'test_cricket_key')
        self.assertIsNone(agent.gemini_api_key)
        self.assertIsNone(agent.llm)
    
    @patch.dict(os.environ, {})
    def test_agent_initialization_with_no_keys(self):
        """Test agent initialization with no API keys"""
        agent = HybridTacticsMasterAgent()
        
        self.assertIsNone(agent.cricket_api_key)
        self.assertIsNone(agent.gemini_api_key)
        self.assertIsNone(agent.llm)
    
    @patch.dict(os.environ, {'GEMINI_API_KEY': 'invalid_key'})
    def test_agent_initialization_with_invalid_gemini_key(self):
        """Test agent initialization with invalid Gemini API key"""
        with patch('backend.hybrid_agent.ChatGoogleGenerativeAI') as mock_gemini:
            mock_gemini.side_effect = Exception("Invalid API key")
            
            agent = HybridTacticsMasterAgent()
            
            self.assertEqual(agent.gemini_api_key, 'invalid_key')
            self.assertIsNone(agent.llm)
    
    async def test_analyze_success_with_ai(self):
        """Test successful analysis with AI"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key', 'CRICKET_API_KEY': 'test_key'}):
            agent = HybridTacticsMasterAgent()
            
            # Mock the methods
            agent._get_cricket_data = AsyncMock(return_value=self.mock_cricket_data)
            agent._ai_analyze = AsyncMock(return_value=self.mock_ai_response)
            
            result = await agent.analyze(self.sample_query, self.sample_context)
            
            self.assertIn("response", result)
            self.assertIn("analysis", result)
            self.assertIn("sources", result)
            self.assertEqual(result["response"], "AI-generated analysis response")
            self.assertTrue(result["analysis"]["ai_generated"])
    
    async def test_analyze_success_with_fallback(self):
        """Test successful analysis with fallback"""
        with patch.dict(os.environ, {'CRICKET_API_KEY': 'test_key'}):
            agent = HybridTacticsMasterAgent()
            
            # Mock the methods
            agent._get_cricket_data = AsyncMock(return_value=self.mock_cricket_data)
            agent._intelligent_fallback = Mock(return_value=self.mock_fallback_response)
            
            result = await agent.analyze(self.sample_query, self.sample_context)
            
            self.assertIn("response", result)
            self.assertIn("analysis", result)
            self.assertIn("sources", result)
            self.assertEqual(result["response"], "Fallback analysis response")
            self.assertTrue(result["analysis"]["data_driven"])
    
    async def test_analyze_empty_query(self):
        """Test analysis with empty query"""
        agent = HybridTacticsMasterAgent()
        
        result = await agent.analyze("", self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("valid query", result["response"])
        self.assertEqual(result["analysis"], {})
        self.assertEqual(result["sources"], [])
    
    async def test_analyze_none_query(self):
        """Test analysis with None query"""
        agent = HybridTacticsMasterAgent()
        
        result = await agent.analyze(None, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("valid query", result["response"])
        self.assertEqual(result["analysis"], {})
        self.assertEqual(result["sources"], [])
    
    async def test_analyze_whitespace_query(self):
        """Test analysis with whitespace-only query"""
        agent = HybridTacticsMasterAgent()
        
        result = await agent.analyze("   ", self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("valid query", result["response"])
        self.assertEqual(result["analysis"], {})
        self.assertEqual(result["sources"], [])
    
    async def test_analyze_exception_handling(self):
        """Test analysis exception handling"""
        agent = HybridTacticsMasterAgent()
        
        # Mock _get_cricket_data to raise exception
        agent._get_cricket_data = AsyncMock(side_effect=Exception("Cricket data error"))
        
        result = await agent.analyze(self.sample_query, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("error", result["response"])
        self.assertEqual(result["analysis"], {})
        self.assertEqual(result["sources"], [])
    
    async def test_get_cricket_data_success(self):
        """Test successful cricket data retrieval"""
        with patch.dict(os.environ, {'CRICKET_API_KEY': 'test_key'}):
            agent = HybridTacticsMasterAgent()
            
            # Mock requests.get
            with patch('backend.hybrid_agent.requests.get') as mock_get:
                # Mock matches response
                matches_response = Mock()
                matches_response.status_code = 200
                matches_response.json.return_value = {"data": self.mock_cricket_data["matches"]}
                
                # Mock players response
                players_response = Mock()
                players_response.status_code = 200
                players_response.json.return_value = {"data": self.mock_cricket_data["players"]}
                
                mock_get.side_effect = [matches_response, players_response]
                
                result = await agent._get_cricket_data(self.sample_query, self.sample_context)
                
                self.assertIn("matches", result)
                self.assertIn("players", result)
                self.assertIn("query", result)
                self.assertIn("context", result)
                self.assertEqual(len(result["matches"]), 1)
                self.assertEqual(len(result["players"]), 1)
    
    async def test_get_cricket_data_no_api_key(self):
        """Test cricket data retrieval without API key"""
        agent = HybridTacticsMasterAgent()
        
        result = await agent._get_cricket_data(self.sample_query, self.sample_context)
        
        self.assertEqual(result, {})
    
    async def test_get_cricket_data_api_failure(self):
        """Test cricket data retrieval with API failure"""
        with patch.dict(os.environ, {'CRICKET_API_KEY': 'test_key'}):
            agent = HybridTacticsMasterAgent()
            
            # Mock requests.get to raise exception
            with patch('backend.hybrid_agent.requests.get') as mock_get:
                mock_get.side_effect = Exception("API error")
                
                result = await agent._get_cricket_data(self.sample_query, self.sample_context)
                
                self.assertEqual(result, {})
    
    async def test_get_cricket_data_http_error(self):
        """Test cricket data retrieval with HTTP error"""
        with patch.dict(os.environ, {'CRICKET_API_KEY': 'test_key'}):
            agent = HybridTacticsMasterAgent()
            
            # Mock requests.get to return error status
            with patch('backend.hybrid_agent.requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 404
                mock_get.return_value = mock_response
                
                result = await agent._get_cricket_data(self.sample_query, self.sample_context)
                
                self.assertEqual(result, {})
    
    async def test_get_cricket_data_timeout(self):
        """Test cricket data retrieval with timeout"""
        with patch.dict(os.environ, {'CRICKET_API_KEY': 'test_key'}):
            agent = HybridTacticsMasterAgent()
            
            # Mock requests.get to raise timeout
            with patch('backend.hybrid_agent.requests.get') as mock_get:
                mock_get.side_effect = requests.Timeout("Request timeout")
                
                result = await agent._get_cricket_data(self.sample_query, self.sample_context)
                
                self.assertEqual(result, {})
    
    async def test_ai_analyze_success(self):
        """Test successful AI analysis"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            agent = HybridTacticsMasterAgent()
            
            # Mock LLM response
            mock_llm_response = Mock()
            mock_llm_response.content = "AI-generated analysis response"
            agent.llm.invoke = Mock(return_value=mock_llm_response)
            
            result = await agent._ai_analyze(self.sample_query, self.mock_cricket_data, self.sample_context)
            
            self.assertIn("response", result)
            self.assertIn("analysis", result)
            self.assertIn("sources", result)
            self.assertEqual(result["response"], "AI-generated analysis response")
            self.assertTrue(result["analysis"]["ai_generated"])
            self.assertEqual(result["sources"], ["CricAPI", "Gemini AI Analysis"])
    
    async def test_ai_analyze_exception(self):
        """Test AI analysis with exception"""
        with patch.dict(os.environ, {'GEMINI_API_KEY': 'test_key'}):
            agent = HybridTacticsMasterAgent()
            
            # Mock LLM to raise exception
            agent.llm.invoke = Mock(side_effect=Exception("AI analysis failed"))
            
            # Mock fallback method
            agent._intelligent_fallback = Mock(return_value=self.mock_fallback_response)
            
            result = await agent._ai_analyze(self.sample_query, self.mock_cricket_data, self.sample_context)
            
            self.assertEqual(result, self.mock_fallback_response)
    
    def test_intelligent_fallback_batting_query(self):
        """Test intelligent fallback with batting query"""
        agent = HybridTacticsMasterAgent()
        
        query = "Analyze batting weaknesses"
        result = agent._intelligent_fallback(query, self.mock_cricket_data, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("batting", result["response"])
        self.assertTrue(result["analysis"]["data_driven"])
    
    def test_intelligent_fallback_bowling_query(self):
        """Test intelligent fallback with bowling query"""
        agent = HybridTacticsMasterAgent()
        
        query = "Analyze bowling strategies"
        result = agent._intelligent_fallback(query, self.mock_cricket_data, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("bowling", result["response"])
        self.assertTrue(result["analysis"]["data_driven"])
    
    def test_intelligent_fallback_general_query(self):
        """Test intelligent fallback with general query"""
        agent = HybridTacticsMasterAgent()
        
        query = "General cricket analysis"
        result = agent._intelligent_fallback(query, self.mock_cricket_data, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("General Cricket Tactics Analysis", result["response"])
        self.assertTrue(result["analysis"]["data_driven"])
    
    def test_intelligent_fallback_no_cricket_data(self):
        """Test intelligent fallback without cricket data"""
        agent = HybridTacticsMasterAgent()
        
        query = "Analyze batting weaknesses"
        result = agent._intelligent_fallback(query, {}, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("batting", result["response"])
        self.assertFalse(result["analysis"]["real_cricket_data"])
        self.assertEqual(result["analysis"]["match_count"], 0)
    
    def test_intelligent_fallback_with_cricket_data(self):
        """Test intelligent fallback with cricket data"""
        agent = HybridTacticsMasterAgent()
        
        query = "Analyze batting weaknesses"
        result = agent._intelligent_fallback(query, self.mock_cricket_data, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("batting", result["response"])
        self.assertTrue(result["analysis"]["real_cricket_data"])
        self.assertEqual(result["analysis"]["match_count"], 1)
    
    def test_intelligent_fallback_unicode_query(self):
        """Test intelligent fallback with unicode query"""
        agent = HybridTacticsMasterAgent()
        
        query = "Analyze batting weaknesses 分析"
        result = agent._intelligent_fallback(query, self.mock_cricket_data, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("batting", result["response"])
    
    def test_intelligent_fallback_special_characters(self):
        """Test intelligent fallback with special characters"""
        agent = HybridTacticsMasterAgent()
        
        query = "Analyze batting weaknesses!@#$%^&*()"
        result = agent._intelligent_fallback(query, self.mock_cricket_data, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("batting", result["response"])
    
    def test_intelligent_fallback_very_long_query(self):
        """Test intelligent fallback with very long query"""
        agent = HybridTacticsMasterAgent()
        
        query = "Analyze batting weaknesses " + "A" * 1000
        result = agent._intelligent_fallback(query, self.mock_cricket_data, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("batting", result["response"])
    
    def test_intelligent_fallback_complex_context(self):
        """Test intelligent fallback with complex context"""
        agent = HybridTacticsMasterAgent()
        
        complex_context = {
            "team": "India",
            "players": ["Virat Kohli", "Rohit Sharma"],
            "match_info": {
                "venue": "Narendra Modi Stadium",
                "conditions": {
                    "pitch": "batting_friendly",
                    "weather": "clear"
                }
            },
            "nested": {
                "deep": {
                    "value": "test"
                }
            }
        }
        
        query = "Analyze batting weaknesses"
        result = agent._intelligent_fallback(query, self.mock_cricket_data, complex_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("batting", result["response"])
    
    def test_intelligent_fallback_none_context(self):
        """Test intelligent fallback with None context"""
        agent = HybridTacticsMasterAgent()
        
        query = "Analyze batting weaknesses"
        result = agent._intelligent_fallback(query, self.mock_cricket_data, None)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("batting", result["response"])
    
    def test_intelligent_fallback_empty_context(self):
        """Test intelligent fallback with empty context"""
        agent = HybridTacticsMasterAgent()
        
        query = "Analyze batting weaknesses"
        result = agent._intelligent_fallback(query, self.mock_cricket_data, {})
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
        self.assertIn("batting", result["response"])

class TestHybridTacticsMasterAgentEdgeCases(unittest.TestCase):
    """Test edge cases and error scenarios for HybridTacticsMasterAgent"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.sample_query = "Test query"
        self.sample_context = {"team": "India"}
    
    async def test_analyze_with_very_large_context(self):
        """Test analysis with very large context"""
        agent = HybridTacticsMasterAgent()
        
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
        
        # Mock methods
        agent._get_cricket_data = AsyncMock(return_value={})
        agent._intelligent_fallback = Mock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        result = await agent.analyze(self.sample_query, large_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
    
    async def test_analyze_with_unicode_context(self):
        """Test analysis with unicode context"""
        agent = HybridTacticsMasterAgent()
        
        unicode_context = {
            "team": "India 印度",
            "players": ["Virat Kohli 维拉特·科利", "Rohit Sharma 罗希特·夏尔马"],
            "venue": "Narendra Modi Stadium 纳伦德拉·莫迪体育场"
        }
        
        # Mock methods
        agent._get_cricket_data = AsyncMock(return_value={})
        agent._intelligent_fallback = Mock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        result = await agent.analyze(self.sample_query, unicode_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
    
    async def test_analyze_with_special_characters_context(self):
        """Test analysis with special characters context"""
        agent = HybridTacticsMasterAgent()
        
        special_context = {
            "team": "India!@#$%^&*()",
            "players": ["Virat Kohli!@#", "Rohit Sharma$%^"],
            "venue": "Narendra Modi Stadium!@#$%^&*()"
        }
        
        # Mock methods
        agent._get_cricket_data = AsyncMock(return_value={})
        agent._intelligent_fallback = Mock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        result = await agent.analyze(self.sample_query, special_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
    
    async def test_analyze_with_nested_context(self):
        """Test analysis with deeply nested context"""
        agent = HybridTacticsMasterAgent()
        
        nested_context = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {
                            "level5": {
                                "level6": {
                                    "level7": {
                                        "level8": {
                                            "level9": {
                                                "level10": {
                                                    "value": "deep"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        # Mock methods
        agent._get_cricket_data = AsyncMock(return_value={})
        agent._intelligent_fallback = Mock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        result = await agent.analyze(self.sample_query, nested_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
    
    async def test_analyze_with_mixed_data_types_context(self):
        """Test analysis with mixed data types in context"""
        agent = HybridTacticsMasterAgent()
        
        mixed_context = {
            "string": "India",
            "integer": 123,
            "float": 45.67,
            "boolean": True,
            "list": ["item1", "item2", "item3"],
            "dict": {"key": "value"},
            "none": None
        }
        
        # Mock methods
        agent._get_cricket_data = AsyncMock(return_value={})
        agent._intelligent_fallback = Mock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        result = await agent.analyze(self.sample_query, mixed_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
    
    async def test_analyze_with_circular_reference_context(self):
        """Test analysis with circular reference in context"""
        agent = HybridTacticsMasterAgent()
        
        # Create circular reference
        circular_context = {"key": "value"}
        circular_context["self"] = circular_context
        
        # Mock methods
        agent._get_cricket_data = AsyncMock(return_value={})
        agent._intelligent_fallback = Mock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        result = await agent.analyze(self.sample_query, circular_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
    
    async def test_analyze_with_large_cricket_data(self):
        """Test analysis with large cricket data"""
        agent = HybridTacticsMasterAgent()
        
        large_cricket_data = {
            "matches": [{"name": f"Match {i}", "status": "Live"} for i in range(1000)],
            "players": [{"name": f"Player {i}", "stats": {"average": i}} for i in range(1000)]
        }
        
        # Mock methods
        agent._get_cricket_data = AsyncMock(return_value=large_cricket_data)
        agent._intelligent_fallback = Mock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        result = await agent.analyze(self.sample_query, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)
    
    async def test_analyze_with_malformed_cricket_data(self):
        """Test analysis with malformed cricket data"""
        agent = HybridTacticsMasterAgent()
        
        malformed_cricket_data = {
            "matches": "not_a_list",
            "players": None,
            "invalid_field": "value"
        }
        
        # Mock methods
        agent._get_cricket_data = AsyncMock(return_value=malformed_cricket_data)
        agent._intelligent_fallback = Mock(return_value={
            "response": "Test response",
            "analysis": {},
            "sources": []
        })
        
        result = await agent.analyze(self.sample_query, self.sample_context)
        
        self.assertIn("response", result)
        self.assertIn("analysis", result)
        self.assertIn("sources", result)

if __name__ == '__main__':
    unittest.main()
