"""
Absolute minimal FastAPI test - no src imports at all
"""

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World", "port_test": "working"}

@app.get("/health")
def health():
    return {"status": "ok"}

# Absolutely minimal - no imports from src, no startup events, nothing