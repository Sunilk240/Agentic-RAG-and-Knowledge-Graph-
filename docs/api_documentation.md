# Graph-Enhanced Agentic RAG API Documentation

## Overview

The Graph-Enhanced Agentic RAG API provides intelligent knowledge discovery through a sophisticated multi-agent architecture that combines graph-based knowledge representation with vector embeddings for comprehensive information retrieval.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Authentication](#authentication)
3. [Endpoints](#endpoints)
4. [Request/Response Formats](#requestresponse-formats)
5. [Error Handling](#error-handling)
6. [Rate Limiting](#rate-limiting)
7. [Examples](#examples)
8. [Best Practices](#best-practices)
9. [Testing](#testing)
10. [Troubleshooting](#troubleshooting)

## Quick Start

### 1. Check API Health

```bash
curl -X GET "http://localhost:8000/health"
```

### 2. Upload a Document

```bash
curl -X POST "http://localhost:8000/documents/upload" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Machine Learning Guide",
       "content": "Machine learning is a subset of AI...",
       "domain": "technical"
     }'
```

### 3. Ask a Question

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is machine learning?",
       "max_results": 10,
       "include_reasoning": true
     }'
```

## Authentication

Currently, the API does not require authentication. In production deployments, consider implementing:

- API key authentication
- OAuth 2.0 / JWT tokens
- Rate limiting per user/API key

## Endpoints

### Core Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and status |
| `/health` | GET | System health check |
| `/query` | POST | Process intelligent queries |
| `/documents/upload` | POST | Upload documents (JSON) |
| `/documents/upload-file` | POST | Upload document files |
| `/agents/status` | GET | Agent system status |
| `/system/status` | GET | Detailed system status |

### Testing Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/test/examples` | GET | API usage examples |
| `/test/validate` | POST | API validation tests |
| `/test/performance` | GET | Performance metrics |

### Documentation Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/docs` | GET | Swagger UI documentation |
| `/redoc` | GET | ReDoc documentation |
| `/openapi.json` | GET | OpenAPI schema |

## Request/Response Formats

### Query Request

```json
{
  "query": "What is machine learning?",
  "max_results": 10,
  "include_reasoning": true,
  "strategy": "hybrid"
}
```

**Fields:**
- `query` (required): The question or query text (1-1000 characters)
- `max_results` (optional): Maximum results to return (1-50, default: 10)
- `include_reasoning` (optional): Include reasoning path (default: true)
- `strategy` (optional): Force specific strategy ("vector_focused", "graph_focused", "hybrid")

### Query Response

```json
{
  "query_id": "123e4567-e89b-12d3-a456-426614174000",
  "response": "Machine learning is a subset of artificial intelligence...",
  "sources": [
    {
      "id": "doc_1",
      "title": "ML Introduction",
      "content_preview": "Machine learning algorithms...",
      "source_type": "document",
      "relevance_score": 0.92
    }
  ],
  "citations": [
    {
      "id": "1",
      "source": "ML Introduction",
      "citation_text": "[1] ML Introduction, p. 15",
      "relevance": 0.92
    }
  ],
  "reasoning_path": "Query Analysis → Strategy Selection → Information Retrieval → Response Synthesis",
  "confidence_score": 0.89,
  "processing_time": 1.23,
  "strategy_used": "hybrid",
  "entities_found": ["machine learning", "artificial intelligence"]
}
```

### Document Upload Request

```json
{
  "title": "Document Title",
  "content": "Document content text...",
  "source": "https://example.com/source",
  "domain": "technical",
  "metadata": {
    "author": "Author Name",
    "tags": ["tag1", "tag2"]
  }
}
```

**Fields:**
- `title` (required): Document title (1-200 characters)
- `content` (required): Document content text
- `source` (optional): Source URL or reference
- `domain` (optional): Knowledge domain (default: "general")
- `metadata` (optional): Additional metadata object

### Document Upload Response

```json
{
  "document_id": "doc_789abc12-def3-4567-8901-234567890abc",
  "status": "success",
  "message": "Document uploaded successfully",
  "entities_extracted": 25,
  "relationships_created": 18,
  "processing_time": 3.45
}
```

## Error Handling

All error responses follow a consistent format:

```json
{
  "error": "Error Type",
  "message": "Human-readable error message",
  "details": {
    "additional": "error details"
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "req_123456789"
}
```

### Common Error Codes

| Code | Error Type | Description |
|------|------------|-------------|
| 400 | Bad Request | Invalid request format |
| 404 | Not Found | Endpoint not found |
| 422 | Validation Error | Request validation failed |
| 429 | Rate Limit Exceeded | Too many requests |
| 500 | Internal Server Error | Unexpected server error |
| 503 | Service Unavailable | Service temporarily unavailable |

### Validation Errors

Validation errors include detailed field information:

```json
{
  "error": "Validation Error",
  "message": "Request validation failed",
  "details": {
    "validation_errors": [
      {
        "loc": ["body", "query"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ],
    "suggestions": [
      "Field 'query' is required but was not provided"
    ]
  }
}
```

## Rate Limiting

Current rate limits (subject to change):

- **Query endpoints**: 100 requests per minute
- **Document upload**: 50 requests per minute
- **Health/status endpoints**: No limit

Rate limit headers are included in responses:
- `X-RateLimit-Limit`: Request limit per window
- `X-RateLimit-Remaining`: Remaining requests in window
- `X-RateLimit-Reset`: Window reset time

## Examples

### Simple Factual Query

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is artificial intelligence?",
       "max_results": 5
     }'
```

### Relationship Query

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "How are neural networks related to deep learning?",
       "strategy": "graph_focused",
       "max_results": 15,
       "include_reasoning": true
     }'
```

### Complex Multi-hop Query

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What are the applications of reinforcement learning in robotics and how do they relate to computer vision?",
       "strategy": "hybrid",
       "max_results": 20
     }'
```

### File Upload

```bash
curl -X POST "http://localhost:8000/documents/upload-file" \
     -F "file=@document.txt" \
     -F "title=Technical Documentation" \
     -F "domain=technical"
```

### Batch Document Upload

```python
import requests
import json

documents = [
    {
        "title": "AI Fundamentals",
        "content": "Artificial intelligence fundamentals...",
        "domain": "educational"
    },
    {
        "title": "ML Algorithms",
        "content": "Machine learning algorithms overview...",
        "domain": "technical"
    }
]

for doc in documents:
    response = requests.post(
        "http://localhost:8000/documents/upload",
        json=doc
    )
    print(f"Uploaded: {response.json()['document_id']}")
```

## Best Practices

### Query Optimization

1. **Be Specific**: More specific queries yield better results
   - Good: "What are convolutional neural networks used for in computer vision?"
   - Poor: "What is AI?"

2. **Use Appropriate Strategy**:
   - `vector_focused`: For factual questions
   - `graph_focused`: For relationship exploration
   - `hybrid`: For complex multi-entity queries

3. **Limit Results**: Use appropriate `max_results` to balance comprehensiveness and performance

### Document Upload Best Practices

1. **Provide Good Metadata**: Include relevant tags, authors, and domain information
2. **Structure Content**: Well-structured content improves entity extraction
3. **Batch Processing**: For multiple documents, implement proper error handling and retry logic
4. **Domain Classification**: Use appropriate domain values for better organization

### Error Handling

```python
import requests
import time

def robust_query(query_text, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.post(
                "http://localhost:8000/query",
                json={"query": query_text},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 429:
                # Rate limited, wait and retry
                time.sleep(60)
                continue
            else:
                # Other error, don't retry
                response.raise_for_status()
                
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)  # Exponential backoff
    
    raise Exception("Max retries exceeded")
```

### Performance Optimization

1. **Connection Pooling**: Use session objects for multiple requests
2. **Async Requests**: Use async libraries for concurrent requests
3. **Caching**: Cache responses for repeated queries
4. **Monitoring**: Monitor response times and error rates

## Testing

### Unit Testing with pytest

```python
import pytest
from fastapi.testclient import TestClient
from src.api.main import app

client = TestClient(app)

def test_query_endpoint():
    response = client.post("/query", json={
        "query": "What is machine learning?",
        "max_results": 5
    })
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert "query_id" in data
```

### Integration Testing

```bash
# Run comprehensive API tests
python scripts/test_api.py --all

# Run only pytest tests
python scripts/test_api.py --pytest

# Run only API integration tests
python scripts/test_api.py --api-tests --url http://localhost:8000
```

### Load Testing

```python
import asyncio
import aiohttp
import time

async def load_test():
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(100):
            task = session.post(
                "http://localhost:8000/query",
                json={"query": f"Test query {i}"}
            )
            tasks.append(task)
        
        start_time = time.time()
        responses = await asyncio.gather(*tasks)
        end_time = time.time()
        
        print(f"100 requests completed in {end_time - start_time:.2f}s")
        print(f"Average: {(end_time - start_time) / 100:.3f}s per request")

# Run load test
asyncio.run(load_test())
```

## Troubleshooting

### Common Issues

#### 1. Connection Refused
```
requests.exceptions.ConnectionError: Connection refused
```
**Solution**: Ensure the API server is running on the correct host/port.

#### 2. Validation Errors
```json
{"error": "Validation Error", "message": "field required"}
```
**Solution**: Check request format against API documentation. Ensure all required fields are provided.

#### 3. Rate Limiting
```json
{"error": "Rate Limit Exceeded"}
```
**Solution**: Implement exponential backoff and respect rate limits.

#### 4. Timeout Errors
```
requests.exceptions.Timeout
```
**Solution**: Increase timeout values for complex queries or large document uploads.

### Debugging Steps

1. **Check API Health**:
   ```bash
   curl http://localhost:8000/health
   ```

2. **Validate Request Format**:
   ```bash
   curl -X POST "http://localhost:8000/test/validate"
   ```

3. **Check System Status**:
   ```bash
   curl http://localhost:8000/system/status
   ```

4. **Review API Examples**:
   ```bash
   curl http://localhost:8000/test/examples
   ```

### Performance Issues

1. **Slow Query Response**:
   - Check system resources
   - Review query complexity
   - Consider using more specific queries

2. **Document Upload Failures**:
   - Check document size limits
   - Verify content encoding
   - Review metadata format

3. **High Error Rates**:
   - Check agent status: `/agents/status`
   - Review system logs
   - Verify database connections

### Getting Help

1. **API Documentation**: Visit `/docs` for interactive documentation
2. **System Status**: Check `/health` and `/system/status` for system information
3. **Examples**: Use `/test/examples` for usage examples
4. **Validation**: Run `/test/validate` to check API functionality

For additional support, include the following information:
- Request ID from error responses
- Complete request/response examples
- System status information
- Error logs and timestamps