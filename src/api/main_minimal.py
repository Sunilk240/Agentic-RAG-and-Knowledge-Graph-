"""
Minimal FastAPI app for testing Render deployment
"""

from fastapi import FastAPI

# Create minimal FastAPI app
app = FastAPI(title="Minimal Test API")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Hello from minimal FastAPI app!", "status": "working"}

@app.get("/health")
async def health():
    """Health check"""
    return {"status": "healthy", "app": "minimal"}

# No startup events, no database connections, no agents - just basic FastAPI