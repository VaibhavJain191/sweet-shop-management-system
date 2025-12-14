"""
Tests for sweets endpoints (TDD - RED phase).
"""
import pytest
from httpx import AsyncClient


# Helper function to get auth token
async def get_auth_token(client: AsyncClient, email: str = "test@example.com", is_admin: bool = False) -> str:
    """Register a user and return auth token."""
    # Register user
    await client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "password123",
            "name": "Test User"
        }
    )
    
    # If admin, we need to manually update the role (for testing)
    # In production, this would be done through an admin panel
    if is_admin:
        from app.models.user import User
        user = await User.find_one(User.email == email)
        user.role = "admin"
        await user.save()
    
    # Login and get token
    response = await client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "password123"
        }
    )
    
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_sweet_success(client: AsyncClient):
    """Test creating a new sweet."""
    token = await get_auth_token(client)
    
    response = await client.post(
        "/api/sweets",
        json={
            "name": "Chocolate Bar",
            "category": "Chocolate",
            "price": 2.99,
            "quantity": 100,
            "description": "Delicious milk chocolate"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Chocolate Bar"
    assert data["category"] == "Chocolate"
    assert data["price"] == 2.99
    assert data["quantity"] == 100
    assert "id" in data


@pytest.mark.asyncio
async def test_create_sweet_unauthorized(client: AsyncClient):
    """Test creating sweet without authentication fails."""
    response = await client.post(
        "/api/sweets",
        json={
            "name": "Chocolate Bar",
            "category": "Chocolate",
            "price": 2.99,
            "quantity": 100
        }
    )
    
    assert response.status_code == 401  # Unauthorized


@pytest.mark.asyncio
async def test_create_sweet_invalid_price(client: AsyncClient):
    """Test creating sweet with invalid price fails."""
    token = await get_auth_token(client)
    
    response = await client.post(
        "/api/sweets",
        json={
            "name": "Chocolate Bar",
            "category": "Chocolate",
            "price": -1.0,  # Invalid negative price
            "quantity": 100
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_get_all_sweets(client: AsyncClient):
    """Test getting all sweets."""
    token = await get_auth_token(client)
    
    # Create some sweets
    await client.post(
        "/api/sweets",
        json={"name": "Sweet 1", "category": "Candy", "price": 1.99, "quantity": 50},
        headers={"Authorization": f"Bearer {token}"}
    )
    await client.post(
        "/api/sweets",
        json={"name": "Sweet 2", "category": "Chocolate", "price": 2.99, "quantity": 30},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Get all sweets
    response = await client.get(
        "/api/sweets",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] in ["Sweet 1", "Sweet 2"]


@pytest.mark.asyncio
async def test_search_sweets_by_name(client: AsyncClient):
    """Test searching sweets by name."""
    token = await get_auth_token(client)
    
    # Create sweets
    await client.post(
        "/api/sweets",
        json={"name": "Chocolate Bar", "category": "Chocolate", "price": 2.99, "quantity": 50},
        headers={"Authorization": f"Bearer {token}"}
    )
    await client.post(
        "/api/sweets",
        json={"name": "Gummy Bears", "category": "Candy", "price": 1.99, "quantity": 30},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Search for chocolate
    response = await client.get(
        "/api/sweets/search?name=Chocolate",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Chocolate Bar"


@pytest.mark.asyncio
async def test_search_sweets_by_category(client: AsyncClient):
    """Test searching sweets by category."""
    token = await get_auth_token(client)
    
    # Create sweets
    await client.post(
        "/api/sweets",
        json={"name": "Chocolate Bar", "category": "Chocolate", "price": 2.99, "quantity": 50},
        headers={"Authorization": f"Bearer {token}"}
    )
    await client.post(
        "/api/sweets",
        json={"name": "Dark Chocolate", "category": "Chocolate", "price": 3.99, "quantity": 30},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Search by category
    response = await client.get(
        "/api/sweets/search?category=Chocolate",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


@pytest.mark.asyncio
async def test_search_sweets_by_price_range(client: AsyncClient):
    """Test searching sweets by price range."""
    token = await get_auth_token(client)
    
    # Create sweets with different prices
    await client.post(
        "/api/sweets",
        json={"name": "Cheap Candy", "category": "Candy", "price": 0.99, "quantity": 50},
        headers={"Authorization": f"Bearer {token}"}
    )
    await client.post(
        "/api/sweets",
        json={"name": "Premium Chocolate", "category": "Chocolate", "price": 5.99, "quantity": 30},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Search by price range
    response = await client.get(
        "/api/sweets/search?min_price=2.0&max_price=10.0",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Premium Chocolate"


@pytest.mark.asyncio
async def test_update_sweet_success(client: AsyncClient):
    """Test updating a sweet."""
    token = await get_auth_token(client)
    
    # Create a sweet
    create_response = await client.post(
        "/api/sweets",
        json={"name": "Original Name", "category": "Candy", "price": 1.99, "quantity": 50},
        headers={"Authorization": f"Bearer {token}"}
    )
    sweet_id = create_response.json()["id"]
    
    # Update the sweet
    response = await client.put(
        f"/api/sweets/{sweet_id}",
        json={"name": "Updated Name", "price": 2.49},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["price"] == 2.49
    assert data["category"] == "Candy"  # Unchanged


@pytest.mark.asyncio
async def test_delete_sweet_admin_only(client: AsyncClient):
    """Test deleting a sweet (admin only)."""
    # Regular user token
    user_token = await get_auth_token(client, "user@example.com")
    
    # Admin token
    admin_token = await get_auth_token(client, "admin@example.com", is_admin=True)
    
    # Create a sweet
    create_response = await client.post(
        "/api/sweets",
        json={"name": "To Delete", "category": "Candy", "price": 1.99, "quantity": 50},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    sweet_id = create_response.json()["id"]
    
    # Try to delete as regular user (should fail)
    response = await client.delete(
        f"/api/sweets/{sweet_id}",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden
    
    # Delete as admin (should succeed)
    response = await client.delete(
        f"/api/sweets/{sweet_id}",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_purchase_sweet_success(client: AsyncClient):
    """Test purchasing a sweet."""
    token = await get_auth_token(client)
    
    # Create a sweet
    create_response = await client.post(
        "/api/sweets",
        json={"name": "Candy", "category": "Candy", "price": 1.99, "quantity": 50},
        headers={"Authorization": f"Bearer {token}"}
    )
    sweet_id = create_response.json()["id"]
    
    # Purchase some quantity
    response = await client.post(
        f"/api/sweets/{sweet_id}/purchase",
        json={"quantity": 10},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 40  # 50 - 10


@pytest.mark.asyncio
async def test_purchase_sweet_insufficient_quantity(client: AsyncClient):
    """Test purchasing more than available quantity fails."""
    token = await get_auth_token(client)
    
    # Create a sweet with limited quantity
    create_response = await client.post(
        "/api/sweets",
        json={"name": "Candy", "category": "Candy", "price": 1.99, "quantity": 5},
        headers={"Authorization": f"Bearer {token}"}
    )
    sweet_id = create_response.json()["id"]
    
    # Try to purchase more than available
    response = await client.post(
        f"/api/sweets/{sweet_id}/purchase",
        json={"quantity": 10},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400
    assert "insufficient" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_restock_sweet_admin_only(client: AsyncClient):
    """Test restocking a sweet (admin only)."""
    # Regular user token
    user_token = await get_auth_token(client, "user@example.com")
    
    # Admin token
    admin_token = await get_auth_token(client, "admin@example.com", is_admin=True)
    
    # Create a sweet
    create_response = await client.post(
        "/api/sweets",
        json={"name": "Candy", "category": "Candy", "price": 1.99, "quantity": 10},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    sweet_id = create_response.json()["id"]
    
    # Try to restock as regular user (should fail)
    response = await client.post(
        f"/api/sweets/{sweet_id}/restock",
        json={"quantity": 50},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert response.status_code == 403  # Forbidden
    
    # Restock as admin (should succeed)
    response = await client.post(
        f"/api/sweets/{sweet_id}/restock",
        json={"quantity": 50},
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["quantity"] == 60  # 10 + 50
