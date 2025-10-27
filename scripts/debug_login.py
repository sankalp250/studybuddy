#!/usr/bin/env python3
"""
Debug login script to test specific credentials
"""

import requests
import sys

def test_login(email, password):
    """Test login with specific credentials."""
    print(f"Testing login for: {email}")
    
    # Test the token endpoint
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/token",
            data={"username": email, "password": password},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 200:
            print("[SUCCESS] Login successful!")
            token_data = response.json()
            print(f"Token: {token_data.get('access_token', 'No token')[:50]}...")
        elif response.status_code == 401:
            print("[FAILED] Login failed: Incorrect email or password")
        elif response.status_code == 500:
            print("[ERROR] Server error: Check backend logs")
        else:
            print(f"[ERROR] Unexpected status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Connection error: {e}")

def test_user_creation(email, password):
    """Test creating a new user."""
    print(f"\nTesting user creation for: {email}")
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/api/users/",
            json={"email": email, "password": password},
            timeout=10
        )
        
        print(f"Status Code: {response.status_code}")
        print(f"Response Text: {response.text}")
        
        if response.status_code == 201:
            print("[SUCCESS] User created successfully!")
        elif response.status_code == 400:
            print("[WARNING] User already exists")
        else:
            print(f"[ERROR] Unexpected status: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Connection error: {e}")

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        email = sys.argv[1]
        password = sys.argv[2]
        
        print("=" * 60)
        print("Login Debug Test")
        print("=" * 60)
        
        # First try to create the user (in case it doesn't exist)
        test_user_creation(email, password)
        
        # Then test login
        test_login(email, password)
        
    else:
        print("Usage: python debug_login.py <email> <password>")
        print("Example: python debug_login.py sankalp250@gmail.com yourpassword")
