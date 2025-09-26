"""
Comprehensive Unit Tests for Hybrid Tactics Master Agent

This module contains detailed unit tests for the HybridTacticsMasterAgent class,
covering all methods, error handling, and edge cases.
"""

import pytest
import json
import asyncio
from unittest.mock import Mock, patch, MagicMock, AsyncMock
from typing import Dict, Any

from backend.hybrid_agent import HybridTacticsMasterAgent


class TestHybridTacticsMasterAgentInitialization:
    """Test hybrid agent initialization scenarios"""
    
    def test_agent_initialization_with_gemini_key(self, mock_environment):
        """Test agent initialization with Gemini API key"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_gemini_key'}):
            with patch('backend.hybrid_agent.ChatGoogleGenerativeAI') as mock_gemini:
                mock_llm = Mock()
                mock_gemini.return_value = mock_llm
                
                agent = HybridTacticsMasterAgent()
                
                assert agent.gemini_api_key == 'test_gemini_key'
                assert agent.llm == mock_llm
                mock_gemini.assert_called_once()
    
    def test_agent_initialization_without_api_keys(self):
        """Test agent initialization without API keys"""
        with patch.dict('os.environ', {}, clear=True):
            agent = HybridTacticsMasterAgent()
            
            assert agent.cricket_api_key is None
            assert agent.gemini_api_key is None
            assert agent.llm is None
    
    def test_agent_initialization_with_cricket_key_only(self):
        """Test agent initialization with only cricket API key"""
        with patch.dict('os.environ', {'CRICKET_API_KEY': 'test_cricket_key'}):
            agent = HybridTacticsMasterAgent()
            
            assert agent.cricket_api_key == 'test_cricket_key'
            assert agent.gemini_api_key is None
            assert agent.llm is None
    
    def test_agent_initialization_gemini_initialization_failure(self):
        """Test agent initialization when Gemini initialization fails"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_gemini_key'}):
            with patch('backend.hybrid_agent.ChatGoogleGenerativeAI', side_effect=Exception("Gemini init failed")):
                agent = HybridTacticsMasterAgent()
                
                assert agent.gemini_api_key == 'test_gemini_key'
                assert agent.llm is None
    
    def test_agent_initialization_with_both_keys(self):
        """Test agent initialization with both API keys"""
        with patch.dict('os.environ', {
            'CRICKET_API_KEY': 'test_cricket_key',
            'GEMINI_API_KEY': 'test_gemini_key'
        }):
            with patch('backend.hybrid_agent.ChatGoogleGenerativeAI') as mock_gemini:
                mock_llm = Mock()
                mock_gemini.return_value = mock_llm
                
                agent = HybridTacticsMasterAgent()
                
                assert agent.cricket_api_key == 'test_cricket_key'
                assert agent.gemini_api_key == 'test_gemini_key'
                assert agent.llm == mock_llm


class TestHybridTacticsMasterAgentAnalyze:
    """Test hybrid agent analyze functionality"""
    
    @pytest.mark.asyncio
    async def test_analyze_success_with_ai(self, mock_environment):
        """Test successful analysis with AI"""
        with patch.dict('os.environ', {
            'CRICKET_API_KEY': 'test_cricket_key',
            'GEMINI_API_KEY': 'test_gemini_key'
        }):
            with patch('backend.hybrid_agent.ChatGoogleGenerativeAI') as mock_gemini:
                mock_llm = Mock()
                mock_llm.invoke = Mock(return_value=Mock(content="AI analysis response"))
                mock_gemini.return_value = mock_llm
                
                agent = HybridTacticsMasterAgent()
                
                with patch.object(agent, '_get_cricket_data', return_value={"matches": []}):
                    result = await agent.analyze("Test query", {"team": "India"})
                    
                    assert result["response"] == "AI analysis response"
                    assert result["analysis"]["ai_generated"] is True
                    assert result["sources"] == ["CricAPI", "Gemini AI Analysis"]
    
    @pytest.mark.asyncio
    async def test_analyze_success_with_fallback(self, mock_environment):
        """Test successful analysis with fallback"""
        with patch.dict('os.environ', {'CRICKET_API_KEY': 'test_cricket_key'}):
            agent = HybridTacticsMasterAgent()
            
            with patch.object(agent, '_get_cricket_data', return_value={"matches": []}):
                result = await agent.analyze("Test query", {"team": "India"})
                
                assert "response" in result
                assert result["analysis"]["data_driven"] is True
                assert "CricAPI Real Data" in result["sources"]
    
    @pytest.mark.asyncio
    async def test_analyze_with_empty_query(self, mock_environment):
        """Test analysis with empty query"""
        agent = HybridTacticsMasterAgent()
        
        result = await agent.analyze("", {})
        
        assert result["response"] == "Please provide a valid query for analysis."
        assert result["analysis"] == {}
        assert result["sources"] == []
    
    @pytest.mark.asyncio
    async def test_analyze_with_whitespace_query(self, mock_environment):
        """Test analysis with whitespace-only query"""
        agent = HybridTacticsMasterAgent()
        
        result = await agent.analyze("   ", {})
        
        assert result["response"] == "Please provide a valid query for analysis."
        assert result["analysis"] == {}
        assert result["sources"] == []
    
    @pytest.mark.asyncio
    async def test_analyze_with_none_query(self, mock_environment):
        """Test analysis with None query"""
        agent = HybridTacticsMasterAgent()
        
        result = await agent.analyze(None, {})
        
        assert result["response"] == "Please provide a valid query for analysis."
        assert result["analysis"] == {}
        assert result["sources"] == []
    
    @pytest.mark.asyncio
    async def test_analyze_with_exception(self, mock_environment):
        """Test analysis with exception"""
        agent = HybridTacticsMasterAgent()
        
        with patch.object(agent, '_get_cricket_data', side_effect=Exception("Test error")):
            result = await agent.analyze("Test query", {})
            
            assert "I encountered an error" in result["response"]
            assert result["analysis"] == {}
            assert result["sources"] == []
    
    @pytest.mark.asyncio
    async def test_analyze_with_special_characters(self, mock_environment):
        """Test analysis with special characters in query"""
        agent = HybridTacticsMasterAgent()
        
        special_query = "Test query!@#$%^&*()"
        
        with patch.object(agent, '_get_cricket_data', return_value={"matches": []}):
            result = await agent.analyze(special_query, {})
            
            assert "response" in result
            assert result["analysis"]["data_driven"] is True
    
    @pytest.mark.asyncio
    async def test_analyze_with_unicode_characters(self, mock_environment):
        """Test analysis with unicode characters in query"""
        agent = HybridTacticsMasterAgent()
        
        unicode_query = "Test query 测试查询"
        
        with patch.object(agent, '_get_cricket_data', return_value={"matches": []}):
            result = await agent.analyze(unicode_query, {})
            
            assert "response" in result
            assert result["analysis"]["data_driven"] is True
    
    @pytest.mark.asyncio
    async def test_analyze_with_complex_context(self, mock_environment):
        """Test analysis with complex context"""
        agent = HybridTacticsMasterAgent()
        
        complex_context = {
            "team": "India",
            "players": ["Virat Kohli", "Rohit Sharma"],
            "match_info": {
                "venue": "Narendra Modi Stadium",
                "conditions": {"pitch": "batting_friendly", "weather": "clear"}
            },
            "nested": {
                "deep": {
                    "value": "test"
                }
            }
        }
        
        with patch.object(agent, '_get_cricket_data', return_value={"matches": []}):
            result = await agent.analyze("Test query", complex_context)
            
            assert "response" in result
            assert result["analysis"]["data_driven"] is True


class TestHybridTacticsMasterAgentGetCricketData:
    """Test hybrid agent cricket data retrieval"""
    
    @pytest.mark.asyncio
    async def test_get_cricket_data_success(self, mock_environment):
        """Test successful cricket data retrieval"""
        with patch.dict('os.environ', {'CRICKET_API_KEY': 'test_cricket_key'}):
            agent = HybridTacticsMasterAgent()
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {
                    "data": [
                        {"name": "Match 1", "status": "Live"},
                        {"name": "Match 2", "status": "Completed"}
                    ]
                }
                mock_get.return_value = mock_response
                
                result = await agent._get_cricket_data("Test query", {"team": "India"})
                
                assert "matches" in result
                assert "query" in result
                assert "context" in result
                assert len(result["matches"]) == 2
    
    @pytest.mark.asyncio
    async def test_get_cricket_data_with_player_mention(self, mock_environment):
        """Test cricket data retrieval with player mention"""
        with patch.dict('os.environ', {'CRICKET_API_KEY': 'test_cricket_key'}):
            agent = HybridTacticsMasterAgent()
            
            with patch('requests.get') as mock_get:
                # Mock matches response
                matches_response = Mock()
                matches_response.status_code = 200
                matches_response.json.return_value = {"data": []}
                
                # Mock players response
                players_response = Mock()
                players_response.status_code = 200
                players_response.json.return_value = {"data": []}
                
                mock_get.side_effect = [matches_response, players_response]
                
                result = await agent._get_cricket_data("Analyze Virat Kohli's performance", {})
                
                assert "matches" in result
                assert "players" in result
                assert mock_get.call_count == 2
    
    @pytest.mark.asyncio
    async def test_get_cricket_data_without_api_key(self, mock_environment):
        """Test cricket data retrieval without API key"""
        agent = HybridTacticsMasterAgent()
        
        result = await agent._get_cricket_data("Test query", {})
        
        assert result == {}
    
    @pytest.mark.asyncio
    async def test_get_cricket_data_with_api_error(self, mock_environment):
        """Test cricket data retrieval with API error"""
        with patch.dict('os.environ', {'CRICKET_API_KEY': 'test_cricket_key'}):
            agent = HybridTacticsMasterAgent()
            
            with patch('requests.get', side_effect=Exception("API error")):
                result = await agent._get_cricket_data("Test query", {})
                
                assert result == {}
    
    @pytest.mark.asyncio
    async def test_get_cricket_data_with_non_200_response(self, mock_environment):
        """Test cricket data retrieval with non-200 response"""
        with patch.dict('os.environ', {'CRICKET_API_KEY': 'test_cricket_key'}):
            agent = HybridTacticsMasterAgent()
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 404
                mock_get.return_value = mock_response
                
                result = await agent._get_cricket_data("Test query", {})
                
                assert result == {}


class TestHybridTacticsMasterAgentAIAnalyze:
    """Test hybrid agent AI analysis functionality"""
    
    @pytest.mark.asyncio
    async def test_ai_analyze_success(self, mock_environment):
        """Test successful AI analysis"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_gemini_key'}):
            with patch('backend.hybrid_agent.ChatGoogleGenerativeAI') as mock_gemini:
                mock_llm = Mock()
                mock_llm.invoke = Mock(return_value=Mock(content="AI analysis response"))
                mock_gemini.return_value = mock_llm
                
                agent = HybridTacticsMasterAgent()
                
                cricket_data = {"matches": [{"name": "Match 1"}]}
                context = {"team": "India"}
                
                result = await agent._ai_analyze("Test query", cricket_data, context)
                
                assert result["response"] == "AI analysis response"
                assert result["analysis"]["ai_generated"] is True
                assert result["analysis"]["data_sources"] == ["CricAPI", "Gemini AI"]
                assert result["sources"] == ["CricAPI", "Gemini AI Analysis"]
    
    @pytest.mark.asyncio
    async def test_ai_analyze_with_exception(self, mock_environment):
        """Test AI analysis with exception"""
        with patch.dict('os.environ', {'GEMINI_API_KEY': 'test_gemini_key'}):
            with patch('backend.hybrid_agent.ChatGoogleGenerativeAI') as mock_gemini:
                mock_llm = Mock()
                mock_llm.invoke = Mock(side_effect=Exception("AI error"))
                mock_gemini.return_value = mock_llm
                
                agent = HybridTacticsMasterAgent()
                
                cricket_data = {"matches": []}
                context = {"team": "India"}
                
                with patch.object(agent, '_intelligent_fallback', return_value={
                    "response": "Fallback response",
                    "analysis": {},
                    "sources": []
                }) as mock_fallback:
                    result = await agent._ai_analyze("Test query", cricket_data, context)
                    
                    assert result["response"] == "Fallback response"
                    mock_fallback.assert_called_once_with("Test query", cricket_data, context)
    
    @pytest.mark.asyncio
    async def test_ai_analyze_without_llm(self, mock_environment):
        """Test AI analysis without LLM"""
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": []}
        context = {"team": "India"}
        
        with patch.object(agent, '_intelligent_fallback', return_value={
            "response": "Fallback response",
            "analysis": {},
            "sources": []
        }) as mock_fallback:
            result = await agent._ai_analyze("Test query", cricket_data, context)
            
            assert result["response"] == "Fallback response"
            mock_fallback.assert_called_once_with("Test query", cricket_data, context)


class TestHybridTacticsMasterAgentIntelligentFallback:
    """Test hybrid agent intelligent fallback functionality"""
    
    def test_intelligent_fallback_batting_query(self, mock_environment):
        """Test intelligent fallback with batting query"""
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": [{"name": "Match 1", "status": "Live"}]}
        context = {"team": "India"}
        
        result = agent._intelligent_fallback("Analyze batting weaknesses", cricket_data, context)
        
        assert "batting" in result["response"].lower()
        assert result["analysis"]["data_driven"] is True
        assert result["analysis"]["real_cricket_data"] is True
        assert "CricAPI Real Data" in result["sources"]
    
    def test_intelligent_fallback_bowling_query(self, mock_environment):
        """Test intelligent fallback with bowling query"""
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": [{"name": "Match 1", "status": "Live"}]}
        context = {"team": "India"}
        
        result = agent._intelligent_fallback("Analyze bowling strategy", cricket_data, context)
        
        assert "bowling" in result["response"].lower()
        assert result["analysis"]["data_driven"] is True
        assert result["analysis"]["real_cricket_data"] is True
        assert "CricAPI Real Data" in result["sources"]
    
    def test_intelligent_fallback_general_query(self, mock_environment):
        """Test intelligent fallback with general query"""
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": [{"name": "Match 1", "status": "Live"}]}
        context = {"team": "India"}
        
        result = agent._intelligent_fallback("General cricket analysis", cricket_data, context)
        
        assert "cricket" in result["response"].lower()
        assert result["analysis"]["data_driven"] is True
        assert result["analysis"]["real_cricket_data"] is True
        assert "CricAPI Real Data" in result["sources"]
    
    def test_intelligent_fallback_without_cricket_data(self, mock_environment):
        """Test intelligent fallback without cricket data"""
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {}
        context = {"team": "India"}
        
        result = agent._intelligent_fallback("Test query", cricket_data, context)
        
        assert "response" in result
        assert result["analysis"]["data_driven"] is True
        assert result["analysis"]["real_cricket_data"] is False
        assert "Cricket Analytics Database" in result["sources"]
    
    def test_intelligent_fallback_with_special_characters(self, mock_environment):
        """Test intelligent fallback with special characters"""
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": []}
        context = {"team": "India!@#$%^&*()"}
        
        result = agent._intelligent_fallback("Test query!@#$%^&*()", cricket_data, context)
        
        assert "response" in result
        assert result["analysis"]["data_driven"] is True
    
    def test_intelligent_fallback_with_unicode_characters(self, mock_environment):
        """Test intelligent fallback with unicode characters"""
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": []}
        context = {"team": "India 印度"}
        
        result = agent._intelligent_fallback("Test query 测试查询", cricket_data, context)
        
        assert "response" in result
        assert result["analysis"]["data_driven"] is True
    
    def test_intelligent_fallback_with_complex_context(self, mock_environment):
        """Test intelligent fallback with complex context"""
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": []}
        complex_context = {
            "team": "India",
            "players": ["Virat Kohli", "Rohit Sharma"],
            "match_info": {
                "venue": "Narendra Modi Stadium",
                "conditions": {"pitch": "batting_friendly", "weather": "clear"}
            },
            "nested": {
                "deep": {
                    "value": "test"
                }
            }
        }
        
        result = agent._intelligent_fallback("Test query", cricket_data, complex_context)
        
        assert "response" in result
        assert result["analysis"]["data_driven"] is True


class TestHybridTacticsMasterAgentPerformance:
    """Test hybrid agent performance scenarios"""
    
    @pytest.mark.asyncio
    async def test_analyze_performance(self, mock_environment):
        """Test analyze method performance"""
        import time
        
        agent = HybridTacticsMasterAgent()
        
        with patch.object(agent, '_get_cricket_data', return_value={"matches": []}):
            start_time = time.time()
            
            for _ in range(10):
                result = await agent.analyze("Test query", {"team": "India"})
                assert "response" in result
            
            end_time = time.time()
            
            # Should complete 10 calls in less than 5 seconds
            assert (end_time - start_time) < 5.0
    
    @pytest.mark.asyncio
    async def test_get_cricket_data_performance(self, mock_environment):
        """Test get_cricket_data method performance"""
        import time
        
        with patch.dict('os.environ', {'CRICKET_API_KEY': 'test_cricket_key'}):
            agent = HybridTacticsMasterAgent()
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"data": []}
                mock_get.return_value = mock_response
                
                start_time = time.time()
                
                for _ in range(10):
                    result = await agent._get_cricket_data("Test query", {})
                    assert isinstance(result, dict)
                
                end_time = time.time()
                
                # Should complete 10 calls in less than 3 seconds
                assert (end_time - start_time) < 3.0
    
    def test_intelligent_fallback_performance(self, mock_environment):
        """Test intelligent_fallback method performance"""
        import time
        
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": []}
        context = {"team": "India"}
        
        start_time = time.time()
        
        for _ in range(100):
            result = agent._intelligent_fallback("Test query", cricket_data, context)
            assert "response" in result
        
        end_time = time.time()
        
        # Should complete 100 calls in less than 2 seconds
        assert (end_time - start_time) < 2.0


class TestHybridTacticsMasterAgentMemoryUsage:
    """Test hybrid agent memory usage scenarios"""
    
    @pytest.mark.asyncio
    async def test_analyze_memory_usage(self, mock_environment):
        """Test analyze method memory usage"""
        import sys
        
        agent = HybridTacticsMasterAgent()
        
        with patch.object(agent, '_get_cricket_data', return_value={"matches": []}):
            result = await agent.analyze("Test query", {"team": "India"})
            
            # Result should not be excessively large
            assert sys.getsizeof(result) < 50000  # Less than 50KB
    
    @pytest.mark.asyncio
    async def test_get_cricket_data_memory_usage(self, mock_environment):
        """Test get_cricket_data method memory usage"""
        import sys
        
        with patch.dict('os.environ', {'CRICKET_API_KEY': 'test_cricket_key'}):
            agent = HybridTacticsMasterAgent()
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"data": []}
                mock_get.return_value = mock_response
                
                result = await agent._get_cricket_data("Test query", {})
                
                # Result should not be excessively large
                assert sys.getsizeof(result) < 10000  # Less than 10KB
    
    def test_intelligent_fallback_memory_usage(self, mock_environment):
        """Test intelligent_fallback method memory usage"""
        import sys
        
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": []}
        context = {"team": "India"}
        
        result = agent._intelligent_fallback("Test query", cricket_data, context)
        
        # Result should not be excessively large
        assert sys.getsizeof(result) < 20000  # Less than 20KB


class TestHybridTacticsMasterAgentDataValidation:
    """Test hybrid agent data validation"""
    
    @pytest.mark.asyncio
    async def test_analyze_data_structure(self, mock_environment):
        """Test analyze method data structure validation"""
        agent = HybridTacticsMasterAgent()
        
        with patch.object(agent, '_get_cricket_data', return_value={"matches": []}):
            result = await agent.analyze("Test query", {"team": "India"})
            
            # Validate required fields
            assert "response" in result
            assert "analysis" in result
            assert "sources" in result
            
            # Validate data types
            assert isinstance(result["response"], str)
            assert isinstance(result["analysis"], dict)
            assert isinstance(result["sources"], list)
    
    @pytest.mark.asyncio
    async def test_get_cricket_data_data_structure(self, mock_environment):
        """Test get_cricket_data method data structure validation"""
        with patch.dict('os.environ', {'CRICKET_API_KEY': 'test_cricket_key'}):
            agent = HybridTacticsMasterAgent()
            
            with patch('requests.get') as mock_get:
                mock_response = Mock()
                mock_response.status_code = 200
                mock_response.json.return_value = {"data": []}
                mock_get.return_value = mock_response
                
                result = await agent._get_cricket_data("Test query", {"team": "India"})
                
                # Validate required fields
                assert "matches" in result
                assert "query" in result
                assert "context" in result
                
                # Validate data types
                assert isinstance(result["matches"], list)
                assert isinstance(result["query"], str)
                assert isinstance(result["context"], dict)
    
    def test_intelligent_fallback_data_structure(self, mock_environment):
        """Test intelligent_fallback method data structure validation"""
        agent = HybridTacticsMasterAgent()
        
        cricket_data = {"matches": []}
        context = {"team": "India"}
        
        result = agent._intelligent_fallback("Test query", cricket_data, context)
        
        # Validate required fields
        assert "response" in result
        assert "analysis" in result
        assert "sources" in result
        
        # Validate data types
        assert isinstance(result["response"], str)
        assert isinstance(result["analysis"], dict)
        assert isinstance(result["sources"], list)
        
        # Validate analysis structure
        assert "data_driven" in result["analysis"]
        assert "real_cricket_data" in result["analysis"]
        assert "match_count" in result["analysis"]
        assert "confidence" in result["analysis"]
