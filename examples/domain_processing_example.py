#!/usr/bin/env python3
"""
Example demonstrating domain-specific processing capabilities.

This example shows how to:
1. Configure different knowledge domains
2. Extract domain-specific entities and relationships
3. Switch between domains
4. Create custom domain configurations
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.domain_processor import (
    DomainType,
    get_domain_manager,
    TechnicalDocumentationExtractor,
    ResearchPapersExtractor
)
from src.core.document_processor import DocumentProcessor
from src.core.domain_config import (
    get_domain_config_manager,
    configure_system_domain
)


def demonstrate_technical_documentation_processing():
    """Demonstrate processing of technical documentation."""
    print("=" * 60)
    print("TECHNICAL DOCUMENTATION PROCESSING")
    print("=" * 60)
    
    # Configure for technical documentation
    configure_system_domain(DomainType.TECHNICAL_DOCUMENTATION)
    
    # Create document processor with domain
    processor = DocumentProcessor(domain_type="technical_documentation")
    
    # Sample technical documentation text
    tech_text = """
    This web application is built with React and TypeScript for the frontend.
    The backend API is implemented using Node.js and Express.js framework.
    Data is stored in a PostgreSQL database with Redis for caching.
    The application uses Docker for containerization and is deployed on AWS.
    
    Key API endpoints include:
    - GET /api/users - Retrieve user list
    - POST /auth/login - User authentication
    - PUT /api/users/{id} - Update user profile
    
    The UserService implements IUserService interface and depends on DatabaseService.
    Configuration is managed through config.json and docker-compose.yml files.
    """
    
    print("Sample Text:")
    print(tech_text.strip())
    print("\n" + "-" * 40)
    
    # Extract entities
    entities = processor.extract_entities(tech_text, use_domain_specific=True)
    
    print(f"\nExtracted Entities ({len(entities)}):")
    for entity in entities:
        extraction_method = entity.properties.get("extraction_method", "general")
        print(f"  • {entity.text} ({entity.label}) - {extraction_method}")
    
    # Extract relationships
    relationships = processor.identify_relationships(tech_text, entities, use_domain_specific=True)
    
    print(f"\nIdentified Relationships ({len(relationships)}):")
    for rel in relationships:
        print(f"  • {rel.source_entity} --[{rel.relationship_type}]--> {rel.target_entity}")
    
    print("\n")


def demonstrate_research_papers_processing():
    """Demonstrate processing of research papers."""
    print("=" * 60)
    print("RESEARCH PAPERS PROCESSING")
    print("=" * 60)
    
    # Configure for research papers
    configure_system_domain(DomainType.RESEARCH_PAPERS)
    
    # Create document processor with domain
    processor = DocumentProcessor(domain_type="research_papers")
    
    # Sample research paper text
    research_text = """
    In this paper, we propose a novel transformer-based architecture for natural language processing.
    Our model, called AdvancedBERT, is trained on the Common Crawl dataset and fine-tuned on GLUE benchmark.
    
    We compare our approach with existing methods including BERT, GPT, and LSTM networks.
    The experimental results show that AdvancedBERT achieves 94.2% accuracy on sentiment classification,
    outperforming BERT by 3.1% and GPT by 2.8%.
    
    The model uses attention mechanisms and is evaluated using standard metrics including F1-score,
    precision, and recall. Training was performed using supervised learning on labeled datasets.
    """
    
    print("Sample Text:")
    print(research_text.strip())
    print("\n" + "-" * 40)
    
    # Extract entities
    entities = processor.extract_entities(research_text, use_domain_specific=True)
    
    print(f"\nExtracted Entities ({len(entities)}):")
    for entity in entities:
        extraction_method = entity.properties.get("extraction_method", "general")
        print(f"  • {entity.text} ({entity.label}) - {extraction_method}")
    
    # Extract relationships
    relationships = processor.identify_relationships(research_text, entities, use_domain_specific=True)
    
    print(f"\nIdentified Relationships ({len(relationships)}):")
    for rel in relationships:
        print(f"  • {rel.source_entity} --[{rel.relationship_type}]--> {rel.target_entity}")
    
    print("\n")


def demonstrate_domain_switching():
    """Demonstrate switching between domains."""
    print("=" * 60)
    print("DOMAIN SWITCHING DEMONSTRATION")
    print("=" * 60)
    
    processor = DocumentProcessor()
    
    # Mixed content that could benefit from different domain processing
    mixed_text = "The React application uses machine learning algorithms implemented in Python."
    
    print("Sample Text:")
    print(mixed_text)
    print("\n" + "-" * 40)
    
    # Process with technical documentation domain
    print("\n1. Processing with TECHNICAL_DOCUMENTATION domain:")
    processor.set_domain("technical_documentation")
    tech_entities = processor.extract_entities(mixed_text, use_domain_specific=True)
    
    for entity in tech_entities:
        extraction_method = entity.properties.get("extraction_method", "general")
        print(f"  • {entity.text} ({entity.label}) - {extraction_method}")
    
    # Process with research papers domain
    print("\n2. Processing with RESEARCH_PAPERS domain:")
    processor.set_domain("research_papers")
    research_entities = processor.extract_entities(mixed_text, use_domain_specific=True)
    
    for entity in research_entities:
        extraction_method = entity.properties.get("extraction_method", "general")
        print(f"  • {entity.text} ({entity.label}) - {extraction_method}")
    
    print("\n")


def demonstrate_custom_domain_creation():
    """Demonstrate creating a custom domain configuration."""
    print("=" * 60)
    print("CUSTOM DOMAIN CREATION")
    print("=" * 60)
    
    config_manager = get_domain_config_manager()
    
    # Define custom entity patterns for a legal documents domain
    entity_patterns = [
        {
            "name": "legal_entity",
            "pattern": r"\b(?:plaintiff|defendant|court|judge|jury|attorney|lawyer|counsel)\b",
            "entity_type": "person",
            "confidence": 0.9,
            "description": "Legal entities and roles"
        },
        {
            "name": "legal_document",
            "pattern": r"\b(?:contract|agreement|statute|regulation|ordinance|brief|motion|complaint)\b",
            "entity_type": "document",
            "confidence": 0.8,
            "description": "Legal documents and instruments"
        },
        {
            "name": "legal_concept",
            "pattern": r"\b(?:liability|negligence|damages|jurisdiction|precedent|due process)\b",
            "entity_type": "concept",
            "confidence": 0.9,
            "description": "Legal concepts and principles"
        }
    ]
    
    # Define custom relationship patterns
    relationship_patterns = [
        {
            "name": "legal_action",
            "pattern": r"(\w+)\s+(?:sues|files against|brings action against)\s+(\w+)",
            "relationship_type": "LEGAL_ACTION",
            "confidence": 0.9,
            "description": "Legal action relationship"
        },
        {
            "name": "legal_precedent",
            "pattern": r"(\w+)\s+(?:cites|references|relies on)\s+(\w+)",
            "relationship_type": "CITES",
            "confidence": 0.8,
            "description": "Legal precedent citation"
        }
    ]
    
    # Create custom domain schema
    custom_schema = config_manager.create_custom_domain(
        domain_name="Legal Documents",
        description="Custom domain for legal document processing",
        entity_patterns=entity_patterns,
        relationship_patterns=relationship_patterns
    )
    
    print("Created custom domain schema:")
    print(f"  Name: {custom_schema.name}")
    print(f"  Description: {custom_schema.description}")
    print(f"  Entity Patterns: {len(custom_schema.entity_patterns)}")
    print(f"  Relationship Patterns: {len(custom_schema.relationship_patterns)}")
    
    # Save the custom schema
    config_path = config_manager.save_schema(custom_schema)
    print(f"  Saved to: {config_path}")
    
    print("\n")


def demonstrate_configuration_management():
    """Demonstrate domain configuration management."""
    print("=" * 60)
    print("CONFIGURATION MANAGEMENT")
    print("=" * 60)
    
    config_manager = get_domain_config_manager()
    
    # List available domains
    domains = config_manager.list_configured_domains()
    print("Available Domains:")
    for domain in domains:
        print(f"  • {domain.value}")
    
    # Get current active domain
    active_domain = config_manager.get_active_domain()
    print(f"\nActive Domain: {active_domain}")
    
    # Export domain configuration
    if domains:
        export_path = f"exported_{domains[0].value}_config.json"
        try:
            config_manager.export_domain_config(domains[0], export_path)
            print(f"\nExported {domains[0].value} configuration to: {export_path}")
        except Exception as e:
            print(f"\nExport failed: {e}")
    
    print("\n")


def main():
    """Run all demonstrations."""
    print("DOMAIN-SPECIFIC PROCESSING DEMONSTRATION")
    print("This example shows the capabilities of the domain-specific processing system.\n")
    
    try:
        demonstrate_technical_documentation_processing()
        demonstrate_research_papers_processing()
        demonstrate_domain_switching()
        demonstrate_custom_domain_creation()
        demonstrate_configuration_management()
        
        print("=" * 60)
        print("DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nKey Features Demonstrated:")
        print("✓ Domain-specific entity extraction")
        print("✓ Domain-specific relationship identification")
        print("✓ Dynamic domain switching")
        print("✓ Custom domain creation")
        print("✓ Configuration management")
        print("\nThe system is now ready for domain-specific document processing!")
        
    except Exception as e:
        print(f"❌ Demonstration failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())