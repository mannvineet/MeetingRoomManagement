from fastapi import APIRouter, Depends, status

from app.core.dependencies import (
    get_user_service,
    require_admin
)
from app.models.users import Users
from app.schemas.response import APIResponse
from app.schemas.users import (
    CreateUserRequest,
    UpdateUserRequest
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(require_admin)]
)


@router.post("",status_code=status.HTTP_201_CREATED,response_model=APIResponse)
async def create_user(data: CreateUserRequest,service: UserService = Depends(get_user_service)):

    user = await service.create_user(data)

    return {
        "success": True,
        "message": "User created successfully",
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        },
        "errors": []
    }


@router.get("",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def get_users(service: UserService = Depends(get_user_service)):

    users = await service.get_all_users()

    return {
        "success": True,
        "message": "Users retrieved successfully",
        "data": {
            "users": [
                {
                    "id": user.id,
                    "name": user.name,
                    "email": user.email,
                    "role": user.role
                }
                for user in users
            ]
        },
        "errors": []
    }


@router.get("/{user_id}",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def get_user(user_id: int,service: UserService = Depends(get_user_service)):

    user = await service.get_user(user_id)

    return {
        "success": True,
        "message": "User retrieved successfully",
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        },
        "errors": []
    }


@router.patch("/{user_id}",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def update_user(user_id: int,data: UpdateUserRequest,
        service: UserService = Depends(get_user_service)):

    user = await service.update_user(user_id, data)

    return {
        "success": True,
        "message": "User updated successfully",
        "data": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        },
        "errors": []
    }


@router.delete("/{user_id}",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def delete_user(user_id: int,service: UserService = Depends(get_user_service)):

    await service.delete_user(user_id)

    return {
        "success": True,
        "message": "User deleted successfully",
        "data": {},
        "errors": []
    }