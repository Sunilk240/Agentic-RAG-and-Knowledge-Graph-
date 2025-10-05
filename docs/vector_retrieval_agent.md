# Vector Retrieval Agent Documentation

## Overview

The Vector Retrieval Agent is a core component of the Graph-Enhanced Agentic RAG system that handles text embedding generation, semantic similarity search, and hybrid search capabilities. It uses sentence transformers for embedding generation and Chroma vector database for storage and retrieval.

## Architecture

### Components

1. **EmbeddingGenerationService**: Handles text-to-vector embedding generation with caching
2. **VectorRetrievalAgent**: Main agent class that orchestrates vector operations
3. **Chroma Integration**: Persistent vector database for document storage and retrieval

### Key Features

- **Text Embedding Generation**: Uses sentence transformers for high-quality embeddings
- **Batch Processing**: Efficient batch embedding generation for multiple documents
- **Caching**: LRU cache for embedding reuse and performance optimization
- **Semantic Search**: Cosine similarity-based document retrieval
- **Hybrid Search**: Combines semantic similarity with keyword matching and relevance scoring
- **Metadata Filtering**: Support for filtered searches based on document metadata
- **Agent Messaging**: Standardized message protocol for inter-agent communication

## Usage

### Basic Initialization

```python
from src.agents.vector_retrieval import VectorRetrievalAgent

# Initialize the agent
vector_agent = VectorRetrievalAgent(
    agent_id="my_vector_agent",
    model_name="all-MiniLM-L6-v2",
    chroma_persist_directory="./vector_db",
    collection_name="documents"
)
```

### Embedding Generation

```python
# Generate single embedding
embedding = await vector_agent.generate_embedding("Sample text to embed")

# Generate batch embeddings
texts = ["Text 1", "Text 2", "Text 3"]
embeddings = await vector_agent.generate_embeddings_batch(texts)
```

### Document Management

```python
from src.core.vector_models import DocumentEmbedding

# Create document with embedding
doc = DocumentEmbedding(
    content="Document content here",
    title="Document Title",
    embedding=embedding,
    embedding_model="all-MiniLM-L6-v2",
    embedding_dimension=384,
    metadata={"category": "example", "author": "user"}
)

# Add documents to vector database
await vector_agent.add_documents([doc])

# Update document
doc.content = "Updated content"
await vector_agent.update_document(doc)

# Delete document
await vector_agent.delete_document(doc.id)
```

### Search Operations

```python
# Semantic similarity search
result = await vector_agent.similarity_search(
    query="search query",
    k=10,  # number of results
    filters={"category": "example"}  # optional metadata filters
)

# Hybrid search (semantic + keyword)
hybrid_result = await vector_agent.hybrid_search(
    query="search query",
    semantic_weight=0.7,  # balance between semantic and keyword matching
    k=10
)

# Access results
for doc, similarity in zip(result.documents, result.similarities):
    print(f"Document: {doc.content}")
    print(f"Similarity: {similarity}")
```

### Agent Messaging

```python
from src.core.interfaces import AgentMessage, MessageType

# Create search message
message = AgentMessage(
    agent_id="coordinator",
    message_type=MessageType.VECTOR_SEARCH,
    payload={
        "query": "search query",
        "k": 5,
        "search_type": "hybrid",
        "semantic_weight": 0.8
    }
)

# Process message
response = await vector_agent.process_message(message)
```

## Configuration

### Model Selection

The agent supports various sentence transformer models:

- `all-MiniLM-L6-v2` (default): Fast, good quality, 384 dimensions
- `all-mpnet-base-v2`: Higher quality, 768 dimensions, slower
- `paraphrase-multilingual-MiniLM-L12-v2`: Multilingual support

### Caching Configuration

```python
embedding_service = EmbeddingGenerationService(
    model_name="all-MiniLM-L6-v2",
    cache_size=1000,  # number of embeddings to cache
    device="cpu"  # or "cuda" for GPU acceleration
)
```

### Chroma Configuration

```python
vector_agent = VectorRetrievalAgent(
    chroma_persist_directory="./chroma_db",  # persistent storage location
    collection_name="my_documents",  # collection name
    embedding_cache_size=1000  # embedding cache size
)
```

## Performance Considerations

### Embedding Generation

- **Batch Processing**: Use `generate_embeddings_batch()` for multiple texts
- **Caching**: Embeddings are cached to avoid recomputation
- **Model Loading**: Models are loaded lazily on first use

### Vector Search

- **Index Optimization**: Chroma automatically optimizes vector indices
- **Batch Size**: Default batch size of 100 for document addition
- **Memory Usage**: Monitor memory usage with large document collections

### Hybrid Search

- **Semantic Weight**: Balance between semantic (0.0-1.0) and keyword matching
- **Re-ranking**: Additional relevance scoring based on exact matches and keyword overlap
- **Result Filtering**: Use metadata filters to narrow search scope

## Error Handling

The agent includes comprehensive error handling:

```python
try:
    result = await vector_agent.similarity_search("query")
except RuntimeError as e:
    print(f"Search failed: {e}")

# Health check
health = await vector_agent.health_check()
if health["status"] != "healthy":
    print("Agent is unhealthy:", health["checks"])
```

## Integration with Other Agents

### Coordinator Agent Integration

The Vector Retrieval Agent is designed to work with the Coordinator Agent:

```python
# Coordinator sends vector search request
vector_message = AgentMessage(
    agent_id="coordinator",
    message_type=MessageType.VECTOR_SEARCH,
    payload={"query": "user query", "k": 10}
)

response = await vector_agent.process_message(vector_message)
```

### Graph Navigator Integration

For hybrid retrieval combining graph and vector search:

```python
# Vector agent provides semantic context
vector_results = await vector_agent.similarity_search("query")

# Results can be combined with graph traversal results
# by the Synthesis Agent
```

## Monitoring and Debugging

### Agent Information

```python
info = vector_agent.get_agent_info()
print(f"Agent ID: {info['agent_id']}")
print(f"Model: {info['model_info']['model_name']}")
print(f"Document Count: {info['document_count']}")
print(f"Cache Size: {info['cache_stats']['cache_size']}")
```

### Health Monitoring

```python
health = await vector_agent.health_check()
print(f"Overall Status: {health['status']}")
print(f"Embedding Service: {health['checks']['embedding_service']['status']}")
print(f"Vector Database: {health['checks']['vector_database']['status']}")
```

### Cache Statistics

```python
from src.agents.vector_retrieval import EmbeddingGenerationService

service = EmbeddingGenerationService()
stats = service.get_cache_stats()
print(f"Cache Hit Ratio: {stats['cache_hit_ratio']}")
print(f"Cache Size: {stats['cache_size']}/{stats['max_cache_size']}")
```

## Best Practices

### Document Preparation

1. **Chunking**: Split large documents into smaller chunks (500-1000 tokens)
2. **Metadata**: Include relevant metadata for filtering and organization
3. **Content Quality**: Ensure clean, well-formatted text for better embeddings

### Search Optimization

1. **Query Preprocessing**: Clean and normalize queries before search
2. **Result Filtering**: Use metadata filters to improve relevance
3. **Hybrid Search**: Use hybrid search for better recall and precision

### Performance Optimization

1. **Batch Operations**: Use batch methods for multiple documents
2. **Cache Management**: Monitor and tune cache size based on usage patterns
3. **Model Selection**: Choose appropriate model based on quality vs. speed requirements

### Error Handling

1. **Graceful Degradation**: Handle model loading failures gracefully
2. **Retry Logic**: Implement retry logic for transient failures
3. **Health Monitoring**: Regular health checks for production deployments

## Troubleshooting

### Common Issues

1. **Model Loading Slow**: First-time model download can be slow
2. **Memory Usage**: Large models and document collections use significant memory
3. **Embedding Dimension Mismatch**: Ensure consistent embedding dimensions

### Solutions

1. **Pre-download Models**: Download models during deployment
2. **Memory Monitoring**: Monitor memory usage and adjust batch sizes
3. **Validation**: Validate embedding dimensions before storage

## Examples

See `examples/vector_retrieval_example.py` for comprehensive usage examples including:

- Basic embedding generation
- Document management
- Search operations
- Agent messaging
- Advanced features like re-ranking and hybrid search

## Testing

Run the test suite:

```bash
python -m pytest tests/test_vector_retrieval_agent.py -v
```

For quick verification without model loading:

```bash
python verify_vector_agent.py
```