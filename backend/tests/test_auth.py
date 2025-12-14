"""
Tests for authentication endpoints (TDD - RED phase).
"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    """Test successful user registration."""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
            "name": "Test User"
        }
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert data["role"] == "user"
    assert "id" in data
    assert "password" not in data


@pytest.mark.asyncio
async def test_register_user_duplicate_email(client: AsyncClient):
    """Test registration with duplicate email fails."""
    user_data = {
        "email": "duplicate@example.com",
        "password": "password123",
        "name": "First User"
    }
    
    # Register first user
    await client.post("/api/auth/register", json=user_data)
    
    # Try to register with same email
    response = await client.post("/api/auth/register", json=user_data)
    
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_user_invalid_email(client: AsyncClient):
    """Test registration with invalid email fails."""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "not-an-email",
            "password": "password123",
            "name": "Test User"
        }
    )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_register_user_short_password(client: AsyncClient):
    """Test registration with short password fails."""
    response = await client.post(
        "/api/auth/register",
        json={
            "email": "test@example.com",
            "password": "123",  # Too short
            "name": "Test User"
        }
    )
    
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    """Test successful user login."""
    # First register a user
    await client.post(
        "/api/auth/register",
        json={
            "email": "login@example.com",
            "password": "password123",
            "name": "Login User"
        }
    )
    
    # Now login
    response = await client.post(
        "/api/auth/login",
        json={
            "email": "login@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    """Test login with wrong password fails."""
    # First register a user
    await client.post(
        "/api/auth/register",
        json={
            "email": "user@example.com",
            "password": "correctpassword",
            "name": "Test User"
        }
    )
    
    # Try to login with wrong password
    response = await client.post(
        "/api/auth/login",
        json={
            "email": "user@example.com",
            "password": "wrongpassword"
        }
    )
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    """Test login with non-existent user fails."""
    response = await client.post(
        "/api/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "password123"
        }
    )
    
    assert response.status_code == 401
    assert "incorrect" in response.json()["detail"].lower()
