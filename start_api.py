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
    return int(os.environ.get("PORT", 8000))

def get_host():
    """Get host from environment variable or default to 0.0.0.0"""
    return os.environ.get("HOST", "0.0.0.0")

def is_production():
    """Check if running in production environment"""
    return os.environ.get("ENVIRONMENT", "development").lower() == "production"

if __name__ == "__main__":
    host = get_host()
    port = get_port()
    environment = "production" if is_production() else "development"
    
    print("🚀 Starting Graph-Enhanced Agentic RAG API...")
    print(f"🌍 Environment: {environment}")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    print(f"🔍 Health Check: http://{host}:{port}/health")
    print(f"🌐 Web Interface: http://{host}:{port}/interface")
    print("\n⚡ Starting server...")
    
    # Production vs Development configuration
    if is_production():
        # Production settings
        uvicorn.run(
            "src.api.main:app",
            host=host,
            port=port,
            reload=False,  # No auto-reload in production
            log_level="info",
            access_log=True,
            workers=1  # Single worker for starter plan
        )
    else:
        # Development settings
        uvicorn.run(
            "src.api.main:app",
            host=host,
            port=port,
            reload=True,  # Auto-reload in development
            log_level="debug"
        )