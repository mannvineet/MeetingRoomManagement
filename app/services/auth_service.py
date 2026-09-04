from fastapi import HTTPException, status

from app.core.security import (
    create_access_token,
    verify_password
)
from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def login(
        self,
        email: str,
        password: str
    ):
        user = await self.repository.get_by_email(email)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not verify_password(password,user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(user.id,user.role)

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }