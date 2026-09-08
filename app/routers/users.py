from fastapi import APIRouter, Depends

from app.dependencies import (
    get_current_user,
    get_user_service,
    require_admin
)
from app.models.dto.response import APIResponse
from app.models.dto.users import (
    CreateUserRequest,
    UpdateUserRequest,
    UserListResponse,
    UserResponse
)
from app.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("", response_model=APIResponse)
async def create_user(
    data: CreateUserRequest,
    service: UserService = Depends(get_user_service),
    current_user=Depends(require_admin)
):
    user = await service.create_user(data)

    return APIResponse(
        success=True,
        message="User created successfully",
        data=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role
        )
    )


@router.get("", response_model=APIResponse)
async def get_users(
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user)
):
    users = await service.get_users()

    return APIResponse(
        success=True,
        message="Users fetched successfully",
        data=UserListResponse(
            users=[
                UserResponse(
                    id=user.id,
                    name=user.name,
                    email=user.email,
                    role=user.role
                )
                for user in users
            ]
        )
    )


@router.get("/{user_id}", response_model=APIResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user=Depends(get_current_user)
):
    user = await service.get_user(user_id)

    return APIResponse(
        success=True,
        message="User fetched successfully",
        data=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role
        )
    )


@router.put("/{user_id}", response_model=APIResponse)
async def update_user(
    user_id: int,
    data: UpdateUserRequest,
    service: UserService = Depends(get_user_service),
    current_user=Depends(require_admin)
):
    user = await service.update_user(user_id, data)

    return APIResponse(
        success=True,
        message="User updated successfully",
        data=UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role
        )
    )


@router.delete("/{user_id}", response_model=APIResponse)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service),
    current_user=Depends(require_admin)
):
    await service.delete_user(user_id)

    return APIResponse(
        success=True,
        message="User deleted successfully",
        data=None
    )
