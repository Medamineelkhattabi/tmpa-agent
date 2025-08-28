#!/usr/bin/env python3
"""
Test script to verify backend functionality
"""

import requests
import json
import sys

def test_backend():
    """Test backend endpoints"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Oracle EBS Assistant Backend...")
    print("-" * 40)
    
    # Test 1: Health check
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Health check: PASSED")
        else:
            print(f"❌ Health check: FAILED ({response.status_code})")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Health check: FAILED (Connection refused)")
        print("💡 Make sure the backend server is running on port 8000")
        return False
    
    # Test 2: Chat endpoint
    try:
        chat_data = {
            "message": "test connection",
            "session_id": "test_session_123"
        }
        response = requests.post(f"{base_url}/api/chat", json=chat_data)
        if response.status_code == 200:
            print("✅ Chat endpoint: PASSED")
        else:
            print(f"❌ Chat endpoint: FAILED ({response.status_code})")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Chat endpoint: FAILED ({e})")
        return False
    
    # Test 3: Procedures endpoint
    try:
        response = requests.get(f"{base_url}/api/procedures")
        if response.status_code == 200:
            print("✅ Procedures endpoint: PASSED")
        else:
            print(f"❌ Procedures endpoint: FAILED ({response.status_code})")
            return False
    except Exception as e:
        print(f"❌ Procedures endpoint: FAILED ({e})")
        return False
    
    print("-" * 40)
    print("🎉 All tests passed! Backend is working correctly.")
    return True

if __name__ == "__main__":
    success = test_backend()
    sys.exit(0 if success else 1)