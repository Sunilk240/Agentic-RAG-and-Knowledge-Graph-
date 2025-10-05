# Domain-Specific Processing System

## Overview

The Domain-Specific Processing System enables the Graph-Enhanced Agentic RAG system to adapt its entity extraction and relationship identification capabilities to different knowledge domains. This allows for more accurate and relevant processing of domain-specific content such as technical documentation, research papers, legal documents, and more.

## Key Features

### 1. Pluggable Entity Extraction
- **Domain-specific patterns**: Each domain defines custom regex patterns for extracting relevant entities
- **Configurable confidence scores**: Different patterns can have different confidence levels
- **Extensible entity types**: Support for domain-specific entity classifications
- **Fallback mechanisms**: Graceful degradation to general NLP processing when domain-specific extraction fails

### 2. Domain-Specific Relationship Patterns
- **Custom relationship types**: Define relationships specific to each domain (e.g., "IMPLEMENTS", "TRAINED_ON", "CITES")
- **Pattern-based identification**: Use regex patterns to identify relationships in text
- **Contextual relationships**: Extract relationships based on co-occurrence and linguistic patterns
- **Confidence scoring**: Each relationship pattern includes confidence metrics

### 3. Configurable Schema Mapping
- **JSON-based configuration**: Store domain schemas in easily editable JSON files
- **Runtime reconfiguration**: Switch between domains without system restart
- **Custom domain creation**: Create new domains through code or configuration files
- **Schema validation**: Ensure domain configurations are valid and complete

## Architecture

### Core Components

```
Domain Processing System
├── DomainProcessorManager
│   ├── Domain Registry
│   ├── Schema Management
│   └── Extractor Coordination
├── Domain Extractors
│   ├── TechnicalDocumentationExtractor
│   ├── ResearchPapersExtractor
│   └── Custom Extractors
├── Configuration Management
│   ├── Schema Loading/Saving
│   ├── Domain Switching
│   └── Custom Domain Creation
└── Integration Layer
    ├── DocumentProcessor Integration
    ├── Ingestion Pipeline Integration
    └── Agent System Integration
```

### Domain Schema Structure

Each domain is defined by a `DomainSchema` that includes:

- **Domain Type**: Enumerated domain identifier
- **Entity Patterns**: Regex patterns for extracting domain-specific entities
- **Relationship Patterns**: Patterns for identifying domain-specific relationships
- **Graph Constraints**: Neo4j constraints and indexes for the domain
- **Metadata**: Additional domain information and configuration

## Supported Domains

### 1. Technical Documentation
**Domain Type**: `technical_documentation`

**Entity Types**:
- Programming languages (Python, JavaScript, Java, etc.)
- Frameworks and libraries (React, Django, TensorFlow, etc.)
- Database systems (MySQL, MongoDB, Neo4j, etc.)
- Cloud services (AWS, Docker, Kubernetes, etc.)
- API endpoints (GET /api/users, POST /auth/login, etc.)
- Configuration files (config.json, docker-compose.yml, etc.)

**Relationship Types**:
- `IMPLEMENTS`: Class implements interface
- `EXTENDS`: Class inheritance
- `USES`: Technology usage
- `DEPENDS_ON`: Dependency relationships
- `CONFIGURES`: Configuration relationships

### 2. Research Papers
**Domain Type**: `research_papers`

**Entity Types**:
- Research methods (machine learning, deep learning, etc.)
- Model architectures (BERT, GPT, ResNet, etc.)
- Datasets (ImageNet, MNIST, Common Crawl, etc.)
- Evaluation metrics (accuracy, F1-score, BLEU, etc.)
- Author names (academic format)

**Relationship Types**:
- `ACHIEVES`: Performance achievements
- `TRAINED_ON`: Training dataset relationships
- `OUTPERFORMS`: Performance comparisons
- `CITES`: Citation relationships

## Usage Examples

### Basic Domain Configuration

```python
from src.core.domain_config import configure_system_domain
from src.core.domain_processor import DomainType
from src.core.document_processor import DocumentProcessor

# Configure for technical documentation
configure_system_domain(DomainType.TECHNICAL_DOCUMENTATION)

# Create document processor with domain
processor = DocumentProcessor(domain_type="technical_documentation")

# Process text with domain-specific extraction
text = "This React application uses Node.js and MongoDB."
entities = processor.extract_entities(text, use_domain_specific=True)
relationships = processor.identify_relationships(text, entities, use_domain_specific=True)
```

### Domain Switching

```python
processor = DocumentProcessor()

# Process with technical documentation domain
processor.set_domain("technical_documentation")
tech_entities = processor.extract_entities(text, use_domain_specific=True)

# Switch to research papers domain
processor.set_domain("research_papers")
research_entities = processor.extract_entities(text, use_domain_specific=True)
```

### Custom Domain Creation

```python
from src.core.domain_config import get_domain_config_manager

config_manager = get_domain_config_manager()

# Define custom entity patterns
entity_patterns = [
    {
        "name": "legal_entity",
        "pattern": r"\b(?:plaintiff|defendant|court|judge)\b",
        "entity_type": "person",
        "confidence": 0.9
    }
]

# Define custom relationship patterns
relationship_patterns = [
    {
        "name": "legal_action",
        "pattern": r"(\w+)\s+sues\s+(\w+)",
        "relationship_type": "LEGAL_ACTION",
        "confidence": 0.9
    }
]

# Create custom domain
schema = config_manager.create_custom_domain(
    domain_name="Legal Documents",
    description="Custom domain for legal document processing",
    entity_patterns=entity_patterns,
    relationship_patterns=relationship_patterns
)

# Save the schema
config_manager.save_schema(schema)
```

## Configuration Files

Domain configurations are stored in JSON format in the `config/domains/` directory:

### Example: Technical Documentation Schema

```json
{
  "domain_type": "technical_documentation",
  "name": "Technical Documentation",
  "description": "Schema for technical documentation, API docs, and software development content",
  "entity_types": ["technology", "concept", "document", "organization"],
  "entity_patterns": [
    {
      "name": "programming_language",
      "pattern": "\\b(?:Python|Java|JavaScript|TypeScript)\\b",
      "entity_type": "technology",
      "confidence": 0.9,
      "description": "Programming languages"
    }
  ],
  "relationship_patterns": [
    {
      "name": "implements_interface",
      "pattern": "(\\w+)\\s+implements\\s+(\\w+)",
      "relationship_type": "IMPLEMENTS",
      "confidence": 0.9,
      "source_group": 1,
      "target_group": 2
    }
  ],
  "graph_constraints": [
    "CREATE CONSTRAINT tech_name_unique IF NOT EXISTS FOR (t:Technology) REQUIRE t.name IS UNIQUE"
  ]
}
```

## Integration with Ingestion Pipeline

The domain-specific processing integrates seamlessly with the existing ingestion pipeline:

```python
from src.core.ingestion_pipeline import IngestionConfig, DualStorageIngestionPipeline
from src.core.domain_processor import DomainType

# Configure ingestion with domain-specific processing
config = IngestionConfig(
    domain_type=DomainType.TECHNICAL_DOCUMENTATION,
    use_domain_specific_processing=True
)

# Create pipeline with domain configuration
pipeline = DualStorageIngestionPipeline(
    document_processor=document_processor,
    graph_db_manager=graph_db,
    vector_db_manager=vector_db,
    mapping_service=mapping_service,
    embedding_service=embedding_service,
    config=config
)

# Documents will be processed with domain-specific extraction
result = await pipeline.ingest_document(document)
```

## Performance Considerations

### Entity Deduplication
The system automatically deduplicates entities, prioritizing:
1. Domain-specific extractions over general NLP
2. Higher confidence scores
3. More specific entity types

### Relationship Filtering
Relationships are filtered to remove:
- Duplicate relationships between the same entities
- Low-confidence relationships below threshold
- Relationships between non-existent entities

### Memory Management
- Lazy initialization of domain managers to avoid circular imports
- Efficient regex compilation and caching
- Minimal memory footprint for inactive domains

## Extensibility

### Adding New Domains

1. **Create Domain Extractor**:
```python
class CustomDomainExtractor(BaseDomainExtractor):
    def extract_entities(self, text: str) -> List[ExtractedEntity]:
        # Implement custom entity extraction logic
        pass
    
    def identify_relationships(self, text: str, entities: List[ExtractedEntity]) -> List[EntityRelationship]:
        # Implement custom relationship identification logic
        pass
```

2. **Register Domain**:
```python
from src.core.domain_processor import get_domain_manager, DomainType

manager = get_domain_manager()
manager.register_extractor(DomainType.CUSTOM, CustomDomainExtractor())
```

3. **Create Configuration**:
```python
# Save domain schema to config/domains/custom.json
config_manager = get_domain_config_manager()
config_manager.save_schema(custom_schema)
```

### Custom Entity Types

Add new entity types by extending the `EntityType` enum:

```python
from src.core.models import EntityType

# Add new entity types as needed
class ExtendedEntityType(EntityType):
    LEGAL_ENTITY = "legal_entity"
    MEDICAL_TERM = "medical_term"
    FINANCIAL_INSTRUMENT = "financial_instrument"
```

## Best Practices

### 1. Pattern Design
- Use specific patterns that minimize false positives
- Include word boundaries (`\b`) to avoid partial matches
- Test patterns with representative text samples
- Provide confidence scores based on pattern reliability

### 2. Domain Switching
- Switch domains based on document type or content analysis
- Use hybrid approaches for documents spanning multiple domains
- Cache domain configurations for performance

### 3. Schema Management
- Version control domain configuration files
- Document pattern rationale and examples
- Regularly review and update patterns based on performance
- Use descriptive names for patterns and relationships

### 4. Testing
- Create comprehensive test suites for each domain
- Test with real-world documents from the target domain
- Validate entity extraction accuracy and relationship precision
- Monitor performance impact of domain-specific processing

## Troubleshooting

### Common Issues

1. **Circular Import Errors**:
   - Use lazy initialization in document processor
   - Import domain modules only when needed

2. **Pattern Matching Issues**:
   - Test regex patterns with online tools
   - Use raw strings for regex patterns
   - Escape special characters properly

3. **Performance Problems**:
   - Optimize regex patterns for efficiency
   - Use compiled patterns for repeated use
   - Limit pattern complexity

4. **Configuration Errors**:
   - Validate JSON schema files
   - Check entity type consistency
   - Verify relationship pattern group numbers

### Debugging

Enable debug logging to troubleshoot issues:

```python
import logging
logging.getLogger('src.core.domain_processor').setLevel(logging.DEBUG)
logging.getLogger('src.core.domain_config').setLevel(logging.DEBUG)
```

## Future Enhancements

### Planned Features
- **Machine Learning Integration**: Use ML models for entity extraction
- **Active Learning**: Improve patterns based on user feedback
- **Multi-Domain Documents**: Handle documents spanning multiple domains
- **Performance Analytics**: Track extraction accuracy and performance metrics
- **GUI Configuration**: Web interface for domain configuration management

### Extensibility Points
- **Custom Confidence Scoring**: Pluggable confidence calculation algorithms
- **Pattern Learning**: Automatic pattern discovery from training data
- **Semantic Validation**: Use embeddings to validate extracted entities
- **Cross-Domain Relationships**: Identify relationships across domain boundaries

This domain-specific processing system provides a robust foundation for adapting the Graph-Enhanced Agentic RAG system to various knowledge domains while maintaining flexibility and extensibility for future enhancements.