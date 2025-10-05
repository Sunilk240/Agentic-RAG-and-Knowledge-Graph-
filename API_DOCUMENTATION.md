# 📡 API Documentation

## Graph-Enhanced Agentic RAG System API

Welcome to the comprehensive API documentation for the Graph-Enhanced Agentic RAG System. This API provides intelligent knowledge discovery through a sophisticated multi-agent architecture.

---

## 🚀 Quick Start

### Base URL
```
Production: https://your-app.onrender.com
Local: http://localhost:8000
```

### Authentication
Currently, the API is open access. Future versions will include API key authentication.

### Content Type
All requests should use `Content-Type: application/json` unless otherwise specified.

---

## 📋 API Endpoints Overview

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and status |
| `/health` | GET | System health check |
| `/query` | POST | Process intelligent queries |
| `/documents/upload` | POST | Upload documents for ingestion |
| `/agents/status` | GET | Multi-agent system status |
| `/docs` | GET | Interactive API documentation |

---

## 🔍 Core Endpoints

### 1. Query Processing

**Endpoint:** `POST /query`

**Description:** Process user queries using the multi-agent system with automatic strategy selection.

#### Request Schema

```json
{
  "query": "string (required, 1-1000 characters)",
  "strategy": "string (optional: 'vector_focused', 'graph_focused', 'hybrid')",
  "max_results": "integer (optional, default: 10, range: 1-100)",
  "include_reasoning": "boolean (optional, default: true)",
  "user_id": "string (optional, for multi-tenant support)"
}
```

#### Request Examples

**Simple Factual Query:**
```json
{
  "query": "What is machine learning?",
  "max_results": 10,
  "include_reasoning": true
}
```

**Relationship Query:**
```json
{
  "query": "How are neural networks related to deep learning and artificial intelligence?",
  "max_results": 15,
  "strategy": "graph_focused",
  "include_reasoning": true
}
```

**Complex Multi-hop Query:**
```json
{
  "query": "What are the applications of reinforcement learning in robotics and how do they relate to computer vision techniques?",
  "max_results": 20,
  "strategy": "hybrid",
  "include_reasoning": true
}
```

#### Response Schema

```json
{
  "query_id": "string (UUID)",
  "response": "string (generated answer)",
  "sources": [
    {
      "id": "string",
      "title": "string",
      "content_preview": "string",
      "source_type": "string (document|graph_entity)",
      "relevance_score": "float (0.0-1.0)",
      "domain": "string"
    }
  ],
  "citations": [
    {
      "id": "string",
      "source": "string",
      "relevance": "float",
      "citation_text": "string"
    }
  ],
  "reasoning_path": "string (explanation of processing steps)",
  "confidence_score": "float (0.0-1.0)",
  "processing_time": "float (seconds)",
  "strategy_used": "string",
  "entities_found": ["string"]
}
```

#### Example Response

```json
{
  "query_id": "123e4567-e89b-12d3-a456-426614174000",
  "response": "Machine learning is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. It involves algorithms that can identify patterns in data and make predictions or decisions based on those patterns. Key types include supervised learning (learning from labeled examples), unsupervised learning (finding patterns in unlabeled data), and reinforcement learning (learning through interaction with an environment).",
  "sources": [
    {
      "id": "doc_ml_intro_001",
      "title": "Introduction to Machine Learning",
      "content_preview": "Machine learning algorithms build mathematical models based on training data...",
      "source_type": "document",
      "relevance_score": 0.92,
      "domain": "technical"
    },
    {
      "id": "entity_ml_concept",
      "name": "Machine Learning",
      "type": "concept",
      "source_type": "graph_entity",
      "relevance_score": 0.89,
      "relationships": ["part_of:Artificial Intelligence", "includes:Supervised Learning"]
    }
  ],
  "citations": [
    {
      "id": "1",
      "source": "Introduction to Machine Learning",
      "page": 15,
      "relevance": 0.92,
      "citation_text": "[1] Introduction to Machine Learning, p. 15"
    }
  ],
  "reasoning_path": "Query Analysis: Identified 'machine learning' as primary concept → Strategy Selection: Chose vector search for factual query → Vector Search: Found 8 relevant documents → Graph Navigation: Explored ML concept relationships → Synthesis: Combined vector results with graph context → Response Generation: Created comprehensive answer with citations",
  "confidence_score": 0.89,
  "processing_time": 1.23,
  "strategy_used": "vector_focused",
  "entities_found": ["machine learning", "artificial intelligence", "supervised learning", "unsupervised learning"]
}
```

#### cURL Example

```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "query": "What is machine learning?",
       "max_results": 10,
       "include_reasoning": true
     }'
```

---

### 2. Document Upload

**Endpoint:** `POST /documents/upload`

**Description:** Upload and ingest documents into the knowledge base.

#### Request Schema (Form Data)

```
file: File (required, supported formats: .txt, .pdf, .md, .html)
title: string (optional, document title)
domain: string (optional: 'technical', 'business', 'research', 'general')
metadata: JSON string (optional, additional metadata)
```

#### Request Examples

**Technical Document Upload:**
```bash
curl -X POST "http://localhost:8000/documents/upload" \
     -F "file=@transformer_paper.pdf" \
     -F "title=Transformer Architecture in NLP" \
     -F "domain=technical" \
     -F 'metadata={"author": "Vaswani et al.", "year": 2017}'
```

**Text Content Upload:**
```bash
curl -X POST "http://localhost:8000/documents/upload" \
     -F "file=@business_strategy.txt" \
     -F "title=AI Implementation Strategy" \
     -F "domain=business"
```

#### Response Schema

```json
{
  "document_id": "string (UUID)",
  "status": "string (success|error)",
  "message": "string",
  "entities_extracted": "integer",
  "relationships_created": "integer",
  "processing_time": "float (seconds)",
  "processing_details": {
    "text_chunks_created": "integer",
    "embeddings_generated": "integer",
    "graph_nodes_created": "integer",
    "graph_relationships_created": "integer",
    "domain_entities_identified": ["string"]
  }
}
```

#### Example Response

```json
{
  "document_id": "doc_789abc12-def3-4567-8901-234567890abc",
  "status": "success",
  "message": "Document 'Transformer Architecture in NLP' uploaded and processed successfully",
  "entities_extracted": 25,
  "relationships_created": 18,
  "processing_time": 3.45,
  "processing_details": {
    "text_chunks_created": 12,
    "embeddings_generated": 12,
    "graph_nodes_created": 25,
    "graph_relationships_created": 18,
    "domain_entities_identified": ["transformer", "attention mechanism", "encoder", "decoder", "NLP"]
  }
}
```

---

### 3. System Health

**Endpoint:** `GET /health`

**Description:** Check system health and component status.

#### Response Schema

```json
{
  "status": "string (healthy|degraded|unhealthy)",
  "version": "string",
  "environment": "string",
  "timestamp": "string (ISO 8601)",
  "components": {
    "api": "string (healthy|degraded|unhealthy)",
    "neo4j": "string",
    "chroma": "string",
    "coordinator_agent": "string",
    "graph_navigator": "string",
    "vector_retrieval": "string",
    "synthesis_agent": "string"
  },
  "uptime": "float (seconds)",
  "issues": ["string"] // Present only if status is degraded/unhealthy
}
```

#### Example Response

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "environment": "production",
  "timestamp": "2024-01-01T12:00:00Z",
  "components": {
    "api": "healthy",
    "neo4j": "healthy",
    "chroma": "healthy",
    "coordinator_agent": "healthy",
    "graph_navigator": "healthy",
    "vector_retrieval": "healthy",
    "synthesis_agent": "healthy"
  },
  "uptime": 86400.5
}
```

#### cURL Example

```bash
curl -X GET "http://localhost:8000/health"
```

---

### 4. Agent Status

**Endpoint:** `GET /agents/status`

**Description:** Get detailed status of all agents in the system.

#### Response Schema

```json
{
  "agents": {
    "coordinator": {
      "status": "string (healthy|degraded|unhealthy)",
      "last_activity": "string (ISO 8601)",
      "queries_processed": "integer",
      "average_response_time": "float (seconds)",
      "error_count": "integer",
      "description": "string"
    },
    "graph_navigator": {
      "status": "string",
      "last_activity": "string",
      "queries_processed": "integer",
      "average_response_time": "float",
      "error_count": "integer",
      "description": "string"
    },
    "vector_retrieval": {
      "status": "string",
      "last_activity": "string",
      "queries_processed": "integer",
      "average_response_time": "float",
      "error_count": "integer",
      "description": "string"
    },
    "synthesis": {
      "status": "string",
      "last_activity": "string",
      "responses_generated": "integer",
      "average_response_time": "float",
      "error_count": "integer",
      "description": "string"
    }
  },
  "total_agents": "integer",
  "healthy_agents": "integer",
  "last_updated": "string (ISO 8601)"
}
```

#### cURL Example

```bash
curl -X GET "http://localhost:8000/agents/status"
```

---

## ⚠️ Error Handling

### Error Response Format

All errors follow a consistent format:

```json
{
  "error": "string (error type)",
  "message": "string (human-readable message)",
  "details": {
    // Additional error-specific details
  },
  "timestamp": "string (ISO 8601)",
  "request_id": "string (for support)"
}
```

### Common Error Codes

#### 400 - Bad Request
```json
{
  "error": "Validation Error",
  "message": "Request validation failed. Please check your input data.",
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
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "req_123456789"
}
```

#### 404 - Not Found
```json
{
  "error": "Not Found",
  "message": "The requested endpoint '/invalid-endpoint' was not found",
  "details": {
    "method": "GET",
    "path": "/invalid-endpoint",
    "available_endpoints": [
      "/docs - API documentation",
      "/health - Health check",
      "/query - Process queries",
      "/documents/upload - Upload documents"
    ],
    "documentation": "/docs"
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "req_987654321"
}
```

#### 429 - Rate Limit Exceeded
```json
{
  "error": "Rate Limit Exceeded",
  "message": "Too many requests. Please slow down.",
  "details": {
    "rate_limits": {
      "query_endpoint": "100 requests per minute",
      "document_upload": "50 requests per minute"
    },
    "retry_after": "60 seconds",
    "suggestions": [
      "Wait before making additional requests",
      "Implement exponential backoff in your client"
    ]
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "req_555666777"
}
```

#### 500 - Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred while processing your request",
  "details": {
    "request_id": "req_111222333",
    "support_message": "Please contact support with this request ID if the problem persists",
    "troubleshooting": [
      "Check system status at /health",
      "Verify your request format matches the API documentation",
      "Try again in a few moments"
    ]
  },
  "timestamp": "2024-01-01T12:00:00Z",
  "request_id": "req_111222333"
}
```

---

## 🔧 Query Strategies

The system automatically selects the best retrieval strategy, but you can also specify one:

### Vector Focused (`vector_focused`)
- **Best for:** Simple factual questions, concept definitions
- **Uses:** Semantic similarity search in vector database
- **Example:** "What is machine learning?"

### Graph Focused (`graph_focused`)
- **Best for:** Relationship questions, entity connections
- **Uses:** Graph traversal and Cypher queries
- **Example:** "How are neural networks related to deep learning?"

### Hybrid (`hybrid`)
- **Best for:** Complex multi-hop questions, comprehensive analysis
- **Uses:** Both graph traversal and vector search
- **Example:** "What are the applications of reinforcement learning in robotics and how do they relate to computer vision?"

---

## 📊 Response Quality Indicators

### Confidence Score
- **Range:** 0.0 - 1.0
- **Interpretation:**
  - 0.8-1.0: High confidence, comprehensive answer
  - 0.6-0.8: Good confidence, reliable answer
  - 0.4-0.6: Moderate confidence, partial answer
  - 0.0-0.4: Low confidence, limited information

### Relevance Score (per source)
- **Range:** 0.0 - 1.0
- **Interpretation:**
  - 0.9-1.0: Highly relevant to query
  - 0.7-0.9: Relevant with good context
  - 0.5-0.7: Moderately relevant
  - 0.0-0.5: Low relevance

---

## 🚀 Best Practices

### Query Optimization
1. **Be specific:** More specific queries yield better results
2. **Use natural language:** The system understands conversational queries
3. **Ask follow-up questions:** Build on previous queries for deeper insights
4. **Specify relationships:** Use words like "related to", "connected with", "part of"

### Document Upload Tips
1. **Provide titles:** Clear titles improve entity extraction
2. **Use metadata:** Additional context helps with categorization
3. **Choose appropriate domains:** Helps with domain-specific processing
4. **Upload related documents:** Creates richer knowledge graphs

### Performance Optimization
1. **Limit max_results:** Use appropriate result limits for your use case
2. **Cache responses:** Cache frequently asked questions
3. **Batch uploads:** Upload multiple documents together when possible
4. **Monitor health:** Check `/health` endpoint for system status

---

## 🔗 Integration Examples

### Python Client

```python
import requests
import json

class GraphRAGClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
    
    def query(self, query_text, strategy=None, max_results=10):
        """Send a query to the API"""
        payload = {
            "query": query_text,
            "max_results": max_results,
            "include_reasoning": True
        }
        if strategy:
            payload["strategy"] = strategy
        
        response = requests.post(
            f"{self.base_url}/query",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        return response.json()
    
    def upload_document(self, file_path, title=None, domain=None):
        """Upload a document"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {}
            if title:
                data['title'] = title
            if domain:
                data['domain'] = domain
            
            response = requests.post(
                f"{self.base_url}/documents/upload",
                files=files,
                data=data
            )
        return response.json()
    
    def health_check(self):
        """Check system health"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()

# Usage example
client = GraphRAGClient()

# Query the system
result = client.query("What is machine learning?")
print(f"Response: {result['response']}")
print(f"Confidence: {result['confidence_score']}")

# Upload a document
upload_result = client.upload_document(
    "my_document.pdf", 
    title="AI Research Paper",
    domain="technical"
)
print(f"Document uploaded: {upload_result['document_id']}")

# Check health
health = client.health_check()
print(f"System status: {health['status']}")
```

### JavaScript/Node.js Client

```javascript
class GraphRAGClient {
    constructor(baseUrl = 'http://localhost:8000') {
        this.baseUrl = baseUrl;
    }

    async query(queryText, options = {}) {
        const payload = {
            query: queryText,
            max_results: options.maxResults || 10,
            include_reasoning: true,
            ...options
        };

        const response = await fetch(`${this.baseUrl}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        });

        return await response.json();
    }

    async uploadDocument(file, options = {}) {
        const formData = new FormData();
        formData.append('file', file);
        
        if (options.title) formData.append('title', options.title);
        if (options.domain) formData.append('domain', options.domain);
        if (options.metadata) formData.append('metadata', JSON.stringify(options.metadata));

        const response = await fetch(`${this.baseUrl}/documents/upload`, {
            method: 'POST',
            body: formData
        });

        return await response.json();
    }

    async healthCheck() {
        const response = await fetch(`${this.baseUrl}/health`);
        return await response.json();
    }
}

// Usage example
const client = new GraphRAGClient();

// Query the system
client.query('What is machine learning?')
    .then(result => {
        console.log('Response:', result.response);
        console.log('Confidence:', result.confidence_score);
    });

// Check health
client.healthCheck()
    .then(health => {
        console.log('System status:', health.status);
    });
```

---

## 📞 Support

### Interactive Documentation
Visit `/docs` for interactive API documentation with live testing capabilities.

### Health Monitoring
Monitor system status at `/health` endpoint.

### Troubleshooting
1. Check system health first: `GET /health`
2. Verify request format matches documentation
3. Check error response for specific guidance
4. Contact support with request ID for server errors

---

## 🔄 API Versioning

Current version: **v1.0.0**

The API follows semantic versioning. Breaking changes will increment the major version number.

---

This documentation covers all available endpoints and features. For the most up-to-date information, always refer to the interactive documentation at `/docs`.