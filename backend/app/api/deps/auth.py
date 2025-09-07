from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.entities.user import User
from app.service.user_service import UserService

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    user_service = UserService()
    user = user_service.get_user_by_token(token)

    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
) -> Optional[User]:
    if not credentials:
        return None

    token = credentials.credentials
    user_service = UserService()
    return user_service.get_user_by_token(token)
