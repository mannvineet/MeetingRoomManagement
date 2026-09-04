from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.users import Users
from app.repositories.user_repository import UserRepository
from app.schemas.users import (
    CreateUserRequest,
    UpdateUserRequest
)


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def create_user(self,data: CreateUserRequest):
        existing_user = await self.repository.get_by_email(data.email)

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )

        if data.role not in ["ADMIN", "USER"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Invalid role"
            )

        user = Users(
            name=data.name,
            email=data.email,
            role=data.role,
            hashed_password=hash_password(data.password)
        )

        await self.repository.create(user)
        await self.repository.db.commit()
        await self.repository.db.refresh(user)

        return user

    async def get_all_users(self):
        return await self.repository.get_all()

    async def get_user(self, user_id: int):
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        return user

    async def update_user(self,user_id: int,data: UpdateUserRequest):
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        if data.role is not None:
            if data.role not in ["ADMIN", "USER"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid role"
                )

            user.role = data.role

        if data.name is not None:
            user.name = data.name

        await self.repository.db.commit()
        await self.repository.db.refresh(user)

        return user

    async def delete_user(self, user_id: int):
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        await self.repository.delete(user)
        await self.repository.db.commit()