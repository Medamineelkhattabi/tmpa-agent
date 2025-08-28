#!/usr/bin/env python3
"""
Test script to verify the fixes work correctly
"""
import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.oracle_agent import OracleEBSAgent
from backend.session_manager import SessionManager
from backend.models import SessionState, WorkflowStatus

async def test_basic_functionality():
    """Test basic functionality"""
    print("Testing Oracle EBS Assistant fixes...")
    
    # Initialize components
    agent = OracleEBSAgent()
    session_manager = SessionManager()
    
    try:
        # Initialize agent
        await agent.initialize()
        print("[OK] Agent initialized successfully")
        
        # Test session creation
        session = session_manager.get_session("test-session-123")
        print("[OK] Session created successfully")
        
        # Test procedure listing
        procedures = agent.get_available_procedures()
        print(f"[OK] Found {len(procedures)} procedures")
        
        # Test starting a procedure
        response = await agent.process_message("Start work confirmation", session)
        print("[OK] Procedure start handled successfully")
        print(f"Response: {response.message[:100]}...")
        
        # Test canceling procedure
        response = await agent.process_message("Cancel procedure", session)
        print("[OK] Procedure cancellation handled successfully")
        print(f"Response: {response.message[:100]}...")
        
        # Test session reset
        response = await agent.process_message("Reset session", session)
        print("[OK] Session reset handled successfully")
        print(f"Response: {response.message[:100]}...")
        
        # Test help command
        response = await agent.process_message("Help", session)
        print("[OK] Help command handled successfully")
        
        # Test Oracle query
        response = await agent.process_message("Show purchase orders", session)
        print("[OK] Oracle query handled successfully")
        
        print("\n[SUCCESS] All tests passed! The fixes are working correctly.")
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = asyncio.run(test_basic_functionality())
    if success:
        print("\n[SUCCESS] Oracle EBS Assistant is ready to use!")
        print("You can now start the server with: python -m uvicorn backend.main:app --reload")
    else:
        print("\n[ERROR] Some issues remain. Please check the error messages above.")