#!/usr/bin/env python3
"""
Startup script for Oracle EBS R12 i-Supplier Assistant
"""
import os
import sys
import subprocess
import asyncio

def check_dependencies():
    """Check if all required dependencies are installed"""
    print("Checking dependencies...")
    
    required_packages = [
        'fastapi', 'uvicorn', 'pydantic', 'google-generativeai'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"[OK] {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"[MISSING] {package}")
    
    if missing_packages:
        print(f"\n[WARNING] Missing packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_packages)
            print("[OK] All packages installed successfully!")
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Failed to install packages: {e}")
            return False
    
    return True

def setup_environment():
    """Setup environment variables"""
    print("\nSetting up environment...")
    
    # Check for Google API key
    if not os.getenv('GOOGLE_API_KEY'):
        print("[WARNING] GOOGLE_API_KEY not found in environment variables")
        print("The Oracle EBS chatbot will work in basic mode without AI enhancement")
        print("To enable AI features, set GOOGLE_API_KEY environment variable")
    else:
        print("[OK] GOOGLE_API_KEY found")
    
    return True

async def test_application():
    """Test the application before starting"""
    print("\nTesting application...")
    
    try:
        # Add backend to path
        sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
        
        from backend.oracle_agent import OracleEBSAgent
        from backend.session_manager import SessionManager
        
        # Test initialization
        agent = OracleEBSAgent()
        await agent.initialize()
        
        session_manager = SessionManager()
        session = session_manager.get_session("test-session")
        
        # Test basic functionality
        response = await agent.process_message("Help", session)
        
        print("[OK] Application test passed!")
        return True
        
    except Exception as e:
        print(f"[ERROR] Application test failed: {e}")
        return False

def start_server():
    """Start the FastAPI server"""
    print("\nStarting Oracle EBS R12 i-Supplier Assistant...")
    print("Server will be available at: http://localhost:8000")
    print("Frontend will be available at: http://localhost:8000/advanced")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        # Change to backend directory
        backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
        
        # Start the server
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'main:app', 
            '--reload', 
            '--host', '0.0.0.0', 
            '--port', '8000'
        ], cwd=backend_dir)
        
    except KeyboardInterrupt:
        print("\n[INFO] Server stopped by user")
    except Exception as e:
        print(f"[ERROR] Failed to start server: {e}")

async def main():
    """Main startup function"""
    print("Oracle EBS R12 i-Supplier Assistant for Tanger Med")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        print("[ERROR] Dependency check failed. Please install missing packages manually.")
        return
    
    # Setup environment
    if not setup_environment():
        print("[ERROR] Environment setup failed.")
        return
    
    # Test application
    if not await test_application():
        print("[ERROR] Application test failed. Please check the error messages.")
        return
    
    print("\n[SUCCESS] All checks passed! Starting server...")
    
    # Start server
    start_server()

if __name__ == "__main__":
    asyncio.run(main())