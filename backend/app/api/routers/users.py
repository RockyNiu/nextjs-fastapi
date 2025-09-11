from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.deps.auth import require_admin, require_moderator_or_admin
from app.api.entities.user_api import (
    ErrorResponseAPI,
    MessageResponseAPI,
    UserAPI,
    UserListResponseAPI,
    UserUpdateAPI,
)
from app.db.orm.user_role_orm import UserRole
from app.entities.user import UserUpdate
from app.service.user_service import UserService

router = APIRouter()


@router.get(
    "/",
    response_model=UserListResponseAPI,
    dependencies=[Depends(require_moderator_or_admin)],
    responses={
        200: {"description": "List of users"},
        403: {
            "model": ErrorResponseAPI,
            "description": "Forbidden - insufficient permissions",
        },
    },
    summary="List all users",
    description="Get a paginated list of all users. Requires moderator or admin role.",
)
def list_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(
        100, ge=1, le=1000, description="Maximum number of users to return"
    ),
) -> Any:
    """
    List all users with pagination.
    """
    user_service = UserService()
    users = user_service.get_all_users(skip=skip, limit=limit)

    return UserListResponseAPI(
        users=[UserAPI.model_validate(user) for user in users],
        total=len(users),
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{user_id}",
    response_model=UserAPI,
    dependencies=[Depends(require_moderator_or_admin)],
    responses={
        200: {"description": "User details"},
        403: {
            "model": ErrorResponseAPI,
            "description": "Forbidden - insufficient permissions",
        },
        404: {"model": ErrorResponseAPI, "description": "User not found"},
    },
    summary="Get user by ID",
    description="Get detailed information about a specific user. Requires moderator or admin role.",
)
def get_user(user_id: int) -> Any:
    """
    Get user by ID.
    """
    user_service = UserService()
    user = user_service.get_user_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserAPI.model_validate(user)


@router.put(
    "/{user_id}",
    response_model=UserAPI,
    dependencies=[Depends(require_admin)],
    responses={
        200: {"description": "User updated successfully"},
        400: {
            "model": ErrorResponseAPI,
            "description": "Bad request - validation error",
        },
        403: {
            "model": ErrorResponseAPI,
            "description": "Forbidden - admin access required",
        },
        404: {"model": ErrorResponseAPI, "description": "User not found"},
    },
    summary="Update user",
    description="Update user information including role assignment. Requires admin role.",
)
def update_user(user_id: int, user_update_api: UserUpdateAPI) -> Any:
    """
    Update user information.
    """
    # Convert API model to internal model
    user_update = UserUpdate(
        first_name=user_update_api.first_name,
        last_name=user_update_api.last_name,
        is_active=user_update_api.is_active,
        role_id=user_update_api.role_id,
    )

    user_service = UserService()
    updated_user = user_service.update_user(user_id, user_update)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return UserAPI.model_validate(updated_user)


@router.post(
    "/{user_id}/deactivate",
    response_model=MessageResponseAPI,
    dependencies=[Depends(require_admin)],
    responses={
        200: {"description": "User deactivated successfully"},
        403: {
            "model": ErrorResponseAPI,
            "description": "Forbidden - admin access required",
        },
        404: {"model": ErrorResponseAPI, "description": "User not found"},
    },
    summary="Deactivate user",
    description="Deactivate a user account. Requires admin role.",
)
def deactivate_user(user_id: int) -> Any:
    """
    Deactivate user account.
    """
    user_service = UserService()
    result = user_service.deactivate_user(user_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return MessageResponseAPI(message="User deactivated successfully", success=True)


@router.post(
    "/{user_id}/activate",
    response_model=MessageResponseAPI,
    dependencies=[Depends(require_admin)],
    responses={
        200: {"description": "User activated successfully"},
        403: {
            "model": ErrorResponseAPI,
            "description": "Forbidden - admin access required",
        },
        404: {"model": ErrorResponseAPI, "description": "User not found"},
    },
    summary="Activate user",
    description="Activate a user account. Requires admin role.",
)
def activate_user(user_id: int) -> Any:
    """
    Activate user account.
    """
    user_service = UserService()
    result = user_service.activate_user(user_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return MessageResponseAPI(message="User activated successfully", success=True)


@router.get(
    "/roles/",
    response_model=List[dict],
    dependencies=[Depends(require_moderator_or_admin)],
    responses={
        200: {"description": "Available user roles"},
        403: {
            "model": ErrorResponseAPI,
            "description": "Forbidden - insufficient permissions",
        },
    },
    summary="Get available roles",
    description="Get list of available user roles. Requires moderator or admin role.",
)
def get_roles() -> Any:
    """
    Get available user roles.
    """
    return [
        {"id": UserRole.USER, "name": "user", "display_name": "User"},
        {"id": UserRole.MODERATOR, "name": "moderator", "display_name": "Moderator"},
        {"id": UserRole.ADMIN, "name": "admin", "display_name": "Admin"},
    ]
