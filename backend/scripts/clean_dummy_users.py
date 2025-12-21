#!/usr/bin/env python
"""
Clean up dummy users from the database.

This script only removes users with emails ending in @dummyuser.com,
leaving all manually created users intact.

Usage:
    uv run python scripts/clean_dummy_users.py
    # or via just command:
    just clean-users
"""

import sys
from pathlib import Path

# Add the backend directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.db.database import database_context
from app.service.user_service import UserService

# Dummy user domain - only users with this domain will be deleted
DUMMY_DOMAIN = "@dummyuser.com"


def clean_dummy_users(dry_run: bool = False):
    """Remove all dummy users from the database.

    Args:
        dry_run: If True, only show what would be deleted without actually deleting.
    """
    with database_context():
        user_service = UserService()

        # Find all dummy users
        dummy_users = user_service.get_users_by_email_domain(DUMMY_DOMAIN)

        if not dummy_users:
            print("No dummy users found to clean up.")
            return

        print(f"Found {len(dummy_users)} dummy user(s) to remove:\n")
        for user in dummy_users:
            print(f"  - {user.email} ({user.first_name} {user.last_name})")

        if dry_run:
            print("\n[DRY RUN] No users were deleted.")
            print("Run without --dry-run to actually delete these users.")
            return

        # Delete all dummy users
        deleted_count = 0
        for user in dummy_users:
            if user_service.delete_user(user.id):
                deleted_count += 1

        print("\n" + "=" * 50)
        print(f"Cleanup complete! Deleted {deleted_count} dummy user(s).")
        print(f"Only users with domain '{DUMMY_DOMAIN}' were removed.")
        print("All manually created users remain intact.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Clean up dummy users from the database."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deleted without actually deleting",
    )
    args = parser.parse_args()

    print("=" * 50)
    print("Cleaning dummy users...")
    print("=" * 50 + "\n")
    clean_dummy_users(dry_run=args.dry_run)
