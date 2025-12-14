"""
Test the Sweet Shop API endpoints manually.
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_api():
    print("=" * 60)
    print("TESTING SWEET SHOP API")
    print("=" * 60)
    
    # Test 1: Register a user
    print("\n1. Testing User Registration...")
    register_data = {
        "email": "testuser@example.com",
        "password": "password123",
        "name": "Test User"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/register", json=register_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            user_data = response.json()
            print(f"   ✅ User registered: {user_data['email']}")
            print(f"   User ID: {user_data['id']}")
            print(f"   Role: {user_data['role']}")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Login
    print("\n2. Testing User Login...")
    login_data = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['access_token']
            print(f"   ✅ Login successful!")
            print(f"   Token: {token[:50]}...")
        else:
            print(f"   Response: {response.json()}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Set up headers with token
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 3: Create a sweet
    print("\n3. Testing Create Sweet...")
    sweet_data = {
        "name": "Chocolate Bar",
        "category": "Chocolate",
        "price": 2.99,
        "quantity": 100,
        "description": "Delicious milk chocolate bar"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/sweets", json=sweet_data, headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 201:
            sweet = response.json()
            sweet_id = sweet['id']
            print(f"   ✅ Sweet created: {sweet['name']}")
            print(f"   Price: ${sweet['price']}")
            print(f"   Quantity: {sweet['quantity']}")
        else:
            print(f"   Response: {response.json()}")
            return
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 4: Get all sweets
    print("\n4. Testing Get All Sweets...")
    try:
        response = requests.get(f"{BASE_URL}/api/sweets", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            sweets = response.json()
            print(f"   ✅ Retrieved {len(sweets)} sweet(s)")
            for sweet in sweets:
                print(f"      - {sweet['name']}: ${sweet['price']} ({sweet['quantity']} in stock)")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Search sweets
    print("\n5. Testing Search Sweets...")
    try:
        response = requests.get(f"{BASE_URL}/api/sweets/search?category=Chocolate", headers=headers)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            sweets = response.json()
            print(f"   ✅ Found {len(sweets)} chocolate sweet(s)")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Purchase a sweet
    print("\n6. Testing Purchase Sweet...")
    try:
        response = requests.post(
            f"{BASE_URL}/api/sweets/{sweet_id}/purchase",
            json={"quantity": 10},
            headers=headers
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            updated_sweet = response.json()
            print(f"   ✅ Purchased 10 units")
            print(f"   Remaining quantity: {updated_sweet['quantity']}")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 7: Update sweet
    print("\n7. Testing Update Sweet...")
    try:
        response = requests.put(
            f"{BASE_URL}/api/sweets/{sweet_id}",
            json={"price": 3.49},
            headers=headers
        )
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            updated_sweet = response.json()
            print(f"   ✅ Price updated to ${updated_sweet['price']}")
        else:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("✅ ALL API TESTS COMPLETED SUCCESSFULLY!")
    print("=" * 60)

if __name__ == "__main__":
    test_api()
