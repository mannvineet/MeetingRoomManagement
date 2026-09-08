from fastapi import HTTPException

from app.models.user_role import UserRole
from app.services.auth_service import AuthService
from app.models.db.users import Users


class UserService:
    def __init__(self, repository):
        self.repository = repository

    async def create_user(self, data):
        if not data.name.strip():
            raise HTTPException(400, "Name is required")

        if not data.email.strip():
            raise HTTPException(400, "Email is required")

        if len(data.password) < 6:
            raise HTTPException(
                400,
                "Password must be at least 6 characters"
            )

        if data.role not in [role.value for role in UserRole]:
            raise HTTPException(400, "Invalid role")

        if await self.repository.get_by_email(data.email):
            raise HTTPException(409, "Email already exists")

        user = Users(
            name=data.name,
            email=data.email,
            role=data.role,
            hashed_password=AuthService.hash_password(data.password)
        )

        return await self.repository.create(user)

    async def get_users(self):
        return await self.repository.get_all()

    async def get_user(self, user_id: int):
        user = await self.repository.get_by_id(user_id)

        if user is None:
            raise HTTPException(404, "User not found")

        return user

    async def update_user(self, user_id: int, data):
        user = await self.get_user(user_id)

        if data.name is not None:
            if not data.name.strip():
                raise HTTPException(400, "Name is required")

            user.name = data.name

        if data.role is not None:
            if data.role not in [role.value for role in UserRole]:
                raise HTTPException(400, "Invalid role")

            user.role = data.role

        return await self.repository.update(user)

    async def delete_user(self, user_id: int):
        user = await self.get_user(user_id)
        await self.repository.delete(user)
