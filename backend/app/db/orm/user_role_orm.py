from enum import IntEnum
from typing import List, Optional

from app.db.orm.ref_base_orm import RefBaseORM


class UserRole(IntEnum):
    USER = 1
    MODERATOR = 2
    ADMIN = 3

    @classmethod
    def from_str(cls, role_name: str) -> Optional["UserRole"]:
        """Convert a role name string to UserRole enum.

        Args:
            role_name: Role name (case-insensitive). Valid values: 'user', 'moderator', 'admin'

        Returns:
            UserRole enum value if valid, None if invalid.

        Example:
            >>> UserRole.from_str('admin')
            <UserRole.ADMIN: 3>
            >>> UserRole.from_str('MODERATOR')
            <UserRole.MODERATOR: 2>
            >>> UserRole.from_str('invalid')
            None
        """
        role_map = {
            "user": cls.USER,
            "moderator": cls.MODERATOR,
            "admin": cls.ADMIN,
        }
        return role_map.get(role_name.lower())

    @classmethod
    def valid_names(cls) -> List[str]:
        """Get list of valid role names.

        Returns:
            List of valid role name strings in lowercase.

        Example:
            >>> UserRole.valid_names()
            ['user', 'moderator', 'admin']
        """
        return [role.name.lower() for role in cls]


class RefUserRole(RefBaseORM[UserRole]):
    __tablename__ = "ref_user_role"
