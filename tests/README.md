# Comprehensive Test Suite for Tactics Master System

This directory contains a comprehensive test suite for the Tactics Master cricket analysis system, covering all components from individual tools to end-to-end integration tests.

## 📁 Test Structure

### Core Component Tests
- **`test_comprehensive_agent.py`** - Tests for the TacticsMasterAgent class including initialization, prompt creation, agent creation, and analysis methods
- **`test_comprehensive_cricket_api_tools.py`** - Tests for all cricket API tools (get_player_stats, get_team_squad, get_matchup_data, get_venue_stats) including error handling and mock data scenarios
- **`test_comprehensive_tactical_tools.py`** - Tests for all tactical analysis tools (analyze_weaknesses, find_best_matchup, generate_bowling_plan, generate_fielding_plan) with various data scenarios

### Backend and Integration Tests
- **`test_comprehensive_backend_api.py`** - Tests for FastAPI backend endpoints including /analyze, /health, and error handling scenarios
- **`test_comprehensive_hybrid_agent.py`** - Tests for HybridTacticsMasterAgent including API integration, fallback mechanisms, and async analysis methods
- **`test_comprehensive_integration.py`** - Integration tests that test the complete workflow from API calls to response generation

### Error Handling and Performance Tests
- **`test_comprehensive_error_handling.py`** - Comprehensive error handling tests for all components including network failures, invalid data, and edge cases
- **`test_comprehensive_performance.py`** - Performance tests to ensure the system can handle concurrent requests and large data sets

### Test Utilities
- **`test_runner.py`** - Comprehensive test runner that executes all tests and provides detailed reporting
- **`README.md`** - This documentation file

## 🚀 Running the Tests

### Run All Tests
```bash
# Run the comprehensive test suite
python test_runner.py

# Run individual test modules
python -m unittest test_comprehensive_agent.py
python -m unittest test_comprehensive_cricket_api_tools.py
python -m unittest test_comprehensive_tactical_tools.py
python -m unittest test_comprehensive_backend_api.py
python -m unittest test_comprehensive_hybrid_agent.py
python -m unittest test_comprehensive_integration.py
python -m unittest test_comprehensive_error_handling.py
python -m unittest test_comprehensive_performance.py
```

### Run with Coverage
```bash
# Install coverage if not already installed
pip install coverage

# Run tests with coverage
coverage run test_runner.py
coverage report
coverage html
```

### Run Specific Test Categories
```bash
# Run only unit tests
python -m unittest test_comprehensive_agent.py test_comprehensive_cricket_api_tools.py test_comprehensive_tactical_tools.py

# Run only integration tests
python -m unittest test_comprehensive_integration.py

# Run only error handling tests
python -m unittest test_comprehensive_error_handling.py

# Run only performance tests
python -m unittest test_comprehensive_performance.py
```

## 📊 Test Coverage

The test suite provides comprehensive coverage of:

### Core Functionality
- ✅ Agent initialization and configuration
- ✅ Prompt creation and management
- ✅ Tool integration and execution
- ✅ Analysis workflow and response generation

### API Tools
- ✅ Cricket data retrieval (player stats, team squads, matchups, venue stats)
- ✅ Real API integration with fallback mechanisms
- ✅ Data validation and error handling
- ✅ Mock data scenarios for development

### Tactical Analysis
- ✅ Weakness analysis and identification
- ✅ Matchup analysis and recommendations
- ✅ Bowling plan generation
- ✅ Fielding plan creation
- ✅ Strategic recommendations

### Backend Services
- ✅ FastAPI endpoint functionality
- ✅ Request/response validation
- ✅ Error handling and status codes
- ✅ CORS and middleware configuration

### Integration Scenarios
- ✅ End-to-end workflow testing
- ✅ Data flow validation
- ✅ Component interaction testing
- ✅ Real-world scenario simulation

### Error Handling
- ✅ Network failure scenarios
- ✅ Invalid data handling
- ✅ Edge case management
- ✅ Graceful degradation

### Performance
- ✅ Concurrent request handling
- ✅ Large data set processing
- ✅ Memory usage optimization
- ✅ Response time benchmarks

## 🧪 Test Categories

### Unit Tests
- **Agent Tests**: Test individual agent methods and functionality
- **Tool Tests**: Test individual cricket API and tactical analysis tools
- **Backend Tests**: Test individual FastAPI endpoints and functionality

### Integration Tests
- **Workflow Tests**: Test complete analysis workflows
- **Data Flow Tests**: Test data flow between components
- **API Integration Tests**: Test real API integrations

### Error Handling Tests
- **Network Error Tests**: Test network failure scenarios
- **Data Validation Tests**: Test invalid data handling
- **Edge Case Tests**: Test boundary conditions and edge cases

### Performance Tests
- **Concurrent Tests**: Test concurrent request handling
- **Load Tests**: Test system under load
- **Memory Tests**: Test memory usage and optimization
- **Benchmark Tests**: Test performance benchmarks

## 📈 Test Metrics

The test suite tracks the following metrics:

### Coverage Metrics
- **Line Coverage**: Percentage of code lines executed during tests
- **Branch Coverage**: Percentage of code branches tested
- **Function Coverage**: Percentage of functions tested

### Performance Metrics
- **Response Time**: Time taken for individual operations
- **Throughput**: Number of operations per second
- **Memory Usage**: Memory consumption during operations
- **Concurrent Performance**: Performance under concurrent load

### Quality Metrics
- **Test Success Rate**: Percentage of tests passing
- **Error Detection Rate**: Ability to detect and handle errors
- **Edge Case Coverage**: Coverage of edge cases and boundary conditions

## 🔧 Test Configuration

### Environment Setup
```bash
# Install required dependencies
pip install -r requirements.txt

# Set up environment variables
export GEMINI_API_KEY="your_gemini_api_key"
export CRICKET_API_KEY="your_cricket_api_key"
export CRICAPI_KEY="your_cricapi_key"
```

### Test Data
- **Mock Data**: Comprehensive mock data for development and testing
- **Real Data**: Integration with real cricket APIs when available
- **Test Scenarios**: Realistic test scenarios covering various use cases

## 📝 Test Reports

The test suite generates comprehensive reports including:

### Test Results Report
- Total tests run
- Pass/fail statistics
- Error details and stack traces
- Execution time metrics

### Coverage Report
- Line-by-line coverage analysis
- Coverage percentage by module
- Missing coverage identification
- Coverage trends over time

### Performance Report
- Response time benchmarks
- Throughput measurements
- Memory usage analysis
- Performance regression detection

## 🚨 Troubleshooting

### Common Issues

#### Import Errors
```bash
# Ensure all dependencies are installed
pip install -r requirements.txt

# Check Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

#### API Key Issues
```bash
# Set required environment variables
export GEMINI_API_KEY="your_key"
export CRICKET_API_KEY="your_key"
```

#### Test Failures
```bash
# Run tests with verbose output
python -m unittest -v test_comprehensive_agent.py

# Check for specific error messages
python -m unittest test_comprehensive_agent.py 2>&1 | grep -i error
```

### Debug Mode
```bash
# Run tests with debug output
python -m unittest -v --debug test_comprehensive_agent.py

# Run specific test method
python -m unittest test_comprehensive_agent.TestTacticsMasterAgentComprehensive.test_agent_initialization_success
```

## 📚 Best Practices

### Writing Tests
1. **Test Naming**: Use descriptive test method names
2. **Test Isolation**: Each test should be independent
3. **Mock External Dependencies**: Use mocks for external APIs
4. **Test Edge Cases**: Include boundary conditions and edge cases
5. **Assertions**: Use specific assertions with clear error messages

### Test Maintenance
1. **Regular Updates**: Keep tests updated with code changes
2. **Performance Monitoring**: Monitor test execution time
3. **Coverage Tracking**: Maintain high test coverage
4. **Documentation**: Keep test documentation current

### Continuous Integration
1. **Automated Testing**: Run tests on every code change
2. **Performance Regression**: Detect performance regressions early
3. **Coverage Gates**: Enforce minimum coverage requirements
4. **Quality Metrics**: Track quality metrics over time

## 🎯 Future Enhancements

### Planned Improvements
- **Visual Test Reports**: HTML-based test reports with charts
- **Performance Profiling**: Detailed performance profiling and analysis
- **Test Data Management**: Centralized test data management
- **Automated Test Generation**: AI-assisted test case generation

### Advanced Features
- **Load Testing**: Comprehensive load testing scenarios
- **Security Testing**: Security vulnerability testing
- **Accessibility Testing**: Accessibility compliance testing
- **Cross-Platform Testing**: Testing across different platforms

## 📞 Support

For questions or issues with the test suite:

1. **Check Documentation**: Review this README and inline comments
2. **Run Debug Mode**: Use verbose output to identify issues
3. **Check Dependencies**: Ensure all required packages are installed
4. **Environment Setup**: Verify environment variables are set correctly

## 📄 License

This test suite is part of the Tactics Master project and follows the same license terms.
