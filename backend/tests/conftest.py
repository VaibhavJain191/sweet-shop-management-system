"""
Pytest configuration and fixtures for testing.
"""
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import app
from app.models.user import User
from app.models.sweet import Sweet


# Test database configuration
TEST_MONGODB_URL = "mongodb://localhost:27017"
TEST_DATABASE_NAME = "sweet_shop_test"


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def test_db():
    """Initialize test database and clean up after each test."""
    # Connect to test database
    client = AsyncIOMotorClient(TEST_MONGODB_URL)
    database = client[TEST_DATABASE_NAME]
    
    # Initialize Beanie with test database
    await init_beanie(
        database=database,
        document_models=[User, Sweet]
    )
    
    yield database
    
    # Clean up: drop all collections after each test
    await User.delete_all()
    await Sweet.delete_all()
    
    client.close()


@pytest.fixture(scope="function")
async def client(test_db) -> AsyncGenerator:
    """Create an async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
