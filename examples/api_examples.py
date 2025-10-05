"""
Example API usage for the Graph-Enhanced Agentic RAG system.

This module demonstrates how to interact with the API endpoints
for various use cases and query types.
"""

import requests
import json
import time
from typing import Dict, Any, List


class RAGAPIClient:
    """Client for interacting with the Graph-Enhanced Agentic RAG API."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """Initialize the API client.
        
        Args:
            base_url: Base URL of the API server
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """Check system health status."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def query(
        self, 
        question: str, 
        max_results: int = 10,
        include_reasoning: bool = True,
        strategy: str = None
    ) -> Dict[str, Any]:
        """Submit a query to the RAG system.
        
        Args:
            question: The question to ask
            max_results: Maximum number of results to return
            include_reasoning: Whether to include reasoning path
            strategy: Specific retrieval strategy ('vector_only', 'graph_only', 'hybrid')
            
        Returns:
            Query response with answer, sources, and metadata
        """
        payload = {
            "query": question,
            "max_results": max_results,
            "include_reasoning": include_reasoning
        }
        
        if strategy:
            payload["strategy"] = strategy
        
        response = self.session.post(f"{self.base_url}/query", json=payload)
        response.raise_for_status()
        return response.json()
    
    def upload_document(
        self,
        title: str,
        content: str,
        source: str = None,
        domain: str = "general",
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Upload a document for ingestion.
        
        Args:
            title: Document title
            content: Document content
            source: Source URL or reference
            domain: Knowledge domain
            metadata: Additional metadata
            
        Returns:
            Upload response with document ID and processing info
        """
        payload = {
            "title": title,
            "content": content,
            "domain": domain,
            "metadata": metadata or {}
        }
        
        if source:
            payload["source"] = source
        
        response = self.session.post(f"{self.base_url}/documents/upload", json=payload)
        response.raise_for_status()
        return response.json()
    
    def upload_file(
        self,
        file_path: str,
        title: str,
        source: str = None,
        domain: str = "general"
    ) -> Dict[str, Any]:
        """Upload a file for ingestion.
        
        Args:
            file_path: Path to the file to upload
            title: Document title
            source: Source URL or reference
            domain: Knowledge domain
            
        Returns:
            Upload response with document ID and processing info
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            data = {
                'title': title,
                'domain': domain
            }
            
            if source:
                data['source'] = source
            
            response = self.session.post(
                f"{self.base_url}/documents/upload-file",
                files=files,
                data=data
            )
            response.raise_for_status()
            return response.json()
    
    def get_agent_status(self) -> Dict[str, Any]:
        """Get status of all agents."""
        response = self.session.get(f"{self.base_url}/agents/status")
        response.raise_for_status()
        return response.json()
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        response = self.session.get(f"{self.base_url}/system/status")
        response.raise_for_status()
        return response.json()


def example_basic_queries():
    """Demonstrate basic query functionality."""
    print("=== Basic Query Examples ===")
    
    client = RAGAPIClient()
    
    # Check system health first
    try:
        health = client.health_check()
        print(f"System Status: {health['status']}")
        print()
    except requests.exceptions.RequestException as e:
        print(f"Failed to connect to API: {e}")
        return
    
    # Example queries of different types
    queries = [
        {
            "question": "What is machine learning?",
            "description": "Simple factual query (should use vector search)",
            "strategy": "vector_only"
        },
        {
            "question": "How are neural networks related to deep learning?",
            "description": "Relationship query (should use graph traversal)",
            "strategy": "graph_only"
        },
        {
            "question": "What are the applications of machine learning in healthcare and how do they relate to AI ethics?",
            "description": "Complex multi-hop query (should use hybrid approach)",
            "strategy": "hybrid"
        }
    ]
    
    for i, query_info in enumerate(queries, 1):
        print(f"Query {i}: {query_info['description']}")
        print(f"Question: {query_info['question']}")
        
        try:
            start_time = time.time()
            result = client.query(
                question=query_info['question'],
                strategy=query_info['strategy'],
                max_results=5,
                include_reasoning=True
            )
            end_time = time.time()
            
            print(f"Strategy Used: {result.get('strategy_used', 'N/A')}")
            print(f"Processing Time: {result.get('processing_time', 0):.2f}s")
            print(f"Confidence Score: {result.get('confidence_score', 0):.2%}")
            print(f"Sources Found: {len(result.get('sources', []))}")
            print(f"Response Preview: {result['response'][:200]}...")
            
            if result.get('reasoning_path'):
                print(f"Reasoning: {result['reasoning_path'][:100]}...")
            
        except requests.exceptions.RequestException as e:
            print(f"Query failed: {e}")
        
        print("-" * 50)


def example_document_upload():
    """Demonstrate document upload functionality."""
    print("=== Document Upload Examples ===")
    
    client = RAGAPIClient()
    
    # Example documents
    documents = [
        {
            "title": "Introduction to Neural Networks",
            "content": """
            Neural networks are computing systems inspired by biological neural networks.
            They consist of interconnected nodes (neurons) that process information using
            a connectionist approach to computation. The basic structure includes:
            
            1. Input Layer: Receives input data
            2. Hidden Layers: Process information through weighted connections
            3. Output Layer: Produces final results
            
            Key concepts include:
            - Weights and biases that determine connection strength
            - Activation functions that introduce non-linearity
            - Backpropagation for training the network
            - Gradient descent for optimization
            
            Applications include image recognition, natural language processing,
            and predictive modeling.
            """,
            "source": "https://example.com/neural-networks-intro",
            "domain": "technical",
            "metadata": {
                "author": "AI Research Team",
                "tags": ["neural networks", "deep learning", "AI"],
                "difficulty": "intermediate"
            }
        },
        {
            "title": "Machine Learning Ethics Guidelines",
            "content": """
            Ethical considerations in machine learning are crucial for responsible AI development.
            Key principles include:
            
            1. Fairness: Ensuring algorithms don't discriminate against protected groups
            2. Transparency: Making AI decisions explainable and interpretable
            3. Privacy: Protecting user data and maintaining confidentiality
            4. Accountability: Establishing clear responsibility for AI decisions
            5. Beneficence: Ensuring AI systems benefit society
            
            Common ethical challenges:
            - Bias in training data leading to discriminatory outcomes
            - Lack of transparency in complex models (black box problem)
            - Privacy concerns with data collection and usage
            - Job displacement due to automation
            - Potential misuse of AI technologies
            
            Best practices include diverse teams, bias testing, regular audits,
            and stakeholder engagement throughout development.
            """,
            "source": "https://example.com/ml-ethics",
            "domain": "research",
            "metadata": {
                "author": "Ethics Committee",
                "tags": ["ethics", "AI", "fairness", "transparency"],
                "publication_date": "2024-01-15"
            }
        }
    ]
    
    uploaded_docs = []
    
    for i, doc in enumerate(documents, 1):
        print(f"Uploading Document {i}: {doc['title']}")
        
        try:
            result = client.upload_document(
                title=doc['title'],
                content=doc['content'],
                source=doc['source'],
                domain=doc['domain'],
                metadata=doc['metadata']
            )
            
            uploaded_docs.append(result)
            
            print(f"✓ Upload successful!")
            print(f"  Document ID: {result['document_id']}")
            print(f"  Entities Extracted: {result.get('entities_extracted', 'N/A')}")
            print(f"  Relationships Created: {result.get('relationships_created', 'N/A')}")
            print(f"  Processing Time: {result.get('processing_time', 0):.2f}s")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Upload failed: {e}")
        
        print("-" * 50)
    
    return uploaded_docs


def example_system_monitoring():
    """Demonstrate system monitoring functionality."""
    print("=== System Monitoring Examples ===")
    
    client = RAGAPIClient()
    
    try:
        # Get comprehensive system status
        print("System Status:")
        system_status = client.get_system_status()
        
        print(f"  API Status: {system_status['api_status']}")
        print(f"  Uptime: {system_status['uptime']:.2f} seconds")
        print(f"  Environment: {system_status['configuration']['environment']}")
        
        # Database status
        print("\nDatabase Status:")
        for db_name, db_info in system_status['databases'].items():
            print(f"  {db_name}: {db_info['status']}")
        
        # Metrics
        print("\nSystem Metrics:")
        metrics = system_status['metrics']
        print(f"  Total Queries: {metrics['total_queries']}")
        print(f"  Total Documents: {metrics['total_documents']}")
        
        print("-" * 50)
        
        # Get agent status
        print("Agent Status:")
        agent_status = client.get_agent_status()
        
        print(f"  Total Agents: {agent_status['total_agents']}")
        print(f"  Healthy Agents: {agent_status['healthy_agents']}")
        
        for agent_name, agent_info in agent_status['agents'].items():
            print(f"  {agent_name}: {agent_info['status']}")
            print(f"    Description: {agent_info['description']}")
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to get system status: {e}")


def example_advanced_queries():
    """Demonstrate advanced query scenarios."""
    print("=== Advanced Query Examples ===")
    
    client = RAGAPIClient()
    
    # Advanced query scenarios
    scenarios = [
        {
            "name": "Multi-domain Query",
            "question": "How do neural networks apply to healthcare AI and what are the ethical considerations?",
            "strategy": "hybrid",
            "max_results": 15
        },
        {
            "name": "Technical Deep Dive",
            "question": "Explain the mathematical foundations of backpropagation in neural networks",
            "strategy": "vector_only",
            "max_results": 8
        },
        {
            "name": "Relationship Exploration",
            "question": "What are all the connections between machine learning, ethics, and healthcare?",
            "strategy": "graph_only",
            "max_results": 20
        }
    ]
    
    for scenario in scenarios:
        print(f"Scenario: {scenario['name']}")
        print(f"Question: {scenario['question']}")
        
        try:
            result = client.query(
                question=scenario['question'],
                strategy=scenario['strategy'],
                max_results=scenario['max_results'],
                include_reasoning=True
            )
            
            print(f"Strategy: {result.get('strategy_used', 'N/A')}")
            print(f"Entities Found: {len(result.get('entities_found', []))}")
            print(f"Sources: {len(result.get('sources', []))}")
            print(f"Citations: {len(result.get('citations', []))}")
            
            # Show source types
            if result.get('sources'):
                source_types = {}
                for source in result['sources']:
                    source_type = source.get('source_type', 'unknown')
                    source_types[source_type] = source_types.get(source_type, 0) + 1
                
                print(f"Source Types: {dict(source_types)}")
            
            print(f"Response Length: {len(result['response'])} characters")
            
        except requests.exceptions.RequestException as e:
            print(f"Query failed: {e}")
        
        print("-" * 50)


def example_error_handling():
    """Demonstrate error handling scenarios."""
    print("=== Error Handling Examples ===")
    
    client = RAGAPIClient()
    
    # Test various error conditions
    error_scenarios = [
        {
            "name": "Empty Query",
            "action": lambda: client.query("")
        },
        {
            "name": "Invalid Strategy",
            "action": lambda: client.query("test query", strategy="invalid_strategy")
        },
        {
            "name": "Invalid Max Results",
            "action": lambda: client.query("test query", max_results=100)
        },
        {
            "name": "Missing Document Title",
            "action": lambda: client.upload_document("", "content")
        }
    ]
    
    for scenario in error_scenarios:
        print(f"Testing: {scenario['name']}")
        
        try:
            result = scenario['action']()
            print(f"  Unexpected success: {result}")
        except requests.exceptions.HTTPError as e:
            print(f"  ✓ Expected error: HTTP {e.response.status_code}")
            try:
                error_detail = e.response.json()
                print(f"    Error: {error_detail.get('error', 'Unknown')}")
                print(f"    Message: {error_detail.get('message', 'No message')}")
            except:
                print(f"    Raw error: {e.response.text}")
        except Exception as e:
            print(f"  Unexpected error type: {type(e).__name__}: {e}")
        
        print("-" * 30)


def main():
    """Run all example scenarios."""
    print("Graph-Enhanced Agentic RAG API Examples")
    print("=" * 50)
    
    try:
        # Run example scenarios
        example_basic_queries()
        print("\n")
        
        example_document_upload()
        print("\n")
        
        example_system_monitoring()
        print("\n")
        
        example_advanced_queries()
        print("\n")
        
        example_error_handling()
        
        print("\n" + "=" * 50)
        print("All examples completed!")
        
    except KeyboardInterrupt:
        print("\nExamples interrupted by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()