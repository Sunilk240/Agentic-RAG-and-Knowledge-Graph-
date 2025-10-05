# Database Setup and Configuration

This document describes the database connection management and entity-vector mapping service implemented for the Graph-Enhanced Agentic RAG system.

## Overview

The system uses two main databases:
- **Neo4j**: Graph database for storing entities and relationships
- **Chroma**: Vector database for storing document embeddings

A mapping service maintains consistency between the two databases by tracking relationships between graph entities and their corresponding vector embeddings.

## Components

### 1. Neo4j Connection Manager (`src/core/database.py`)

Provides robust connection management for Neo4j with:
- Connection pooling and retry logic
- Automatic reconnection on transient failures
- Support for both read and write transactions
- Async query execution
- Health monitoring

**Key Features:**
- Exponential backoff retry strategy
- Connection timeout handling
- Support for Neo4j AuraDB cloud connections
- Thread-safe operations

**Usage:**
```python
from src.core.database import Neo4jConnectionManager

manager = Neo4jConnectionManager(
    uri="bolt://localhost:7687",
    user="neo4j", 
    password="password",
    database="neo4j"
)

manager.connect()
result = manager.execute_query("MATCH (n) RETURN count(n) as node_count")
manager.disconnect()
```

### 2. Chroma Connection Manager (`src/core/database.py`)

Manages connections to Chroma vector database with:
- Support for both persistent and HTTP client modes
- Collection management and optimization
- Batch document operations
- Metadata filtering and search

**Key Features:**
- Persistent storage configuration
- Collection caching for performance
- Batch processing capabilities
- Vector search optimization

**Usage:**
```python
from src.core.database import ChromaConnectionManager

manager = ChromaConnectionManager(
    persist_directory="./chroma_db"
)

manager.connect()
collection = manager.create_collection("documents")
manager.add_documents("documents", ["Document text"], [{"source": "file.pdf"}])
results = manager.query_collection("documents", ["Query text"], n_results=5)
```

### 3. Entity-Vector Mapping Service (`src/core/mapping_service.py`)

Maintains bidirectional mapping between graph entities and vector embeddings:
- Creates and manages entity-vector links
- Validates mapping integrity
- Synchronizes data between databases
- Provides consistency checks

**Key Features:**
- Bidirectional mapping tracking
- Data consistency validation
- Automatic synchronization
- Orphaned data detection and cleanup

**Usage:**
```python
from src.core.mapping_service import get_mapping_service

service = get_mapping_service()
service.initialize()

# Create mapping
link = service.create_mapping(
    entity_id="entity_123",
    entity_type="Document",
    vector_id="vector_456", 
    collection_name="documents"
)

# Query mappings
vectors = service.get_vectors_for_entity("entity_123")
entities = service.get_entities_for_vector("vector_456", "documents")

# Validate integrity
results = service.validate_mapping_integrity()
```

## Configuration

Database settings are managed through environment variables and the configuration system:

### Environment Variables

```bash
# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

# Chroma Configuration  
CHROMA_HOST=localhost
CHROMA_PORT=8000
CHROMA_PERSIST_DIRECTORY=./chroma_db

# Agent Configuration
MAX_RETRIES=3
COORDINATOR_TIMEOUT=30
```

### Configuration Classes

The system uses Pydantic settings classes for type-safe configuration:

```python
from src.core.config import get_config

config = get_config()
print(config.database.neo4j_uri)
print(config.database.chroma_persist_directory)
```

## Database Schema

### Neo4j Schema

**Entity Nodes:**
```cypher
(:Entity {
  id: string,           // Unique entity identifier
  name: string,         // Entity name
  type: string,         // Entity type (Document, Concept, etc.)
  vector_id: string,    // Link to vector embedding
  vector_collection: string, // Chroma collection name
  updated_at: datetime  // Last update timestamp
})
```

**Relationships:**
```cypher
(:Entity)-[:RELATED_TO {strength: float, type: string}]->(:Entity)
(:Entity)-[:MENTIONED_IN {frequency: int}]->(:Document)
```

### Chroma Collections

**Document Collection:**
- Documents stored as text with embeddings
- Metadata includes entity references
- Supports filtered search by entity type

**Mapping Collection:**
- Stores entity-vector mapping metadata
- Used for consistency validation
- Enables bidirectional lookups

## Deployment

### Local Development

1. **Start Neo4j:**
   ```bash
   # Using Docker
   docker run -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j:latest
   ```

2. **Configure Chroma:**
   ```bash
   # Chroma will use persistent storage in ./chroma_db directory
   # No separate server needed for persistent mode
   ```

3. **Set Environment Variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

### Cloud Deployment (Render)

1. **Neo4j AuraDB:**
   - Create free Neo4j AuraDB instance
   - Use `neo4j+s://` URI for secure connection
   - Set environment variables in Render dashboard

2. **Chroma Cloud:**
   - Use persistent storage with mounted volumes
   - Configure `CHROMA_PERSIST_DIRECTORY` to persistent path

## Error Handling

The system includes comprehensive error handling:

### Connection Errors
- Automatic retry with exponential backoff
- Graceful degradation when databases unavailable
- Health check endpoints for monitoring

### Data Consistency Errors
- Validation of entity-vector mappings
- Detection of orphaned entities/vectors
- Automatic synchronization capabilities

### Example Error Handling:
```python
from src.core.database import Neo4jConnectionError, ChromaConnectionError

try:
    manager.execute_query("MATCH (n) RETURN n")
except Neo4jConnectionError as e:
    logger.error(f"Neo4j operation failed: {e}")
    # Implement fallback logic
```

## Testing

Run the database tests:

```bash
# Unit tests
python -m pytest tests/test_database_connections.py -v

# Integration tests  
python -m pytest tests/test_database_integration.py -v

# Example usage
python examples/database_example.py
```

## Performance Considerations

### Neo4j Optimization
- Connection pooling (max 50 connections)
- Query parameterization to prevent injection
- Index creation for frequently queried properties
- Transaction batching for bulk operations

### Chroma Optimization
- Collection caching to avoid repeated lookups
- Batch document operations
- Persistent storage for faster startup
- Metadata indexing for filtered searches

### Mapping Service Optimization
- Lazy initialization of connections
- Caching of frequently accessed mappings
- Batch validation operations
- Asynchronous synchronization

## Monitoring and Maintenance

### Health Checks
```python
# Check database health
neo4j_healthy = neo4j_manager.health_check()
chroma_healthy = chroma_manager.health_check()

# Get database statistics
neo4j_info = neo4j_manager.get_database_info()
chroma_stats = chroma_manager.get_collection_stats("documents")
```

### Maintenance Operations
```python
# Validate mapping integrity
results = mapping_service.validate_mapping_integrity()

# Synchronize mappings
sync_results = mapping_service.synchronize_mappings(dry_run=False)

# Get mapping statistics
stats = mapping_service.get_mapping_statistics()
```

## Troubleshooting

### Common Issues

1. **Neo4j Authentication Errors:**
   - Verify NEO4J_USER and NEO4J_PASSWORD
   - Check if Neo4j is running and accessible

2. **Chroma Connection Issues:**
   - Ensure CHROMA_PERSIST_DIRECTORY exists and is writable
   - Check if Chroma server is running (for HTTP mode)

3. **Mapping Inconsistencies:**
   - Run `validate_mapping_integrity()` to identify issues
   - Use `synchronize_mappings()` to fix inconsistencies

4. **Performance Issues:**
   - Monitor connection pool usage
   - Check for long-running transactions
   - Optimize query patterns and indexing

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

This will provide detailed information about database operations and connection management.