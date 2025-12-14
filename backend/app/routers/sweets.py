"""
Sweets routes for CRUD operations and inventory management.
"""
from fastapi import APIRouter, Depends, status
from typing import List, Optional
from app.schemas.sweet import SweetCreate, SweetUpdate, SweetResponse, PurchaseRequest, RestockRequest
from app.services import sweets_service
from app.middleware.auth import get_current_user, get_current_admin
from app.models.user import User

router = APIRouter(prefix="/api/sweets", tags=["Sweets"])


@router.post("", response_model=SweetResponse, status_code=status.HTTP_201_CREATED)
async def create_sweet(
    sweet_data: SweetCreate,
    current_user: User = Depends(get_current_user)
):
    """
    Create a new sweet (protected route).
    
    Args:
        sweet_data: Sweet creation data
        current_user: Current authenticated user
        
    Returns:
        Created sweet
    """
    sweet = await sweets_service.create_sweet(sweet_data)
    return SweetResponse(
        id=str(sweet.id),
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity,
        description=sweet.description,
        image_url=sweet.image_url,
        created_at=sweet.created_at,
        updated_at=sweet.updated_at
    )


@router.get("", response_model=List[SweetResponse])
async def get_all_sweets(current_user: User = Depends(get_current_user)):
    """
    Get all sweets (protected route).
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        List of all sweets
    """
    sweets = await sweets_service.get_all_sweets()
    return [
        SweetResponse(
            id=str(sweet.id),
            name=sweet.name,
            category=sweet.category,
            price=sweet.price,
            quantity=sweet.quantity,
            description=sweet.description,
            image_url=sweet.image_url,
            created_at=sweet.created_at,
            updated_at=sweet.updated_at
        )
        for sweet in sweets
    ]


@router.get("/search", response_model=List[SweetResponse])
async def search_sweets(
    name: Optional[str] = None,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    current_user: User = Depends(get_current_user)
):
    """
    Search sweets by various criteria (protected route).
    
    Args:
        name: Filter by name
        category: Filter by category
        min_price: Minimum price
        max_price: Maximum price
        current_user: Current authenticated user
        
    Returns:
        List of matching sweets
    """
    sweets = await sweets_service.search_sweets(name, category, min_price, max_price)
    return [
        SweetResponse(
            id=str(sweet.id),
            name=sweet.name,
            category=sweet.category,
            price=sweet.price,
            quantity=sweet.quantity,
            description=sweet.description,
            image_url=sweet.image_url,
            created_at=sweet.created_at,
            updated_at=sweet.updated_at
        )
        for sweet in sweets
    ]


@router.put("/{sweet_id}", response_model=SweetResponse)
async def update_sweet(
    sweet_id: str,
    sweet_data: SweetUpdate,
    current_user: User = Depends(get_current_user)
):
    """
    Update a sweet (protected route).
    
    Args:
        sweet_id: Sweet ID
        sweet_data: Sweet update data
        current_user: Current authenticated user
        
    Returns:
        Updated sweet
    """
    sweet = await sweets_service.update_sweet(sweet_id, sweet_data)
    return SweetResponse(
        id=str(sweet.id),
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity,
        description=sweet.description,
        image_url=sweet.image_url,
        created_at=sweet.created_at,
        updated_at=sweet.updated_at
    )


@router.delete("/{sweet_id}")
async def delete_sweet(
    sweet_id: str,
    current_admin: User = Depends(get_current_admin)
):
    """
    Delete a sweet (admin only).
    
    Args:
        sweet_id: Sweet ID
        current_admin: Current admin user
        
    Returns:
        Success message
    """
    return await sweets_service.delete_sweet(sweet_id)


@router.post("/{sweet_id}/purchase", response_model=SweetResponse)
async def purchase_sweet(
    sweet_id: str,
    purchase_data: PurchaseRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Purchase a sweet (protected route).
    
    Args:
        sweet_id: Sweet ID
        purchase_data: Purchase quantity
        current_user: Current authenticated user
        
    Returns:
        Updated sweet with decreased quantity
    """
    sweet = await sweets_service.purchase_sweet(sweet_id, purchase_data.quantity)
    return SweetResponse(
        id=str(sweet.id),
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity,
        description=sweet.description,
        image_url=sweet.image_url,
        created_at=sweet.created_at,
        updated_at=sweet.updated_at
    )


@router.post("/{sweet_id}/restock", response_model=SweetResponse)
async def restock_sweet(
    sweet_id: str,
    restock_data: RestockRequest,
    current_admin: User = Depends(get_current_admin)
):
    """
    Restock a sweet (admin only).
    
    Args:
        sweet_id: Sweet ID
        restock_data: Restock quantity
        current_admin: Current admin user
        
    Returns:
        Updated sweet with increased quantity
    """
    sweet = await sweets_service.restock_sweet(sweet_id, restock_data.quantity)
    return SweetResponse(
        id=str(sweet.id),
        name=sweet.name,
        category=sweet.category,
        price=sweet.price,
        quantity=sweet.quantity,
        description=sweet.description,
        image_url=sweet.image_url,
        created_at=sweet.created_at,
        updated_at=sweet.updated_at
    )
