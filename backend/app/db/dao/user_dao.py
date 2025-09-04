from typing import Optional
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.base_dao import BaseDAO
from app.db.orm.user_orm import UserORM
from app.entities.user import UserCreate
from app.core.security import get_password_hash, verify_password, generate_password_reset_token, generate_email_verification_token


class UserDAO(BaseDAO):
    def __init__(self, db: Optional[Session] = None):
        super().__init__(db)

    def get_by_email(self, email: str) -> Optional[UserORM]:
        return self.session.query(UserORM).filter(UserORM.email == email).first()

    def create_user(self, user_create: UserCreate) -> UserORM:
        hashed_password = get_password_hash(user_create.password)
        db_user = UserORM(
            email=user_create.email,
            hashed_password=hashed_password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            is_active=user_create.is_active,
            email_verification_token=generate_email_verification_token(),
        )
        self.session.add(db_user)
        self.session.flush()  # Flush to get the ID without committing
        return db_user

    def authenticate(self, email: str, password: str) -> Optional[UserORM]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, str(user.hashed_password)):
            return None
        return user

    def is_active(self, user: UserORM) -> bool:
        return bool(user.is_active)

    def set_password_reset_token(self, user: UserORM) -> str:
        token = generate_password_reset_token()
        user.password_reset_token = token  # type: ignore
        user.password_reset_expires = datetime.now(timezone.utc) + timedelta(hours=1)  # type: ignore
        return token

    def reset_password_by_token(self, token: str, new_password: str) -> Optional[UserORM]:
        user = self.session.query(UserORM).filter(
            and_(
                UserORM.password_reset_token == token,
                UserORM.password_reset_expires > datetime.now(timezone.utc)
            )
        ).first()
        
        if not user:
            return None
            
        user.hashed_password = get_password_hash(new_password)  # type: ignore
        user.password_reset_token = None  # type: ignore
        user.password_reset_expires = None  # type: ignore
        return user

    def verify_email(self, token: str) -> Optional[UserORM]:
        user = self.session.query(UserORM).filter(
            UserORM.email_verification_token == token
        ).first()
        
        if not user:
            return None
            
        user.email_verified = True  # type: ignore
        user.email_verification_token = None  # type: ignore
        return user