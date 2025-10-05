# Graph Navigator Agent

The Graph Navigator Agent is a core component of the Graph-Enhanced Agentic RAG system responsible for intelligent graph database operations. It provides sophisticated entity lookup, relationship traversal, and Cypher query generation capabilities.

## Overview

The Graph Navigator Agent implements three main functionalities:

1. **Entity Lookup and Identification** - Fuzzy matching and disambiguation of entities in the graph
2. **Graph Traversal Algorithms** - Multi-hop relationship exploration and path finding
3. **Cypher Query Generation** - Dynamic query building with optimization

## Architecture

The agent is composed of four main classes:

### EntityMatcher
Handles fuzzy entity matching and disambiguation:
- Extracts entity candidates from natural language queries
- Performs fuzzy string matching against the graph database
- Disambiguates multiple matches using contextual information
- Scores and ranks entity matches by relevance

### GraphTraverser
Manages graph traversal operations:
- Traverses relationships from starting entities with configurable depth
- Finds shortest paths between specific entities
- Extracts relevant subgraphs around center entities
- Supports directional traversal (incoming, outgoing, both)

### CypherQueryGenerator
Generates and optimizes Cypher queries:
- Creates parameterized queries for common patterns
- Optimizes queries for performance with indexes and limits
- Provides templates for frequent operations
- Supports dynamic query building

### GraphNavigatorAgent
Main agent class that orchestrates all operations:
- Implements the GraphNavigatorInterface
- Handles message processing and agent communication
- Coordinates between EntityMatcher, GraphTraverser, and CypherQueryGenerator
- Provides high-level API for graph operations

## Key Features

### Fuzzy Entity Matching
```python
# Find entities using natural language
entities = await agent.find_entities("Python web development frameworks")
# Returns: [Entity(name="Python", type="Technology"), Entity(name="Django", type="Framework"), ...]
```

### Multi-hop Relationship Traversal
```python
# Traverse relationships up to depth 3
result = await agent.traverse_relationships(start_entities, depth=3)
# Returns: GraphResult with entities, relationships, and paths
```

### Dynamic Cypher Query Generation
```python
# Generate optimized queries
query, params = query_generator.generate_entity_search_query(
    "Python", 
    entity_types=["Technology"], 
    limit=10
)
```

### Path Finding
```python
# Find paths between entities
paths = await traverser.find_paths_between_entities("entity-1", "entity-2", max_depth=4)
# Returns: [["entity-1", "intermediate", "entity-2"], ...]
```

## Usage Examples

### Basic Entity Search
```python
from src.agents.graph_navigator import GraphNavigatorAgent

# Initialize agent
agent = GraphNavigatorAgent("my-graph-navigator")

# Search for entities
entities = await agent.find_entities("machine learning algorithms")

for entity in entities:
    print(f"{entity.name} ({entity.type}): {entity.description}")
```

### Relationship Exploration
```python
# Start from specific entities
start_entities = [
    Entity(id="python-1", name="Python", type="Technology"),
    Entity(id="django-1", name="Django", type="Framework")
]

# Traverse relationships
result = await agent.traverse_relationships(start_entities, depth=2)

print(f"Found {len(result.entities)} connected entities")
print(f"Discovered {len(result.relationships)} relationships")
print(f"Identified {len(result.paths)} connection paths")
```

### Custom Cypher Queries
```python
# Execute custom Cypher query
cypher = """
MATCH (tech:Entity {entity_type: 'Technology'})
MATCH (tech)-[:RELATED_TO]-(framework:Entity {entity_type: 'Framework'})
RETURN tech, framework
LIMIT 10
"""

result = await agent.execute_cypher_query(cypher)
```

### Message-Based Communication
```python
from src.core.interfaces import MessageType, AgentMessage

# Create graph search message
message = AgentMessage(
    agent_id="coordinator",
    message_type=MessageType.GRAPH_SEARCH,
    payload={
        "query": "Find connections between Python and web development",
        "depth": 2
    }
)

# Process message
response = await agent.process_message(message)
```

## Configuration

### Entity Matching Parameters
```python
entity_matcher = EntityMatcher(neo4j_manager)
entity_matcher.similarity_threshold = 0.6  # Minimum similarity for fuzzy matching
```

### Traversal Limits
```python
graph_traverser = GraphTraverser(neo4j_manager)
graph_traverser.max_traversal_depth = 4      # Maximum depth for safety
graph_traverser.max_paths_per_query = 50     # Limit paths returned
```

### Query Optimization
```python
# Queries are automatically optimized with:
# - Index hints where appropriate
# - Automatic LIMIT clauses for safety
# - Parameter binding for security
```

## Performance Considerations

### Indexing
The agent works best with proper Neo4j indexes:
```cypher
CREATE INDEX entity_name_index FOR (e:Entity) ON (e.name);
CREATE INDEX entity_type_index FOR (e:Entity) ON (e.entity_type);
CREATE INDEX entity_vector_id_index FOR (e:Entity) ON (e.vector_id);
```

### Query Limits
- Automatic limits prevent runaway queries
- Configurable maximum traversal depth
- Result set size limits for performance

### Connection Pooling
- Uses Neo4j driver connection pooling
- Async query execution for better performance
- Retry logic for transient failures

## Error Handling

The agent includes comprehensive error handling:

### Connection Errors
```python
try:
    entities = await agent.find_entities("query")
except Neo4jConnectionError as e:
    logger.error(f"Database connection failed: {e}")
```

### Query Errors
```python
try:
    result = await agent.execute_cypher_query(cypher)
except Exception as e:
    logger.error(f"Query execution failed: {e}")
    # Returns empty GraphResult on error
```

### Graceful Degradation
- Returns empty results instead of crashing
- Logs detailed error information
- Provides fallback mechanisms

## Integration with Other Agents

### Coordinator Agent Integration
```python
# Coordinator sends graph search requests
graph_message = create_graph_search_message(
    query="Find related technologies",
    entities=["Python", "Django"],
    depth=2
)

response = await graph_navigator.process_message(graph_message)
```

### Vector Retrieval Agent Coordination
```python
# Graph results can be combined with vector search
graph_entities = await graph_navigator.find_entities(query)
vector_results = await vector_agent.search_similar_documents(query)

# Synthesis agent combines both results
combined_result = await synthesis_agent.integrate_results(
    graph_results=graph_result,
    vector_results=vector_results
)
```

## Testing

The agent includes comprehensive tests:

```bash
# Run all Graph Navigator tests
python -m pytest tests/test_graph_navigator_agent.py -v

# Run specific test class
python -m pytest tests/test_graph_navigator_agent.py::TestEntityMatcher -v

# Run with coverage
python -m pytest tests/test_graph_navigator_agent.py --cov=src.agents.graph_navigator
```

## Requirements Mapping

This implementation satisfies the following requirements:

- **Requirement 1.1**: Entity extraction and identification from user queries
- **Requirement 1.2**: Multi-hop relationship exploration and traversal
- **Requirement 1.3**: Graph-based context discovery for complex queries
- **Requirement 1.4**: Dynamic Cypher query generation and optimization

## Future Enhancements

Potential improvements for the Graph Navigator Agent:

1. **Machine Learning Integration**: Use ML models for better entity disambiguation
2. **Caching Layer**: Add intelligent caching for frequently accessed paths
3. **Graph Analytics**: Implement centrality and community detection algorithms
4. **Real-time Updates**: Support for real-time graph updates and notifications
5. **Multi-database Support**: Extend to support multiple graph databases

## Troubleshooting

### Common Issues

**Entity Not Found**
```python
# Check entity exists in database
entities = await agent.find_entities("exact entity name")
if not entities:
    print("Entity not found - check spelling or add to database")
```

**Slow Traversal**
```python
# Reduce traversal depth or add more specific filters
result = await agent.traverse_relationships(entities, depth=1)  # Reduce depth
```

**Connection Timeouts**
```python
# Check Neo4j connection settings and network connectivity
# Increase timeout in configuration if needed
```

### Debug Mode
```python
import logging
logging.getLogger('src.agents.graph_navigator').setLevel(logging.DEBUG)
```

This enables detailed logging of all graph operations for troubleshooting.