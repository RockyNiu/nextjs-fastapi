from datetime import datetime, timedelta, timezone
from typing import Optional

from jose import JWTError, jwt

from app.common.logger import logger
from app.config import ConfigLoader


class AuthService:
    """Service for handling authentication and JWT operations"""

    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_SECONDS = 30 * 60  # 30 minutes in seconds

    def __init__(self):
        self.config = ConfigLoader.get_config()

    def create_access_token(
        self, data: dict, expires_delta: Optional[timedelta] = None
    ) -> str:
        """Create a JWT access token"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                seconds=self.ACCESS_TOKEN_EXPIRE_SECONDS
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, self.config.secret_key, algorithm=self.ALGORITHM
        )
        logger.info(f"Created access token for subject: {data.get('sub')}")
        return encoded_jwt

    def verify_token(self, token: str) -> Optional[str]:
        """Verify JWT token and return email subject"""
        try:
            payload = jwt.decode(
                token, self.config.secret_key, algorithms=[self.ALGORITHM]
            )
            email = payload.get("sub")
            if email is None:
                logger.warning("Token verification failed: no subject in payload")
                return None
            logger.info(f"Token verified for user: {email}")
            return email
        except JWTError as e:
            logger.warning(f"Token verification failed: {e}")
            return None
