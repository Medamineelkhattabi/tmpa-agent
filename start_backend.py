#!/usr/bin/env python3
"""
Simple script to start the Oracle EBS Assistant backend server
"""

import sys
import os
import subprocess

def main():
    # Add the project root to Python path
    project_root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, project_root)
    
    print("Starting Oracle EBS Assistant Backend...")
    print(f"Project root: {project_root}")
    
    try:
        # Start the server
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "backend.main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=project_root)
        
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Error starting server: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())