from datetime import datetime, timedelta, timezone
from typing import Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.core.security import (
    generate_email_verification_token,
    generate_password_reset_token,
    get_password_hash,
    verify_password,
)
from app.db.dao.base_dao import BaseDAO
from app.db.orm.user_orm import UserORM
from app.entities.user import User, UserCreate


class UserDAO(BaseDAO):
    def __init__(self, db: Optional[Session] = None):
        super().__init__(db)

    def get_by_email(self, email: str) -> Optional[User]:
        user_orm = self.session.query(UserORM).filter(UserORM.email == email).first()
        if user_orm:
            return User.model_validate(user_orm)
        return None

    def create_user(self, user_create: UserCreate) -> User:
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
        return User.model_validate(db_user)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        stmt = select(UserORM).where(UserORM.email == email)
        user_orm = self.session.execute(stmt).scalar_one_or_none()
        if not user_orm or user_orm.hashed_password is None:
            return None
        if not verify_password(password, str(user_orm.hashed_password)):
            return None
        return User.model_validate(user_orm)

    def is_active(self, user: User) -> bool:
        return user.is_active

    def set_password_reset_token(self, email: str) -> str:
        user_orm = self.session.query(UserORM).filter(UserORM.email == email).first()
        if not user_orm:
            raise ValueError(f"User with email {email} not found")

        token = generate_password_reset_token()
        user_orm.password_reset_token = token  # type: ignore
        user_orm.password_reset_expires = datetime.now(timezone.utc) + timedelta(
            hours=1
        )  # type: ignore
        return token

    def reset_password_by_token(self, token: str, new_password: str) -> Optional[User]:
        user = (
            self.session.query(UserORM)
            .filter(
                and_(
                    UserORM.password_reset_token == token,
                    UserORM.password_reset_expires > datetime.now(timezone.utc),
                )
            )
            .first()
        )

        if not user:
            return None

        user.hashed_password = get_password_hash(new_password)  # type: ignore
        user.password_reset_token = None  # type: ignore
        user.password_reset_expires = None  # type: ignore
        return User.model_validate(user)

    def verify_email(self, token: str) -> Optional[User]:
        user = (
            self.session.query(UserORM)
            .filter(UserORM.email_verification_token == token)
            .first()
        )

        if not user:
            return None

        user.email_verified = True  # type: ignore
        user.email_verification_token = None  # type: ignore
        return User.model_validate(user)
