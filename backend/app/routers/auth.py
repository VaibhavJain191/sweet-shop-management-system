"""
Authentication routes for user registration and login.
"""
from fastapi import APIRouter, status
from app.schemas.user import UserRegister, UserLogin, UserResponse, Token
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        
    Returns:
        Created user (without password)
    """
    user = await register_user(user_data)
    return UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        role=user.role,
        created_at=user.created_at
    )


@router.post("/login", response_model=Token)
async def login(login_data: UserLogin):
    """
    Login user and return JWT token.
    
    Args:
        login_data: User login credentials
        
    Returns:
        JWT access token
    """
    return await login_user(login_data)
