# 🚀 Deployment Checklist

## ✅ Pre-Deployment Setup

### 1. Create Cloud Database Accounts

#### Neo4j AuraDB (Free Tier)
- [ ] Go to https://console.neo4j.io/
- [ ] Create free AuraDB instance
- [ ] Note down connection URI: `neo4j+s://xxxxx.databases.neo4j.io`
- [ ] Note down username: `neo4j`
- [ ] Note down password: `your_generated_password`

#### Pinecone (Free Tier)
- [ ] Go to https://www.pinecone.io/
- [ ] Create free account
- [ ] Create index named `rag-documents`
- [ ] Set dimensions to `384` (for all-MiniLM-L6-v2)
- [ ] Note down API key

#### Google Gemini API (Free Tier)
- [ ] Go to https://ai.google.dev/
- [ ] Create API key for Gemini
- [ ] Note down API key

### 2. Prepare Repository
- [ ] Commit all changes to GitHub
- [ ] Push to main branch
- [ ] Verify all files are committed
- [ ] Ensure .env is NOT committed (check .gitignore)

## 🌐 Render Deployment

### 1. Connect to Render
- [ ] Go to https://render.com/
- [ ] Sign up/login with GitHub
- [ ] Click "New +" → "Web Service"
- [ ] Connect your GitHub repository
- [ ] Select the repository

### 2. Configure Deployment
- [ ] **Name**: `graph-enhanced-rag` (or your preferred name)
- [ ] **Environment**: `Python 3`
- [ ] **Build Command**: `pip install -r requirements.txt`
- [ ] **Start Command**: `python start_api.py`
- [ ] **Plan**: Free (or upgrade as needed)

### 3. Set Environment Variables
In Render dashboard, add these environment variables:

#### Required Variables
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

#### Optional Variables (have defaults)
```env
GEMINI_MODEL=gemini-2.0-flash-exp
LOG_LEVEL=INFO
CORS_ORIGINS=["*"]
```

### 4. Deploy
- [ ] Click "Create Web Service"
- [ ] Wait for build to complete (5-10 minutes)
- [ ] Check deployment logs for any errors
- [ ] Verify deployment success

## 🧪 Post-Deployment Testing

### 1. Test Main Application
- [ ] Visit your Render URL: `https://your-app.onrender.com`
- [ ] Test the main interface
- [ ] Upload a test document
- [ ] Ask a test question
- [ ] Verify response quality

### 2. Test Admin Portal
- [ ] Visit: `https://your-app.onrender.com/admin`
- [ ] Check database statistics
- [ ] View Neo4j details
- [ ] View Pinecone details

### 3. Test User Guide
- [ ] Visit: `https://your-app.onrender.com/guide`
- [ ] Verify all sections load properly
- [ ] Check responsive design on mobile

### 4. Test API Endpoints
- [ ] Visit: `https://your-app.onrender.com/docs`
- [ ] Test query endpoint
- [ ] Test document upload
- [ ] Test health check

## 📊 Performance Monitoring

### 1. Monitor Render Dashboard
- [ ] Check CPU and memory usage
- [ ] Monitor response times
- [ ] Watch for any errors in logs

### 2. Database Monitoring
- [ ] Monitor Neo4j AuraDB usage
- [ ] Monitor Pinecone index usage
- [ ] Check API rate limits

## 🎯 Your Live URLs

Once deployed, your application will be available at:
- **Main Application**: `https://your-app.onrender.com/`
- **User Guide**: `https://your-app.onrender.com/guide`
- **Admin Portal**: `https://your-app.onrender.com/admin`
- **API Documentation**: `https://your-app.onrender.com/docs`

## 🎉 Deployment Complete!

### Share Your Application
- ✅ **End Users**: Share the main application URL
- ✅ **Developers**: Share the API documentation URL
- ✅ **Administrators**: Share the admin portal URL (with credentials)

### Maintenance
- **Updates**: Push code changes to GitHub → Render auto-deploys
- **Monitoring**: Check Render dashboard regularly
- **Backup**: Neo4j AuraDB has automatic backups

---

**🚀 Your Graph-Enhanced Agentic RAG System is now live!**