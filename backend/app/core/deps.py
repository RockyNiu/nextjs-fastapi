from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.security import verify_token
from app.db.dao.user_dao import UserDAO
from app.entities.user import User

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
    email = verify_token(token)

    if email is None:
        raise credentials_exception

    user_dao = UserDAO()
    user = user_dao.get_by_email(email=email)

    if user is None:
        raise credentials_exception

    return User.model_validate(user)


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
    email = verify_token(token)

    if email is None:
        return None

    user_dao = UserDAO()
    user = user_dao.get_by_email(email=email)

    if user is None:
        return None

    return User.model_validate(user)
