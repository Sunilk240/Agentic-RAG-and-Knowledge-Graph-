# 🧠 Graph-Enhanced Agentic RAG System

A sophisticated multi-agent retrieval-augmented generation system that combines graph databases and vector search for intelligent knowledge discovery.

## ✨ Features

- **🤖 Multi-Agent Architecture**: Specialized agents for coordination, graph navigation, vector retrieval, and synthesis
- **🔗 Hybrid Search**: Combines Neo4j graph traversal with vector similarity search
- **📊 Intelligent Query Routing**: Automatically selects optimal retrieval strategy
- **🌐 Web Interface**: Professional UI for queries and document upload
- **🔧 Admin Portal**: Database management and system monitoring
- **📚 User Guide**: Comprehensive documentation built-in

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone <your-repo-url>
cd graph-enhanced-agentic-rag
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys and database credentials
```

### 4. Run Server
```bash
python start_api.py
```

### 5. Access Application
- **Main Interface**: http://localhost:8000
- **User Guide**: http://localhost:8000/guide
- **Admin Portal**: http://localhost:8000/admin
- **API Docs**: http://localhost:8000/docs

## 🌐 Render Deployment

### Prerequisites
1. **Neo4j AuraDB**: Create free instance at [console.neo4j.io](https://console.neo4j.io/)
2. **Pinecone**: Create free account at [pinecone.io](https://www.pinecone.io/)
3. **Google Gemini**: Get API key at [ai.google.dev](https://ai.google.dev/)

### Deploy Steps
1. **Push to GitHub**: Upload your repository
2. **Connect to Render**: Link your GitHub repo
3. **Configure Build**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python start_api.py`
4. **Set Environment Variables**:
   ```env
   ENVIRONMENT=production
   NEO4J_URI=neo4j+s://your-instance.databases.neo4j.io
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=your_auradb_password
   PINECONE_API_KEY=your_pinecone_api_key
   GEMINI_API_KEY=your_gemini_api_key
   VECTOR_DB_TYPE=pinecone
   PINECONE_INDEX_NAME=rag-documents
   ```

## 🔐 Admin Access

- **Username**: `Sunil`
- **Password**: `test0663`
- **URL**: `/admin`

## 📁 Project Structure

```
├── src/
│   ├── agents/          # Multi-agent system
│   ├── api/            # FastAPI application
│   │   ├── static/     # Frontend files
│   │   └── main.py     # API routes
│   ├── core/           # Core functionality
│   └── database/       # Database managers
├── start_api.py        # Server startup
├── requirements.txt    # Dependencies
├── .env.example       # Environment template
└── README.md          # This file
```

## 🛠️ API Endpoints

- `POST /query` - Process intelligent queries
- `POST /documents/upload` - Upload documents
- `GET /health` - System health check
- `GET /admin/stats` - Database statistics
- `GET /docs` - API documentation

## 🧪 Testing

```bash
# Run tests
pytest

# Test specific component
pytest tests/test_agents.py
```

## 📝 Environment Variables

See `.env.example` for complete list of configuration options.

### Required for Production:
- `NEO4J_URI` - Neo4j database connection
- `NEO4J_USER` - Neo4j username
- `NEO4J_PASSWORD` - Neo4j password
- `PINECONE_API_KEY` - Pinecone API key
- `GEMINI_API_KEY` - Google Gemini API key

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details.

## 🆘 Support

- **Documentation**: Visit `/guide` in the application
- **API Reference**: Visit `/docs` for interactive API documentation
- **Issues**: Create GitHub issue for bugs or feature requests

---

**🎉 Ready to deploy your intelligent knowledge discovery system!**