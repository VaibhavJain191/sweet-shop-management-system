"""
User document model for MongoDB using Beanie ODM.
"""
from beanie import Document, Indexed
from pydantic import EmailStr, Field
from datetime import datetime
from typing import Optional


class User(Document):
    """User document model."""
    
    email: Indexed(EmailStr, unique=True)  # type: ignore
    password_hash: str
    name: str
    role: str = Field(default="user")  # "user" or "admin"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"
        
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "role": "user"
            }
        }
