"""
Pydantic schemas for sweet-related requests and responses.
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class SweetCreate(BaseModel):
    """Schema for creating a new sweet."""
    name: str = Field(min_length=1, description="Sweet name is required")
    category: str = Field(min_length=1, description="Category is required")
    price: float = Field(gt=0, description="Price must be greater than 0")
    quantity: int = Field(default=0, ge=0, description="Quantity must be >= 0")
    description: Optional[str] = None
    image_url: Optional[str] = None


class SweetUpdate(BaseModel):
    """Schema for updating a sweet."""
    name: Optional[str] = Field(None, min_length=1)
    category: Optional[str] = Field(None, min_length=1)
    price: Optional[float] = Field(None, gt=0)
    quantity: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    image_url: Optional[str] = None


class SweetResponse(BaseModel):
    """Schema for sweet response."""
    id: str
    name: str
    category: str
    price: float
    quantity: int
    description: Optional[str] = None
    image_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PurchaseRequest(BaseModel):
    """Schema for purchasing a sweet."""
    quantity: int = Field(gt=0, description="Purchase quantity must be greater than 0")


class RestockRequest(BaseModel):
    """Schema for restocking a sweet."""
    quantity: int = Field(gt=0, description="Restock quantity must be greater than 0")
