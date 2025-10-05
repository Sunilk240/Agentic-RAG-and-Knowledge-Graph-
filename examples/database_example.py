"""
Example usage of database connections and entity-vector mapping service.
"""

import os
import sys
import asyncio
from datetime import datetime

# Add src to path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core.database import (
    Neo4jConnectionManager, ChromaConnectionManager,
    initialize_databases, close_databases,
    get_neo4j_manager, get_chroma_manager
)
from core.mapping_service import get_mapping_service
from core.config import get_config


async def main():
    """Demonstrate database connections and mapping service usage."""
    print("=== Database Connection and Mapping Service Example ===\n")
    
    try:
        # Load configuration
        config = get_config()
        print(f"Environment: {config.environment}")
        print(f"Neo4j URI: {config.database.neo4j_uri}")
        print(f"Chroma persist directory: {config.database.chroma_persist_directory}")
        print()
        
        # Example 1: Direct connection manager usage
        print("1. Creating connection managers...")
        
        neo4j_manager = Neo4jConnectionManager(
            uri="bolt://localhost:7687",  # Use local Neo4j for example
            user="neo4j",
            password="password",
            database="neo4j"
        )
        
        chroma_manager = ChromaConnectionManager(
            persist_directory="./example_chroma_db"
        )
        
        print("   ✓ Connection managers created")
        
        # Example 2: Test connections (will fail if databases not running)
        print("\n2. Testing connections...")
        
        try:
            neo4j_manager.connect()
            print("   ✓ Neo4j connection successful")
            
            # Test a simple query
            result = neo4j_manager.execute_query("RETURN 'Hello Neo4j' as message")
            print(f"   ✓ Neo4j query result: {result[0]['message']}")
            
        except Exception as e:
            print(f"   ✗ Neo4j connection failed: {e}")
        
        try:
            chroma_manager.connect()
            print("   ✓ Chroma connection successful")
            
            # Test collection creation
            collection = chroma_manager.create_collection("test_collection")
            print("   ✓ Chroma test collection created")
            
        except Exception as e:
            print(f"   ✗ Chroma connection failed: {e}")
        
        # Example 3: Entity-Vector Mapping Service
        print("\n3. Testing Entity-Vector Mapping Service...")
        
        try:
            mapping_service = get_mapping_service()
            print("   ✓ Mapping service instance created")
            
            # Note: This would require actual database connections to work
            print("   ℹ Mapping service operations require live database connections")
            
            # Show what operations are available
            print("   Available operations:")
            print("     - create_mapping(entity_id, entity_type, vector_id, collection_name)")
            print("     - get_vectors_for_entity(entity_id)")
            print("     - get_entities_for_vector(vector_id, collection_name)")
            print("     - validate_mapping_integrity()")
            print("     - synchronize_mappings()")
            
        except Exception as e:
            print(f"   ✗ Mapping service error: {e}")
        
        # Example 4: Configuration examples
        print("\n4. Configuration examples...")
        
        print("   Database configuration:")
        print(f"     Neo4j URI: {config.database.neo4j_uri}")
        print(f"     Neo4j User: {config.database.neo4j_user}")
        print(f"     Neo4j Database: {config.database.neo4j_database}")
        print(f"     Chroma Host: {config.database.chroma_host}")
        print(f"     Chroma Port: {config.database.chroma_port}")
        
        print("\n   Agent configuration:")
        print(f"     Max Retries: {config.agents.max_retries}")
        print(f"     Coordinator Timeout: {config.agents.coordinator_timeout}")
        print(f"     Graph Traversal Depth: {config.agents.graph_traversal_depth}")
        
        # Example 5: Health checks
        print("\n5. Health check examples...")
        
        try:
            neo4j_healthy = neo4j_manager.health_check()
            print(f"   Neo4j health: {'✓ Healthy' if neo4j_healthy else '✗ Unhealthy'}")
        except:
            print("   Neo4j health: ✗ Cannot check (not connected)")
        
        try:
            chroma_healthy = chroma_manager.health_check()
            print(f"   Chroma health: {'✓ Healthy' if chroma_healthy else '✗ Unhealthy'}")
        except:
            print("   Chroma health: ✗ Cannot check (not connected)")
        
        # Example 6: Async operations
        print("\n6. Async operation example...")
        
        try:
            # This would work if Neo4j is connected
            # result = await neo4j_manager.execute_query_async("RETURN datetime() as current_time")
            # print(f"   ✓ Async query result: {result}")
            print("   ℹ Async operations available for Neo4j queries")
        except Exception as e:
            print(f"   ✗ Async operation failed: {e}")
        
        print("\n=== Example completed ===")
        
    except Exception as e:
        print(f"Example failed with error: {e}")
    
    finally:
        # Clean up connections
        try:
            neo4j_manager.disconnect()
            chroma_manager.disconnect()
            print("\n✓ Connections closed")
        except:
            pass


def demonstrate_mapping_workflow():
    """Demonstrate the entity-vector mapping workflow (conceptual)."""
    print("\n=== Entity-Vector Mapping Workflow ===")
    
    print("""
    Typical workflow for using the mapping service:
    
    1. Initialize the service:
       mapping_service = get_mapping_service()
       mapping_service.initialize()
    
    2. Create mappings when ingesting data:
       link = mapping_service.create_mapping(
           entity_id="doc_123",
           entity_type="Document", 
           vector_id="vec_456",
           collection_name="documents",
           metadata={"source": "research_paper.pdf"}
       )
    
    3. Query mappings during retrieval:
       vectors = mapping_service.get_vectors_for_entity("doc_123")
       entities = mapping_service.get_entities_for_vector("vec_456", "documents")
    
    4. Validate data consistency:
       results = mapping_service.validate_mapping_integrity()
       if not results["validation_passed"]:
           print("Found inconsistencies:", results["orphaned_entities"])
    
    5. Synchronize if needed:
       sync_results = mapping_service.synchronize_mappings(dry_run=False)
       print(f"Synchronized {sync_results['mappings_updated']} mappings")
    """)


if __name__ == "__main__":
    # Run the main example
    asyncio.run(main())
    
    # Show the mapping workflow
    demonstrate_mapping_workflow()