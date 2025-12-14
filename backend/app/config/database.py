"""
Database configuration and initialization for MongoDB with Beanie ODM.
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "sweet_shop"
    secret_key: str = "your-secret-key-change-this-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# MongoDB client
mongo_client: Optional[AsyncIOMotorClient] = None


async def connect_to_mongo():
    """Initialize MongoDB connection and Beanie ODM."""
    global mongo_client
    
    # Import models here to avoid circular imports
    from app.models.user import User
    from app.models.sweet import Sweet
    
    mongo_client = AsyncIOMotorClient(settings.mongodb_url)
    database = mongo_client[settings.database_name]
    
    await init_beanie(
        database=database,
        document_models=[User, Sweet]
    )
    
    print(f"Connected to MongoDB: {settings.database_name}")


async def close_mongo_connection():
    """Close MongoDB connection."""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("Closed MongoDB connection")
