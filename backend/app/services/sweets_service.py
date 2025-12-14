"""
Sweets service for CRUD operations and inventory management.
"""
from typing import List, Optional
from fastapi import HTTPException, status
from beanie import PydanticObjectId
from app.models.sweet import Sweet
from app.schemas.sweet import SweetCreate, SweetUpdate


async def create_sweet(sweet_data: SweetCreate) -> Sweet:
    """
    Create a new sweet.
    
    Args:
        sweet_data: Sweet creation data
        
    Returns:
        Created sweet document
    """
    sweet = Sweet(**sweet_data.model_dump())
    await sweet.insert()
    return sweet


async def get_all_sweets() -> List[Sweet]:
    """
    Get all sweets.
    
    Returns:
        List of all sweets
    """
    return await Sweet.find_all().to_list()


async def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
) -> List[Sweet]:
    """
    Search sweets by various criteria.
    
    Args:
        name: Filter by name (case-insensitive partial match)
        category: Filter by category (case-insensitive partial match)
        min_price: Minimum price filter
        max_price: Maximum price filter
        
    Returns:
        List of matching sweets
    """
    query = {}
    
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    
    if category:
        query["category"] = {"$regex": category, "$options": "i"}
    
    if min_price is not None or max_price is not None:
        price_query = {}
        if min_price is not None:
            price_query["$gte"] = min_price
        if max_price is not None:
            price_query["$lte"] = max_price
        query["price"] = price_query
    
    return await Sweet.find(query).to_list()


async def get_sweet_by_id(sweet_id: str) -> Sweet:
    """
    Get sweet by ID.
    
    Args:
        sweet_id: Sweet ID
        
    Returns:
        Sweet document
        
    Raises:
        HTTPException: If sweet not found
    """
    try:
        sweet = await Sweet.get(PydanticObjectId(sweet_id))
        if not sweet:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Sweet not found"
            )
        return sweet
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sweet not found"
        )


async def update_sweet(sweet_id: str, sweet_data: SweetUpdate) -> Sweet:
    """
    Update a sweet.
    
    Args:
        sweet_id: Sweet ID
        sweet_data: Sweet update data
        
    Returns:
        Updated sweet document
        
    Raises:
        HTTPException: If sweet not found
    """
    sweet = await get_sweet_by_id(sweet_id)
    
    # Update only provided fields
    update_data = sweet_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(sweet, field, value)
    
    await sweet.save()
    return sweet


async def delete_sweet(sweet_id: str) -> dict:
    """
    Delete a sweet.
    
    Args:
        sweet_id: Sweet ID
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If sweet not found
    """
    sweet = await get_sweet_by_id(sweet_id)
    await sweet.delete()
    return {"message": "Sweet deleted successfully"}


async def purchase_sweet(sweet_id: str, quantity: int) -> Sweet:
    """
    Purchase a sweet (decrease quantity).
    
    Args:
        sweet_id: Sweet ID
        quantity: Quantity to purchase
        
    Returns:
        Updated sweet document
        
    Raises:
        HTTPException: If sweet not found or insufficient quantity
    """
    sweet = await get_sweet_by_id(sweet_id)
    
    if sweet.quantity < quantity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient quantity. Available: {sweet.quantity}, Requested: {quantity}"
        )
    
    sweet.quantity -= quantity
    await sweet.save()
    return sweet


async def restock_sweet(sweet_id: str, quantity: int) -> Sweet:
    """
    Restock a sweet (increase quantity).
    
    Args:
        sweet_id: Sweet ID
        quantity: Quantity to add
        
    Returns:
        Updated sweet document
        
    Raises:
        HTTPException: If sweet not found
    """
    sweet = await get_sweet_by_id(sweet_id)
    sweet.quantity += quantity
    await sweet.save()
    return sweet
