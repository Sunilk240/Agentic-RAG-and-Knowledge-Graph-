# Graph-Enhanced Agentic RAG System

🤖 **A sophisticated multi-agent retrieval-augmented generation system** that combines graph-based knowledge representation with vector embeddings for intelligent information retrieval and synthesis.

## 🌟 Key Features

- **🧠 Multi-Agent Architecture**: Four specialized agents working in coordination
- **🔗 Hybrid Retrieval**: Combines graph traversal with semantic vector search
- **⚡ Intelligent Query Routing**: Automatic strategy selection based on query complexity
- **🎯 Context-Aware Synthesis**: Advanced response generation using Google Gemini
- **📊 Dual Storage**: Neo4j graph database + Pinecone/Chroma vector store
- **🚀 Production Ready**: FastAPI, Docker, cloud deployment support

## 🏗️ Architecture Overview

### Multi-Agent System
- **🎯 Coordinator Agent**: Query analysis, entity extraction, strategy selection
- **🗺️ Graph Navigator Agent**: Neo4j traversal, relationship exploration, Cypher queries
- **🔍 Vector Retrieval Agent**: Semantic search, embedding generation, similarity matching
- **✨ Synthesis Agent**: Result integration, response generation, citation management

### Data Flow
```
User Query → Coordinator → Strategy Selection → Parallel Retrieval → Synthesis → Response
              ↓              ↓                    ↓                    ↓
         Entity Extract   Graph/Vector      Neo4j + Pinecone     Gemini API
```

📖 **[Detailed Architecture Documentation](ARCHITECTURE.md)**

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Neo4j Database (local or AuraDB)
- Google Gemini API Key
- Optional: Pinecone API Key

### Local Development

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd graph-enhanced-agentic-rag
   pip install -r requirements.txt
   ```

2. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database connections
   ```

3. **Start with Docker (Recommended)**:
   ```bash
   docker-compose up -d
   ```

4. **Or run locally**:
   ```bash
   python start_api.py
   ```

5. **Access the system**:
   - 🌐 **API**: http://localhost:8000
   - 📚 **Documentation**: http://localhost:8000/docs
   - 🔍 **Health Check**: http://localhost:8000/health
   - 💻 **Web Interface**: http://localhost:8000/interface

## 📡 API Endpoints

### Core Endpoints
- `GET /` - API information and status
- `GET /health` - System health check
- `POST /query` - Process intelligent queries
- `POST /ingest` - Ingest documents into the system
- `GET /agents/status` - Multi-agent system status

### Advanced Endpoints
- `POST /query/analyze` - Query analysis only
- `GET /graph/entities` - Browse graph entities
- `GET /vector/search` - Direct vector search
- `POST /synthesis/custom` - Custom synthesis requests

### Example Usage

**Basic Query**:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{"query": "What are the relationships between machine learning and neural networks?"}'
```

**Document Ingestion**:
```bash
curl -X POST "http://localhost:8000/ingest" \
     -F "file=@document.pdf" \
     -F "title=ML Research Paper"
```

**Health Check**:
```bash
curl http://localhost:8000/health
```

## Deployment

### Render Deployment

1. **Connect repository** to Render
2. **Set environment variables** in Render dashboard:
   - `NEO4J_URI` - Neo4j AuraDB connection string
   - `NEO4J_USER` - Neo4j username
   - `NEO4J_PASSWORD` - Neo4j password
   - `CHROMA_HOST` - Chroma service host
   - `GEMINI_API_KEY` - Google AI Studio API key

3. **Deploy** using the provided `render.yaml` configuration

### Docker Deployment

```bash
# Build image
docker build -t graph-rag-api .

# Run container
docker run -p 8000:8000 --env-file .env graph-rag-api
```

## ⚙️ Configuration

### Environment Variables (.env)

**Database Configuration**:
```env
# Neo4j Graph Database
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_password
NEO4J_DATABASE=neo4j

# Vector Database (Pinecone or Chroma)
VECTOR_DB_TYPE=pinecone  # or "chroma"
PINECONE_API_KEY=your_pinecone_key
PINECONE_INDEX_NAME=rag-documents
CHROMA_HOST=localhost
CHROMA_PORT=8000
```

**AI/LLM Configuration**:
```env
# Google Gemini API
GEMINI_API_KEY=your_gemini_key
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=2048
```

**System Configuration**:
```env
# API Settings
API_HOST=0.0.0.0
API_PORT=8000
API_CORS_ORIGINS=*

# Agent Settings
AGENT_TIMEOUT=30
AGENT_MAX_RETRIES=3
```

## 🛠️ Development

### Project Structure

```
📁 graph-enhanced-agentic-rag/
├── 📁 src/
│   ├── 📁 core/              # Core system components
│   │   ├── models.py         # Data models (Entity, Document, Concept)
│   │   ├── interfaces.py     # Agent interfaces and protocols
│   │   ├── database.py       # Database connection managers
│   │   ├── config.py         # Configuration management
│   │   └── ingestion_pipeline.py  # Document ingestion system
│   ├── 📁 agents/            # Multi-agent implementations
│   │   ├── coordinator.py    # Query analysis and orchestration
│   │   ├── graph_navigator.py # Graph traversal and Cypher queries
│   │   ├── vector_retrieval.py # Semantic search and embeddings
│   │   └── synthesis.py      # Response generation and integration
│   ├── 📁 api/               # FastAPI web service
│   │   ├── main.py          # API endpoints and middleware
│   │   └── static/          # Web interface assets
│   └── 📁 database/          # Database-specific implementations
├── 📁 tests/                 # Comprehensive test suite
├── 📁 docs/                  # Documentation
├── 📁 scripts/               # Utility scripts
├── 🐳 docker-compose.yml     # Local development environment
├── 🚀 render.yaml           # Cloud deployment configuration
└── 📋 requirements.txt       # Python dependencies
```

### Development Workflow

1. **Setup Development Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

2. **Run Tests**:
   ```bash
   pytest tests/ -v
   ```

3. **Start Development Server**:
   ```bash
   python start_api.py
   ```

4. **Access Development Tools**:
   - 📊 **Admin Portal**: `python admin_portal.py`
   - 🧪 **Test Scripts**: `python scripts/test_api.py`

