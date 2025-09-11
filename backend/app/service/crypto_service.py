import secrets

from passlib.context import CryptContext

from app.common.logger import logger


class CryptoService:
    """Service for handling cryptographic operations"""

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain password against a hashed password"""
        result = self.pwd_context.verify(plain_password, hashed_password)
        logger.info(f"Password verification: {'success' if result else 'failed'}")
        return result

    def get_password_hash(self, password: str) -> str:
        """Hash a password"""
        hashed = self.pwd_context.hash(password)
        logger.info("Password hashed successfully")
        return hashed

    def generate_password_reset_token(self) -> str:
        """Generate a secure password reset token"""
        token = secrets.token_urlsafe(32)
        logger.info("Generated password reset token")
        return token

    def generate_email_verification_token(self) -> str:
        """Generate a secure email verification token"""
        token = secrets.token_urlsafe(32)
        logger.info("Generated email verification token")
        return token
