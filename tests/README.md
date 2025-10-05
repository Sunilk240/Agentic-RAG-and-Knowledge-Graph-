# Comprehensive Testing Suite for Graph-Enhanced Agentic RAG

This directory contains a comprehensive testing suite for the Graph-Enhanced Agentic RAG system, implementing task 10 from the specification.

## Overview

The testing suite covers all aspects of the system with three main categories:

### 1. Unit Tests (Task 10.1)
**Requirements: 4.1, 4.2, 4.3, 4.4**

- **`test_coordinator_agent.py`** - Comprehensive tests for the Coordinator Agent
  - Query analysis and entity extraction
  - Strategy selection and orchestration
  - Agent communication and coordination
  - Error handling and edge cases
  - Performance metrics collection

- **`test_graph_navigator_agent.py`** - Tests for the Graph Navigator Agent
  - Entity fuzzy matching and disambiguation
  - Graph traversal algorithms and path finding
  - Cypher query generation and optimization
  - Subgraph extraction for context
  - Concurrent operations and error recovery

- **`test_vector_retrieval_agent.py`** - Tests for the Vector Retrieval Agent
  - Embedding generation and caching mechanisms
  - Semantic similarity search with various filters
  - Hybrid search combining semantic and keyword matching
  - Batch processing and concurrent operations
  - Performance optimization and error handling

- **`test_synthesis_agent.py`** - Tests for the Synthesis Agent
  - Multi-source result integration and deduplication
  - Response generation using Gemini API
  - Citation and source attribution
  - Context window management for LLM input
  - Quality validation and reasoning explanation

### 2. Integration Tests (Task 10.2)
**Requirements: 6.3, 6.4, 4.5**

- **`test_integration_workflows.py`** - End-to-end workflow tests
  - Complete query processing workflows (factual, relational, hybrid)
  - Data consistency between graph and vector stores
  - Agent communication and coordination
  - Error propagation and recovery mechanisms
  - Concurrent query processing
  - Workflow state management

- **`test_system_resilience.py`** - System resilience and fault tolerance
  - Database connection failures and recovery
  - Network timeouts and retry logic with exponential backoff
  - Resource exhaustion scenarios
  - Graceful degradation strategies
  - Circuit breaker patterns
  - Progressive timeout strategies

### 3. Performance and Load Tests (Task 10.3)
**Requirements: 2.4**

- **`test_performance_load.py`** - Performance and scalability tests
  - Concurrent query handling and throughput measurement
  - Large dataset processing performance
  - Memory usage and optimization
  - Sustained load performance testing
  - Burst load handling
  - Scalability bottleneck identification
  - Memory leak detection

## Test Infrastructure

### Test Runner
- **`run_comprehensive_tests.py`** - Comprehensive test execution framework
  - Runs all test suites with detailed reporting
  - Generates JSON and HTML test reports
  - Provides performance metrics and success rates
  - Supports individual suite execution
  - Includes timeout handling and error recovery

### Performance Monitoring
- **`PerformanceMetrics`** class for collecting detailed performance data
- Memory usage tracking with `psutil`
- CPU usage monitoring
- Query timing and throughput analysis
- Statistical analysis (mean, median, percentiles)

## Key Testing Features

### Comprehensive Coverage
- **Unit Tests**: 200+ test cases covering all agent functionality
- **Integration Tests**: 50+ test scenarios for end-to-end workflows
- **Performance Tests**: 30+ load and scalability test cases
- **Error Handling**: Extensive edge case and failure scenario testing

### Advanced Testing Techniques
- **Mock-based Testing**: Isolated unit testing with comprehensive mocking
- **Concurrent Testing**: Multi-threaded and async operation testing
- **Load Testing**: Sustained and burst load simulation
- **Memory Profiling**: Memory leak detection and optimization validation
- **Fault Injection**: Simulated failures for resilience testing

### Quality Assurance
- **Automated Assertions**: Performance thresholds and quality gates
- **Regression Detection**: Performance baseline comparisons
- **Resource Monitoring**: Memory and CPU usage validation
- **Error Recovery**: Graceful degradation and fallback testing

## Usage

### Run All Tests
```bash
python tests/run_comprehensive_tests.py --verbose --report
```

### Run Specific Test Suite
```bash
# Unit tests only
python tests/run_comprehensive_tests.py --suite unit --verbose

# Integration tests only
python tests/run_comprehensive_tests.py --suite integration --verbose

# Performance tests only
python tests/run_comprehensive_tests.py --suite performance --verbose
```

### Run Individual Test Files
```bash
# Run specific agent tests
python -m pytest tests/test_coordinator_agent.py -v
python -m pytest tests/test_graph_navigator_agent.py -v
python -m pytest tests/test_vector_retrieval_agent.py -v
python -m pytest tests/test_synthesis_agent.py -v

# Run integration tests
python -m pytest tests/test_integration_workflows.py -v
python -m pytest tests/test_system_resilience.py -v

# Run performance tests
python -m pytest tests/test_performance_load.py -v
```

## Test Reports

The test runner generates comprehensive reports:

- **JSON Report**: Detailed test results with metrics (`test_report.json`)
- **HTML Report**: Visual test summary with charts (`test_report.html`)
- **Console Output**: Real-time test progress and summaries

## Performance Benchmarks

### Expected Performance Thresholds
- **Query Processing**: < 1 second average, < 2 seconds P95
- **Concurrent Throughput**: ≥ 10 queries per second
- **Memory Usage**: < 1GB for normal operations
- **Success Rate**: ≥ 90% for all test suites

### Scalability Targets
- **Dataset Size**: Support for 10,000+ documents
- **Concurrent Users**: Handle 50+ simultaneous queries
- **Graph Traversal**: Process 1,000+ entity graphs efficiently
- **Memory Efficiency**: < 100KB per document indexed

## Dependencies

### Required Packages
```
pytest>=7.0.0
pytest-asyncio>=0.21.0
pytest-json-report>=1.5.0
psutil>=5.9.0
numpy>=1.21.0
```

### Optional Packages for Enhanced Testing
```
pytest-cov>=4.0.0          # Coverage reporting
pytest-benchmark>=4.0.0    # Performance benchmarking
pytest-xdist>=3.0.0        # Parallel test execution
pytest-html>=3.1.0         # HTML test reports
```

## Test Configuration

### Environment Variables
- `TEST_TIMEOUT`: Default test timeout (default: 300 seconds)
- `TEST_VERBOSE`: Enable verbose output (default: false)
- `TEST_PARALLEL`: Enable parallel test execution (default: false)

### Test Data
- Tests use temporary directories for isolation
- Mock data generators create realistic test scenarios
- Large datasets are generated programmatically for performance tests

## Continuous Integration

The test suite is designed for CI/CD integration:

- **Fast Feedback**: Unit tests complete in < 2 minutes
- **Comprehensive Coverage**: Integration tests in < 10 minutes
- **Performance Validation**: Load tests in < 15 minutes
- **Parallel Execution**: Support for distributed test execution
- **Failure Isolation**: Individual test failures don't block others

## Contributing

When adding new functionality:

1. **Add Unit Tests**: Cover all new methods and edge cases
2. **Update Integration Tests**: Test end-to-end workflows
3. **Consider Performance**: Add performance tests for critical paths
4. **Document Changes**: Update test documentation
5. **Validate Coverage**: Ensure comprehensive test coverage

## Troubleshooting

### Common Issues
- **Memory Errors**: Reduce dataset sizes in performance tests
- **Timeout Errors**: Increase timeout values for slow systems
- **Import Errors**: Ensure all dependencies are installed
- **Database Errors**: Check mock configurations and test isolation

### Debug Mode
```bash
# Run with maximum verbosity and debugging
python -m pytest tests/ -v -s --tb=long --log-cli-level=DEBUG
```

This comprehensive testing suite ensures the reliability, performance, and maintainability of the Graph-Enhanced Agentic RAG system across all operational scenarios.