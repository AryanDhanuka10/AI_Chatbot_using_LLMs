# app.py - Entry point for HuggingFace Spaces

import subprocess
import sys
import os

# Ensure dependencies are installed
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

# Run FastAPI with Uvicorn
from src.api.server import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=7860,  # HuggingFace default port
        log_level="info",
    )