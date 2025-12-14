"""
Authentication service for user registration and login.
"""
from typing import Optional
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserRegister, UserLogin, Token
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token


async def register_user(user_data: UserRegister) -> User:
    """
    Register a new user.
    
    Args:
        user_data: User registration data
        
    Returns:
        Created user document
        
    Raises:
        HTTPException: If email is already registered
    """
    # Check if user already exists
    existing_user = await User.find_one(User.email == user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Hash the password
    password_hash = hash_password(user_data.password)
    
    # Create new user
    user = User(
        email=user_data.email,
        password_hash=password_hash,
        name=user_data.name
    )
    
    await user.insert()
    return user


async def login_user(login_data: UserLogin) -> Token:
    """
    Authenticate user and return JWT token.
    
    Args:
        login_data: User login credentials
        
    Returns:
        JWT access token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    # Find user by email
    user = await User.find_one(User.email == login_data.email)
    
    if not user or not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}
    )
    
    return Token(access_token=access_token)


async def get_user_by_email(email: str) -> Optional[User]:
    """
    Get user by email.
    
    Args:
        email: User email
        
    Returns:
        User document or None if not found
    """
    return await User.find_one(User.email == email)
