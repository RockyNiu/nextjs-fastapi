from typing import Optional
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.base_dao import BaseDAO
from app.db.orm.user_orm import UserORM
from app.entities.user import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, generate_password_reset_token


class UserDAO(BaseDAO[UserORM, UserCreate, UserUpdate]):
    def __init__(self, db: Session):
        super().__init__(UserORM, db)

    def get_by_email(self, email: str) -> Optional[UserORM]:
        return self.db.query(UserORM).filter(UserORM.email == email).first()

    def create_user(self, user_create: UserCreate) -> UserORM:
        hashed_password = get_password_hash(user_create.password)
        db_user = UserORM(
            email=user_create.email,
            hashed_password=hashed_password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            is_active=user_create.is_active,
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def authenticate(self, email: str, password: str) -> Optional[UserORM]:
        user = self.get_by_email(email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: UserORM) -> bool:
        return user.is_active

    def set_password_reset_token(self, user: UserORM) -> str:
        token = generate_password_reset_token()
        user.password_reset_token = token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
        self.db.commit()
        return token

    def reset_password_by_token(self, token: str, new_password: str) -> Optional[UserORM]:
        user = self.db.query(UserORM).filter(
            and_(
                UserORM.password_reset_token == token,
                UserORM.password_reset_expires > datetime.utcnow()
            )
        ).first()
        
        if not user:
            return None
            
        user.hashed_password = get_password_hash(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        self.db.commit()
        self.db.refresh(user)
        return user

    def verify_email(self, token: str) -> Optional[UserORM]:
        user = self.db.query(UserORM).filter(
            UserORM.email_verification_token == token
        ).first()
        
        if not user:
            return None
            
        user.email_verified = True
        user.email_verification_token = None
        self.db.commit()
        self.db.refresh(user)
        return user