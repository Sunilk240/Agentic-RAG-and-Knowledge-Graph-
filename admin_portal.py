#!/usr/bin/env python3
"""
Admin Portal for Graph-Enhanced Agentic RAG System

Provides comprehensive visibility into:
1. Neo4j Graph Database (documents, entities, relationships)
2. Pinecone Vector Database (embeddings, chunks, metadata)
3. Chroma Fallback Database (if configured)

Features:
- Database statistics and health monitoring
- Document inventory and content preview
- Entity and relationship exploration
- Vector embedding analysis
- Search and filtering capabilities
"""

import asyncio
import sys
import os
from datetime import datetime
from typing import Dict, List, Any, Optional
import json
from dataclasses import dataclass

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import get_neo4j_manager, get_vector_manager
from src.core.config import get_config


@dataclass
class DatabaseStats:
    """Statistics for a database"""
    name: str
    status: str
    total_documents: int
    total_entities: int
    total_relationships: int
    total_embeddings: int
    last_updated: Optional[str]
    size_info: Dict[str, Any]


@dataclass
class DocumentInfo:
    """Information about a document across all databases"""
    id: str
    title: str
    content_preview: str
    source: str
    created_at: str
    in_neo4j: bool
    in_pinecone: bool
    in_chroma: bool
    entity_count: int
    chunk_count: int
    metadata: Dict[str, Any]


class AdminPortal:
    """Main admin portal class"""
    
    def __init__(self):
        self.config = get_config()
        self.neo4j_manager = None
        self.vector_manager = None
        self.chroma_manager = None
        
    async def initialize(self):
        """Initialize database connections"""
        print("🔌 Initializing database connections...")
        
        try:
            # Neo4j connection
            self.neo4j_manager = get_neo4j_manager()
            self.neo4j_manager.connect()  # Explicitly connect
            print("✅ Neo4j connection established")
        except Exception as e:
            print(f"❌ Neo4j connection failed: {e}")
            self.neo4j_manager = None
        
        try:
            # Pinecone connection
            self.vector_manager = get_vector_manager()
            print("✅ Pinecone connection established")
        except Exception as e:
            print(f"❌ Pinecone connection failed: {e}")
        
        try:
            # Chroma connection (if configured)
            # This would be implemented if Chroma is set up as fallback
            print("ℹ️ Chroma fallback not configured")
        except Exception as e:
            print(f"❌ Chroma connection failed: {e}")
    
    async def get_database_statistics(self) -> List[DatabaseStats]:
        """Get comprehensive statistics for all databases"""
        stats = []
        
        # Neo4j Statistics
        if self.neo4j_manager:
            try:
                neo4j_stats = await self._get_neo4j_stats()
                stats.append(neo4j_stats)
            except Exception as e:
                print(f"Error getting Neo4j stats: {e}")
        
        # Pinecone Statistics
        if self.vector_manager:
            try:
                pinecone_stats = await self._get_pinecone_stats()
                stats.append(pinecone_stats)
            except Exception as e:
                print(f"Error getting Pinecone stats: {e}")
        
        return stats
    
    async def _get_neo4j_stats(self) -> DatabaseStats:
        """Get Neo4j database statistics"""
        # Document count
        doc_query = "MATCH (d:Document) RETURN count(d) as count"
        doc_result = self.neo4j_manager.execute_query(doc_query)
        doc_count = doc_result[0]["count"] if doc_result else 0
        
        # Entity count
        entity_query = "MATCH (e:Entity) RETURN count(e) as count"
        entity_result = self.neo4j_manager.execute_query(entity_query)
        entity_count = entity_result[0]["count"] if entity_result else 0
        
        # Relationship count
        rel_query = "MATCH ()-[r]->() RETURN count(r) as count"
        rel_result = self.neo4j_manager.execute_query(rel_query)
        rel_count = rel_result[0]["count"] if rel_result else 0
        
        # Last updated document
        last_updated_query = """
        MATCH (d:Document) 
        RETURN d.updated_at as last_updated 
        ORDER BY d.updated_at DESC 
        LIMIT 1
        """
        last_updated_result = self.neo4j_manager.execute_query(last_updated_query)
        last_updated = last_updated_result[0]["last_updated"] if last_updated_result else None
        
        return DatabaseStats(
            name="Neo4j Graph Database",
            status="Connected",
            total_documents=doc_count,
            total_entities=entity_count,
            total_relationships=rel_count,
            total_embeddings=0,
            last_updated=last_updated,
            size_info={
                "documents": doc_count,
                "entities": entity_count,
                "relationships": rel_count
            }
        )
    
    async def _get_pinecone_stats(self) -> DatabaseStats:
        """Get Pinecone database statistics"""
        try:
            # Get index stats
            if hasattr(self.vector_manager, 'get_index_stats'):
                stats = self.vector_manager.get_index_stats()
                vector_count = stats.get('total_vectors', 0)
            else:
                # Fallback method
                vector_count = 0
            
            # Try to get document count by querying
            try:
                results = self.vector_manager.query_collection(
                    collection_name="documents",
                    query_text="test",
                    n_results=1
                )
                # This is an approximation - Pinecone doesn't give exact counts easily
                doc_count = vector_count  # Each vector is typically a document chunk
            except:
                doc_count = 0
            
            return DatabaseStats(
                name="Pinecone Vector Database",
                status="Connected",
                total_documents=doc_count,
                total_entities=0,
                total_relationships=0,
                total_embeddings=vector_count,
                last_updated=datetime.now().isoformat(),
                size_info={
                    "vectors": vector_count,
                    "dimensions": 384,  # Based on all-MiniLM-L6-v2
                    "collections": ["documents", "entities"]
                }
            )
        except Exception as e:
            return DatabaseStats(
                name="Pinecone Vector Database",
                status=f"Error: {e}",
                total_documents=0,
                total_entities=0,
                total_relationships=0,
                total_embeddings=0,
                last_updated=None,
                size_info={}
            )
    
    async def get_document_inventory(self, limit: int = 50) -> List[DocumentInfo]:
        """Get comprehensive document inventory across all databases"""
        documents = []
        
        if not self.neo4j_manager:
            print("❌ Neo4j not available for document inventory")
            return documents
        
        # Get documents from Neo4j
        doc_query = """
        MATCH (d:Document)
        OPTIONAL MATCH (e:Entity)-[:MENTIONED_IN]->(d)
        RETURN d.id as id, d.title as title, d.content as content, 
               d.source as source, d.created_at as created_at,
               count(e) as entity_count
        ORDER BY d.created_at DESC
        LIMIT $limit
        """
        
        neo4j_docs = self.neo4j_manager.execute_query(doc_query, {"limit": limit})
        
        for doc in neo4j_docs:
            doc_id = doc["id"]
            
            # Check if document exists in Pinecone
            in_pinecone = await self._check_document_in_pinecone(doc_id)
            chunk_count = await self._get_pinecone_chunk_count(doc_id)
            
            # Check if document exists in Chroma (if configured)
            in_chroma = False  # Would implement if Chroma is configured
            
            documents.append(DocumentInfo(
                id=doc_id,
                title=doc["title"] or "Untitled",
                content_preview=doc["content"][:200] + "..." if doc["content"] and len(doc["content"]) > 200 else doc["content"] or "",
                source=doc["source"] or "Unknown",
                created_at=doc["created_at"] or "Unknown",
                in_neo4j=True,
                in_pinecone=in_pinecone,
                in_chroma=in_chroma,
                entity_count=doc["entity_count"] or 0,
                chunk_count=chunk_count,
                metadata={}
            ))
        
        return documents
    
    async def _check_document_in_pinecone(self, doc_id: str) -> bool:
        """Check if a document exists in Pinecone"""
        try:
            results = self.vector_manager.query_collection(
                collection_name="documents",
                query_text="test",
                n_results=1,
                where={"document_id": doc_id}
            )
            return bool(results.get("ids") and results["ids"][0])
        except:
            return False
    
    async def _get_pinecone_chunk_count(self, doc_id: str) -> int:
        """Get number of chunks for a document in Pinecone"""
        try:
            results = self.vector_manager.query_collection(
                collection_name="documents",
                query_text="test",
                n_results=100,  # Get more to count chunks
                where={"document_id": doc_id}
            )
            return len(results.get("ids", [[]])[0]) if results.get("ids") else 0
        except:
            return 0
    
    async def get_entity_analysis(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get entity analysis from Neo4j"""
        if not self.neo4j_manager:
            return []
        
        entity_query = """
        MATCH (e:Entity)
        OPTIONAL MATCH (e)-[r]->(d:Document)
        RETURN e.name as name, e.type as type, e.description as description,
               count(d) as document_count, collect(DISTINCT d.title)[0..3] as sample_documents
        ORDER BY document_count DESC
        LIMIT $limit
        """
        
        entities = self.neo4j_manager.execute_query(entity_query, {"limit": limit})
        
        return [
            {
                "name": entity["name"],
                "type": entity["type"],
                "description": entity["description"] or "No description",
                "document_count": entity["document_count"],
                "sample_documents": entity["sample_documents"] or []
            }
            for entity in entities
        ]
    
    async def search_documents(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search documents across databases"""
        results = []
        
        # Search in Neo4j
        if self.neo4j_manager:
            neo4j_query = """
            MATCH (d:Document)
            WHERE d.title CONTAINS $query OR d.content CONTAINS $query
            RETURN d.id as id, d.title as title, d.content as content,
                   d.source as source, d.created_at as created_at
            ORDER BY d.created_at DESC
            LIMIT $limit
            """
            
            neo4j_results = self.neo4j_manager.execute_query(neo4j_query, {
                "query": query,
                "limit": limit
            })
            
            for doc in neo4j_results:
                results.append({
                    "source": "Neo4j",
                    "id": doc["id"],
                    "title": doc["title"],
                    "content_preview": doc["content"][:300] + "..." if doc["content"] and len(doc["content"]) > 300 else doc["content"],
                    "created_at": doc["created_at"]
                })
        
        # Search in Pinecone
        if self.vector_manager:
            try:
                vector_results = self.vector_manager.query_collection(
                    collection_name="documents",
                    query_text=query,
                    n_results=limit
                )
                
                if vector_results.get("documents") and vector_results["documents"][0]:
                    for i, (content, metadata, distance) in enumerate(zip(
                        vector_results["documents"][0],
                        vector_results.get("metadatas", [[]])[0] or [],
                        vector_results.get("distances", [[]])[0] or []
                    )):
                        results.append({
                            "source": "Pinecone",
                            "id": metadata.get("chunk_id", f"chunk_{i}"),
                            "title": f"Chunk from {metadata.get('document_id', 'Unknown')}",
                            "content_preview": content[:300] + "..." if len(content) > 300 else content,
                            "similarity": 1 - distance if distance else 0,
                            "metadata": metadata
                        })
            except Exception as e:
                print(f"Error searching Pinecone: {e}")
        
        return results
    
    def print_dashboard(self, stats: List[DatabaseStats], documents: List[DocumentInfo], entities: List[Dict[str, Any]]):
        """Print a comprehensive dashboard"""
        print("\n" + "="*80)
        print("🏛️  GRAPH-ENHANCED AGENTIC RAG - ADMIN PORTAL")
        print("="*80)
        
        # Database Statistics
        print("\n📊 DATABASE STATISTICS")
        print("-" * 50)
        for stat in stats:
            print(f"\n🗄️  {stat.name}")
            print(f"   Status: {stat.status}")
            print(f"   Documents: {stat.total_documents:,}")
            print(f"   Entities: {stat.total_entities:,}")
            print(f"   Relationships: {stat.total_relationships:,}")
            print(f"   Embeddings: {stat.total_embeddings:,}")
            if stat.last_updated:
                print(f"   Last Updated: {stat.last_updated}")
        
        # Document Inventory
        print(f"\n📚 DOCUMENT INVENTORY (Top {len(documents)})")
        print("-" * 50)
        for doc in documents[:10]:  # Show top 10
            status_icons = []
            if doc.in_neo4j:
                status_icons.append("🔗")
            if doc.in_pinecone:
                status_icons.append("🔍")
            if doc.in_chroma:
                status_icons.append("💾")
            
            print(f"\n📄 {doc.title}")
            print(f"   ID: {doc.id}")
            print(f"   Status: {''.join(status_icons)} Neo4j: {doc.in_neo4j}, Pinecone: {doc.in_pinecone}")
            print(f"   Entities: {doc.entity_count}, Chunks: {doc.chunk_count}")
            print(f"   Source: {doc.source}")
            print(f"   Preview: {doc.content_preview}")
        
        # Entity Analysis
        print(f"\n🏷️  ENTITY ANALYSIS (Top {len(entities)})")
        print("-" * 50)
        for entity in entities[:10]:  # Show top 10
            print(f"\n🔖 {entity['name']} ({entity['type']})")
            print(f"   Documents: {entity['document_count']}")
            print(f"   Description: {entity['description']}")
            if entity['sample_documents']:
                print(f"   Found in: {', '.join(entity['sample_documents'][:2])}...")


async def main():
    """Main admin portal function"""
    portal = AdminPortal()
    
    print("🚀 Starting Admin Portal...")
    await portal.initialize()
    
    while True:
        print("\n" + "="*60)
        print("🏛️  ADMIN PORTAL MENU")
        print("="*60)
        print("1. 📊 View Database Statistics")
        print("2. 📚 Document Inventory")
        print("3. 🏷️  Entity Analysis")
        print("4. 🔍 Search Documents")
        print("5. 📋 Full Dashboard")
        print("6. 🚪 Exit")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            print("\n📊 Getting database statistics...")
            stats = await portal.get_database_statistics()
            for stat in stats:
                print(f"\n🗄️  {stat.name}: {stat.status}")
                print(f"   📄 Documents: {stat.total_documents:,}")
                print(f"   🏷️  Entities: {stat.total_entities:,}")
                print(f"   🔗 Relationships: {stat.total_relationships:,}")
                print(f"   🔍 Embeddings: {stat.total_embeddings:,}")
        
        elif choice == "2":
            limit = int(input("Number of documents to show (default 20): ") or "20")
            print(f"\n📚 Getting document inventory (limit: {limit})...")
            documents = await portal.get_document_inventory(limit)
            
            for doc in documents:
                print(f"\n📄 {doc.title}")
                print(f"   🆔 ID: {doc.id}")
                print(f"   📍 Databases: Neo4j: {doc.in_neo4j}, Pinecone: {doc.in_pinecone}")
                print(f"   📊 Stats: {doc.entity_count} entities, {doc.chunk_count} chunks")
                print(f"   📝 Preview: {doc.content_preview}")
        
        elif choice == "3":
            limit = int(input("Number of entities to show (default 20): ") or "20")
            print(f"\n🏷️  Getting entity analysis (limit: {limit})...")
            entities = await portal.get_entity_analysis(limit)
            
            for entity in entities:
                print(f"\n🔖 {entity['name']} ({entity['type']})")
                print(f"   📄 Documents: {entity['document_count']}")
                print(f"   📝 Description: {entity['description']}")
                if entity['sample_documents']:
                    print(f"   📚 Found in: {', '.join(entity['sample_documents'])}")
        
        elif choice == "4":
            query = input("Enter search query: ").strip()
            if query:
                limit = int(input("Number of results (default 10): ") or "10")
                print(f"\n🔍 Searching for '{query}'...")
                results = await portal.search_documents(query, limit)
                
                for result in results:
                    print(f"\n📄 {result['title']} ({result['source']})")
                    print(f"   🆔 ID: {result['id']}")
                    if 'similarity' in result:
                        print(f"   📊 Similarity: {result['similarity']:.2%}")
                    print(f"   📝 Preview: {result['content_preview']}")
        
        elif choice == "5":
            print("\n📋 Generating full dashboard...")
            stats = await portal.get_database_statistics()
            documents = await portal.get_document_inventory(20)
            entities = await portal.get_entity_analysis(20)
            portal.print_dashboard(stats, documents, entities)
        
        elif choice == "6":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("❌ Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Admin Portal closed by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()