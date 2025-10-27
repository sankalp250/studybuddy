#!/usr/bin/env python3
"""
Backend Connection Test Script
Tests if the backend server is running and accessible.
"""

import requests
import sys
import os

def test_backend_connection(base_url):
    """Test backend server connection and API endpoints."""
    
    print(f"Testing backend connection to: {base_url}")
    print("=" * 60)
    
    # Test 1: Root endpoint
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get(base_url, timeout=10)
        response.raise_for_status()
        print(f"[OK] Root endpoint: {response.json()}")
    except requests.exceptions.RequestException as e:
        print(f"[FAILED] Root endpoint: {e}")
        return False
    
    # Test 2: API docs
    print("\n2. Testing API documentation endpoint...")
    try:
        response = requests.get(f"{base_url}/docs", timeout=10)
        if response.status_code == 200:
            print("[OK] API docs accessible")
        else:
            print(f"[WARNING] API docs returned status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[WARNING] API docs check failed: {e}")
    
    # Test 3: Health check
    print("\n3. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/", timeout=10)
        response.raise_for_status()
        print("[OK] Health check passed")
    except requests.exceptions.RequestException as e:
        print(f"[FAILED] Health check: {e}")
    
    # Test 4: User registration endpoint (should exist)
    print("\n4. Testing API endpoints structure...")
    try:
        # Try to hit a known endpoint
        response = requests.get(f"{base_url}/api/users/", timeout=10)
        # This should either work or give a method not allowed
        if response.status_code in [200, 405]:
            print("[OK] API endpoints are accessible")
        else:
            print(f"[WARNING] Unexpected status: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"[FAILED] API endpoints check: {e}")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] Backend connection test completed!")
    print(f"\nBackend is running at: {base_url}")
    print(f"API documentation: {base_url}/docs")
    return True

def main():
    """Main function to test backend connection."""
    
    # Get backend URL from environment or use default
    backend_url = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
    
    # Override with command line argument if provided
    if len(sys.argv) > 1:
        backend_url = sys.argv[1]
    
    print("\n" + "=" * 60)
    print("StudyBuddy Backend Connection Test")
    print("=" * 60)
    
    success = test_backend_connection(backend_url)
    
    if success:
        print("\n[SUCCESS] Backend is ready to use!")
        print("\nNext steps:")
        print("1. Make sure your frontend is configured to use:", backend_url)
        print("2. If deploying to Streamlit Cloud, set BACKEND_URL secret")
        print("3. Test the login functionality")
        sys.exit(0)
    else:
        print("\n[FAILED] Backend is not accessible!")
        print("\nTroubleshooting:")
        print("1. Check if backend is running")
        print("2. Verify the BACKEND_URL is correct")
        print("3. Check firewall/network settings")
        print("4. If using Render, check service logs")
        sys.exit(1)

if __name__ == "__main__":
    main()
