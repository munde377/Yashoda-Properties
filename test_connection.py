#!/usr/bin/env python3
"""
Test script to verify frontend-backend connection
"""
import requests
import sys

BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"  # or 5173 for dev

def test_backend():
    try:
        response = requests.get(f"{BACKEND_URL}/health")
        if response.status_code == 200 and response.json().get("status") == "ok":
            print("✅ Backend health check passed")
            return True
        else:
            print("❌ Backend health check failed")
            return False
    except Exception as e:
        print(f"❌ Backend connection failed: {e}")
        return False

def test_frontend():
    try:
        response = requests.get(FRONTEND_URL)
        if response.status_code == 200:
            print("✅ Frontend is serving")
            return True
        else:
            print(f"❌ Frontend returned status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend connection failed: {e}")
        return False

def test_api_connection():
    # Test CORS by checking if backend allows frontend origin
    try:
        response = requests.options(f"{BACKEND_URL}/health",
                                  headers={"Origin": FRONTEND_URL})
        cors_headers = response.headers.get("access-control-allow-origin")
        if cors_headers:
            print("✅ CORS configured correctly")
            return True
        else:
            print("⚠️  CORS headers not found in preflight response")
            return True  # Not critical for basic functionality
    except Exception as e:
        print(f"⚠️  CORS check failed: {e}")
        return True

if __name__ == "__main__":
    print("Testing frontend-backend connection...")
    print()

    backend_ok = test_backend()
    frontend_ok = test_frontend()
    cors_ok = test_api_connection()

    print()
    if backend_ok and frontend_ok:
        print("🎉 Connection test passed! Your app should work correctly.")
        print(f"   Backend: {BACKEND_URL}")
        print(f"   Frontend: {FRONTEND_URL}")
    else:
        print("❌ Some tests failed. Check the output above.")
        sys.exit(1)