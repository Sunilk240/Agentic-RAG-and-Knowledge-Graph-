#!/usr/bin/env python3
"""
Start the Graph-Enhanced Agentic RAG API server.
"""
import uvicorn
import sys
import os
import logging

# Add the project root to Python path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def get_port():
    """Get port from environment variable or default to 8000"""
    try:
        port = int(os.environ.get("PORT", 8000))
        print(f"🔌 Using port: {port}")
        return port
    except:
        print("🔌 Using fallback port: 8000")
        return 8000

def get_host():
    """Get host from environment variable or default to 0.0.0.0"""
    host = os.environ.get("HOST", "0.0.0.0")
    if not host:
        host = "0.0.0.0"
    print(f"🌐 Using host: {host}")
    return host

def is_production():
    """Check if running in production environment"""
    return os.environ.get("ENVIRONMENT", "development").lower() == "production"

if __name__ == "__main__":
    # Force hardcoded values for Render
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", 8000))
    
    print("🚀 Starting Graph-Enhanced Agentic RAG API...")
    print(f"🔌 RENDER PORT: {os.environ.get('PORT', 'NOT SET')}")
    print(f"🌐 BINDING TO: {host}:{port}")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print("\n⚡ Starting server NOW...")
    
    # Simple uvicorn run - no workers, no complexity
    uvicorn.run(
        "src.api.main:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )