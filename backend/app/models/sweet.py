"""
Sweet document model for MongoDB using Beanie ODM.
"""
from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Optional


class Sweet(Document):
    """Sweet document model."""
    
    name: str
    category: str
    price: float = Field(gt=0)  # Price must be greater than 0
    quantity: int = Field(default=0, ge=0)  # Quantity must be >= 0
    description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "sweets"
        
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Chocolate Bar",
                "category": "Chocolate",
                "price": 2.99,
                "quantity": 100,
                "description": "Delicious milk chocolate bar",
                "image_url": "https://example.com/chocolate.jpg"
            }
        }
