"""
Example usage of the Graph Navigator Agent.

This example demonstrates how to use the Graph Navigator Agent to:
1. Find entities in the graph database
2. Traverse relationships between entities
3. Execute custom Cypher queries
"""

import asyncio
import logging
from typing import List

from src.agents.graph_navigator import GraphNavigatorAgent
from src.core.interfaces import Entity, MessageType, AgentMessage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def example_entity_search():
    """Example of finding entities in the graph."""
    print("\n=== Entity Search Example ===")
    
    # Initialize the Graph Navigator Agent
    agent = GraphNavigatorAgent("example-graph-navigator")
    
    # Search for entities related to "Python"
    query = "What is Python and how does it relate to web development?"
    print(f"Searching for entities in query: {query}")
    
    try:
        entities = await agent.find_entities(query)
        
        print(f"Found {len(entities)} entities:")
        for i, entity in enumerate(entities, 1):
            print(f"  {i}. {entity.name} ({entity.type})")
            if entity.description:
                print(f"     Description: {entity.description[:100]}...")
        
        return entities
        
    except Exception as e:
        print(f"Error in entity search: {e}")
        return []


async def example_relationship_traversal(entities: List[Entity]):
    """Example of traversing relationships from entities."""
    print("\n=== Relationship Traversal Example ===")
    
    if not entities:
        print("No entities to traverse from")
        return
    
    agent = GraphNavigatorAgent("example-graph-navigator")
    
    # Take the first few entities for traversal
    start_entities = entities[:2]
    print(f"Traversing relationships from {len(start_entities)} entities:")
    for entity in start_entities:
        print(f"  - {entity.name}")
    
    try:
        result = await agent.traverse_relationships(start_entities, depth=2)
        
        print(f"\nTraversal Results:")
        print(f"  - Found {len(result.entities)} connected entities")
        print(f"  - Found {len(result.relationships)} relationships")
        print(f"  - Found {len(result.paths)} paths")
        
        # Show some of the connected entities
        if result.entities:
            print(f"\nConnected entities (showing first 5):")
            for i, entity in enumerate(result.entities[:5], 1):
                print(f"  {i}. {entity.name} ({entity.type})")
        
        # Show some relationship types
        if result.relationships:
            rel_types = set(rel.get('type', 'Unknown') for rel in result.relationships)
            print(f"\nRelationship types found: {', '.join(rel_types)}")
        
        # Show some paths
        if result.paths:
            print(f"\nExample paths (showing first 3):")
            for i, path in enumerate(result.paths[:3], 1):
                print(f"  {i}. Path length {len(path)}: {' -> '.join(path[:3])}{'...' if len(path) > 3 else ''}")
        
        return result
        
    except Exception as e:
        print(f"Error in relationship traversal: {e}")
        return None


async def example_cypher_query():
    """Example of executing a custom Cypher query."""
    print("\n=== Custom Cypher Query Example ===")
    
    agent = GraphNavigatorAgent("example-graph-navigator")
    
    # Example query to find technology entities and their relationships
    cypher_query = """
    MATCH (tech:Entity)
    WHERE tech.entity_type = 'Technology'
    OPTIONAL MATCH (tech)-[r]-(related)
    RETURN tech, type(r) as relationship_type, related
    ORDER BY tech.name
    LIMIT 10
    """
    
    print("Executing Cypher query:")
    print(cypher_query)
    
    try:
        result = await agent.execute_cypher_query(cypher_query)
        
        print(f"\nQuery Results:")
        print(f"  - Found {len(result.entities)} entities")
        print(f"  - Query: {result.cypher_query[:50]}...")
        
        if result.entities:
            print(f"\nEntities found:")
            for i, entity in enumerate(result.entities[:5], 1):
                print(f"  {i}. {entity.name} ({entity.type})")
        
        return result
        
    except Exception as e:
        print(f"Error executing Cypher query: {e}")
        return None


async def example_message_processing():
    """Example of processing messages through the agent."""
    print("\n=== Message Processing Example ===")
    
    agent = GraphNavigatorAgent("example-graph-navigator")
    
    # Create a graph search message
    message = AgentMessage(
        agent_id="example-coordinator",
        message_type=MessageType.GRAPH_SEARCH,
        payload={
            "query": "Find relationships between Python and Django",
            "depth": 2,
            "entities": []
        },
        correlation_id="example-123"
    )
    
    print("Processing graph search message:")
    print(f"  Query: {message.payload['query']}")
    print(f"  Depth: {message.payload['depth']}")
    
    try:
        response = await agent.process_message(message)
        
        if response:
            print(f"\nResponse received:")
            print(f"  Message type: {response.message_type}")
            print(f"  Correlation ID: {response.correlation_id}")
            
            if response.message_type == MessageType.RESPONSE:
                payload = response.payload
                entities = payload.get('entities', [])
                relationships = payload.get('relationships', [])
                paths = payload.get('paths', [])
                
                print(f"  Found {len(entities)} entities")
                print(f"  Found {len(relationships)} relationships")
                print(f"  Found {len(paths)} paths")
            elif response.message_type == MessageType.ERROR:
                print(f"  Error: {response.payload.get('error', 'Unknown error')}")
        else:
            print("No response received")
        
        return response
        
    except Exception as e:
        print(f"Error processing message: {e}")
        return None


async def main():
    """Main example function."""
    print("Graph Navigator Agent Examples")
    print("=" * 50)
    
    try:
        # Example 1: Entity Search
        entities = await example_entity_search()
        
        # Example 2: Relationship Traversal
        if entities:
            await example_relationship_traversal(entities)
        
        # Example 3: Custom Cypher Query
        await example_cypher_query()
        
        # Example 4: Message Processing
        await example_message_processing()
        
        print("\n" + "=" * 50)
        print("Examples completed successfully!")
        
    except Exception as e:
        print(f"Error in examples: {e}")
        logger.exception("Detailed error information:")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())