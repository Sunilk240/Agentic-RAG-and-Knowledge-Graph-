"""
Example usage of the Vector Retrieval Agent.

This script demonstrates how to use the Vector Retrieval Agent for:
- Embedding generation
- Document storage and retrieval
- Semantic similarity search
- Hybrid search capabilities
"""

import asyncio
import tempfile
import shutil
from datetime import datetime
from typing import List

from src.agents.vector_retrieval import VectorRetrievalAgent, EmbeddingGenerationService
from src.core.vector_models import DocumentEmbedding
from src.core.interfaces import AgentMessage, MessageType


async def demonstrate_embedding_service():
    """Demonstrate the embedding generation service."""
    print("=== Embedding Generation Service Demo ===")
    
    # Initialize embedding service
    embedding_service = EmbeddingGenerationService(
        model_name="all-MiniLM-L6-v2",
        cache_size=100
    )
    
    # Generate single embedding
    text = "This is a sample text for embedding generation."
    print(f"Generating embedding for: '{text}'")
    
    embedding = await embedding_service.generate_embedding(text)
    print(f"Generated embedding with dimension: {embedding.dimension}")
    print(f"Model used: {embedding.model_name}")
    print(f"First 5 values: {embedding.to_list()[:5]}")
    
    # Generate batch embeddings
    texts = [
        "First document about machine learning and artificial intelligence.",
        "Second document discussing natural language processing techniques.",
        "Third document covering computer vision and image recognition.",
        "Fourth document about deep learning and neural networks.",
        "Fifth document on data science and statistical analysis."
    ]
    
    print(f"\nGenerating batch embeddings for {len(texts)} texts...")
    batch_embeddings = await embedding_service.generate_embeddings_batch(texts)
    print(f"Generated {len(batch_embeddings)} embeddings in batch")
    
    # Test caching
    print("\nTesting embedding cache...")
    cached_embedding = await embedding_service.generate_embedding(text)
    print(f"Cache hit - same embedding retrieved: {embedding.created_at == cached_embedding.created_at}")
    
    # Show cache statistics
    cache_stats = embedding_service.get_cache_stats()
    print(f"Cache statistics: {cache_stats}")
    
    return batch_embeddings


async def create_sample_documents(embeddings: List) -> List[DocumentEmbedding]:
    """Create sample documents with embeddings."""
    documents = []
    
    contents = [
        "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data.",
        "Natural language processing enables computers to understand, interpret, and generate human language.",
        "Computer vision allows machines to interpret and understand visual information from the world.",
        "Deep learning uses neural networks with multiple layers to model complex patterns in data.",
        "Data science combines statistics, programming, and domain expertise to extract insights from data."
    ]
    
    titles = [
        "Introduction to Machine Learning",
        "Natural Language Processing Fundamentals",
        "Computer Vision Basics",
        "Deep Learning Overview",
        "Data Science Principles"
    ]
    
    topics = ["ml", "nlp", "cv", "dl", "ds"]
    
    for i, (content, title, topic, embedding) in enumerate(zip(contents, titles, topics, embeddings)):
        doc = DocumentEmbedding(
            content=content,
            title=title,
            embedding=embedding.to_list(),
            embedding_model="all-MiniLM-L6-v2",
            embedding_dimension=embedding.dimension,
            metadata={
                "topic": topic,
                "category": "ai_ml",
                "difficulty": "beginner",
                "author": f"Author {i+1}"
            },
            source=f"textbook_chapter_{i+1}.txt"
        )
        documents.append(doc)
    
    return documents


async def demonstrate_vector_agent():
    """Demonstrate the Vector Retrieval Agent functionality."""
    print("\n=== Vector Retrieval Agent Demo ===")
    
    # Create temporary directory for Chroma
    temp_dir = tempfile.mkdtemp()
    
    try:
        # Initialize vector agent
        vector_agent = VectorRetrievalAgent(
            agent_id="demo_vector_agent",
            model_name="all-MiniLM-L6-v2",
            chroma_persist_directory=temp_dir,
            collection_name="demo_collection"
        )
        
        print("Vector Retrieval Agent initialized")
        
        # Generate embeddings and create documents
        embedding_service = EmbeddingGenerationService()
        texts = [
            "Machine learning is a subset of artificial intelligence that focuses on algorithms that can learn from data.",
            "Natural language processing enables computers to understand, interpret, and generate human language.",
            "Computer vision allows machines to interpret and understand visual information from the world.",
            "Deep learning uses neural networks with multiple layers to model complex patterns in data.",
            "Data science combines statistics, programming, and domain expertise to extract insights from data."
        ]
        
        embeddings = await embedding_service.generate_embeddings_batch(texts)
        documents = await create_sample_documents(embeddings)
        
        # Add documents to vector database
        print(f"\nAdding {len(documents)} documents to vector database...")
        await vector_agent.add_documents(documents)
        
        doc_count = await vector_agent.get_document_count()
        print(f"Total documents in database: {doc_count}")
        
        # Demonstrate similarity search
        print("\n--- Similarity Search Demo ---")
        query = "algorithms that learn from data"
        print(f"Query: '{query}'")
        
        result = await vector_agent.similarity_search(query, k=3)
        print(f"Found {len(result.documents)} similar documents:")
        
        for i, (doc, similarity) in enumerate(zip(result.documents, result.similarities)):
            print(f"{i+1}. Title: {doc.metadata.get('title', 'N/A')}")
            print(f"   Similarity: {similarity:.4f}")
            print(f"   Content: {doc.content[:100]}...")
            print()
        
        # Demonstrate filtered search
        print("--- Filtered Search Demo ---")
        query = "computer understanding"
        filters = {"topic": "nlp"}
        print(f"Query: '{query}' with filter: {filters}")
        
        filtered_result = await vector_agent.similarity_search(query, k=5, filters=filters)
        print(f"Found {len(filtered_result.documents)} filtered results:")
        
        for i, (doc, similarity) in enumerate(zip(filtered_result.documents, filtered_result.similarities)):
            print(f"{i+1}. Title: {doc.metadata.get('title', 'N/A')}")
            print(f"   Topic: {doc.metadata.get('topic', 'N/A')}")
            print(f"   Similarity: {similarity:.4f}")
            print()
        
        # Demonstrate hybrid search
        print("--- Hybrid Search Demo ---")
        query = "neural networks deep learning"
        print(f"Query: '{query}'")
        
        hybrid_result = await vector_agent.hybrid_search(query, semantic_weight=0.7, k=3)
        print(f"Found {len(hybrid_result.documents)} hybrid search results:")
        
        for i, (doc, score) in enumerate(zip(hybrid_result.documents, hybrid_result.similarities)):
            print(f"{i+1}. Title: {doc.metadata.get('title', 'N/A')}")
            print(f"   Hybrid Score: {score:.4f}")
            print(f"   Content: {doc.content[:100]}...")
            print()
        
        # Demonstrate agent messaging
        print("--- Agent Messaging Demo ---")
        message = AgentMessage(
            agent_id="demo_coordinator",
            message_type=MessageType.VECTOR_SEARCH,
            payload={
                "query": "artificial intelligence machine learning",
                "k": 2,
                "search_type": "hybrid",
                "semantic_weight": 0.8
            },
            correlation_id="demo_correlation_123"
        )
        
        print(f"Sending message: {message.message_type.value}")
        response = await vector_agent.process_message(message)
        
        if response:
            print(f"Received response: {response.message_type.value}")
            print(f"Correlation ID: {response.correlation_id}")
            print(f"Found {len(response.payload['documents'])} documents via messaging")
        
        # Show agent information
        print("\n--- Agent Information ---")
        agent_info = vector_agent.get_agent_info()
        print(f"Agent ID: {agent_info['agent_id']}")
        print(f"Agent Type: {agent_info['agent_type']}")
        print(f"Model: {agent_info['model_info']['model_name']}")
        print(f"Document Count: {agent_info['document_count']}")
        print(f"Cache Size: {agent_info['cache_stats']['cache_size']}")
        
        # Health check
        print("\n--- Health Check ---")
        health = await vector_agent.health_check()
        print(f"Overall Status: {health['status']}")
        print(f"Embedding Service: {health['checks']['embedding_service']['status']}")
        print(f"Vector Database: {health['checks']['vector_database']['status']}")
        
        # Demonstrate document update
        print("\n--- Document Update Demo ---")
        updated_doc = documents[0]
        updated_doc.content = "Updated: Machine learning and AI are transforming how we process and understand data."
        updated_doc.title = "Updated: ML and AI Overview"
        
        await vector_agent.update_document(updated_doc)
        print("Document updated successfully")
        
        # Search for updated content
        update_result = await vector_agent.similarity_search("transforming data processing", k=1)
        if update_result.documents:
            print(f"Found updated document: {update_result.documents[0].metadata.get('title')}")
        
        # Demonstrate document deletion
        print("\n--- Document Deletion Demo ---")
        initial_count = await vector_agent.get_document_count()
        await vector_agent.delete_document(documents[1].id)
        final_count = await vector_agent.get_document_count()
        
        print(f"Documents before deletion: {initial_count}")
        print(f"Documents after deletion: {final_count}")
        print(f"Successfully deleted 1 document")
        
    finally:
        # Clean up temporary directory
        shutil.rmtree(temp_dir)
        print(f"\nCleaned up temporary directory: {temp_dir}")


async def demonstrate_advanced_features():
    """Demonstrate advanced features of the vector retrieval system."""
    print("\n=== Advanced Features Demo ===")
    
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    
    try:
        vector_agent = VectorRetrievalAgent(
            agent_id="advanced_demo_agent",
            chroma_persist_directory=temp_dir,
            collection_name="advanced_collection"
        )
        
        # Create documents with different characteristics
        diverse_documents = []
        
        # Short document
        short_doc = DocumentEmbedding(
            content="AI is powerful.",
            title="Short AI Note",
            embedding=[0.1] * 384,  # Mock embedding
            embedding_model="all-MiniLM-L6-v2",
            embedding_dimension=384,
            metadata={"length": "short", "category": "note"}
        )
        diverse_documents.append(short_doc)
        
        # Long document
        long_content = " ".join([
            "Artificial intelligence represents one of the most significant technological advances of our time.",
            "It encompasses machine learning, deep learning, natural language processing, computer vision,",
            "and many other subfields that are revolutionizing industries and changing how we interact with technology.",
            "The applications are vast, from autonomous vehicles to medical diagnosis, from financial trading",
            "to creative content generation. As AI continues to evolve, we must consider both its tremendous",
            "potential and the ethical implications of its widespread adoption."
        ])
        
        long_doc = DocumentEmbedding(
            content=long_content,
            title="Comprehensive AI Overview",
            embedding=[0.2] * 384,  # Mock embedding
            embedding_model="all-MiniLM-L6-v2",
            embedding_dimension=384,
            metadata={"length": "long", "category": "article"}
        )
        diverse_documents.append(long_doc)
        
        # Document with exact phrase match
        exact_doc = DocumentEmbedding(
            content="This document contains the exact phrase we will search for: machine learning algorithms.",
            title="Exact Match Document",
            embedding=[0.3] * 384,  # Mock embedding
            embedding_model="all-MiniLM-L6-v2",
            embedding_dimension=384,
            metadata={"type": "exact_match", "category": "technical"}
        )
        diverse_documents.append(exact_doc)
        
        await vector_agent.add_documents(diverse_documents)
        
        # Demonstrate re-ranking
        print("--- Re-ranking Demo ---")
        query = "machine learning algorithms"
        
        # First, get results without re-ranking
        basic_result = await vector_agent.similarity_search(query, k=3)
        print(f"Basic search results for '{query}':")
        for i, (doc, sim) in enumerate(zip(basic_result.documents, basic_result.similarities)):
            print(f"{i+1}. {doc.metadata.get('title', 'N/A')} (sim: {sim:.4f})")
        
        # Now demonstrate re-ranking
        reranked_docs, reranked_scores = await vector_agent.rerank_results(
            basic_result.documents, 
            basic_result.similarities, 
            query
        )
        
        print(f"\nRe-ranked results:")
        for i, (doc, score) in enumerate(zip(reranked_docs, reranked_scores)):
            print(f"{i+1}. {doc.metadata.get('title', 'N/A')} (enhanced score: {score:.4f})")
        
        # Demonstrate different semantic weights in hybrid search
        print("\n--- Semantic Weight Comparison ---")
        query = "AI technology applications"
        
        for weight in [0.3, 0.5, 0.7, 0.9]:
            result = await vector_agent.hybrid_search(query, semantic_weight=weight, k=2)
            print(f"Semantic weight {weight}: {len(result.documents)} results")
            if result.documents:
                top_doc = result.documents[0]
                print(f"  Top result: {top_doc.metadata.get('title', 'N/A')} (score: {result.similarities[0]:.4f})")
        
    finally:
        shutil.rmtree(temp_dir)
        print(f"\nCleaned up temporary directory: {temp_dir}")


async def main():
    """Run all demonstrations."""
    print("Vector Retrieval Agent Demonstration")
    print("=" * 50)
    
    try:
        # Demonstrate embedding service
        embeddings = await demonstrate_embedding_service()
        
        # Demonstrate vector agent
        await demonstrate_vector_agent()
        
        # Demonstrate advanced features
        await demonstrate_advanced_features()
        
        print("\n" + "=" * 50)
        print("All demonstrations completed successfully!")
        
    except Exception as e:
        print(f"\nError during demonstration: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())