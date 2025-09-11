from enum import IntEnum

from app.db.orm.ref_base_orm import RefBaseORM


class UserRole(IntEnum):
    USER = 1
    MODERATOR = 2
    ADMIN = 3


class RefUserRole(RefBaseORM[UserRole]):
    __tablename__ = "ref_user_role"
