import requests
import json

BASE_URL = "http://localhost:8000/api/v1/auth"

def test_auth():
    # 1. Login
    print("Testing Login...")
    login_data = {"username": "admin", "password": "admin123"}
    response = requests.post(f"{BASE_URL}/login", json=login_data)
    
    if response.status_code != 200:
        print(f"FAILED: Login returned {response.status_code}")
        print(response.text)
        return

    result = response.json()
    token = result.get("access_token")
    print(f"SUCCESS: Login successful. Token: {token[:20]}...")

    # 2. Get Me
    print("\nTesting /me...")
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/me", headers=headers)
    
    if response.status_code != 200:
        print(f"FAILED: /me returned {response.status_code}")
        print(response.text)
        return

    user = response.json()
    print(f"SUCCESS: /me returned user: {user.get('username')}")
    print(f"User Info: {json.dumps(user, indent=2)}")

if __name__ == "__main__":
    test_auth()
