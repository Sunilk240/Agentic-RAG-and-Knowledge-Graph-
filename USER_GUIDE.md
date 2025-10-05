# 👥 User Guide

## Graph-Enhanced Agentic RAG System

Welcome to the comprehensive user guide for the Graph-Enhanced Agentic RAG System! This guide will help you get the most out of our intelligent knowledge discovery platform.

---

## 🌟 What is Graph-Enhanced Agentic RAG?

Our system is an advanced AI-powered knowledge discovery platform that combines the best of both worlds:

- **🧠 Intelligent Understanding**: Uses AI agents to understand your questions and find the best way to answer them
- **🔗 Relationship Discovery**: Explores connections between concepts using knowledge graphs
- **📚 Semantic Search**: Finds relevant information using advanced text understanding
- **✨ Smart Synthesis**: Combines information from multiple sources to give you comprehensive answers

### Key Benefits
- **🎯 Accurate Answers**: Get precise, well-sourced responses to complex questions
- **🔍 Deep Insights**: Discover relationships and connections you might miss
- **📖 Transparent Sources**: See exactly where information comes from
- **⚡ Fast Results**: Get answers in seconds, not hours of research

---

## 🚀 Getting Started

### Accessing the System

1. **Web Interface**: Visit the web application at your provided URL
2. **Direct API**: Use the API endpoints for programmatic access
3. **Health Check**: Visit `/health` to verify the system is running

### First Steps

1. **Start with Simple Questions**: Begin with straightforward factual questions
2. **Upload Your Documents**: Add your own knowledge base for personalized results
3. **Explore Relationships**: Ask about connections between concepts
4. **Review Sources**: Always check the citations and sources provided

---

## 💬 How to Ask Questions

### Question Types We Excel At

#### 1. 📋 **Factual Questions**
Perfect for getting definitions and basic information.

**Examples:**
- "What is machine learning?"
- "Define neural networks"
- "Explain the transformer architecture"

**What happens:** The system uses semantic search to find the most relevant documents and provides a comprehensive definition with sources.

#### 2. 🔗 **Relationship Questions**
Great for understanding how concepts connect.

**Examples:**
- "How are neural networks related to deep learning?"
- "What's the connection between AI and robotics?"
- "How does reinforcement learning relate to game theory?"

**What happens:** The system explores the knowledge graph to find and explain relationships between entities.

#### 3. 🧩 **Complex Multi-Part Questions**
Ideal for comprehensive analysis requiring multiple reasoning steps.

**Examples:**
- "What are the applications of reinforcement learning in robotics and how do they relate to computer vision?"
- "How has the transformer architecture influenced both NLP and computer vision, and what are the key differences in implementation?"
- "What are the ethical implications of AI in healthcare and how do they relate to data privacy concerns?"

**What happens:** The system uses both graph exploration and semantic search to provide a thorough, multi-faceted answer.

### 💡 Tips for Better Questions

#### ✅ **Do This:**
- **Be specific**: "How does BERT differ from GPT?" vs "Tell me about language models"
- **Use natural language**: Write as you would speak to a knowledgeable colleague
- **Ask about relationships**: Use phrases like "related to", "connected with", "compared to"
- **Build on previous questions**: Follow up with deeper inquiries
- **Specify context**: "In the context of computer vision..." when relevant

#### ❌ **Avoid This:**
- **Overly broad questions**: "Tell me everything about AI"
- **Yes/no questions**: "Is machine learning good?" (instead ask "What are the benefits and limitations of machine learning?")
- **Ambiguous terms**: Be specific about which "model" or "system" you mean
- **Multiple unrelated questions**: Ask one focused question at a time

---

## 📚 Understanding Your Results

### Response Components

#### 1. **Main Answer**
The primary response synthesized from multiple sources.
- **Clear and comprehensive**: Combines information from various sources
- **Well-structured**: Organized with logical flow
- **Contextual**: Tailored to your specific question

#### 2. **Sources**
The documents and entities used to generate the answer.
- **Document Sources**: Specific documents with relevance scores
- **Graph Entities**: Concepts and entities from the knowledge graph
- **Relevance Scores**: How closely each source matches your question (0.0-1.0)

#### 3. **Citations**
Formal references you can use for further research.
- **Numbered references**: [1], [2], etc.
- **Source details**: Document titles, pages, or entity information
- **Clickable links**: When available, direct links to source materials

#### 4. **Reasoning Path**
Explanation of how the system processed your question.
- **Query Analysis**: How your question was interpreted
- **Strategy Selection**: Which approach was chosen (graph, vector, or hybrid)
- **Processing Steps**: What the system did to find and synthesize information
- **Agent Coordination**: Which AI agents were involved

#### 5. **Confidence Score**
How confident the system is in its answer (0.0-1.0).
- **0.8-1.0**: High confidence - comprehensive, well-supported answer
- **0.6-0.8**: Good confidence - reliable answer with good sources
- **0.4-0.6**: Moderate confidence - partial answer, may need more context
- **0.0-0.4**: Low confidence - limited information available

### Quality Indicators

#### 🟢 **High Quality Response**
- Confidence score > 0.7
- Multiple relevant sources
- Clear reasoning path
- Specific, actionable information

#### 🟡 **Good Response**
- Confidence score 0.5-0.7
- Some relevant sources
- Partial information
- May benefit from follow-up questions

#### 🔴 **Limited Response**
- Confidence score < 0.5
- Few or low-relevance sources
- General or vague information
- Consider rephrasing your question

---

## 📤 Adding Your Own Documents

### Why Upload Documents?

- **Personalized Knowledge**: Get answers specific to your domain or organization
- **Comprehensive Coverage**: Ensure important information is included
- **Better Context**: Improve answer quality with relevant background material
- **Custom Insights**: Discover connections within your own content

### Supported File Types

- **📄 Text Files**: .txt, .md (Markdown)
- **📋 PDF Documents**: .pdf
- **🌐 Web Content**: .html
- **📊 Structured Data**: .json, .xml (limited support)

### How to Upload Documents

#### Via Web Interface
1. **Click "Upload Document"** button
2. **Select your file** from your computer
3. **Add a title** (optional but recommended)
4. **Choose a domain** (technical, business, research, general)
5. **Add metadata** (optional: author, date, keywords)
6. **Click "Upload"** and wait for processing

#### Via API
```bash
curl -X POST "http://your-api-url/documents/upload" \
     -F "file=@your-document.pdf" \
     -F "title=Your Document Title" \
     -F "domain=technical"
```

### Upload Best Practices

#### ✅ **For Best Results:**
- **Provide clear titles**: Helps with entity extraction and organization
- **Choose appropriate domains**: Improves processing accuracy
- **Upload related documents**: Creates richer knowledge connections
- **Include metadata**: Author, date, keywords help with context
- **Use high-quality sources**: Better input = better output

#### 📋 **Document Preparation Tips:**
- **Clean formatting**: Remove unnecessary headers/footers
- **Clear structure**: Use headings and sections
- **Complete content**: Avoid truncated or partial documents
- **Relevant material**: Focus on documents related to your query topics

### What Happens During Processing?

1. **Text Extraction**: Content is extracted and cleaned
2. **Chunking**: Document is split into manageable sections
3. **Entity Extraction**: Key concepts and entities are identified
4. **Relationship Discovery**: Connections between entities are found
5. **Graph Storage**: Entities and relationships are added to the knowledge graph
6. **Vector Storage**: Text chunks are converted to embeddings for semantic search
7. **Mapping Creation**: Links between graph and vector representations are established

### Processing Time

- **Small documents** (< 10 pages): 30 seconds - 2 minutes
- **Medium documents** (10-50 pages): 2-5 minutes
- **Large documents** (50+ pages): 5-15 minutes

---

## 🎯 Advanced Usage Tips

### Getting Better Answers

#### 1. **Progressive Questioning**
Start broad, then get specific:
1. "What is reinforcement learning?"
2. "How is reinforcement learning used in robotics?"
3. "What are the challenges of applying reinforcement learning to robotic manipulation tasks?"

#### 2. **Context Building**
Reference previous concepts:
- "Building on the transformer architecture we discussed, how does BERT differ from GPT?"
- "Given the relationship between neural networks and deep learning, how do CNNs fit into this picture?"

#### 3. **Comparative Analysis**
Ask for comparisons:
- "Compare supervised and unsupervised learning approaches"
- "What are the trade-offs between accuracy and interpretability in machine learning models?"

#### 4. **Application-Focused Questions**
Ask about real-world applications:
- "How is natural language processing used in customer service?"
- "What are the practical applications of computer vision in manufacturing?"

### Understanding System Behavior

#### **Vector-Focused Responses** (Semantic Search)
- **When used**: Simple factual questions, definitions
- **Strengths**: Fast, comprehensive coverage of topics
- **Best for**: "What is...", "Define...", "Explain..."

#### **Graph-Focused Responses** (Relationship Exploration)
- **When used**: Questions about connections and relationships
- **Strengths**: Discovers hidden connections, multi-hop reasoning
- **Best for**: "How are X and Y related?", "What connects...", "Show the relationship..."

#### **Hybrid Responses** (Combined Approach)
- **When used**: Complex, multi-part questions
- **Strengths**: Comprehensive analysis, multiple perspectives
- **Best for**: Complex analysis, research-style questions

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### **"I'm not getting relevant results"**

**Possible causes:**
- Question too broad or vague
- Relevant documents not uploaded
- Technical terms not recognized

**Solutions:**
- ✅ Be more specific in your question
- ✅ Upload relevant documents to your domain
- ✅ Try alternative phrasings
- ✅ Break complex questions into parts

#### **"The confidence score is low"**

**Possible causes:**
- Limited information in knowledge base
- Question outside system's domain
- Ambiguous or unclear question

**Solutions:**
- ✅ Upload more relevant documents
- ✅ Rephrase your question more clearly
- ✅ Ask for specific aspects rather than general overviews
- ✅ Check if you're asking about a specialized domain

#### **"I'm not seeing the sources I expect"**

**Possible causes:**
- Documents not fully processed
- Search terms don't match document content
- Relevance threshold filtering results

**Solutions:**
- ✅ Wait for document processing to complete
- ✅ Try different keywords or phrasings
- ✅ Check document upload status
- ✅ Verify document content is relevant to your question

#### **"The system seems slow"**

**Possible causes:**
- Complex question requiring extensive processing
- High system load
- Large knowledge base

**Solutions:**
- ✅ Check system health at `/health` endpoint
- ✅ Try simpler questions first
- ✅ Break complex questions into parts
- ✅ Wait for current processing to complete

### Getting Help

#### **System Status**
- Check `/health` for system status
- Monitor processing times
- Verify all components are healthy

#### **Question Optimization**
- Start with simple questions
- Gradually increase complexity
- Use the reasoning path to understand system behavior

#### **Document Issues**
- Verify file format is supported
- Check upload completion status
- Ensure document content is relevant

---

## 🎓 Use Case Examples

### 1. **Research and Academic Work**

**Scenario**: Graduate student researching AI ethics

**Questions to ask:**
1. "What are the main ethical concerns in artificial intelligence?"
2. "How do bias and fairness relate to machine learning algorithms?"
3. "What are the current approaches to addressing algorithmic bias in hiring systems?"

**Documents to upload:**
- Academic papers on AI ethics
- Industry reports on bias in AI
- Regulatory guidelines and frameworks

**Expected outcomes:**
- Comprehensive literature review
- Understanding of key concepts and relationships
- Identification of research gaps

### 2. **Business Strategy and Planning**

**Scenario**: Business analyst evaluating AI adoption

**Questions to ask:**
1. "What are the key considerations for implementing AI in enterprise environments?"
2. "How do different AI technologies compare in terms of ROI and implementation complexity?"
3. "What are the common challenges and success factors for AI projects?"

**Documents to upload:**
- Industry case studies
- Implementation guides
- ROI analysis reports
- Vendor documentation

**Expected outcomes:**
- Strategic insights for AI adoption
- Risk assessment and mitigation strategies
- Implementation roadmap guidance

### 3. **Technical Development**

**Scenario**: Software engineer learning about new technologies

**Questions to ask:**
1. "How does the transformer architecture work in natural language processing?"
2. "What are the key differences between BERT and GPT models?"
3. "How can I implement attention mechanisms in my own neural network?"

**Documents to upload:**
- Technical papers and documentation
- Code examples and tutorials
- API documentation
- Best practices guides

**Expected outcomes:**
- Deep technical understanding
- Implementation guidance
- Best practices and patterns

### 4. **Educational Content Creation**

**Scenario**: Educator developing course materials

**Questions to ask:**
1. "What are the fundamental concepts students need to understand about machine learning?"
2. "How can I explain the relationship between statistics and machine learning to beginners?"
3. "What are good practical examples to demonstrate supervised learning concepts?"

**Documents to upload:**
- Textbooks and educational materials
- Research papers with clear explanations
- Case studies and examples
- Curriculum guidelines

**Expected outcomes:**
- Structured learning pathways
- Clear explanations and examples
- Comprehensive topic coverage

---

## 📊 Monitoring Your Usage

### Understanding System Feedback

#### **Processing Time**
- **< 2 seconds**: Simple vector search
- **2-5 seconds**: Graph exploration or hybrid approach
- **> 5 seconds**: Complex multi-hop reasoning

#### **Entity Recognition**
- Check which entities the system identified in your question
- Verify they match your intent
- Add clarification if important entities are missed

#### **Strategy Selection**
- **Vector-focused**: System chose semantic search
- **Graph-focused**: System chose relationship exploration
- **Hybrid**: System used both approaches

### Optimizing Your Experience

#### **Track What Works**
- Note which question phrasings give better results
- Identify which document types improve answers
- Observe which domains work best for your use cases

#### **Build Your Knowledge Base**
- Regularly upload relevant documents
- Organize documents by domain
- Update with new information as it becomes available

#### **Refine Your Approach**
- Start with broad questions, then narrow down
- Use follow-up questions to dive deeper
- Reference previous answers to build context

---

## 🔒 Privacy and Security

### Data Handling

- **Your questions**: Processed to provide answers, not stored long-term
- **Uploaded documents**: Stored securely in the knowledge base
- **Generated responses**: May be cached temporarily for performance

### Best Practices

- **Sensitive information**: Avoid uploading confidential documents
- **Personal data**: Don't include personal identifiers in questions
- **Proprietary content**: Ensure you have rights to upload documents

---

## 🚀 Advanced Features

### Multi-Domain Support

The system supports different knowledge domains:
- **Technical**: Programming, engineering, scientific concepts
- **Business**: Strategy, management, market analysis
- **Research**: Academic papers, experimental results
- **General**: Broad knowledge topics

### Reasoning Transparency

Every response includes:
- **Query analysis**: How your question was interpreted
- **Strategy selection**: Why a particular approach was chosen
- **Processing steps**: What the system did to find information
- **Source evaluation**: How sources were selected and ranked

### Continuous Learning

The system improves over time:
- **Document ingestion**: Each new document enriches the knowledge base
- **Relationship discovery**: New connections are automatically identified
- **Query patterns**: System learns from usage patterns (anonymized)

---

## 📞 Support and Feedback

### Getting Help

1. **Check system health**: Visit `/health` to verify system status
2. **Review this guide**: Most questions are answered here
3. **Try different phrasings**: Rephrase your question if results aren't satisfactory
4. **Upload relevant documents**: Add domain-specific content for better results

### Providing Feedback

Your feedback helps improve the system:
- **Rate responses**: Use confidence scores as guidance
- **Report issues**: Note any problems with specific queries
- **Suggest improvements**: Share ideas for better functionality

---

## 🎯 Quick Reference

### Question Types
- **Factual**: "What is...?", "Define...", "Explain..."
- **Relational**: "How are X and Y related?", "What connects...?"
- **Comparative**: "Compare X and Y", "What are the differences...?"
- **Applied**: "How is X used in Y?", "What are applications of...?"

### Upload Guidelines
- **Supported formats**: PDF, TXT, MD, HTML
- **Best practices**: Clear titles, appropriate domains, relevant content
- **Processing time**: 30 seconds to 15 minutes depending on size

### Quality Indicators
- **Confidence score**: 0.0-1.0 (higher is better)
- **Relevance scores**: Per source, 0.0-1.0
- **Source count**: More sources generally indicate better coverage
- **Reasoning path**: Shows system's decision-making process

### Troubleshooting
- **Low confidence**: Try more specific questions or upload relevant documents
- **Slow responses**: Check system health, break down complex questions
- **Irrelevant results**: Rephrase question, verify document relevance

---

This user guide covers everything you need to know to get the most out of the Graph-Enhanced Agentic RAG System. For technical details about the API, see the [API Documentation](API_DOCUMENTATION.md). For system architecture information, see the [Architecture Documentation](ARCHITECTURE.md).