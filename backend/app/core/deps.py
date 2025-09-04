from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.db.dao.user_dao import UserDAO
from app.core.security import verify_token
from app.entities.user import UserResponse

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> UserResponse:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    email = verify_token(token)
    
    if email is None:
        raise credentials_exception
    
    user_dao = UserDAO()
    user = user_dao.get_by_email(email=email)
    
    if user is None:
        raise credentials_exception
    
    return UserResponse.model_validate(user)


def get_current_active_user(
    current_user: UserResponse = Depends(get_current_user)
) -> UserResponse:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Inactive user"
        )
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)
) -> Optional[UserResponse]:
    if not credentials:
        return None
    
    token = credentials.credentials
    email = verify_token(token)
    
    if email is None:
        return None
    
    user_dao = UserDAO()
    user = user_dao.get_by_email(email=email)
    
    if user is None:
        return None
    
    return UserResponse.model_validate(user)