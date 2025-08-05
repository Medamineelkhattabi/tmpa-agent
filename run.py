#!/usr/bin/env python3
"""
Oracle EBS R12 i-Supplier Assistant
Run script for the FastAPI backend server
"""

import uvicorn
import os
import sys

# Add the workspace to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    debug = os.getenv("DEBUG", "false").lower() == "true"
    
    print("🚀 Starting Oracle EBS R12 i-Supplier Assistant")
    print(f"📡 Server will be available at: http://{host}:{port}")
    print(f"📖 API Documentation: http://{host}:{port}/docs")
    print(f"🔧 Debug mode: {'ON' if debug else 'OFF'}")
    print("-" * 50)
    
    # Run the server
    uvicorn.run(
        "backend.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="debug" if debug else "info"
    )