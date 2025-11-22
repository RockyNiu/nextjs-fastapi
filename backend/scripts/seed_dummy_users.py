#!/usr/bin/env python
"""
Seed dummy users for testing purposes.

All dummy users will have emails ending with @dummyuser.com to make them easy to identify
and clean up later. This script is idempotent - running it multiple times won't create
duplicate users.

Usage:
    uv run python scripts/seed_dummy_users.py
    # or via just command:
    just seed-users
"""

import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import database_context
from app.db.orm.user_role_orm import UserRole
from app.entities.user import UserCreate
from app.exceptions.user_exceptions import UserAlreadyExistsError
from app.service.user_service import UserService

# Dummy user domain - used to identify dummy users for cleanup
DUMMY_DOMAIN = "@dummyuser.com"

# Default password for all dummy users
DEFAULT_PASSWORD = "DummyPass123!"

# Dummy users to create
DUMMY_USERS = [
    # Regular users
    {
        "email": "john.doe@dummyuser.com",
        "first_name": "John",
        "last_name": "Doe",
        "role_id": UserRole.USER,
        "is_active": True,
        "email_verified": True,
    },
    {
        "email": "jane.smith@dummyuser.com",
        "first_name": "Jane",
        "last_name": "Smith",
        "role_id": UserRole.USER,
        "is_active": True,
        "email_verified": True,
    },
    {
        "email": "bob.wilson@dummyuser.com",
        "first_name": "Bob",
        "last_name": "Wilson",
        "role_id": UserRole.USER,
        "is_active": True,
        "email_verified": False,
    },
    {
        "email": "alice.johnson@dummyuser.com",
        "first_name": "Alice",
        "last_name": "Johnson",
        "role_id": UserRole.USER,
        "is_active": False,  # Inactive user
        "email_verified": True,
    },
    {
        "email": "charlie.brown@dummyuser.com",
        "first_name": "Charlie",
        "last_name": "Brown",
        "role_id": UserRole.USER,
        "is_active": True,
        "email_verified": True,
    },
    # Moderators
    {
        "email": "mod.sarah@dummyuser.com",
        "first_name": "Sarah",
        "last_name": "Moderator",
        "role_id": UserRole.MODERATOR,
        "is_active": True,
        "email_verified": True,
    },
    {
        "email": "mod.mike@dummyuser.com",
        "first_name": "Mike",
        "last_name": "Moderator",
        "role_id": UserRole.MODERATOR,
        "is_active": True,
        "email_verified": True,
    },
    # Admin
    {
        "email": "admin.test@dummyuser.com",
        "first_name": "Test",
        "last_name": "Admin",
        "role_id": UserRole.ADMIN,
        "is_active": True,
        "email_verified": True,
    },
    # Additional regular users for pagination testing
    {
        "email": "user1@dummyuser.com",
        "first_name": "User",
        "last_name": "One",
        "role_id": UserRole.USER,
        "is_active": True,
        "email_verified": True,
    },
    {
        "email": "user2@dummyuser.com",
        "first_name": "User",
        "last_name": "Two",
        "role_id": UserRole.USER,
        "is_active": True,
        "email_verified": True,
    },
    {
        "email": "user3@dummyuser.com",
        "first_name": "User",
        "last_name": "Three",
        "role_id": UserRole.USER,
        "is_active": True,
        "email_verified": True,
    },
    {
        "email": "user4@dummyuser.com",
        "first_name": "User",
        "last_name": "Four",
        "role_id": UserRole.USER,
        "is_active": True,
        "email_verified": True,
    },
    {
        "email": "user5@dummyuser.com",
        "first_name": "User",
        "last_name": "Five",
        "role_id": UserRole.USER,
        "is_active": False,
        "email_verified": True,
    },
]


def seed_dummy_users():
    """Seed dummy users into the database."""
    with database_context():
        user_service = UserService()
        created_count = 0
        skipped_count = 0

        for user_data in DUMMY_USERS:
            # Create UserCreate object
            user_create = UserCreate(
                email=user_data["email"],
                first_name=user_data["first_name"],
                last_name=user_data["last_name"],
                password=DEFAULT_PASSWORD,
                is_active=user_data["is_active"],
                role_id=user_data["role_id"],
            )

            try:
                user_service.create_user_without_verification(
                    user_create, email_verified=user_data["email_verified"]
                )
                print(
                    f"  Created: {user_data['email']} (role: {user_data['role_id'].name})"
                )
                created_count += 1
            except UserAlreadyExistsError:
                print(f"  Skipping (exists): {user_data['email']}")
                skipped_count += 1

        print("\n" + "=" * 50)
        print("Seeding complete!")
        print(f"  Created: {created_count} users")
        print(f"  Skipped: {skipped_count} users (already exist)")
        print(f"\nDefault password for all dummy users: {DEFAULT_PASSWORD}")
        print(f"Dummy users can be identified by domain: {DUMMY_DOMAIN}")


if __name__ == "__main__":
    print("=" * 50)
    print("Seeding dummy users...")
    print("=" * 50 + "\n")
    seed_dummy_users()
