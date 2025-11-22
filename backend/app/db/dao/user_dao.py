from datetime import datetime, timedelta, timezone
from typing import List, Optional

from sqlalchemy import and_, func, or_, select
from sqlalchemy.orm import Session

from app.db.dao.base_dao import BaseDAO
from app.db.orm.user_orm import UserORM
from app.entities.user import User, UserCreate, UserUpdate
from app.service.crypto_service import CryptoService


class UserDAO(BaseDAO):
    def __init__(self, db: Optional[Session] = None):
        super().__init__(db)
        self.crypto_service = CryptoService()

    def get_by_email(self, email: str) -> Optional[User]:
        stmt = select(UserORM).where(UserORM.email == email)
        user_orm = self.session.execute(stmt).scalar_one_or_none()
        if user_orm:
            return User.model_validate(user_orm)
        return None

    def create_user(self, user_create: UserCreate) -> User:
        hashed_password = self.crypto_service.get_password_hash(user_create.password)
        db_user = UserORM(
            email=user_create.email,
            hashed_password=hashed_password,
            first_name=user_create.first_name,
            last_name=user_create.last_name,
            is_active=user_create.is_active,
            role_id=user_create.role_id,
            email_verification_token=self.crypto_service.generate_email_verification_token(),
        )
        self.session.add(db_user)
        self.session.flush()  # Flush to get the ID without committing
        return User.model_validate(db_user)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        stmt = select(UserORM).where(UserORM.email == email)
        user_orm = self.session.execute(stmt).scalar_one_or_none()
        if not user_orm or user_orm.hashed_password is None:
            return None
        if not self.crypto_service.verify_password(
            password, str(user_orm.hashed_password)
        ):
            return None
        return User.model_validate(user_orm)

    def is_active(self, user: User) -> bool:
        return user.is_active

    def set_password_reset_token(self, email: str) -> str:
        stmt = select(UserORM).where(UserORM.email == email)
        user_orm = self.session.execute(stmt).scalar_one_or_none()
        if not user_orm:
            raise ValueError(f"User with email {email} not found")

        token = self.crypto_service.generate_password_reset_token()
        user_orm.password_reset_token = token
        user_orm.password_reset_expires = datetime.now(timezone.utc) + timedelta(
            hours=1
        )
        self.session.flush()  # Ensure changes are persisted
        return token

    def reset_password_by_token(self, token: str, new_password: str) -> Optional[User]:
        stmt = select(UserORM).where(
            and_(
                UserORM.password_reset_token == token,
                UserORM.password_reset_expires > datetime.now(timezone.utc),
            )
        )
        user = self.session.execute(stmt).scalar_one_or_none()

        if not user:
            return None

        user.hashed_password = self.crypto_service.get_password_hash(new_password)
        user.password_reset_token = None
        user.password_reset_expires = None
        self.session.flush()  # Ensure changes are persisted
        return User.model_validate(user)

    def verify_email(self, token: str) -> Optional[User]:
        # First, try to find user by verification token
        stmt = select(UserORM).where(UserORM.email_verification_token == token)
        user = self.session.execute(stmt).scalar_one_or_none()

        if user:
            # User found with token, verify them
            user.email_verified = True
            user.email_verification_token = None
            self.session.flush()  # Ensure changes are persisted
            return User.model_validate(user)

        # If not found by token, check if there's already a verified user
        # This handles the case where the token was already used
        # We can't return the user in this case because we don't know which user it was
        return None

    def get_all_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get all users with pagination."""
        stmt = select(UserORM).offset(skip).limit(limit)
        user_orms = self.session.execute(stmt).scalars().all()
        return [User.model_validate(user_orm) for user_orm in user_orms]

    def count_all(self) -> int:
        """Get total count of all users."""
        stmt = select(func.count()).select_from(UserORM)
        return self.session.execute(stmt).scalar() or 0

    def get_users_filtered(
        self,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        role_id: Optional[int] = None,
        is_active: Optional[bool] = None,
    ) -> tuple[List[User], int]:
        """Get users with filtering and pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search term for name or email (case-insensitive)
            role_id: Filter by role ID
            is_active: Filter by active status

        Returns:
            Tuple of (list of users, total count matching filters)
        """
        # Build base query
        conditions = []

        if search:
            search_term = f"%{search.lower()}%"
            conditions.append(
                or_(
                    func.lower(UserORM.email).like(search_term),
                    func.lower(UserORM.first_name).like(search_term),
                    func.lower(UserORM.last_name).like(search_term),
                )
            )

        if role_id is not None:
            conditions.append(UserORM.role_id == role_id)

        if is_active is not None:
            conditions.append(UserORM.is_active == is_active)

        # Get total count with filters
        count_stmt = select(func.count()).select_from(UserORM)
        if conditions:
            count_stmt = count_stmt.where(and_(*conditions))
        total_count = self.session.execute(count_stmt).scalar() or 0

        # Get paginated results
        query_stmt = select(UserORM)
        if conditions:
            query_stmt = query_stmt.where(and_(*conditions))
        query_stmt = query_stmt.offset(skip).limit(limit)

        user_orms = self.session.execute(query_stmt).scalars().all()
        users = [User.model_validate(user_orm) for user_orm in user_orms]

        return users, total_count

    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        stmt = select(UserORM).where(UserORM.id == user_id)
        user_orm = self.session.execute(stmt).scalar_one_or_none()
        if user_orm:
            return User.model_validate(user_orm)
        return None

    def update_user(self, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Update user information."""
        stmt = select(UserORM).where(UserORM.id == user_id)
        user_orm = self.session.execute(stmt).scalar_one_or_none()

        if not user_orm:
            return None

        # Update fields that are not None
        if user_update.first_name is not None:
            user_orm.first_name = user_update.first_name
        if user_update.last_name is not None:
            user_orm.last_name = user_update.last_name
        if user_update.is_active is not None:
            user_orm.is_active = user_update.is_active
        if user_update.role_id is not None:
            user_orm.role_id = user_update.role_id

        user_orm.date_updated = datetime.now(timezone.utc)
        self.session.flush()
        return User.model_validate(user_orm)

    def set_email_verified(self, user_id: int, verified: bool) -> Optional[User]:
        """Set the email verified status for a user."""
        stmt = select(UserORM).where(UserORM.id == user_id)
        user_orm = self.session.execute(stmt).scalar_one_or_none()

        if not user_orm:
            return None

        user_orm.email_verified = verified
        if verified:
            user_orm.email_verification_token = None
        user_orm.date_updated = datetime.now(timezone.utc)
        self.session.flush()
        return User.model_validate(user_orm)

    def get_users_by_email_domain(self, domain: str) -> List[User]:
        """Get all users with emails matching a domain pattern."""
        stmt = select(UserORM).where(UserORM.email.like(f"%{domain}"))
        user_orms = self.session.execute(stmt).scalars().all()
        return [User.model_validate(user_orm) for user_orm in user_orms]

    def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID."""
        stmt = select(UserORM).where(UserORM.id == user_id)
        user_orm = self.session.execute(stmt).scalar_one_or_none()

        if not user_orm:
            return False

        self.session.delete(user_orm)
        self.session.flush()
        return True
